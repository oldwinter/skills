---
name: vault-moc
description: Build or refresh Markdown MOC (map of content) index notes inside an existing Obsidian vault, including topic maps that connect an existing set of notes, dated summary maps such as yearly or project-span overviews, and deeper indexes under a hub note. Finds the vault by its .obsidian folder, reads the vault's own placement, frontmatter and linking rules, inventories candidate notes with their real wikilinks and backlinks as evidence, then writes the MOC with a dated scope line and source-note links. Use for /vault-moc, make a MOC for X, map out what I have on X, index these notes, create the 2026 summary note, or refresh this MOC. Not for saving one note (to-note), Canvas maps (canvas-atlas), or editing Obsidian syntax (obsidian-markdown).
---

# Vault MOC

A MOC is a Markdown note whose job is navigation: a reader lands on it, understands the shape of a topic, and reaches the real notes in one click. Build MOCs over a vault that already contains the notes. Link evidence comes from the vault, not from imagination.

## Scope

Reach for this when the request names a MOC, map, index, dashboard, or summary over notes that already exist in an Obsidian vault.

In scope: topic MOCs, dashboard MOCs, dated summary MOCs (year, quarter, project span), folder or project index notes, and refreshing an existing MOC.

Out of scope: saving one new note (`to-note`), Canvas or graph deliverables (`canvas-atlas`), Obsidian syntax questions (`obsidian-markdown`).

Defaults: the user's language and vault language win. One MOC per request. A MOC is an index; do not turn it into a second copy of the notes.

## Completion contract

Done when all of these hold:

1. Every target MOC file exists at a vault-relative path inside the found vault.
2. Every wikilink in those files resolves to an existing note path, alias, or heading; unresolved candidates are listed in the report, never guessed into the MOC.
3. Each MOC carries a dated scope line naming the topic, the covered date range, and the cutoff date of the inventory.
4. The report records the scope decision, the notes inventoried, the links verified, the files written or updated, and the gaps left.
5. No note outside the target MOC set was created, modified, deleted, or moved.

## Steps

1. **Find the vault.** A path the user names wins. Otherwise use `OBSIDIAN_VAULT_ROOT` when it contains a `.obsidian/` folder. Otherwise read Obsidian's own vault registry (`obsidian.json` in the platform app-data folder) and prefer the vault currently open, then the most recently opened. Otherwise do one shallow search of the home folder and take `.obsidian/` folders found near the current project. With several candidates left, ask once, listing their paths.

   Done when: exactly one vault root, and it contains `.obsidian/`.

2. **Read the vault's rules.** Read `AGENTS.md` or `CLAUDE.md` at the vault root, then the same name in the nearest folder that will receive the MOC. Placement, naming, frontmatter, tag, link-style, and language rules override every default below.

   Done when: every rule that bears on the MOC is known and quoted into the working notes.

3. **Inventory notes and link evidence.** Search the vault by the topic's terms, tags, and plausible folders. For each candidate record: vault-relative path, title, one-line claim taken from the note itself, inbound and outbound wikilinks, and dates. Prefer notes with incoming links and recent edits; an orphan note is not automatically out of scope, but mark it as orphaned. Read enough of each note to write its one-line claim; do not read the whole vault when search can narrow it.

   Done when: a candidate table exists where every row has a path and at least one piece of link or tag evidence.

4. **Propose the MOC set and structure.** Default to one MOC. Write more than one only when the user asked for separate topics or the scope is genuinely split; cap the set at three and say why. Present: target paths, heading outline, which notes fall under which heading, and the gaps.

   **CHECKPOINT** before writing more than one MOC, before overwriting an existing note, and whenever the target path is ambiguous. Continue only after the user confirms or the request already named the targets.

   Done when: target paths and outline are recorded, and the checkpoint outcome is explicit.

5. **Write or refresh.** Copy the frontmatter style of two or three existing notes in the target folder; when the vault has no convention, use `created` and optional `tags`. Open with a scope line:

   `Scope: <topic> — covers notes through <YYYY-MM-DD>; inventory cutoff <YYYY-MM-DD>`

   Keep the title as the reader's question or the topic name. Under each heading, place a wikilink per note plus one line saying why it belongs; link aliases when the note title differs from the reader-facing name. Close with a short Gaps section for terms that had no note yet, written as candidate note titles, not as links. Refresh an existing MOC with the smallest edit that adds new notes and updates the scope line, preserving hand-written sections, ordering, and callouts.

   Done when: the file content is written and every included link was copied from inventory evidence rather than invented.

6. **Verify and report.** Resolve every wikilink target against the vault, including case, path, alias, and heading anchors. Re-read the written file. Report: vault-relative paths, notes inventoried, links verified and unresolved, gaps, and any check left unverified.

   Done when: the verification result is recorded per link and the report names every file touched.

## Failure modes

| Trigger | First-line fix | Fallback |
|---|---|---|
| No vault found | Ask for the vault path; check `OBSIDIAN_VAULT_ROOT` again | Draft the MOC in a scratch file and stop before writing into any vault |
| Several candidate vaults | Prefer a named path, then the open vault, then the newest | Ask once and list the candidates; do not pick silently |
| Vault too large to inventory fully | Narrow by search terms, tags, and folder; record the query used | State the sampling limit and the unsearched folders in the report |
| Target MOC already exists | Refresh with the smallest edit and keep manual content | Ask when the existing note's purpose looks different |
| Broken or ambiguous link | Leave the note out of the MOC and record it as unresolved with the reason | Ask which title the user means; never invent a target |
| Obsidian is not running or unavailable | Verify statically against vault files | Report static verification only; do not claim a rendered check |
| Date range unclear | Use the inventory cutoff only, and name the missing bound | Ask once for the intended span |

## Checkpoints

- **CHECKPOINT** before creating or overwriting more than one note.
- **CHECKPOINT** before deleting, moving, or renaming anything. Default is to leave the existing note structure untouched; a confirmed delete or move needs a recorded rollback path.
- **CHECKPOINT** before a MOC set larger than three, with the reason for each extra note.

## Counter-examples and blacklist

- Fabricating wikilinks, note titles, or aliases to fill a section.
- Rewriting, reorganizing, or deleting the user's prose in an existing MOC.
- Dumping raw note bodies into the MOC instead of linking to them.
- Creating dozens of thin MOCs; one navigable MOC beats ten empty hubs.
- Moving or renaming notes to make the MOC read better.
- Writing absolute machine paths, credentials, API keys, or private hostnames into the vault.
- Claiming links were verified when only the text was written.
- Treating a folder listing as the MOC structure; the reader's questions, not the filesystem, set the headings.

## Notes

- Backlinks are the strongest evidence for inclusion; order by how many paths reach the note, then by recency.
- Keep each entry to one line; the note itself carries the detail.
- MOC titles usually stay stable across refreshes, so inbound links keep resolving; record renamed MOCs in the report.
- Runtime-neutral: use whatever file search, read, and write tools the current harness offers; no Obsidian CLI or plugin is required for v1.
