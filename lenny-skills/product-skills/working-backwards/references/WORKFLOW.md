# Working Backwards — Expanded Workflow Notes

Use this file when you need more detail than the 8-step workflow in `../SKILL.md`.

## Principles (convert “insights” into rules)

### 1) Start with the customer problem, not a solution
- **Rule:** The PR must contain a “Problem today” paragraph before describing the solution.
- **Anti-pattern:** “We want to build X” → reverse it into “Customers struggle with Y, causing Z.”
- **Check:** If you removed the solution section, the problem paragraph still stands as coherent and compelling.

### 2) Use options to prevent solution lock-in
- **Rule:** Draft 2–3 divergent PR options before committing to one.
- **Check:** Options differ on the core mechanism or value delivery (not just wording).
- **Artifact:** Use the Option A/B/C table in [TEMPLATES.md](TEMPLATES.md).

### 3) Backcasting is about the whole system (“machinery”), not just a doc
- **Rule:** The output must include a backcasting plan with owners, milestones, and dependencies.
- **Check:** Legal/compliance, analytics, docs/support, and rollout are addressed (when relevant).

### 4) Make assumptions explicit and testable
- **Rule:** If key facts are missing, write assumptions as a numbered list and propose 1–3 validation tests.
- **Check:** At least one test can be run before full build (prototype, concierge/WoZ, research, data pull).

## How to draft strong press releases

### Make it customer-readable
- Avoid internal acronyms and org names.
- Lead with the customer outcome, not the feature.
- Keep “How it works” to 3–6 concrete bullets.

### Include boundaries to keep scope honest
- Always include “Who it’s for / not for”.
- Call out “Out of scope for v1” in the FAQ (and optionally the PR).

### Write credible quotes
- Customer quote should reflect a real pain and a measurable/observable improvement.
- Company quote should emphasize customer obsession and why now.

## How to write an FAQ that de-risks execution

Aim for four sections:
1) **Customer FAQs** (use cases, permissions, UX, limitations)
2) **Business FAQs** (pricing/packaging, positioning, sales/support impact)
3) **Technical/ops FAQs** (dependencies, reliability, rollout, rollback, instrumentation)
4) **Legal/compliance FAQs** (privacy, data retention, regulatory constraints, security review)

Prefer concrete answers and explicit unknowns:
- If unknown: “Open question: … Options: A/B/C. Proposed decision owner + date.”

## Backcasting: turning narrative into a plan

### Start from a launch tier and date
Pick a tier (internal, beta, GA) and a date or timebox. If unknown, propose a realistic sequence:
- Internal dogfood → limited beta → GA

### Milestones to include (as relevant)
- Prototype / validation checkpoint
- Engineering milestones (MVP, hardening, scalability)
- Data/instrumentation readiness (events, dashboards, monitoring)
- Legal/privacy/security reviews and sign-offs
- Docs/support readiness + escalation paths
- Comms: release notes, customer emails, sales enablement
- Rollout + rollback plan

## Stress-testing (pre-mortem)

Write: “It’s 6 weeks after launch and this failed. Why?”
Cover at least:
- Adoption failure (wrong segment, weak value)
- Trust/safety/privacy failure (abuse, leakage, bad outcomes)
- Operational failure (support load, edge cases, reliability)
- Business failure (pricing mismatch, cannibalization, margin/cost blow-up)

Then add mitigations + monitoring signals for each.

