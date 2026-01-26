# Intake (Question Bank)

Ask **up to 5 questions** (3–5 at a time). If answers are missing, proceed with explicit assumptions.

## Ask first (pick up to 5)
1) What is the **decision** to make (adopt / replace / build / defer), and by **when**?
2) What **problem/workflow** are we improving, and who are the primary users/stakeholders?
3) What is the **candidate technology** (vendor/product/version) and what alternatives are already on the table?
4) What is the **current stack/process**, and what’s broken or too slow/expensive/risky today?
5) What are the **hard constraints** (security/privacy/compliance, budget, deployment model, data residency, timeline, integration requirements)?

## Success, constraints, and “deal breakers”
- What does success look like in 30/60/90 days (leading + lagging metrics)?
- What are non-goals (what we explicitly will NOT do)?
- What would make this an immediate “no” (deal breakers)?
- What is the acceptable risk level (sandbox pilot vs production-grade from day one)?

## Options and evaluation criteria
- What are the realistic options? (Status quo, vendor A/B/C, build, hybrid)
- Which criteria matter most? (time-to-value, TCO, security posture, UX, flexibility, lock-in, reliability)
- How will we score options (1–5 scale, weighted criteria, or pass/fail gates)?

## Build vs buy specifics
- What would we build (scope boundaries) and what would we buy?
- Who will maintain it 12 months from now (on-call, upgrades, support)?
- What is the opportunity cost (what won’t the team build if we build this)?
- Is this a core competency / differentiator, or table stakes?

## Integration and data fit
- Required integrations: SSO, RBAC, audit logs, APIs/webhooks, data pipelines, CI/CD, ticketing, etc.
- Data sources/sinks: where does data originate, where must it end up, and who owns it?
- Migration needs: backfills, schema changes, historical data, downtime tolerance.
- Exit path: data export, contract terms, switching costs.

## AI-specific (if relevant)
- What data will be sent to the model/vendor (PII? sensitive customer data? code/IP)?
- Does the vendor train on your data by default? Retention/deletion policy?
- What are the top model failure modes (hallucination, toxicity, prompt injection, leakage)?
- What “guardrails” are claimed, and what is the fallback/defense-in-depth plan?

## Pilot/proof-of-value
- What is the smallest pilot that is still representative?
- Pilot success criteria: what would convince us to adopt vs reject?
- Who will run the pilot, and what resources are required?
- What is the rollback and data deletion plan if we stop?

