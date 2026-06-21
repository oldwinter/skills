# Obsidian Skills Sync Design

**Date:** 2026-03-07

## Goal

Build a repo-to-Obsidian sync flow so skills from this repository can be managed inside `/Users/oldwinter/oldwinter-notes` with personal ratings, statuses, and tags, without polluting `SKILL.md` frontmatter in the repository.

## Scope

- Scan every `SKILL.md` in this repository.
- Sync each skill into one note under `Atlas/Skills/`.
- Preserve personal metadata already stored in the vault.
- Update `Atlas/Bases/skills管理.base` so it can filter and sort by personal rating/classification fields.

## Data Model

The vault note is the source of truth for personal metadata.

Managed repo-derived fields:

- `skill_name`
- `skill_id`
- `仓库分类`
- `仓库子分类`
- `仓库路径`
- `作用描述`
- `触发场景`
- `英文说明`
- `来源路径`
- `同步时间`

Personal fields kept in Obsidian:

- `个人评分`
- `个人状态`
- `个人标签`
- `精选`
- `最后评估`

## Sync Rules

- Repository metadata overwrites only managed fields.
- Existing personal fields are preserved.
- Existing note body is preserved.
- New notes get a simple generated body with usage hints.
- Files in `Atlas/Skills/` that do not map to a repo skill are left untouched.

## Base Rules

Update the existing `skills管理.base` with views for:

- all synced skills
- unrated skills
- high-rated skills
- favorites / frequently used skills

The base will rely on note frontmatter fields only; no repo-local metadata files are required.
