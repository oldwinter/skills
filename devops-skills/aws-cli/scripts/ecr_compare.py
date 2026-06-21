#!/usr/bin/env python3
"""
ECR Image Comparison Script

Compares container image versions across ECR repositories.
Usage: python3 ecr_compare.py [--repository REPO] [--limit N]
"""

import subprocess
import json
import argparse
from datetime import datetime


def run_aws_command(cmd: list) -> dict | list | None:
    """Execute AWS CLI command and return parsed JSON output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        print(f"Error: {e}")
        return None


def list_repositories() -> list[str]:
    """List all ECR repositories."""
    cmd = [
        "aws", "ecr", "describe-repositories",
        "--query", "repositories[].repositoryName",
        "--output", "json"
    ]
    result = run_aws_command(cmd)
    return result if result else []


def get_latest_images(repository: str, limit: int = 5) -> list[dict]:
    """Get latest images for a repository."""
    cmd = [
        "aws", "ecr", "describe-images",
        "--repository-name", repository,
        "--query", f"imageDetails | sort_by(@, &imagePushedAt) | [-{limit}:]",
        "--output", "json"
    ]
    result = run_aws_command(cmd)
    return result if result else []


def format_timestamp(ts: str) -> str:
    """Format timestamp for display."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts[:16] if len(ts) > 16 else ts


def format_size(size_bytes: int) -> str:
    """Format size in human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def main():
    parser = argparse.ArgumentParser(description="ECR Image Comparison")
    parser.add_argument("--repository", "-r", help="Specific repository to check")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of images per repo")
    parser.add_argument("--filter", "-f", help="Filter repositories by name pattern")
    args = parser.parse_args()

    print("🐳 ECR Image Report")
    print("=" * 70)

    if args.repository:
        repos = [args.repository]
    else:
        repos = list_repositories()
        if args.filter:
            repos = [r for r in repos if args.filter.lower() in r.lower()]

    if not repos:
        print("No repositories found.")
        return

    print(f"Found {len(repos)} repositories\n")

    for repo in sorted(repos):
        print(f"\n📦 {repo}")
        print("-" * 50)

        images = get_latest_images(repo, args.limit)

        if not images:
            print("   No images found")
            continue

        for img in reversed(images):  # Show newest first
            tags = img.get("imageTags", ["<untagged>"])
            pushed = format_timestamp(img.get("imagePushedAt", ""))
            size = format_size(img.get("imageSizeInBytes", 0))
            digest = img.get("imageDigest", "")[:20]

            tag_str = ", ".join(tags[:3])
            if len(tags) > 3:
                tag_str += f" (+{len(tags)-3} more)"

            print(f"   {tag_str}")
            print(f"      Pushed: {pushed} | Size: {size} | {digest}...")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
