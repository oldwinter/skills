# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and heuristics.

## Step 1 — Decide the artifact set
Goal: create the smallest set of artifacts that still makes the decision executable.

Rules of thumb:
- If stakeholders disagree on “why this matters”, start with **PR/FAQ**.
- If engineering is blocked on ambiguity, prioritize **PRD requirements + acceptance criteria**.
- If it’s an AI feature, treat **Prompt Set + Eval Spec** as first-class requirements.

Common failure mode: writing a long PRD when the real need is a crisp narrative + decision.

## Step 2 — Intake + decision framing
Output a **Context snapshot**:
- Product, user, problem, why now
- Decision to be made + DRI/approver
- Timeline and constraints
- Success metrics + guardrails
- Stakeholders and reviewers

Heuristic: if you cannot explain the problem in one sentence, requirements will be unstable.

## Step 3 — Customer narrative first (PR/FAQ or PRD narrative)
The narrative should be readable by non-builders.

Include:
- Who the user is
- What they struggle with today
- What changes with the solution
- Why now (trigger/event)

If doing PR/FAQ, include a **hypothetical launch date** to force a realism check.

## Step 4 — Lock scope boundaries
Make tradeoffs explicit:
- Goals (what success means)
- Non-goals (important, but not for this effort)
- Out of scope (explicit exclusions)
- Assumptions + dependencies

Common failure mode: “scope creep by omission” — leaving exclusions implicit.

## Step 5 — Testable requirements (R1…Rn)
Write requirements so they can be tested and estimated:
- Use **R1…Rn** labels
- Add acceptance criteria and edge cases
- Add non-functional requirements (privacy, latency, reliability)
- Separate “must” vs “should” vs “could”

Heuristic: if a requirement can’t be falsified, it’s not a requirement yet.

## Step 6 — UX flows + instrumentation
Describe key flows and states:
- Entry points
- Happy path
- Error states
- Permissions/roles

Instrumentation:
- For each goal/guardrail, define metric → data source → owner → cadence.

Common failure mode: metrics defined without a path to measurement.

## Step 7 — AI add-ons (Prompt Set + Eval Spec)
For AI features, requirements are incomplete without tests.

Minimum viable AI pack:
- Prompt Set: versioned prompts + examples + guardrails + tool usage notes
- Eval Spec: test set + judge prompt + scoring + pass thresholds
- Failure modes: hallucination, refusal, policy violations, tone drift, sensitive data leakage

Heuristic: if the eval can’t catch regressions, it’s not the “source of truth”.

## Step 8 — Quality gate + finalize
Before circulation:
- Run [CHECKLISTS.md](CHECKLISTS.md) and score [RUBRIC.md](RUBRIC.md)
- Ensure Risks/Open questions/Next steps exist
- Ensure the artifact can be understood without a meeting

