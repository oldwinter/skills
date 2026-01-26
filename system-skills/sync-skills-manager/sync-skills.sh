#!/bin/bash
# Sync Skills Manager - Sync between system and repository skills

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_SKILLS_DIR="$HOME/.agents/skills"
REPO_SKILLS_DIR="${SCRIPT_DIR}/../system-skills"
COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RED='\033[0;31m'

log_info() { echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $1"; }
log_warn() { echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1"; }
log_error() { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"; }

show_help() {
  cat << EOF
Sync Skills Manager - Sync between system and repository skills

Usage: $0 <command>

Commands:
  diff    Preview changes (system skills not in repo)
  pull    Sync system → repository (add new skills)
  push    Sync repository → system (install all)
  status  Show current sync status
  help    Show this help message

Examples:
  $0 diff      # Preview what would be synced
  $0 pull      # Add new skills from system to repo
  $0 push      # Install all repo skills to system
  $0 status    # Show sync status

EOF
}

get_skill_count() {
  local dir="$1"
  ls -1d "$dir"/*/ 2>/dev/null | wc -l | tr -d ' '
}

get_file_count() {
  local dir="$1"
  find "$dir" -type f ! -name '*.md' 2>/dev/null | wc -l | tr -d ' '
}

cmd_diff() {
  log_info "Previewing sync changes..."

  local system_count=$(get_skill_count "$SYSTEM_SKILLS_DIR")
  local repo_count=$(get_skill_count "$REPO_SKILLS_DIR")

  echo ""
  echo "System skills:  $system_count"
  echo "Repo skills:    $repo_count"
  echo ""

  echo "Skills in system but NOT in repo:"
  echo "----------------------------------------"

  local found=0
  for skill_dir in "$SYSTEM_SKILLS_DIR"/*/; do
    local skill_name=$(basename "$skill_dir")
    if [ ! -d "$REPO_SKILLS_DIR/$skill_name" ]; then
      echo "  + $skill_name"
      found=1
    fi
  done

  if [ $found -eq 0 ]; then
    echo "  (no new skills)"
  fi

  echo ""
  echo "Skills in repo but NOT in system:"
  echo "----------------------------------------"

  found=0
  for skill_dir in "$REPO_SKILLS_DIR"/*/; do
    local skill_name=$(basename "$skill_dir")
    if [ "$skill_name" != "sync-skills-manager" ] && [ ! -d "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
      echo "  - $skill_name"
      found=1
    fi
  done

  if [ $found -eq 0 ]; then
    echo "  (all repo skills exist in system)"
  fi
}

cmd_pull() {
  log_info "Syncing skills from system to repository..."

  local pulled=0

  for skill_dir in "$SYSTEM_SKILLS_DIR"/*/; do
    local skill_name=$(basename "$skill_dir")

    # Skip sync-skills-manager itself
    if [ "$skill_name" == "sync-skills-manager" ]; then
      continue
    fi

    # Skip if skill already exists in repo
    if [ -d "$REPO_SKILLS_DIR/$skill_name" ]; then
      continue
    fi

    log_info "Adding: $skill_name"
    cp -r "$skill_dir" "$REPO_SKILLS_DIR/"
    pulled=$((pulled + 1))
  done

  if [ $pulled -eq 0 ]; then
    log_info "No new skills to sync (all skills already exist in repo)"
  else
    log_info "Synced $pulled new skill(s) to repository"
    log_info "Run 'git add -A && git commit' to save changes"
  fi
}

cmd_push() {
  log_info "Installing all repository skills to system..."

  cd "$SCRIPT_DIR"

  # Use npx add-skill to install
  npx add-skill .. --all --global

  log_info "All skills installed to system"
}

cmd_status() {
  echo "Sync Status"
  echo "=============================================="
  echo ""

  local system_count=$(get_skill_count "$SYSTEM_SKILLS_DIR")
  local repo_count=$(get_skill_count "$REPO_SKILLS_DIR")

  echo "System skills:  $system_count"
  echo "Repo skills:    $repo_count"
  echo ""

  local missing=0
  echo "Skills missing in system:"
  for skill_dir in "$REPO_SKILLS_DIR"/*/; do
    local skill_name=$(basename "$skill_dir")
    if [ "$skill_name" != "sync-skills-manager" ] && [ ! -d "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
      echo "  [ ] $skill_name"
      missing=$((missing + 1))
    fi
  done

  if [ $missing -eq 0 ]; then
    echo "  (all skills synced)"
  fi

  local new_in_system=0
  echo ""
  echo "New skills in system (not in repo):"
  for skill_dir in "$SYSTEM_SKILLS_DIR"/*/; do
    local skill_name=$(basename "$skill_name")
    if [ ! -d "$REPO_SKILLS_DIR/$skill_name" ]; then
      echo "  [+] $skill_name"
      new_in_system=$((new_in_system + 1))
    fi
  done

  if [ $new_in_system -eq 0 ]; then
    echo "  (no new skills)"
  fi
}

# Main
case "${1:-help}" in
  diff)
    cmd_diff
    ;;
  pull)
    cmd_pull
    ;;
  push)
    cmd_push
    ;;
  status)
    cmd_status
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    log_error "Unknown command: $1"
    show_help
    exit 1
    ;;
esac
