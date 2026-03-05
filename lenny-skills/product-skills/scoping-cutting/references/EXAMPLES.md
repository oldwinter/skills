# Examples (Scoping & Cutting)

These are illustrative prompts and what “good” output looks like (artifact-driven, not generic advice).

## Example 1 — B2B SaaS (4-week appetite)
**Prompt:** “We’re building bulk CSV import for admins. We have 4 weeks. Cut scope so we can ship something useful; include a Wizard-of-Oz validation plan for risky parts.”

**What good output includes**
- A 4-week appetite and explicit non-negotiables (privacy, reliability, support load)
- An MLS that covers an end-to-end happy path (upload → mapping → import → confirmation/errors)
- A cut list that defers rare edge cases (complex encodings, multi-file batching) with revisit triggers
- A WoZ plan to validate mapping defaults and error messaging (e.g., manual review of mapping suggestions) before building automation

## Example 2 — Consumer (2-week appetite)
**Prompt:** “Define a minimum lovable first version of ‘saved searches’ on mobile within 2 weeks. Prevent scope creep from ‘power user’ requests.”

**What good output includes**
- A coherent MLS (save → manage list → run saved search) with clear UX states and 1–2 trust/lovability choices (defaults, confirmations)
- Explicit non-goals (sharing, complex filters, cross-device sync if it won’t fit)
- A scope-change policy: trade-offs and who decides

## Boundary example — Not a scoping problem
**Prompt:** “Pick our entire 2026 roadmap across 20 ideas and decide where to invest.”

**How the skill should respond**
- Push back: this is prioritization, not cutting within an appetite
- Recommend `prioritizing-roadmap`, then apply `scoping-cutting` to the top initiative(s)

