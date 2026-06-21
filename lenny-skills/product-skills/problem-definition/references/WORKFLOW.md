# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and heuristics.

## Step 1 — Intake + decision framing
Output a **Context snapshot**:
- Product + target user
- Trigger signal (why this matters now)
- Decision to make + deadline + stakeholders/DRI
- Constraints (tech, legal, privacy, capacity)

Heuristic: if the decision isn’t explicit, the “problem” will keep changing mid-stream.

## Step 2 — Target user + situation
Rules of thumb:
- Prefer a *narrow* primary segment over “everyone”.
- Describe the situation that creates the pain (time, place, device, role, permissions, urgency).
- If multiple segments exist, choose the primary and list secondary segments explicitly.

Common failure mode: describing a persona without a situation (“busy professionals”) and ending up with a generic problem statement.

## Step 3 — Problem statement (avoid solution language)
Write two versions:
- **1-liner**: sharp enough to repeat in a meeting.
- **Expanded**: symptoms, impact, and likely causes (as hypotheses).

Anti-patterns to avoid:
- Embedding a solution (“need an AI copilot to…”)
- Defining the problem as a feature request (“need a dashboard”)
- Using non-falsifiable language (“users want an easier experience”)

## Step 4 — Alternatives + “why use this”
Map what users do today:
- Manual/analog workflows (email, phone calls, paper, spreadsheets)
- Existing digital tools and workarounds
- Doing nothing / delaying

Ask: **“Why would a user switch?”**  
If your proposal is just digitizing an analog predecessor, you need a platform-native reason to exist (speed, trust, collaboration, automation, personalization, reach).

## Step 5 — Evidence & assumptions log (don’t over-argue the known)
If the problem is obviously real (support tickets, churn, repeated complaints), avoid “discovery theater”.

Instead:
- Record the evidence and move on to the uncertain parts.
- Focus learning on what’s unclear: segment severity, root cause, willingness to switch/pay, and which solution direction wins.

## Step 6 — Success criteria + guardrails
Make success measurable and decision-useful:
- Outcome metrics (user value delivered)
- Leading indicators (what you can move in weeks)
- Guardrails (what must not get worse)

Heuristic: if the metric can be interpreted two ways, you don’t have a metric yet.

## Step 7 — Visualize end state + prototype a path to clarity
Before committing to build:
- Describe the end state in user terms (what they can do that they can’t today).
- Define “what good looks like” and key failure modes.
- Prototype the fastest thing that produces learning (clickable mock, concierge test, Wizard-of-Oz, scripted demo).

Heuristic: if you can’t “see the end from the beginning”, the scope is too fuzzy to estimate or execute.

## Step 8 — Quality gate + finalize
Before sharing:
- Run [CHECKLISTS.md](CHECKLISTS.md) and score [RUBRIC.md](RUBRIC.md)
- Ensure **Risks / Open questions / Next steps** are present
- Ensure someone can review async without a meeting

