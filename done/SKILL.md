---
name: done
description: Finish the current change by validating, committing, opening and merging a PR or MR, reconciling related issues, and updating the local default-branch worktree.
disable-model-invocation: true
---

# Done

Take the current task to an observable merged state. Manual invocation is explicit authorization to commit, push, create or edit a PR/MR, merge it, and mutate directly related issues. It does not authorize force-pushes, protection bypasses, unrelated edits, or other external writes.

Treat user arguments as optional scope, issue context, or merge-method preferences. Otherwise infer scope from the current conversation and repository evidence.

## Process

1. **Establish the closure contract.** Resolve the git root, forge from the remote URL, authenticated user, default branch, current branch and upstream, worktree layout, dirty state, and any open PR/MR for the branch. Store the resolved forge default branch as `DEFAULT_BRANCH` and use that value consistently below; never assume a fixed branch name. Define the intended change set from the current task; preserve unrelated work unstaged. If intended and unrelated edits cannot be separated safely, ask one precise question before any external write.

   Completion criterion: the forge, resolved `DEFAULT_BRANCH`, intended paths, unrelated paths, existing review state, and local default-branch worktree are accounted for.

2. **Validate the intended change.** Read the full diff and repository instructions. Run the smallest relevant checks after the final edit, including tests, lint, build, or generated-file checks required by the changed surface. Fix failures caused by the intended change; stop with the exact blocker when a green result requires broader scope or unavailable infrastructure.

   Completion criterion: every intended change is represented in the diff, required artifacts are present, and no relevant check is red.

3. **Commit and push.** When on `DEFAULT_BRANCH` or detached HEAD, create a `codex/<short-slug>` branch without disturbing the working tree. Follow recent commit-message style and split independent concerns into atomic commits. Stage only the intended paths, inspect the staged diff, commit, and push with upstream tracking. Resolve ordinary remote divergence without rewriting published history.

   Completion criterion: every intended change is in a remote-reachable commit and unrelated local changes remain untouched.

4. **Reconcile issues when useful.** Using the matching forge CLI or API, inspect open issues assigned to the authenticated user or unassigned. Judge relevance by shared behavior, root cause, and scope rather than keyword overlap.

   - For a strong match fully resolved by this change, add the forge's closing reference to the PR/MR.
   - For a strong match that remains open, add a non-closing relationship.
   - With no match, create an issue only when the problem or follow-up is independently worth tracking. Skip issue creation for small fixes, routine cleanup, or changes with no meaningful follow-up.

   Completion criterion: record one evidence-backed outcome: closing link, related link, newly created issue, or deliberate skip.

5. **Create or update the PR/MR.** Reuse the open PR/MR for the branch when one exists; otherwise create a ready-for-review PR/MR targeting `DEFAULT_BRANCH`. Derive the title and body from the actual commits and diff. Include a concise summary, verification evidence, the chosen issue relationship, and any known residual risks.

   Completion criterion: one non-draft PR/MR represents the remote branch and its description matches the delivered change.

6. **Reach the merge gate.** Inspect mergeability, required checks, approvals, and unresolved review threads. Watch pending checks. Fix failures attributable to the change, push the correction, and re-run the same gate. If a remote CI lane fails and this manually invoked skill has explicit push/PR/merge authorization, first read the actual failure and record its run URL, failed lane, confirmed root cause, local equivalent validation result, and unresolved code/test/privacy/security risks in the PR/MR and final report. Under the repository's standing CI-failure policy, that evidence permits proceeding without a second confirmation; it does not permit hiding failures, bypassing protections, force-pushing, or ignoring non-CI merge blockers. After merge, disclose the failed lanes, why the standing policy applied, and local validation status to the user. Respect repository protections and use the repository's established merge method.

   Completion criterion: the PR/MR is mergeable, approvals are satisfied, and checks either pass or each failed CI lane has the required standing-policy evidence and risk disclosure; otherwise report the exact external blocker without claiming completion.

7. **Merge and reconcile issue state.** Merge with `gh` or `glab`, then query the forge to verify the merged state and merge commit. Confirm that closing-linked issues are closed; close a still-open issue only when the merged change fully resolves it.

   Completion criterion: the forge reports the PR/MR merged and every touched issue has the intended final state.

8. **Refresh the local default-branch worktree.** Use `git worktree list --porcelain` to find the worktree already on `refs/heads/$DEFAULT_BRANCH`. If none exists and the current worktree is clean after the merge, switch the current worktree to `$DEFAULT_BRANCH`. Run `git pull --ff-only` in the selected worktree. Preserve any unrelated dirty state and report it if it blocks the fast-forward.

   Completion criterion: the local `DEFAULT_BRANCH` worktree is identified, its HEAD matches the latest remote `DEFAULT_BRANCH`, and the merged change is reachable from it.

## Final Report

Report the commit hash(es), PR/MR URL and merge result, issue action or skip reason, verification commands, and default-branch worktree path and HEAD. List any untouched local changes or external blocker explicitly.
