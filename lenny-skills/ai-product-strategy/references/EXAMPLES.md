# Examples (Expanded)

These examples are intentionally compact; use them as patterns, not copy.

## Example 1 — AI-first product (coding assistant)
Prompt: “Use `ai-product-strategy`. Product: AI coding assistant. Users: mid-market engineering teams. Constraints: beta in 8 weeks, must not leak proprietary code, cost cap, latency target. Output: AI Product Strategy Pack.”

Expected artifacts:
- Strategy thesis with workflow anchor (where the assistant fits), differentiation, and explicit non-goals
- Use-case portfolio (e.g., code explanation, refactors, PR review, test writing) with top 1–3 bets
- Autonomy policy that starts with copilot (suggestions + diffs) before agentic actions
- System plan with eval approach (offline test suite + online monitoring) and budgets
- Empirical plan (dogfooding + telemetry + iteration loop)
- Roadmap with exit criteria (quality, safety, cost, latency)

Common pitfalls:
- Shipping “agent” behavior without permissioning and rollback
- No eval coverage for regressions (non-determinism treated as “bug reports”)

## Example 2 — AI feature portfolio (customer support)
Prompt: “Use `ai-product-strategy`. Product: customer support platform. Goal: reduce time-to-resolution while maintaining CSAT. Decide copilot vs agent. Include safety posture and a 2-quarter roadmap.”

Expected artifacts:
- Use-case portfolio: summarization, suggested replies, KB draft, triage, agentic actions (refunds, plan changes) scored separately
- Autonomy policy: start with copilot suggestions; gate action-taking behind approvals
- Empirical plan: measure both utility (TTR, deflection) and risk (incorrect actions, escalations, policy violations)

Common pitfalls:
- Optimizing for automation without guardrails, auditability, or “must-not-do” constraints

## Boundary example — missing ICP and success metrics
Prompt: “What AI features should we build?”

Response pattern:
- Ask 3–5 Tier 1 intake questions (ICP, job/pain, why now, constraints, success metrics/guardrails)
- If still missing, propose 2–3 plausible ICP/use-case directions with explicit assumptions and recommend validating the problem before committing to a roadmap

