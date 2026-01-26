# Examples (Technical Roadmaps)

## Example A (good): reliability + scale
**Prompt:** “We’re adding 3× traffic in 6 months and reliability is shaky. Create a technical roadmap (2 quarters) for Platform Eng. Audience is VP Eng + Product leadership. Use quarterly format.”

**What a good output includes**
- Diagnosis with evidence (incident themes, SLO gaps, cost/latency)
- Guiding policy (3–5 principles)
- Roadmap table with owners, dependencies, milestones, confidence
- Initiative briefs for top items (e.g., SLO program, deploy pipeline hardening, database scaling)
- Risk register + governance cadence

## Example B (good): architecture modernization under product pressure
**Prompt:** “We need an architecture roadmap to migrate off a legacy monolith while still shipping product features. Provide Now/Next/Later with decision gates and metrics.”

**What a good output includes**
- Explicit trade-offs and non-goals
- Sequencing via dependencies (e.g., strangler pattern, service boundaries)
- Decision gates (RFC/spike) before large commitments
- Metrics for modernization progress and developer velocity

## Example C (boundary): task-level scheduling
**Prompt:** “Make a weekly plan with dates for every task for the next 6 months.”

**How to respond**
- Clarify that this skill outputs strategy → roadmap (themes/initiatives/milestones), not task scheduling.
- Suggest using `managing-timelines` for delivery planning once initiatives are chosen.

