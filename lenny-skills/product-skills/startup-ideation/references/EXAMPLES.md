# Examples

These examples show what “good” looks like at the prompt level and what artifacts to expect.

## Example 1 — Domain advantage (B2B)

**Prompt**
“Use `startup-ideation`. We’re 2 founders: ex‑ops managers in logistics + a PM from warehouse software. Constraints: 3 months runway, can do sales calls, prefer B2B SaaS. Decision: pick 1 idea to validate in 14 days. Output: Startup Ideation Pack.”

**Expected artifacts**
- Signals list grounded in real workflows (dock scheduling, compliance paperwork, exception handling)
- Shift scan (automation costs dropping, new APIs, labor constraints)
- 15–30 opportunity theses with first tests
- Scorecard for top 3–5 with evidence
- Top idea brief + 2-week plan (10 interviews, concierge pilot, clear pass/fail)

## Example 2 — Why Now (AI capability shift)

**Prompt**
“Use `startup-ideation`. We want a startup idea enabled by new LLM capabilities. Prefer B2B. Constraints: strong engineering, weak sales. Decision: shortlist 3 ideas and pick 1 to validate. Output: Startup Ideation Pack.”

**Expected artifacts**
- Shift scan identifies specific capability shifts (e.g., reliable extraction/classification; voice; tool use)
- Theses are grounded in a workflow (support QA, compliance review, back office ops) rather than generic “AI assistant”
- Scorecard penalizes ideas requiring enterprise sales motions
- Validation plan includes non-building tests and stop rules

## Boundary example — No context

**Prompt**
“Give me 100 startup ideas.”

**Expected response**
- Ask 3–5 intake questions first.
- If the user refuses, produce a small set of generic theses with explicit assumptions and advise how to gather signals before scaling the list.

