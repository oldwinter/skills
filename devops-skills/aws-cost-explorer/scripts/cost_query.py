#!/usr/bin/env python3
"""
AWS Cost Explorer 查询脚本
支持按服务粒度和细分资源类型查询费用
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional


def get_date_range(days_ago: int) -> tuple[str, str]:
    """计算日期范围"""
    target_date = datetime.now() - timedelta(days=days_ago)
    start_date = target_date.strftime("%Y-%m-%d")
    end_date = (target_date + timedelta(days=1)).strftime("%Y-%m-%d")
    return start_date, end_date


def run_aws_command(cmd: list[str]) -> dict:
    """执行 AWS CLI 命令并返回 JSON 结果"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"AWS CLI 错误: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)


def query_by_service(start_date: str, end_date: str, min_cost: float = 0) -> list[dict]:
    """按服务查询费用"""
    cmd = [
        "aws", "ce", "get-cost-and-usage",
        "--time-period", f"Start={start_date},End={end_date}",
        "--granularity", "DAILY",
        "--metrics", "UnblendedCost",
        "--group-by", "Type=DIMENSION,Key=SERVICE",
        "--output", "json"
    ]

    data = run_aws_command(cmd)
    results = []

    for group in data.get("ResultsByTime", [{}])[0].get("Groups", []):
        service = group["Keys"][0]
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        if amount >= min_cost:
            results.append({
                "service": service,
                "amount": amount
            })

    return sorted(results, key=lambda x: x["amount"], reverse=True)


def query_by_usage_type(start_date: str, end_date: str, service: str, min_cost: float = 0) -> list[dict]:
    """按使用类型查询特定服务的费用明细"""
    filter_expr = json.dumps({
        "Dimensions": {
            "Key": "SERVICE",
            "Values": [service]
        }
    })

    cmd = [
        "aws", "ce", "get-cost-and-usage",
        "--time-period", f"Start={start_date},End={end_date}",
        "--granularity", "DAILY",
        "--metrics", "UnblendedCost",
        "--filter", filter_expr,
        "--group-by", "Type=DIMENSION,Key=USAGE_TYPE",
        "--output", "json"
    ]

    data = run_aws_command(cmd)
    results = []

    for group in data.get("ResultsByTime", [{}])[0].get("Groups", []):
        usage_type = group["Keys"][0]
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        if amount >= min_cost:
            results.append({
                "usage_type": usage_type,
                "amount": amount
            })

    return sorted(results, key=lambda x: x["amount"], reverse=True)


def query_all_usage_types(start_date: str, end_date: str, min_cost: float = 0) -> list[dict]:
    """查询所有服务的使用类型明细"""
    cmd = [
        "aws", "ce", "get-cost-and-usage",
        "--time-period", f"Start={start_date},End={end_date}",
        "--granularity", "DAILY",
        "--metrics", "UnblendedCost",
        "--group-by", "Type=DIMENSION,Key=SERVICE", "Type=DIMENSION,Key=USAGE_TYPE",
        "--output", "json"
    ]

    data = run_aws_command(cmd)
    results = []

    for group in data.get("ResultsByTime", [{}])[0].get("Groups", []):
        service = group["Keys"][0]
        usage_type = group["Keys"][1]
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        if amount >= min_cost:
            results.append({
                "service": service,
                "usage_type": usage_type,
                "amount": amount
            })

    return sorted(results, key=lambda x: x["amount"], reverse=True)


def format_currency(amount: float) -> str:
    """格式化货币显示"""
    return f"${amount:.2f}"


def print_service_report(results: list[dict], date: str):
    """打印服务级别报告"""
    total = sum(r["amount"] for r in results)

    print(f"\n{'='*70}")
    print(f"📊 AWS 费用报告 - {date} (按服务)")
    print(f"{'='*70}")
    print(f"{'排名':<6}{'服务':<50}{'费用 (USD)':>12}")
    print(f"{'-'*70}")

    for i, r in enumerate(results, 1):
        print(f"{i:<6}{r['service']:<50}{format_currency(r['amount']):>12}")

    print(f"{'-'*70}")
    print(f"{'总计':<56}{format_currency(total):>12}")
    print()


