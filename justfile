set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

PROFILES := "python3 system-skills/sync-skills-manager/scripts/skills_profiles.py"
AGENT_AUDIT := "python3 system-skills/sync-skills-manager/scripts/agent_skills_audit.py"
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

ps-normalize-apply agent="" backup_root="~/.claude/skills-backups":
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

ps-refresh-apply agent="" backup_root="~/.claude/skills-backups":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" refresh --agent "{{agent}}" --apply --backup-root "{{backup_root}}"; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" refresh --apply --backup-root "{{backup_root}}"; \
  fi

ps-stars stars="7" mode="only" agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" stars --agent "{{agent}}" --mode "{{mode}}" --stars "{{stars}}" --dry-run; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" stars --mode "{{mode}}" --stars "{{stars}}" --dry-run; \
  fi

ps-stars-apply stars="7" mode="only" agent="":
  @if [[ -n "{{agent}}" ]]; then \
    {{PROFILES}} --config "{{CONFIG}}" stars --agent "{{agent}}" --mode "{{mode}}" --stars "{{stars}}" --apply; \
  else \
    {{PROFILES}} --config "{{CONFIG}}" stars --mode "{{mode}}" --stars "{{stars}}" --apply; \
  fi

ps-edit:
  @${EDITOR:-vi} "{{CONFIG}}"

ps-help:
  @{{PROFILES}} --help

agent-scan agents="":
  @if [[ -n "{{agents}}" ]]; then \
    {{AGENT_AUDIT}} scan --agent "{{agents}}"; \
  else \
    {{AGENT_AUDIT}} scan; \
  fi

agent-scan-installed agents="":
  @if [[ -n "{{agents}}" ]]; then \
    {{AGENT_AUDIT}} scan --installed-only --agent "{{agents}}"; \
  else \
    {{AGENT_AUDIT}} scan --installed-only; \
  fi

agent-skills agents="" installed_only="true":
  @if [[ -n "{{agents}}" ]]; then \
    if [[ "{{installed_only}}" == "true" ]]; then {{AGENT_AUDIT}} skills --installed-only --agent "{{agents}}"; else {{AGENT_AUDIT}} skills --agent "{{agents}}"; fi; \
  else \
    if [[ "{{installed_only}}" == "true" ]]; then {{AGENT_AUDIT}} skills --installed-only; else {{AGENT_AUDIT}} skills; fi; \
  fi

agent-diff left="codex" right="cursor":
  @{{AGENT_AUDIT}} diff --left "{{left}}" --right "{{right}}"

agent-sync-check canonical="claude-code" agents="" installed_only="true":
  @if [[ -n "{{agents}}" ]]; then \
    if [[ "{{installed_only}}" == "true" ]]; then {{AGENT_AUDIT}} sync-check --canonical-agent "{{canonical}}" --installed-only --agent "{{agents}}"; else {{AGENT_AUDIT}} sync-check --canonical-agent "{{canonical}}" --agent "{{agents}}"; fi; \
  else \
    if [[ "{{installed_only}}" == "true" ]]; then {{AGENT_AUDIT}} sync-check --canonical-agent "{{canonical}}" --installed-only; else {{AGENT_AUDIT}} sync-check --canonical-agent "{{canonical}}"; fi; \
  fi

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
