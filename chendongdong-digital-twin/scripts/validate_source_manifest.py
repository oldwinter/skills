#!/usr/bin/env python3
import json
import sys
from pathlib import Path


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
    print(json.dumps({"ok": not errors, "errors": errors}))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
