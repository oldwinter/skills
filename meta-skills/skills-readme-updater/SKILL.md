---
name: skills-readme-updater
description: Audit this repository's two-layer skill tree against the handwritten README. Use after adding or moving skills, or when asked to refresh the skills directory map. Prints drift; does not write README.md.
---

# Skills README Updater

Audit the **repository** skill tree. Do not scan `~/.claude/skills/` and do not overwrite `README.md`.

The public catalog is the handwritten two-layer map in `README.md`: root standalone skills plus `*-skills/` buckets (`base`, `devops`, `lenny` and its sub-buckets, `meta`, `obsidian`, `tools`). This skill reports what the tree has that the README does not, the reverse, and root-vs-bucket name collisions.

## Usage

From the repository root:

```bash
python3 meta-skills/skills-readme-updater/scripts/update_readme.py
```

Or point at a checkout:

```bash
python3 meta-skills/skills-readme-updater/scripts/update_readme.py --repo .
```

The script will:

1. Scan root directories that contain `SKILL.md`
2. Scan `base-skills/`, `devops-skills/`, `lenny-skills/` (including sub-buckets), `meta-skills/`, `obsidian-skills/`, and `tools-skills/`
3. Print those lists, name collisions, and README drift
4. Leave `README.md` unchanged

## Workflow: after adding a skill

1. Add the skill directory (root or a category bucket)
2. Update the handwritten `README.md` map if the skill should be listed
3. Run the auditor and confirm the new name appears under the right bucket
4. Do not run a generator that writes `README.md`

## Tests

```bash
bash meta-skills/skills-readme-updater/scripts/test_update_readme.sh
```
