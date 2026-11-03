# Brief template

Copy into the workspace as `BRIEF.md` (gallery round) and `BRIEF-2-N.md` (extend round), fill the angle-bracket fields, delete the comments. Designers read only this file and their style paragraph, so everything they may say lives here.

```markdown
# Slide <N> brief: <topic>

You are designing ONE 16:9 slide (1920×1080 CSS px) as a self-contained HTML file in a named visual
style. Other designers do other styles of the same slide; the user picks styles from the gallery and
the remaining slides follow them. Make the style unmistakable and finished, as a senior product
designer would.

## Product
<one paragraph: what it is, who it is for>. Footer line: `<brand · tagline>`.
Master line (optional, small): <CN> / <EN>.

## This slide (Chinese primary, English secondary; both appear)
- Kicker: <NN · topic>
- Headline: **<CN>** / **<EN>**
- Body: <CN> / <EN>
- Facts, each with its label (measured / estimate / in progress) and source:
  - <fact> — <label>, <source>
- Not claimable: <things that sound true but are unverified; say how to phrase them instead>
- Footnotes that must appear: <e.g. "*estimate, source pending">

Use only these facts. Every number on the slide carries its label.

## Hard constraints
- Everything inside 1920×1080: `html,body{margin:0;width:1920px;height:1080px;overflow:hidden}`.
- Fonts via Google Fonts <link> (Inter, Inter Tight, Geist, IBM Plex, JetBrains Mono, Newsreader,
  Source Serif 4, Fraunces, Lato, Noto Sans SC, Noto Serif SC). Chinese in a CJK face matching the
  style: serif styles use Noto Serif SC, sans styles use Noto Sans SC.
- Inline SVG and CSS only; local images only where this brief names them.
- Taste: one strong visual idea per slide (e.g. a bar drawn to scale), clear hierarchy, generous
  whitespace, tight tracking on display type, a consistent grid, real numbers in place of filler,
  flat color in place of purple-blue gradients, glows and emoji.
- Chinese lines end on whole phrases: `word-break: keep-all` or explicit <br>, no single orphan
  character on a line.
- Render with `node <workspace>/scripts/render.cjs <file>.html`, Read the PNG, fix overlap, clipping,
  wrapping and contrast, render again. At least two passes.

## Output
`<style>.html` and `<style>.png` (extend round: `<style>-0N.*`) in `<workspace>`. Write nowhere else.
Report: paths, one line on the visual idea, and every piece of text you wrote that this brief does
not contain (status words, button labels, illustrative positions, derived numbers).
```
