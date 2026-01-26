# Examples

These are abbreviated examples showing the expected shape of outputs.

## Example 1 — Mobile invite flow (tap economy)

Prompt:
“Use `writing-specs-designs`. We’re a consumer iOS app. Add an ‘invite friends’ flow. Goal: increase successful invites. Constraint: ship in 4 weeks. Please optimize taps to first value.”

Expected output highlights:
- Tap budget target + a tap economy worksheet with removal ideas
- Low‑fidelity flow diagram covering entry points (profile, post-share, settings)
- State table for: invite picker, permission prompt, share sheet, success/failure
- Prototype brief for the riskiest interaction (permission timing + copy)
- Requirements with acceptance criteria + measurement plan (invite sent, invite accepted, drop-off)

## Example 2 — B2B bulk role edit (permissions + edge cases)

Prompt:
“Turn these notes into a spec/design doc for bulk role edits for admins. Include edge cases.”

Expected output highlights:
- Diagram of moving pieces: admin UI → permission check → role update service → audit log → analytics
- Flow + state tables for: select users, confirm changes, partial failure, rollback
- Requirements with acceptance criteria covering permission errors and partial success
- Risks/open questions: audit requirements, performance limits, undo semantics

## Boundary example — Vague request

Prompt:
“Write a spec to improve engagement.”

Expected response:
- Ask up to 5 intake questions (user segment, why now, platform, success metric, key flow).
- If still missing, produce 2–3 scoped spec options with explicit assumptions and recommend upstream discovery before committing to a build plan.

