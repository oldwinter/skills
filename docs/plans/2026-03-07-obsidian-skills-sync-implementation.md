# Obsidian Skills Sync Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a repository script that syncs skills into Obsidian notes, preserves user-owned rating metadata, and upgrades the Obsidian Base used to manage the notes.

**Architecture:** A standalone Python script will scan `SKILL.md` files, derive repo metadata, merge it into note frontmatter under `Atlas/Skills/`, and optionally write a `.base` file. Frontmatter merging will preserve non-managed keys and existing note bodies. Tests will use `unittest` with temporary directories because the repository has no shared test runner and no `pytest` dependency installed.

**Tech Stack:** Python 3 standard library, Markdown frontmatter text processing, Obsidian `.base` YAML files

---

### Task 1: Lock behavior with tests

**Files:**
- Create: `meta-skills/sync-skills-manager/scripts/test_export_skills_to_obsidian.py`

**Step 1: Write the failing test**

Cover:
- scanning repo skills
- creating a new vault note with default personal fields
- preserving existing personal fields and note body
- rendering the base file content

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest meta-skills.sync-skills-manager.scripts.test_export_skills_to_obsidian -v`

Expected: FAIL because the export script does not exist yet.

### Task 2: Implement the sync script

**Files:**
- Create: `meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py`

**Step 1: Implement repo scanning**

Read every `SKILL.md`, extract frontmatter `name` and `description`, and derive category/subcategory/path metadata from the file path.

**Step 2: Implement frontmatter block merge**

Preserve unknown keys from existing notes, overwrite managed keys, and add default personal fields only when missing.

**Step 3: Implement note writing**

Create/update files in the target vault notes folder without modifying unrelated notes.

**Step 4: Implement base rendering**

Render a `.base` file with views for overview, unrated, high-rated, and favorites/frequently used skills.

### Task 3: Verify behavior end-to-end

**Files:**
- Modify: `meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py`
- Modify: `meta-skills/sync-skills-manager/scripts/test_export_skills_to_obsidian.py`

**Step 1: Run unit tests**

Run: `python3 -m unittest meta-skills.sync-skills-manager.scripts.test_export_skills_to_obsidian -v`

Expected: PASS

**Step 2: Dry-run against the real vault**

Run: `python3 meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py --vault-root /Users/oldwinter/oldwinter-notes --dry-run`

Expected: summary of notes that would be created/updated and base file target.

**Step 3: Apply against the real vault**

Run: `python3 meta-skills/sync-skills-manager/scripts/export_skills_to_obsidian.py --vault-root /Users/oldwinter/oldwinter-notes --write-base`

Expected: notes synced into `Atlas/Skills` and `Atlas/Bases/skills管理.base` rewritten with the new views.

### Task 4: Final verification

**Files:**
- Read: `/Users/oldwinter/oldwinter-notes/Atlas/Skills/*.md`
- Read: `/Users/oldwinter/oldwinter-notes/Atlas/Bases/skills管理.base`

**Step 1: Inspect a sample note**

Confirm managed repo fields exist and personal fields remain intact.

**Step 2: Inspect the base file**

Confirm target columns and filters reference the new rating/classification fields.
