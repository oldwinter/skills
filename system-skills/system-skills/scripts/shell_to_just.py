#!/usr/bin/env python3
"""
从 shell history 或命令列表生成 Justfile

用法:
  python shell_to_just.py --history [输出路径]     # 从 shell history 提取
  python shell_to_just.py commands.txt [输出路径]  # 从文件读取命令列表

示例:
  python shell_to_just.py --history justfile
  python shell_to_just.py my_commands.txt justfile
"""

import os
import re
import sys
from collections import Counter
from pathlib import Path


def get_shell_history() -> list[str]:
    """获取 shell history"""
    history_files = [
        Path.home() / ".zsh_history",
        Path.home() / ".bash_history",
        Path.home() / ".history",
    ]

    commands = []
    for hist_file in history_files:
        if hist_file.exists():
            try:
                content = hist_file.read_text(errors='ignore')
                # 处理 zsh 格式 (: timestamp:0;command)
                zsh_cmds = re.findall(r'^: \d+:\d+;(.+)$', content, re.MULTILINE)
                if zsh_cmds:
                    commands.extend(zsh_cmds)
                else:
                    # bash 格式
                    commands.extend(content.strip().split('\n'))
                break
            except Exception as e:
                print(f"警告: 无法读取 {hist_file}: {e}")

    return commands


def analyze_commands(commands: list[str]) -> dict:
    """分析命令，找出重复和常用的命令"""
    # 过滤和清理
    cleaned = []
    for cmd in commands:
        cmd = cmd.strip()
        # 跳过太短或太长的命令
        if len(cmd) < 5 or len(cmd) > 200:
            continue
        # 跳过某些命令
        skip_patterns = [
            r'^cd\s', r'^ls\s*$', r'^pwd$', r'^exit$', r'^clear$',
            r'^history', r'^echo\s', r'^cat\s', r'^vim?\s', r'^nano\s',
        ]
        if any(re.match(p, cmd) for p in skip_patterns):
            continue
        cleaned.append(cmd)

    # 统计频率
    counter = Counter(cleaned)

    # 分类
    categories = {
        'docker': [],
        'git': [],
        'npm': [],
        'python': [],
        'kubectl': [],
        'make': [],
        'other': []
    }

    for cmd, count in counter.most_common(50):
        if count < 2:
            continue

        if cmd.startswith('docker'):
            categories['docker'].append((cmd, count))
        elif cmd.startswith('git'):
            categories['git'].append((cmd, count))
        elif cmd.startswith(('npm', 'yarn', 'pnpm')):
            categories['npm'].append((cmd, count))
        elif cmd.startswith(('python', 'pip', 'poetry', 'uv')):
            categories['python'].append((cmd, count))
        elif cmd.startswith(('kubectl', 'k ', 'k8s')):
            categories['kubectl'].append((cmd, count))
        elif cmd.startswith('make'):
            categories['make'].append((cmd, count))
        else:
            categories['other'].append((cmd, count))

    return categories


def generate_recipe_name(cmd: str, index: int) -> str:
    """为命令生成一个合理的 recipe 名称"""
    # 尝试从命令提取有意义的名称
    words = cmd.split()[:3]
    name_parts = []

    for word in words:
        # 跳过选项
        if word.startswith('-'):
            continue
        # 清理特殊字符
        clean = re.sub(r'[^a-zA-Z0-9]', '', word)
        if clean and len(clean) > 1:
            name_parts.append(clean.lower())

    if name_parts:
        name = '-'.join(name_parts[:3])
        return name if len(name) > 3 else f"cmd-{index}"

    return f"cmd-{index}"


def generate_justfile(categories: dict) -> str:
    """生成 Justfile 内容"""
    output_lines = []

    output_lines.append("# 从常用命令自动生成的 Justfile")
    output_lines.append("# 请根据需要修改 recipe 名称和命令")
    output_lines.append("")
    output_lines.append("set dotenv-load")
    output_lines.append("set shell := [\"bash\", \"-cu\"]")
    output_lines.append("")

    category_names = {
        'docker': 'Docker',
        'git': 'Git',
        'npm': 'Node.js',
        'python': 'Python',
        'kubectl': 'Kubernetes',
        'make': 'Make',
        'other': '其他'
    }

    recipe_index = 0
    used_names = set()

    for cat_key, cat_cmds in categories.items():
        if not cat_cmds:
            continue

        output_lines.append(f"# === {category_names[cat_key]} ===")
        output_lines.append("")

        for cmd, count in cat_cmds[:10]:  # 每个分类最多 10 个
            recipe_name = generate_recipe_name(cmd, recipe_index)

            # 确保名称唯一
            base_name = recipe_name
            suffix = 1
            while recipe_name in used_names:
                recipe_name = f"{base_name}-{suffix}"
                suffix += 1
            used_names.add(recipe_name)

            output_lines.append(f"# 使用次数: {count}")
            output_lines.append(f"{recipe_name}:")
            output_lines.append(f"    {cmd}")
            output_lines.append("")

            recipe_index += 1

    return '\n'.join(output_lines)


def main():
    output_path = Path("justfile")

    if len(sys.argv) < 2:
        print("用法:")
        print("  python shell_to_just.py --history [输出路径]     # 从 shell history 提取")
        print("  python shell_to_just.py commands.txt [输出路径]  # 从文件读取命令列表")
        sys.exit(1)

    if sys.argv[1] == '--history':
        commands = get_shell_history()
        if len(sys.argv) > 2:
            output_path = Path(sys.argv[2])
    else:
        input_path = Path(sys.argv[1])
        if not input_path.exists():
            print(f"错误: 文件不存在 - {input_path}")
            sys.exit(1)
        commands = input_path.read_text().strip().split('\n')
        if len(sys.argv) > 2:
            output_path = Path(sys.argv[2])

    if not commands:
        print("错误: 未找到命令")
        sys.exit(1)

    print(f"📊 分析 {len(commands)} 条命令...")
    categories = analyze_commands(commands)

    total = sum(len(cmds) for cmds in categories.values())
    print(f"✨ 找到 {total} 条重复命令")

    result = generate_justfile(categories)
    output_path.write_text(result)

    print(f"✅ 已生成: {output_path}")
    print("\n⚠️  请检查并修改 recipe 名称使其更有意义")


if __name__ == "__main__":
    main()
