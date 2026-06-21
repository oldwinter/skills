# Obsidian Skill State Sync Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add an Obsidian-to-repo sidecar sync so personal skill ratings, statuses, aliases, tags, and supplemental notes can be versioned in this repository without modifying `SKILL.md`.

**Architecture:** Keep repository-owned skill metadata in `SKILL.md` and store Obsidian-owned personal state in a sidecar file under `meta-skills/sync-skills-manager/data/`. A new import script will scan `Atlas/Skills/*.md`, extract a small whitelist of personal fields plus the `## 补充笔记` section, and write them to the sidecar. The existing repo-to-Obsidian export script will read that sidecar and use it only as a seed source when a vault note is new or missing those personal fields.

**Tech Stack:** Python 3 standard library, Markdown frontmatter text parsing, custom YAML emitter/parser for the sidecar, Obsidian Markdown notes

---

### Task 1: Write failing tests for sidecar round-trip

**Files:**
- Create: `meta-skills/sync-skills-manager/scripts/test_obsidian_skill_state.py`

**Step 1: Write the failing test**

Cover:
- parsing a skill note and extracting white-listed personal state
- capturing the `## 补充笔记` section only
- writing sidecar YAML and reading it back
- importing vault state into the sidecar file
- seeding repo-to-Obsidian export from the sidecar when a note is created

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest meta-skills/sync-skills-manager/scripts/test_obsidian_skill_state.py -v`

Expected: FAIL because the shared state helpers and import script do not exist yet.

### Task 2: Implement shared state helpers

**Files:**
- Create: `meta-skills/sync-skills-manager/scripts/obsidian_skill_state.py`

**Step 1: Add frontmatter parsing helpers**

Parse top-level scalar/list frontmatter values from Obsidian skill notes using standard library only.

**Step 2: Add supplemental notes extraction**

Extract only the `## 补充笔记` section from note bodies so generated sections are not duplicated into the sidecar.

**Step 3: Add sidecar YAML read/write**

Support the repository-owned schema:

```yaml
generated_at: "YYYY-MM-DD"
skills:
  skill-id:
    rating: 5
    status: "常用"
    tags:
      - "obsidian"
    favorite: true
    reviewed_at: "YYYY-MM-DD"
    aliases:
      - "alias"
    notes: |
      Extra note content
```

### Task 3: Implement Obsidian-to-repo import

**Files:**
- Create: `meta-skills/sync-skills-manager/scripts/import_obsidian_skill_state.py`

**Step 1: Scan target notes folder**

Read `Atlas/Skills/*.md`, ignore index notes without `skill_id`, and normalize values for the sidecar.

**Step 2: Write only meaningful personal state**

Skip entries that contain only defaults and no supplemental notes to keep the sidecar compact.

**Step 3: Add CLI**

Add `--vault-root`, `--notes-dir`, `--state-path`, and `--dry-run`.

### Task 4: Update repo-to-Obsidian export

**Files:**
- Modify: `meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py`

**Step 1: Read sidecar state**

Load the sidecar file if present.

**Step 2: Seed missing personal fields**

Use sidecar values for `aliases`, `个人评分`, `个人状态`, `个人标签`, `精选`, and `最后评估` only when the vault note is new or the specific field is missing.

**Step 3: Seed supplemental notes for new notes**

Append a `## 补充笔记` section for newly created notes when the sidecar contains notes.

### Task 5: Document the workflow

**Files:**
- Modify: `/Users/oldwinter/oldwinter-notes/Atlas/Skills/∑ Skills 管理.md`

**Step 1: Add bidirectional sync commands**

Document:
- repo -> Obsidian
- Obsidian -> repo sidecar

**Step 2: Add ownership rules**

Clarify which fields are owned by the repo and which are owned by Obsidian.

### Task 6: Verify behavior end-to-end

**Files:**
- Read: `meta-skills/sync-skills-manager/scripts/*.py`
- Read: `meta-skills/sync-skills-manager/data/obsidian-skill-state.yaml`

**Step 1: Run tests**

Run: `python3 -m unittest meta-skills/sync-skills-manager/scripts/test_obsidian_skill_state.py -v`

Expected: PASS

**Step 2: Import real vault state**

Run: `python3 meta-skills/sync-skills-manager/scripts/import_obsidian_skill_state.py --vault-root /Users/oldwinter/oldwinter-notes`

Expected: sidecar file written under `meta-skills/sync-skills-manager/data/`.

**Step 3: Verify export stays clean**

Run: `python3 meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py --vault-root /Users/oldwinter/oldwinter-notes --dry-run --write-base`

Expected: `created=0, updated=0` after import and one fresh export.
