# Checklists (Quality Gate)

Use these before finalizing the Design Engineering Execution Pack.

## A) Scope + assumptions
- [ ] The “design engineering” definition for this context is explicit (role/function/project).
- [ ] In-scope vs out-of-scope responsibilities are listed (no hidden work).
- [ ] Stakeholders and decision-maker(s) are explicit.
- [ ] Assumptions are clearly labeled (stack, team, timeline, a11y/perf).

## B) Operating model + boundaries
- [ ] Engagement model is selected (embedded/platform/tiger team) and justified.
- [ ] Ownership boundaries are unambiguous for: tokens, components, visual QA, accessibility, performance.
- [ ] Handoff and review gates are documented (who reviews what, when).

## C) Prototype → production workflow
- [ ] A prototype ladder exists and each rung has a purpose and “graduation” rule.
- [ ] Each artifact is labeled **throwaway** vs **shippable**.
- [ ] Review gates exist for shippable work (design + engineering + QA/a11y).

## D) Design-to-code contract
- [ ] Component/flow spec requires states (loading/empty/error/disabled/focus/hover).
- [ ] Token usage is defined (avoid one-off pixels/colors).
- [ ] PR expectations are explicit (screenshots, test plan, a11y notes).

## E) Delivery plan quality
- [ ] Backlog is prioritized by user impact + reuse, not convenience.
- [ ] Milestones are incremental and pattern-setting (first milestone ships within 1–2 weeks).
- [ ] Each milestone has acceptance criteria and a rollback/stop condition.

## F) Quality bar + sustainability
- [ ] Accessibility requirements are stated and testable (at least a component-level checklist).
- [ ] Consistency mechanism exists (docs, Storybook, linting, review gates).
- [ ] Success signals/KPIs are defined (even if directional).

## G) Finalization
- [ ] Risks, open questions, and next steps are included at the end.
- [ ] No secrets/credentials were requested or recorded.

