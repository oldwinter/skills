# Porting notes

This suite ports the maintenance-loop work from `readest/readest` pull request
#6796, *chore(agent): maintenance loops with a Reply Desk, lessons and acceptance
rules*. That pull request is the only place in the suite that is allowed to talk
about it: every other file has to work for any repository, so nothing else names
a project, a machine or a state path.

## What the original did

One `.claude/skills/` directory per loop — `triage-github`, `watch-social`,
`nightly-review` — plus `.claude/rules/acceptance.md`, a root `LESSONS.md`, a
`watch-prs.py` event watcher, and a new section in `AGENTS.md`. Three `/loop`
sessions ran in parallel. Every outbound action was drafted to a **Reply Desk**:
a private hosted artifact page whose rows were read and written through an
artifact-data tool. State lived in a fixed directory under the maintainer's home,
and the repository, the state path and the worktree command were hardcoded in the
skill text.

## The mapping

| Original | This suite |
| --- | --- |
| One skill directory per loop, self-contained | `loop-kit` owns the shared runtime — config, state dir, desk, templates, `AGENTS.md` block, `doctor`, tick lock — and the three tick skills call it. |
| Reply Desk = a private hosted artifact page plus an artifact-data tool | Reply Desk = JSON cards in the state directory, a `desk.py` CLI, and a rendered static `index.html`. Adapters for a harness with a native approval UI are documented in [desk.md](desk.md), not required. |
| Repository and state path hardcoded (`readest/readest`, a fixed directory under `~`) | Everything comes from `.loop/config.json` in the target repository: `repo`, `stateDir`, `defaultBranch`, `lessonsPath`, `rulesPath`, `agentsPath`. `stateDir` is never inside the repository. |
| `pnpm worktree:new`, submodule rules, a design document, a platform matrix | A generic `worktreeCmd` template over `{project}`, `{branch}`, `{slug}`, a `checks` list, and a `verifyDoc` pointer. Project-specific rules live in the generated rules file, not in the skill. |
| A specific browser tool and a specific cheap model | Any browser tool and any cheap model. The portable part is the *filter-first* pattern: collect raw items to a file, have the cheap model keep only what matters, and act only on items whose id, URL and text match the collected file. |
| Claude Code's `/loop` and its monitor tool | A harness table: Claude Code, this harness's `schedule_create` and background jobs, cron, systemd, Windows Task Scheduler. See [harnesses.md](harnesses.md). |
| Skills as `.claude/skills/*` inside one application directory | Four installable skills in a skills repository, each with `SKILL.md` frontmatter and an `agents/openai.yaml`. |
| A `user_invocable: true` frontmatter key | `disable-model-invocation: true` with a manual-invocation clause in the description, which is what this repository's contract checker understands. |

## What we deliberately changed, and why

**The desk is files, not a hosted page.** The original desk was a private
artifact: it needed one specific harness, one specific account and a network
round trip to read a draft. Cards in the state directory plus a static page work
in every harness, survive a session restart, are diffable and reviewable, and
make the gate checkable by a test. The property that mattered — nothing is posted
without a recorded human approval — is enforced by the card state machine
instead of by the page: `put` refuses to overwrite an `approved`, `sending` or
`sent` card, `claim` refuses a card that is not approved, and `claim` is atomic.

**The approval gate is state, not presentation.** A hosted page can be edited by
the same agent that drafted the card. Files with a refusal rule cannot: the loop
literally cannot write over the human's decision without passing `--replace`, and
`--replace` is not something a tick has any reason to call.

**Config replaces hardcoding.** The original assumed one repository, one
maintainer and one package manager. Anything project-specific here is either a
config key or a generated template, so the suite installs into a Go service, a
Python CLI or a monorepo without editing skill text.

**`doctor` exists at all.** The original assumed its environment. A portable
suite has to answer "is this install complete" in one command, because the usual
failure is not a crash: it is a tick that silently does nothing because the
config, the lessons file or a sibling skill is missing.

**The tick lock is explicit.** Three loops in parallel sessions with a shared
state directory need one writer per loop. `loopkit.py lock` uses an exclusive
create and an age-based takeover, so a crashed tick does not block the loop
forever and a live tick is never doubled up.

**Cursors advance only at the end of a finished tick.** Same intent as the
original, but stated as an invariant in
[send-protocol.md](send-protocol.md): a crashed tick repeats its window instead
of skipping it.

**The event watcher is injectable.** `watch-prs.py` lives in the triage skill,
but its `gh` access goes through one function so the event logic can be tested
with a fake runner, with no network and no `gh` installed. The original was a
script that only ran for real.

## Hard-won recipes kept from the original

These were learned the expensive way upstream and are carried into the GitHub
loop's recipes file:

- Forge search takes dates, not timestamps: a full timestamp in the
  "updated since" filter silently matches nothing, so filter the results by
  timestamp locally instead.
- No `--slurp` in the CLI version in use; one page of 100 covers a pull request's
  runs, reviews and comments.
- Editing an issue or pull request through the high-level CLI can fail on a
  deprecated project field; the API patch works.
- One review bot reports as a commit status, not as a check run, so both
  endpoints have to be read.
- A merge is pinned to the reviewed head so the forge refuses it if the head
  moved.
- A review-bot login is matched on both login and `user.type == "Bot"`.

## What did not port

- The upstream contributor policy, block lists and platform matrix: those are
  product decisions for one project, and the suite only provides the rules file
  they belong in.
- Release naming and store submission: maintainer-only, and project-specific.
- The upstream package manager's worktree script: replaced by `worktreeCmd`.
