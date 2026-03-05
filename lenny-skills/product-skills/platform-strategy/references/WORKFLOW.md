# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with heuristics and common failure modes.

## Step 1 — Define the platform as a product
Heuristics:
- Name the users explicitly; “developers” is rarely specific enough.
- Prefer outcome metrics (cycle time, failed deploy rate, time-to-first-integration) over activity metrics.

Failure modes:
- Treating the platform as “infrastructure” with no clear user promise.
- Measuring “output” (migrations, tickets closed) instead of user outcomes.

## Step 2 — Diagnose the lifecycle stage
Heuristics:
- If you can’t name a plausible moat or loop, you’re likely in an internal-productivity stage.
- Write the decision you need to make *this quarter* (open/close/pricing/governance), not an aspirational end-state.

Failure modes:
- “We should be a platform” without evidence of demand or leverage.
- Opening too early and getting buried in support/compatibility debt.

## Step 3 — Map surface area and boundaries
Heuristics:
- Create “paved roads”: default stacks that remove repeated decisions.
- Make boundaries explicit to avoid surprise ownership (who owns auth/logging/guardrails?).

Failure modes:
- Platform owns everything → becomes a bottleneck.
- Platform owns nothing → no consistency; every team reinvents core decisions.

## Step 4 — Identify moat + compounding loops
Heuristics:
- Write the loop as a causal chain (A → B → C → A).
- Define 2–3 leading indicators you can measure quickly (activated devs, integration success, retained builders).

Failure modes:
- “Network effects” claimed without a measurable loop.
- Over-investing before you see signals (“no truffles found, but we bought the farm”).

## Step 5 — Decide what to open and how to govern it
Heuristics:
- Openness requires sustainability: docs, support, versioning, incident response.
- Decide parity rules: when do first-party apps get privileged access vs third parties?

Failure modes:
- Public APIs without deprecation/versioning → partner breakages.
- No abuse/quality plan → ecosystem spam or reliability incidents.

## Step 6 — (If AI) Build defensibility as a system
Heuristics:
- Treat “context” as a first-class asset with permissions, audit, and retrieval quality.
- Integrate multiple AI experiences into one system rather than shipping disconnected features.

Failure modes:
- Feature soup: autocomplete + chat + agent shipped with inconsistent policies and duplicated context.
- Over-trusting guardrails; under-investing in evals, logging, and access controls.

## Step 7 — Metrics + operating model
Heuristics:
- Combine adoption + productivity + reliability: all three are needed for healthy platforms.
- Treat documentation and migration tooling as “product surface”, not chores.

Failure modes:
- Success defined as “everyone migrated” without proof of outcome improvement.
- No intake/prioritization → platform roadmap captured by the loudest team.

## Step 8 — Roadmap + quality gate
Heuristics:
- Use 3 horizons (Now/Next/Later) to avoid false precision.
- Include reversibility: pilots, staged rollouts, and exit paths.

Failure modes:
- Roadmap is a wishlist; no sequencing or resourcing reality.
- No explicit risks/open questions → decision gets re-litigated repeatedly.

