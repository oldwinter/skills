#!/usr/bin/env python3
"""
将 CI kustomization.yaml 的镜像标签同步到 staging。

使用方法：
    python sync_images.py [--dry-run] [--images IMAGE1,IMAGE2,...] [--all]

选项：
    --dry-run       显示将要更改的内容，但不修改文件
    --images        要同步的镜像名称（逗号分隔，支持部分匹配）
    --all           同步所有镜像
    --diff          显示 CI 和 staging 镜像之间的差异
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def find_gitops_root() -> Path:
    """查找 simplex-gitops 仓库根目录。"""
    # 尝试常见位置
    candidates = [
        Path.cwd(),
        Path.cwd() / "simplex-gitops",
        Path.home() / "Code" / "all-code-in-mba" / "simplex-gitops",
        Path("/Users/cdd/Code/all-code-in-mba/simplex-gitops"),
    ]

    for candidate in candidates:
        if (candidate / "kubernetes" / "overlays").exists():
            return candidate

    # 从当前目录向上查找
    current = Path.cwd()
    while current != current.parent:
        if (current / "kubernetes" / "overlays").exists():
            return current
        current = current.parent

    raise FileNotFoundError("无法找到 simplex-gitops 仓库根目录")


def parse_images_section(content: str) -> Tuple[Dict[str, dict], int, int]:
    """
    从 kustomization.yaml 解析 images 部分。
    返回：(images_dict, start_line, end_line)
    """
    lines = content.split('\n')
    images = {}
    in_images_section = False
    images_start = -1
    images_end = -1
    current_image = None

    for i, line in enumerate(lines):
        # 检测 images 部分的开始（可能有尾随注释）
        if re.match(r'^images:\s*(#.*)?$', line):
            in_images_section = True
            images_start = i
            continue

        if in_images_section:
            # 检测 images 部分的结束（新的顶级键或 EOF）
            # 必须是非缩进、非空、非注释的行，包含冒号
            stripped = line.strip()
            if line and not line.startswith(' ') and not line.startswith('-') and not stripped.startswith('#') and ':' in line:
                images_end = i
                break

            # 解析镜像条目
            name_match = re.match(r'^\s*-\s*name:\s*(.+)$', line)
            if name_match:
                current_image = name_match.group(1).strip()
                images[current_image] = {'name': current_image}
                continue

            if current_image:
                new_name_match = re.match(r'^\s+newName:\s*(.+)$', line)
                if new_name_match:
                    images[current_image]['newName'] = new_name_match.group(1).strip()
                    continue

                new_tag_match = re.match(r'^\s+newTag:\s*(.+)$', line)
                if new_tag_match:
                    images[current_image]['newTag'] = new_tag_match.group(1).strip()
                    continue

    if images_end == -1:
        images_end = len(lines)

    return images, images_start, images_end


def extract_service_name(image_name: str) -> str:
    """从完整镜像路径提取服务名称。"""
    # 处理 ECR 格式：xxx.ecr.region.amazonaws.com/simplexai/service-name
    # 处理阿里云格式：xxx-registry.cn-hangzhou.cr.aliyuncs.com/simplexai/service-name
    # 处理 ghcr 格式：ghcr.io/org/image
    parts = image_name.split('/')
    return parts[-1] if parts else image_name


def compare_images(ci: Dict[str, dict], staging: Dict[str, dict]) -> List[dict]:
    """
    比较 CI 和 staging 镜像。
    返回差异列表。
    """
    differences = []

    # 按服务名称构建查找表（用于 ECR 镜像）
    ci_by_service = {}
    staging_by_service = {}

    for name, info in ci.items():
        service = extract_service_name(name)
        # 优先选择 ECR 镜像而不是阿里云
        if 'ecr' in name or service not in ci_by_service:
            ci_by_service[service] = {'full_name': name, **info}

    for name, info in staging.items():
        service = extract_service_name(name)
        if 'ecr' in name or service not in staging_by_service:
            staging_by_service[service] = {'full_name': name, **info}

    # 比较
    all_services = set(ci_by_service.keys()) | set(staging_by_service.keys())

    for service in sorted(all_services):
        ci_info = ci_by_service.get(service)
        staging_info = staging_by_service.get(service)

        if ci_info and staging_info:
            ci_tag = ci_info.get('newTag', 'N/A')
            staging_tag = staging_info.get('newTag', 'N/A')

            if ci_tag != staging_tag:
                differences.append({
                    'service': service,
                    'ci_image': ci_info['full_name'],
                    'ci_tag': ci_tag,
                    'staging_image': staging_info['full_name'],
                    'staging_tag': staging_tag,
                    'status': 'different'
                })
            else:
                differences.append({
                    'service': service,
                    'ci_tag': ci_tag,
                    'staging_tag': staging_tag,
                    'status': 'same'
                })
        elif ci_info and not staging_info:
            differences.append({
                'service': service,
                'ci_image': ci_info['full_name'],
                'ci_tag': ci_info.get('newTag', 'N/A'),
                'status': 'ci_only'
            })
        elif staging_info and not ci_info:
            differences.append({
                'service': service,
                'staging_image': staging_info['full_name'],
                'staging_tag': staging_info.get('newTag', 'N/A'),
                'status': 'staging_only'
            })

    return differences


def update_staging_images(
    staging_content: str,
    ci_images: Dict[str, dict],
    staging_images: Dict[str, dict],
    target_services: Optional[List[str]] = None
) -> Tuple[str, List[dict]]:
    """
    用 CI 镜像标签更新 staging kustomization。
    返回：(updated_content, changes_made)
    """
    changes = []
    lines = staging_content.split('\n')

    # 按服务名称构建 CI 查找表（优先 ECR）
    ci_by_service = {}
    for name, info in ci_images.items():
        service = extract_service_name(name)
        if 'ecr' in name or service not in ci_by_service:
            ci_by_service[service] = info

    current_image = None
    current_service = None

    for i, line in enumerate(lines):
        # 跟踪当前镜像
        name_match = re.match(r'^(\s*)-\s*name:\s*(.+)$', line)
        if name_match:
            current_image = name_match.group(2).strip()
            current_service = extract_service_name(current_image)
            continue

        # 如果服务匹配，更新 newTag
        if current_service:
            tag_match = re.match(r'^(\s+)newTag:\s*(.+)$', line)
            if tag_match:
                indent = tag_match.group(1)
                old_tag = tag_match.group(2).strip()

                # 检查是否应更新此服务
                if target_services is None or any(
                    t.lower() in current_service.lower() for t in target_services
                ):
                    ci_info = ci_by_service.get(current_service)
                    if ci_info and 'newTag' in ci_info:
                        new_tag = ci_info['newTag']
                        if old_tag != new_tag:
                            lines[i] = f"{indent}newTag: {new_tag}"
                            changes.append({
                                'service': current_service,
                                'image': current_image,
                                'old_tag': old_tag,
                                'new_tag': new_tag
                            })

    return '\n'.join(lines), changes


def print_diff(differences: List[dict]):
    """打印格式化的差异表。"""
    print("\n" + "=" * 80)
    print("镜像标签比较：CI vs Staging")
    print("=" * 80)

    different = [d for d in differences if d['status'] == 'different']
    same = [d for d in differences if d['status'] == 'same']
    ci_only = [d for d in differences if d['status'] == 'ci_only']
    staging_only = [d for d in differences if d['status'] == 'staging_only']

    if different:
        print(f"\n🔄 标签不同 ({len(different)} 个服务):")
        print("-" * 80)
        print(f"{'服务':<30} {'CI 标签':<25} {'Staging 标签':<25}")
        print("-" * 80)
        for d in different:
            print(f"{d['service']:<30} {d['ci_tag']:<25} {d['staging_tag']:<25}")

    if same:
        print(f"\n✅ 标签相同 ({len(same)} 个服务):")
        print("-" * 80)
        for d in same:
            print(f"  {d['service']}: {d['ci_tag']}")

    if ci_only:
        print(f"\n⚠️  仅 CI ({len(ci_only)} 个服务):")
        for d in ci_only:
            print(f"  {d['service']}: {d['ci_tag']}")

    if staging_only:
        print(f"\n⚠️  仅 STAGING ({len(staging_only)} 个服务):")
        for d in staging_only:
            print(f"  {d['service']}: {d['staging_tag']}")

    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description='将 CI 镜像标签同步到 staging')
    parser.add_argument('--dry-run', action='store_true', help='显示更改但不应用')
    parser.add_argument('--images', type=str, help='要同步的镜像（逗号分隔）')
    parser.add_argument('--all', action='store_true', help='同步所有镜像')
    parser.add_argument('--diff', action='store_true', help='仅显示差异')
    args = parser.parse_args()

    try:
        root = find_gitops_root()
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    ci_path = root / "kubernetes" / "overlays" / "aws-ci" / "kustomization.yaml"
    staging_path = root / "kubernetes" / "overlays" / "aws-staging" / "kustomization.yaml"

    if not ci_path.exists():
        print(f"错误: 未找到 CI kustomization: {ci_path}", file=sys.stderr)
        sys.exit(1)

    if not staging_path.exists():
        print(f"错误: 未找到 Staging kustomization: {staging_path}", file=sys.stderr)
        sys.exit(1)

    # 读取文件
    ci_content = ci_path.read_text()
    staging_content = staging_path.read_text()

    # 解析 images 部分
    ci_images, _, _ = parse_images_section(ci_content)
    staging_images, _, _ = parse_images_section(staging_content)

    # 显示差异
    differences = compare_images(ci_images, staging_images)
    print_diff(differences)

    if args.diff:
        return

    # 确定目标服务
    target_services = None
    if args.images:
        target_services = [s.strip() for s in args.images.split(',')]
    elif not args.all:
        print("\n未指定镜像。使用 --all 同步所有，或使用 --images 指定服务。")
        print("示例: --images front,anotherme-agent,simplex-api")
        return

    # 执行更新
    updated_content, changes = update_staging_images(
        staging_content, ci_images, staging_images, target_services
    )

    if not changes:
        print("\n✅ 无需更改 - staging 已经同步!")
        return

    print(f"\n📝 将应用的更改 ({len(changes)} 个更新):")
    print("-" * 60)
    for change in changes:
        print(f"  {change['service']}:")
        print(f"    {change['old_tag']} → {change['new_tag']}")

    if args.dry_run:
        print("\n🔍 DRY RUN - 未写入更改")
        return

    # 写入更改
    staging_path.write_text(updated_content)
    print(f"\n✅ 已更新 {staging_path}")
    print("\n下一步:")
    print("  1. 查看更改: git diff")
    print("  2. 提交: git add -A && git commit -m 'chore: 从 CI 推广镜像到 staging'")
    print("  3. 推送以触发 ArgoCD 同步")


if __name__ == '__main__':
    main()
