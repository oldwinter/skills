# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with heuristics and common failure modes when vibe coding prototypes.

## Step 1 — Pick a single demo outcome
Heuristics:
- Force a one-sentence demo promise and a “hero” scenario. Everything else is optional.
- Choose non-goals that prevent “and also…” scope creep.

Failure modes:
- Building a pile of UI screens that don’t connect to a runnable flow.
- Trying to solve the whole product instead of a single demoable slice.

## Step 2 — Define the prototype’s contract (fake vs real)
Heuristics:
- Default to mock data and stubbed integrations unless the real integration is the point of the demo.
- Write acceptance criteria as observable behaviors (“User can…”).

Failure modes:
- Getting stuck on auth, databases, deployment, or polishing.
- Ambiguous success: “looks good” with no runnable path.

## Step 3 — Set the build loop + guardrails
Heuristics:
- Treat the coding agent like a fast junior engineer: specify constraints, ask for a plan, insist on small diffs.
- Keep a change log: what changed, why, how verified.

Failure modes:
- Large, unreviewable changes that break the app.
- Copy/pasting secrets or proprietary data into prompts/logs.

## Step 4 — Scaffold the thinnest runnable slice
Heuristics:
- Get to “it runs” fast. Then improve.
- Keep dependencies minimal and avoid novel stack choices during a timebox.

Failure modes:
- Spending the whole time on setup with nothing runnable.
- Over-engineering the architecture for a prototype.

## Step 5 — Iterate in vertical slices
Heuristics:
- Slice work by user-visible behavior, not by layers (UI-only, then backend-only).
- After each slice: run → verify → checkpoint (and optionally commit).

Failure modes:
- Refactors that don’t advance the demo.
- Not testing the flow, then discovering breakage during the demo.

## Step 6 — Optional helper tool (timeboxed)
Heuristics:
- Build the smallest helper that pays for itself immediately.
- Use it right away; otherwise it’s probably not worth it.

Failure modes:
- Building a tool because it’s fun, not because it accelerates the demo.
- Tooling rabbit hole that consumes the timebox.

## Step 7 — Package, quality gate, and handoff
Heuristics:
- Optimize for demo reliability: predictable run steps, stable data, clear narrative.
- Convert unknowns into explicit risks and next experiments.

Failure modes:
- No runbook; demo depends on the creator’s memory.
- “We should…” next steps that aren’t prioritized or owned.

