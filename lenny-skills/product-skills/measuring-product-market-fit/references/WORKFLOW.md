# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with additional guidance, heuristics, and common pitfalls.

## Step 1 — Intake + decision framing
Anchor on a decision, not curiosity.

Output a **Context snapshot**:
- Product + category
- Stage (pre-PMF / early PMF / growth / mature)
- Decision + deadline
- Segments that matter
- Constraints (PII, internal-only, tools)
- Confidence target (directional vs high-confidence)

Pitfall: “Do we have PMF?” without a decision produces a report that doesn’t change anything.

## Step 2 — Define the measurement model (and segments)
PMF is rarely “global.” Treat it as **segment-specific**:
- Segment by persona/use case/tenure/tier
- Look for the “must-have cohort” first, then expand

Define:
- **Core value moment:** the smallest action that reliably predicts sustained value
- **Active user:** a clear inclusion rule for survey and cohorts
- **Signal set:** survey + behavior + customer evidence

Heuristic thresholds (directional, not universal):
- “Very disappointed” (Sean Ellis) at or above **~40%** in the *right segment* often indicates must-have.
- Reference-customer count targets (B2B: **6–8**; B2C: **15–25**) are useful as a reality check.

Pitfall: averaging across all users hides PMF in a niche segment (and leads to wrong strategy).

## Step 3 — Sean Ellis survey (must-have test)
Use the standard questions:
- “How would you feel if you could no longer use <product>?” (Very / Somewhat / Not disappointed)
- “What is the primary benefit you receive?” (text)

Sampling guidance:
- Survey **active users** (not signups who never activated).
- If you have multiple segments, aim for enough responses to compare them (even if directional).

Interpretation guidance:
- Treat “very disappointed” as a leading indicator, not a guarantee.
- The follow-up benefit question is the key: it tells you what value users think they get.
- Always report **n** and call out bias risks (survivorship, channel bias, enterprise procurement bias).

## Step 4 — Behavioral evidence (retention + engagement)
Choose the behavioral lens that matches your model:
- B2C / SaaS: user retention + WAU/MAU; engagement frequency
- B2B: logo retention + expansion; active seats; time-to-value
- Transactional: repeat purchase/usage within an expected cadence window
- Marketplace: repeat behavior by side + liquidity proxies (time-to-match, fill rates)

Retention curve reading (common patterns):
- **Fast drop then flatten:** often indicates a core cohort gets recurring value (potential PMF for a segment).
- **Continuous decay:** usually indicates weak habit/recurrence or value isn’t sustained.
- **Step changes by cohort:** launches/instrumentation changes; avoid false conclusions.

Pitfalls:
- Confusing activation improvements with retention improvements.
- Using “DAU” for a naturally weekly/monthly product and calling it low-PMF.

## Step 5 — Reference-customer / advocacy evidence
References are a “put your reputation on the line” proxy.

Capture:
- Who is willing to vouch (name/org if allowed; otherwise anonymized)
- The segment they represent
- The primary benefit (in their words)
- Whether they’ll do: testimonial, case study, reference call, referral

Pitfall: references from a past market era may not reflect current PMF (PMF drift).

## Step 6 — Scorecard + diagnosis (by segment)
Triangulate to a clear answer:
- **PMF status:** No PMF / Partial PMF (segment) / Strong PMF / At-risk (drifting)
- **Strongest segment:** who is “must-have” and why
- **Biggest gaps:** what breaks in adjacent segments (value, onboarding, pricing, trust, workflow fit)
- **Confidence:** High/Medium/Low based on data quality and coverage

Marketplace reminder:
- Measure PMF **per side**. If pre-PMF, focus on the core value exchange and the hardest side first.

## Step 7 — Action plan + cadence
Translate measurement into action:
- 3–5 highest-leverage actions (product, onboarding, positioning, pricing, distribution)
- For each: expected mechanism, metric to move, leading indicator, and the fastest test

Cadence:
- Re-run the PMF survey quarterly (or after major shifts) for your core segment.
- Define drift triggers (conversion drop, churn increase, engagement down, competitor shifts) that force a re-measurement.

Before finalizing:
- Run [CHECKLISTS.md](CHECKLISTS.md)
- Score with [RUBRIC.md](RUBRIC.md)
- Add **Risks / Open questions / Next steps**

