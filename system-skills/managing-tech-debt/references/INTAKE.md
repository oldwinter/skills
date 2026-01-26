# Intake (Question Bank)

Ask up to **5** questions at a time, then proceed with explicit assumptions.

## A) Context + scope
1) What system(s)/repo(s)/service(s) are in scope? What do they do?
2) Who are the stakeholders and who is the decision-maker (Eng/PM/Leadership)?
3) What’s the time horizon (e.g., 6 weeks / next quarter / 12 months) and any fixed deadlines (launches, contracts, compliance)?

## B) Pain + symptoms
4) What are the top symptoms? (incidents, latency, deploy pain, slow iteration, flaky tests, UX inconsistency, broken integrations, cost)
5) Which symptoms are **user-visible** vs internal-only? Any examples users complain about?

## C) Constraints + risk tolerance
6) Team capacity (people, on-call load) and how much can be allocated to debt work?
7) Constraints: freeze windows, compliance/security requirements, data migration limits, uptime/SLO requirements.
8) Risk tolerance: is this a “must not break” system? What’s the rollback expectation?

## D) Options under consideration
9) Are you considering: refactor, partial migration (“strangler”), full rebuild, deprecation, vendor replacement?
10) What “capabilities” does the business need that the current system can’t support (operational flexibility, pricing control, reporting, scalability)?

## E) Evidence + baselines (if available)
11) Any baseline metrics? (incident rate, MTTR, p95 latency, deploy frequency, lead time, cost, support volume)
12) Any known dependencies or blockers (teams, vendors, data contracts)?

