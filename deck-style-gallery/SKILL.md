---
name: deck-style-gallery
description: "Design a bilingual slide deck as HTML rendered to PNG: a gallery of about ten visual styles on slide one, the user picks, then the picked styles extend to every slide and ship as PPTX. Best on Claude Opus 5.5. Manual invocation only: use when the user says /deck-style-gallery or $deck-style-gallery."
disable-model-invocation: true
---

# Deck style gallery

**Model: run on Claude Opus 5.5 (`claude-opus-5-5`)**, the parent session and every designer agent. The first run was built there and its designs held up. In Codex or another harness, switch the session model to Opus 5.5 first (through your model gateway if the harness has no native Claude option).
模型：Opus 5.5 效果最好。在 Codex 里用时，先把模型切到 Opus 5.5 再开始。

Slides are HTML/CSS rendered to PNG, then wrapped into PPTX. Drawing shapes directly in python-pptx gives templated, sloppy slides; HTML gives real typography and layout. The scripts live in `scripts/`; copy them into a scratch workspace outside any repo.

Two rounds, two leading words: the **gallery** (slide one in many styles, so the user chooses by looking) and the **extension** (the chosen styles carried to every slide by the same designers).

## Steps

1. **Ground the brief.** Gather every slide's message and every number from its source of truth: repo docs, dated reports, the user's notes. Fill [`references/brief-template.md`](references/brief-template.md) as `BRIEF.md` for slide one. Done when each number names its source and its label (measured / estimate / in progress), and each claim you could not trace is dropped or put to the user as open.

2. **Set up the workspace.** Copy `scripts/` in. Run `node scripts/render.cjs --check`; set `PLAYWRIGHT_CORE` (module path) and `CHROMIUM_PATH` when Playwright is not installed globally. Python needs Pillow and python-pptx in a venv. Done when `--check` prints `ok`.

3. **Gallery round.** Choose about ten styles from [`references/styles.md`](references/styles.md); each reference image the user supplies replaces one. Spawn designer agents in the background, two styles each, all in one message. Each prompt: read `BRIEF.md`, the two style paragraphs (or image paths), output `<style>.html` and `.png`, render-read-fix at least twice. Record every agent ID: the extension resumes the same designers.

4. **Gallery review.** After all designers report: run `python3 scripts/vendor_fonts.py *.html`, re-render everything with `render.cjs`, tile with `contact_sheet.py` (four per sheet), and Read every sheet. Fix overflow, orphan CJK characters, fallback fonts, wrong labels. Present a table (style, look, visual idea, verdict) with a recommendation per use: projector, website, technical audience. Done when the user names the styles to extend: one, several, or all.

5. **Extension.** Fill the template again as `BRIEF-2-N.md` for the remaining slides. Resume each designer with SendMessage, keeping its context and tokens. Output names are `<style>-0N.html`, and each slide gets its own visual idea within the style's colors, fonts, header and footer.

6. **Consistency audit.** Every key figure carries the same label in every style: grep the HTML for it. A derived figure (a sum, a ratio, a combined speed) is an estimate unless it was measured directly. Collect the text designers report inventing (status words, button labels, illustrative positions) into a list for the user. Re-vendor, re-render, build one contact sheet per style, Read them all. Done when every sheet is read and every key figure's label agrees across styles.

7. **Package.** `build_pptx.py` makes one deck per style plus an all-styles deck. Each slide is a full-bleed image, so text edits go HTML → render → rebuild; say so on delivery. Add an index markdown: what each slide says, one line per style, sources, and open items. Upload or share only when the user asks; that publishes.

## Gotchas

- **Silent font fallback.** When the Google Fonts stylesheet fails, no face is registered, nothing errors, and Latin text renders in a CJK face. `vendor_fonts.py` moves Latin faces into local `fonts/`; `render.cjs` verifies every Latin face loaded and retries before it screenshots.
- **Designers fork.** A designer may hand its styles to its own sub-agents and report early; wait for its final report before reviewing.
- **Portable embeds.** A screenshot embedded by absolute path breaks when the folder moves: copy it beside the HTML and use a relative path.
- **Invented text.** Designers fill layouts with plausible wording. The brief makes them report it; the audit shows it to the user.
