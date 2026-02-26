# Examples (2 good, 1 boundary)

## Example 1 — 60-minute prototype: “AI meeting notes → action items”

### Vibe Coding Brief (excerpt)
- **Demo promise:** “In 60 minutes, we will demo pasting meeting notes and getting a prioritized action-item list for a PM.”
- **Non-goals:** real LLM integration, auth, persistence, multi-user.
- **Fake vs real:** LLM output mocked; static sample notes; no external APIs.

### Build Plan + Task Board (excerpt)
| Slice | User-visible behavior | Validation (steps) |
|------:|------------------------|--------------------|
| 1 | App runs; paste notes textbox + “Generate” button | Run app; click button; see placeholder output |
| 2 | Mock “action items” generation with deterministic rules | Paste sample notes; output shows 5 items |
| 3 | “Priority” and “owner” fields; basic filtering | Toggle filter; list updates |
| 4 | Demo mode: preloaded sample notes + one-click demo flow | Click “Load demo”; run through hero scenario |

### Demo script (talk track bullets)
1) “Here’s the workflow today (manual).”
2) “Paste notes → action items in 10 seconds.”
3) “What’s real vs mocked, and why.”
4) “If this resonates, next is integrating the real LLM and evaluation.”

## Example 2 — 45-minute prototype: onboarding checklist app

### Vibe Coding Brief (excerpt)
- **Demo promise:** “In 45 minutes, we will demo a new user completing a 5-step onboarding checklist with progress saved for this session.”
- **Non-goals:** accounts, backend DB, notifications, polished design system.
- **Fake vs real:** checklist items hardcoded; session-only state.

### Acceptance criteria (excerpt)
- [ ] User can check/uncheck items and see progress %.
- [ ] User can reset the checklist.
- [ ] Demo has a single hero path that never 404s or crashes.

## Boundary example — production payments backend

Request: “Build a production payments backend and deploy it.”

Response:
- Out of scope for vibe coding. Propose: mock payments for a prototype, define required security/compliance owners, and create a separate production plan with reviews, testing, and rollout/rollback.

