# Examples (Expanded)

These examples are intentionally compact; use them as patterns, not copy.

## Example 1 — PR/FAQ → PRD (B2B SaaS)
Prompt: “Use `writing-prds`. Product: analytics dashboard. Users: admins. Feature: saved views. Output: PR/FAQ + PRD.”

Expected artifacts:
- PR/FAQ: headline, summary, alternatives, out-of-scope, metrics
- PRD: R1…Rn requirements, metrics + instrumentation plan, rollout tiers

Common pitfalls to avoid:
- “Saved views” without specifying permissions, sharing, or default behavior
- Metrics without a data source or owner

## Example 2 — AI feature (Prompt Set + Eval Spec)
Prompt: “Use `writing-prds`. Feature: AI email reply assistant. Constraints: brand tone, no sensitive data leakage. Output: PRD + Prompt Set + Eval Spec.”

Expected artifacts:
- Requirements include “must-not-do” constraints
- Prompt Set includes examples (2 good + 1 bad) and versioning
- Eval Spec includes judge prompt + thresholds and critical failures

## Boundary example — missing problem and success
Prompt: “Write a PRD for ‘make onboarding better’.”

Response pattern:
- Ask 3–5 minimum intake questions
- If still vague, propose 2–3 scoped options (activation flow vs education vs permissions) with explicit assumptions and recommend discovery

