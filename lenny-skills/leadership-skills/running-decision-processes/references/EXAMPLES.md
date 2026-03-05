# Examples — Running Decision Processes

Use these as patterns for prompts and expected outputs.

## Example 1 (typical): Sunset a feature
**Prompt:** “Use `running-decision-processes`. Decision: sunset Feature X. Deadline: March 15. Context: support load is rising and adoption is falling. Constraints: no downtime; must notify top customers 30 days prior. Stakeholders: PM, Eng, Support, Sales, Legal. Options: keep as-is, invest to fix, sunset. Output: Decision Process Pack.”

**Good output includes**
- One-sentence decision + deadline + one-way/two-way door classification
- Options/criteria matrix with explicit assumptions (customer churn risk, support cost trajectory)
- DACI/RAPID roles and a lightweight consult plan (Sales + Support + Legal pre-read)
- Decision log entry with tradeoffs and review date
- Draft customer-facing and internal comms (or at least internal + plan for external)

## Example 2 (high stakes): Build vs buy (one-way door)
**Prompt:** “We must decide build vs buy for analytics by Feb 2. One-way door. Budget $250k/yr. Security requires SOC2. Output a rigorous Decision Process Pack.”

**Good output includes**
- Weighted criteria (time-to-value, security, total cost, flexibility, switching cost)
- Explicit veto/escalation rules for Security/Legal/Finance
- Curiosity loop to 8–12 peers (who have done build/buy) with rationale capture
- Clear Decider and ownership for follow-through

## Boundary example (not a fit)
**Prompt:** “Decide if our weekly sync should be 30 or 45 minutes.”

**Response pattern**
- Identify as a low-stakes, reversible two-way door.
- Recommend a lightweight experiment instead (timebox, measure, decide later) rather than a full Decision Process Pack.

