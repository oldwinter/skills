# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra heuristics, patterns, and decision shortcuts for PM-led usability testing.

## Step 1 — Anchor on the decision (avoid “testing for testing”)
Before writing tasks, name:
- The **decision** (what will change)
- The **unknowns** (what you genuinely don’t know)
- The **success bar** (what “good enough to ship” looks like)

Heuristic: If you can’t name the decision, you’ll end up with a nice report and no follow-through.

## Step 2 — Choose the cheapest valid stimulus
Pick the lowest-cost setup that still tests the behavior you care about:
- **Clickable prototype** to test navigation, comprehension, and flow
- **Wizard of Oz** to test “value perception + interaction” when the backend isn’t ready
- **Fake door** to test intent/interest (pair with follow-up interviews or sessions to avoid misreading clicks)
- **Concierge** to test an end-to-end experience with manual fulfillment
- **Live product** when you need real data/constraints (permissions, latency, integrations)

Rule of thumb: early = validate *value + comprehension*; later = validate *efficiency + edge cases*.

## Step 3 — Write tasks that reveal friction (not opinions)
Task-writing patterns:
- Use real intent: “You’re trying to <goal>… what would you do?”
- Include starting state: account type, plan tier, sample dataset, logged-in/out
- Avoid UI labels: don’t say “Click ‘Generate report’”
- Include one “expectation check”: “What do you think will happen if you do that?”

Keep the set small: 5–8 tasks max (or split into multiple sessions).

## Step 4 — Recruit the right participants (and overbook)
Prefer participants who match the situation:
- Similar job-to-be-done, constraints, and familiarity level
- Recency matters if the flow depends on memory (“first-time user” means *tried in last 1–14 days*)

Operationally:
- Expect no-shows. Build backups and slack.
- If stakeholders are hard to schedule (e.g., editors during breaking news), treat scheduling as a first-class risk.

## Step 5 — Script for neutrality and evidence
Moderator guide basics:
- Explicitly say: “We’re testing the product, not you.”
- Ask for think-aloud, but don’t force constant narration.
- Probe with: “What were you expecting?” “What made you choose that?” “What would you do next?”
- Capture micro-friction: confusing CTAs, wording, labels, and uncertainty moments.

## Step 6 — Run sessions + capture clean notes
Evidence capture rules:
- Separate **verbatim** from interpretation
- Capture the “moment”: trigger → action → confusion/error → workaround → outcome
- Note time/effort directionally (fast/slow; stuck for 60s)
- Save artifacts: screenshots, timestamps, short quotes

Optional “reality check” (build intuition):
- Observe a comparable real-world flow (competitor, adjacent product, physical world analog) and record what people actually do.

## Step 7 — Synthesize into actions (including micro wins)
Turn findings into decisions:
- Convert each finding into an **issue** with evidence + severity + frequency
- Propose a fix and expected impact (directional), especially for high-leverage microcopy/CTA changes
- Separate **quick wins** (hours/days) from **structural fixes** (weeks)

## Step 8 — Close the loop
Before you finalize:
- Run [CHECKLISTS.md](CHECKLISTS.md) + score [RUBRIC.md](RUBRIC.md)
- Call out **Risks**, **Open questions**, **Next steps**
- Propose the smallest follow-up (iterate prototype, retest 3 users, ship behind flag, run experiment)

