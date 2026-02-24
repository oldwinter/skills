#!/usr/bin/env python3
"""
Sync image tags from staging kustomization.yaml to production.

Usage:
    python sync_images.py [--dry-run] [--images IMAGE1,IMAGE2,...] [--all]

Options:
    --dry-run       Show what would be changed without modifying files
    --images        Comma-separated list of image names to sync (partial match)
    --all           Sync all images
    --diff          Show diff between staging and production images
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def find_gitops_root() -> Path:
    """Find the simplex-gitops repository root."""
    # Try common locations
    candidates = [
        Path.cwd(),
        Path.cwd() / "simplex-gitops",
        Path.home() / "Code" / "all-code-in-mba" / "simplex-gitops",
    ]

    for candidate in candidates:
        if (candidate / "kubernetes" / "overlays").exists():
            return candidate

    # Walk up from cwd
    current = Path.cwd()
    while current != current.parent:
        if (current / "kubernetes" / "overlays").exists():
            return current
        current = current.parent

    raise FileNotFoundError("Cannot find simplex-gitops repository root")


def parse_images_section(content: str) -> Tuple[Dict[str, dict], int, int]:
    """
    Parse the images section from kustomization.yaml.
    Returns: (images_dict, start_line, end_line)
    """
    lines = content.split('\n')
    images = {}
    in_images_section = False
    images_start = -1
    images_end = -1
    current_image = None

    for i, line in enumerate(lines):
        # Detect start of images section (may have trailing comment)
        if re.match(r'^images:\s*(#.*)?$', line):
            in_images_section = True
            images_start = i
            continue

        if in_images_section:
            # Detect end of images section (new top-level key or EOF)
            # Must be non-indented, non-empty, non-comment line with a colon
            stripped = line.strip()
            if line and not line.startswith(' ') and not line.startswith('-') and not stripped.startswith('#') and ':' in line:
                images_end = i
                break

            # Parse image entry
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
    """Extract service name from full image path."""
    # Handle ECR format: xxx.ecr.region.amazonaws.com/simplexai/service-name
    # Handle Aliyun format: xxx-registry.cn-hangzhou.cr.aliyuncs.com/simplexai/service-name
    # Handle ghcr format: ghcr.io/org/image
    parts = image_name.split('/')
    return parts[-1] if parts else image_name


def compare_images(staging: Dict[str, dict], prod: Dict[str, dict]) -> List[dict]:
    """
    Compare staging and production images.
    Returns list of differences.
    """
    differences = []

    # Build lookup by service name for ECR images
    staging_by_service = {}
    prod_by_service = {}

    for name, info in staging.items():
        service = extract_service_name(name)
        # Prefer ECR images over Aliyun
        if 'ecr' in name or service not in staging_by_service:
            staging_by_service[service] = {'full_name': name, **info}

    for name, info in prod.items():
        service = extract_service_name(name)
        if 'ecr' in name or service not in prod_by_service:
            prod_by_service[service] = {'full_name': name, **info}

    # Compare
    all_services = set(staging_by_service.keys()) | set(prod_by_service.keys())

    for service in sorted(all_services):
        staging_info = staging_by_service.get(service)
        prod_info = prod_by_service.get(service)

        if staging_info and prod_info:
            staging_tag = staging_info.get('newTag', 'N/A')
            prod_tag = prod_info.get('newTag', 'N/A')

            if staging_tag != prod_tag:
                differences.append({
                    'service': service,
                    'staging_image': staging_info['full_name'],
                    'staging_tag': staging_tag,
                    'prod_image': prod_info['full_name'],
                    'prod_tag': prod_tag,
                    'status': 'different'
                })
            else:
                differences.append({
                    'service': service,
                    'staging_tag': staging_tag,
                    'prod_tag': prod_tag,
                    'status': 'same'
                })
        elif staging_info and not prod_info:
            differences.append({
                'service': service,
                'staging_image': staging_info['full_name'],
                'staging_tag': staging_info.get('newTag', 'N/A'),
                'status': 'staging_only'
            })
        elif prod_info and not staging_info:
            differences.append({
                'service': service,
                'prod_image': prod_info['full_name'],
                'prod_tag': prod_info.get('newTag', 'N/A'),
                'status': 'prod_only'
            })

    return differences


def update_prod_images(
    prod_content: str,
    staging_images: Dict[str, dict],
    prod_images: Dict[str, dict],
    target_services: Optional[List[str]] = None
) -> Tuple[str, List[dict]]:
    """
    Update production kustomization with staging image tags.
    Returns: (updated_content, changes_made)
    """
    changes = []
    lines = prod_content.split('\n')

    # Build staging lookup by service name (prefer ECR)
    staging_by_service = {}
    for name, info in staging_images.items():
        service = extract_service_name(name)
        if 'ecr' in name or service not in staging_by_service:
            staging_by_service[service] = info

    current_image = None
    current_service = None

    for i, line in enumerate(lines):
        # Track current image
        name_match = re.match(r'^(\s*)-\s*name:\s*(.+)$', line)
        if name_match:
            current_image = name_match.group(2).strip()
            current_service = extract_service_name(current_image)
            continue

        # Update newTag if service matches
        if current_service:
            tag_match = re.match(r'^(\s+)newTag:\s*(.+)$', line)
            if tag_match:
                indent = tag_match.group(1)
                old_tag = tag_match.group(2).strip()

                # Check if we should update this service
                if target_services is None or any(
                    t.lower() in current_service.lower() for t in target_services
                ):
                    staging_info = staging_by_service.get(current_service)
                    if staging_info and 'newTag' in staging_info:
                        new_tag = staging_info['newTag']
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
    """Print formatted diff table."""
    print("\n" + "=" * 80)
    print("Image Tag Comparison: Staging vs Production")
    print("=" * 80)

    different = [d for d in differences if d['status'] == 'different']
    same = [d for d in differences if d['status'] == 'same']
    staging_only = [d for d in differences if d['status'] == 'staging_only']
    prod_only = [d for d in differences if d['status'] == 'prod_only']

    if different:
        print(f"\n🔄 DIFFERENT TAGS ({len(different)} services):")
        print("-" * 80)
        print(f"{'Service':<30} {'Staging Tag':<25} {'Prod Tag':<25}")
        print("-" * 80)
        for d in different:
            print(f"{d['service']:<30} {d['staging_tag']:<25} {d['prod_tag']:<25}")

    if same:
        print(f"\n✅ SAME TAGS ({len(same)} services):")
        print("-" * 80)
        for d in same:
            print(f"  {d['service']}: {d['staging_tag']}")

    if staging_only:
        print(f"\n⚠️  STAGING ONLY ({len(staging_only)} services):")
        for d in staging_only:
            print(f"  {d['service']}: {d['staging_tag']}")

    if prod_only:
        print(f"\n⚠️  PROD ONLY ({len(prod_only)} services):")
        for d in prod_only:
            print(f"  {d['service']}: {d['prod_tag']}")

    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Sync image tags from staging to production')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    parser.add_argument('--images', type=str, help='Comma-separated list of images to sync')
    parser.add_argument('--all', action='store_true', help='Sync all images')
    parser.add_argument('--diff', action='store_true', help='Show diff only')
    args = parser.parse_args()

    try:
        root = find_gitops_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    staging_path = root / "kubernetes" / "overlays" / "aws-staging" / "kustomization.yaml"
    prod_path = root / "kubernetes" / "overlays" / "aws-prod" / "kustomization.yaml"

    if not staging_path.exists():
        print(f"Error: Staging kustomization not found: {staging_path}", file=sys.stderr)
        sys.exit(1)

    if not prod_path.exists():
        print(f"Error: Production kustomization not found: {prod_path}", file=sys.stderr)
        sys.exit(1)

    # Read files
    staging_content = staging_path.read_text()
    prod_content = prod_path.read_text()

    # Parse images sections
    staging_images, _, _ = parse_images_section(staging_content)
    prod_images, _, _ = parse_images_section(prod_content)

    # Show diff
    differences = compare_images(staging_images, prod_images)
    print_diff(differences)

    if args.diff:
        return

    # Determine target services
    target_services = None
    if args.images:
        target_services = [s.strip() for s in args.images.split(',')]
    elif not args.all:
        print("\nNo images specified. Use --all to sync all, or --images to specify services.")
        print("Example: --images front,anotherme-agent,simplex-api")
        return

    # Perform update
    updated_content, changes = update_prod_images(
        prod_content, staging_images, prod_images, target_services
    )

    if not changes:
        print("\n✅ No changes needed - production is already in sync!")
        return

    print(f"\n📝 Changes to apply ({len(changes)} updates):")
    print("-" * 60)
    for change in changes:
        print(f"  {change['service']}:")
        print(f"    {change['old_tag']} → {change['new_tag']}")

    if args.dry_run:
        print("\n🔍 DRY RUN - No changes written")
        return

    # Write changes
    prod_path.write_text(updated_content)
    print(f"\n✅ Updated {prod_path}")
    print("\nNext steps:")
    print("  1. Review changes: git diff")
    print("  2. Commit: git add -A && git commit -m 'chore: promote staging images to prod'")
    print("  3. Push to trigger ArgoCD sync")


if __name__ == '__main__':
    main()
