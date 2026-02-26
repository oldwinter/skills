# Examples (2 good, 1 boundary)

## Example 1 — Stand up design engineering (embedded)
**Prompt**
“Use `design-engineering`. Context: B2B SaaS web app. 2 designers, 8 engineers. We ship slowly because UI polish and edge states get missed. Goal: reduce rework and increase consistency. Constraints: accessibility is required; need initial impact in 4 weeks. Output: a Design Engineering Execution Pack with an embedded model.”

**What “good” looks like**
- Clear boundaries: Design owns interaction/visual direction; Design Eng owns component implementation + a11y checklist + visual QA sign-off.
- Prototype ladder labels which artifacts are throwaway vs shippable.
- A 4-week milestone plan starting with 2 “golden path” components and a PR checklist.

## Example 2 — Build a component library (platform model)
**Prompt**
“Use `design-engineering`. We want to create a design system and component library for our React app. Current state: lots of one-off CSS and inconsistent patterns. Output: charter + design-to-code contract + prioritized component backlog + milestones for 6 weeks.”

**What “good” looks like**
- Backlog prioritizes high-reuse primitives first (buttons/inputs/tables) with acceptance criteria.
- Contract mandates tokens and states (hover/focus/disabled/loading/error).
- Lightweight gates (Storybook preview + PR screenshot checklist).

## Boundary example — Pure definition request
**Prompt**
“Explain what design engineering is.”

**Recommended response**
- Give a 2–3 sentence definition.
- Ask whether they want to apply it (team, product, goal). If yes, proceed with up to 5 intake questions from [INTAKE.md](INTAKE.md).

