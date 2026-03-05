# Transformation Rules: Refound/Lenny Skill → Agent-Executable Skill Pack

Use this as a procedural playbook.

## A) Decompose the source into 3 layers
1) **Insights**: what to do / why it matters
2) **Actions**: how to do it, step-by-step
3) **Artifacts**: what you leave behind (docs, checklists, tables, scripts)

If the source is mostly “insights”, your job is to manufacture the missing layers.

## B) Convert insights into “rules + checks”
For each insight:
- Rewrite as a rule: “DO / DO NOT”
- Add a check: “How will we know it’s done well?”
- Add a deliverable: “What artifact captures this?”

Example:
- Insight: “Start with the why and why now.”
- Rule: “Every doc must include a Why/Why now section.”
- Check: “Can a stakeholder restate the urgency in one sentence?”
- Artifact: “PRD section + 1–2 evidence bullets.”

## C) Write a tight scope
In SKILL.md:
- Add “When to use” triggers (artifact names + synonyms)
- Add “When NOT to use” boundaries (adjacent skills / upstream tasks)

## D) Define the contracts
Input contract:
- minimum inputs
- missing-info strategy (ask max 3–5 questions)
Output contract:
- explicit deliverables (files or structured sections)
- ordering + naming

## E) Build the workflow (5–9 steps)
Each step must specify:
- Inputs
- Actions
- Outputs
- Checks

Avoid vague steps like “think deeply”. Replace with concrete actions.

## F) Create the reference kit
Minimum recommended files:
- Intake question bank (copy/paste)
- One template per deliverable
- Quality checklist + scoring rubric
- Examples (2 good, 1 bad/boundary)
- Source notes (what you preserved from Lenny)

## G) Keep SKILL.md short
Anything long goes into references/.
SKILL.md should point to those files.

## H) Add safety + robustness
- least privilege
- no secrets
- human checkpoints
- rollback guidance if writing files
