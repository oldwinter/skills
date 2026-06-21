# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and heuristics.

## Step 1 — Intake + decision framing
Core rule: **No decision, no survey.**

Define:
- The decision to make (by date)
- The primary learning goal (1 goal)
- The audience you can actually reach
- Operational constraints (time, channels, privacy)

Common failure mode: “general feedback” surveys that generate a long list of opinions with no clear next action.

## Step 2 — Audience + sampling plan
Prefer behavior-based and recency-based cohorts:
- If you need recall of the “before” state, target users who adopted **3–6 months ago** (they remember the switch and are stable enough to have real usage).
- If you need friction diagnostics, target **active** users who recently hit the workflow you care about.
- If you need onboarding profiling, target **new signups** in the first session/week.

Sampling guidance (practical, not academic):
- Decide if you want a point-in-time read or to track a trend (repeatable sample definition).
- Use quotas if you must represent sub-segments (buyer vs user, plan tier, region).
- Expect selection bias; write down who is excluded (e.g., churned users you can’t reach).

## Step 3 — Measurement design (metrics, scales, prioritization)
Prefer **CSAT** when you need precision and a clear satisfaction read:
- Example: “Overall, how satisfied are you with <experience>?”
- Use **5–7 point scales** and label endpoints (and ideally each point).

Use **NPS** only if you have an organizational reason (benchmarking, exec expectation):
- Treat it as one input, not the decision itself.
- Always pair it with a diagnostic follow-up (“What is the primary reason?”).

Force prioritization when diagnosing drivers:
- “Pick your top 3 barriers” yields cleaner, more actionable data than “check all that apply”.
- Ask **frequency/impact** to weight issues (e.g., daily vs quarterly; “blocks work” vs “minor annoyance”).

## Step 4 — Questionnaire drafting (question writing rules)
Rules of thumb:
- One concept per question (avoid double-barreled: “fast and easy”).
- Neutral wording (don’t “sell” a hypothesis in the prompt).
- Prefer recent behavior over hypotheticals (“In the last 7 days…”).
- Put sensitive or high-effort questions at the end (or remove them).
- Every segmentation question must be used in analysis, or it doesn’t belong.

Open-ended questions:
- Use 1–2 max, and make them specific (“What is the #1 thing we could change to improve <X>?”).
- Have a coding plan before you launch (see Step 7).

## Step 5 — Instrument table + QA (mobile + bias)
Instrument QA checks:
- Mobile: all scale points visible without scrolling.
- Randomize option order where order bias is likely (except “Other” and intentionally ordered scales).
- Minimize required questions; required fields increase abandonment.
- Provide “Not applicable” when relevant to avoid forced noise.
- Add “Other (free text)” when your option list may be incomplete.

Pilot guidance:
- Run a pilot with 10–20 respondents (or internal dogfooders) to catch ambiguity and logic bugs.
- Measure drop-off per question; remove the question where drop-off spikes unless it’s critical.

## Step 6 — Launch plan + monitoring
Launch plan components:
- Target cohort definition + timing window
- Initial send + 1 reminder (avoid spamming)
- Incentives (if used): define eligibility and fulfillment
- Monitoring: response rate, completion rate, segment mix, drop-off by question
- Close-the-loop plan: what respondents will hear back and when

Message validation “survey alternative”:
- If the goal is “Does this messaging resonate?”, consider a lightweight **ad/landing page test**:
  - Metric: CTR → message comprehension/appeal
  - Metric: conversion → expectation vs reality

## Step 7 — Analysis + reporting plan
Analysis design:
- Predefine the segment cuts you’ll run (don’t fish after the fact).
- Define what “good enough to act” means (thresholds or decision rules).
- For forced-ranking diagnostics, plan how you’ll compute the ranked list:
  - % selected as top-3
  - weighted by frequency/impact

Open-ended coding:
- Create a tag list (start with 10–20 tags, allow new tags).
- Code in batches; quantify themes and segment differences.

Reporting:
- Lead with decisions and implications (not charts).
- Include: what you learned, what you’ll change, what you won’t, and what you still don’t know.

## Common survey types (quick guidance)

### Onboarding profiling (buyer vs user)
Keep to 3–4 screens. Ask only what you will use immediately:
- Role / function
- Company size
- Primary use case / job
- “Are you evaluating for yourself or for a team?”

### CSAT + drivers (friction survey)
Use:
- CSAT (1–7)
- “Pick top 3 barriers”
- frequency/impact weighting
- 1 open-ended “what’s the #1 change?”

### PMF (Sean Ellis)
Best for active users past initial onboarding:
- “How would you feel if you could no longer use <product>?” (Very / Somewhat / Not disappointed)
- Follow-up: “What is the primary benefit you receive?”

### Churn / cancellation
Ask immediately after cancellation and within 7 days:
- primary reason (forced choice)
- what would have prevented it (specific)
- competitor/alternative used

