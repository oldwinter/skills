# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with heuristics and common failure modes.

## Step 1 — Start with the problem (avoid tool bias)
Heuristics:
- Force a one-sentence problem statement without naming the technology.
- Write non-goals early to prevent “shiny object” scope creep.

Failure modes:
- Selecting tools because they’re trendy (“AI-first”) rather than useful.
- Evaluating features instead of whether a workflow improves.

## Step 2 — Define “good” and hard constraints
Heuristics:
- Use a mix of outcome metrics (e.g., activation, cycle time) and operational constraints (security, uptime, cost).
- Make “deal breakers” explicit (e.g., no SSO, no SOC2, no EU residency).

Failure modes:
- Starting a pilot with no success criteria.
- Underestimating compliance/security constraints until procurement blocks launch.

## Step 3 — Map options and evaluation criteria (workflows → ROI)
Heuristics:
- Always include “do nothing/status quo” as an option.
- Anchor criteria to workflows and ROI (time saved, revenue impact, risk reduction), not vendor checklists.

Failure modes:
- Comparing tools on superficial features.
- Only evaluating the “preferred” option; missing credible alternatives.

## Step 4 — Fast reality check: integration + data fit
Heuristics:
- Draw the data/control flow (inputs → processing → outputs) in bullets.
- Prefer tools that fit your existing stack layers (data hub, analytics, lifecycle) over tools that require a rebuild.

Failure modes:
- Integration complexity dominates the timeline.
- No plan for data export/exit → accidental lock-in.

## Step 5 — Build vs buy with bandwidth as a first-class cost
Heuristics:
- Model “bandwidth” as a real cost: build time + maintenance + on-call + upgrades.
- Build only if it’s a differentiator or vendors are unacceptable (security, cost, capability, control).

Failure modes:
- “We can build it quickly with AI” → long-term maintenance trap.
- Ignoring opportunity cost (what you’re not building).

## Step 6 — Risk & guardrails review (skepticism is healthy)
Heuristics:
- Treat vendor security claims as hypotheses to verify (not facts).
- For AI: assume guardrails are imperfect; design defense-in-depth (permissions, logging, human approvals, evals).

Failure modes:
- Relying on a single “guardrails” layer for security.
- No ownership for risks; mitigations are vague.

## Step 7 — Plan a proof-of-value pilot (or document why you can skip it)
Heuristics:
- Keep the pilot small but real: representative data, real users, real workflow.
- Make exit criteria binary (adopt / iterate / reject) and time-box it.

Failure modes:
- Endless pilots with moving goalposts.
- Pilots that only test demos, not production realities (SSO, logs, permissions, deletion).

## Step 8 — Decide, communicate, and quality-gate
Heuristics:
- Write the decision memo for the next owner who wasn’t in the room.
- Use the checklist + rubric; tighten unclear assumptions and add “next experiments.”

Failure modes:
- A recommendation without an adoption/rollback plan.
- Decision is undocumented; re-litigated every quarter.

