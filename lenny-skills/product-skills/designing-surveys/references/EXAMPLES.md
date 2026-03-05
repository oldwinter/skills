# Examples (Designing Surveys)

Use these as invocation and output-shape examples.

## Example 1 — Onboarding profiling (B2B SaaS)

**Prompt:** “Use `designing-surveys`. We’re a B2B analytics tool. Decision: route new signups to the right onboarding path and prevent sales from contacting non-buyers. Survey type: onboarding profiling. Channel: in-product during first session. Constraints: keep under 2 minutes. Output: Survey Pack.”

**Expected output characteristics**
- Profiling questions only (role, company size, use case, buyer vs user)
- 3–4 screens max
- Clear routing rules implied in the analysis plan

**Sample questionnaire rows**
| ID | Section | Question | Type | Options / Scale | Required | Logic | Rationale |
|---:|---|---|---|---|:---:|---|---|
| Q01 | Profile | What best describes your role? | single_choice | {role list} + Other | Y |  | Route onboarding |
| Q02 | Profile | What’s your primary use case for <product>? | single_choice | {use cases} + Other | Y |  | Personalize onboarding |
| Q03 | Profile | Are you evaluating for yourself or for a team? | single_choice | Myself / Team | Y |  | Separate buyer vs user |

## Example 2 — CSAT + friction drivers (product workflow)

**Prompt:** “Use `designing-surveys`. We want to reduce churn for API users. Decision: which 2–3 friction points to fix next quarter. Survey type: CSAT + drivers. Channel: email to active API users. Constraints: segment by plan tier and tenure. Output: Survey Pack with forced ranking + frequency.”

**Expected output characteristics**
- CSAT (1–7) + “primary reason” follow-up
- “Pick top 3 barriers” diagnostic + frequency/impact weighting plan
- Analysis plan yields a ranked list by segment (plan tier/tenure)

## Boundary example — Causality request

**Prompt:** “We shipped feature X and retention went up. Design a survey to prove feature X caused it.”

**How to respond**
- Push back on causality: surveys can provide context, not proof.
- Recommend instrumentation/experiment for causality.
- Offer a small contextual survey only if needed (e.g., “What changed in your workflow?”) and/or interviews for depth.

