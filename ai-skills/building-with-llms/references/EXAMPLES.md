# Examples (detailed)

## Example 1 — Support copilot with citations (good)

Scenario: Draft customer support replies using internal KB articles.

Key choices:
- Pattern: copilot (suggestions only), human approves send.
- Context strategy: RAG over approved KB only; require citations.
- Eval: must-pass privacy cases; rubric includes “groundedness” and “policy compliance.”

Artifacts to produce (using [TEMPLATES.md](TEMPLATES.md)):
- Feature brief (with strict non-goals: “never fabricate policy”)
- Prompt + tool contract (citations required; abstain when no KB coverage)
- Data + eval plan (red-team: prompt injection, PII exfiltration)
- Launch plan (monitor citation rate, escalation rate, cost/ticket)

## Example 2 — Tool-using triage assistant (good)

Scenario: Summarize bug reports and propose Jira tickets; tool creates tickets after confirmation.

Key choices:
- Pattern: tool-using agent with human confirmations for `create_ticket`.
- Output schema: JSON with required fields (title, severity, repro steps, suggested owner).
- Eval: schema validity + “no over-creation” (avoid spam tickets).

## Example 3 — “Make it smarter” (bad / boundary)

Prompt: “Our AI is not smart enough. Improve it.”

Why this fails:
- No job statement, no constraints, no success metric, no eval plan.

How to respond:
- Ask 3–5 intake questions from [INTAKE.md](INTAKE.md) (use case, failure modes, constraints).
- Propose a starter eval set and a thin-slice prototype plan rather than changing prompts blindly.

