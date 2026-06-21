#!/usr/bin/env python3
"""
比较 CI 和 staging 环境之间的配置文件。

此脚本识别以下差异：
- patches/ 中的 ConfigMaps 和 Secrets
- kustomization.yaml 中新增的资源
- 资源文件中的更改

使用方法：
    python compare_configs.py [--detailed] [--file FILENAME]

选项：
    --detailed      显示每个文件的详细差异
    --file          仅比较特定文件
    --safe-only     只显示安全可同步的配置差异（排除 secrets、ingress）
"""

import argparse
import difflib
import re
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


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


def get_resource_type(filepath: Path) -> str:
    """从文件内容确定 Kubernetes 资源类型。"""
    try:
        with open(filepath) as f:
            for line in f:
                if line.startswith('kind:'):
                    return line.split(':', 1)[1].strip()
    except:
        pass
    return "Unknown"


def is_safe_to_sync(filename: str) -> Tuple[bool, str]:
    """
    确定文件是否安全地从 CI 同步到 staging。
    返回：(is_safe, reason)
    """
    filename_lower = filename.lower()
    
    # 永不同步这些
    if 'secret' in filename_lower:
        return False, "🔐 Secrets (环境特定)"
    if 'ingress' in filename_lower:
        return False, "🌐 Ingress (域名不同)"
    
    # 通常是环境特定的
    if any(x in filename_lower for x in ['gateway', 'router', 'api-cm0']):
        return False, "⚙️  基础设施配置 (通常是环境特定的)"
    
    # 可能需要选择性同步
    if 'configmap' in filename_lower or 'env' in filename_lower:
        return True, "📝 ConfigMap (同步前仔细审查)"
    
    return True, "✅ 安全可审查"


def compare_patches_dir(ci_dir: Path, staging_dir: Path, detailed: bool = False, 
                       target_file: Optional[str] = None, safe_only: bool = False) -> Dict:
    """比较 CI 和 staging 之间的 patches 目录。"""
    results = {
        'identical': [],
        'different': [],
        'ci_only': [],
        'staging_only': []
    }
    
    ci_files = set(f.name for f in ci_dir.glob('*.yaml'))
    staging_files = set(f.name for f in staging_dir.glob('*.yaml'))
    
    # 仅在 CI 中的文件（新配置）
    results['ci_only'] = sorted(ci_files - staging_files)
    
    # 仅在 staging 中的文件（已删除的配置）
    results['staging_only'] = sorted(staging_files - ci_files)
    
    # 两者中都有的文件 - 检查差异
    common_files = ci_files & staging_files
    
    if target_file:
        common_files = {target_file} if target_file in common_files else set()
    
    for filename in sorted(common_files):
        ci_file = ci_dir / filename
        staging_file = staging_dir / filename
        
        # 检查安全性
        safe, reason = is_safe_to_sync(filename)
        if safe_only and not safe:
            continue
        
        ci_content = ci_file.read_text()
        staging_content = staging_file.read_text()
        
        if ci_content == staging_content:
            results['identical'].append(filename)
        else:
            diff_info = {
                'filename': filename,
                'safe_to_sync': safe,
                'reason': reason,
                'resource_type': get_resource_type(ci_file)
            }
            
            if detailed:
                # 生成统一差异
                diff = list(difflib.unified_diff(
                    staging_content.splitlines(keepends=True),
                    ci_content.splitlines(keepends=True),
                    fromfile=f'staging/{filename}',
                    tofile=f'ci/{filename}',
                    lineterm=''
                ))
                diff_info['diff'] = ''.join(diff)
                
                # 尝试识别关键更改
                changes = analyze_config_changes(staging_content, ci_content)
                diff_info['changes'] = changes
            
            results['different'].append(diff_info)
    
    return results


