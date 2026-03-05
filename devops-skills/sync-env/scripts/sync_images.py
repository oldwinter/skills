#!/usr/bin/env python3
"""
Sync image tags between environments (CI -> Staging -> Production).

Default: sync from CI to Staging.

Usage:
    python sync_images.py --diff
    python sync_images.py --all [--target staging|prod|all] [--dry-run]
    python sync_images.py --images front,agent [--target staging|prod|all] [--dry-run]

Options:
    --diff          Show image tag differences between environments
    --images        Comma-separated image names to sync (partial match)
    --all           Sync all images
    --dry-run       Show changes without modifying files
    --target        Target environment: staging (default), prod, or all
    --source        Source environment: ci (default) or staging (only for --target prod)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


OVERLAY_MAP = {
    "ci": "aws-ci",
    "staging": "aws-staging",
    "prod": "aws-prod",
}


def find_gitops_root() -> Path:
    """查找 simplex-gitops 仓库根目录。"""
    candidates = [
        Path.cwd(),
        Path.cwd() / "simplex-gitops",
        Path.home() / "Code" / "all-code-in-mba" / "simplex-gitops",
    ]

    for candidate in candidates:
        if (candidate / "kubernetes" / "overlays").exists():
            return candidate

    current = Path.cwd()
    while current != current.parent:
        if (current / "kubernetes" / "overlays").exists():
            return current
        current = current.parent

    raise FileNotFoundError("无法找到 simplex-gitops 仓库根目录")


def kustomization_path(root: Path, env: str) -> Path:
    overlay = OVERLAY_MAP[env]
    return root / "kubernetes" / "overlays" / overlay / "kustomization.yaml"


def parse_images_section(content: str) -> Tuple[Dict[str, dict], int, int]:
    """从 kustomization.yaml 解析 images 部分。"""
    lines = content.split("\n")
    images: Dict[str, dict] = {}
    in_images_section = False
    images_start = -1
    images_end = -1
    current_image: str | None = None

    for i, line in enumerate(lines):
        if re.match(r"^images:\s*(#.*)?$", line):
            in_images_section = True
            images_start = i
            continue

        if in_images_section:
            stripped = line.strip()
            if (
                line
                and not line.startswith(" ")
                and not line.startswith("-")
                and not stripped.startswith("#")
                and ":" in line
            ):
                images_end = i
                break

            name_match = re.match(r"^\s*-\s*name:\s*(.+)$", line)
            if name_match:
                current_image = name_match.group(1).strip()
                images[current_image] = {"name": current_image}
                continue

            if current_image:
                new_name_match = re.match(r"^\s+newName:\s*(.+)$", line)
                if new_name_match:
                    images[current_image]["newName"] = new_name_match.group(1).strip()
                    continue

                new_tag_match = re.match(r"^\s+newTag:\s*(.+)$", line)
                if new_tag_match:
                    images[current_image]["newTag"] = new_tag_match.group(1).strip()
                    continue

    if images_end == -1:
        images_end = len(lines)

    return images, images_start, images_end


def extract_service_name(image_name: str) -> str:
    """从完整镜像路径提取服务名称。"""
    parts = image_name.split("/")
    return parts[-1] if parts else image_name


def build_service_lookup(images: Dict[str, dict]) -> Dict[str, dict]:
    """按服务名称构建查找表（优先 ECR 镜像）。"""
    by_service: Dict[str, dict] = {}
    for name, info in images.items():
        service = extract_service_name(name)
        if "ecr" in name or service not in by_service:
            by_service[service] = {"full_name": name, **info}
    return by_service


def compare_images(
    src_images: Dict[str, dict],
    dst_images: Dict[str, dict],
    src_label: str,
    dst_label: str,
) -> List[dict]:
    """比较源和目标环境的镜像。"""
    differences = []
    src_by_svc = build_service_lookup(src_images)
    dst_by_svc = build_service_lookup(dst_images)
    all_services = sorted(set(src_by_svc) | set(dst_by_svc))

    for service in all_services:
        src_info = src_by_svc.get(service)
        dst_info = dst_by_svc.get(service)

        if src_info and dst_info:
            src_tag = src_info.get("newTag", "N/A")
            dst_tag = dst_info.get("newTag", "N/A")
            if src_tag != dst_tag:
                differences.append(
                    {
                        "service": service,
                        "src_image": src_info["full_name"],
                        "src_tag": src_tag,
                        "dst_image": dst_info["full_name"],
                        "dst_tag": dst_tag,
                        "status": "different",
                    }
                )
            else:
                differences.append(
                    {
                        "service": service,
                        "src_tag": src_tag,
                        "dst_tag": dst_tag,
                        "status": "same",
                    }
                )
        elif src_info:
            differences.append(
                {
                    "service": service,
                    "src_image": src_info["full_name"],
                    "src_tag": src_info.get("newTag", "N/A"),
                    "status": "src_only",
                }
            )
        elif dst_info:
            differences.append(
                {
                    "service": service,
                    "dst_image": dst_info["full_name"],
                    "dst_tag": dst_info.get("newTag", "N/A"),
                    "status": "dst_only",
                }
            )

    return differences


def update_target_images(
    target_content: str,
    src_images: Dict[str, dict],
    target_services: Optional[List[str]] = None,
) -> Tuple[str, List[dict]]:
    """用源环境镜像标签更新目标 kustomization。"""
    changes: List[dict] = []
    lines = target_content.split("\n")
    src_by_svc = build_service_lookup(src_images)

    current_image: str | None = None
    current_service: str | None = None

    for i, line in enumerate(lines):
        name_match = re.match(r"^(\s*)-\s*name:\s*(.+)$", line)
        if name_match:
            current_image = name_match.group(2).strip()
            current_service = extract_service_name(current_image)
            continue

        if current_service:
            tag_match = re.match(r"^(\s+)newTag:\s*(.+)$", line)
            if tag_match:
                indent = tag_match.group(1)
                old_tag = tag_match.group(2).strip()

                if target_services is None or any(
                    t.lower() in current_service.lower() for t in target_services
                ):
                    src_info = src_by_svc.get(current_service)
                    if src_info and "newTag" in src_info:
                        new_tag = src_info["newTag"]
                        if old_tag != new_tag:
                            lines[i] = f"{indent}newTag: {new_tag}"
                            changes.append(
                                {
                                    "service": current_service,
                                    "image": current_image,
                                    "old_tag": old_tag,
                                    "new_tag": new_tag,
                                }
                            )

    return "\n".join(lines), changes


def print_diff(differences: List[dict], src_label: str, dst_label: str):
    """打印格式化的差异表。"""
    print("\n" + "=" * 80)
    print(f"镜像标签比较：{src_label} vs {dst_label}")
    print("=" * 80)

    different = [d for d in differences if d["status"] == "different"]
    same = [d for d in differences if d["status"] == "same"]
    src_only = [d for d in differences if d["status"] == "src_only"]
    dst_only = [d for d in differences if d["status"] == "dst_only"]

    if different:
        print(f"\n🔄 标签不同 ({len(different)} 个服务):")
        print("-" * 80)
        print(f"{'服务':<30} {src_label + ' 标签':<25} {dst_label + ' 标签':<25}")
        print("-" * 80)
        for d in different:
            print(f"{d['service']:<30} {d['src_tag']:<25} {d['dst_tag']:<25}")

    if same:
        print(f"\n✅ 标签相同 ({len(same)} 个服务):")
        print("-" * 80)
        for d in same:
            print(f"  {d['service']}: {d['src_tag']}")

    if src_only:
        print(f"\n⚠️  仅 {src_label} ({len(src_only)} 个服务):")
        for d in src_only:
            print(f"  {d['service']}: {d['src_tag']}")

    if dst_only:
        print(f"\n⚠️  仅 {dst_label} ({len(dst_only)} 个服务):")
        for d in dst_only:
            print(f"  {d['service']}: {d['dst_tag']}")

    print("\n" + "=" * 80)


def sync_one_target(
    root: Path,
    source: str,
    target: str,
    src_images: Dict[str, dict],
    target_services: Optional[List[str]],
    dry_run: bool,
) -> bool:
    """同步一个目标环境。返回是否有变更。"""
    src_label = source.upper()
    dst_label = target.upper()

    target_path = kustomization_path(root, target)
    if not target_path.exists():
        print(f"错误: 未找到 {dst_label} kustomization: {target_path}", file=sys.stderr)
        return False

    target_content = target_path.read_text()
    target_images, _, _ = parse_images_section(target_content)

    differences = compare_images(src_images, target_images, src_label, dst_label)
    print_diff(differences, src_label, dst_label)

    updated_content, changes = update_target_images(
        target_content, src_images, target_services
    )

    if not changes:
        print(f"\n✅ 无需更改 - {dst_label} 已经同步!")
        return False

    print(f"\n📝 将应用到 {dst_label} 的更改 ({len(changes)} 个更新):")
    print("-" * 60)
    for change in changes:
        print(f"  {change['service']}:")
        print(f"    {change['old_tag']} → {change['new_tag']}")

    if dry_run:
        print(f"\n🔍 DRY RUN ({dst_label}) - 未写入更改")
        return False

    target_path.write_text(updated_content)
    print(f"\n✅ 已更新 {target_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Sync image tags between environments (CI -> Staging -> Production)"
    )
    parser.add_argument("--dry-run", action="store_true", help="显示更改但不应用")
    parser.add_argument("--images", type=str, help="要同步的镜像（逗号分隔）")
    parser.add_argument("--all", action="store_true", help="同步所有镜像")
    parser.add_argument("--diff", action="store_true", help="仅显示差异")
    parser.add_argument(
        "--target",
        choices=["staging", "prod", "all"],
        default="staging",
        help="目标环境：staging（默认）、prod、all",
    )
    parser.add_argument(
        "--source",
        choices=["ci", "staging"],
        default=None,
        help="源环境：ci（默认）或 staging（仅用于 --target prod）",
    )
    args = parser.parse_args()

    # Resolve source: default is "ci"; for --target prod without explicit --source, use "staging"
    if args.source is None:
        if args.target == "prod":
            args.source = "staging"
        else:
            args.source = "ci"

    if args.source == "staging" and args.target == "staging":
        print("错误: 源和目标不能都是 staging", file=sys.stderr)
        sys.exit(1)

    try:
        root = find_gitops_root()
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    src_path = kustomization_path(root, args.source)
    if not src_path.exists():
        print(f"错误: 未找到 {args.source.upper()} kustomization: {src_path}", file=sys.stderr)
        sys.exit(1)

    src_content = src_path.read_text()
    src_images, _, _ = parse_images_section(src_content)

    # Determine targets
    if args.target == "all":
        targets = ["staging", "prod"]
    else:
        targets = [args.target]

    # Diff-only mode
    if args.diff:
        for t in targets:
            t_path = kustomization_path(root, t)
            if not t_path.exists():
                print(f"警告: 未找到 {t.upper()} kustomization: {t_path}", file=sys.stderr)
                continue
            t_content = t_path.read_text()
            t_images, _, _ = parse_images_section(t_content)
            src_label = args.source.upper()
            if args.target == "all" and t == "prod" and args.source == "ci":
                src_label = "CI"
            differences = compare_images(src_images, t_images, src_label, t.upper())
            print_diff(differences, src_label, t.upper())
        return

    # Determine target services
    target_services = None
    if args.images:
        target_services = [s.strip() for s in args.images.split(",")]
    elif not args.all:
        print("\n未指定镜像。使用 --all 同步所有，或使用 --images 指定服务。")
        print("示例: --images front,anotherme-agent,simplex-api")
        return

    any_changed = False
    for t in targets:
        # For --target all, staging uses CI as source; prod uses CI as source too
        # (user can override with --source)
        changed = sync_one_target(
            root, args.source, t, src_images, target_services, args.dry_run
        )
        if changed:
            any_changed = True

    if any_changed:
        print("\n下一步:")
        if "staging" in targets and "prod" in targets:
            print(
                "  1. 查看更改: git diff kubernetes/overlays/aws-staging/ kubernetes/overlays/aws-prod/"
            )
            print(
                "  2. 提交: git add -A && git commit -m 'chore: 从 CI 推广镜像到 staging 和 prod'"
            )
        elif "prod" in targets:
            print("  1. 查看更改: git diff kubernetes/overlays/aws-prod/")
            print(
                "  2. 提交: git add -A && git commit -m 'chore: 推广镜像到 prod'"
            )
        else:
            print("  1. 查看更改: git diff kubernetes/overlays/aws-staging/")
            print(
                "  2. 提交: git add -A && git commit -m 'chore: 从 CI 推广镜像到 staging'"
            )
        print("  3. 推送以触发 ArgoCD 同步")

        if "prod" in targets:
            print("\n  ⛔ Production 部署需要手动触发 ArgoCD sync:")
            print("     argocd app sync simplex-aws-prod")


if __name__ == "__main__":
    main()
