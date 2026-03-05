#!/usr/bin/env python3
"""
Skills README 自动更新脚本
扫描 skills 目录，提取每个 skill 的信息并更新 README.md
"""

import os
import re
from datetime import datetime
from pathlib import Path


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


def main():
    """主函数"""
    print("🔍 扫描 skills 目录...")
    categorized = scan_skills()

    total = sum(len(skills) for skills in categorized.values())
    print(f"✅ 发现 {total} 个 skills")

    print("📝 生成 README...")
    readme_content = generate_readme(categorized)

    README_PATH.write_text(readme_content, encoding="utf-8")
    print(f"✅ README 已更新: {README_PATH}")

    # 输出摘要
    print("\n📊 Skills 统计:")
    for category, skills in categorized.items():
        print(f"  {category}: {len(skills)} 个")


if __name__ == "__main__":
    main()
