---
name: obsidian-note-capture
description: Capture documents, notes, research processes, conversation summaries, and deliverables into the user's Obsidian vault oldwinter-notes. Use when the user asks to save, write, archive, extract, distill, or record content into Obsidian, oldwinter-notes, a note vault, a digital garden, or a markdown knowledge base.
---

# Obsidian Note Capture

## Overview

Use this skill to turn working material into durable Obsidian notes in the user's primary vault.

Resolve the vault root at runtime. Do not keep a device-specific absolute path in this shared skill.

Use this precedence:

1. A vault path explicitly provided by the user.
2. The vault derived from `OBSIDIAN_AGENT_ROOT` by removing the `/_system/agents` suffix.
3. `OBSIDIAN_VAULT_ROOT`.
4. In the `general-tasks` workspace, read the device ID from `local/device-name`, then read the vault root from `local/<device-id>/obsidian-vault-root.txt`.
5. If none resolves to an existing vault, ask one concise path question instead of reusing a path from another device.

This skill is about note capture and knowledge preservation. For raw Obsidian syntax details, combine it with `obsidian-markdown`. For batch CLI operations, combine it with `obsidian-cli-automation`.

## Workflow

1. Identify the capture intent.
   - Preserve source documents, research traces, conversation summaries, implementation notes, or final deliverables.
   - Keep Chinese as the default language unless the source or user asks otherwise.
2. Resolve the target path.
   - If the user specifies a file or directory, use it.
   - Otherwise resolve the vault root using the precedence above.
   - If the user explicitly says root directory, write under the vault root.
   - Otherwise route by reading vault rules and nearby directory conventions.
   - If routing is still ambiguous, ask one concise path question before writing.
3. Read applicable instructions before mutation.
   - Always read the vault root `AGENTS.md`.
   - If writing under a subdirectory, read the nearest subdirectory `AGENTS.md` files that apply.
   - Load `references/oldwinter-notes-rules.md` for the detailed capture contract.
4. Inspect existing notes before creating duplicates.
   - Search for same or near-same title.
   - If updating an existing note, read it first and make a local edit.
   - If a same-name note is the same topic, merge or append.
   - If the same name is a different topic, create `Title - YYYY-MM-DD.md`.
5. Write a valid Obsidian Markdown note.
   - Include frontmatter for new Markdown notes.
   - Use Obsidian wikilinks only when they are useful and do not invent fake links casually.
   - Do not write local absolute paths into tracked Markdown unless the user explicitly wants the path recorded.
6. Verify.
   - Confirm the target file exists.
   - Re-read the frontmatter and first section.
   - Report the final vault-relative path.

## Note Shape

New Markdown notes must include:

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

Prefer this body structure unless the target directory has a stronger convention:

```markdown
# Note Title

One-sentence definition or summary.

## 核心判断

- ...

## 事实

- ...

## 判断

- ...

## 待确认

- ...
```

For short notes, collapse sections and keep only what helps future retrieval.

## Routing Defaults

- Root directory: only when explicitly requested or when the note is a top-level entry/document.
- `_system/`: stable operating context, memory, plans, tool notes, and agent collaboration infrastructure.
- `Atlas/LLM Wiki/`: source/query/concept/synthesis style compiled knowledge.
- `Calendar/`: daily notes, tasks, plans, and dated working material.
- `Cards/`: compact evergreen cards.
- `Clippings/` or `Sources/`: imported or clipped source material.
- Existing project or area folders: use when the note clearly belongs to an active folder and its local rules allow it.

When in doubt, prefer asking over silently widening the target.

## References

- `references/oldwinter-notes-rules.md`: Detailed oldwinter-notes capture rules, routing heuristics, and verification checklist.
