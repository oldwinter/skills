#!/bin/bash
# Sync Skills Manager - Sync repository-canonical skills and local agent dirs
# Supports categorized subdirectories (repo-root first, system-skills compatible)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_SKILLS_DIR="${SYSTEM_SKILLS_DIR:-$HOME/.claude/skills}"
GEMINI_SKILLS_DIR="${GEMINI_SKILLS_DIR:-$HOME/.gemini/skills}"
AGENT_TARGET_DIRS="${AGENT_TARGET_DIRS:-$HOME/.codex/skills,$HOME/.config/agents/skills,$HOME/.cursor/skills,$HOME/.gemini/antigravity/skills,$HOME/.factory/skills,$HOME/.gemini/skills,$HOME/.config/opencode/skills,$HOME/.agents/skills}"
REPO_ROOT="${REPO_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
REPO_SKILLS_DIR="${REPO_SKILLS_DIR:-$REPO_ROOT}"
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
Sync Skills Manager - Sync between repository-canonical skills and runtime skill directories

Usage: $0 <command> [options]

Commands:
  diff      Preview changes (runtime skills not in repo)
  pull      Sync runtime → repository (add new skills only)
  push      Sync repository → runtime ($SYSTEM_SKILLS_DIR)
  link-all  Rebuild agent dirs as symlinks to runtime source
  dedupe  Remove duplicate skills from ~/.gemini/skills
  status  Show current sync status
  auto      Auto-categorize and sync new skills
  help    Show this help message

Examples:
  $0 diff      # Preview what would be synced
  $0 pull      # Add new skills from runtime directory to repo
  $0 auto      # Auto-categorize and sync new skills
  $0 push      # Sync all repo skills to runtime source
  $0 link-all  # Rebuild agent directories to symlink from runtime source
  $0 dedupe    # Remove overlaps from ~/.gemini/skills
  $0 status    # Show sync status

Environment:
  SYSTEM_SKILLS_DIR (default: ~/.claude/skills)
  REPO_ROOT        (default: repo root of this script)
  REPO_SKILLS_DIR  (default: \$REPO_ROOT)
  AGENT_TARGET_DIRS (comma-separated target skill dirs)

EOF
}

# Get all skill names in repo (recursively, excluding sync-skills-manager and category dirs)
get_repo_skill_names() {
  while IFS= read -r -d '' skill_md; do
    basename "$(dirname "$skill_md")"
  done < <(find "$REPO_SKILLS_DIR" -type f -name "SKILL.md" -print0) \
    | grep -v '^sync-skills-manager$' \
    | sort -u
}

# List category directories (dirs ending with "-skills" that directly contain skill dirs)
list_repo_category_dirs() {
  local cat_dir
  while IFS= read -r -d '' cat_dir; do
    case "$cat_dir" in
      */.git/*|*/node_modules/*|*/__pycache__/*)
        continue
        ;;
    esac
    if [ "$(basename "$cat_dir")" = "system-skills" ]; then
      continue
    fi

    local has_skill=0
    local maybe_skill
    for maybe_skill in "$cat_dir"/*/; do
      [ -d "$maybe_skill" ] || continue
      if [ -f "$maybe_skill/SKILL.md" ]; then
        has_skill=1
        break
      fi
    done

    if [ "$has_skill" -eq 1 ]; then
      echo "$cat_dir"
    fi
  done < <(find "$REPO_SKILLS_DIR" -type d -name "*-skills" -print0) | sort -u
}

resolve_category_dir() {
  local category="$1"
  local root_candidate="$REPO_SKILLS_DIR/$category"
  local fallback=""
  local cat_dir

  # Repo-root is canonical when present.
  if [ -d "$root_candidate" ]; then
    echo "$root_candidate"
    return 0
  fi

  while IFS= read -r cat_dir; do
    [ "$(basename "$cat_dir")" = "$category" ] || continue
    case "$cat_dir" in
      "$REPO_SKILLS_DIR/system-skills/"*)
        [ -n "$fallback" ] || fallback="$cat_dir"
        ;;
      *)
        echo "$cat_dir"
        return 0
        ;;
    esac
  done < <(list_repo_category_dirs)

  if [ -n "$fallback" ]; then
    echo "$fallback"
    return 0
  fi

  echo "$root_candidate"
}

