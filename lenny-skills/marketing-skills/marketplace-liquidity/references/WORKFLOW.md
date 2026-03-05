# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with additional guidance, heuristics, and common pitfalls.

## Step 1 — Intake + define local markets

Heuristic: liquidity is **local**, not global. Pick a unit where a match actually happens:
- Geo marketplaces: `city × category × week` (or `neighborhood × daypart`)
- Category marketplaces: `category × price band × week`
- Time-sensitive marketplaces: `geo × category × hour`

Pitfall: a single global “fill rate” hides that 20% of segments drive 80% of failures.

## Step 2 — Define liquidity as reliability

Define liquidity from the **buyer perspective** unless there’s a strong reason not to:
> “If a buyer has intent, how reliably can they complete the core action within acceptable time/quality?”

Common reliability components:
- **Match/fill rate:** % of demand attempts that result in a match/booking/purchase
- **Time-to-match:** p50/p90 time from intent → match (or intent → first acceptable option)
- **Availability:** supply coverage at the moment of intent (e.g., “% searches with at least N options”)
- **Quality:** cancellations/no-shows/disputes that undo the match

Pitfall: optimizing supply acquisition volume without improving reliability at the moment of intent.

## Step 3 — Segment scorecards + fragmentation

Fragmentation signals:
- Thin markets (low supply or demand volume) → high variance outcomes
- Long-tail categories or geo pockets with poor coverage
- Heterogeneous needs (too many “micro niches”) that reduce match probability

Uniform needs heuristic: the more uniform the buyer needs, the easier liquidity is to achieve.

Pitfall: mixing segments with different “jobs” (e.g., emergency vs planned) which require different SLAs.

## Step 4 — Bottleneck diagnosis (flip-flop + mechanics + quality)

Classify each priority segment:
- **Supply-limited:** not enough availability, low coverage at intent, high time-to-match, high price due to scarcity
- **Demand-limited:** low intent volume, low utilization of supply, high idle time
- **Mechanics-limited:** supply exists but not discoverable; response/acceptance is slow; ranking/pricing friction
- **Quality/trust-limited:** matches happen but fail (cancels, no-shows, disputes, fraud)

Flip-flop note: many marketplaces alternate between supply- and demand-limited states as you intervene.

Graduation problem checklist:
- Do top suppliers churn after success?
- Do you lose “anchor supply” that made the segment reliable?
- Is there a clear path for suppliers to scale without leaving the platform?

Pitfall: addressing the wrong side (buy more demand when the segment is supply-constrained).

## Step 5 — Interventions + “whac-a-mole” rebalancing

Intervention menu (choose by bottleneck):
- **Supply:** targeted supply acquisition, improved onboarding, availability nudges, minimum standards, reactivation
- **Demand:** targeted acquisition, pricing promos, demand shaping (time/geo flexibility), education
- **Mechanics:** ranking/discovery improvements, better filters, faster response flows, pricing transparency
- **Quality/trust:** verification, dispute tooling, cancellation penalties, quality tiers, fraud prevention

“Whac-a-mole” plan:
- Decide your weekly reallocation levers (budget, incentives, ranking boosts, ops outreach)
- Define triggers (e.g., “if fill rate < X for 2 weeks, allocate Y”)
- Track second-order effects (e.g., incentives improve fills but increase cancellations)

Pitfall: launching incentives without guardrails (quality drop, fraud).

## Step 6 — Measurement + operating cadence

Cadence guidelines:
- Weekly review with a stable agenda and a single owner
- Use a “top segments” list (worst 10) + “watchlist” (improving/at risk)
- Produce decisions: reallocate, ship, stop, investigate

Pitfall: dashboards without decisions; decisions without follow-through.

## Step 7 — Quality gate

Minimum bar:
- Clear reliability definition + thresholds
- Segment scorecard (local markets) + ranked worst segments
- Diagnoses tied to evidence
- 5–10 experiments with owners/timebox (if known)
- Risks / Open questions / Next steps

