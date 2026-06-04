#!/usr/bin/env python3
"""Extract Lev8 pressure-test cases from a CSV file."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="CSV file containing Lev8 cases")
    parser.add_argument("--limit", type=int, default=10, help="maximum non-empty cases to return")
    parser.add_argument(
        "--query-column",
        help="column to use as query; defaults to the last CSV column",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.csv_path).expanduser()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    headers = reader.fieldnames or []
    if not headers:
        raise SystemExit(f"No CSV header found: {path}")

    query_column = args.query_column or headers[-1]
    if query_column not in headers:
        raise SystemExit(f"Query column not found: {query_column}")

    selected = []
    non_empty = 0
    for record_index, row in enumerate(rows, start=1):
        query = (row.get(query_column) or "").strip()
        if not query:
            continue
        non_empty += 1
        if len(selected) >= args.limit:
            continue
        selected.append(
            {
                "case_index": len(selected) + 1,
                "record_index": record_index,
                "scenario_id": row.get("scenario_id", ""),
                "ID": row.get("ID", ""),
                "query": query,
                "query_preview": query if len(query) <= 160 else query[:157] + "...",
                "query_chars": len(query),
            }
        )

    payload = {
        "csv_path": str(path),
        "headers": headers,
        "logical_record_count": len(rows),
        "query_column": query_column,
        "non_empty_query_count": non_empty,
        "selected_count": len(selected),
        "selected": selected,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
