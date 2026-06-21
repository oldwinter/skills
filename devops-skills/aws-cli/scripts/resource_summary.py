#!/usr/bin/env python3
"""
AWS Resource Summary Script

Generates a quick overview of key AWS resources in the account.
Usage: python3 resource_summary.py [--region REGION]
"""

import subprocess
import json
import sys
import argparse


def run_aws_command(cmd: list) -> dict | list | None:
    """Execute AWS CLI command and return parsed JSON output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return None


def get_ec2_summary(region: str) -> dict:
    """Get EC2 instance summary."""
    cmd = [
        "aws", "ec2", "describe-instances",
        "--region", region,
        "--query", "Reservations[].Instances[].State.Name",
        "--output", "json"
    ]
    result = run_aws_command(cmd)
    if result:
        states = {}
        for state in result:
            states[state] = states.get(state, 0) + 1
        return states
    return {}


def get_s3_bucket_count() -> int:
    """Get total S3 bucket count."""
    cmd = ["aws", "s3api", "list-buckets", "--query", "length(Buckets)"]
    result = run_aws_command(cmd)
    return result if isinstance(result, int) else 0


def get_rds_summary(region: str) -> dict:
    """Get RDS instance summary."""
    cmd = [
        "aws", "rds", "describe-db-instances",
        "--region", region,
        "--query", "DBInstances[].DBInstanceStatus",
        "--output", "json"
    ]
    result = run_aws_command(cmd)
    if result:
        states = {}
        for state in result:
            states[state] = states.get(state, 0) + 1
        return states
    return {}


def get_lambda_count(region: str) -> int:
    """Get Lambda function count."""
    cmd = [
        "aws", "lambda", "list-functions",
        "--region", region,
        "--query", "length(Functions)"
    ]
    result = run_aws_command(cmd)
    return result if isinstance(result, int) else 0


def get_ecs_cluster_count(region: str) -> int:
    """Get ECS cluster count."""
    cmd = [
        "aws", "ecs", "list-clusters",
        "--region", region,
        "--query", "length(clusterArns)"
    ]
    result = run_aws_command(cmd)
    return result if isinstance(result, int) else 0


def get_eks_cluster_count(region: str) -> int:
    """Get EKS cluster count."""
    cmd = [
        "aws", "eks", "list-clusters",
        "--region", region,
        "--query", "length(clusters)"
    ]
    result = run_aws_command(cmd)
    return result if isinstance(result, int) else 0


def main():
    parser = argparse.ArgumentParser(description="AWS Resource Summary")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    args = parser.parse_args()

    print(f"📊 AWS Resource Summary ({args.region})")
    print("=" * 50)

    # EC2
    ec2 = get_ec2_summary(args.region)
    print(f"\n🖥️  EC2 Instances:")
    if ec2:
        for state, count in sorted(ec2.items()):
            print(f"   {state}: {count}")
    else:
        print("   No instances or unable to fetch")

    # S3
    s3_count = get_s3_bucket_count()
    print(f"\n📦 S3 Buckets: {s3_count}")

    # RDS
    rds = get_rds_summary(args.region)
    print(f"\n🗄️  RDS Instances:")
    if rds:
        for state, count in sorted(rds.items()):
            print(f"   {state}: {count}")
    else:
        print("   No instances or unable to fetch")

    # Lambda
    lambda_count = get_lambda_count(args.region)
    print(f"\n⚡ Lambda Functions: {lambda_count}")

    # ECS
    ecs_count = get_ecs_cluster_count(args.region)
    print(f"\n🐳 ECS Clusters: {ecs_count}")

    # EKS
    eks_count = get_eks_cluster_count(args.region)
    print(f"\n☸️  EKS Clusters: {eks_count}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
