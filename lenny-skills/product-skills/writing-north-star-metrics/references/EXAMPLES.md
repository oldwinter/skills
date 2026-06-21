# Examples

These are end-to-end example outputs for smoke-testing.

## Example 1 — B2B SaaS (team collaboration tool)

### 0) Context snapshot
- Product: Team collaboration SaaS
- Primary customer segment: 10–200 person tech companies; team leads
- Value moment: “A team successfully completes their first project together using the product.”
- Business model: Subscription (per-seat)
- Strategic goal: Improve activation → conversion
- Horizon: This quarter
- Measurement constraints: Product analytics available; limited CRM linkage
- Stakeholders to align: Head of Product, Growth PM, CS lead

### 1) North Star Narrative (short)
We exist to help teams coordinate work and ship outcomes faster. Customers succeed when teams repeatedly complete projects with fewer delays and less coordination overhead.

In scope: onboarding, collaboration flows, project completion.  
Out of scope: sales pipeline velocity, marketing site traffic.

Tie-breaker: choose work that increases repeated team-level project completion in-product.

### 2) Candidate metrics (evaluation table)
| Candidate metric | Measures customer value? | Definition (1–2 lines) | Update frequency | Controllable this quarter? | Gaming risk | Instrumentation readiness | Notes |
|---|---|---|---|---|---|---|---|
| Weekly active teams completing ≥1 project | Yes | Count of teams that complete at least one project in a given week | Weekly | Yes | Teams can “complete” trivial projects | Medium | Add quality threshold if needed |
| % of teams reaching value moment within 7 days | Yes | % of new teams that complete first project within 7 days of signup | Daily/weekly | Yes | Incentivizes rushed setup | High | High | Use guardrails (quality, support tickets) |
| Weekly active users | Partial | Unique users active per week | Weekly | Yes | Vanity (activity ≠ value) | Low | High | Better as input metric |
| % of teams with zero critical onboarding errors | Yes | % new teams with no “blocking errors” events in first 7 days | Daily/weekly | Medium | Might ignore value delivery | Low | Medium | Useful friction option |

### 3) Chosen metric spec
- Name: Weekly Active Teams Completing ≥1 Project (WATCP)
- Definition: Number of distinct teams that complete at least one project meeting the “non-trivial” threshold in a calendar week.
- Why: Represents delivered customer value (teams finishing work), not internal activity.

Formula:
- Numerator: count(distinct team_id where project_completed=true AND project_quality=non_trivial) over 7 days
- Unit: teams/week

Rules:
- “Non-trivial” project: ≥2 collaborators OR ≥5 tasks completed OR ≥1 external integration enabled
- Exclude internal/test teams

Ops:
- Segments: company size, plan tier, acquisition channel, cohort week
- Data source: product events table
- Latency: ~2 hours
- Owner: Growth Analytics
- Review cadence: weekly metric review; monthly spec review

### 4) Driver tree + guardrails
| Driver | Why it matters | Leading input/proxy metrics | Example levers | Notes |
|---|---|---|---|---|
| Onboarding success | Teams must reach value moment | Time-to-first-project, % teams creating first project within 1 day | onboarding flow changes, templates, guided setup | |
| Collaboration depth | Metric depends on team usage | % projects with ≥2 collaborators, invites sent per new team | invite nudges, role setup, permissions UX | |
| Reliability | Failures block completion | onboarding error rate, crash-free sessions | bug fixes, performance work | |

Guardrails:
- Support tickets per new team (should not spike)
- Refunds / cancellations within 30 days

### 5) Validation & rollout
Validation:
- Sanity: onboarding template change should improve time-to-first-project
- Leadingness: time-to-first-project should predict WATCP and trial→paid conversion

Rollout:
- Dashboard: “North Star / WATCP”
- Weekly review owner: Growth PM
- Monthly spec owner: Growth Analytics
- Decision rule: prioritize roadmap items that plausibly move one of the top drivers and show impact within 2–4 weeks

### 6) Risks / Open questions / Next steps
Risks:
- “Non-trivial” threshold may exclude real value for small teams
Open questions:
- Should we weight by project size or focus on frequency?
Next steps:
1) Validate the threshold on historical cohorts (Analytics, 1 week)
2) Add guardrail tracking (CS, 1 week)

## Example 2 — Marketplace (local services)

High-level expected choice:
- North Star: **Successful jobs completed that meet a quality bar**
- Inputs: supply availability, match rate, time-to-booking, cancellation rate
- Guardrails: refunds, complaints, fraud, provider churn

## Boundary example — “Retention should be our North Star”

Response pattern:
- Keep retention as an outcome/validation metric.
- Propose a customer value metric that the team can influence this quarter.
- Build a driver tree of controllable inputs (activation, value frequency, friction reduction) and add guardrails.

