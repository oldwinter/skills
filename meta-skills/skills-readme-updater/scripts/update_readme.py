#!/usr/bin/env python3
"""
Skills README 自动更新脚本
扫描 skills 目录，提取每个 skill 的信息并更新 README.md
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = Path(os.path.expanduser("~/.claude/skills"))
README_PATH = SKILLS_DIR / "README.md"

# Skill 分类配置
CATEGORIES = {
    "云基础设施 (Cloud Infrastructure)": [
        "aws-cli", "aws-cost-explorer", "eksctl"
    ],
    "Kubernetes & GitOps": [
        "kubectl", "argocd-cli", "kargo-cli", "sync-to-prod"
    ],
    "代码仓库 (Repository Management)": [
        "github-cli", "gitlab-cli", "changelog-generator"
    ],
    "开发工具 (Development Tools)": [
        "justfile", "skill-creator", "skills-readme-updater"
    ],
    "内容处理 (Content Processing)": [
        "humanizer-zh", "obsidian-dashboard"
    ],
}


def parse_simple_yaml(yaml_text: str) -> dict:
    """简单解析 YAML frontmatter（不依赖 yaml 库）"""
    result = {}
    current_key = None
    current_value = []

    for line in yaml_text.split('\n'):
        # 检查是否是 key: value 格式
        match = re.match(r'^(\w[\w-]*)\s*:\s*(.*)$', line)
        if match:
            # 保存上一个 key 的值
            if current_key:
                result[current_key] = ' '.join(current_value).strip()

            current_key = match.group(1)
            value = match.group(2).strip()

            # 处理多行值的开始 (|)
            if value == '|':
                current_value = []
            elif value.startswith('"') and value.endswith('"'):
                current_value = [value[1:-1]]
            elif value.startswith("'") and value.endswith("'"):
                current_value = [value[1:-1]]
            else:
                current_value = [value] if value else []
        elif current_key and line.strip():
            # 多行值的续行
            current_value.append(line.strip())

    # 保存最后一个 key
    if current_key:
        result[current_key] = ' '.join(current_value).strip()

    return result


def parse_skill_metadata(skill_path: Path) -> dict | None:
    """解析 SKILL.md 的 YAML frontmatter"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding="utf-8")

    # 提取 YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        metadata = parse_simple_yaml(match.group(1))
        desc = metadata.get("description", "")
        # 取第一句作为简短描述
        first_sentence = desc.split(".")[0].strip() if desc else ""
        return {
            "name": metadata.get("name", skill_path.name),
            "description": first_sentence
        }
    except Exception:
        return None


def get_category(skill_name: str) -> str:
    """获取 skill 所属分类"""
    for category, skills in CATEGORIES.items():
        if skill_name in skills:
            return category
    return "其他 (Other)"


def scan_skills() -> dict[str, list[dict]]:
    """扫描所有 skills 并按分类组织"""
    categorized = {}

    for item in SKILLS_DIR.iterdir():
        if not item.is_dir() or item.name.startswith("."):
            continue

        metadata = parse_skill_metadata(item)
        if metadata:
            category = get_category(item.name)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(metadata)

    # 按名称排序
    for category in categorized:
        categorized[category].sort(key=lambda x: x["name"])

    return categorized


def generate_readme(categorized: dict[str, list[dict]]) -> str:
    """生成 README 内容"""
    lines = [
        "# Claude Code Skills",
        "",
        "这是我的 Claude Code Skills 集合，用于扩展 Claude 的能力，提供专业领域的工作流和工具集成。",
        "",
        "## Skills 列表",
        "",
    ]

    # 按预定义顺序输出分类
    category_order = list(CATEGORIES.keys()) + ["其他 (Other)"]

    for category in category_order:
        if category not in categorized:
            continue

        skills = categorized[category]
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Skill | 描述 |")
        lines.append("|-------|------|")

        for skill in skills:
            # 截取描述，最多 80 个字符
            desc = skill["description"]
            if len(desc) > 80:
                desc = desc[:77] + "..."
            lines.append(f"| **{skill['name']}** | {desc} |")

        lines.append("")

    # 目录结构
    lines.extend([
        "## 目录结构",
        "",
        "```",
        "~/.claude/skills/",
        "├── README.md                 # 本文件",
    ])

    all_skills = []
    for skills in categorized.values():
        all_skills.extend([s["name"] for s in skills])
    all_skills.sort()

    for i, skill in enumerate(all_skills):
        prefix = "└──" if i == len(all_skills) - 1 else "├──"
        lines.append(f"{prefix} {skill}/")

    lines.extend([
        "```",
        "",
        "## 使用方式",
        "",
        "Skills 会在对话中根据上下文自动触发，也可以通过 `/skill-name` 手动调用。",
        "",
        "## 添加新 Skill",
        "",
        "使用 `skill-creator` 来创建新的 skill：",
        "",
        "```bash",
        "# 初始化新 skill",
        "python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path ~/.claude/skills",
        "",
        "# 编辑 SKILL.md 和相关文件",
        "",
        "# 验证并打包",
        "python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ~/.claude/skills/<skill-name>",
        "",
        "# 更新 README",
        "python3 ~/.claude/skills/skills-readme-updater/scripts/update_readme.py",
        "```",
        "",
        "---",
        "",
        f"*最后更新: {datetime.now().strftime('%Y-%m-%d')}*",
        "",
    ])

    return "\n".join(lines)


def root_skill_names(root: Path) -> list[str]:
    names = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and (child / "SKILL.md").is_file():
            names.append(child.name)
    return names


def mentioned_in_readme(readme: str, name: str) -> bool:
    return re.search(rf"(^|[^A-Za-z0-9_-]){re.escape(name)}([^A-Za-z0-9_-]|$)", readme) is not None


def audit_readme(root: Path, readme_path: Path) -> int:
    if not readme_path.is_file():
        print(f"error  README not found: {readme_path}", file=sys.stderr)
        print("try: just audit-readme", file=sys.stderr)
        return 2
    names = root_skill_names(root)
    text = readme_path.read_text(encoding="utf-8")
    missing = [name for name in names if not mentioned_in_readme(text, name)]
    if missing:
        print("error  README omits root skills: " + ", ".join(missing), file=sys.stderr)
        print("try: just audit-readme", file=sys.stderr)
        return 1
    print(f"ok  README mentions {len(names)} root skills")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit the handwritten README against this repo's skill tree. Does not rewrite README."
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--readme", type=Path, default=None)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Rejected: would overwrite the two-layer README with a ~/.claude five-bucket dump.",
    )
    args = parser.parse_args(argv)
    if args.write:
        print("error  --write would replace the handwritten two-layer README", file=sys.stderr)
        print("try: just audit-readme", file=sys.stderr)
        return 2
    readme = args.readme if args.readme is not None else args.root / "README.md"
    return audit_readme(args.root, readme)


if __name__ == "__main__":
    raise SystemExit(main())
