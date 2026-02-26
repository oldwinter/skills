# Checklists

Use this before you circulate a PRD Pack.

## PRD Pack — universal checklist
- Narrative: problem + user + why now are clear in plain language
- Scope: goals/non-goals/out of scope are explicit (no “scope by omission”)
- Requirements: numbered (R1…Rn) and testable; must/should/could is clear
- Metrics: each goal has success metrics; guardrails are defined
- Measurement: each metric has an owner and a realistic data source
- Rollout: launch tiers, eligibility, and rollback plan are included
- Decision clarity: what needs approval is explicit; open questions are listed
- Craft: consistent terminology, readable structure, minimal fluff
- Safety: no secrets/credentials; privacy/policy constraints are acknowledged

## PR/FAQ checklist (if included)
- Press release is customer-readable (no internal jargon)
- The “how it works” section is high level but concrete
- FAQs address: why now, alternatives, out of scope, risks, success metrics
- Hypothetical release date is included and feels plausible

## AI add-ons checklist (if AI feature)
- Prompt Set includes versioning, output contract, and examples (2 good + 1 bad)
- Eval Spec includes: test set, judge prompt, scoring, thresholds, and critical failures
- Must-not-do behaviors are explicit (policy/privacy/safety)
- Known failure modes are listed with mitigation/monitoring
- Evals can catch regressions against requirements (not just “nice to have”)

