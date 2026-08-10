#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


HIGH_RISK_TAGS = {
    "destructive",
    "financial",
    "legal",
    "personnel",
    "production",
    "secrets",
    "security",
}
REQUIRED_FIELDS = {
    "action_type",
    "ambiguity_present",
    "reversible",
    "scope_confirmed",
    "precedent_count",
    "confidence",
    "explicit_send_authorization",
    "risk_tags",
}
MAX_PRECEDENT_COUNT = 1_000_000


def emit(action: str, confidence: float, reason: str) -> int:
    print(json.dumps({"action": action, "confidence": confidence, "reason": reason}))
    return 0


def valid_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        request = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return emit("escalate", 0.0, "invalid JSON input")
    except (OSError, UnicodeError):
        return emit("escalate", 0.0, "input file is unreadable")
    if not isinstance(request, dict):
        return emit("escalate", 0.0, "input must be a JSON object")

    missing_fields = sorted(REQUIRED_FIELDS.difference(request))
    if missing_fields:
        return emit(
            "escalate",
            0.0,
            f"missing required fields: {', '.join(missing_fields)}",
        )

    invalid_fields = []
    if not isinstance(request["action_type"], str) or not request["action_type"].strip():
        invalid_fields.append("action_type")
    for field in (
        "ambiguity_present",
        "explicit_send_authorization",
        "reversible",
        "scope_confirmed",
    ):
        if type(request[field]) is not bool:
            invalid_fields.append(field)
    if (
        type(request["precedent_count"]) is not int
        or not 0 <= request["precedent_count"] <= MAX_PRECEDENT_COUNT
    ):
        invalid_fields.append("precedent_count")
    if not valid_number(request["confidence"]) or not 0 <= request["confidence"] <= 1:
        invalid_fields.append("confidence")
    if not isinstance(request["risk_tags"], list) or any(
        not isinstance(tag, str) or not tag for tag in request["risk_tags"]
    ):
        invalid_fields.append("risk_tags")
    if invalid_fields:
        return emit(
            "escalate",
            0.0,
            f"invalid fields: {', '.join(sorted(invalid_fields))}",
        )

    risk_tags = set(request["risk_tags"])
    unknown_risks = risk_tags.difference(HIGH_RISK_TAGS)
    if unknown_risks:
        return emit(
            "escalate",
            request["confidence"],
            f"unknown risk tags require human review: {', '.join(sorted(unknown_risks))}",
        )
    matched_risks = HIGH_RISK_TAGS.intersection(risk_tags)
    if matched_risks:
        return emit(
            "escalate",
            request["confidence"],
            f"high-risk tags require human review: {', '.join(sorted(matched_risks))}",
        )
    if request["ambiguity_present"]:
        return emit("escalate", request["confidence"], "ambiguity requires human review")
    if (
        request.get("action_type") == "outbound_colleague_message"
        and request.get("explicit_send_authorization") is not True
    ):
        action = "draft"
        reason = "current send authorization is required for outbound communication"
    else:
        blockers = []
        if request["reversible"] is not True:
            blockers.append("action must be reversible")
        if request["scope_confirmed"] is not True:
            blockers.append("scope is not confirmed")
        if request["precedent_count"] < 1:
            blockers.append("no matching precedent")
        if request["confidence"] < 0.85:
            blockers.append("confidence is below 0.85")
        if blockers:
            action = "escalate"
            reason = "; ".join(blockers)
        else:
            action = "act"
            reason = "scoped reversible work matches prior decisions"
    return emit(action, request["confidence"], reason)


if __name__ == "__main__":
    raise SystemExit(main())
