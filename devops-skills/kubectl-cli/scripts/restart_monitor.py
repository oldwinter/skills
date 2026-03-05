#!/usr/bin/env python3
"""
Pod Restart Monitor

Monitors pods with high restart counts across environments.
Usage: python3 restart_monitor.py [--threshold N] [--env ENV]

Options:
  --threshold N   Alert on pods with N or more restarts (default: 3)
  --env ENV       Environment to check: all, prod, staging, local (default: all)
"""

import subprocess
import json
import argparse
from datetime import datetime
from typing import Optional


CLUSTERS = {
    "prod": {
        "name": "Production",
        "context": "arn:aws:eks:us-east-1:830101142436:cluster/production",
        "namespace": "production",
        "alias": "k1"
    },
    "staging": {
        "name": "Staging",
        "context": "arn:aws:eks:us-east-1:830101142436:cluster/production",
        "namespace": "staging",
        "alias": "k2"
    },
    "local": {
        "name": "Local K3s",
        "context": "k3s-117",
        "namespace": "simplex",
        "alias": "k"
    }
}


def run_kubectl(context: str, namespace: str, args: list) -> Optional[str]:
    """Execute kubectl command and return output."""
    cmd = ["kubectl", f"--context={context}", f"-n={namespace}"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except (subprocess.TimeoutExpired, Exception):
        return None


def get_pods_with_restarts(context: str, namespace: str, threshold: int) -> list:
    """Get pods with restart count >= threshold."""
    output = run_kubectl(context, namespace, ["get", "pods", "-o", "json"])

    if not output:
        return []

    try:
        data = json.loads(output)
        pods = data.get("items", [])

        results = []
        for pod in pods:
            name = pod.get("metadata", {}).get("name", "unknown")
            container_statuses = pod.get("status", {}).get("containerStatuses", [])

            total_restarts = 0
            last_restart = None

            for cs in container_statuses:
                restarts = cs.get("restartCount", 0)
                total_restarts += restarts

                # Get last termination time
                last_state = cs.get("lastState", {})
                terminated = last_state.get("terminated", {})
                if terminated:
                    finished = terminated.get("finishedAt")
                    if finished:
                        try:
                            dt = datetime.fromisoformat(finished.replace("Z", "+00:00"))
                            if last_restart is None or dt > last_restart:
                                last_restart = dt
                        except ValueError:
                            pass

            if total_restarts >= threshold:
                results.append({
                    "name": name,
                    "restarts": total_restarts,
                    "last_restart": last_restart,
                    "status": pod.get("status", {}).get("phase", "Unknown")
                })

        return sorted(results, key=lambda x: x["restarts"], reverse=True)
    except json.JSONDecodeError:
        return []


def format_time_ago(dt: Optional[datetime]) -> str:
    """Format datetime as relative time."""
    if dt is None:
        return "N/A"

    now = datetime.now(dt.tzinfo)
    delta = now - dt

    if delta.days > 0:
        return f"{delta.days}d ago"
    elif delta.seconds >= 3600:
        return f"{delta.seconds // 3600}h ago"
    elif delta.seconds >= 60:
        return f"{delta.seconds // 60}m ago"
    else:
        return "just now"


def check_environment(env_key: str, config: dict, threshold: int) -> int:
    """Check a single environment and return count of problematic pods."""
    print(f"\n📍 {config['name']} ({config['alias']})")
    print("-" * 50)

    pods = get_pods_with_restarts(config['context'], config['namespace'], threshold)

    if not pods:
        print(f"   ✅ No pods with {threshold}+ restarts")
        return 0

    print(f"   ⚠️  Found {len(pods)} pod(s) with {threshold}+ restarts:\n")

    for pod in pods:
        icon = "🔴" if pod['restarts'] >= 10 else "🟡"
        last = format_time_ago(pod['last_restart'])
        print(f"   {icon} {pod['name']}")
        print(f"      Restarts: {pod['restarts']} | Last: {last} | Status: {pod['status']}")

    return len(pods)


def main():
    parser = argparse.ArgumentParser(description="Pod Restart Monitor")
    parser.add_argument(
        "--threshold", "-t",
        type=int,
        default=3,
        help="Alert on pods with N or more restarts (default: 3)"
    )
    parser.add_argument(
        "--env", "-e",
        choices=["all", "prod", "staging", "local"],
        default="all",
        help="Environment to check (default: all)"
    )
    args = parser.parse_args()

    print("🔄 Pod Restart Monitor")
    print(f"   Threshold: {args.threshold}+ restarts")
    print("=" * 50)

    total_issues = 0

    if args.env == "all":
        for env_key, config in CLUSTERS.items():
            total_issues += check_environment(env_key, config, args.threshold)
    else:
        config = CLUSTERS.get(args.env)
        if config:
            total_issues += check_environment(args.env, config, args.threshold)
        else:
            print(f"Unknown environment: {args.env}")
            return 1

    print("\n" + "=" * 50)
    if total_issues > 0:
        print(f"⚠️  Total: {total_issues} pod(s) need attention")
    else:
        print("✅ All pods healthy")

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    exit(main())
