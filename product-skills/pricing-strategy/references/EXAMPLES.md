# Pricing Strategy — Example Prompts and Outputs

These examples show what “good” looks like for the deliverables. Use them as calibration, not as copy/paste pricing advice.

## Example 1: B2B SaaS repricing (hybrid motion)
**Prompt:**  
“Use `pricing-strategy`. We sell analytics to finance teams. Current: $99/user/mo with a 14-day trial. Goal: increase expansion revenue without hurting retention. Motion: self-serve + sales assist. Constraints: must keep a free tier; SSO only on enterprise. Output: Pricing Strategy Pack.”

**Expected output highlights:**
- Segment map distinguishes buyer (Head of Finance) vs user (analyst).
- Value metric candidates include seats vs connected data sources; selects one primary with rationale.
- Packaging table includes a self-serve “Pro” and a sales-led “Enterprise” with explicit triggers (SSO, invoicing, contract size).
- WTP plan includes 10–15 interviews across segments + a pilot offer for a new “Team” plan.
- Conversion mechanics include sampling premium reports and a capped trial for advanced exports.
- Rollout plan includes grandfathering rules and rollback criteria.

## Example 2: Consumer freemium with reverse trial
**Prompt:**  
“Use `pricing-strategy`. We’re a habit tracking app. Current: freemium with $7.99/mo. Goal: improve upgrades via reverse trial while protecting retention. Output: pricing + trial mechanics + experiment backlog.”

**Expected output highlights:**
- Reverse trial plan (premium enabled for 7 days) with abuse controls and cohorting.
- Experiment backlog includes retention guardrails and “time-to-habit” proxy metrics.
- Pricing cadence and triggers are defined (major feature releases, conversion drift).

## Boundary example: No context
**Prompt:**  
“Pick the best price for our product.”

**Good response pattern:**
- Ask 3–5 intake questions (ICP/use case, objective, current pricing, motion, constraints).
- Provide a WTP plan and 2–3 pricing architecture options with explicit assumptions.

