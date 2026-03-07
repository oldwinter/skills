# Skills repository task runner
#
# Common usage:
#   just help
#   just test-sync
#   OBSIDIAN_VAULT=/path/to/vault just obsidian-sync
#   just validate-skill obsidian-skills/obsidian-bases
#
# This justfile focuses on the real workflows in this repository:
# - validate one skill or skill pack
# - run sync-manager unit tests
# - sync repo skills <-> Obsidian
# - sync repo categories <-> runtime agent installs

vault_root := env_var_or_default("OBSIDIAN_VAULT", "/Users/oldwinter/oldwinter-notes")
repo_root := "."
state_file := "meta-skills/sync-skills-manager/data/obsidian-skill-state.yaml"

default: help

help:
    @echo "Skills repository task runner"
    @echo ""
    @echo "Environment"
    @echo "  OBSIDIAN_VAULT={{vault_root}}"
    @echo ""
    @echo "Validation"
    @echo "  just test-sync                  Run sync-manager unit tests"
    @echo "  just validate-skill <dir>       Quick-validate one skill directory (requires PyYAML)"
    @echo "  just validate-skillpack <dir>   Strict validate one skill pack (requires PyYAML)"
    @echo ""
    @echo "Obsidian"
    @echo "  just obsidian-import            Import personal state from Obsidian into the repo sidecar"
    @echo "  just obsidian-export            Export repo skills to Obsidian and write the Base file"
    @echo "  just obsidian-export-dry        Dry-run repo-to-Obsidian export"
    @echo "  just obsidian-sync              Import from Obsidian, then export back to Obsidian"
    @echo "  just obsidian-state             Print the current sidecar file"
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
    python3 -m unittest meta-skills/sync-skills-manager/scripts/test_agent_skills_audit.py meta-skills/sync-skills-manager/scripts/test_flatten_system_skills_layout.py meta-skills/sync-skills-manager/scripts/test_reclassify_system_skills.py meta-skills/sync-skills-manager/scripts/test_skills_profiles.py meta-skills/sync-skills-manager/scripts/test_export_skills_to_obsidian.py meta-skills/sync-skills-manager/scripts/test_obsidian_skill_state.py -v

validate-skill skill_dir:
    python3 -c 'import importlib.util, sys; sys.exit(0 if importlib.util.find_spec("yaml") else 1)' || { echo "PyYAML is required for validate-skill. Install it with: python3 -m pip install pyyaml"; exit 1; }
    python3 meta-skills/skill-creator/scripts/quick_validate.py {{skill_dir}}

validate-skillpack skill_dir:
    python3 -c 'import importlib.util, sys; sys.exit(0 if importlib.util.find_spec("yaml") else 1)' || { echo "PyYAML is required for validate-skillpack. Install it with: python3 -m pip install pyyaml"; exit 1; }
    python3 meta-skills/lenny-skillpack-creator/scripts/lint_skillpack.py {{skill_dir}}

obsidian-import:
    python3 meta-skills/sync-skills-manager/scripts/import_obsidian_skill_state.py --vault-root {{vault_root}} --repo-root {{repo_root}} --state-path {{state_file}}

obsidian-export:
    python3 meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py --vault-root {{vault_root}} --repo-root {{repo_root}} --state-path {{state_file}} --write-base

obsidian-export-dry:
    python3 meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py --vault-root {{vault_root}} --repo-root {{repo_root}} --state-path {{state_file}} --dry-run --write-base

obsidian-sync:
    python3 meta-skills/sync-skills-manager/scripts/import_obsidian_skill_state.py --vault-root {{vault_root}} --repo-root {{repo_root}} --state-path {{state_file}}
    python3 meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py --vault-root {{vault_root}} --repo-root {{repo_root}} --state-path {{state_file}} --write-base

obsidian-state:
    test -f {{state_file}} && sed -n '1,200p' {{state_file}} || echo "No sidecar file yet: {{state_file}}"

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
