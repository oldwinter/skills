# Templates (Copy/Paste)

Use these templates to produce the **Dogfooding Pack**.

## 0) Context snapshot
- Product:
- Target user persona:
- Core workflows to dogfood (1–3):
- Time box + cadence:
- Participants (roles):
- Environment (prod/staging) + constraints:
- Known pain points / hypotheses:
- Tracking tools (Jira/Linear/Notion/etc.):
- Ship gate definition:
- Assumptions / unknowns:

## 1) Dogfooding charter
- **Why we are dogfooding:** (goal in 1 sentence)
- **What we are dogfooding:** (workflows + scenarios)
- **Who participates:** (names/roles)
- **Cadence:** (daily sessions + weekly triage)
- **Rules:**
  - Use the product as a real user would (avoid admin shortcuts unless the persona has them).
  - Log issues as reproducible artifacts (steps + evidence).
  - No real customer data unless explicitly approved and safe.
- **Success criteria:** (measurable)
- **Ship gate:** (what must be true to ship)

## 2) Scenario map
| Scenario | User goal | Start state | Steps (high level) | “Done” definition | Evidence of done | Notes / edge cases |
|---|---|---|---|---|---|---|
| S1 | | | | | | |

## 3) Routine plan (daily/weekly)

### Daily (time-boxed)
- Time box (minutes):
- Each participant runs:
  - Mon:
  - Tue:
  - Wed:
  - Thu:
  - Fri:

### Weekly triage agenda (45–60 min)
1) Review metrics (participation + scenario completion)
2) Review top pains (S0/S1 first)
3) Decide disposition (fix now / schedule / won’t fix)
4) Assign owners + next actions
5) Confirm ship gate progress
6) Pick next week’s scenario focus

## 4) Dogfooding log (issue-level)
| ID | Date | Participant | Scenario | Step | Severity | Issue summary | Steps to reproduce | Expected | Actual | Evidence link | Workaround | Disposition | Owner | Due | Verified? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | |

## 5) Triage board spec (if using a tracker)
Recommended fields/labels:
- Labels: `dogfooding`, `scenario:S1`, `type:bug|ux|gap|docs`, `severity:S0|S1|S2|S3`
- Statuses: `new` → `triaged` → `in progress` → `ready for verification` → `verified` (or `won't fix`)
- Required fields for `new`: scenario, severity, repro steps, expected vs actual, evidence

## 6) Weekly dogfooding report

### Summary
- Time box:
- Participation:
- Scenarios covered:
- Ship gate status:

### Top pains (3–5)
1) Pain:
   - Scenario impacted:
   - Severity:
   - Evidence:
   - Why it matters:

### Decisions
**Fix now**
- …

**Schedule**
- …

**Won’t fix (why)**
- …

### Shipped + verified fixes
- Fix:
  - Scenario verified:
  - Evidence:

### Risks
- …

### Open questions
- …

### Next steps
1) …
2) …

