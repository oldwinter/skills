# Skills repository task runner
#
# Common usage:
#   just help
#   just test-sync
#   just audit-readme
#   just validate-skill obsidian-skills/obsidian-bases
#
# This justfile focuses on the real workflows in this repository:
# - validate one skill or skill pack
# - run sync-manager unit tests
# - audit the handwritten README skill map
# - sync repo categories <-> runtime agent installs
#
# Obsidian sidecar import/export is still a plan
# (docs/plans/2026-03-08-obsidian-skill-state-sync.md). Recipes below fail closed.

obsidian_plan := "docs/plans/2026-03-08-obsidian-skill-state-sync.md"

default: help

help:
    @echo "Skills repository task runner"
    @echo ""
    @echo "Validation"
    @echo "  just test-sync                  Run sync-manager unit tests"
    @echo "  just audit-readme               Audit repo skill tree vs handwritten README"
    @echo "  just validate-skill <dir>       Quick-validate one skill directory (requires PyYAML)"
    @echo "  just validate-skillpack <dir>   Strict validate one skill pack (requires PyYAML)"
    @echo ""
    @echo "Runtime sync"
    @echo "  just sync-status                Show repo/runtime sync status"
    @echo "  just sync-diff                  Show repo/runtime sync diff"
    @echo "  just sync-pull                  Pull runtime changes into the repo"
    @echo "  just sync-push                  Push repo changes to runtime installs"
    @echo "  just sync-link-all              Rebuild other agent skill dirs as symlinks"
    @echo "  just sync-3way-status           Show incremental three-way sync status"
    @echo "  just sync-3way                  Run incremental three-way sync"
    @echo ""
    @echo "Repository helpers"
    @echo "  just plans                      List implementation plans in docs/plans"

test-sync:
    python3 -m unittest meta-skills/sync-skills-manager/scripts/test_agent_skills_audit.py meta-skills/sync-skills-manager/scripts/test_flatten_system_skills_layout.py meta-skills/sync-skills-manager/scripts/test_reclassify_system_skills.py meta-skills/sync-skills-manager/scripts/test_skills_profiles.py meta-skills/sync-skills-manager/scripts/test_justfile.py meta-skills/skills-readme-updater/scripts/test_update_readme.py -v

audit-readme:
    python3 meta-skills/skills-readme-updater/scripts/update_readme.py

obsidian-unavailable:
    @echo "error  Obsidian sidecar scripts are not in this repo yet"
    @echo "try: {{obsidian_plan}}"
    @exit 2

obsidian-import: obsidian-unavailable
obsidian-export: obsidian-unavailable
obsidian-export-dry: obsidian-unavailable
obsidian-sync: obsidian-unavailable
obsidian-state: obsidian-unavailable

validate-skill skill_dir:
    python3 -c 'import importlib.util, sys; sys.exit(0 if importlib.util.find_spec("yaml") else 1)' || { echo "PyYAML is required for validate-skill. Install it with: python3 -m pip install pyyaml"; exit 1; }
    python3 meta-skills/skill-creator/scripts/quick_validate.py {{skill_dir}}

validate-skillpack skill_dir:
    python3 -c 'import importlib.util, sys; sys.exit(0 if importlib.util.find_spec("yaml") else 1)' || { echo "PyYAML is required for validate-skillpack. Install it with: python3 -m pip install pyyaml"; exit 1; }
    python3 meta-skills/lenny-skillpack-creator/scripts/lint_skillpack.py {{skill_dir}}

sync-status:
    bash meta-skills/sync-skills-manager/sync-skills.sh status

sync-diff:
    bash meta-skills/sync-skills-manager/sync-skills.sh diff

sync-pull:
    bash meta-skills/sync-skills-manager/sync-skills.sh pull

sync-push:
    bash meta-skills/sync-skills-manager/sync-skills.sh push

sync-link-all:
    bash meta-skills/sync-skills-manager/sync-skills.sh link-all

sync-3way-status:
    bash meta-skills/sync-skills-manager/sync-skills-3way.sh status

sync-3way:
    bash meta-skills/sync-skills-manager/sync-skills-3way.sh sync

plans:
    find docs/plans -maxdepth 1 -type f | sort
