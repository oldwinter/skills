# Scheduling a tick

A tick is one bounded run of one loop skill. Something has to start it again:
that is the whole scheduler contract. This page gives the lines for the harnesses
in use, then the two things that are easy to forget — the five-minute send check
and re-arming the event watcher.

`<kit-dir>` below is the directory containing this file's skill — the `loop-kit`
skill directory, wherever the suite was installed (`<repo>/.claude/skills/loop-kit`
for a Claude Code project, or `<repo>/loop-kit` when the skills are checked out
as siblings at the repository root). Every invocation is written against
`<kit-dir>` so the lines work from wherever the suite lives.

`<suite-dir>` is the directory that holds all four skills — `<kit-dir>/..`, which
is `<repo>/.claude/skills` in an installed project and the repository root in the
skills library. The three tick skills are `<suite-dir>/loop-triage-github`,
`<suite-dir>/loop-watch-social` and `<suite-dir>/loop-nightly-review`.

## The lines `loopkit.py init` prints

Intervals come from `.loop/config.json`; the defaults are `30m` for
`triage-github`, `60m` for `watch-social` and `24h` for `nightly-review`. Only
enabled loops get a tick line.

```
4-59/5 * * * *   # desk send check: post approved cards within five minutes
*/30 * * * *     # triage-github tick
0 * * * *        # watch-social tick
0 3 * * *        # nightly-review tick
```

The send check deliberately runs off the tick's minutes: on the hour and the half
hour a tick is already starting, and there is no point in two processes racing
for the same approved cards. `desk.py claim` is atomic, so a race would be safe —
just wasteful.

## Claude Code

Claude Code's `/loop` re-runs a slash command on an interval, in the session it
was started in:

```
/loop 30m /triage-github
/loop 60m /watch-social
/loop 24h /nightly-review
```

Each loop needs its own session; run them in parallel. The event watcher is a
long-running command, so it goes in the Monitor tool rather than in `/loop`:

```
python3 <suite-dir>/loop-triage-github/scripts/watch-prs.py
# Monitor: description "loop PRs: CI, reviews, merges", timeout_ms 1800000
```

When the monitor expires, or a tick finds none running, arm it again. The
watcher's stdout lines wake the loop; treat a line as a reason to run the
relevant steps for that pull request only.

## This harness

`schedule_create` gives a session its own reminders, and a background job runs a
command without blocking:

```
schedule_create: cron "4-59/5 * * * *"  prompt "Run the desk send check: post approved cards."
schedule_create: cron "*/30 * * * *"    prompt "Run one loop-triage-github tick."
schedule_create: cron "0 3 * * *"       prompt "Run one loop-nightly-review tick."
```

Run the watcher as a background job and keep its job id: when it exits, start it
again. A scheduled prompt in a session that is not running is delivered when the
session resumes, so a tick can be late; the loops are written to repeat work
rather than skip it.

## cron (POSIX)

```cron
4-59/5 * * * * cd <repo> && python3 <kit-dir>/scripts/loopkit.py lock acquire --name send-check && <agent> run <kit-dir>/references/send-protocol.md#0-send-what-was-approved
*/30 * * * *   cd <repo> && <agent> run loop-triage-github
0 * * * *      cd <repo> && <agent> run loop-watch-social
0 3 * * *      cd <repo> && <agent> run loop-nightly-review
```

Replace `<agent>` with the command that runs one unattended agent turn for the
harness in use. Whatever starts a tick must also release the lock when the tick
ends; the agent turn is expected to call `loopkit.py lock release --name <loop>`
last. A tick that dies leaves the lock behind, and the next acquire takes over
after `--stale-seconds` (default 7200) while saying so in the log.

## systemd

A user timer per loop, plus a service that runs one tick:

```ini
# ~/.config/systemd/user/loop-triage.service
[Service]
Type=oneshot
WorkingDirectory=%h/<repo>
ExecStart=/usr/bin/env python3 <kit-dir>/scripts/loopkit.py lock acquire --name triage-github
ExecStart=/usr/bin/env <agent> run loop-triage-github
ExecStartPost=/usr/bin/env python3 <kit-dir>/scripts/loopkit.py lock release --name triage-github
```

```ini
# ~/.config/systemd/user/loop-triage.timer
[Timer]
OnCalendar=*:0/30
Persistent=true
[Install]
WantedBy=timers.target
```

`Persistent=true` is what makes a missed tick run once after the machine wakes,
which matches the suite's "repeat rather than skip" rule.

Write `<kit-dir>` as an absolute path, or as one relative to `WorkingDirectory`
(for a Claude Code project that is `.claude/skills/loop-kit`). Never prefix it
with `%h/<repo>/`: `<kit-dir>` already includes wherever the suite was installed.

## Windows Task Scheduler

```powershell
$action = New-ScheduledTaskAction -Execute "python3" `
  -Argument "<kit-dir>/scripts/loopkit.py lock acquire --name triage-github" `
  -WorkingDirectory "<repo>"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
  -RepetitionInterval (New-TimeSpan -Minutes 30)
Register-ScheduledTask -TaskName "loop-triage-github" -Action $action -Trigger $trigger
```

Use `-RepetitionInterval (New-TimeSpan -Minutes 5)` for the send check, and
`-RepetitionInterval (New-TimeSpan -Days 1)` for the nightly review. Task
Scheduler does not run a task while the previous one is still running unless the
task's multiple-instances policy says so; leave it at the default, which is
"do not start a new instance", and let the tick lock cover the rest.

## The five-minute send check

The watcher only sees the forge. An approval on the Reply Desk is invisible to
it, so a second, light job picks approvals up:

1. List cards in `approved` and `sending`. If there are none, stop — this job
   does no work most of the time.
2. Otherwise run only "Send what was approved" for those cards, under the same
   trust boundary, then stop.

That keeps the wait after an approval to about five minutes without running a
full tick. The send check is also the right place to notice a card stuck in
`sending`: report it, and leave the decision to the maintainer.

## Re-arming the watcher

- Keep exactly one watcher per repository. Two watchers double-report events and
  fight over `watch-seen.json`.
- The watcher reads `watch.json` on every pass, so a tick that adds or removes a
  pull request does not need to restart it.
- When the watcher's monitor expires, or a tick sees no watcher running, start it
  again. Its dedupe file means it neither repeats events nor misses the ones that
  happened while it was down; the first time it sees a pull request it records
  the current reviews and comments without reporting them.
- A `WATCH_ERROR` line is a failed read, not quiet: look into it. A watcher that
  cannot read the owner's login exits `1` rather than mislabelling every pull
  request as foreign.

## Choosing an interval

- The GitHub loop wants the shortest interval: `30m` keeps a reply close to the
  report, and the watcher covers the gaps that matter.
- The social loop is `60m` by default; its sources are rate-limited and the
  cheap-model filter is the cost driver.
- The nightly review is `24h`, and it does nothing while the lessons file's
  `reviewed-through` window is under about twenty hours old.
- Whatever the interval, the tick lock is what keeps two runs from overlapping.
  A tick that finds its lock held stops and reports, rather than queueing.
