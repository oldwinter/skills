#!/bin/bash
set -euo pipefail

OUTPUT_DIR="${1:-.}"
mkdir -p "$OUTPUT_DIR"

TOP_HELP="$OUTPUT_DIR/top-help.txt"
COMMANDS="$OUTPUT_DIR/commands.txt"
ALL_HELP="$OUTPUT_DIR/all-commands-help.txt"
REPORT="$OUTPUT_DIR/help-report.md"

if ! command -v obsidian >/dev/null 2>&1; then
  echo "[ERROR] obsidian CLI not found in PATH" >&2
  exit 1
fi

obsidian --help > "$TOP_HELP"

awk '/^  [a-z][a-z0-9:-]*[[:space:]]{2,}/ {cmd=$1; if (cmd !~ /=/) print cmd}' "$TOP_HELP" \
  | sort -u > "$COMMANDS"

: > "$ALL_HELP"
while IFS= read -r cmd; do
  {
    echo "### $cmd"
    obsidian help "$cmd"
    echo
  } >> "$ALL_HELP"
done < "$COMMANDS"

{
  echo "# Obsidian CLI Help Dump"
  echo
  echo "- Generated (UTC): $(date -u '+%Y-%m-%d %H:%M:%SZ')"
  echo "- Command count: $(wc -l < "$COMMANDS" | tr -d ' ')"
  echo
  echo "## Top-Level Help"
  echo '```text'
  cat "$TOP_HELP"
  echo '```'
  echo
  echo "## Per-Command Help"
  echo '```text'
  cat "$ALL_HELP"
  echo '```'
} > "$REPORT"

echo "[OK] Top-level help: $TOP_HELP"
echo "[OK] Command list: $COMMANDS"
echo "[OK] Per-command help: $ALL_HELP"
echo "[OK] Markdown report: $REPORT"
