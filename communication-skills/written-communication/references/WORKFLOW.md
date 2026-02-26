# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and heuristics.

## Step 1 — Choose the lightest artifact
Default rule: pick the smallest artifact that still achieves the outcome.

Common picks:
- **Email/Slack message:** fast update + clear ask.
- **Memo (1–2 pages):** recommendation + tradeoffs + decision.
- **Doc (longer):** shared context that will be referenced repeatedly.
- **Canonical doc:** ongoing project hub (links + decisions + current state).

Failure mode: writing a long doc when the reader only needed a crisp ask + next steps.

## Step 2 — Lock outcome + ask
Write the “after reading…” sentence and keep it visible while drafting.

Ask patterns:
- **Decision:** “Approve option B by Friday.”
- **Feedback:** “Reply with concerns by EOD Wednesday.”
- **Action:** “Please do X by DATE; I’ll do Y.”
- **FYI:** “No action needed; next update DATE.”

Failure mode: implied asks (readers don’t know what you want).

## Step 3 — Make the “how” concrete (don’t over-explain the premise)
Source insight: readers usually already accept the “what/why”. They need the “how”.

Include:
- What changes vs what stays the same
- Owners (names/roles) and dates
- Dependencies and risks

Failure mode: paragraphs of context with no actionable next steps.

## Step 4 — Structure for skim (clarity at scale)
Defaults that work for most audiences:
- **TL;DR first**
- Headings that match reader questions: “What’s happening?”, “What I need from you”, “Next steps”
- Bullets > paragraphs (especially for steps/asks)

Heuristic: if the reader only reads the TL;DR and headings, they should still act correctly.

## Step 5 — Draft to be forwarded
Write like your message might be forwarded to:
- A new exec who has zero context
- A partner team who is skeptical

Practical rules:
- Avoid “this/that/it” without nouns (“this change” vs “this”)
- Define acronyms on first use
- Put key numbers in writing (dates, scope cuts, thresholds)

## Step 6 — “Letter to yourself” clarity pass
Source insight: writing is a thinking tool. If you’re confused, the reader will be too.

Technique:
1) Write a blunt internal version (“What am I actually trying to say?”).
2) Extract the through-line (problem → decision → next steps).
3) Rewrite for the audience’s incentives and vocabulary.

Failure mode: polishing unclear thinking instead of clarifying it.

## Step 7 — Canonical doc (single source of truth)
Source insight: projects need one canonical place to learn the current state.

Canonical doc should make it easy to answer:
- What’s the latest?
- What decisions have been made?
- What’s next, and who owns it?

Include “last updated” and an update cadence to reduce anxiety and follow-ups.

## Step 8 — Quality gate
Before sending:
- Run [CHECKLISTS.md](CHECKLISTS.md)
- Score [RUBRIC.md](RUBRIC.md)
- Add **Risks / Open questions / Next steps**

Failure mode: sending a draft that creates more meetings and confusion than it prevents.

