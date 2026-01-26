# Workflow notes (Technical Roadmaps)

This file expands the workflow in `skills/technical-roadmaps/SKILL.md` with practical guidance and patterns.

## Core principle: write it down so you can debug it
If the technical roadmap keeps getting misunderstood, the fix is often to produce a **single written strategy + roadmap** that can be reviewed, critiqued, and iterated.

## Rumelt strategy in practice (engineering version)

### Diagnosis (what’s true right now?)
Good inputs:
- Reliability signals (incidents, SLO breaches, pager load)
- Performance/cost signals (p95 latency, infra spend trends)
- Delivery signals (cycle time, lead time, deploy frequency, build times)
- Architecture constraints (coupling, scaling limits, data model bottlenecks)

Output characteristics:
- Specific, evidence-backed, and framed as constraints.
- Names the “why now” (what changed, what broke, what’s coming).

### Guiding policy (how will we approach it?)
Examples (choose 3–5, keep them crisp):
- “Prefer platform primitives over bespoke team solutions.”
- “Reduce coupling before attempting re-architecture.”
- “Stabilize reliability (SLOs) before scaling traffic.”
- “Security-by-default for all new services.”

### Coherent actions (what will we do?)
Engineering roadmap items should be:
- Outcome-oriented (what improves, by how much)
- Dependency-aware (what unblocks what)
- Sized enough to execute (or explicitly gated by an RFC/spike)

## Roadmap patterns that work well for engineering

### Time horizons
- 0–6 weeks: can be more specific (owners, milestones)
- 1–2 quarters: should be sequenced with dependencies, but avoid task-level detail
- 3–4 quarters: should be theme-heavy with major milestones and clear confidence levels

### Use “decision gates” to handle uncertainty
For any large or ambiguous item, avoid pretending you know the full solution up front. Add a gate as an explicit milestone:
- **Gate types:** RFC, architecture review, spike, prototype, load test, vendor evaluation.
- **Gate output:** a decision plus a smaller, clearer next milestone (or a kill decision).
- **Gate check:** “What did we learn that changes scope, sequence, or resourcing?”

Pattern:
- Gate → commit to near-term learning output
- After gate → re-sequence the roadmap using the new constraints

## Aligning technical roadmaps with product roadmaps
Technical roadmaps land best when they connect to product outcomes without pretending technical work is the product roadmap.

Practical moves:
- Add a **“product bet enabled”** column for each initiative where applicable.
- Describe technical work in terms of **risk reduction**, **time-to-ship**, **reliability**, **cost**, or **capability unlocks**.
- Separate “must do” (risk/compliance) from “should do” (improvement) from “could do” (nice-to-have).

## Common anti-patterns (and fixes)
- **Anti-pattern:** Roadmap is a list of activities.  
  **Fix:** Rewrite each item as an outcome with a success metric.
- **Anti-pattern:** No trade-offs; everything is “top priority”.  
  **Fix:** Add non-goals/cut list and explicitly name the constraints.
- **Anti-pattern:** No owners/dependencies, so execution stalls.  
  **Fix:** Assign owners and call out cross-team dependencies up front.
- **Anti-pattern:** Over-specific long-range dates.  
  **Fix:** Use themes + major milestones and label confidence; add decision gates.

## Recommended governance
- Treat the roadmap as a **living document** with a simple version history.
- Review cadence:
  - Weekly team check: are gates/milestones on track?
  - Monthly cross-functional review: dependency and trade-off review
  - Quarterly refresh: re-run Diagnosis and re-sequence as needed
