# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and heuristics for leaders.

## Step 1 — Intake + focal decision/problem
Aim: make the problem *decision-ready*.

Heuristics:
- Rewrite “We need to build X” into “We need to achieve Y under constraints Z.”
- If the “problem” is mostly a list of symptoms, choose a focal symptom and treat it as an entry point, not the root cause.

## Step 2 — System boundary (useful, not complete)
Pick a boundary that is actionable:
- **Too narrow:** ignores externalities (partners, incentives, culture).
- **Too wide:** becomes “everything,” which prevents decisions.

Boundary outputs should include:
- Goal + time horizon
- In-scope actors and interfaces
- Explicit non-scope
- 1–3 outcome metrics + 3–7 leading indicators

## Step 3 — Actors + incentives map
For each actor/player, capture:
- Incentives (what they optimize for)
- Constraints (what they can’t do)
- Power/agency (what they can influence)
- Likely behavior if nothing changes

Don’t forget “invisible actors,” when relevant:
- Policies and compliance requirements
- Cultural norms (“this is how we do things”)
- Legacy platform constraints
- Funding/allocations and performance reviews

## Step 4 — System map (variables + causal links)
Keep the map simple and testable:
- Prefer concrete variables (“time-to-resolution”, “feature adoption”, “incident rate”) over abstract ones (“quality”, “alignment”).
- Express links as: **A increases/decreases B**, optionally with a note on time delay.

If you can’t define a variable or how you’d observe it, it doesn’t belong in the map yet.

## Step 5 — Feedback loops + time delays
Classify loops:
- **Reinforcing (R):** amplifies change (growth loops, death spirals).
- **Balancing (B):** stabilizes (capacity limits, budget caps, policy enforcement).

For each loop, add a short “so what”:
- What behavior/pattern does it create over time?
- What does the loop “optimize” for?

Common leadership traps caused by delays:
- Over-correcting (oscillation)
- Fixing the metric, breaking the system (Goodhart)
- Firefighting loops that starve prevention

## Step 6 — Second-/third-order effects ledger
For each candidate move:
- 1st order: immediate, local effect
- 2nd order: effects created by responses/adaptations of other actors
- 3rd order: longer-term constraints, norm changes, path dependence

Include:
- Who wins/loses (and how they might respond)
- Which constraints tighten/loosen over time
- What new loop you might create (intentional or accidental)

## Step 7 — Leverage points + intervention plan
Leverage point categories that often matter in leadership contexts:
- **Incentives:** what gets rewarded/punished
- **Information flows:** who sees what, when (dashboards, transparency)
- **Rules/policies:** definitions, SLAs, decision rights
- **Buffers/capacity:** staffing, WIP limits, throttles
- **Tools/automation:** eliminate recurring manual work
- **Interfaces:** contracts between teams, APIs, handoffs

Design interventions with:
- Owner + sequencing
- Leading indicator(s)
- Guardrail metric(s) to prevent harm
- Rollback or stop condition if risks materialize

## Step 8 — Quality gate + finalize
Before finalizing:
- Run [CHECKLISTS.md](CHECKLISTS.md)
- Score with [RUBRIC.md](RUBRIC.md)
- Add **Risks / Open questions / Next steps**

If the score is low, fix these first:
1) Boundary and success measures
2) Actor/incentive realism
3) Testable causal links (no abstractions)

