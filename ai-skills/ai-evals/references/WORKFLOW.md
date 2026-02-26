# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with practical heuristics and common failure modes when designing AI/LLM evals.

## Step 1 — Define the decision and write the Eval PRD
Heuristics:
- Treat the eval as a product requirement: define a decision, acceptance thresholds, and non-goals.
- If stakes are high, split requirements into “must-pass” (blocking) vs “nice-to-have” (non-blocking).

Failure modes:
- “We’ll know it when we see it” (no measurable pass criteria).
- Measuring the wrong thing (optimizing vibe while missing safety/compliance).

## Step 2 — Draft golden set structure + coverage plan
Heuristics:
- Start small (20–50 high-signal cases) before scaling.
- Tag every case (scenario, user segment, severity, risk type) to enable per-slice reporting.

Failure modes:
- Only happy-path cases → regressions appear in production.
- Mixed/ambiguous expected outputs with no rubric guidance.

## Step 3 — Error analysis + open coding → taxonomy
Heuristics:
- Every failure must become: a category, a severity, and a candidate test case.
- Separate “symptoms” (wrong tone) from likely causes (missing context, prompt ambiguity).

Failure modes:
- Taxonomy that is too generic (“bad answer”) to drive improvements.
- Overfitting taxonomy to one week of failures; missing long-tail risks.

## Step 4 — Taxonomy → rubric + scoring rules
Heuristics:
- Prefer behaviorally anchored scales (“includes X”, “omits Y”) over abstract adjectives (“good”, “helpful”).
- Decide whether you need absolute scores or pairwise comparisons (pairwise is often easier for subjective outputs).

Failure modes:
- Rubric that judges “style” while ignoring factuality/grounding.
- Rubric that cannot be executed consistently by different judges.

## Step 5 — Choose judge + harness/runbook
Heuristics:
- Use layered evaluation: automated checks (schema/safety) + LLM judge/human for semantic quality.
- Calibrate judges using a small set of “gold” examples with expected scores; measure agreement.

Failure modes:
- LLM-as-judge without guardrails (leaks, bias, prompt injection via model output).
- Non-repeatable runs (no versioning; changing prompts/models silently).

## Step 6 — Reporting, thresholds, iteration loop
Heuristics:
- Always report slice metrics: overall score hides regressions in critical segments.
- Define “regression policy” explicitly (what blocks shipping; how to handle trade-offs).

Failure modes:
- Winning overall score while breaking a critical tag (“billing refunds” got worse).
- No clear “next action”; results don’t translate into product/eng work.

## Step 7 — Quality gate + finalize
Heuristics:
- Use the checklists and rubric; don’t “feel” done.
- Convert open questions into concrete experiments or data collection tasks.

Failure modes:
- A pack that is insightful but not executable (missing schema, runbook, thresholds).
- Risks are noted but not owned; next steps aren’t prioritized.

