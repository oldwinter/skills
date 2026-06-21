# Examples — Sales Qualification

## Example 1 — Inbound volume, low win rate (SDR triage)
**Prompt:**  
“Use `sales-qualification`. We sell B2B SaaS to operations teams at 50–500 employee companies. Inbound is high volume, but AEs say meetings are low quality. ACV $12k, cycle ~45 days. We have SDRs qualifying and handing off to AEs. Output: Sales Qualification Pack.”

**What “good” looks like:**
- Clear disqualifiers that prevent SDRs from booking “maybe forever” meetings
- Scorecard thresholds that separate accept vs nurture vs reject
- Script that covers urgency and decision process (not only pain)
- Stage exit criteria that prevent opportunities without a next step

## Example 2 — Outbound, complex stakeholders (enterprise-ish)
**Prompt:**  
“Use `sales-qualification`. We sell to security leadership. ACV $75k–$250k, cycle 120–180 days. Deals stall after first call because we don’t understand procurement and stakeholders early. Output: disqualifiers, scorecard, and CRM notes template + hygiene rules.”

**What “good” looks like:**
- Scorecard includes access/process clarity and stakeholder mapping
- Script includes procurement/security requirements early enough to disqualify or plan
- CRM notes template captures decision steps + owners + timeline consistently

## Boundary example — Wrong intent / missing ICP
**Prompt:**  
“Write a universal script that qualifies any lead for any product.”

**Good response:**
- Explain qualification is product/ICP-specific; ask 3–5 intake questions
- If the user cannot provide an ICP, recommend upstream work (e.g., `problem-definition` and/or `positioning-messaging`)

