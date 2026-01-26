# Checklists

## A) Feature brief checklist
- [ ] Job statement is one sentence and action-oriented.
- [ ] 3–5 explicit non-goals prevent scope creep.
- [ ] Success metrics and guardrails include quality, safety, cost, and latency.
- [ ] Top failure modes are listed and tied to user harm or trust loss.

## B) Prompt + tool contract checklist
- [ ] Prompt includes DO/DO NOT rules and “how to behave when uncertain.”
- [ ] Output format is explicit (schema if structured) and validated in evals.
- [ ] Tool descriptions include side effects and safety constraints.
- [ ] Any irreversible tool action requires confirmation and is logged.
- [ ] Prompt injection/tool misuse mitigations are documented.
- [ ] At least 3 examples exist: normal, tricky, refusal/abstain.

## C) Data + evaluation checklist
- [ ] Test set covers happy path, edge cases, and adversarial/red-team cases.
- [ ] Each test case names an expected trait and a source of truth.
- [ ] Rubric criteria have clear anchors (what “1” vs “5” means).
- [ ] Acceptance thresholds are explicit (pass rate / average score / must-pass cases).
- [ ] Every discovered bug adds a new test case (“evals as debugger”).
- [ ] Conflicting/ambiguous data is labeled and handled intentionally.

## D) Build + iteration checklist (coding agent safe use)
- [ ] Agent work is constrained (small diffs, clear tasks, minimal blast radius).
- [ ] No secrets are requested or written to prompts/logs/files.
- [ ] Tests/evals are run after changes; results are recorded.
- [ ] Code changes are reviewed like a PR (linting, style, security, edge cases).
- [ ] Rollback path exists (git diff, revert plan, feature flags).

## E) Production readiness checklist
- [ ] Cost and latency budgets are defined and monitored.
- [ ] Fallback/degeneration behavior is designed (retry, alternate prompt/model, cached response, human escalation).
- [ ] Logging fields include prompt version and model/version for debugging.
- [ ] Monitoring includes quality + safety + cost + latency + abuse signals.
- [ ] Rate limits and abuse protections exist (especially for tool use).
- [ ] Privacy/compliance constraints are satisfied (retention, redaction, access controls).

## F) Final pack checklist
- [ ] All deliverables are present in the specified order.
- [ ] Risks, open questions, and next steps are included and concrete.
- [ ] Checklist B–E pass; rubric score meets the bar (see [RUBRIC.md](RUBRIC.md)).

