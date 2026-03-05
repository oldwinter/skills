# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance, heuristics, and common failure modes.

## Step 1 — Frame the decision and boundaries
Output: a crisp “decision statement” and explicit non-goals.

Heuristics:
- If stakeholders disagree on “why this matters,” spend extra time on **why now** and **non-goals**.
- If the request is “add AI,” force a use-case portfolio instead of starting from a solution.

Failure modes:
- Strategy that is actually a PRD (too detailed) or a vision (too lofty).
- No explicit non-goals → scope creep by omission.

## Step 2 — Map the workflow and role shift
AI changes what users do, not just what the product can do.

Heuristics:
- Identify the “human control points”: review/approve moments where trust must be earned.
- Write 3–5 failure modes that would destroy trust and treat them as guardrails.

Failure modes:
- “AI will do X” without specifying where it fits in the user’s day.
- Underestimating that users will adapt their behavior (and find unexpected use cases).

## Step 3 — Use-case portfolio and prioritization
Create a portfolio table and choose 1–3 bets.

Heuristics:
- Prefer use cases with clear feedback signals and fast iteration loops.
- Separate “value” from “cool demo.” Demand a measurable outcome.

Failure modes:
- Picking use cases that require perfect model behavior in v1.
- Ignoring operational load (support burden, escalation, policy review).

## Step 4 — Differentiation + why us/why now
“We use AI” is not a differentiator. Differentiation is usually:
- Proprietary/unique data (or privileged access to workflow context)
- Distribution (embedded surface area, default workflows, partnerships)
- UX integration (where the AI lives and how it reduces work)
- Trust (safety, privacy, predictable behavior, auditability)

Failure modes:
- Confusing model selection with strategy.
- No compounding loop (data flywheel, workflow lock-in, network effect, cost advantage).

## Step 5 — Form factor + autonomy policy
Assistant → Copilot → Agent is a spectrum of autonomy and risk.

Heuristics:
- Start with the minimum autonomy that still delivers value.
- For any action-taking capability, define: permissioning, confirmations, audit logs, and undo/rollback.

Failure modes:
- “Agent” without a permission model.
- No plan for prompt injection and tool misuse.

## Step 6 — System plan (build/buy, data, evals, budgets)
Keep this strategy-level: enough specificity to be executable, not an architecture doc.

Include:
- Build/buy stance (vendor/LLM choice as an assumption; validate later)
- Data sources + governance constraints
- Eval approach: offline tests + online monitoring
- Budgets: cost/user/day and latency targets

Failure modes:
- No evals → non-determinism becomes unmanageable.
- No cost/latency budget → “success” becomes financially unsustainable.

## Step 7 — Empirical learning plan (experiments + instrumentation)
AI products are empirical: utility and risks emerge in real usage.

Heuristics:
- For each assumption: hypothesis → experiment → metric → timebox → owner.
- Instrument both utility and risk (e.g., escalation rate, policy violations, user overrides).

Failure modes:
- “We’ll iterate” without an experiment design or instrumentation.
- Only optimizing for engagement; ignoring trust/safety regressions.

## Step 8 — Roadmap + quality gate
Roadmap should be phased and reversible.

Heuristics:
- Use rollout tiers (internal → beta → GA) with exit criteria.
- Convert risks into mitigation work items (security review, red teaming, eval coverage).

Failure modes:
- A roadmap that is only feature bullets (no owners, no exit criteria, no risk work).

