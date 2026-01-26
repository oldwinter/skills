#!/bin/bash
# Sync Skills Manager - Sync between system and repository skills
# Supports categorized subdirectories

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_SKILLS_DIR="$HOME/.agents/skills"
REPO_SKILLS_DIR="${SCRIPT_DIR}/../../system-skills"
COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RED='\033[0;31m'
COLOR_CYAN='\033[0;36m'

log_info() { echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $1"; }
log_warn() { echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1"; }
log_error() { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"; }
log_diff() { echo -e "${COLOR_CYAN}[DIFF]${COLOR_RESET} $1"; }

show_help() {
  cat << EOF
Sync Skills Manager - Sync between system and repository skills

Usage: $0 <command> [options]

Commands:
  diff    Preview changes (system skills not in repo)
  pull    Sync system → repository (add new skills only)
  push    Sync repository → system (install all)
  status  Show current sync status
  auto    Auto-categorize and sync new skills
  help    Show this help message

Options:
  --skip-cp-errors  Skip broken symlink errors during copy

Examples:
  $0 diff          # Preview what would be synced
  $0 pull          # Add new skills from system to repo
  $0 auto          # Auto-categorize and sync new skills
  $0 push          # Install all repo skills to system
  $0 status        # Show sync status

EOF
}

# Get all skill names in repo (recursively, excluding sync-skills-manager and category dirs)
get_repo_skill_names() {
  find "$REPO_SKILLS_DIR" -mindepth 1 -maxdepth 2 -type d \
    ! -name "sync-skills-manager" \
    ! -name "system-skills" \
    ! -name "ai-skills" \
    ! -name "product-skills" \
    ! -name "leadership-skills" \
    ! -name "career-skills" \
    ! -name "communication-skills" \
    ! -name "marketing-skills" \
    ! -name "sales-skills" \
    ! -name "engineering-skills" \
    ! -name "devops-skills" \
    ! -name "tools-skills" \
    ! -name "obsidian-skills" \
    -exec basename {} \; 2>/dev/null | sort -u
}

# Find which category directory contains a skill
find_skill_category() {
  local skill_name="$1"
  for cat_dir in "$REPO_SKILLS_DIR"/*/; do
    local cat_name=$(basename "$cat_dir")
    if [ "$cat_name" == "sync-skills-manager" ]; then
      continue
    fi
    if [ -d "$cat_dir/$skill_name" ]; then
      echo "$cat_dir"
      return 0
    fi
  done
  return 1
}

# Get all categories (subdirectories)
get_categories() {
  ls -d "$REPO_SKILLS_DIR"/*/ 2>/dev/null | grep -v "sync-skills-manager" | xargs -I {} basename {}
}

# Auto-determine category for a skill
auto_categorize() {
  local skill_name="$1"
  local name_lower=$(echo "$skill_name" | tr '[:upper:]' '[:lower:]')

  # AI & ML
  if [[ "$name_lower" == ai-* || "$name_lower" == *llm* || "$name_lower" == *ai* ]]; then
    echo "ai-skills"
  # DevOps & Infrastructure
  elif [[ "$name_lower" == *kubectl* || "$name_lower" == *eksctl* || "$name_lower" == *argocd* || \
         "$name_lower" == *k8s* || "$name_lower" == *docker* || "$name_lower" == *aws* || \
         "$name_lower" == *gitlab* || "$name_lower" == *github* || "$name_lower" == *kargo* ]]; then
    echo "devops-skills"
  # Database & Backend
  elif [[ "$name_lower" == *postgres* || "$name_lower" == *supabase* || "$name_lower" == *database* || \
         "$name_lower" == *sql* || "$name_lower" == *postgres* ]]; then
    echo "tools-skills"
  # Marketing & SEO
  elif [[ "$name_lower" == *seo* || "$name_lower" == *marketing* || "$name_lower" == *audit* || \
         "$name_lower" == *content* || "$name_lower" == *brand* || "$name_lower" == *community* ]]; then
    echo "marketing-skills"
  # Product Management
  elif [[ "$name_lower" == *product* || "$name_lower" == *roadmap* || "$name_lower" == *prd* || \
         "$name_lower" == *metric* || "$name_lower" == *priorit* || "$name_lower" == *vision* ]]; then
    echo "product-skills"
  # Leadership & Team
  elif [[ "$name_lower" == *leadership* || "$name_lower" == *culture* || "$name_lower" == *hiring* || \
         "$name_lower" == *onboarding* || "$name_lower" == *1-1* || "$name_lower" == *1:1* || \
         "$name_lower" == *coaching* || "$name_lower" == *delegate* || "$name_lower" == *decision* ]]; then
    echo "leadership-skills"
  # Career
  elif [[ "$name_lower" == *career* || "$name_lower" == *job* || "$name_lower" == *interview* || \
         "$name_lower" == *promotion* || "$name_lower" == *offer* || "$name_lower" == *mentor* ]]; then
    echo "career-skills"
  # Engineering
  elif [[ "$name_lower" == *engineer* || "$name_lower" == *tech-debt* || "$name_lower" == *roadmap* || \
         "$name_lower" == *platform* || "$name_lower" == *design-syst* ]]; then
    echo "engineering-skills"
  # Communication
  elif [[ "$name_lower" == *presentation* || "$name_lower" == *communicat* || "$name_lower" == *writing* || \
         "$name_lower" == *fundrais* ]]; then
    echo "communication-skills"
  # Sales & GTM
  elif [[ "$name_lower" == *sales* || "$name_lower" == *founder* || "$name_lower" == *enterprise* || \
         "$name_lower" == *partnership* || "$name_lower" == *bd* ]]; then
    echo "sales-skills"
  # Obsidian & Notes
  elif [[ "$name_lower" == *obsidian* || "$name_lower" == *canvas* || "$name_lower" == *notebook* || \
         "$name_lower" == *note* || "$name_lower" == *task* ]]; then
    echo "obsidian-skills"
  # Default to tools
  else
    echo "tools-skills"
  fi
}

cmd_diff() {
  log_info "Previewing sync changes..."
  echo ""

  local system_skills=($(ls -d "$SYSTEM_SKILLS_DIR"/*/ 2>/dev/null | xargs -I {} basename {}))
  local system_count=${#system_skills[@]}

  local repo_skills=($(get_repo_skill_names))
  local repo_count=${#repo_skills[@]}

  echo "System skills:  $system_count"
  echo "Repo skills:    $repo_count"
  echo ""

  # Build a map of repo skills for fast lookup (using grep instead of associative array)
  echo "=== New skills in system (not in repo) ==="
  echo "----------------------------------------"

  local new_count=0
  for skill_dir in "$SYSTEM_SKILLS_DIR"/*/; do
    local skill_name=$(basename "$skill_dir")

    if [ "$skill_name" == "sync-skills-manager" ]; then
      continue
    fi

    # Check if skill exists in repo (any category)
    local found_in_repo=""
    for cat_dir in "$REPO_SKILLS_DIR"/*/; do
      local cat_name=$(basename "$cat_dir")
      if [ "$cat_name" == "sync-skills-manager" ]; then
        continue
      fi
      if [ -d "$cat_dir/$skill_name" ]; then
        found_in_repo="1"
        break
      fi
    done

    if [ -z "$found_in_repo" ]; then
      local category=$(auto_categorize "$skill_name")
      log_diff "  + $skill_name → $category/"
      new_count=$((new_count + 1))
    fi
  done

  if [ $new_count -eq 0 ]; then
    echo "  (no new skills)"
  else
    echo ""
    echo "Total: $new_count new skill(s)"
  fi

  echo ""
  echo "=== Skills in repo but NOT in system ==="
  echo "----------------------------------------"

  local missing_count=0
  for skill_name in "${repo_skills[@]}"; do
    if [ ! -d "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
      log_warn "  - $skill_name"
      missing_count=$((missing_count + 1))
    fi
  done

  if [ $missing_count -eq 0 ]; then
    echo "  (all repo skills exist in system)"
  else
    echo ""
    echo "Total: $missing_count skill(s) missing in system"
  fi
}

cmd_auto() {
  log_info "Auto-categorizing and syncing new skills..."

  local system_skills=($(ls -d "$SYSTEM_SKILLS_DIR"/*/ 2>/dev/null | xargs -I {} basename {}))
  local synced=0
  local skipped=0

  for skill_name in "${system_skills[@]}"; do
    if [ "$skill_name" == "sync-skills-manager" ]; then
      continue
    fi

    # Check if skill already exists in repo (any category)
    local found_in_repo=""
    for cat_dir in "$REPO_SKILLS_DIR"/*/; do
      local cat_name=$(basename "$cat_dir")
      if [ "$cat_name" == "sync-skills-manager" ]; then
        continue
      fi
      if [ -d "$cat_dir/$skill_name" ]; then
        found_in_repo="1"
        break
      fi
    done

    if [ -n "$found_in_repo" ]; then
      continue
    fi

    local category=$(auto_categorize "$skill_name")
    local target_dir="$REPO_SKILLS_DIR/$category"

    if [ ! -d "$target_dir" ]; then
      log_warn "Category $category doesn't exist, using tools-skills"
      category="tools-skills"
      target_dir="$REPO_SKILLS_DIR/$category"
    fi

    log_info "Adding: $skill_name → $category/"
    mkdir -p "$target_dir"

    # Copy with error handling for broken symlinks
    if cp -rL "$SYSTEM_SKILLS_DIR/$skill_name" "$target_dir/" 2>/dev/null; then
      synced=$((synced + 1))
    else
      # Try rsync without broken symlinks
      if rsync -av --exclude='data' --exclude='scripts' \
         "$SYSTEM_SKILLS_DIR/$skill_name/" "$target_dir/$skill_name/" 2>/dev/null; then
        log_warn "  Copied with some exclusions (broken symlinks skipped)"
        synced=$((synced + 1))
      else
        log_error "  Failed to copy $skill_name"
        skipped=$((skipped + 1))
      fi
    fi
  done

  echo ""
  if [ $synced -gt 0 ]; then
    log_info "Synced $synced new skill(s) to repository"
    log_info "Run 'git add -A && git commit' to save changes"
  fi
  if [ $skipped -gt 0 ]; then
    log_warn "Skipped $skipped skill(s) due to errors"
  fi
  if [ $synced -eq 0 ] && [ $skipped -eq 0 ]; then
    log_info "No new skills to sync (all skills already exist in repo)"
  fi
}

cmd_pull() {
  cmd_auto
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

  local system_count=$(ls -d "$SYSTEM_SKILLS_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ')
  local repo_count=$(get_repo_skill_names | wc -l | tr -d ' ')

  echo "System skills:  $system_count"
  echo "Repo skills:    $repo_count"
  echo ""

  # Count by category
  echo "Repo by category:"
  for cat_dir in "$REPO_SKILLS_DIR"/*/; do
    local cat_name=$(basename "$cat_dir")
    if [ "$cat_name" == "sync-skills-manager" ]; then
      continue
    fi
    local count=$(ls -d "$cat_dir"/*/ 2>/dev/null | wc -l | tr -d ' ')
    echo "  $cat_name: $count skills"
  done
  echo ""

  local missing=0
  echo "Skills in repo but NOT in system:"
  for skill_name in $(get_repo_skill_names); do
    if [ ! -d "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
      echo "  [ ] $skill_name"
      missing=$((missing + 1))
    fi
  done

  if [ $missing -eq 0 ]; then
    echo "  (all skills synced)"
  fi
}

# Main
case "${1:-help}" in
  diff)
    cmd_diff
    ;;
  pull|auto)
    cmd_auto
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
