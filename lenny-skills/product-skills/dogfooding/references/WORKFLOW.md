# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and decision heuristics.

## Step 1 — Frame the goal (experience + value)
Dogfooding fails when it becomes “find bugs” without a target workflow outcome.

Define 1–3 success criteria:
- Time-to-complete for a scenario (e.g., “< 10 minutes”)
- Workarounds allowed (ideally none; if any, list them explicitly)
- Output quality (e.g., “shareable without manual cleanup”)

Heuristic: if success is not measurable, you’ll argue about feelings instead of fixing flows.

## Step 2 — Scenarios + creator commitments
Dogfood **jobs**, not features.

Scenario design tips:
- Include at least one “day-0” scenario (new user, empty workspace).
- Include at least one “creator” scenario when your customer is a creator:
  - Publish an episode, ship a newsletter, create a dashboard, produce a report, etc.
- Include at least one “stress” scenario: longer content, messy inputs, edge-case formatting, failed integrations.

Creator commitments should be real:
- A cadence (weekly publish)
- A definition of “done” (artifact actually shipped/shared)
- A place where the artifact lives (internal channel, public link, shared folder)

## Step 3 — Capture system (log + triage)
Dogfooding output must be **reproducible**.

Minimum fields to capture:
- Scenario + step (where in the flow)
- Severity (see below)
- Steps to reproduce + expected vs actual
- Evidence (screenshots, timestamps, logs)
- Workaround used (if any)
- Impact on completing the scenario

Suggested severity scale:
- **S0 Blocker:** Can’t complete scenario / data loss / privacy/security risk
- **S1 Major:** Can complete with major workaround / takes too long / output unusable
- **S2 Minor:** Irritating but scenario completes; paper cuts
- **S3 Nit:** Cosmetic; low impact

Triage rule: if it blocks completing a core scenario, it’s automatically S0/S1 until proven otherwise.

## Step 4 — Daily sessions (time-boxed)
Make it routine:
- Each person runs 1 scenario/day (or 2 shorter ones)
- Log issues immediately
- End with a 2-minute “top pain” note: what would stop a real user from returning?

Heuristic: without time-boxing, dogfooding expands to fill the week and never converges.

## Step 5 — Weekly triage (decide, assign, protect focus)
Triage is where dogfooding becomes product development.

During triage:
- Cluster duplicates and link them
- Decide disposition: **Fix now / Schedule / Won’t fix** (with reason)
- Assign owners and define the smallest next step (PR, design tweak, copy change)
- Adjust scenarios if they were unrealistic or missing key steps

Protect focus:
- Limit “fix now” to what fits the next release window
- Keep a visible “won’t fix (why)” list to avoid re-arguing

## Step 6 — Ship loop + verification gate
Close the loop:
- Re-run the scenario after the fix (ideally by someone who didn’t implement it)
- Record “verified in dogfooding” evidence (link/screenshot)

Simple gate options:
- “Core scenario completes end-to-end with no workaround.”
- “Core scenario completes in <X minutes and output is shareable.”

## Step 7 — Report + next cycle plan
A good report is decision-oriented:
- What changed?
- What did we learn?
- What do we do next?

Include:
- Top 3–5 pains (with evidence)
- Decisions made (fix now/schedule/won’t fix)
- Shipped + verified fixes
- Next cycle focus (scenarios or customer segment)
- Risks / Open questions / Next steps

