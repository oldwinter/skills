# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and decision heuristics.

## Step 1 — Intake + decision framing
Goal: align on what decision is being made and what “good” means.

Output a **Context snapshot**:
- Decision type (ranked backlog vs roadmap themes vs annual planning)
- Horizon + cadence
- Success criteria (North Star + guardrails)
- Constraints (capacity, commitments, deadlines, dependencies)
- Stakeholders (deciders, contributors, approvers)

Common failure mode: jumping to scoring before agreeing on success criteria and constraints.

## Step 2 — Define the “season” + success criteria
Use “season” to ground the roadmap in the current macro context.

Season framing should include:
- Season name (short)
- “What changed / why now” (2–4 bullets)
- 3–5 season bets (what we will prioritize)
- 3–7 explicit non-goals (what we will not do)
- North Star / primary goal + guardrails

Heuristic: if the season can’t be explained in plain language, alignment will be fragile.

## Step 3 — Opportunity inventory (truth vs hypotheses)
Normalize every input into a comparable unit:
- A problem statement + target segment
- Intended outcome metric (or driver)
- Conviction level:
  - **Known:** repeatedly observed + measured
  - **Belief:** directional evidence, but incomplete
  - **Hypothesis:** mostly intuition; needs discovery
- Evidence summary (1–3 bullets)

Split into two tracks:
- **Discovery backlog:** hypotheses that need validation (research, prototypes, small experiments)
- **Delivery backlog:** items you are ready to commit to building

## Step 4 — Common-currency scoring model (ICE + assumptions)
Goal: make tradeoffs comparable across teams and initiative types.

1) Pick a **common currency** (choose one):
- North Star units (preferred if available)
- Revenue/margin impact
- Cost reduction
- Risk reduction (e.g., severity × probability)

2) Define ICE scales:
- **Impact:** expected delta in the common currency (use ranges where needed)
- **Confidence:** based on evidence quality (not optimism)
- **Ease (or Effort):** relative cost/complexity, including dependencies

3) Make assumptions explicit:
- Input metrics → output impact mapping
- Time-to-impact
- Segment size / reach

If you have multiple teams, add a “common currency” conversion line per team so “Team A impact” and “Team B impact” can be compared.

## Step 5 — Stress test ranking (scenarios + constraints)
Apply constraints after scoring:
- Capacity limits (by team/function)
- Dependencies and critical path
- Commitments (security, compliance, platform migrations)
- Risk tolerance (do you need near-term wins, or can you take bigger bets?)

Run 2–3 scenarios:
- **Base:** most likely assumptions
- **Conservative:** lower impact / higher effort
- **Aggressive:** higher impact / faster adoption

Outcome: a shortlist with explicit tradeoffs and “no’s”.

## Step 6 — Draft the roadmap (sequencing + cadence)
Turn the shortlist into a roadmap representation that fits the decision:
- **Now/Next/Later:** best when uncertainty is high and you want flexibility
- **Quarterly themes:** best for cross-functional alignment and OKRs
- **Rolling 12–24 month view:** best for company-wide alignment, refreshed every ~6 months

Sequencing rules of thumb:
- Put high-confidence, high-impact items earlier
- Pull forward items that unlock learning or reduce risk
- Explicitly note dependencies and “gates” (what must be true before starting)

## Step 7 — Decision narrative + alignment plan
The narrative is what “rallies the team around a single goal”.

Include:
- Why now (season framing)
- Why these items (impact + evidence)
- Why not others (explicit non-goals / parking lot)
- How we will revisit decisions (cadence + triggers)

Always add a **Think Bigger** section:
- “With 20% more time, what would we do that isn’t on this list?”
- Capture 3–5 big-bet ideas; decide whether they belong in discovery or future seasons.

## Step 8 — Quality gate + finalize
Run [CHECKLISTS.md](CHECKLISTS.md) and score with [RUBRIC.md](RUBRIC.md), then finalize with:
- Risks (what could go wrong, what might we be wrong about)
- Open questions (what would change the ranking)
- Next steps (owners + dates if possible)

