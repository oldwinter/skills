# EXAMPLES

## Positive example 1 (standard conversion)

“Use `$lenny-skillpack-creator`. Source: `sources/refound/raw/<slug>/SKILL.md`. Persona: PM. Output: write an executable skill pack to `skills/<slug>/` with clear scope, input/output contracts, 7-step workflow, templates, checklists, rubric, and examples. All content must be English.”

## Positive example 2 (HTML fallback)

“Use `$lenny-skillpack-creator`. Source: `sources/refound/raw/<slug>/page.html` (no SKILL.md available). Persona: Recruiter. Output: write an executable skill pack to `skills/<slug>/` and include a `references/SOURCE_SUMMARY.md` that distinguishes what came from the source vs what was manufactured.”

## Boundary example (not enough inputs)

“Convert the entire Refound database into skills automatically; don’t ask any questions.”

Expected response:
- Ask up to 3–5 clarifying questions (persona, deliverables, constraints).
- If still missing, proceed with explicit assumptions and clearly list risks/open questions/next steps.

