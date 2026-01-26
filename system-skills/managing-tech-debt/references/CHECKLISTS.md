# Checklists (Quality Gate)

Use these before finalizing the Tech Debt Management Pack.

## A) Scope + assumptions
- [ ] System(s) in scope are explicitly named; out-of-scope areas are listed.
- [ ] The decision(s) this pack supports are explicit.
- [ ] Time horizon and key constraints are captured (capacity, compliance, freeze windows, SLOs).
- [ ] Assumptions are clearly labeled (no hidden guesses).

## B) Debt register quality
- [ ] Each debt item has: symptoms, impact statement, owner, and effort **range**.
- [ ] User-visible symptoms are represented (not purely internal concerns).
- [ ] Dependencies and sequencing constraints are captured where relevant.
- [ ] Items are worded as problems/outcomes, not vague labels (“cleanup”).

## C) Prioritization quality
- [ ] Scoring model is simple, explained, and applied consistently.
- [ ] The top priorities are justified with evidence/signals or explicit hypotheses.
- [ ] “Enabler” work is identified (work that unlocks multiple downstream improvements).

## D) Rebuild/migration safety (if applicable)
- [ ] The plan acknowledges migration uncertainty and uses ranges/buffers.
- [ ] Dual-run (supporting old + new) cost and staffing/on-call impact are called out.
- [ ] Cutover plan exists (how traffic/data moves; failure handling).
- [ ] Decommission plan exists (what is turned off; when; definition of done).
- [ ] Rollback plan exists with triggers.

## E) Execution plan quality
- [ ] Milestones are incremental and independently valuable.
- [ ] Each milestone has acceptance criteria and a stop/rollback condition.
- [ ] Capacity allocation is explicit (e.g., % per sprint) and realistic.

## F) Metrics + funding
- [ ] Baselines and targets are provided (or a plan to measure them).
- [ ] At least 1 leading indicator and 1 guardrail metric are defined.
- [ ] Instrumentation gaps are listed with owners.
- [ ] Hard-to-measure benefits have a proxy metric and/or a small test plan.

## G) Stakeholder alignment
- [ ] Stakeholder cadence and decision gates are defined.
- [ ] The first milestone can start immediately (clear next step + owner).
- [ ] Risks, open questions, and next steps are included at the end.

## H) Safety
- [ ] No secrets/credentials were requested or recorded.
- [ ] No destructive code changes are proposed without an explicit confirmation step.

