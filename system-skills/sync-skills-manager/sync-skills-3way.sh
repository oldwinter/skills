#!/bin/bash
# Three-way incremental sync for skills:
#   ~/.codex/skills  <->  ~/.claude/skills  <->  repo skills tree
#
# Behavior:
# - Incremental only (rsync --update), no delete.
# - Uses newest repo copy per skill name as canonical when syncing repo -> local dirs.
# - New skills not found in repo are placed under system-skills/tools-skills/<skill-name>.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex/skills}"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude/skills}"
REPO_NEW_SKILL_DIR="${REPO_NEW_SKILL_DIR:-$REPO_ROOT/system-skills/tools-skills}"
LINK_SCRIPT="${LINK_SCRIPT:-$SCRIPT_DIR/sync-skills.sh}"

COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RED='\033[0;31m'

log_info() { echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $1"; }
log_warn() { echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1"; }
log_error() { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"; }

usage() {
  cat <<EOF
3-way incremental skills sync

Usage:
  $0 sync      # Run 3-way incremental sync (default)
  $0 status    # Show counts + name-level diff summary
  $0 help

Environment overrides:
  CODEX_DIR           (default: ~/.codex/skills)
  CLAUDE_DIR          (default: ~/.claude/skills)
  REPO_NEW_SKILL_DIR  (default: <repo>/system-skills/tools-skills)
  LINK_SCRIPT         (default: <repo>/system-skills/sync-skills-manager/sync-skills.sh)
EOF
}

TMP_DIR=""
MAP_DIR=""

cleanup() {
  if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}

init_runtime() {
  mkdir -p "$CLAUDE_DIR" "$REPO_NEW_SKILL_DIR"
  TMP_DIR="$(mktemp -d)"
  MAP_DIR="$TMP_DIR/repo-map"
  mkdir -p "$MAP_DIR"
  trap cleanup EXIT
}

build_repo_map() {
  rm -rf "$MAP_DIR"
  mkdir -p "$MAP_DIR"

  while IFS= read -r -d '' skill_md; do
    local skill_dir
    skill_dir="$(dirname "$skill_md")"
    local skill_name
    skill_name="$(basename "$skill_dir")"
    printf '%s\n' "$skill_dir" >> "$MAP_DIR/$skill_name.list"
  done < <(find "$REPO_ROOT" -type f -name 'SKILL.md' -print0)

  for f in "$MAP_DIR"/*.list; do
    [ -f "$f" ] || continue
    sort -u "$f" -o "$f"
    prune_nested_paths "$f"
  done
}

prune_nested_paths() {
  local list_file="$1"
  local tmp_file
  tmp_file="$(mktemp)"

  awk '
    { paths[NR]=$0 }
    END {
      for (i=1; i<=NR; i++) {
        keep=1
        for (j=1; j<=NR; j++) {
          if (i==j) continue
          prefix=paths[j] "/"
          if (index(paths[i], prefix)==1) {
            keep=0
            break
          }
        }
        if (keep) print paths[i]
      }
    }
  ' "$list_file" | sort -u > "$tmp_file"

  mv "$tmp_file" "$list_file"
}

rsync_skill_dir() {
  local src_dir="$1"
  local dst_dir="$2"
  local follow_links="$3"
  local skill_name="$4"

  if [ -L "$dst_dir" ]; then
    rm -f "$dst_dir"
  fi
  mkdir -p "$dst_dir"

  if [ "$follow_links" = "yes" ]; then
    rsync -aL --update --exclude "$skill_name/" "$src_dir/" "$dst_dir/" >/dev/null
  else
    rsync -a --update --exclude "$skill_name/" "$src_dir/" "$dst_dir/" >/dev/null
  fi
}

sync_skill_to_repo() {
  local skill_name="$1"
  local src_dir="$2"
  local follow_links="$3"

  if [ -f "$MAP_DIR/$skill_name.list" ]; then
    while IFS= read -r repo_dir; do
      [ -n "$repo_dir" ] || continue
      rsync_skill_dir "$src_dir" "$repo_dir" "$follow_links" "$skill_name"
    done < "$MAP_DIR/$skill_name.list"
  else
    local target_dir="$REPO_NEW_SKILL_DIR/$skill_name"
    mkdir -p "$target_dir"
    rsync_skill_dir "$src_dir" "$target_dir" "$follow_links" "$skill_name"
    printf '%s\n' "$target_dir" > "$MAP_DIR/$skill_name.list"
    log_info "repo add: $skill_name -> ${target_dir#$REPO_ROOT/}"
  fi
}

sync_skill_to_canonical() {
  local skill_name="$1"
  local src_dir="$2"
  local follow_links="$3"
  rsync_skill_dir "$src_dir" "$CLAUDE_DIR/$skill_name" "$follow_links" "$skill_name"
}

collect_codex_sources() {
  local out_file="$1"
  : > "$out_file"

  if [ -d "$CODEX_DIR/.system" ]; then
    while IFS= read -r -d '' d; do
      [ -f "$d/SKILL.md" ] || continue
      printf '%s\n' "$d" >> "$out_file"
    done < <(find "$CODEX_DIR/.system" -mindepth 1 -maxdepth 1 -type d -print0)
  fi

  if [ -d "$CODEX_DIR" ]; then
    while IFS= read -r -d '' d; do
      local name
      name="$(basename "$d")"
      [ "$name" = ".system" ] && continue
      [ -f "$d/SKILL.md" ] || continue

      # Skip mirrored links that already point into canonical Claude source.
      if [ -L "$d" ]; then
        local link_target abs_target
        link_target="$(readlink "$d" || true)"
        abs_target="$(cd "$(dirname "$d")" && cd "$(dirname "$link_target")" 2>/dev/null && pwd)/$(basename "$link_target")"
        case "$abs_target" in
          "$CLAUDE_DIR"/*) continue ;;
        esac
      fi

      printf '%s\n' "$d" >> "$out_file"
    done < <(find "$CODEX_DIR" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) -print0)
  fi

  sort -u "$out_file" -o "$out_file"
}

repo_latest_dir_for_skill() {
  local list_file="$1"
  local latest_path=""
  local latest_mtime=0

  while IFS= read -r repo_dir; do
    [ -f "$repo_dir/SKILL.md" ] || continue
    local mtime
    mtime="$(stat -f '%m' "$repo_dir/SKILL.md")"
    if [ "$mtime" -gt "$latest_mtime" ]; then
      latest_mtime="$mtime"
      latest_path="$repo_dir"
    fi
  done < "$list_file"

  printf '%s' "$latest_path"
}

cmd_sync() {
  init_runtime
  build_repo_map

  local codex_list="$TMP_DIR/codex-sources.list"
  collect_codex_sources "$codex_list"

  log_info "Step 1/4: codex -> claude/repo"
  while IFS= read -r src_dir; do
    [ -n "$src_dir" ] || continue
    local skill_name
    skill_name="$(basename "$src_dir")"
    [ "$skill_name" = ".system" ] && continue

    sync_skill_to_canonical "$skill_name" "$src_dir" "yes"
    sync_skill_to_repo "$skill_name" "$src_dir" "yes"
  done < "$codex_list"

  log_info "Step 2/4: ~/.claude/skills -> repo"
  while IFS= read -r -d '' src_dir; do
    [ -f "$src_dir/SKILL.md" ] || continue
    local skill_name
    skill_name="$(basename "$src_dir")"
    sync_skill_to_repo "$skill_name" "$src_dir" "yes"
  done < <(find "$CLAUDE_DIR" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) -print0)

  log_info "Step 3/4: newest repo copy -> ~/.claude/skills"
  for list_file in "$MAP_DIR"/*.list; do
    [ -f "$list_file" ] || continue
    local skill_name
    skill_name="$(basename "$list_file" .list)"

    local latest_repo_dir
    latest_repo_dir="$(repo_latest_dir_for_skill "$list_file")"
    [ -n "$latest_repo_dir" ] || continue

    rsync_skill_dir "$latest_repo_dir" "$CLAUDE_DIR/$skill_name" "no" "$skill_name"
  done

  log_info "Step 4/4: refresh agent symlinks from ~/.claude/skills"
  if [ -x "$LINK_SCRIPT" ]; then
    "$LINK_SCRIPT" link-all >/dev/null
  else
    log_warn "Skip link refresh (script not executable): $LINK_SCRIPT"
  fi

  log_info "Sync finished"
  cmd_status
}

cmd_status() {
  local claude_list codex_list repo_list
  claude_list="$(mktemp)"
  codex_list="$(mktemp)"
  repo_list="$(mktemp)"

  find "$CLAUDE_DIR" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) \
    -exec sh -c '[ -f "$1/SKILL.md" ] && basename "$1"' _ {} \; | sort -u > "$claude_list"

  if [ -d "$CODEX_DIR/.system" ]; then
    find "$CODEX_DIR/.system" -mindepth 1 -maxdepth 1 -type d \
      -exec sh -c '[ -f "$1/SKILL.md" ] && basename "$1"' _ {} \; > "$codex_list"
  else
    : > "$codex_list"
  fi

  find "$CODEX_DIR" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) \
    -exec sh -c 'name="$(basename "$1")"; [ "$name" = ".system" ] && exit 0; [ -f "$1/SKILL.md" ] && echo "$name"' _ {} \; \
    | sort -u >> "$codex_list"
  sort -u "$codex_list" -o "$codex_list"

  find "$REPO_ROOT" -type f -name 'SKILL.md' -exec dirname {} \; | xargs -I{} basename {} | sort -u > "$repo_list"

  local claude_count codex_count repo_count
  claude_count="$(wc -l < "$claude_list" | tr -d ' ')"
  codex_count="$(wc -l < "$codex_list" | tr -d ' ')"
  repo_count="$(wc -l < "$repo_list" | tr -d ' ')"

  echo "3-way sync status"
  echo "----------------------------------------"
  echo "codex dir:    $CODEX_DIR"
  echo "claude dir:   $CLAUDE_DIR"
  echo "repo root:    $REPO_ROOT"
  echo ""
  echo "counts"
  echo "  codex unique      : $codex_count"
  echo "  claude canonical  : $claude_count"
  echo "  repo unique       : $repo_count"
  echo ""

  local claude_only repo_only codex_only codex_diff
  claude_only="$(comm -23 "$claude_list" "$repo_list" | wc -l | tr -d ' ')"
  repo_only="$(comm -13 "$claude_list" "$repo_list" | wc -l | tr -d ' ')"
  codex_only="$(comm -23 "$codex_list" "$claude_list" | wc -l | tr -d ' ')"
  codex_diff="$(comm -3 "$codex_list" "$claude_list" | wc -l | tr -d ' ')"

  echo "name-level diff summary"
  echo "  claude only vs repo : $claude_only"
  echo "  repo only vs claude : $repo_only"
  echo "  codex only vs claude: $codex_only"
  echo "  codex vs claude diff-lines: $codex_diff"

  rm -f "$claude_list" "$codex_list" "$repo_list"
}

case "${1:-sync}" in
  sync)
    cmd_sync
    ;;
  status)
    cmd_status
    ;;
  help|--help|-h)
    usage
    ;;
  *)
    log_error "Unknown command: $1"
    usage
    exit 1
    ;;
esac
