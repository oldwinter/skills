# Examples (2 good + 1 boundary)

Use these as “smoke tests” to ensure the skill produces concrete artifacts.

## Example 1 — On-demand services marketplace (geo × daypart)

**Prompt:**  
“Use `marketplace-liquidity`. We run an on-demand dog walking marketplace in NYC, SF, and LA. Core action: request → booked within 10 minutes. Goal: improve booking fill rate from 55% to 75% in SF evenings within 6 weeks. Baseline: p50 time-to-book is 18 minutes, cancellation rate is 9%. Constraints: $25k/month in incentives, limited eng capacity. Output a Marketplace Liquidity Management Pack.”

**What good output includes (high-level):**
- Local market definition (`city × daypart × week`) and a segment scorecard
- Reliability thresholds (fill + time-to-book + cancel guardrails)
- Bottleneck diagnosis (e.g., supply availability in SF evenings + slow responses)
- Experiments (targeted reactivation, response-time nudges, ranked boosts) with metrics/timeboxes
- Weekly liquidity review cadence with reallocation triggers

## Example 2 — Productized B2B services marketplace (category fragmentation)

**Prompt:**  
“Use `marketplace-liquidity`. Marketplace: matching fintech startups with compliance consultants. Core action: request → first qualified match within 48 hours. We’re strong in ‘SOC2’ but weak in ‘GDPR.’ Goal: cut p90 time-to-first-match from 10 days to 4 days for GDPR in 90 days. Output a pack with a metric tree, fragmentation analysis, and top 7 experiments.”

**What good output includes (high-level):**
- Category-level fragmentation map (GDPR has thin supply + mismatched expectations)
- Experiments across supply acquisition, matching mechanics, and demand shaping
- Operating cadence and instrumentation gaps

## Boundary example — Not a marketplace reliability problem

**Prompt:**  
“We have low conversion on our landing page. Write better copy.”

**Correct response:**  
This request is primarily messaging/copy. Use a copywriting/messaging skill. Only use `marketplace-liquidity` if the core issue is matching reliability (availability, fill, time-to-match, cancellations).

