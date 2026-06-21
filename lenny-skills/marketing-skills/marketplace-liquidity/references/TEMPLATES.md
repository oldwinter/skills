# Templates (copy/paste)

Use these templates to produce concrete artifacts quickly. Adapt wording to your marketplace.

## 1) Marketplace Liquidity Management Pack (skeleton)

### 0) Context snapshot
- Marketplace:
- Buyer / Seller sides:
- Core action (success definition):
- Priority segment(s):
- Timebox:
- Goal (metric + target):
- Constraints:
- Decision this informs:

### 1) Liquidity definition (reliability)
- Working definition:
- Thresholds (“good enough”):
  - Fill/match rate target:
  - Time-to-match target (p50/p90):
  - Cancellation/no-show/dispute guardrails:

### 2) Liquidity metric tree
(See template table below.)

### 3) Local market definition + segmentation
- Local market unit:
- Segment list (top 10 by volume, plus “worst 10” by reliability):
- Fragmentation notes:

### 4) Segment scorecard (baseline)
(See template table below.)

### 5) Bottleneck diagnosis (per priority segment)
- Segment:
- Primary failure mode (supply / demand / mechanics / quality):
- Evidence (metrics):
- Hypothesis (why):
- “Flip-flop” risk (what changes might shift the constraint):
- Graduation problem signals (if any):

### 6) Intervention plan + experiment backlog
(See template table below.)

### 7) Measurement + instrumentation plan
- Dashboards:
- Alerts/thresholds:
- Event definitions / key tables:
- Instrumentation gaps:

### 8) Operating cadence (weekly liquidity review)
- Owner:
- Participants:
- Agenda (see template below):
- Decisions captured in a decision log:

### 9) Risks / Open questions / Next steps
- Risks:
- Open questions:
- Next steps (next 2 weeks):

---

## 2) Liquidity metric tree (table)

| Level | Metric | Definition | Segmentable by | Data source | Notes |
|------:|--------|------------|----------------|------------|-------|
| North star | Liquidity reliability | % of intent events that end in successful core action within SLA | geo, category, cohort | | |
| Driver | Fill/match rate | % intent → match/booking/purchase | geo, category | | |
| Driver | Time-to-match (p50/p90) | Time from intent → match | geo, category | | |
| Driver | Availability at intent | % intents with ≥ N viable options | geo, category, time | | |
| Driver | Acceptance/response | % offers accepted; median response time | geo, seller type | | |
| Guardrail | Cancellation/no-show | % matches that fail post-match | geo, category | | |
| Guardrail | Disputes/fraud | % matches with disputes/fraud flags | geo, category | | |

---

## 3) Segment scorecard (baseline)

| Segment (local market) | Demand volume | Supply available | Fill/match rate | Time-to-match p50/p90 | Cancellation rate | Primary bottleneck | Notes |
|------------------------|---------------|------------------|-----------------|------------------------|------------------|-------------------|-------|
| city A × category X | | | | | | | |
| city B × category X | | | | | | | |

---

## 4) Experiment backlog (prioritized)

| Priority | Segment | Bottleneck | Hypothesis | Intervention | Metric(s) | Expected effect | Effort | Risks/guardrails | Timebox |
|---------:|---------|------------|-----------|--------------|----------|----------------|--------|------------------|--------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |

---

## 5) Weekly liquidity review agenda (30–45 min)

1) **Topline reliability trend** (north-star + key drivers)
2) **Worst segments (bottom 10)** (what changed, why, what we’ll do)
3) **Watchlist segments** (at risk / improving)
4) **Experiment readouts** (what we learned; ship/stop/iterate)
5) **Reallocation decisions** (budget/incentives/ranking boosts/ops outreach)
6) **Risks & quality** (fraud, cancellations, supplier churn)
7) **Next week commitments** (owners + due dates)

