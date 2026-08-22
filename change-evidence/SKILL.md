---
name: change-evidence
description: "Capture and deliver screen-recorded evidence for UI/UX, frontend, visual, responsive, accessibility, interaction, or animation changes and their bug fixes, covering the baseline or reproduction, changed behavior, and acceptance results."
---

# Change Evidence

## Trigger

Use this skill for UI/UX, frontend, visual, responsive, accessibility, interaction, or animation changes and for bug fixes in those user-facing surfaces. Pure backend, data, CLI, infrastructure, documentation, and non-visual refactoring work is outside this skill unless it also changes user-facing behavior.

## Completion contract

A task in scope is complete only when the handoff contains:

- a readable recording of the baseline or bug reproduction;
- a focused recording of the changed or fixed behavior; and
- the acceptance checks and their results, with paths to the recordings.

If a display, recorder, permission, or usable acceptance surface is unavailable, report that exact blocker and keep the task incomplete. A dry run or a verbal claim is not recording evidence.

## Workflow

1. Define the changed point and acceptance path before editing. Name the user-visible state and interaction. For a bug fix, reproduce and record the failure before changing code.
2. Record a short baseline or reproduction focused on that path. Prefer a recorder already provided by the repository; otherwise use a platform recorder that produces a common video format. Choose a duration long enough to show the path, usually 20–60 seconds. Review the visible screen first and close or mask secrets, tokens, private sessions, and unrelated windows.
3. Make the requested change while preserving the same entry point and test data where possible.
4. Record the fixed behavior through the same focused path. Keep the affected browser or app state visible so the recording shows the observable acceptance signal.
5. Run the smallest relevant checks after the final edit. Confirm that each recording exists, is non-empty, opens successfully, and matches the stated acceptance result.
6. Deliver the evidence in the handoff: changed point, baseline or reproduction path, fixed path, recording paths, and exact checks/results. Attach or post evidence to an issue only when the task explicitly authorizes that external write; otherwise provide the prepared paths without posting.

## Evidence quality

Keep each recording scoped to the changed point, include enough context to identify the page or test, and show the acceptance state rather than an idle desktop. When recording fails, report the failure and its cause instead of substituting screenshots or an assertion.
