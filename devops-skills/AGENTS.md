# devops-skills

## OVERVIEW
Canonical DevOps / infrastructure skills for this repository.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI runbooks | `devops-skills/*/SKILL.md` | Usually contains commands and guardrails.
| Extended docs | `devops-skills/*/references/` | Troubleshooting and examples.

## CONVENTIONS
- Skill entrypoint is `SKILL.md`.
- Many skills are “CLI wrapper” style (kubectl, AWS, ArgoCD, etc.).

## ANTI-PATTERNS
- Don’t copy/paste production-impacting commands without checking the skill’s DO/DO NOT guidance (some skills contain explicit “never run X automatically”).
