# WORKFLOW (detailed)

This is the detailed procedure behind the `lenny-skillpack-creator` meta-skill.

## 1) Ingest the source

- Prefer `sources/refound/raw/<slug>/SKILL.md` if available.
- If only HTML exists (`page.html`), extract the core ideas and normalize into:
  - **Insights** (what/why)
  - **Actions** (how)
  - **Artifacts** (what to deliver)

## 2) Define the execution contract

- Draft **Scope**: when to use / when NOT to use (name adjacent skills explicitly).
- Draft **Inputs**: minimum required + missing-info strategy.
- Draft **Outputs**: explicit deliverables (files/sections), in a fixed order.

## 3) Build the 5–9 step workflow

For each step, write:
- Inputs → Actions → Outputs → Checks

Avoid “think/consider” language. Convert to concrete actions and artifact updates.

## 4) Create the reference kit

Minimum required reference files (required by linter):
- `references/INTAKE.md` (question bank)
- `references/WORKFLOW.md` (expanded flow + branches)
- `references/TEMPLATES.md` (copy/paste templates)
- `references/CHECKLISTS.md` (DoD checklist)
- `references/RUBRIC.md` (scoring)
- `references/SOURCE_SUMMARY.md` (what was preserved + rules distilled)

Recommended additions:
- `references/EXAMPLES.md` (2 good + 1 boundary prompt)
- `scripts/` (optional validators/scaffolds)

## 5) Apply safety rules

Use [SECURITY_GUIDE.md](SECURITY_GUIDE.md):
- No secrets/credentials.
- Least privilege by default.
- Require explicit confirmation for irreversible actions.

## 6) Run lint + fix until passing

- `python3 skills/lenny-skillpack-creator/scripts/lint_skillpack.py <skill-dir>`

If lint fails:
- Fix structure/missing files/frontmatter.
- Re-run lint until it passes.

## 7) Smoke test (artifact realism)

Run 1–2 realistic prompts. Verify:
- Outputs match the output contract (not generic advice).
- Workflow produces concrete artifacts in the promised order.
- Quality gate produces risks/open questions/next steps.

