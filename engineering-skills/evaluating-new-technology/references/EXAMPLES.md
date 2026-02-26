# Examples

## Example 1 — AI vendor evaluation (guardrails/tooling)
Prompt:
“Use `evaluating-new-technology`. Candidate: an AI ‘guardrails’ vendor that claims to block prompt injection. Problem: we’re launching a customer-facing support agent and need safer tool use. Current stack: Zendesk + internal KB. Constraints: SOC2 required, PII present, SSO required, budget $50k/yr, decision in 3 weeks. Output: Technology Evaluation Pack.”

What “good” looks like:
- Criteria include measurable safety tests (red-team suite) and operational controls (SSO, audit logs, data retention).
- Risk review treats vendor claims skeptically and proposes defense-in-depth.
- Pilot is time-boxed with exit criteria.

## Example 2 — Product analytics stack decision
Prompt:
“Use `evaluating-new-technology`. Candidate: PostHog vs Amplitude. Problem: onboarding and activation iteration is slow; instrumentation is inconsistent. Current stack: Segment + warehouse + basic email tool. Constraints: minimal eng time for migration; GDPR and EU residency required. Output: Technology Evaluation Pack.”

What “good” looks like:
- Options include status quo + phased adoption path.
- Integration notes cover event taxonomy, migration/backfill, and lifecycle triggers.
- Pilot measures improved iteration speed and activation lift.

## Boundary example — No real problem
Prompt:
“What’s the best new AI tool to adopt?”

Response:
- Ask intake questions first; recommend `problem-definition` if there’s no concrete workflow/job-to-be-done.

