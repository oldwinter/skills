<!-- reviewed-through: 0000000 (never reviewed) -->
# Lessons from merged work

Agents write, review and merge most of this repository's changes. Each day the
merged commits are reviewed for what had to be fixed again, what should not have
merged and what was verified too thinly (the nightly-review loop). What we learn
is kept here. Read this before changing code.

Each lesson is a one-sentence rule, then the evidence that earned it. "Seen"
counts the distinct days a review found the lesson, not the commits. A lesson
seen on 3 or more separate days moves into [{{rulesPath}}]({{rulesPath}}), under
"Moved from LESSONS.md"; from then on every review checks it.

The first line above is `<!-- reviewed-through: <sha> (<date time>) -->`, the
last commit the review covered. The nightly review advances it when the window
is done, and does nothing while it is under about twenty hours old.

## Reading the report

*(Lessons about reproducing what a user reported: their platform, their version,
their data, before calling a report unreproducible or fixed.)*

## Fix the class, not the sample

*(Lessons about a fix that stopped at the first surface: the sibling callers, the
other modes, the other entry points that share the mechanism.)*

## Dependencies and builds

*(Lessons about a change that had to build everywhere it ships.)*

## Verification

*(Lessons about evidence: the test that fails without the change, what was run
and what was not run, the checks that were listed but never executed.)*

## Moved to the rules

Lessons promoted into `{{rulesPath}}` after being seen on 3 or more days. The
rule lives there; this table is the ledger.

| Lesson | Promoted on | Where it lives now |
| --- | --- | --- |
| *(none yet)* | | |

## Format

```markdown
**<one-sentence rule>**
- <sha> (#PR): <what went wrong and what it cost>. Fixed in <sha>, when a later
  commit fixed it.
- Done right: <sha> (#N) <what it did>.
- Seen Nx (YYYY-MM-DD, YYYY-MM-DD).
```

- No evidence, no lesson. A lesson is general enough to recur and specific enough
  that a reviewer can check it.
- Add a dated paragraph under the intro for each review window: the window, how
  many commits, and in a sentence or two what went wrong.
- Keep this file lean: it is loaded into every session. Once a lesson is
  promoted, trim evidence older than about two weeks to the most telling
  example.
- In a public repository, never include user counts, payment data, user ids or
  email addresses.
