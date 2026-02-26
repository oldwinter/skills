# Workflow (Expanded Guidance)

This file expands the steps from `../SKILL.md` with additional heuristics and common failure modes.

## Step 1 — Frame around decisions
Tech debt work is easiest to fund when it answers a decision like:
- “What do we fix next quarter and why?”
- “Do we migrate/rebuild, or refactor in place?”
- “How much capacity do we reserve for debt without starving feature delivery?”

Avoid outputting a “laundry list” without a ranked plan.

## Step 2 — Look for user-visible debt
Technical debt is often visible externally through:
- Inconsistent UI patterns / fragmented flows
- Poor integration between product areas (silos)
- Slow or unreliable workflows that users notice

If you can tie a debt item to user pain, it becomes easier to prioritize and fund.

## Step 3 — Build a register with a consistent schema
Common debt “types”:
- **Architecture:** tight coupling, monolith boundaries, brittle service interactions
- **Code health:** unreadable/duplicated code, unsafe patterns, missing tests
- **Data:** weak schemas, ambiguous definitions, expensive migrations
- **Infra/ops:** slow deploys, poor observability, manual runbooks
- **Product/UX constraints:** backend limitations forcing awkward UX

Debt register fields should be consistent so scoring is possible.

## Step 4 — Scoring model suggestions
Keep it simple and explainable.

Recommended scoring dimensions (1–5 each):
- **User impact** (does it block workflows or degrade experience?)
- **Reliability risk** (incidents, correctness, on-call pain)
- **Security/compliance risk**
- **Velocity tax** (how much it slows shipping and increases bugs)
- **Effort** (t-shirt size or range) and **sequencing constraints**

Heuristic: prioritize items with **high impact/risk** and **low/medium effort**, plus “enablers” that unblock multiple downstream improvements.

## Step 5 — Rebuild/migration traps to avoid
If you recommend a rebuild/migration, you must explicitly address:
- **Migration duration is usually underestimated** (include ranges and buffers)
- You must often **support the old system while building the new one** (dual-run)
- A rebuild is not “done” until there’s a **decommission plan** and a real cutover

If any of these are unclear, prefer a “thin-slice migration” or “strangler” approach.

## Step 6 — Make the plan incremental
Prefer milestones that ship value and reduce risk:
- Add observability first (to measure before/after)
- Replace one dependency or flow at a time
- Reduce coupling (interfaces/adapters) before large internal rewrites

Define “stop conditions” and rollback for each milestone.

## Step 7 — Funding: quantify the unsexy work
Some of the most impactful debt work is hard to measure. Tactics:
- Create **proxy metrics** (deploy frequency, cycle time, incident rate)
- Run **small experiments** (canary, limited rollout, instrumentation spike)
- Use “before/after” baselines and confidence levels (directional vs high-confidence)

## Step 8 — Operating cadence
Tech debt dies without an operating system:
- Regular register review cadence (monthly/quarterly)
- A clear owner for the register and metrics
- A decision log for strategy calls (rebuild vs refactor)

