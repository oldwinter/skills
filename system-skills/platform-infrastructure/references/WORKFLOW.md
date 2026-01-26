# Workflow (expanded)

Use this as the detailed playbook behind `SKILL.md`.

## Step 1 — Decision framing
- Produce a single decision statement: **“We will do X (and not Y) by Z to achieve metric M.”**
- Include a “not in scope” list to prevent this from turning into a rewrite.

## Step 2 — Platformization candidates
Heuristics for good shared capabilities:
- Multiple consumers (2+ teams/services) and repeated rebuilds
- Stable contract surface (API/schema) even if implementations evolve
- Clear migration path (shim, adapter, dual-run, deprecate)

Output: a table of candidates with consumer count, current duplication, proposed contract, and rollout plan.

## Step 3 — Make “invisible” platform work measurable
Minimum recommended quality attributes to address explicitly:
- Reliability: availability, error rate, MTTR targets; incident classes
- Performance: p95/p99 latency and throughput targets for key journeys
- Privacy/safety: encryption, access control, residency, retention, auditability
- Operability: on-call ownership, dashboards/alerts, runbooks, escalation paths
- Cost: top drivers (compute, storage, third-party) and guardrails/budgets

## Step 4 — Doomsday clock
Guideline: triggers should fire **before** you’re in crisis.
- Define “lead time to fix” (weeks/months) and set thresholds earlier than the point of failure
- Separate: (a) monitoring + alerting, (b) mitigation project(s), (c) “feature freeze” trigger policy

## Step 5 — Instrumentation + analytics contract
Rules of thumb:
- Prefer server-side event capture for canonical behaviors; clients can send hints but not the source of truth.
- Define identity strategy early (user_id, account_id, anonymous_id) and how merges happen.
- Add automated data-quality checks: schema validation, volume deltas, null rates, dedupe rates.

## Step 6 — Discoverability (optional)
Only do this step if the platform is web-indexable and SEO matters.
- Define what is indexable vs not (noindex, robots, canonical)
- Sitemap: categories, pagination strategy, freshness cadence
- Internal linking: “related content” rules to avoid orphan pages

## Step 7 — Roadmap
Roadmap should include:
- Milestones with acceptance criteria (measurable)
- Ownership (DRI) and dependencies
- Rollout plan: canary/gradual rollout; deprecation/decommission plan

## Step 8 — Quality gate
Run `references/CHECKLISTS.md` and score with `references/RUBRIC.md`.
If any critical item fails, revise before finalizing.

