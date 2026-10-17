# The Reply Desk

The human approval gate. Every outbound action a loop wants to take exists first
as a JSON card; the maintainer reads the cards, approves, edits or drops them,
and only an approved card can be posted. The desk is portable on purpose: cards
are files in the state directory, the CLI is Python 3 standard library, and the
page the maintainer reads is a static `index.html` that any browser can open.

`<kit-dir>` below is the directory containing this file's skill — the `loop-kit`
skill directory, wherever the suite was installed (`<repo>/.claude/skills/loop-kit`
for a Claude Code project, or `<repo>/loop-kit` when the skills are checked out
as siblings at the repository root). Every invocation is written against
`<kit-dir>`, so it works from wherever the suite lives.

## Where it lives

```
<stateDir>/                 from .loop/config.json, expanded with ~
  desk/
    <id>.json               one card per draft: the only writable card store
    index.html              rendered by `desk.py render`
    archive/                cards moved here by `desk.py gc`
  tick-<loop>.lock          tick lock, owned by loopkit.py
  github.json               triage cursor
  social.json               social cursor
  watch.json                the PRs the watcher follows
  watch-seen.json           watcher dedupe
```

`desk.py --state DIR` picks the directory directly. Without it, `desk.py` reads
`stateDir` from `<repo>/.loop/config.json` and appends `desk`; failing that it
uses `$LOOP_STATE/desk`. The state directory is never inside the repository.

## The config keys a loop reads

Everything project-specific is in `.loop/config.json`; `loopkit.py config` prints
the resolved file.

| Key | Read by | Meaning |
| --- | --- | --- |
| `repo` | every loop | `owner/name`, the scope of every outbound action. |
| `defaultBranch` | every loop | Branch a tick branches from and merges into. |
| `stateDir` | every loop | State, cards and locks. `~` is expanded; never in the repo. |
| `lessonsPath`, `rulesPath`, `agentsPath` | nightly review | The lessons file, the promoted rules and the marked agents block. |
| `verifyDoc`, `worktreeCmd`, `checks` | triage, social | How to verify, where to work, and what must pass before a PR is drafted. `checks` empty means ask the project, never "no checks needed". |
| `trustedLogins` | triage, social | Bot logins that may be treated as trusted reviewers. |
| `windowDays` | triage, nightly review | The shared lookback knob, in days. See below. |
| `desk` | every loop | `{"kind": "files"}` for this desk. |
| `loops` | the scheduler | Per-loop `interval` and `enabled`, plus loop-specific keys. |

`windowDays` is deliberately one number with one meaning read in two places:

- **`loop-triage-github` — the recent-issue window.** Only threads created within
  the last `windowDays` days are the loop's to triage; older ones are the
  maintainer's backlog, and a new comment does not move them into the window.
- **`loop-nightly-review` — the seed range and backfill cap.** When `LESSONS.md`
  is still fresh (`<!-- reviewed-through: 0000000 (never reviewed) -->`), the
  review seeds lessons from the last `windowDays` days of merged commits, and
  that same number caps how far back a later backfill may reach.

Both are the same intent — how far back this project treats a thread or a commit
as current — so the two skills cannot drift apart. A tick with no cursor yet
falls back to `windowDays` rather than to "everything".

## Card schema (v1)

```json
{
  "id": "pr-123",
  "kind": "issue",
  "repo": "owner/myapp",
  "number": 123,
  "where": null,
  "url": "https://github.com/owner/myapp/issues/123",
  "title": "short title",
  "author": "login",
  "lastComment": {"author": "login", "at": "2026-10-14T06:33:00Z", "text": "excerpt"},
  "verdict": "reply",
  "verdictLabel": "Answer",
  "summary": "one line",
  "decision": null,
  "fix": null,
  "sendWith": "next-tick",
  "then": null,
  "headSha": null,
  "newTitle": null,
  "draft": "the exact text to post",
  "edited": null,
  "note": "",
  "status": "pending",
  "staleReason": null,
  "order": 0,
  "createdAt": "2026-10-14T06:33:00Z",
  "sentAt": null,
  "sentUrl": null,
  "version": 1
}
```

| Field | Values and meaning |
| --- | --- |
| `id` | Stable per thread: `123`, `pr-123`, `social-<id>`; `<id>-2` for a follow-up after a sent card. |
| `kind` | `issue`, `pr`, `social`. |
| `where` | For social cards: `x`, `discord`, `reddit`, `github-issue`; `null` for GitHub threads. |
| `verdict` | `reply`, `close`, `merge`, `request-changes`, `retitle`. |
| `verdictLabel` | What the desk page shows instead of the raw verdict. |
| `decision` | What the maintainer must decide, or `null`. |
| `fix` | `{"branch", "commit", "run": [], "notRun": []}` or `null`. |
| `sendWith` | `next-tick` (just post it) or `fix-pr` (push the branch and open the pull request first). |
| `then` | `null`, `close` or `merge`. `merge` requires `headSha`. |
| `headSha` | The reviewed head a merge is pinned to. |
| `newTitle` | Retitle applied with the reply, or `null`. |
| `draft` | The exact text to post. |
| `edited` | The maintainer's replacement for `draft`; non-null wins. |
| `note` | The maintainer's feedback to the loop. |
| `status` | `pending`, `approved`, `sending`, `sent`, `stale`, `dropped`. |
| `staleReason` | Who or what moved the thread. |
| `order` | Sort order on the page. |
| `version` | Bumped by every write; the desk page shows it. |

