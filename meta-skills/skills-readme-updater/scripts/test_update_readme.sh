#!/usr/bin/env bash
# Fixture and live tests for the README auditor.
set -euo pipefail

root="$(cd "$(dirname "$0")/../../.." && pwd)"
script="$root/meta-skills/skills-readme-updater/scripts/update_readme.py"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fail() {
  echo "test_update_readme: $1" >&2
  exit 1
}

chmod +x "$script"

if grep -n 'expanduser("~/.claude/skills")' "$script"; then
  fail "auditor must not default to ~/.claude/skills"
fi
if grep -n 'README_PATH' "$script"; then
  fail "auditor must not define a README write path"
fi
if grep -nE 'write_text|open\(.+[\"w\"]' "$script"; then
  fail "auditor must not write files"
fi

before="$(cksum "$root/README.md")"
live="$tmp/live.txt"
python3 "$script" --repo "$root" >"$live"
after="$(cksum "$root/README.md")"
[[ "$before" == "$after" ]] || fail "live audit must not change README.md"
grep -q '^- add-just-doctor$' "$live" || fail "live audit must list root skill add-just-doctor"
grep -q '^- github-cli$' "$live" || fail "live audit must list bucket skill github-cli"
grep -q '^## root' "$live" || fail "live audit must have a root section"
grep -q '^## devops-skills' "$live" || fail "live audit must have a devops-skills section"
grep -q '^## collisions' "$live" || fail "live audit must report collisions"

fixture="$tmp/repo"
mkdir -p "$fixture/add-just-doctor" "$fixture/devops-skills/github-cli" \
  "$fixture/meta-skills/find-skills" "$fixture/find-skills"
for path in add-just-doctor devops-skills/github-cli meta-skills/find-skills find-skills; do
  printf '%s\n' '---' 'name: demo' 'description: demo' '---' >"$fixture/$path/SKILL.md"
done
printf '%s\n' '### Standalone Skills' '- **add-just-doctor** — demo' >"$fixture/README.md"

out="$tmp/fixture.txt"
python3 "$script" --repo "$fixture" >"$out"
[[ "$(cksum "$fixture/README.md")" == "$(cksum "$fixture/README.md")" ]]
grep -q '^- add-just-doctor$' "$out" || fail "fixture must list root add-just-doctor"
grep -q '^- github-cli$' "$out" || fail "fixture must list github-cli"
grep -q 'github-cli' <(grep -A20 'in tree, not in README' "$out") || fail "fixture should report github-cli missing from README"
grep -q 'find-skills: find-skills, meta-skills/find-skills' "$out" || fail "fixture should report find-skills collision"

printf '%s\n' '### Standalone Skills' '- **add-just-doctor** — demo' '- **github-cli** — demo' '- **ghost-skill** — demo' >"$fixture/README.md"
python3 "$script" --repo "$fixture" >"$out"
grep -q 'ghost-skill' <(grep -A20 'in README, not in tree' "$out") || fail "fixture should report README-only ghost-skill"
after_fixture="$(cksum "$fixture/README.md")"
python3 "$script" --repo "$fixture" >/dev/null
[[ "$(cksum "$fixture/README.md")" == "$after_fixture" ]] || fail "fixture audit must not rewrite README.md"

echo "test_update_readme: ok"
