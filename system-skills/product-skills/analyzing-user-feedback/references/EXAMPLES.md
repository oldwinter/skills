# Examples

Use these to test that the skill produces **concrete artifacts**, not generic advice.

## Example 1 — Support tickets synthesis (B2B SaaS)

**Prompt**
“Use `analyzing-user-feedback`. Context: B2B SaaS. Area: onboarding + activation. Decision: what to fix in the next 2 sprints. Sources: last 90 days of support tickets (redacted excerpts) + churn survey comments. Segments: SMB vs Mid-market. Output: a User Feedback Analysis Pack.”

**Expected output structure**
1) Context snapshot
2) Source inventory + sampling plan (including segment coverage)
3) Taxonomy/codebook (themes + severity + root cause)
4) Tagged feedback table schema + sample rows (or full table if provided)
5) Themes & evidence report (top 5–10 themes with quotes + counts)
6) Ranked recommendations (bugs/UX/docs) + open questions
7) Feedback loop plan (cadence + owners + share-out)
8) Risks / Open questions / Next steps

## Example 2 — AI feature failure-mode analysis (trace review)

**Prompt**
“Use `analyzing-user-feedback`. Context: AI writing assistant. Area: ‘rewrite’ feature quality. Decision: what to improve before expanding rollout. Sources: 200 redacted production traces + 50 support tickets. Output: taxonomy of failure modes + top fixes + learning plan.”

**Expected output structure**
- Failure-mode taxonomy (e.g., factuality, instruction-following, tone mismatch, formatting errors)
- Tagged table (trace_id, prompt type, failure tag, severity, excerpt, notes)
- Theme report with examples and quantification (by failure mode)
- Recommendations split into: model/prompting, UX/guardrails, evaluation/instrumentation
- Risks + what to validate next

## Boundary example — No scope/data

**Prompt**
“Analyze user feedback for our product and tell us what to build.”

**Expected response**
- Ask up to 5 intake questions (decision, scope, sources, time window, segments).
- If data still isn’t available, produce a source inventory + sampling plan + proposed taxonomy and state limitations.

