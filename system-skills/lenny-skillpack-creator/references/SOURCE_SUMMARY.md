# SOURCE_SUMMARY

This is a meta-skill. Its “source” is the factory intent of this repository:
convert Refound/Lenny skills (insight-heavy) into **agent-executable skill packs**.

## Core rules preserved

- Convert insights into **rules + checks + artifacts** (not prose).
- Keep `SKILL.md` short; put long content in `references/`.
- Always include:
  - When to use / when NOT to use
  - Input contract + missing-info strategy
  - Output contract (explicit deliverables)
  - 5–9 step workflow (Inputs/Actions/Outputs/Checks)
  - Quality gate (checklists + rubric)
  - Examples (good + boundary)
- Safety: least privilege, no secrets, explicit confirmation for irreversible actions.

## What this meta-skill adds

- A consistent folder/file structure (enforced by `lint_skillpack.py`)
- A repeatable conversion workflow (`references/WORKFLOW.md`)
- Reusable templates and scoring (`references/TEMPLATES.md`, `references/RUBRIC.md`)

