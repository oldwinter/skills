# EXAMPLES (Retention & Engagement)

Use these to sanity-check that outputs are artifact-driven and executable (not generic advice).

## Positive example 1 — B2C subscription churn

**Prompt**
“Use `retention-engagement`. Product: meditation app. Segment: paid subscribers. Baseline: D30 paid retention 22%, churn spikes after week 2. Constraint: 4-week sprint, no major redesign. Channels: push + in-app, no email. Output: a Retention & Engagement Improvement Pack.”

**What a good output includes**
- A clear diagnosis naming the primary failure mode (e.g., engagement decay after week 2) and the biggest leak.
- An activation/aha definition (v1) tied to behaviors (e.g., “3 sessions + saved 1 program within 7 days”).
- 5–8 experiments with cards (push cadence, streak UX, “resume your plan” entry point, content freshness).
- A measurement plan (events + dashboards) and a 30/60/90 execution plan.
- Risks/open questions/next steps (e.g., avoid notification fatigue; confirm content supply).

## Positive example 2 — B2B SaaS activation + habit

**Prompt**
“Use `retention-engagement`. Product: team task management tool. Segment: teams with 3–10 seats. Baseline: activation 30% (team creates project + assigns 1 task), D7 retention 12%. Constraint: engineering capacity 1 squad for 6 weeks. Output a Retention & Engagement Improvement Pack.”

**What a good output includes**
- A data-backed activation/aha proposal with thresholds (e.g., “invites 2 teammates + completes 5 tasks across 2 users within 14 days”).
- Onboarding/time-to-value experiments (defaults, templates, guided setup).
- Accruing value experiments (progress history, weekly summary, “what changed since last time”).
- Re-engagement experiments (in-app prompts, email if allowed) tied to next-best action.

## Negative / boundary example — wrong problem

**Prompt**
“We’re not sure what we’re building yet. Pick an ICP and write our positioning.”

**Correct response behavior**
- Decline to produce a retention optimization pack.
- Route to `problem-definition` first (then revisit retention once value/ICP is clearer).

