# Examples (Shipping Products)

These are illustrative prompts and what “good” output looks like (artifact-driven, not generic advice).

## Example 1 — B2B SaaS (staged rollout + enablement)
**Prompt:** “We’re shipping Role-Based Access Control (RBAC) for admins in 3 weeks. Create a Shipping & Launch Pack: staged rollout, go/no-go criteria (PQL), support enablement, and internal/external comms.”

**What good output includes**
- A clear scope/non-goals (e.g., “no custom roles in v1”)
- Rollout: internal → selected beta customers → 25% → 100%, with eligibility rules and a kill switch owner
- A PQL focused on permissions edge cases (least privilege, downgrade/upgrade flows, audit logs if relevant)
- Support assets: troubleshooting notes, known issues, escalation path
- Comms: internal “what changed / how to sell / FAQs” + customer messaging (if external)

## Example 2 — Consumer app (flagged rollout + monitoring)
**Prompt:** “Ship ‘saved searches’ to 10% of users next week behind a flag. Define monitoring and rollback triggers, and a launch day runbook.”

**What good output includes**
- Slices: “create saved search” first, then “manage list”, then “notifications” later
- Guardrails: crash rate, latency, opt-out/uninstall, support tickets
- Stop-the-line triggers and specific rollback steps (who toggles, how quickly, what happens to user state)
- A runbook timeline (T-1d checks, T0 rollout, T+1h review, T+24h retro)

## Boundary example — Not a shipping problem
**Prompt:** “Decide our roadmap for the next 6 months across 15 initiatives.”

**How the skill should respond**
- Push back: this is a prioritization/strategy problem
- Recommend `prioritizing-roadmap` (and/or `defining-product-vision`) first
- Then apply `shipping-products` to the chosen initiative’s release

