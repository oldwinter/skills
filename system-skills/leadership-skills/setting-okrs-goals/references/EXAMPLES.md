# Examples

These are end-to-end example outputs for smoke-testing.

## Example 1 — B2B SaaS, Activation OKRs (quarter)

### 0) Context snapshot
- Cycle + horizon: Q2 (Apr–Jun)
- Team(s) in scope: Activation squad (PM, 4 eng, 1 design)
- Strategy anchor: “Increase weekly active teams completing the core workflow”
- Baselines + data sources: Amplitude dashboards; weekly refresh
- Constraints: must ship SSO by May; limited design bandwidth
- Stakeholders: Head of Product (decider), Eng Manager (approver), Data lead (consulted)
- Notes / assumptions: activation funnel drop-off is biggest lever this quarter

### 1) Alignment map
| Company goal / North Star | Team objective | Why this is “one step away” | Primary metric(s) it should influence | Notes |
|---|---|---|---|---|
| Increase weekly active teams completing the core workflow | New teams reach first value reliably in week 1 | First value is the leading driver of weekly active teams | # teams reaching value moment in first week | |

### 2) OKRs
**Objective:** New teams reach first value reliably in week 1  
**Why now:** activation is flat; early friction is high; sales pressure is pulling us toward enterprise work  
**How this supports the company goal:** more teams reach the value moment → more teams return weekly  
**Primary owner:** Activation squad  

| KR | Metric definition (unambiguous) | Baseline | Target | Window | Owner | Data source | Type | Anti-gaming note | Guardrails |
|---|---|---:|---:|---|---|---|---|---|---|
| Increase teams reaching value moment in first 7 days | # of new workspaces that complete “core workflow” within 7 days of creation | 1,200/qtr | 1,650/qtr | Q2 | PM | Amplitude | absolute | Don’t “improve” by shrinking new-team volume | Guardrail: new workspace creations ≥ baseline |
| Reduce onboarding blocker incidence | # of sessions hitting onboarding-blocker error codes | 4,500/qtr | 2,500/qtr | Q2 | Eng | Sentry | absolute | Avoid hiding errors via logging changes | Guardrail: error logging coverage unchanged |
| Improve first-week setup completion (ratio) | % of new workspaces completing setup checklist within 48h | 42% | 55% | Q2 | Design | Amplitude | ratio | Could be gamed by excluding hard segments | Guardrail: track absolute completions + segment parity |

### 3) Systems & habits
| System/habit (default-on) | Cadence | Owner | What it changes | Evidence/output captured |
|---|---|---|---|---|
| Onboarding funnel review + experiment pick | Weekly | PM + Data | Keeps focus on biggest drop-off | 1-page weekly note + next experiment |
| 5 user sessions on onboarding flow | Weekly | Research/PM | Builds customer empathy + catches friction | Notes + top 3 issues |

### 4) Review + grading plan (excerpt)
- Weekly OKR review every Monday; mid-cycle checkpoint in week 6; end-of-quarter grading + retro in final week.

### 5) Risks / Open questions / Next steps (excerpt)
Risks:
- SSO commitment might steal capacity from activation improvements
Open questions:
- Is the biggest lever setup flow, reliability, or collaboration invite depth?
Next steps:
1) Confirm baseline definitions with Data (this week)
2) Align on non-goals with leadership (next week)

## Example 2 — Growth, avoid “ratio gaming”

Prompt: “Set quarterly OKRs for Growth. Teams keep arguing about conversion rate vs volume.”

Expected pattern:
- Primary KRs are **absolute counts** (e.g., activated users, retained users).
- If a ratio is included, it is paired with denominator checks and a volume guardrail.

## Boundary example — No strategy anchor

Prompt: “Write OKRs, but we don’t have a company goal.”

Response pattern:
- Ask for the minimal anchor (exec priority, North Star, or success definition).
- If still missing, propose 2–3 plausible goal frames + draft OKRs as options with explicit assumptions.

