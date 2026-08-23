#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


HIGH_RISK_TAGS = {
    "destructive",
    "financial",
    "identity",
    "legal",
    "personnel",
    "permissions",
    "production",
    "secrets",
    "security",
}
SAFE_ACTION_CATEGORIES = {"local_reversible", "read_only"}
ACTION_CATEGORIES = SAFE_ACTION_CATEGORIES | HIGH_RISK_TAGS | {"outbound"}
KNOWN_ACTION_TYPES = {
    "local_code_edit": "local_reversible",
    "local_documentation_edit": "local_reversible",
    "local_reversible_change": "local_reversible",
    "outbound_colleague_message": "outbound",
    "read_only_analysis": "read_only",
    "read_only_check": "read_only",
    "read_only_inspection": "read_only",
}
ACTION_KEYWORDS = {
    "destructive": {
        "delete",
        "destroy",
        "drop",
        "overwrite",
        "prune",
        "purge",
        "remove",
        "truncate",
        "wipe",
    },
    "financial": {"buy", "pay", "purchase", "sell", "spend", "trade", "transfer"},
    "identity": {"impersonate", "identity", "sign_as"},
    "legal": {"contract", "legal"},
    "local_reversible": {
        "append",
        "create",
        "edit",
        "modify",
        "move",
        "mutate",
        "patch",
        "rename",
        "write",
    },
    "outbound": {"comment", "dm", "email", "message", "post", "publish", "reply", "send"},
    "permissions": {"access", "grant", "granted", "permission", "revoke", "role"},
    "personnel": {"fire", "hire", "personnel", "performance", "terminate"},
    "production": {"deploy", "prod", "production", "restart"},
    "secrets": {"credential", "keychain", "password", "private_key", "secret", "token"},
    "security": {"firewall", "security"},
}
SAFE_MUTATION_SCOPES = {
    "current repository policy",
    "current task",
    "current task and canonical skill only",
    "reviewed local runbook",
    "scheduled refresh contract",
}
PROTECTED_LOCAL_TARGETS = {
    "references/autonomy-policy.json",
    "references/decision-policy.md",
    "scripts/decision_gate.py",
    "scripts/privacy_check.py",
    "scripts/validate_source_manifest.py",
}
REQUIRED_FIELDS = {
    "action_category",
    "action_type",
    "ambiguity_present",
    "authorization_scope",
    "evidence_refs",
    "reversible",
    "scope_confirmed",
    "target",
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


def normalize_tokens(value: str) -> set[str]:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return set(normalized.split("_")) if normalized else set()


def semantic_categories(value: str) -> set[str]:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    tokens = normalize_tokens(value)
    categories = {
        category
        for category, keywords in ACTION_KEYWORDS.items()
        if tokens.intersection(keywords)
    }
    if "read_only" in normalized or "diagnosis_only" in normalized:
        categories.add("read_only")
    if "draft_only" in normalized:
        categories.add("draft_only")
    return categories


def classify_action(action_type: str) -> tuple[str | None, set[str]]:
    normalized = re.sub(r"[^a-z0-9]+", "_", action_type.lower()).strip("_")
    inferred_categories = semantic_categories(action_type)
    known_category = KNOWN_ACTION_TYPES.get(normalized)
    if known_category:
        inferred_categories.add(known_category)
    if inferred_categories.intersection(HIGH_RISK_TAGS):
        return None, inferred_categories
    if known_category in SAFE_ACTION_CATEGORIES | {"outbound"}:
        return known_category, inferred_categories
    return None, inferred_categories


def evidence_ref_exists(reference: str, skill_root: Path) -> bool:
    if reference == "current-request":
        return True
    prefix = "reference:"
    if not reference.startswith(prefix):
        return False
    relative = reference.removeprefix(prefix)
    if not relative:
        return False
    try:
        references_root = (skill_root / "references").resolve()
        candidate = (references_root / relative).resolve()
        return candidate.is_relative_to(references_root) and candidate.is_file()
    except (OSError, RuntimeError, ValueError):
        return False


def is_bounded_existing_local_file(target: str, workspace_root: Path) -> bool:
    try:
        candidate = Path(target)
        if candidate.is_absolute() or ".." in candidate.parts:
            return False
        root = workspace_root.resolve()
        resolved = (root / candidate).resolve()
        return resolved.is_relative_to(root) and resolved.is_file()
    except (OSError, RuntimeError, ValueError):
        return False


def is_protected_local_target(target: str) -> bool:
    return Path(target).as_posix() in PROTECTED_LOCAL_TARGETS


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
    if (
        not isinstance(request["action_category"], str)
        or request["action_category"] not in ACTION_CATEGORIES
    ):
        invalid_fields.append("action_category")
    if not isinstance(request["action_type"], str) or not request["action_type"].strip():
        invalid_fields.append("action_type")
    if not isinstance(request["authorization_scope"], str) or not request[
        "authorization_scope"
    ].strip():
        invalid_fields.append("authorization_scope")
    if not isinstance(request["target"], str) or not request["target"].strip():
        invalid_fields.append("target")
    if not isinstance(request["evidence_refs"], list) or not request["evidence_refs"] or any(
        not isinstance(reference, str) or not reference.strip()
        for reference in request["evidence_refs"]
    ):
        invalid_fields.append("evidence_refs")
    elif any(
        not evidence_ref_exists(reference, Path(__file__).resolve().parents[1])
        for reference in request["evidence_refs"]
    ):
        invalid_fields.append("evidence_refs")
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
    expected_category, action_semantics = classify_action(request["action_type"])
    target_semantics = semantic_categories(request["target"])
    scope_semantics = semantic_categories(request["authorization_scope"])
    semantic_risks = (
        action_semantics | target_semantics | scope_semantics
    ).intersection(HIGH_RISK_TAGS)
    matched_risks = HIGH_RISK_TAGS.intersection(risk_tags) | semantic_risks
    if request["action_category"] in HIGH_RISK_TAGS:
        matched_risks.add(request["action_category"])
    if matched_risks:
        return emit(
            "escalate",
            request["confidence"],
            f"high-risk tags require human review: {', '.join(sorted(matched_risks))}",
        )
    if expected_category is None:
        return emit(
            "escalate",
            request["confidence"],
            "action type is not in the explicit low-risk or outbound allowlist",
        )
    if request["action_category"] != expected_category:
        return emit(
            "escalate",
            request["confidence"],
            f"action category conflicts with action semantics: expected {expected_category}",
        )
    if request["ambiguity_present"]:
        return emit("escalate", request["confidence"], "ambiguity requires human review")
    allowed_semantics = {expected_category}
    if expected_category == "outbound":
        allowed_semantics.add("draft_only")
    semantic_conflicts = (target_semantics | scope_semantics).difference(allowed_semantics)
    if semantic_conflicts:
        return emit(
            "escalate",
            request["confidence"],
            "target or authorization scope conflicts with the declared action category: "
            + ", ".join(sorted(semantic_conflicts)),
        )
    if expected_category == "outbound":
        if request.get("explicit_send_authorization") is not True:
            action = "draft"
            reason = "current send authorization is required for outbound communication"
        else:
            action = "escalate"
            reason = "live human authorization must be verified outside the autonomous twin gate"
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
        if expected_category == "local_reversible":
            if request["authorization_scope"] not in SAFE_MUTATION_SCOPES:
                blockers.append("authorization scope is not approved for local mutation")
            if not is_bounded_existing_local_file(request["target"], Path.cwd()):
                blockers.append(
                    "local mutation target must be an existing relative file inside the current workspace"
                )
            if is_protected_local_target(request["target"]):
                blockers.append("autonomous mutation of a safety gate or policy file is prohibited")
            if not any(
                reference.startswith("reference:") for reference in request["evidence_refs"]
            ):
                blockers.append("local mutation requires an existing reference-file precedent")
        if blockers:
            action = "escalate"
            reason = "; ".join(blockers)
        else:
            action = "act"
            reason = "scoped reversible work matches prior decisions and cited evidence"
    return emit(action, request["confidence"], reason)


if __name__ == "__main__":
    raise SystemExit(main())
