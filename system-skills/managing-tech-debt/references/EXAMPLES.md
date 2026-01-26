# Examples

These examples illustrate what “good” looks like and help test the skill.

## Example A — Good (register + prioritization)
**Prompt:**  
“Use `managing-tech-debt`. System: `checkout-service` (Node + Postgres). Pain: weekly incidents from timeouts + slow releases. Horizon: 8 weeks. Constraint: 2 engineers available, on-call load high. Output: Tech Debt Management Pack with a prioritized register and 3 milestones.”

**Expected output highlights:**
- A register with 10–20 items including owner, symptoms, effort range, dependencies
- Top 5 items justified by incident frequency/impact + velocity tax
- Milestones start with observability and safe increments, not a full rewrite

## Example B — Good (rewrite decision + migration plan)
**Prompt:**  
“We think we must rebuild our pricing engine to support experimentation and marketplace rules. Compare refactor vs rebuild. Include migration phases, dual-run cost estimate ranges, cutover/decommission plan, rollback triggers, and success metrics.”

**Expected output highlights:**
- Options matrix with explicit criteria, not vibes
- A phased migration plan with acceptance criteria and rollback triggers
- Dual-run duration and staffing/on-call impact called out

## Example C — Boundary (insufficient context)
**Prompt:**  
“Fix our technical debt.”

**Expected response behavior:**
- Ask up to 5 intake questions (system, pain, horizon, constraints, decision-maker)
- If unanswered, proceed with assumptions and produce a minimal register schema + scoring model + next steps