# Find which category directory contains a skill
find_skill_category() {
  local skill_name="$1"
  local cat_dir
  while IFS= read -r cat_dir; do
    if [ -d "$cat_dir/$skill_name" ]; then
      echo "$cat_dir"
      return 0
    fi
  done < <(list_repo_category_dirs)
  return 1
}

# Get all categories (subdirectories)
get_categories() {
  list_repo_category_dirs | xargs -I {} basename {} | sort -u
}

# Auto-determine category for a skill
auto_categorize() {
  local skill_name="$1"
  local name_lower=$(echo "$skill_name" | tr '[:upper:]' '[:lower:]')

  # AI & ML
  if [[ "$name_lower" == ai-* || "$name_lower" == *llm* || "$name_lower" == *openai* || \
        "$name_lower" == *context7* || "$name_lower" == *doc*lookup* || "$name_lower" == *firecrawl* || \
        "$name_lower" == *mcp-builder* || "$name_lower" == *retrieval* || "$name_lower" == *eval-harness* ]]; then
    echo "ai-skills"
  # DevOps & Infrastructure
  elif [[ "$name_lower" == *kubectl* || "$name_lower" == *eksctl* || "$name_lower" == *argocd* || \
         "$name_lower" == *k8s* || "$name_lower" == *docker* || "$name_lower" == *aws* || \
         "$name_lower" == *gitlab* || "$name_lower" == *github* || "$name_lower" == gh-* || \
         "$name_lower" == *kargo* || "$name_lower" == *deploy* || "$name_lower" == *release* || \
         "$name_lower" == *terraform* || "$name_lower" == *sync-ci* || "$name_lower" == *ci-fix* || \
         "$name_lower" == *cloudflare* || "$name_lower" == *vercel* || "$name_lower" == *ecc* ]]; then
    echo "devops-skills"
  # Engineering & Code Quality
  elif [[ "$name_lower" == *pattern* || "$name_lower" == *testing* || "$name_lower" == *security* || \
         "$name_lower" == *tdd* || "$name_lower" == *verification* || "$name_lower" == *playwright* || \
         "$name_lower" == *web-performance* || "$name_lower" == *web-accessibility* || "$name_lower" == *web-design* || \
         "$name_lower" == *ui-ux* || "$name_lower" == *remotion* || "$name_lower" == *postgres* || \
         "$name_lower" == *supabase* || "$name_lower" == *clickhouse* || "$name_lower" == *mdbase* || \
         "$name_lower" == *coding-standards* ]]; then
    echo "engineering-skills"
  # Marketing & SEO
  elif [[ "$name_lower" == baoyu-* || "$name_lower" == *seo* || "$name_lower" == *marketing* || "$name_lower" == *audit* || \
         "$name_lower" == *content* || "$name_lower" == *brand* || "$name_lower" == *community* ]]; then
    echo "marketing-skills"
  # Product Management
  elif [[ "$name_lower" == *product* || "$name_lower" == *roadmap* || "$name_lower" == *prd* || \
         "$name_lower" == *metric* || "$name_lower" == *priorit* || "$name_lower" == *vision* || \
         "$name_lower" == *linear* || "$name_lower" == *retention* || "$name_lower" == *scoping* || \
         "$name_lower" == *positioning* || "$name_lower" == *research* || "$name_lower" == *marketplace* ]]; then
    echo "product-skills"
  # Leadership & Team
  elif [[ "$name_lower" == *leadership* || "$name_lower" == *culture* || "$name_lower" == *hiring* || \
         "$name_lower" == *onboarding* || "$name_lower" == *1-1* || "$name_lower" == *1:1* || \
         "$name_lower" == *coaching* || "$name_lower" == *delegate* || "$name_lower" == *decision* || \
         "$name_lower" == *ritual* || "$name_lower" == *post-mortem* || "$name_lower" == *okrs* ]]; then
    echo "leadership-skills"
  # Career
  elif [[ "$name_lower" == *career* || "$name_lower" == *job* || "$name_lower" == *interview* || \
         "$name_lower" == *promotion* || "$name_lower" == *offer* || "$name_lower" == *mentor* || \
         "$name_lower" == *continuous-learning* ]]; then
    echo "career-skills"
  # Communication
  elif [[ "$name_lower" == *presentation* || "$name_lower" == *communicat* || "$name_lower" == *writing* || \
         "$name_lower" == *fundrais* || "$name_lower" == *humanizer* || "$name_lower" == *docs-update* || \
         "$name_lower" == *changelog* ]]; then
    echo "communication-skills"
  # Sales & GTM
  elif [[ "$name_lower" == *sales* || "$name_lower" == *founder* || "$name_lower" == *enterprise* || \
         "$name_lower" == *partnership* || "$name_lower" == *bd* ]]; then
    echo "sales-skills"
  # Obsidian & Notes
  elif [[ "$name_lower" == *obsidian* || "$name_lower" == *canvas* || "$name_lower" == *notebook* || \
         "$name_lower" == *note* || "$name_lower" == *task* || "$name_lower" == *scheduler* || \
         "$name_lower" == *excalidraw* ]]; then
    echo "obsidian-skills"
  # Default to tools
  else
    echo "tools-skills"
  fi
}

