## Acceptance criteria

A change is merged only when it shows each of these. Say which were run and what
they printed, in the commit body or on the pull request. A check that was not run
is listed as not run, never left out.

1. **A test that fails without the change**, for a change in behavior. Put the old
   code back and run the new test: it must fail on an assertion that names the
   behavior. A type error or a skipped test does not count. Say which test and
   what it failed with, then restore the change and see it pass. A change with no
   behavior to test (docs, config, agent files) says how it was checked instead.
2. **The project's verification commands**, run on the change merged onto the
   current default branch. The commands live in `.loop/config.json` under
   `checks`; when that list is empty, ask the project which commands to run
   rather than assuming there are none.
3. **Real use on the reporter's surface**, when a report drove the change.
   Reproduce it the way they saw it, then see it fixed there. If that is not
   possible, say so, and do not tell users it works.
4. **UI changes** hold in every mode and form factor the project ships: themes,
   layout overrides, right-to-left, safe areas, and every new string through
   localization.

Merge only the head that was reviewed, after the last review pass is answered,
and record what was run at that head. A test that fails on the default branch is
a bug to fix now, in its own change; "fails the same way there" is not a
baseline.

Product decisions belong to the maintainer. A change that reverses one (a
behavior, a layout, a default the maintainer chose) is left for the maintainer,
however good its reason.

A commit body says how the change was verified and which test fails without it,
and credits the reporter by the public name they posted under, never an email or
an account id.

## Moved from LESSONS.md

Lessons seen on 3 or more distinct days, checked on every review. The nightly
review appends a row here when it promotes a lesson; the evidence stays in
`{{lessonsPath}}`.

| Rule | What a reviewer looks at |
| --- | --- |
| *(none yet)* | |
