# Examples

These are end-to-end example outputs for smoke-testing.

## Example 1 — B2B SaaS (collaboration tool), next-quarter roadmap

### 0) Context snapshot
- Product: Team collaboration SaaS
- Primary customer segment: 10–200 person tech companies; team leads
- Decision to make (and deadline): Pick Q2 roadmap themes and top 8 initiatives; decision in 2 weeks
- Horizon + cadence: Next quarter; refresh quarterly; rolling 12-month view maintained
- North Star / primary goal: Weekly active teams completing ≥1 project
- Guardrails: support tickets/new team, churn, crash-free sessions, gross margin
- Constraints: 6 engineers, 1 designer; must complete SSO launch; platform migration dependency in May
- Stakeholders: Head of Product (decider), Eng Manager (approver), Growth PM + CS lead (contributors)
- Notes / assumptions: Sales wants enterprise features; product wants to protect activation funnel

### 1) Season framing
Season name: “Season of Activation Reliability”

Why now:
- Activation is flat; new teams struggle to reach the value moment
- Reliability issues are hurting trial → paid conversion
- Enterprise interest is real, but capacity is constrained this quarter

Season bets:
1) Improve time-to-first-project for new teams
2) Reduce activation drop-offs caused by reliability and confusing setup
3) Add one enterprise “wedge” feature that supports sales without derailing activation work

Non-goals:
- Full enterprise admin suite
- New pricing packaging overhaul
- Major UI redesign unrelated to activation

Success criteria:
- Primary metric: Weekly active teams completing ≥1 project
- Guardrails: churn does not increase; support tickets/new team do not spike

### 2) Opportunity inventory (excerpt)
| Opportunity | Target segment | Problem statement | Intended outcome metric/driver | Conviction | Evidence | Effort | Dependencies | Notes |
|---|---|---|---|---|---|---|---|---|
| Guided setup + templates | New teams | Teams don’t know how to configure and start a first project | Time-to-first-project | Belief | Funnel shows drop at “create first project”; CS hears confusion weekly | M | Design | |
| Fix onboarding reliability bugs | All new users | Errors/crashes block early progress | Crash-free sessions; activation completion | Known | Error logs + spike in tickets | M | Platform migration | |
| Invite flow improvements | New teams | Teams fail to invite collaborators, limiting value | % projects with ≥2 collaborators | Belief | Cohorts w/ invites have higher completion | S | None | |
| SSO (must-do) | Enterprise | Enterprise trials can’t roll out without SSO | Enterprise trial conversion | Known | 5 active deals blocked | L | Security review | Commitment |
| Admin roles (phase 1) | Enterprise | Admins need minimal role control | Enterprise activation | Hypothesis | Anecdotal sales feedback only | M | SSO | Might be discovery first |

### 3) Scoring model + table (ICE, excerpt)
Common currency: North Star units (weekly active teams completing ≥1 project) within the quarter.

| Opportunity | Common-currency impact (range) | Impact | Confidence | Ease | ICE score | Key assumptions | Notes |
|---|---:|---:|---:|---:|---:|---|---|
| Guided setup + templates | +3–8% | 4 | 3 | 3 | 36 | Templates reduce friction and increase first-project completion | |
| Fix onboarding reliability bugs | +2–6% | 3 | 4 | 3 | 36 | Bug fixes remove blockers; impact shows within weeks | Depends on migration timing |
| Invite flow improvements | +1–3% | 2 | 3 | 4 | 24 | Small UI nudge increases invites | |
| SSO (must-do) | Indirect | 2 | 5 | 1 | 10 | Doesn’t move North Star directly, but required commitment | Must-do |
| Admin roles (phase 1) | Unclear | 2 | 1 | 2 | 4 | Needs discovery; impact unclear | Put in discovery backlog |

### 4) Shortlist + parking lot
Shortlist:
1) Guided setup + templates
2) Fix onboarding reliability bugs
3) Invite flow improvements
4) SSO (must-do)

Parking lot:
- Admin roles (phase 1) — insufficient evidence; do discovery after SSO
- Pricing overhaul — out of season

### 5) Roadmap draft (Now/Next/Later)
| Now | Next | Later |
|---|---|---|
| Onboarding reliability bug fixes | Guided setup + templates rollout (iterative) | Admin roles (discovery) |
| Invite flow improvements | SSO implementation | Enterprise admin suite (future season) |

Rolling plan cadence:
- Rolling horizon: 12 months (theme-level)
- Refresh cadence: quarterly; major re-plan every 6 months
- Update triggers: material metric shift, major platform change, exec strategy change

### 6) Decision narrative + Think Bigger
One-paragraph summary:
This quarter is the “Season of Activation Reliability.” We will prioritize work that measurably improves time-to-first-project and removes early blockers, while delivering SSO as a required enterprise commitment. We will defer broader enterprise admin work until we have evidence and capacity.

Think Bigger:
- Big bet: “Instant team setup” (one-click workspace + auto-generated project plan)
  - Why it matters: compresses time-to-value dramatically
  - What we’d need to believe/learn: users trust defaults; quality doesn’t degrade
  - Discovery next step: prototype + 5 user tests; measure setup completion rate

### 7) Risks / Open questions / Next steps
Risks:
- Platform migration delays could block reliability fixes
Open questions:
- Is the activation bottleneck mainly “setup confusion” or “invite + collaboration depth”?
Next steps:
1) Validate impact assumptions with cohort analysis (Analytics, 1 week)
2) Schedule roadmap review with stakeholders; confirm season non-goals (Head of Product, next week)

## Example 2 — Marketplace, 6-month roadmap (high-level expected output)

High-level expected structure:
- Season framing: “Season of Trust-First Growth”
- Common currency: successful jobs completed with a quality threshold
- Opportunities: supply availability, match rate, time-to-booking, cancellations, fraud prevention
- Roadmap: quarterly themes with explicit non-goals; rolling 18–24 month view refreshed every 6 months

## Boundary example — “Give me a 2-year roadmap; we don’t have goals”

Response pattern:
- Ask for the decision and success criteria (North Star + guardrails).
- If still missing, propose 2–3 plausible season options and the minimum discovery needed.
- Recommend running product vision + North Star metric work before committing to a 2-year plan.

