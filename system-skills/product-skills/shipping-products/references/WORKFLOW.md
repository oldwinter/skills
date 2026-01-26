# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with heuristics and defaults that help you ship faster without breaking trust.

## Principles (from the source skill)
- **Speed is a craft signal**: high output velocity usually comes from competence and clean systems, not recklessness.
- **Speed enables feedback**: shipping sooner yields faster learning.
- **Speed and stability move together**: smaller, more frequent changes reduce blast radius.
- **A PQL is a factory inspection**: a standard checklist catches repeat failures and improves over time.
- **“Ship tomorrow” is a forcing function**: it reveals the critical path and exposes avoidable blockers.

## Step 1 — Define “shipped”
Heuristics:
- Write a 1-sentence “ship statement”: *what* + *who* + *when* + *rollout*.
- If you can’t state “who gets it first”, you don’t have a rollout plan yet.

Useful outputs:
- Scope + non-goals
- Stakeholder list and owners

## Step 2 — Pick a rollout strategy that makes the change small
Defaults:
- Prefer a **flagged rollout** over a “big bang” release.
- Prefer **phased exposure**: internal → beta → staged % → GA.
- Prefer **small slices** that each deliver a coherent user outcome.

Anti-patterns:
- Shipping “backend now, UX later” while users can’t complete an end-to-end flow
- Large batch releases that combine multiple risk types (migrations + UI + pricing)

## Step 3 — “Maximally accelerated” without being reckless
How to use the forcing function:
- Ask: “If we had to ship tomorrow, what would we do?”
- Then translate into: “Given our real constraints, what’s the fastest safe path?”

What often falls out:
- Missing decision owners
- Over-cautious sequencing that doesn’t reduce risk
- Dependencies that are “nice to have” but not required for the first slice

## Step 4 — PQL + acceptance criteria
Guidance:
- Make the PQL a **living document**: every escape (bug/incident) adds or improves a check.
- Separate **stop-ship** items from “follow-up after launch” items.

PQL categories:
- Correctness (happy path + key edge cases)
- UX states and clarity (loading, empty, error)
- Security/privacy/compliance
- Performance/reliability
- Observability (logs/metrics/traces)
- Support readiness (docs, macros, known issues)

## Step 5 — Monitoring + rollback
Rules of thumb:
- If you can’t roll back, you must ship smaller.
- Define **stop-the-line triggers** before launch (not after the metric drops).
- Ensure dashboard ownership: a name, not “the team”.

## Step 6 — Comms + enablement
Defaults:
- **Internal first**: align Sales/Support/Success before customers hear about it.
- Provide “what changed / why it matters / how to use / known issues / how to get help”.

## Step 7 — Go/No-go
Good go/no-go is not a meeting; it’s a **checklist**:
- Everyone reviews async
- Only unresolved blockers require sync time

## Step 8 — Post-launch
Retro prompts:
- What surprised us? What did we miss?
- What was the highest-leverage decision we made?
- What should become a standard (PQL item / automation / comms pattern)?

