# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with facilitation guidance and decision heuristics.

## Step 1 — Classify + safety + roles

Good retros fail when the **goal is ambiguous**.

Minimum roles:
- **Facilitator:** protects process, timeboxes, psychological safety
- **Scribe:** captures facts, decisions, and actions live
- **Decision owner:** commits to actions and follow-through (may be the same person as facilitator)

Language tip:
- If “postmortem” sounds punitive in your culture, call it a **retrospective** or **learning review**.

Ground rules (copy/paste):
- “We are here to improve systems, not judge individuals.”
- “Assume people acted reasonably given what they knew at the time.”
- “If performance topics exist, we will handle them separately through the right channels.”

## Step 2 — Facts + timeline (no opinions yet)

Two common failure modes:
1) The document becomes **opinionated storytelling** without timestamps/evidence.
2) The timeline is missing key “invisible work” (hand-offs, waiting, approvals).

Heuristics:
- Put **timestamps** everywhere you can.
- Write “**fact**” vs “**hypothesis**” explicitly.
- If you can’t cite evidence, label it as a hypothesis to confirm.

## Step 3 — Contributing factors (systems lens)

Prompting questions:
- What made this outcome **likely**?
- What constraints or incentives shaped behavior?
- Where did we rely on heroics, tribal knowledge, or unowned components?

Use clusters:
- People (skills coverage, oncall load, staffing, handoffs)
- Process (change management, reviews, incident roles, decision latency)
- Product/UX (guardrails, unsafe defaults, user confusion)
- Tech (architecture, dependencies, observability, test gaps)
- Comms (stakeholder awareness, escalation paths, ambiguous ownership)
- Environment (traffic spikes, vendor outages, seasonality)

Avoid:
- “X forgot” / “Y didn’t try hard enough”
Replace with:
- “We lacked a reminder/check” / “The system allowed an unsafe default”

## Step 4 — Learnings + decisions (learning > grading)

If this is an OKR/goal retro, keep the numeric grade secondary to:
- “What was the *system* that produced 0.8?”
- “What would we change to make 1.0 plausible next time?”

Decision types to consider:
- **Fix now** (bug, reliability, UX)
- **Guardrail** (safe defaults, limits, feature flags)
- **Instrumentation** (alerts, dashboards, missing metrics)
- **Runbook/training** (operational readiness)
- **Process change** (reviews, approvals, decision rights)
- **Scope change** (de-scope, postpone, kill/pivot)

## Step 5 — Action tracker (follow-through mechanism)

Rules:
- Every action must have: **owner**, **due date**, **success signal**, **follow-up date**
- Prefer actions that remove entire classes of failure (systemic)
- Limit “Fix now” items to what fits capacity; park the rest explicitly

Anti-patterns:
- “We should communicate better.”
- “Be more careful.”

Replace with:
- “Add an escalation policy and a single owner for X by <date>.”
- “Add an automated check that blocks unsafe deploys by <date>.”

## Step 6 — Kill criteria / triggers (pre-commit to action)

Kill criteria only work if you **pre-commit**.

Template:
- **Signal:** observable threshold (metric drop, incident count, adoption stall)
- **Window:** how long before it counts
- **Action:** pause/pivot/kill/escalate/add investment
- **Owner:** who declares and executes the action

Examples:
- “If activation doesn’t improve by +2pp over 4 weeks after shipping feature X, we pause new scope and run 5 user interviews.”
- “If we have 2+ S0 incidents in a month for subsystem Y, we freeze feature work and fund reliability work for 2 sprints.”

## Step 7 — Dissemination + learning rituals

Retros fail when learnings stay local.

Lightweight options:
- Weekly/biweekly **Impact & Learnings Review** (30 min):
  - Top learnings (not status)
  - “What we changed” (decisions)
  - “What we’ll do next” (actions/experiments)
- A single shared “Learning Log” channel/document with a consistent format

Shareout heuristic:
- A leader should be able to read the TL;DR and answer: “What changed because of this?”

