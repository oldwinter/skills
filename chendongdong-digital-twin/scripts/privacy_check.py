#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


FORBIDDEN_FIELDS = {
    "access_token",
    "email_body",
    "message_text",
    "private_key",
    "raw_content",
    "raw_messages",
    "refresh_token",
}
FORBIDDEN_SUFFIXES = {".db", ".eml", ".jsonl", ".mbox", ".sqlite", ".zip"}
SKIP_PARTS = {"__pycache__", "evidence", "tests"}
CREDENTIAL_PATTERNS = (
    re.compile(r"glpat-[A-Za-z0-9_-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:oc|om|ou)_[A-Za-z0-9]{12,}\b"),
)


def walk_json_fields(value: object) -> set[str]:
    fields: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            fields.add(str(key))
            fields.update(walk_json_fields(child))
    elif isinstance(value, list):
        for child in value:
            fields.update(walk_json_fields(child))
    return fields


def scan_tree(root: Path) -> list[str]:
    findings = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in SKIP_PARTS for part in relative.parts) or not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"forbidden raw-data file: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix.lower() == ".json":
            try:
                fields = walk_json_fields(json.loads(text))
            except json.JSONDecodeError:
                fields = set()
            for field in sorted(FORBIDDEN_FIELDS.intersection(fields)):
                findings.append(f"forbidden field: {field} in {relative}")
        if any(pattern.search(text) for pattern in CREDENTIAL_PATTERNS):
            findings.append(f"credential pattern in {relative}")
    return findings


def main() -> int:
    root = Path(sys.argv[1])
    policy = json.loads(
        (root / "references" / "autonomy-policy.json").read_text(encoding="utf-8")
    )
    findings = scan_tree(root)
    result = {"ok": not findings, **policy, "findings": findings}
    print(json.dumps(result))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