def analyze_config_changes(old_content: str, new_content: str) -> List[str]:
    """分析配置文件中的特定更改。"""
    changes = []
    
    try:
        # 使用简单正则表达式解析 data 部分的键
        old_data_keys = set(re.findall(r'^\s+(\S+):\s*[|>]?', old_content, re.MULTILINE))
        new_data_keys = set(re.findall(r'^\s+(\S+):\s*[|>]?', new_content, re.MULTILINE))
        
        # 查找 data: 部分边界
        old_in_data = 'data:' in old_content or 'stringData:' in old_content
        new_in_data = 'data:' in new_content or 'stringData:' in new_content
        
        if old_in_data and new_in_data:
            added_keys = new_data_keys - old_data_keys
            removed_keys = old_data_keys - new_data_keys
            
            if added_keys:
                changes.append(f"➕ 新增键: {', '.join(sorted(list(added_keys)[:5]))}")
            if removed_keys:
                changes.append(f"➖ 删除键: {', '.join(sorted(list(removed_keys)[:5]))}")
            
            # 检查值变化（简单方法）
            common_keys = old_data_keys & new_data_keys
            modified_count = 0
            for key in common_keys:
                # 在两个内容中查找键
                old_match = re.search(rf'^\s+{re.escape(key)}:\s*(.+)$', old_content, re.MULTILINE)
                new_match = re.search(rf'^\s+{re.escape(key)}:\s*(.+)$', new_content, re.MULTILINE)
                
                if old_match and new_match:
                    if old_match.group(1) != new_match.group(1):
                        modified_count += 1
            
            if modified_count > 0:
                changes.append(f"🔄 已修改: {modified_count} 个键更改了值")
        else:
            # 计算总行差异
            old_lines = old_content.splitlines()
            new_lines = new_content.splitlines()
            diff_count = sum(1 for a, b in zip(old_lines, new_lines) if a != b)
            diff_count += abs(len(old_lines) - len(new_lines))
            changes.append(f"🔄 {diff_count} 行不同")
    
    except Exception as e:
        changes.append(f"⚠️  解析错误: {str(e)}")
    
    return changes if changes else ["内容不同但未识别特定更改"]


def compare_kustomization_resources(ci_file: Path, staging_file: Path) -> Dict:
    """比较 kustomization.yaml 中的 resources 和 patches 部分。"""
    ci_content = ci_file.read_text()
    staging_content = staging_file.read_text()
    
    def extract_section(content: str, section: str) -> Set[str]:
        """从 YAML 部分提取列表项。"""
        items = set()
        in_section = False
        for line in content.splitlines():
            if re.match(rf'^{section}:\s*$', line):
                in_section = True
                continue
            if in_section:
                # 如果遇到另一个顶级键，则结束部分
                if line and not line.startswith(' ') and not line.startswith('-') and ':' in line:
                    break
                # 提取列表项
                match = re.match(r'^\s*-\s*(.+)$', line)
                if match:
                    item = match.group(1).strip()
                    items.add(item)
        return items
    
    results = {
        'resources': {
            'ci_only': [],
            'staging_only': [],
            'common': []
        },
        'patches': {
            'ci_only': [],
            'staging_only': [],
            'common': []
        }
    }
    
    # 比较 resources
    ci_resources = extract_section(ci_content, 'resources')
    staging_resources = extract_section(staging_content, 'resources')
    
    results['resources']['ci_only'] = sorted(ci_resources - staging_resources)
    results['resources']['staging_only'] = sorted(staging_resources - ci_resources)
    results['resources']['common'] = sorted(ci_resources & staging_resources)
    
    # 比较 patches（处理字符串和对象格式）
    def extract_patches(content: str) -> Set[str]:
        patches = set()
        in_patches = False
        for line in content.splitlines():
            if re.match(r'^patches:\s*$', line):
                in_patches = True
                continue
            if in_patches:
                if line and not line.startswith(' ') and not line.startswith('-') and ':' in line:
                    break
                # 字符串格式: - patches/file.yaml
                match = re.match(r'^\s*-\s*patches/(.+\.yaml)', line)
                if match:
                    patches.add(f"patches/{match.group(1)}")
                    continue
                # 对象格式: path: patches/file.yaml
                match = re.match(r'^\s+path:\s*patches/(.+\.yaml)', line)
                if match:
                    patches.add(f"patches/{match.group(1)}")
        return patches
    
    ci_patches = extract_patches(ci_content)
    staging_patches = extract_patches(staging_content)
    
    results['patches']['ci_only'] = sorted(ci_patches - staging_patches)
    results['patches']['staging_only'] = sorted(staging_patches - ci_patches)
    results['patches']['common'] = sorted(ci_patches & staging_patches)
    
    return results


