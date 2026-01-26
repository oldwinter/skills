# Checklists

## A) Scope + demo promise checklist
- [ ] Demo promise is one sentence and timeboxed.
- [ ] Hero scenario is a single runnable flow (not a list of screens).
- [ ] 3–5 explicit non-goals prevent scope creep.
- [ ] “Fake vs real” decisions are explicit (data, integrations, auth).

## B) Prototype spec checklist
- [ ] User flow is written as 3–7 concrete steps.
- [ ] Acceptance criteria are observable (“User can…”).
- [ ] Data model is simple and includes example mock data.
- [ ] Out-of-scope items are listed.

## C) Vibe coding loop checklist (agent-assisted execution)
- [ ] Agent receives constraints and asks clarifying questions when needed.
- [ ] Changes are small and localized; file list is explicit.
- [ ] App is run and verified after each slice (or tests are run).
- [ ] A short change log exists (what changed, why, how verified).
- [ ] No secrets/credentials are requested, pasted, or written to files.

## D) “Build tools to build the thing” checklist (optional)
- [ ] The helper tool is timeboxed and has a clear payoff within the demo.
- [ ] The tool is immediately used to advance the prototype.
- [ ] If payoff isn’t clear, the tool is cut.

## E) Demo readiness checklist
- [ ] Runbook enables a fresh user to run the prototype in ≤ 5 minutes.
- [ ] Demo script is 3–5 minutes and tells a coherent story.
- [ ] Demo does not rely on fragile external dependencies when avoidable.
- [ ] Backup plan exists (fallback flow or recording).

## F) Final pack checklist
- [ ] All deliverables are present in the specified order (brief → spec → prompts → plan → demo → risks).
- [ ] Risks, open questions, and next steps are specific and prioritized.
- [ ] Rubric score meets the bar (see [RUBRIC.md](RUBRIC.md)).

