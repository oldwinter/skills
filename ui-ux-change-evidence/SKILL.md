---
name: ui-ux-change-evidence
description: Require screen-recorded acceptance evidence for every implemented UI or UX requirement and bug fix. Use whenever a task changes visible UI, interaction behavior, responsive layout, accessibility behavior, motion, user-facing copy, or a user flow, including review and delivery of that change. Do not use for planning-only or backend-only work with no user-visible change.
---

# UI/UX Change Evidence

Treat a UI/UX-changing implementation as incomplete until current screen-recorded evidence and a concise change summary have been delivered.

## Scope

Apply this gate to web, mobile, desktop, extension, embedded, and other graphical interfaces. It covers new UI requirements and bug fixes affecting visuals, interaction, navigation, feedback states, responsiveness, accessibility behavior, motion, or user-facing copy.

Do not trigger it for design discussion, planning, or audit work that changes no runnable interface, or for backend-only changes with no observable UI effect.

## Record The Changed Experience

1. Derive one or more recording scenarios from the changed behavior and its acceptance criteria.
2. Run the final current build. Complete relevant functional, visual, and accessibility checks before recording; the video supplements those checks and does not replace them.
3. Record each affected flow from its recognizable entry point through the changed interaction to the visible result.
4. For a bug fix, exercise the scenario that previously failed and show it succeeding. Include an affected error, loading, empty, keyboard, or responsive state when it is material to the fix.
5. For viewport-specific changes, record every affected viewport or device class. Separate short clips are acceptable.
6. Keep the capture focused and brief. Disable audio unless the user explicitly requests narration.

Prefer the project's existing recording workflow. For web interfaces, a browser automation video is usually the most reproducible option; for native interfaces, use the platform recorder. Produce an actual video such as MP4 or WebM. A screenshot, test trace, or written claim is not a substitute.

## Protect The Capture

- Use sanitized test data and close unrelated windows before recording.
- Exclude secrets, tokens, cookies, personal data, private notifications, and unrelated private URLs.
- Record only the app surface needed for acceptance. If safe capture is impossible, stop and report the blocker instead of exposing sensitive data.
- Store the working video in the repository's ignored evidence/runtime location, or another user-approved artifact location. Do not commit large recordings unless the repository explicitly requires tracked evidence.

## Verify And Deliver

Play the saved recording back after the final code edit and app restart. Confirm that it is nonblank, readable, current, and covers every claimed change.

Deliver the evidence through one of these paths:

- When the task already has a corresponding issue and the issue is in scope, attach the recording or an accessible artifact link there and add the change summary. Do not create a new issue or publish elsewhere solely for this evidence.
- Otherwise, send the recording or a directly accessible local artifact path to the user in the final response.

The accompanying summary must identify the changed points, demonstrated scenario, tested platform or viewport, and recording path or link. Add timestamps when one clip demonstrates multiple changes.

Do not claim the UI/UX task is complete if the recording is missing, stale, unreadable, or not delivered. If the environment cannot record or the issue provider cannot accept the artifact, state exactly what is blocked and preserve the verified local video for handoff.
