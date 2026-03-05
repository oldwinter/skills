# Enterprise Sales — Examples

Use these as “golden prompts” to invoke the skill and as shape examples for outputs.

## Example 1 — Procurement + security tracker + MAP
Prompt:
“Use `enterprise-sales`. Product: <...>. Account: <...>. Deal: ACV ~$80k, timeline 6 weeks. Stakeholders: champion in Ops, economic buyer in Finance, security review owned by IT. Blocker: procurement vendor onboarding + security questionnaire. Output: an Enterprise Deal Execution Pack with a MAP, procurement/security tracker, and champion one-pagers.”

Expected output highlights:
- A MAP with a decision date and buyer-owned tasks
- A procurement/security tracker with owners, due dates, and blockers
- Forwardable one-pagers for IT/Security, Procurement, Legal, and the Economic Buyer

## Example 2 — POC reframed as business-case pilot
Prompt:
“Use `enterprise-sales`. We’re being asked for a POC to ‘prove it works’. ACV target $150k. We can do a 30-day pilot. Output: a pilot plan that produces an ROI model and a decision-ready business case.”

Expected output highlights:
- Success metrics table with baselines/targets and data sources
- A simple ROI model with explicit assumptions
- Decision criteria and decision meeting scheduled before kickoff

## Boundary example — No deal context
Prompt:
“Teach me enterprise sales.”

Expected response behavior:
- Ask for a specific deal/account context (up to 5 intake questions)
- If the user can’t provide it, proceed with explicit assumptions and a “validation plan,” but keep the output framed as a deal pack (not generic advice)

