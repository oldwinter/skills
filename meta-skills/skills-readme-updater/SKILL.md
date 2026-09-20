---
name: skills-readme-updater
description: Audit this repo's handwritten README against root SKILL.md directories. Default is check-only; --write is rejected so it cannot overwrite the two-layer map with a ~/.claude five-bucket dump. Triggers on "update skills readme", "audit-readme", or after adding a root skill.
---

# Skills README Updater

Automatically scan and update the skills README.md when skills are added, modified, or removed.

## Usage

After adding a root-level skill, audit the handwritten map:

```bash
just audit-readme
python3 meta-skills/skills-readme-updater/scripts/update_readme.py
```

The script will:
1. Scan this repository (not `~/.claude/skills/`)
2. Require each root directory with `SKILL.md` to appear in `README.md`
3. Exit 1 with `try: just audit-readme` if names are missing
4. Refuse `--write` so it cannot replace the two-layer README

## Categories

Skills are organized into these categories:

| Category | Skills |
|----------|--------|
| 云基础设施 | aws-cli, aws-cost-explorer, eksctl |
| Kubernetes & GitOps | kubectl, argocd-cli, kargo-cli, sync-to-prod |
| 代码仓库 | github-cli, gitlab-cli, changelog-generator |
| 开发工具 | justfile, skill-creator, skills-readme-updater |
| 内容处理 | humanizer-zh, obsidian-dashboard |

To add a new category or reassign skills, edit the `CATEGORIES` dict in `scripts/update_readme.py`.

## Workflow: Adding a New Skill

1. Create the skill using `skill-creator`
2. Edit `SKILL.md` with proper metadata
3. Run the README updater:
   ```bash
   python3 ~/.claude/skills/skills-readme-updater/scripts/update_readme.py
   ```
4. Verify the README was updated correctly
