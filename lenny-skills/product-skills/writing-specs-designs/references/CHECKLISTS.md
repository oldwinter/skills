# Checklists (Quality Gates)

Use these before finalizing the Spec & Design Doc Pack.

## Checklist 1 — Scope + decision clarity
- Problem and **why now** are stated in 1–2 sentences.
- Goals, non-goals, and out-of-scope items are explicit.
- Constraints and dependencies are listed (and realistic).
- Success metrics (1–3) and guardrails (2–5) are defined and measurable.
- Assumptions are labeled and easy to audit.

## Checklist 2 — Diagram quality (“moving pieces”)
- Diagram has **≤10 moving pieces** and is understandable without narration.
- It includes the key states/components and how they connect (hand-offs, data, decisions).
- It avoids pixel-level UI while still making feasibility and responsibilities clear.
- A reviewer can say “I know what to build” after reading the diagram + annotations.

## Checklist 3 — Flows + states completeness
- Happy path has clear entry and exit (the “value moment”).
- Top edge cases are covered (permissions, empty/loading/error, interruptions).
- Each critical screen/component has a state table (or equivalent) with intended outcomes.
- Ambiguous copy/labels are written down (or explicitly delegated to design).

## Checklist 4 — Prototype brief (only when needed)
- The prototype answers a specific decision (not “prototype for prototype’s sake”).
- Fidelity is appropriate (lo-fi/hi-fi/in-code) and timeboxed.
- Prototype uses realistic data/examples (no misleading empty states).
- Success criteria are concrete (time, comprehension, error rate, preference signal).
- If using code, it is explicitly **throwaway by default** unless promoted intentionally.

## Checklist 5 — Mobile tap economy (when mobile is in scope)
- A tap budget target is defined for the critical path to value.
- Tap count from entry → value is documented and optimized.
- The spec includes ideas for reducing taps and minimizing attention loss.

## Checklist 6 — Testability + handoff
- Requirements are falsifiable and include acceptance criteria.
- Non-functional requirements are captured (accessibility, performance, privacy).
- Measurement plan maps metrics → events/data → owner.
- Risks, open questions, and next steps are included with owners when possible.

