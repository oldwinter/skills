# Checklists

Use these before finalizing an **AI Evals Pack**.

## 1) Eval PRD checklist
- Decision is explicit (ship/no-ship, compare A vs B, regression gate).
- SUT is clearly described (inputs → outputs; workflow; any tool calls).
- Target behaviors include both must-do and must-not-do items.
- Acceptance thresholds are written and include “must-pass” blocking criteria.
- Non-goals are stated to prevent scope creep.

## 2) Golden set + coverage checklist
- Case schema is defined and consistent; IDs are stable.
- Each target behavior has ≥2 cases; each critical risk has ≥3 cases.
- Cases are tagged (scenario, severity, segment) to enable slice reporting.
- Data handling is safe (redaction/anonymization rules; no secrets/PII leakage).
- Includes adversarial/safety cases where relevant (prompt injection, jailbreak attempts, policy violations).

## 3) Taxonomy checklist
- Categories are specific enough to drive fixes (not “bad answer”).
- Each category has 1–2 concrete examples and a severity definition.
- Taxonomy reflects both user-visible issues and likely root causes (kept distinct).

## 4) Rubric checklist
- Dimensions match the task (e.g., factuality/grounding for RAG; schema validity for JSON).
- Scale is behaviorally anchored with clear pass/fail definitions.
- Tie-breakers are defined (what matters most when trade-offs exist).
- Includes explicit disallowed behaviors (safety/compliance, privacy, hallucination).

## 5) Judge + harness checklist
- Judge choice is justified (human vs LLM judge vs automated checks).
- Calibration plan exists (gold examples; inter-rater agreement target).
- Runbook is repeatable (versioned prompts/models; stable dataset; deterministic settings where possible).
- Cost/time estimate exists and is within constraints.

## 6) Reporting + iteration checklist
- Report includes overall + per-tag metrics (critical tags highlighted).
- Regression policy is explicit (what blocks shipping; how to resolve trade-offs).
- Every discovered failure produces a new/updated test and taxonomy update.
- Ends with **Risks / Open questions / Next steps**.