dedupe_gemini_overlaps() {
  local removed=0

  if [ ! -d "$GEMINI_SKILLS_DIR" ]; then
    echo "$removed"
    return
  fi

  while IFS= read -r -d '' gemini_dir; do
    local skill_name
    skill_name="$(basename "$gemini_dir")"

    # Keep canonical symlinks; remove copied/foreign overlaps from Gemini.
    if [ -L "$gemini_dir" ]; then
      local link_target abs_target expected_target
      link_target="$(readlink "$gemini_dir" || true)"
      abs_target="$(cd "$(dirname "$gemini_dir")" && cd "$(dirname "$link_target")" 2>/dev/null && pwd)/$(basename "$link_target")"
      expected_target="$SYSTEM_SKILLS_DIR/$skill_name"
      if [ "$abs_target" = "$expected_target" ]; then
        continue
      fi
    fi

    if [ -d "$SYSTEM_SKILLS_DIR/$skill_name" ] || [ -L "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
      rm -rf "$gemini_dir"
      removed=$((removed + 1))
    fi
  done < <(find "$GEMINI_SKILLS_DIR" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) -print0)

  echo "$removed"
}

get_canonical_skill_names() {
  find "$SYSTEM_SKILLS_DIR" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) \
    -exec sh -c 'p="$1"; [ -f "$p/SKILL.md" ] && basename "$p"' _ {} \; 2>/dev/null | sort -u
}

is_reserved_entry() {
  local target_dir="$1"
  local entry_name="$2"

  case "$target_dir" in
    "$HOME/.codex/skills")
      [ "$entry_name" = ".system" ]
      return
      ;;
    "$HOME/.factory/skills")
      [ "$entry_name" = "template" ]
      return
      ;;
  esac

  return 1
}

relink_target_dir() {
  local target_dir="$1"
  mkdir -p "$target_dir"

  while IFS= read -r -d '' entry; do
    local name
    name="$(basename "$entry")"

    # Keep dotfiles/directories as agent internals.
    if [[ "$name" == .* ]]; then
      continue
    fi

    if is_reserved_entry "$target_dir" "$name"; then
      continue
    fi

    rm -rf "$entry"
  done < <(find "$target_dir" -mindepth 1 -maxdepth 1 -print0)

  local linked=0
  while IFS= read -r skill_name; do
    [ -n "$skill_name" ] || continue
    if is_reserved_entry "$target_dir" "$skill_name"; then
      continue
    fi
    ln -s "$SYSTEM_SKILLS_DIR/$skill_name" "$target_dir/$skill_name"
    linked=$((linked + 1))
  done < <(get_canonical_skill_names)

  log_info "Linked $linked skill(s) -> $target_dir"
}

