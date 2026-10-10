---
name: to-note
description: Save content as a Markdown note in the user's Obsidian vault. Use for /to-note, or when asked to save, record, or send something to Obsidian or the notes vault.
---

# To Note

Turn what the user hands over (text, a page's content, a research result, or the conversation's conclusions) into one note in their Obsidian vault. A vault is any folder that contains a `.obsidian/` directory.

## Steps

1. **Find the vault.** A vault path the user names wins. Otherwise run `python3 <this skill's folder>/scripts/find_vaults.py`. It prints `source<TAB>path` for each folder with `.obsidian/`, best first: `env` (`OBSIDIAN_VAULT_ROOT`, printed alone when set), `open` (open in Obsidian now), `recent`, then `found` by a shallow search of the home folder. Use the `env` line, else the only `open` line, else the only line; with several candidates left, ask once which vault, listing their paths.

   Done when: exactly one vault root, and it contains `.obsidian/`.

2. **Read the vault's rules.** Read `AGENTS.md` (or `CLAUDE.md`) at the vault root. Its placement, naming, frontmatter, tag, and language rules override every default below.

   Done when: each rule that bears on a new note is known.

3. **Place and name it.** Folder: the user's choice, else the vault rules, else Obsidian's default for new notes (`.obsidian/app.json`: `newFileFolderPath` when `newFileLocation` is `folder`), else the vault root; when that folder has its own `AGENTS.md`, its rules apply too. Title: the user's, else the content's main point in a few words, minus the characters Obsidian rejects in file names (`* " \ / < > : | ? # ^ [ ]`). Search the vault's note file names for that title first: on the same topic, read the note and extend it in place; on a different topic, append the date (`Title YYYY-MM-DD`), plus a number when that name is taken too.

   Done when: one vault-relative path, and every unrelated note stays as it was.

4. **Write it.** Obsidian Markdown with frontmatter: `created: YYYY-MM-DD`, `tags` (the vault's required tags first), and `source` when the content came from a URL, a file, or a conversation. Text the user hands over goes in verbatim; a conversation becomes a distilled note of its conclusions, key facts, links, and the open questions it left, with guesses marked as guesses. Link with `[[wikilinks]]` only to notes that exist. Credentials and absolute machine paths stay out of the vault.

   Done when: the note file exists in the vault.

5. **Verify and report.** Re-read the file: the frontmatter parses and the body says what was meant. Report the vault-relative path and the link `obsidian://open?vault=<vault folder name>&file=<path without .md>`, with both values URL-encoded.
