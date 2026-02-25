set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

PROFILES := "python3 system-skills/sync-skills-manager/scripts/skills_profiles.py"
CONFIG := "system-skills/sync-skills-manager/skills-profiles.json"
SYNC3 := "./sync-skills-3way.sh"
SYNC_MGR := "./system-skills/sync-skills-manager/sync-skills.sh"

default:
  @just --list

# -----------------------------
# Profiles manager (recommended)
# -----------------------------

ps-status agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" status --agent "{{agent}}"; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" status; \
  fi

ps-diff agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" diff --agent "{{agent}}"; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" diff; \
  fi

ps-sync:
  @{{PROFILES}} sync

ps-normalize agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" normalize --agent "{{agent}}" --dry-run; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" normalize --dry-run; \
  fi

ps-normalize-apply agent="" backup_root="~/.agents/skills-backups":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" normalize --agent "{{agent}}" --apply --backup-root "{{backup_root}}"; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" normalize --apply --backup-root "{{backup_root}}"; \
  fi

ps-apply agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" apply --agent "{{agent}}" --dry-run; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" apply --dry-run; \
  fi

ps-apply-apply agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" apply --agent "{{agent}}" --apply; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" apply --apply; \
  fi

ps-refresh agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" refresh --agent "{{agent}}" --dry-run; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" refresh --dry-run; \
  fi

ps-refresh-apply agent="" backup_root="~/.agents/skills-backups":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" refresh --agent "{{agent}}" --apply --backup-root "{{backup_root}}"; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" refresh --apply --backup-root "{{backup_root}}"; \
  fi

ps-edit:
  @${EDITOR:-vi} "{{CONFIG}}"

ps-help:
  @{{PROFILES}} --help

# -----------------------------
# Sync helpers
# -----------------------------

sync3:
  @{{SYNC3}} sync

sync3-status:
  @{{SYNC3}} status

sync-mgr-diff:
  @{{SYNC_MGR}} diff

sync-mgr-pull:
  @{{SYNC_MGR}} pull

sync-mgr-push:
  @{{SYNC_MGR}} push

# -----------------------------
# Repo checks
# -----------------------------

test:
  @python3 -m unittest -q

