# oldwinter-notes Capture Rules

## Purpose

Use these rules when saving work into the user's Obsidian vault `oldwinter-notes`.

The goal is not to dump text. The goal is to create durable, findable notes that preserve context, decisions, and reusable knowledge.

## Required Preflight

Before writing:

1. Read the vault root `AGENTS.md`.
2. If the target path is inside a subdirectory, read the closest applicable `AGENTS.md`.
3. Search for an existing note with the same or similar title.
4. Decide whether the task is create, append, merge, or local edit.

Do not ask where files or rules are when the vault can answer it. Ask only when product intent or routing remains ambiguous after inspection.

## Vault Resolution

Resolve the vault root per device instead of storing an absolute default in this shared skill:

1. Use a vault path explicitly provided by the user.
2. Otherwise derive the vault root from `OBSIDIAN_AGENT_ROOT` by removing the `/_system/agents` suffix.
3. Otherwise use `OBSIDIAN_VAULT_ROOT` when set.
4. In the `general-tasks` workspace, read `local/device-name`, then read the first line of `local/<device-id>/obsidian-vault-root.txt`.
5. Confirm the resolved directory exists. If it cannot be resolved, ask one concise path question and do not guess from another device's path.

Report paths to the user as vault-relative paths unless an absolute path is necessary for a local file link.

## Routing Heuristics

Use the user's explicit target first.

If no target is provided:

- Use the vault root only for user-requested root notes, public entry notes, or one-off top-level documents.
- Use `_system/` for agent operating rules, memory, tool notes, plans, roadmaps, and durable collaboration infrastructure.
- Use `Atlas/LLM Wiki/` for compiled knowledge from sources, questions, concepts, and synthesis.
- Use `Calendar/Daily notes/` for day-bound logs and diary-like entries.
- Use `Calendar/Tasks/` for actionable task notes.
- Use `Cards/` for short evergreen cards with one clear idea.
- Use `Clippings/` or `Sources/` for imported source material or raw clippings.
- Use an existing project/area/resource folder when the subject clearly belongs there and local rules allow it.

If multiple routes are equally plausible, ask one concise question with 2 to 3 concrete path candidates.

## Frontmatter

For new Markdown notes, include at minimum:

```yaml
---
publish: false
date created: YYYY-MM-DD
date modified: YYYY-MM-DD
title: Note Title
tags:
  - AI生成
---
```

Follow local directory property conventions when a nearer `AGENTS.md` or nearby notes show a stronger schema.

When updating an existing note:

- Preserve existing frontmatter keys unless the edit directly requires changing them.
- Update `date modified` when that key exists.
- Add `AI生成` only if local conventions and the note's purpose make it appropriate.

## Body Structure

Prefer a note that starts with a useful one-sentence summary.

For analysis or research notes, use sections like:

```markdown
## 核心判断

## 事实

## 判断

## 待确认

## 来源与上下文
```

For process notes, use:

```markdown
## 背景

## 过程

## 结果

## 后续
```

For concise evergreen cards, use:

```markdown
一句定义。

## 核心判断

- ...
```

Keep the structure proportional. Do not create empty sections just to satisfy a template.

## Link Rules

- Prefer Obsidian wikilinks for stable concepts and existing notes.
- Before adding a wikilink to a specific note, verify that the note exists when feasible.
- Do not create noisy or speculative links.
- Do not manufacture fake backlinks just to make the note look connected.
- Use plain Markdown links for external URLs.

## Privacy and Path Rules

- Do not write local absolute paths into tracked Markdown unless the user explicitly asks to record the path.
- Do not copy secrets, tokens, private credentials, or irrelevant runtime state into the vault.
- Summarize sensitive operational details instead of pasting raw logs when a short note is enough.

## Conflict Handling

When the target file exists:

- Same topic: read the existing note, then merge or append in place.
- Different topic: create `Title - YYYY-MM-DD.md`.
- User requested update: make the smallest local edit that satisfies the request.

Avoid overwriting existing notes wholesale unless the user explicitly asked for replacement.

## Verification Checklist

Before reporting completion:

1. Confirm the file exists.
2. Re-read the frontmatter and first section.
3. Check that there are no unintended absolute local paths.
4. Check that requested title/path was honored.
5. Report the vault-relative path and any important assumptions.
