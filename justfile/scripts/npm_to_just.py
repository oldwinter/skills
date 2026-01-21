#!/usr/bin/env python3
"""
将 package.json scripts 转换为 Justfile

用法: python npm_to_just.py [package.json路径] [输出路径]
示例: python npm_to_just.py package.json justfile
"""

import json
import re
import sys
from pathlib import Path


def sanitize_name(name: str) -> str:
    """将 npm script 名称转换为 just recipe 名称"""
    # 替换 : 为 -
    name = name.replace(':', '-')
    # 替换其他非法字符
    name = re.sub(r'[^a-zA-Z0-9_-]', '-', name)
    return name


def convert_npm_command(cmd: str) -> str:
    """转换 npm 命令为 shell 命令"""
    # 替换 npm run xxx 为 just xxx
    cmd = re.sub(r'npm run ([a-zA-Z0-9_:-]+)', r'just \1', cmd)
    # 替换 yarn xxx 为 just xxx (如果是 script 引用)
    cmd = re.sub(r'yarn ([a-zA-Z0-9_:-]+)(?!\s)', r'just \1', cmd)
    return cmd


def convert_package_json_to_justfile(package_json: dict) -> str:
    """将 package.json scripts 转换为 Justfile"""
    scripts = package_json.get('scripts', {})

    if not scripts:
        return "# 未找到 scripts\n"

    output_lines = []

    # 头部
    output_lines.append("# 由 package.json scripts 自动转换生成")
    output_lines.append("")
    output_lines.append("set dotenv-load")
    output_lines.append("set shell := [\"bash\", \"-cu\"]")
    output_lines.append("")

    # 提取项目信息
    name = package_json.get('name', 'project')
    version = package_json.get('version', '0.0.0')
    output_lines.append(f"project := \"{name}\"")
    output_lines.append(f"version := \"{version}\"")
    output_lines.append("")

    # 分组 scripts
    groups = {
        'dev': [],      # 开发相关
        'build': [],    # 构建相关
        'test': [],     # 测试相关
        'lint': [],     # 代码检查
        'other': []     # 其他
    }

    for script_name, script_cmd in scripts.items():
        if any(x in script_name.lower() for x in ['dev', 'start', 'serve', 'watch']):
            groups['dev'].append((script_name, script_cmd))
        elif any(x in script_name.lower() for x in ['build', 'compile', 'bundle']):
            groups['build'].append((script_name, script_cmd))
        elif any(x in script_name.lower() for x in ['test', 'spec', 'e2e']):
            groups['test'].append((script_name, script_cmd))
        elif any(x in script_name.lower() for x in ['lint', 'format', 'prettier', 'eslint']):
            groups['lint'].append((script_name, script_cmd))
        else:
            groups['other'].append((script_name, script_cmd))

    # 默认 recipe
    if 'dev' in scripts:
        output_lines.append("# 默认运行开发服务器")
        output_lines.append("default: dev")
        output_lines.append("")
    elif 'start' in scripts:
        output_lines.append("# 默认启动")
        output_lines.append("default: start")
        output_lines.append("")

    # 按分组输出
    group_names = {
        'dev': '开发',
        'build': '构建',
        'test': '测试',
        'lint': '代码检查',
        'other': '其他'
    }

    for group_key, group_scripts in groups.items():
        if not group_scripts:
            continue

        output_lines.append(f"# === {group_names[group_key]} ===")
        output_lines.append("")

        for script_name, script_cmd in group_scripts:
            recipe_name = sanitize_name(script_name)
            converted_cmd = convert_npm_command(script_cmd)

            # 添加文档注释
            output_lines.append(f"# npm run {script_name}")
            output_lines.append(f"{recipe_name}:")

            # 处理 && 连接的命令
            if ' && ' in converted_cmd:
                commands = converted_cmd.split(' && ')
                for cmd in commands:
                    output_lines.append(f"    {cmd.strip()}")
            else:
                output_lines.append(f"    {converted_cmd}")

            output_lines.append("")

    # 添加辅助 recipes
    output_lines.append("# === 辅助命令 ===")
    output_lines.append("")
    output_lines.append("# 安装依赖")
    output_lines.append("install:")
    output_lines.append("    npm install")
    output_lines.append("")
    output_lines.append("# 清理")
    output_lines.append("clean:")
    output_lines.append("    rm -rf node_modules dist build .cache")
    output_lines.append("")
    output_lines.append("# 更新依赖")
    output_lines.append("update:")
    output_lines.append("    npm update")
    output_lines.append("")

    return '\n'.join(output_lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python npm_to_just.py [package.json路径] [输出路径]")
        print("示例: python npm_to_just.py package.json justfile")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("justfile")

    if not input_path.exists():
        print(f"错误: 文件不存在 - {input_path}")
        sys.exit(1)

    with open(input_path) as f:
        package_json = json.load(f)

    result = convert_package_json_to_justfile(package_json)

    output_path.write_text(result)
    print(f"✅ 已转换: {input_path} -> {output_path}")
    print(f"\n📦 项目: {package_json.get('name', 'unknown')}")
    print(f"📝 转换了 {len(package_json.get('scripts', {}))} 个 scripts")


if __name__ == "__main__":
    main()
