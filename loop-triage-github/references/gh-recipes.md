# `gh` and REST recipes for the GitHub loop

Every recipe here was learned by having it fail first. They are the ones that cost time
to rediscover, so the tick uses them instead of the obvious command.

Placeholders: `R` is the `repo` value from `.loop/config.json` (`owner/name`), `N` a
number, `S` a sha. Nothing here is specific to one project.

## Searching

**Search takes dates, not timestamps.** `gh search issues --updated ">=2026-10-14T06:33:00Z"`
does not error: it silently matches nothing, which reads as "no new issues" and makes a
tick look quiet when it is blind.

```bash
gh search issues --repo R --include-prs --created ">=YYYY-MM-DD" --updated ">=YYYY-MM-DD" \
  --limit 100 --json number,title,isPullRequest,state,author,createdAt,updatedAt,url
```

Filter `updatedAt >= since` on the JSON afterwards, with both sides parsed, and ignore an
update that is only the loop's own comment. `--include-prs` is what makes one search cover
issues and pull requests; without it the PR half of the queue is invisible.

**Portable date arithmetic.** `date -u -d '3 days ago'` is GNU coreutils only; it is missing
on macOS and in PowerShell. Compute the window in Python, which is present wherever this
loop runs:

```bash
python3 -c "import datetime as d;print((d.datetime.now(d.datetime.timezone.utc)-d.timedelta(days=3)).strftime('%Y-%m-%d'))"
```

## Reading a thread

**`gh issue view` and `gh pr view` fail on the deprecated Projects-classic field** on
repositories that still carry one, with an error about a project card, and no useful output.
Read the REST resource instead and select the fields with `--jq`:

```bash
gh api repos/R/issues/N --jq '{title,body,state,user:.user.login,comments_url}'
gh api repos/R/issues/N/comments --jq '.[] | {author:.user.login,at:.created_at,body}'
gh api repos/R/pulls/N --jq '{title,body,state,merged,head:.head.sha,author:.user.login}'
```

**One page is usually the whole thread.** `per_page=100` covers the runs, reviews and
comments of a normal PR, and older `gh` releases have no `--slurp` to merge pages: `gh api
... --slurp` fails with an unknown-flag error on them. Use one page and `per_page=100`, or
`--paginate` with `--jq` when a thread is genuinely long.

**`--jq` prints scalars bare.** `gh api user --jq .login` prints the login with no quotes, so
do not feed it to a JSON parser; read it as a string. `gh api ... --jq '.[].login'` prints one
login per line.

## Checks, statuses and reviews

**`gh pr checks --json` does not work here** (it rejects `--json`). Read the check runs from
the API on the head sha:

```bash
gh api repos/R/commits/S/check-runs?per_page=100 \
  --jq '.check_runs[] | {name,status,conclusion}'
```

Conclusions that are not a pass: `failure`, `cancelled`, `timed_out`, `action_required`,
`startup_failure`, `stale`. `skipped` is a third thing: the job did not run, so it is
reported as not run, never as green.

**The review bot reports a commit status, not a check run.** A review bot's "done" signal
lives in the commit statuses, under a context name such as `CodeRabbit`, so a check-runs-only
read waits forever for it:

```bash
gh api repos/R/commits/S/status --jq '.statuses[] | {context,state,description}'
```

**Review threads need GraphQL.** The REST reviews endpoint gives top-level reviews only;
`isResolved` and `isOutdated` live on the threads:

```bash
gh api graphql -f query='
  query($owner:String!,$name:String!,$number:Int!){
    repository(owner:$owner,name:$name){
      pullRequest(number:$number){
        reviewThreads(first:100){nodes{isResolved isOutdated path
          comments(first:50){nodes{author{login} body createdAt}}}}}}}' \
  -F owner=OWNER -F name=NAME -F number=N
```

A finding is answered only when its author is in `trustedLogins` or is the owner. Anyone
else's comment is listed in the report and not read further.

**Failed logs.** A check run's `id` is a workflow run id for Actions:

```bash
gh run view RUN_ID --repo R --log-failed
```

**Commit authors on a PR** (the trust check that stops work on a foreign commit):

```bash
gh api repos/R/pulls/N/commits --jq '.[].author.login'
```

## Writing, and why the API is used instead of the CLI

**`gh issue edit` and `gh pr edit` fail on Projects-classic**, exactly as the read commands
do, and they also rewrite more than asked. Patch the resource directly, from a file so the
body is not mangled by shell quoting:

```bash
gh api -X PATCH repos/R/issues/N -f title="New title"
gh api -X PATCH repos/R/pulls/N -F body=@/path/to/body.md
```

**Comment from a file, never `--body`.** The draft is posted byte for byte, and a body on
the command line loses newlines, backticks and non-ASCII text to the shell:

```bash
gh issue comment N --repo R --body-file /path/to/draft.md
gh pr comment N --repo R --body-file /path/to/draft.md
gh pr review N --repo R --request-changes --body-file /path/to/draft.md
```

**Merge with the head pinned.** An approved card names the head it was approved at; the
merge must fail if the head moved in between:

```bash
gh pr merge N --repo R --squash --match-head-commit S
gh api -X PUT repos/R/pulls/N/merge -f merge_method=squash -f sha=S
```

The API form is what a `then: "merge"` card uses, because it pins `sha` in the same call
that merges. GitHub returns `405` when the sha is no longer the head: that is the check
working, not a bug — mark the card stale and rewrite it for the new head.

## Failure reading

- **`404` is not always "gone".** On a private repository a missing scope also reads as
  `404`; report it as an unreadable resource, not as a deleted one.
- **`403` with a rate-limit body** is a failed read. Report it (`WATCH_ERROR` in the
  watcher); never treat it as "nothing happened".
- **A check-read error is a failure, not a pass.** The same applies to a `--jq` filter that
  returns `null`: an unexpected shape is reported, never interpreted as "no checks".
- **Timestamps from the API are UTC ISO 8601** (`2026-10-14T06:33:00Z`). Parse them before
  comparing, and write only API timestamps or clock readings into cards — the stale check
  compares them across ticks.
