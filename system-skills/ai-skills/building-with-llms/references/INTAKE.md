# Intake questions (ask 3–5 at a time)

## 1) Goal + users
- Who is the target user and what workflow step are we improving?
- What is the “job to be done” for the LLM in one sentence?
- What does success look like (1–3 metrics) and what are the top 3 failure modes?

## 2) Product surface + autonomy
- Where does this live (UI, API, internal tool)? Who approves outputs?
- Should the LLM only suggest, or can it take actions via tools? If it can act, what approvals are required?
- What are explicit non-goals (3–5)?

## 3) Data + context sources
- What information should the LLM rely on (docs, DBs, tickets, codebase, user input)?
- What are the sources of truth, and what happens when sources conflict?
- What freshness requirements exist (real-time vs daily vs static)?

## 4) Constraints (hard)
- Privacy/compliance: PII/PHI? retention limits? audit needs? regions?
- Latency target (p50/p95) and throughput expectations.
- Cost target (per request / per user / per task).
- Reliability expectations: what failure is acceptable and what must never happen?

## 5) Output + integrations
- What should the output look like (freeform text, JSON schema, citations, tool calls)?
- What tools/APIs are available? Any rate limits or side effects?
- Any must-use libraries/patterns or existing services?

## 6) Evaluation + iteration
- Do we have historical examples or “golden” outputs to seed a test set?
- What are acceptable thresholds (e.g., pass rate, rubric score, escalation rate)?
- How will we collect feedback post-launch (thumbs, edits, support tickets, human review labels)?

## 7) Engineering context (if building code)
- Repo/language/runtime and where this will be implemented.
- Test strategy: existing tests, how to run them, CI expectations.
- Deployment model and rollback mechanism.

