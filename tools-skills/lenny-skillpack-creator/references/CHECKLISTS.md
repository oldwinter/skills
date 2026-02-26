# CHECKLISTS (quality gate)

Use this before finalizing any generated skill pack.

## Structural checks (must pass)
- `SKILL.md` exists and has YAML frontmatter with `name` + `description`.
- Frontmatter `name` matches the folder name (slug).
- `references/` contains:
  - [INTAKE.md](INTAKE.md)
  - [WORKFLOW.md](WORKFLOW.md)
  - [TEMPLATES.md](TEMPLATES.md)
  - [CHECKLISTS.md](CHECKLISTS.md)
  - [RUBRIC.md](RUBRIC.md)
  - [SOURCE_SUMMARY.md](SOURCE_SUMMARY.md)

## Execution contract checks
- Scope includes **When to use** and **When NOT to use** with clear boundaries and adjacent-skill pointers.
- Inputs list minimum required + missing-info strategy (3–5 questions per round, otherwise explicit assumptions).
- Outputs are explicit deliverables (files or structured sections) with a fixed order.
- Workflow has 5–9 steps, each step has: Inputs → Actions → Outputs → Checks.

## Testability checks
- At least 2 positive examples and 1 boundary example exist in SKILL.md or `references/EXAMPLES.md`.
- “Checks” are objective enough that a reviewer can say pass/fail.

## Safety checks
- No requests for secrets/credentials.
- High-risk actions require explicit confirmation and include rollback guidance.

## Completeness checks (always included)
- Risks
- Open questions
- Next steps

