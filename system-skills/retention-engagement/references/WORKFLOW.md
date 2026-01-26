# WORKFLOW (Retention & Engagement)

Use this file when you need deeper guidance than the 7-step workflow in `../SKILL.md`.

## A) Pick the right retention metric

Choose the metric that matches the product’s natural cadence.

Common options:
- **Cohort retention (D1/D7/D30):** best for new-user retention and onboarding issues.
- **Weekly retention:** best when usage is naturally weekly (B2B tools, planning, collaboration).
- **Rolling retention:** “has the user been active on or after day N?” Useful for long-tail products.
- **Churn rate:** best for subscriptions, but interpret alongside engagement + value delivery.

Always define:
- Segment(s)
- Time window (e.g., “D30 = active at least once on day 30 ± 3 days”)
- What counts as “active” (a meaningful action, not just an app open)

## B) Diagnose the failure mode

Use the “three failure modes” framing:

1) **Activation failure**
- Symptoms: very low D1/D2; users don’t complete onboarding; low first-value rate.
- Typical causes: unclear value prop in-product, too much setup, empty state friction, wrong default.
- Primary levers: onboarding, time-to-value, guided setup, better defaults.

2) **Engagement decay**
- Symptoms: D1 is okay, but D7/D14 drops; users get value once but don’t form a habit.
- Typical causes: low frequency use case, no re-engagement hooks, value doesn’t accrue, novelty wears off.
- Primary levers: habit loops, reminders, content freshness, collaboration/reasons to return, progress tracking.

3) **Monetization churn**
- Symptoms: engagement looks healthy but churn is high around renewal, trial end, or paywall moments.
- Typical causes: misaligned pricing, surprise billing, friction in renewal, low perceived ROI at renewal.
- Primary levers: improve value communication, reduce billing friction, fix packaging, improve “value moments” before renewal.

Output a diagnosis that names:
- Which failure mode is primary (and why)
- The biggest leak (segment × step × timeframe)
- The leading indicator to move first (time-to-value, key action frequency, etc.)

## C) Define the activation / “aha moment”

The goal: a behavioral definition of “a user experienced value” that correlates with future retention.

### How to generate candidates
- Identify 3–5 actions that represent real value (not vanity actions).
- Include multi-entity thresholds if the product is collaborative:
  - “invited 2 teammates”
  - “connected 2 integrations”
  - “used 2 key features”

### How to validate (fast options)
- Compare retention for users who did vs didn’t do each candidate behavior.
- Try simple thresholds: 1×, 2×, 3× within 7/14 days.
- Prefer the simplest definition that strongly separates retained vs churned cohorts.

### Caution
Correlation isn’t causation. Treat the activation definition as a working hypothesis to validate with experiments/holdouts when feasible.

## D) Retention levers (a practical library)

Use these as starting points; only keep what ties to the diagnosis.

### 1) Onboarding → time-to-value (high leverage)
- Reduce steps to first value; remove optional setup.
- Use progressive disclosure: do the minimum now, the rest later.
- Pre-fill defaults; use templates; import from existing tools.
- Instrument every onboarding step to find drop-offs.

### 2) Habit formation → “come back tomorrow”
- Identify a natural trigger (time-based, event-based, social).
- Reduce friction to restart (one-tap resume, saved state).
- Add a clear next action (“what should I do now?”).
- Reward progress (streaks, milestones) without coercive/dark patterns.

### 3) Accruing value + ethical “mounting loss”
- Make the product improve with use: personalization, learned preferences, history.
- Turn activity into an asset: saved work, progress, reputation, collections.
- Surface what the user has built (“your progress”, “your library”, “your team workspace”).
- Avoid hostage tactics: provide export, transparency, and user control.

### 4) Re-engagement + winback
- Segment by reason for inactivity (never activated, activated-then-decayed, churned).
- Tailor messaging to the next-best action and the value they’re missing.
- Prefer fewer, higher-signal messages; cap frequency; allow opt-out.

### 5) Retention before aggressive monetization (subscriptions)
- If retention is weak, heavy day-one upsells often backfire.
- Focus first on getting users to repeated value, then optimize paywall/timing.

## E) Experiment design and measurement

For each experiment card:
- Hypothesis (what changes and why)
- Target segment
- Success metric (primary) + leading indicator(s)
- Guardrails (unsubscribe rate, complaint rate, refunds, revenue, latency)
- Instrumentation needed (events/properties)
- Rollout + rollback plan

## F) Assemble the final pack

Use [TEMPLATES.md](TEMPLATES.md) to produce a single “Retention & Engagement Improvement Pack” that includes:
- Diagnosis + activation spec + experiment backlog + measurement plan + 30/60/90 plan
- Risks / Open questions / Next steps (required)