def print_usage_type_report(results: list[dict], date: str, service: Optional[str] = None):
    """打印使用类型级别报告"""
    total = sum(r["amount"] for r in results)

    title = f"按使用类型 - {service}" if service else "按使用类型 (全部服务)"

    print(f"\n{'='*90}")
    print(f"📊 AWS 费用报告 - {date} ({title})")
    print(f"{'='*90}")

    if service:
        print(f"{'排名':<6}{'使用类型':<60}{'费用 (USD)':>12}")
        print(f"{'-'*90}")
        for i, r in enumerate(results, 1):
            print(f"{i:<6}{r['usage_type']:<60}{format_currency(r['amount']):>12}")
    else:
        print(f"{'排名':<6}{'服务':<35}{'使用类型':<35}{'费用 (USD)':>12}")
        print(f"{'-'*90}")
        for i, r in enumerate(results, 1):
            svc = r['service'][:33] + '..' if len(r['service']) > 35 else r['service']
            ut = r['usage_type'][:33] + '..' if len(r['usage_type']) > 35 else r['usage_type']
            print(f"{i:<6}{svc:<35}{ut:<35}{format_currency(r['amount']):>12}")

    print(f"{'-'*90}")
    print(f"{'总计':<76}{format_currency(total):>12}")
    print()


def output_json(results: list[dict], date: str):
    """输出 JSON 格式"""
    output = {
        "date": date,
        "items": results,
        "total": sum(r["amount"] for r in results)
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="AWS Cost Explorer 费用查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查询前天按服务的费用 (默认)
  python cost_query.py

  # 查询昨天按服务的费用，只显示高于 $5 的
  python cost_query.py --days-ago 1 --min-cost 5

  # 查询指定日期按服务的费用
  python cost_query.py --date 2026-01-15

  # 查询特定服务的细分费用
  python cost_query.py --service "Amazon OpenSearch Service" --min-cost 1

  # 查询所有服务的细分费用
  python cost_query.py --detailed --min-cost 5

  # 输出 JSON 格式
  python cost_query.py --json --min-cost 5
        """
    )

    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument(
        "--days-ago", "-d",
        type=int,
        default=2,
        help="查询几天前的费用 (默认: 2，即前天)"
    )
    date_group.add_argument(
        "--date",
        type=str,
        help="查询指定日期的费用 (格式: YYYY-MM-DD)"
    )

    parser.add_argument(
        "--min-cost", "-m",
        type=float,
        default=0,
        help="最小费用阈值，只显示高于此值的项目 (默认: 0)"
    )

    parser.add_argument(
        "--service", "-s",
        type=str,
        help="查询特定服务的细分费用"
    )

    parser.add_argument(
        "--detailed",
        action="store_true",
        help="显示所有服务的细分使用类型"
    )

    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="输出 JSON 格式"
    )

    args = parser.parse_args()

    # 确定日期范围
    if args.date:
        try:
            target = datetime.strptime(args.date, "%Y-%m-%d")
            start_date = args.date
            end_date = (target + timedelta(days=1)).strftime("%Y-%m-%d")
        except ValueError:
            print(f"错误: 日期格式无效 '{args.date}'，请使用 YYYY-MM-DD 格式", file=sys.stderr)
            sys.exit(1)
    else:
        start_date, end_date = get_date_range(args.days_ago)

    # 执行查询
    if args.service:
        results = query_by_usage_type(start_date, end_date, args.service, args.min_cost)
        if args.json:
            output_json(results, start_date)
        else:
            print_usage_type_report(results, start_date, args.service)
    elif args.detailed:
        results = query_all_usage_types(start_date, end_date, args.min_cost)
        if args.json:
            output_json(results, start_date)
        else:
            print_usage_type_report(results, start_date)
    else:
        results = query_by_service(start_date, end_date, args.min_cost)
        if args.json:
            output_json(results, start_date)
        else:
            print_service_report(results, start_date)


if __name__ == "__main__":
    main()
