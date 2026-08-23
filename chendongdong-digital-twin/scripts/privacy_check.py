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
SKIP_PARTS = {"__pycache__", "tests"}
EXPECTED_POLICY = {
    "human_override": True,
    "identity_claim": "simulation",
    "incomplete_refresh_policy": "tentative_only",
    "irreversible_default": "escalate",
    "one_off_approval_is_precedent": False,
    "outbound_default": "draft",
    "raw_content_stored": False,
    "scheduled_refresh_external_actions": "escalate",
}
CREDENTIAL_PATTERNS = (
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{16,}={0,2}\b", re.IGNORECASE),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"glpat-[A-Za-z0-9_-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:oc|om|ou)_[A-Za-z0-9]{12,}\b"),
)
RAW_CORPUS_PATTERNS = (
    re.compile(r'"type"\s*:\s*"(?:agentMessage|userMessage)"'),
    re.compile(r"<response-annotations>"),
    re.compile(r'"(?:message_text|raw_content|raw_messages)"\s*:'),
    re.compile(r'"(?:messages|turns)"\s*:\s*\['),
    re.compile(r'"role"\s*:\s*"(?:assistant|user)"'),
    re.compile(r"(?m)^\s*(?:message_text|raw_content|raw_messages)\s*:"),
    re.compile(r"(?mi)^\s*(?:assistant|user|助手|用户)\s*:\s+\S"),
)
PROFILE_PII_PATTERNS = (
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("private network address", re.compile(r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b")),
    ("absolute home path", re.compile(r"/(?:Users|home)/[^/\s]+(?:/|(?=[\s\"']))")),
    ("mainland China mobile number", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("mainland China identity number", re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)")),
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
            findings.append(f"non-UTF-8 file requires privacy review: {relative}")
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
        if relative != Path("scripts/privacy_check.py") and any(
            pattern.search(text) for pattern in RAW_CORPUS_PATTERNS
        ):
            findings.append(f"raw conversation pattern in {relative}")
        if relative != Path("scripts/privacy_check.py"):
            for label, pattern in PROFILE_PII_PATTERNS:
                if pattern.search(text):
                    findings.append(f"{label} in {relative}")
    return findings


def main() -> int:
    root = Path(sys.argv[1])
    findings = scan_tree(root)
    try:
        policy = json.loads(
            (root / "references" / "autonomy-policy.json").read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError, UnicodeError):
        policy = {}
        findings.append("autonomy policy is missing, unreadable, or invalid JSON")
    if not isinstance(policy, dict):
        policy = {}
        findings.append("autonomy policy must be a JSON object")
    for field, expected in EXPECTED_POLICY.items():
        if policy.get(field) != expected:
            findings.append(f"unsafe autonomy policy field: {field}")
    result = {"ok": not findings, **policy, "findings": findings}
    print(json.dumps(result))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
