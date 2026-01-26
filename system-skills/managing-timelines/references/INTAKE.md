# Intake (Managing Timelines)

Ask **up to 5 questions at a time**. Prefer questions that would change the date, scope, or resourcing decision.

## Quick-start (pick the most important 5)

1) **What is the date type?**
   - Fixed external deadline (event/regulatory/contract)?
   - Internal target date?
   - Window (“late March”)?
   - Who is the decision owner for changing the date or scope?

2) **What are we shipping (minimum)?**
   - “Done means…” in 1–3 bullets
   - Explicit non-goals (what is out)

3) **What constraints are non-negotiable?**
   - Quality/reliability bar, compliance/privacy/security, platform constraints
   - “Must not worsen” guardrails (e.g., latency, support load, cost)

4) **Who is the team and what is capacity?**
   - Roles (Eng/Design/DS/PMM), availability, competing priorities
   - Any planned PTO / freezes

5) **What dependencies or approvals could block us?**
   - Other teams, vendors, data access, legal/security review, launch approvals

## Deeper clarifiers (ask only if needed)

### Scope & uncertainty
- What are the biggest unknowns right now (top 3)?
- What is already decided vs still open (requirements, UX, tech approach)?

### Stakeholders & comms
- Who needs weekly updates? Who needs immediate escalation on “red”?
- What format works best (Slack/email/doc)? Any standing forums?

### Risk tolerance & trade-offs
- If we slip, what is the least-bad trade: cut scope, add resources, reduce quality, move date?
- What’s the fastest acceptable rollback/mitigation if something goes wrong at launch?

### AI/ML-specific (only if applicable)
- Is this a prototype/demo, or production user-facing?
- What is the evaluation plan (quality metrics, red-teaming, safety constraints)?
- Data availability and privacy constraints (PII, retention, vendor usage)?
- What are the “outer loop” requirements: monitoring, fallback behavior, cost/latency budgets?

## Default assumptions (if the user can’t answer)
- Treat the date as a **target**, not a commitment, until solutioning is complete.
- Commit only to the **next phase output** and a “next re-forecast date”.
- Use weekly RAG updates with explicit asks/decisions when yellow/red.