cmd_link_all() {
  log_info "Rebuilding agent links from canonical source: $SYSTEM_SKILLS_DIR"

  local list="$AGENT_TARGET_DIRS"
  IFS=',' read -r -a targets <<< "$list"

  local target
  for target in "${targets[@]}"; do
    # trim leading/trailing whitespace
    target="$(echo "$target" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
    [ -n "$target" ] || continue
    relink_target_dir "$target"
  done
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
    local cat_dir
    while IFS= read -r cat_dir; do
      if [ -d "$cat_dir/$skill_name" ]; then
        found_in_repo="1"
        break
      fi
    done < <(list_repo_category_dirs)

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
    local cat_dir
    while IFS= read -r cat_dir; do
      if [ -d "$cat_dir/$skill_name" ]; then
        found_in_repo="1"
        break
      fi
    done < <(list_repo_category_dirs)

    if [ -n "$found_in_repo" ]; then
      continue
    fi

    local category=$(auto_categorize "$skill_name")
    local target_dir
    target_dir="$(resolve_category_dir "$category")"

    if [ ! -d "$target_dir" ]; then
      log_warn "Category $category doesn't exist, using tools-skills"
      category="tools-skills"
      target_dir="$(resolve_category_dir "$category")"
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
  log_info "Syncing repository skills to: $SYSTEM_SKILLS_DIR"

  mkdir -p "$SYSTEM_SKILLS_DIR"

  local synced=0
  local updated=0
  local tmp_file
  tmp_file="$(mktemp)"

  # Choose newest SKILL.md copy per skill name when duplicates exist in repo.
  while IFS= read -r -d '' skill_md; do
    local skill_dir
    local skill_name
    local mtime
    skill_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$skill_dir")"
    if [ "$skill_name" == "sync-skills-manager" ]; then
      continue
    fi
    mtime="$(stat -f '%m' "$skill_md")"
    printf '%s\t%s\t%s\n' "$skill_name" "$mtime" "$skill_dir" >> "$tmp_file"
  done < <(find "$REPO_SKILLS_DIR" -type f -name "SKILL.md" -print0)

  if [ -s "$tmp_file" ]; then
    while IFS=$'\t' read -r skill_name skill_dir; do
      if [ -d "$SYSTEM_SKILLS_DIR/$skill_name" ] || [ -L "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
        updated=$((updated + 1))
      else
        synced=$((synced + 1))
      fi
      # Canonical should own real directories; avoid writing through symlink targets.
      if [ -L "$SYSTEM_SKILLS_DIR/$skill_name" ]; then
        rm -f "$SYSTEM_SKILLS_DIR/$skill_name"
      fi
      mkdir -p "$SYSTEM_SKILLS_DIR/$skill_name"
      rsync -a --delete "$skill_dir/" "$SYSTEM_SKILLS_DIR/$skill_name/"
    done < <(sort -k1,1 -k2,2nr "$tmp_file" | awk -F '\t' '!seen[$1]++ {print $1 "\t" $3}')
  fi

  rm -f "$tmp_file"

  log_info "Repo push complete (new: $synced, updated: $updated)"
  cmd_link_all
  local removed
  removed="$(dedupe_gemini_overlaps)"
  if [ "$removed" -gt 0 ]; then
    log_info "Gemini dedupe complete (removed overlaps: $removed)"
  else
    log_info "Gemini dedupe: no overlapping entries found"
  fi
}

cmd_dedupe() {
  local removed
  removed="$(dedupe_gemini_overlaps)"
  if [ "$removed" -gt 0 ]; then
    log_info "Gemini dedupe complete (removed overlaps: $removed)"
  else
    log_info "Gemini dedupe: no overlapping entries found"
  fi
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
  local cat_dir
  while IFS= read -r cat_dir; do
    local cat_name="${cat_dir#$REPO_SKILLS_DIR/}"
    local count
    count="$(find "$cat_dir" -mindepth 1 -maxdepth 1 -type d -exec sh -c '[ -f "$1/SKILL.md" ] && echo "$1"' _ {} \; | wc -l | tr -d ' ')"
    echo "  $cat_name: $count skills"
  done < <(list_repo_category_dirs)
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
  link-all)
    cmd_link_all
    ;;
  dedupe)
    cmd_dedupe
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
