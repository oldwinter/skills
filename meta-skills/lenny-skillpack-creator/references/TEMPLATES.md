# TEMPLATES (copy/paste)

Use these templates when generating a new skill pack.

## SKILL.md skeleton (minimal)

```md
---
name: <skill-slug>
description: <one sentence + trigger phrases + expected outputs>
---

# <Skill Title>

## Scope
**When to use**
- ...
**When NOT to use**
- ...

## Inputs
**Minimum required**
- ...
**Missing-info strategy**
- Ask up to 3–5 questions from `references/INTAKE.md`, then proceed with explicit assumptions.

## Outputs
Deliver (in order):
1) ...
2) ...
3) ...
Always include: Risks / Open questions / Next steps

## Workflow (5–9 steps)
1) ...
2) ...

## Quality gate (required)
- Run `references/CHECKLISTS.md` and score with `references/RUBRIC.md`.

## Examples
- 2 positive prompts
- 1 boundary prompt
```

## README.md skeleton

```md
# <skill-slug>

## What this skill produces
- ...

## How to use (prompt)
“Use `<skill-slug>`. Context: ... Constraints: ... Output: ...”

## Lint
`python3 skills/lenny-skillpack-creator/scripts/lint_skillpack.py skills/<skill-slug>`
```

## references/SOURCE_SUMMARY.md skeleton

```md
# SOURCE_SUMMARY

## Source
- Origin: Refound/Lenny
- URL / file:

## What was preserved (high-signal rules)
- DO:
- DO NOT:

## What was added (manufactured for executability)
- Output contract:
- Workflow:
- Quality gates:
```

