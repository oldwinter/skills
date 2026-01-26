# Intake (question bank)

Ask 3–5 questions at a time. If answers aren’t available, proceed with explicit assumptions and provide options.

## Context + scope
1) What is the system boundary (apps/services) and who are the users/customers?
2) What are the top 1–3 pains right now (reliability, performance, cost, privacy/compliance, developer velocity, analytics/data quality, SEO)?
3) What’s the time horizon and any hard deadlines (launch, migration, contract, seasonal spike)?
4) Who are the stakeholders and decision-maker(s) (platform eng, product eng, SRE, security, PM)?

## Architecture + constraints
5) What are the key architectural constraints (data stores, tenancy model, deployment model, runtime/language, hosting)?
6) Where do you feel the biggest bottlenecks are (DB, queues, cache, build/deploy, dependencies)?
7) Any compliance/privacy constraints (PII, data residency, encryption, retention, audit)?

## Shared capabilities / platformization
8) Which capabilities are teams re-implementing repeatedly (e.g., permissions, export, filtering/search, notifications, audit logs, billing, feature flags)?
9) How many teams/services would consume the shared capability, and what are the top integration pain points today?
10) What is the desired interface: library/SDK, service/API, workflow engine, schema, UI component?

## Reliability + performance targets
11) Do you have existing SLOs/SLIs? If not, what reliability/performance does the business expect (e.g., “99.9%”, “p95 < 300ms”)?
12) What are the top user journeys that must not break (and how are they measured)?
13) What are the biggest reliability risks (single points of failure, noisy neighbors, operational gaps)?

## Scaling / “doomsday clock”
14) What growth is expected (users, traffic, data volume) and what are the known spike risks?
15) What are the current hard limits you’re worried about (DB size/IOPS, connection count, queue depth, rate limits)?
16) What’s the estimated lead time for major scaling work (weeks/months), and how much feature freeze can you tolerate?

## Instrumentation + analytics
17) How are events tracked today (client SDKs, server logs, data warehouse)? What’s broken (loss, inconsistency, identity)?
18) Which decisions depend on analytics (activation/retention, billing, compliance, experimentation)?
19) What’s the current observability posture (logs/metrics/traces, dashboards, on-call, alerts, incident history)?

## Discoverability (web platforms only)
20) Is SEO/discoverability important? If yes: are pages renderable/indexable, and do you have a sitemap/internal linking strategy?

