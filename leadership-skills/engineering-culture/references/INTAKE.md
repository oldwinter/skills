# Intake Questionnaire (Engineering Culture)

Ask up to **5** questions at a time. Prefer redacted summaries over sensitive details.

## 1) Context + scope
1) What’s the scope: one team, multiple teams, or the full engineering org? Who is the decision owner?
2) What are you building (product/domain), and what stage are you in (startup/scale/enterprise)?
3) Engineering size and composition (SWE/SRE/data/mobile/etc), and remote/hybrid/in-office setup?
4) What’s the timeline or forcing function (launch, reliability crisis, growth, org changes)?

## 2) Symptoms (with examples)
5) What are the top 2–3 symptoms you want to fix? Share 2–5 concrete examples (anonymized):
   - Slow delivery / long PR cycle time
   - Frequent incidents / regressions
   - Low ownership / “throw it over the wall”
   - High toil / burnout
   - Cross-team friction / unclear ownership
   - Poor cross-functional collaboration

## 3) Delivery system + quality
6) Current release/deploy cadence (per day/week), environments, and rollback strategy?
7) CI/CD maturity: automated tests, build times, flaky tests, deploy approvals, progressive delivery?
8) Quality signals you track today (incidents, MTTR, change failure rate, p95 latency, support volume)?
9) Where does work get stuck most often (idea→issue, issue→PR, PR→merge, merge→deploy, deploy→learn)?

## 4) Architecture + ownership
10) Architecture shape (monolith/services) and the top coupling/ownership hotspots?
11) How is code ownership defined (teams, CODEOWNERS, components)? Where is ownership unclear?
12) Which interfaces between teams are most painful (APIs, data contracts, shared libraries, platform dependencies)?

## 5) Culture signals (stated vs lived)
13) What behaviors are implicitly rewarded today (speed, caution, heroics, polish, collaboration, “not breaking things”)?
14) What are the most common cultural anti-patterns (blame, over-reviews, under-specifying, “works on my machine”, gatekeeping)?
15) What norms exist today for code review, testing, documentation, and incident retros?

## 6) Org design + policies (Conway’s Law)
16) Current team topology and reporting structure? Any planned org changes?
17) Do you have standardized leveling/policies (what “senior” means, on-call expectations, review expectations) across teams?
18) Where does the operating model differ across teams (process, tooling, quality bar)?

## 7) Cross-functional workflow
19) Where is work tracked (Jira, GitHub, Linear, docs), and who uses what?
20) What collaboration is hardest (PM↔Eng scope, Design↔Eng handoff, Marketing↔deploy, Data↔experiments)?
21) Do non-engineers ever touch the engineering toolchain (issues/PRs/feature flags/config)? What’s the desired level?

## 8) AI-assisted development (optional)
22) Are engineers using AI coding tools/agents today? For what tasks? Any incidents or policy constraints?
23) What “human as architect” shift do you want (more spec, more review, less boilerplate)?

## 9) Success definition
24) In 4–12 weeks, what should be measurably different (2–5 outcomes + how you’ll know)?
25) What must not change (non-negotiables, compliance/security constraints, quality guardrails)?

