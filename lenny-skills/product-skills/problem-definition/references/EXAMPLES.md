# Examples (Problem Definition)

## Example 1 — B2B SaaS (activation drop)

**User prompt**
“Use `problem-definition`. Product: B2B analytics tool. Segment: ops managers at 50–500 employee companies. Signal: activation drops after connecting data sources. Decision: decide whether to invest in fixing activation this quarter. Output: Problem Definition Pack.”

**What a good output includes**
- A segment-specific problem statement (not “onboarding is bad”)
- Alternatives table including “ask IT for help”, “use CSV exports”, “do nothing”
- Evidence/assumptions log (e.g., root cause hypotheses: permissions, unclear value, time-to-first-insight)
- Metrics (activation completion rate, time-to-first-insight) + guardrails (support load, data integrity)
- Prototype plan (clickable prototype of guided connection, concierge onboarding call, usability test)

## Example 2 — Consumer (checkout abandonment)

**User prompt**
“Use `problem-definition`. Product: consumer marketplace app. Signal: mobile checkout abandonment rising 15% in 30 days. Constraints: must not increase fraud/chargebacks. Output: Problem Definition Pack.”

**What a good output includes**
- “Why now” tied to a trigger (payment provider change, UI regression, new traffic source)
- Alternatives table including “buy on desktop”, “use competitor”, “delay purchase”
- Guardrails including fraud, chargebacks, support contacts
- Prototype plan focused on the hardest unknown (trust cues vs form friction) rather than a full redesign

## Boundary example — Solution-first request

**User prompt**
“Write a PRD for an AI assistant that summarizes customer calls.”

**Good response**
- Pushes back: asks for the user pain point and job first
- Produces a minimal Problem Definition Pack with assumptions/tests
- Recommends handing off to `writing-prds` once the problem and success metrics are clear

