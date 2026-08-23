#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


EXPECTED_WINDOW = {
    "start": "2026-02-10",
    "end": "2026-08-10",
    "timezone": "Asia/Shanghai",
}
REQUIRED_SOURCES = ("notes", "gitlab", "lark_im")
REQUIRED_DIMENSIONS = (
    "writings",
    "conversations",
    "expression_dna",
    "external_views",
    "decisions",
    "timeline",
)
REFRESH_STATUSES = {"complete", "partial", "blocked"}
REFRESH_INVENTORY_FIELDS = (
    "visible_tasks",
    "manual_codex_tasks",
    "chatgpt_conversations",
    "automation_runs",
    "delegated_tasks",
    "read_errors",
)
REFRESH_COVERAGE_FIELDS = {
    "active_list_limit": "positive_integer",
    "active_list_reached_window_start": "boolean",
    "active_list_saturated": "boolean",
    "archived_pagination_complete_to_window": "boolean",
    "visible_hosts": "positive_integer",
}
PROMOTION_POLICIES = {
    "blocked": "no_model_update",
    "complete": "full_model_update",
    "partial": "reinforce_or_tentative_only",
}
REFRESH_DURATION = timedelta(days=7)
REFRESH_TIMEZONE = ZoneInfo("Asia/Shanghai")


def parse_aware_datetime(value: object, field: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{field} must be an ISO-8601 string")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{field} must be a valid ISO-8601 datetime")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        errors.append(f"{field} must include a timezone offset")
        return None
    return parsed


def main() -> int:
    manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = []
    if manifest.get("raw_content_stored") is not False:
        errors.append("raw_content_stored must be false")
    if manifest.get("window") != EXPECTED_WINDOW:
        errors.append("window must be 2026-02-10..2026-08-10 Asia/Shanghai")

    sources = manifest.get("sources", {})
    for source in REQUIRED_SOURCES:
        if source not in sources:
            errors.append(f"missing required source: {source}")

    dimensions = manifest.get("research_dimensions", {})
    for dimension in REQUIRED_DIMENSIONS:
        if dimension not in dimensions:
            errors.append(f"missing research dimension: {dimension}")
        elif not isinstance(dimensions[dimension], int) or dimensions[dimension] < 1:
            errors.append(f"research dimension must be nonempty: {dimension}")

    refresh = manifest.get("latest_refresh")
    if refresh is not None:
        if not isinstance(refresh, dict):
            errors.append("latest_refresh must be an object")
        else:
            if refresh.get("status") not in REFRESH_STATUSES:
                errors.append("latest_refresh status must be complete, partial, or blocked")
            if refresh.get("raw_content_stored") is not False:
                errors.append("latest_refresh raw_content_stored must be false")

            refresh_window = refresh.get("window", {})
            if not isinstance(refresh_window, dict):
                errors.append("latest_refresh window must be an object")
                refresh_window = {}
            if refresh_window.get("timezone") != "Asia/Shanghai":
                errors.append("latest_refresh timezone must be Asia/Shanghai")
            refresh_start = parse_aware_datetime(
                refresh_window.get("start"), "latest_refresh window start", errors
            )
            refresh_end = parse_aware_datetime(
                refresh_window.get("end"), "latest_refresh window end", errors
            )
            run_at = parse_aware_datetime(refresh.get("run_at"), "latest_refresh run_at", errors)
            if refresh_start and refresh_end and refresh_start >= refresh_end:
                errors.append("latest_refresh window start must be before end")
            if refresh_start and refresh_start.utcoffset() != refresh_start.astimezone(
                REFRESH_TIMEZONE
            ).utcoffset():
                errors.append("latest_refresh window start offset must match Asia/Shanghai")
            if refresh_end and refresh_end.utcoffset() != refresh_end.astimezone(
                REFRESH_TIMEZONE
            ).utcoffset():
                errors.append("latest_refresh window end offset must match Asia/Shanghai")
            if refresh_start and refresh_end and refresh_end - refresh_start != REFRESH_DURATION:
                errors.append("latest_refresh half-open window must span exactly seven days")
            if refresh_end and run_at and refresh_end != run_at:
                errors.append("latest_refresh run_at must equal the half-open window end")
            if run_at and run_at.utcoffset() != run_at.astimezone(REFRESH_TIMEZONE).utcoffset():
                errors.append("latest_refresh run_at offset must match Asia/Shanghai")

            inventory = refresh.get("inventory", {})
            if not isinstance(inventory, dict):
                errors.append("latest_refresh inventory must be an object")
                inventory = {}
            for field in REFRESH_INVENTORY_FIELDS:
                value = inventory.get(field)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    errors.append(f"latest_refresh inventory field must be a nonnegative integer: {field}")
            classified = sum(
                inventory.get(field, 0)
                for field in (
                    "manual_codex_tasks",
                    "chatgpt_conversations",
                    "automation_runs",
                    "delegated_tasks",
                )
                if isinstance(inventory.get(field, 0), int)
            )
            if inventory.get("visible_tasks") != classified:
                errors.append("latest_refresh visible_tasks must equal classified task counts")

            coverage = refresh.get("coverage", {})
            if not isinstance(coverage, dict):
                errors.append("latest_refresh coverage must be an object")
                coverage = {}
            for field, expected_type in REFRESH_COVERAGE_FIELDS.items():
                value = coverage.get(field)
                if expected_type == "boolean" and type(value) is not bool:
                    errors.append(f"latest_refresh coverage field must be boolean: {field}")
                if expected_type == "positive_integer" and (
                    type(value) is not int or value < 1
                ):
                    errors.append(
                        f"latest_refresh coverage field must be a positive integer: {field}"
                    )
            status = refresh.get("status")
            expected_promotion = PROMOTION_POLICIES.get(status)
            if expected_promotion and coverage.get("promotion_policy") != expected_promotion:
                errors.append(
                    f"latest_refresh promotion_policy for {status} must be {expected_promotion}"
                )
            if status == "complete" and inventory.get("read_errors") != 0:
                errors.append("complete latest_refresh must have zero read_errors")
            if status == "complete" and coverage.get(
                "archived_pagination_complete_to_window"
            ) is not True:
                errors.append("complete latest_refresh requires complete archived pagination")
            if coverage.get("active_list_saturated") is True and refresh.get("status") == "complete":
                if coverage.get("active_list_reached_window_start") is not True:
                    errors.append("saturated active listing cannot be complete before reaching the window start")
    print(json.dumps({"ok": not errors, "errors": errors}))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
