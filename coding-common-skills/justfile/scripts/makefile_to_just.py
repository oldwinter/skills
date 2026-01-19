#!/usr/bin/env python3
"""
将 Makefile 转换为 Justfile

用法: python makefile_to_just.py [Makefile路径] [输出路径]
示例: python makefile_to_just.py Makefile justfile
"""

import re
import sys
from pathlib import Path


def convert_makefile_to_justfile(makefile_content: str) -> str:
    """将 Makefile 内容转换为 Justfile 格式"""
    lines = makefile_content.split('\n')
    output_lines = []

    # 跟踪状态
    in_recipe = False
    phony_targets = set()
    variables = {}

    # 第一遍：收集 .PHONY 和变量
    for line in lines:
        # 收集 .PHONY
        if line.startswith('.PHONY:'):
            targets = line.replace('.PHONY:', '').strip().split()
            phony_targets.update(targets)

        # 收集变量定义
        var_match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*[:?]?=\s*(.*)$', line)
        if var_match:
            var_name, var_value = var_match.groups()
            variables[var_name] = var_value.strip()

    # 添加头部注释
    output_lines.append("# 由 Makefile 自动转换生成")
    output_lines.append("# 原始文件可能需要手动调整")
    output_lines.append("")

    # 添加设置
    output_lines.append("set dotenv-load")
    output_lines.append("set shell := [\"bash\", \"-cu\"]")
    output_lines.append("")

    # 转换变量
    for var_name, var_value in variables.items():
        # 转换 $(shell ...) 为反引号
        var_value = re.sub(r'\$\(shell\s+(.+?)\)', r'`\1`', var_value)
        # 转换 $(VAR) 为 {{VAR}}
        var_value = re.sub(r'\$\(([A-Z_][A-Z0-9_]*)\)', r'{{\1}}', var_value)
        var_value = re.sub(r'\$([A-Z_][A-Z0-9_]*)', r'{{\1}}', var_value)

        # 处理导出变量
        if var_name.startswith('export '):
            var_name = var_name.replace('export ', '')
            output_lines.append(f"export {var_name.lower()} := \"{var_value}\"")
        else:
            output_lines.append(f"{var_name.lower()} := \"{var_value}\"")

    if variables:
        output_lines.append("")

    # 第二遍：转换 recipes
    i = 0
    while i < len(lines):
        line = lines[i]

        # 跳过 .PHONY 和变量定义
        if line.startswith('.PHONY:') or re.match(r'^[A-Z_][A-Z0-9_]*\s*[:?]?=', line):
            i += 1
            continue

        # 跳过空行和注释（保留注释）
        if line.strip() == '':
            if not in_recipe:
                output_lines.append('')
            i += 1
            continue

        if line.strip().startswith('#'):
            output_lines.append(line)
            i += 1
            continue

        # 匹配 target 定义
        target_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)$', line)
        if target_match and not line.startswith('\t'):
            target_name = target_match.group(1)
            dependencies = target_match.group(2).strip()

            in_recipe = True

            # 转换 target 名称（下划线转连字符更符合 just 风格）
            just_name = target_name.replace('_', '-')

            # 处理依赖
            if dependencies:
                # 过滤掉文件依赖，只保留 target 依赖
                deps = [d.replace('_', '-') for d in dependencies.split()
                        if not '.' in d and not '/' in d]
                if deps:
                    output_lines.append(f"{just_name}: {' '.join(deps)}")
                else:
                    output_lines.append(f"{just_name}:")
            else:
                output_lines.append(f"{just_name}:")

            i += 1
            continue

        # 处理 recipe 命令行
        if line.startswith('\t'):
            cmd = line[1:]  # 去掉 tab

            # 转换变量引用
            cmd = re.sub(r'\$\(([A-Z_][A-Z0-9_]*)\)', r'{{\1}}', cmd)
            cmd = re.sub(r'\$([A-Z_][A-Z0-9_]*)', r'{{\1}}', cmd)

            # 转换自动变量
            cmd = cmd.replace('$@', '# TODO: replace $@')
            cmd = cmd.replace('$<', '# TODO: replace $<')
            cmd = cmd.replace('$^', '# TODO: replace $^')

            # 保持 @ 前缀（静默执行）
            output_lines.append(f"    {cmd}")
            i += 1
            continue

        in_recipe = False
        i += 1

    return '\n'.join(output_lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python makefile_to_just.py [Makefile路径] [输出路径]")
        print("示例: python makefile_to_just.py Makefile justfile")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("justfile")

    if not input_path.exists():
        print(f"错误: 文件不存在 - {input_path}")
        sys.exit(1)

    content = input_path.read_text()
    result = convert_makefile_to_justfile(content)

    output_path.write_text(result)
    print(f"✅ 已转换: {input_path} -> {output_path}")
    print("\n⚠️  请检查以下内容：")
    print("   - 自动变量 ($@, $<, $^) 需要手动替换")
    print("   - 文件依赖已被移除，可能需要恢复")
    print("   - 变量名已转为小写")


if __name__ == "__main__":
    main()
