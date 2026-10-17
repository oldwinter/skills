## Maintenance loops

Four agent loops run against this repository. One tick does a slice of work and
stops; a scheduler starts the next tick. Nothing they do reaches the network
without a card approved on the Reply Desk by a human.

| Loop | What one tick does |
| --- | --- |
| `loop-triage-github` | Triages recent issues, fixes what is worth fixing, follows the owner's own PRs to merge, drafts every outbound action. |
| `loop-watch-social` | Reads community feedback, filters it with a cheap model first, fixes what matters, drafts replies. |
| `loop-nightly-review` | Reviews the merged commits, writes lessons, promotes repeated ones into the rules, proposes one cleanup. |

- Configuration: `.loop/config.json` in this repository. State and Reply Desk
  cards live in `{{stateDir}}`, never inside the repository.
- Lessons: read [{{lessonsPath}}]({{lessonsPath}}) before changing code. What
  recent merged work got wrong, and the rule that would have caught it.
- Acceptance rules: [{{rulesPath}}]({{rulesPath}}).
- Schedule a tick with one line per enabled loop; the intervals are in
  `.loop/config.json`, and `<kit-dir>/references/harnesses.md` has the scheduler
  syntax for each harness.
- Check the install with `python3 <kit-dir>/scripts/loopkit.py doctor`.
