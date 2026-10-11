---
name: to-note
description: Save content as a Markdown note in the user's Obsidian vault. Use for /to-note, or when asked to save, record, or send something to Obsidian or the notes vault.
---

# To Note

Turn what the user hands over (text, a page's content, a research result, or the conversation's conclusions) into one findable note in their Obsidian vault: a later search surfaces it, and a later reader understands it without this conversation. A vault is any folder that contains a `.obsidian/` directory.

## Steps

1. **Find the vault.** A vault path the user names wins. Otherwise run `python3 <this skill's folder>/scripts/find_vaults.py`. It prints `source<TAB>path` for each folder with `.obsidian/`, best first: `env` (`OBSIDIAN_VAULT_ROOT`, printed alone when set), `open` (open in Obsidian now), `recent`, then `found` by a shallow search of the home folder. Use the `env` line, else the only `open` line, else the only line; with several candidates left, ask once which vault, listing their paths.

   Done when: exactly one vault root, and it contains `.obsidian/`.

2. **Read the vault's rules.** Read `AGENTS.md` (or `CLAUDE.md`) at the vault root. Its placement, naming, frontmatter, tag, and language rules override every default below.

   Done when: each rule that bears on a new note is known.

3. **Place and name it.** A note the user names is the target: extend it. Otherwise, folder: the user's choice, else the vault rules, else Obsidian's default for new notes (`.obsidian/app.json`: `newFileFolderPath` when `newFileLocation` is `folder`), else the vault root; when that folder has its own `AGENTS.md`, its rules apply too. When the rules leave two or three folders equally plausible, ask once, offering them. Title: the user's, else the content's main point in a few words, minus the characters Obsidian rejects in file names (`* " \ / < > : | ? # ^ [ ]`). Search the vault's note file names for that title or a near-same one first: when the new material fits under that note's title, read the note and extend it; otherwise append the date (`Title YYYY-MM-DD`), plus a number when that name is taken too. Extending makes the smallest edit that adds the new material in the note's own layout, keeps its frontmatter, and updates its modified-date property (such as `date modified` or `updated`) when it has one.

   Done when: one vault-relative path, and every unrelated note stays as it was.

4. **Write it.** For a new note: frontmatter in the property style of the folder's existing notes (check two or three of them), or, in an empty folder, `created: YYYY-MM-DD`, `tags` (the vault's required tags first), and `source` when the content came from a URL, a file, or a conversation. Open with a one-sentence summary, written in the language the vault's notes use. The user's own text stays verbatim, even when it is research. Anything else becomes a distilled note shaped by its kind, with a section only where there is content:
   - analysis or research: key points, facts, judgments, the open questions it left, and sources, keeping facts apart from judgments and marking guesses as guesses;
   - a process or session: background, steps, result, and next steps;
   - a single idea: a one-line definition and its key point.

   Link with `[[wikilinks]]` the existing notes the content directly mentions. Credentials, raw logs, and absolute machine paths stay out of the vault; summarize what matters from them.

   Done when: the note file exists in the vault.

5. **Verify and report.** Re-read the file: the frontmatter parses and the body says what was meant. Report the vault-relative path, the link `obsidian://open?vault=<vault folder name>&file=<path without .md>` with both values percent-encoded (`%20` for a space, `%2F` for `/`), and each choice made for the user (folder, title, or merging into an existing note).