Unknown fields survive a rewrite: `desk.py` updates the keys it owns and writes
the rest of the object back unchanged.

## CLI

```
python3 <kit-dir>/scripts/desk.py --state DIR <command> ...
  put --file FILE|- [--replace]          # one card object, or an array/JSONL of cards; refuses to
                                         # overwrite a card in approved/sending/sent unless --replace
  list [--status pending,approved] [--json]
  show ID
  approve ID [--edited-file FILE] [--note TEXT]
  drop ID [--reason TEXT]
  note ID TEXT
  claim ID [--stale-seconds N]           # approved|stale -> sending, atomic; exit 3 if not claimable
  sent ID --url URL
  stale ID --reason TEXT
  render                                 # writes <desk>/index.html
  gc [--older-than-days N]               # moves sent/dropped cards to archive/
```

`--state` defaults to `<config stateDir>/desk`, else `$LOOP_STATE/desk`; `--state DIR`
takes the desk directory itself. Card files are read with `utf-8-sig`, so a card
hand-edited in an editor that writes a byte-order mark still parses.

Exit codes: `0` ok, `2` usage or config error, `3` refused by state (already
sent, not approved, a live claim lock, a sent card that cannot go stale).

## The maintainer's review workflow

1. A tick drafts cards: `put` writes them `pending`, then `render` refreshes the
   page.
2. The maintainer opens `index.html`. Every card shows its thread, the last
   comment, what was run, and the exact draft.
3. The maintainer answers with the CLI:
   - `approve ID` — post it as drafted.
   - `approve ID --edited-file new.md` — post the maintainer's text instead; the
     difference between `draft` and `edited` is feedback.
   - `approve ID --note "shorter next time"` — approve and leave feedback.
   - `drop ID --reason "not worth it"` — never post it.
   - `note ID "..."` — feedback without deciding yet.
4. The next tick (or the five-minute send check) claims each approved card and
   posts it, then records `sent` with the comment URL.
5. `render` again: sent cards show what went out and where.
6. `gc` moves old `sent` and `dropped` cards into `archive/` so the desk stays
   readable.

## What the desk guarantees

- **No card in `approved`, `sending` or `sent` is overwritten by `put`.** A loop
  that wants a follow-up drafts a new card with a new id. The human's decision
  cannot be erased by the machine that asked for it.
- **`claim` is atomic and refuses a card that is not approved.** It takes an
  exclusive lock file, re-reads the card inside the lock, and refuses a second
  claim of a card already `sending`.
- **`sending` means a tick died mid-send.** The next tick reports it and never
  resends; a human decides what to do with it.
- **Every write is atomic.** Cards and the page are written to a sibling temp
  file and moved into place with `os.replace`, so a crash leaves the old file
  intact rather than a half-written one.
- **Every write bumps `version`.** Two writers cannot silently interleave: the
  later write is visible, and the number on the page changes.

## Adapters

The file desk is the reference implementation. A harness with a native approval
surface may replace the *presentation* with an adapter, but not the guarantees
above.

| Adapter | How it presents a card | What it must still guarantee |
| --- | --- | --- |
| Files (default, `"desk": {"kind": "files"}`) | `index.html` plus the CLI | The whole list above; no harness support needed. |
| Native approval UI | The harness's own approve/deny prompt or artifact page, fed from the same card JSON | The approval is written back as `status: approved` with a `version` bump before anything is posted; a prompt timeout is not approval. |
| GitHub label | A label on the thread (for example `loop-approved`) as the approval signal | A human applied it; the loop re-reads it immediately before posting; the label is removed or changed after `sent` so a stale label cannot re-approve a new draft. |
| Chat approval | A message in a maintainer-only channel, answered by the maintainer | The message names the card id and a hash of the draft text; only an exact-id reply counts; the bot's own messages never approve anything. |

Whatever the adapter, the rule does not move: nothing is posted unless a human
decision is recorded on the card first, and a card in `approved` is not
overwritten by the loop.

## Rendering

`desk.py render` writes a single self-contained `index.html` — no scripts, no
external assets — grouping cards as waiting, stale, approved, mid-send, sent and
dropped. Draft text is HTML-escaped, so a draft containing markup is shown, not
executed. The page is a view of the cards: deleting it loses nothing, and
`render` rebuilds it.

## Operating notes

- `list --json` is the machine-readable view; `show ID` prints one card.
- Keep card ids stable and human-readable; they are the audit trail.
- `gc --older-than-days N` uses `sentAt`, then `droppedAt`, then `createdAt`, and
  only ever moves cards that are `sent` or `dropped`.
- `loopkit.py doctor` checks that the desk renders by rendering into a throwaway
  file, so running it never replaces the `index.html` the maintainer is reading.
- `loopkit.py doctor` finds the sibling tick skills next to `<kit-dir>` (the
  directory `<kit-dir>` lives in: `<repo>/.claude/skills` once installed, the
  repository root in the skills library), never in the target repository. A
  `FAIL skill ...` row prints the install command for exactly what is missing.
- The desk never talks to the network. Posting is the loop's job, and it happens
  only between `claim` and `sent`.