def print_results(patch_results: Dict, kust_results: Dict, detailed: bool):
    """以格式化方式打印比较结果。"""
    print("\n" + "=" * 80)
    print("配置比较：CI vs Staging")
    print("=" * 80)
    
    # Patches 目录比较
    print("\n📁 Patches 目录比较")
    print("-" * 80)
    
    if patch_results['different']:
        print(f"\n🔄 配置不同 ({len(patch_results['different'])} 个文件):")
        for item in patch_results['different']:
            safe_icon = "✅" if item['safe_to_sync'] else "⚠️"
            print(f"\n  {safe_icon} {item['filename']} ({item['resource_type']})")
            print(f"     {item['reason']}")
            
            if 'changes' in item and item['changes']:
                for change in item['changes']:
                    print(f"     {change}")
            
            if detailed and 'diff' in item:
                print("\n" + "-" * 60)
                print(item['diff'])
                print("-" * 60)
    
    if patch_results['ci_only']:
        print(f"\n➕ CI 中的新配置 ({len(patch_results['ci_only'])} 个文件):")
        for filename in patch_results['ci_only']:
            safe, reason = is_safe_to_sync(filename)
            safe_icon = "✅" if safe else "⚠️"
            print(f"  {safe_icon} {filename} - {reason}")
    
    if patch_results['staging_only']:
        print(f"\n➖ CI 中已删除 ({len(patch_results['staging_only'])} 个文件):")
        for filename in patch_results['staging_only']:
            print(f"  ⚠️  {filename}")
    
    if patch_results['identical']:
        print(f"\n✅ 相同 ({len(patch_results['identical'])} 个文件):")
        for filename in patch_results['identical']:
            print(f"  {filename}")
    
    # Kustomization resources 比较
    print("\n\n📦 Kustomization Resources 比较")
    print("-" * 80)
    
    if kust_results['resources']['ci_only']:
        print(f"\n➕ CI 中的新资源 ({len(kust_results['resources']['ci_only'])}):")
        for resource in kust_results['resources']['ci_only']:
            print(f"  {resource}")
    
    if kust_results['resources']['staging_only']:
        print(f"\n➖ 仅 STAGING 中的资源 ({len(kust_results['resources']['staging_only'])}):")
        for resource in kust_results['resources']['staging_only']:
            print(f"  {resource}")
    
    if kust_results['patches']['ci_only']:
        print(f"\n➕ CI 中的新 Patches ({len(kust_results['patches']['ci_only'])}):")
        for patch in kust_results['patches']['ci_only']:
            print(f"  {patch}")
    
    if kust_results['patches']['staging_only']:
        print(f"\n➖ 仅 STAGING 中的 Patches ({len(kust_results['patches']['staging_only'])}):")
        for patch in kust_results['patches']['staging_only']:
            print(f"  {patch}")
    
    print("\n" + "=" * 80)
    
    # 摘要和建议
    print("\n💡 建议:")
    print("-" * 80)
    
    safe_to_sync = [item for item in patch_results['different'] 
                    if item['safe_to_sync']]
    unsafe_to_sync = [item for item in patch_results['different'] 
                      if not item['safe_to_sync']]
    
    if safe_to_sync:
        print(f"\n✅ 安全可审查以同步 ({len(safe_to_sync)} 个文件):")
        for item in safe_to_sync:
            print(f"  • {item['filename']}")
        print("\n  审查这些文件，如果合适则同步:")
        print("  python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py --file <filename> --detailed")
    
    if unsafe_to_sync:
        print(f"\n⚠️  环境特定配置 ({len(unsafe_to_sync)} 个文件):")
        for item in unsafe_to_sync:
            print(f"  • {item['filename']} - {item['reason']}")
        print("\n  这些通常不应在环境之间同步。")
    
    if patch_results['ci_only']:
        print(f"\n➕ 要添加到 staging 的新配置:")
        for filename in patch_results['ci_only']:
            safe, reason = is_safe_to_sync(filename)
            if safe:
                print(f"  • {filename}")
    
    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='比较 CI 和 staging 之间的配置'
    )
    parser.add_argument('--detailed', action='store_true', 
                       help='显示每个文件的详细差异')
    parser.add_argument('--file', type=str, 
                       help='仅比较特定文件')
    parser.add_argument('--safe-only', action='store_true',
                       help='只显示安全可同步的配置差异')
    args = parser.parse_args()
    
    try:
        root = find_gitops_root()
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    
    ci_dir = root / "kubernetes" / "overlays" / "aws-ci"
    staging_dir = root / "kubernetes" / "overlays" / "aws-staging"
    
    # 比较 patches 目录
    patch_results = compare_patches_dir(
        ci_dir / "patches",
        staging_dir / "patches",
        detailed=args.detailed,
        target_file=args.file,
        safe_only=args.safe_only
    )
    
    # 比较 kustomization.yaml resources
    kust_results = compare_kustomization_resources(
        ci_dir / "kustomization.yaml",
        staging_dir / "kustomization.yaml"
    )
    
    # 打印结果
    print_results(patch_results, kust_results, args.detailed)


if __name__ == '__main__':
    main()
