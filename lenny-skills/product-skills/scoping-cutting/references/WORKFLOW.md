# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and heuristics.

## Step 1 — Intake + decision framing
Rules of thumb:
- If the decision isn’t explicit, scope discussions will loop forever.
- Always name the DRI/decision owner; otherwise every stakeholder becomes a “scope approver”.

Useful outputs:
- A 1-sentence decision statement (“We will ship <slice> by <date>…”)
- A short list of non-negotiables (privacy, reliability, brand, compliance)

## Step 2 — Outcome + hypothesis (MVP = test)
Rewrite “MVP” into a testable claim:
- “We believe <segment> will <behavior/outcome> if we <capability>, because <reason>. We’ll know by <metric/threshold>.”

Common failure mode:
- “MVP = low quality product.” Instead, keep a high bar on trust/safety/clarity and cut breadth.

## Step 3 — Appetite (time as a budget)
The point of appetite is to change the conversation:
- From “how long will this take?” → “how much time are we willing to spend?”
- From “extend the deadline” → “shrink the solution”

Heuristics:
- Pick a single appetite (2/4/6 weeks) and design the slice to fit.
- Keep teams small when possible; coordination overhead is scope.

## Step 4 — Minimum Lovable Slice (MLS)
MLS is not “polish everything.” It’s:
- A coherent end-to-end flow
- Clear UX copy/states so users trust what’s happening
- 1–2 high-leverage “lovability” choices (often clarity, feedback, defaults)

Anti-patterns:
- Shipping a half-flow (“backend done, UI later”)
- Adding random animation/polish while the core flow is incomplete

## Step 5 — Cut list with trade-offs
How to cut without regret:
- Prefer cutting **rare edge cases** over degrading the core flow.
- Cut configuration surfaces before cutting core value.
- When in doubt, defer breadth and keep depth on the happy path.

Make cuts explicit:
- “Non-goals” are part of the product spec.
- Add a revisit trigger (“when adoption > X” / “when we onboard segment Y”).

## Step 6 — Validation (Wizard-of-Oz / concierge)
Use manual approaches when the biggest unknown is **value**, not implementation:
- If you can deliver value manually for 10–50 users, do it.
- Design the manual process so it’s honest and safe (no deception that implies guarantees).

Checklist for a good Wizard-of-Oz test:
- The “fake” is invisible to the user *only insofar as it doesn’t misrepresent risk*.
- You can run it with available people/time.
- You capture learnings in a structured way (script + notes + success criteria).

## Step 7 — Scope-change guardrails (prevent creep)
Define “trade, don’t add” mechanics:
- A place where scope requests land (single backlog section)
- A rule for evaluation (impact on outcome, risk, appetite)
- A default cut order (edge cases → integrations → advanced settings → polish)

Common failure mode:
- “We’ll decide later” becomes “we silently add it,” and the appetite explodes.

## Step 8 — Quality gate + finalize
Before sharing:
- Run [CHECKLISTS.md](CHECKLISTS.md) and score [RUBRIC.md](RUBRIC.md)
- Ensure **Risks / Open questions / Next steps** exist and are decision-useful
- Confirm the pack could be executed without another scope meeting

