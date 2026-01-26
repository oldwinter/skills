# Skill Pack Output Spec (for generated skills)

Goal: Convert an “insight/methodology” skill into an **execution contract** that an agent can follow to produce real deliverables.

## 1) Recommended folder structure (minimal)

`<skill-slug>/`
- `SKILL.md`
- `README.md`
- `references/`
  - [INTAKE.md](INTAKE.md) (or `INTAKE_QUESTIONNAIRE.md`)
  - [TEMPLATES.md](TEMPLATES.md) (or multiple template files)
  - `CHECKLIST.md` (quality checklist)
  - [RUBRIC.md](RUBRIC.md) (scoring rubric)
  - [EXAMPLES.md](EXAMPLES.md) (2 good, 1 bad/boundary)
  - `SOURCE_NOTES.md` (what was preserved from the original skill)
- `scripts/` (optional)
  - `lint_*.py` (validate required sections)
  - `init_*.py` (scaffold artifacts)
  - `package_*.py` (zip)

## 2) SKILL.md required sections

SKILL.md should be short, executable, and high-signal.

Required sections:
1) **Scope**
   - What this skill covers
   - When to use / when NOT to use
2) **Inputs**
   - Minimum required inputs
   - Missing-info strategy (ask max 3–5 questions at a time; otherwise make explicit assumptions)
3) **Outputs**
   - Explicit deliverables (files or structured sections)
   - Output order (if multiple artifacts)
4) **Workflow**
   - 5–9 steps max
   - Each step must specify: Inputs → Actions → Outputs → Checks
5) **Quality gate**
   - Run a checklist/rubric before finalizing
   - Always produce: Risks, Open questions, Next steps
6) **Examples**
   - 2 positive examples (typical use)
   - 1 negative/boundary example (when not to use / when to ask for clarification)

## 3) Progressive disclosure

- Keep SKILL.md lean.
- Move long templates and lists into `references/`.
- In SKILL.md, point to files by path, e.g., `references/PRD_TEMPLATE.md`.

## 4) Naming

- Prefer lowercase, hyphenated skill slugs.
- Keep names stable; avoid renaming skills unless necessary.

## 5) Compatibility notes

Agent Skills systems commonly load:
- frontmatter (name/description) for discovery
- SKILL.md on demand
So description must contain “trigger phrases” users will actually say.
