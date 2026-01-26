#!/usr/bin/env python3
"""
Kubernetes Cluster Status Summary

Generates a quick overview of cluster health across all environments.
Usage: python3 cluster_status.py [--env ENV]

ENV options: all, prod, staging, local (default: all)
"""

import subprocess
import json
import argparse
from typing import Optional


# Cluster configurations matching shell aliases
CLUSTERS = {
    "prod": {
        "name": "Production (k1)",
        "context": "arn:aws:eks:us-east-1:830101142436:cluster/production",
        "namespace": "production",
        "alias": "k1"
    },
    "staging": {
        "name": "Staging (k2)",
        "context": "arn:aws:eks:us-east-1:830101142436:cluster/production",
        "namespace": "staging",
        "alias": "k2"
    },
    "local": {
        "name": "Local K3s (k)",
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


def get_pod_summary(context: str, namespace: str) -> dict:
    """Get pod status summary."""
    output = run_kubectl(context, namespace, [
        "get", "pods", "-o", "json"
    ])

    if not output:
        return {"error": "Unable to fetch pods"}

    try:
        data = json.loads(output)
        pods = data.get("items", [])

        summary = {
            "total": len(pods),
            "running": 0,
            "pending": 0,
            "failed": 0,
            "other": 0,
            "restarts": 0
        }

        for pod in pods:
            phase = pod.get("status", {}).get("phase", "Unknown")
            if phase == "Running":
                summary["running"] += 1
            elif phase == "Pending":
                summary["pending"] += 1
            elif phase == "Failed":
                summary["failed"] += 1
            else:
                summary["other"] += 1

            # Count restarts
            for cs in pod.get("status", {}).get("containerStatuses", []):
                summary["restarts"] += cs.get("restartCount", 0)

        return summary
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def get_deployment_summary(context: str, namespace: str) -> dict:
    """Get deployment status summary."""
    output = run_kubectl(context, namespace, [
        "get", "deployments", "-o", "json"
    ])

    if not output:
        return {"error": "Unable to fetch deployments"}

    try:
        data = json.loads(output)
        deployments = data.get("items", [])

        summary = {
            "total": len(deployments),
            "ready": 0,
            "progressing": 0,
            "degraded": 0
        }

        for deploy in deployments:
            desired = deploy.get("spec", {}).get("replicas", 0)
            available = deploy.get("status", {}).get("availableReplicas", 0)

            if available == desired:
                summary["ready"] += 1
            elif available > 0:
                summary["progressing"] += 1
            else:
                summary["degraded"] += 1

        return summary
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def get_node_summary(context: str) -> dict:
    """Get node status summary (cluster-wide, not namespace-scoped)."""
    cmd = ["kubectl", f"--context={context}", "get", "nodes", "-o", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": "Unable to fetch nodes"}

        data = json.loads(result.stdout)
        nodes = data.get("items", [])

        summary = {
            "total": len(nodes),
            "ready": 0,
            "not_ready": 0
        }

        for node in nodes:
            conditions = node.get("status", {}).get("conditions", [])
            is_ready = any(
                c.get("type") == "Ready" and c.get("status") == "True"
                for c in conditions
            )
            if is_ready:
                summary["ready"] += 1
            else:
                summary["not_ready"] += 1

        return summary
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return {"error": "Unable to fetch nodes"}


def print_cluster_status(env_key: str, config: dict):
    """Print status for a single cluster."""
    print(f"\n{'='*60}")
    print(f"📍 {config['name']}")
    print(f"   Context: {config['context']}")
    print(f"   Namespace: {config['namespace']}")
    print(f"{'='*60}")

    # Pods
    pods = get_pod_summary(config['context'], config['namespace'])
    if "error" in pods:
        print(f"\n🔴 Pods: {pods['error']}")
    else:
        status_icon = "🟢" if pods['failed'] == 0 and pods['pending'] == 0 else "🟡"
        if pods['failed'] > 0:
            status_icon = "🔴"
        print(f"\n{status_icon} Pods: {pods['running']}/{pods['total']} running")
        if pods['pending'] > 0:
            print(f"   ⏳ Pending: {pods['pending']}")
        if pods['failed'] > 0:
            print(f"   ❌ Failed: {pods['failed']}")
        if pods['restarts'] > 0:
            print(f"   🔄 Total restarts: {pods['restarts']}")

    # Deployments
    deploys = get_deployment_summary(config['context'], config['namespace'])
    if "error" in deploys:
        print(f"\n🔴 Deployments: {deploys['error']}")
    else:
        status_icon = "🟢" if deploys['degraded'] == 0 else "🔴"
        print(f"\n{status_icon} Deployments: {deploys['ready']}/{deploys['total']} ready")
        if deploys['progressing'] > 0:
            print(f"   🔄 Progressing: {deploys['progressing']}")
        if deploys['degraded'] > 0:
            print(f"   ❌ Degraded: {deploys['degraded']}")

    # Nodes (only show once per unique context)
    nodes = get_node_summary(config['context'])
    if "error" not in nodes:
        status_icon = "🟢" if nodes['not_ready'] == 0 else "🔴"
        print(f"\n{status_icon} Nodes: {nodes['ready']}/{nodes['total']} ready")


def main():
    parser = argparse.ArgumentParser(description="Kubernetes Cluster Status Summary")
    parser.add_argument(
        "--env", "-e",
        choices=["all", "prod", "staging", "local"],
        default="all",
        help="Environment to check (default: all)"
    )
    args = parser.parse_args()

    print("🔍 Kubernetes Cluster Status Report")
    print(f"{'='*60}")

    if args.env == "all":
        for env_key, config in CLUSTERS.items():
            print_cluster_status(env_key, config)
    else:
        config = CLUSTERS.get(args.env)
        if config:
            print_cluster_status(args.env, config)
        else:
            print(f"Unknown environment: {args.env}")
            return 1

    print(f"\n{'='*60}")
    print("✅ Status check complete")
    return 0


if __name__ == "__main__":
    exit(main())
