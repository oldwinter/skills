# Checklists

Use these checklists as the **quality gate** before finalizing the AI Product Strategy Pack.

## 1) Strategy thesis checklist
- The decision statement is explicit (what, by when, for whom).
- The problem is user-centered and has at least 1–2 evidence points.
- “Why now” is concrete (capability shift, market shift, distribution shift, regulation, or cost curve).
- Differentiation is defensible (not “we use AI”); includes at least 2 compounding levers.
- Non-goals are explicit (3+), preventing scope creep.
- Assumptions are listed with tests, metrics, owners, and timeboxes.

## 2) Use-case portfolio checklist
- Portfolio lists 6–12 candidates (not just the chosen idea).
- Top 1–3 bets have clear target user + workflow anchor + measurable outcome.
- Each selected bet includes at least one “must-not-do” constraint.
- Feasibility and risk are assessed (even if rough) and tied to constraints (data, privacy, latency, cost).

## 3) Autonomy policy checklist (assistant/copilot/agent)
- The chosen form factor is the minimum autonomy needed for value.
- Any action-taking capability has: approval model, permission scope, audit logs, and rollback/undo.
- The “must never do” list is explicit and enforced via product + policy + evals.
- There is a plan for prompt injection/tool misuse and unsafe instructions.

## 4) System plan checklist (data, evals, budgets)
- Data sources are explicit; prohibited data and governance constraints are clear.
- Eval plan includes:
  - Offline tests with critical failure cases
  - Online monitoring signals + cadence + owner
- Budgets are explicit: cost target, latency target, and reliability target.
- The plan acknowledges non-determinism (behavior variance) and includes mitigation (fallbacks, guardrails, routing).

## 5) Empirical learning plan checklist
- Every key assumption has an experiment and a decision rule.
- Instrumentation is concrete (events/logs) with owners.
- The plan monitors both utility and risk (trust/safety, overrides, escalations).
- Rollout is staged and reversible (internal → beta → GA).

## 6) Roadmap checklist
- Phases have entry/exit criteria (not just feature bullets).
- Owners/DRIs are named (or role placeholders).
- Risk retirement work is included as first-class roadmap items (security review, red team, eval coverage).

## 7) Final packaging checklist
- Pack includes **Risks**, **Open questions**, **Next steps**.
- All major trade-offs are stated (quality vs cost vs latency vs autonomy).
- Assumptions are clearly labeled vs facts.
- Output is shareable as-is without needing a meeting to interpret.

