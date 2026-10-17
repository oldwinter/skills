# The lessons file

`lessonsPath` (default `LESSONS.md`) is the ratchet. Each review adds what the merged work got wrong, and a lesson seen on three or more distinct days becomes a rule in `rulesPath`. The file is read at the start of every session in the project, so it is kept short on purpose. This reference is the shape the review writes and the counting it obeys; it matches the file `loopkit.py init` writes from `<kit-dir>/templates/LESSONS.md` (`<kit-dir>` is the `loop-kit` skill directory, the sibling of this skill's directory; `init` substitutes `{{lessonsPath}}` and `{{rulesPath}}`).

## Layout

```markdown
<!-- reviewed-through: <sha> (<date time>) -->
# Lessons from merged work

<One paragraph: what this file is, that it is read before changing code, and that
each lesson is a one-sentence rule followed by its evidence.>

<One paragraph: "Seen" counts the distinct days a review found the lesson, not the
commits; a lesson seen on 3 or more separate days moves into <rulesPath>, under
"Moved from LESSONS.md"; from then on every review checks it.>

<One paragraph: the first line is the reviewed-through cursor, the last commit the
review covered; the review advances it when the window is done.>

<One dated paragraph per review, oldest first: the range, the number of commits,
and in a sentence or two what went wrong.>

## <section>

**<one-sentence rule>**
- <sha> (#PR): <what went wrong and what it cost>. Fixed in <sha>, when a later
  commit fixed it.
- Done right: <sha> (#N) <what it did>.
- Seen N× (YYYY-MM-DD, YYYY-MM-DD).

## Moved to the rules

Lessons promoted into `<rulesPath>` after being seen on 3 or more days. The rule
lives there; this table is the ledger.

| Lesson | Promoted on | Where it lives now |
| --- | --- | --- |
| **<rule>** | <YYYY-MM-DD> | `<rulesPath>`, "Moved from LESSONS.md" |

## Format

<The reminder the template ships: the lesson shape, "no evidence, no lesson",
one dated paragraph per window, keep the file lean, and the public-repo rule.>
```

- The first line is the cursor. Nothing goes above it, not even a blank line; the review reads it as the start of its window. The template ships it as `<!-- reviewed-through: 0000000 (never reviewed) -->`; `0000000` is the sentinel for "no review has run", and the first review falls back to the configured `windowDays` for its range.
- The date is the commit's own date, written `YYYY-MM-DD HH:MM ±HHMM`, or `never reviewed` before the first tick.
- The template ships four starter sections — "Reading the report", "Fix the class, not the sample", "Dependencies and builds", "Verification" — and a `## Format` reminder at the end. A section names a class of mistake, not a component or a commit: add one when two lessons share a class, never one per commit.
- A lesson is a bold one-sentence rule, then its evidence. If it cannot be stated as a rule a reviewer can check, it belongs in the tick report as a note, not in this file.
- Evidence bullets carry a sha and a PR number. `Done right:` bullets record the positive model, because the loop must learn what to do as well as what not to do. `Seen` is the last bullet.
- `## Moved to the rules` holds one ledger row per promoted rule, and `## Format` stays last.

## Counting `Seen`

`Seen N×` counts **distinct days on which a review found the lesson** — not commits, not PRs, not occurrences, and not the days the bad code was written. The template's reminder writes the count as `Nx`; write `×`.

- Two commits on one day that show one lesson: `Seen 1× (2026-10-04)`.
- The same lesson found again on another day: `Seen 2× (2026-10-04, 2026-10-09)`; the days list is ascending, and a day already listed does not change the count.
- A lesson first recorded today: `Seen 1× (<today>)`.
- A lesson that came from the desk (a maintainer correction: a non-empty `note`, an `edited` that differs from `draft`, or a dropped card) counts the same way, and its evidence names the card id and what the maintainer changed.
- A promoted rule that the window violates again is evidence for the rule and for its lesson's day count, not a new lesson.

## Promotion at three days

- At three or more distinct days the lesson moves. Add the rule to `rulesPath` as a row of its `## Moved from LESSONS.md` table — `| Rule | What a reviewer looks at |`, where the second cell carries the evidence that earned the rule — then add one row to the `## Moved to the rules` ledger in `lessonsPath` with the rule, the promotion date and where it now lives.
- Promotion happens in the same lessons commit, and the tick report names the rule and the days that promoted it.
- Keep the lesson body in `lessonsPath` (trimmed): the days are the evidence that it earned a rule, and the detailed evidence stays with the lesson.
- From then on, every review — this loop and the triage loop — checks the rule against the window.
- Never promote on a count of commits, on one bad day repeated, or on a lesson that is still changing shape.

## Seeding a fresh file

A file that is still the template (`0000000 (never reviewed)`, no dated paragraph) is seeded from a retrospective of past merged work, not left to start empty. The PR this suite ports seeded from 10 days of commits and promoted three lessons on its first run.

1. Pick the seed range: the most recent `windowDays` of merged commits. Say in the report when older history was not seeded.
2. Bucket it exactly as a tick does (rework / shouldn't have merged / verified too thinly / done right) and write the lessons with their evidence.
3. Start every lesson found in the seed at `Seen 1× (<the day it was found>)`. A pattern seen on three distinct days inside the seeded range is promoted on day one, with its evidence.
4. Write the dated intro paragraph — the range, the commit count, and in a sentence or two what went wrong — and set `reviewed-through` to the newest commit reviewed.
5. Ship the seed as one PR, approved like any other card. Afterwards the normal tick window takes over.

## Trimming

`lessonsPath` is loaded into every session, so it stays lean:

- Once a lesson is promoted, evidence older than about two weeks is cut to the most telling example; the rest is deleted, and the days list stays.
- An unpromoted lesson keeps its evidence: it is still counting days toward a rule.
- The `## Moved to the rules` ledger keeps one row per rule indefinitely; the detail lives in `rulesPath`.
- A lesson that never recurs and never promotes can be folded into a promoted rule it belongs to, or dropped with its days named in the tick report. Never drop one silently.

## Public-repo safety

- Never write user counts, payment data, user ids or emails into `lessonsPath` or `rulesPath`.
- Credit a person by the public login or handle they posted under; a ticket or PR number is fine, an account id is not.
- The same rule applies to the dated paragraph, the evidence bullets and the promoted rules.

## Wiring

- The file only ratchets if later sessions read it: `loopkit.py init` adds the pointer to `agentsPath` inside its own marked block. If that pointer is missing, the review reports it and does not hand-edit the block.
- `rulesPath` is read on every review in this loop and in the triage loop, so a promoted rule is checked, not archived.
