# Examples

## Example 1 (consumer onboarding calibration)

**Prompt**
“Use `product-taste-intuition`. Domain: onboarding. Target user + job: first-time user trying to connect their bank account and see value in 2 minutes. Benchmarks: unknown—propose. Time box: 90 minutes. Constraints: mobile-first, high trust, accessibility AA. Output: a Taste Calibration Pack.”

**Expected characteristics**
- Benchmarks include direct (fintech) + outside-category (e.g., best-in-class identity/trust flows).
- Study notes capture at least 3 concrete moments per benchmark.
- Rules include trust cues, error recovery, perceived speed.
- Hypotheses include predicted/counter-signals and smallest viable validation tests.

## Example 2 (B2B workflow “feels slow” intuition)

**Prompt**
“Use `product-taste-intuition`. Domain: editor/workflow. Target user + job: power user creating a new project in under 60 seconds. Benchmarks: Linear, Notion, Figma. Time box: 60 minutes. Output: hypotheses + validation plan.”

**Expected characteristics**
- Intuition statements are translated into falsifiable hypotheses (e.g., perceived latency, cognitive load, default choices).
- Validation plan proposes quick checks (5-user task, replay review, instrumentation slice).

## Boundary example (too broad)

**Prompt**
“Teach me good product taste.”

**Expected response**
- Ask for a domain + target user/job (max 5 questions).
- If still missing, propose a narrow starting domain and a short benchmark shortlist rather than generic advice.

