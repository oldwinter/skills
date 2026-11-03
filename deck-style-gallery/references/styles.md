# Style catalog

The ten styles of the first run, written as the designer prompts that produced them. Paste a style's paragraph into a designer's prompt as-is. Four imitate a public product site: the designer studies the live site (`curl -sL <url>` or WebFetch) for palette, radii and type scale and never copies its logo or copy text. Six came from reference images the user supplied; without those images, the paragraph alone carries the style.

When the user brings reference images, each image becomes one style: the designer Reads the image and follows its layout grammar, palette and type pairing, adapted to 16:9.

| slug | origin | Best for |
|---|---|---|
| `raycast` | raycast.com | developer audience, product feel |
| `linear` | linear.app | website, restrained premium |
| `herdr-tui` | herdr.dev/tui | CLI products |
| `notion` | notion.com | friendly docs-style, low drama |
| `swiss-bold` | reference image | projector, legible from the back row |
| `blueprint` | reference image | technical audience, most distinctive |
| `health-report` | reference image | storytelling (diagnosis, then prescription); small type |
| `lab-notes` | reference image | opinionated editorial; dense |
| `stepflow` | reference image | explaining a mechanism step by step |
| `calm-green` | reference image | quiet, trustworthy |

## raycast

The look of raycast.com: near-black background, Raycast's coral-red accent used sparingly, a macOS command-palette window as the central motif (rounded window, search field, result rows, keycap chips such as ⌘ K), Inter, 1px hairline borders in low-alpha white, crisp product-UI density. Render the proof as a palette result list, e.g. the search field holds the slide's claim and the result rows are its evidence. Headline on the left, palette on the right.

## linear

The look of linear.app: very dark (#08090A-ish) background, large tight display headline with Linear's subtle white-to-gray text treatment, muted gray body, precise hairline-bordered panels that read as real app UI (an issue or status panel, an allocation panel), small monospace metadata, one restrained accent.

## herdr-tui

The look of herdr.dev/tui: study its CSS first. The slide is a terminal UI: monospace panes with box-drawing structure, a status line, block-cell meters (draw cells and brackets in CSS; web subsets of mono fonts often lack box-drawing glyphs and the fallback breaks alignment). Pair the mono face with Noto Sans SC so Chinese stays readable. Dark grid background, one pastel accent.

## notion

A well-made Notion page: white page, warm near-black text (#37352F), Notion's system-sans heading hierarchy, breadcrumb, a gray callout block, a small inline database or chart view with property pills (Measured / Estimate / In evaluation), toggle-list arrows, inline code chips, light dividers, calm whitespace. Optionally a simple black line illustration in SVG as the page icon.

## swiss-bold

Off-white paper, heavy black grotesk display type (Inter Tight / Inter at 800–900 with Noto Sans SC Black), one red accent, huge numerals, vertical or horizontal bar gauges drawn to scale, thin black rules, a black footer band carrying baseline facts, small measured / partly measured / estimated pill badges.

## blueprint

Navy engineering-drawing grid, a drawing-sheet header (DWG no., SCALE, REV), a central technical diagram drawn to scale with numbered callouts on leader lines, dimension lines, a big stat row, and a title-block table along the bottom (TITLE, PROJECT, SOURCE, NOTE, DATE, SHEET). Mono for labels, bold sans for headlines, one yellow highlight for measured numbers.

## health-report

A clinical lab-report sheet on warm paper: header with report number and barcode, a meta row (device, host, date, mode), ITEM / RESULT / REFERENCE / STATUS tables with colored status words, a framed DIAGNOSIS box holding the headline, a red round rubber stamp. Frame each slide as a document type (report, lab panel, prescription, monitoring chart). Serif headline (Newsreader or Source Serif with Noto Serif SC), sans body, mono values.

## lab-notes

Cream magazine editorial: masthead with a double rule ("LAB NOTES · ISSUE 01 · <MONTH YEAR>"), big serif headline with a rust-red second line, drop cap, small-caps section labels, numbered columns pairing a struck-through generic "BENCHMARK" line with a "WE FOUND" line, big serif numerals, a dark pull-quote band. Newsreader / Source Serif 4 with Noto Serif SC; Lato or Inter for small labels. The struck-through lines stay generic phrases, never attributed claims.

## stepflow

Light gray-blue page, big serif headline with one blue-highlighted phrase, legend pills at the top, numbered step cards with tinted header strips (blue / orange / purple), block-grid bars where one block is one unit, arrow connectors with pill labels, and a dark green result card at the end with a terminal command chip. Flow runs left to right on 16:9.

## calm-green

Warm off-white, a large serif headline whose second line is deep green, a small letter-spaced kicker, a numbered vertical timeline with outlined circle markers (last one filled), a right column of claims with circled check marks (dashed circle for in-progress items), mono code chips, a quiet footer with a small shield mark carrying the source line. Source Serif 4 / Newsreader with Noto Serif SC; Lato / Inter with Noto Sans SC.
