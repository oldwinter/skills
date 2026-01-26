# Intake (Question Bank)

Ask **3–5 questions at a time**, starting from Tier 1. If answers aren’t available, proceed with **explicit assumptions** and offer 2–3 options.

## Tier 1 — Minimum viable context
1) What is the product today, and who is the target user/customer segment?
2) What job/pain are we solving, and what evidence do we have (tickets, calls, metrics, anecdotes)?
3) What decision are we making and by when? (single feature vs portfolio vs platform)
4) What constraints matter most? (budget, latency, policy/legal, privacy, data access, regions, platforms)
5) What are 1–3 success metrics and 2–5 guardrails? (safety/trust, cost, latency, quality)

## Tier 2 — AI-specific strategy inputs
6) What is the intended form factor: assistant, copilot, or agent? Where does it live in the workflow?
7) What actions (if any) is the system allowed to take? What actions must always require human approval?
8) What are the “must-not-do” constraints? (privacy, IP, safety, compliance, brand trust)
9) What are the top failure modes you worry about? (hallucination, wrong action, prompt injection, data leakage)
10) What is the rollout risk tolerance? (internal only, beta, GA; regulated users; high-stakes domains)

## Tier 3 — Differentiation and defensibility
11) What assets do we have that could compound? (unique data, distribution, workflow surface area, brand trust)
12) What alternatives do users have today (manual workarounds, competitors, “just use ChatGPT”)?
13) What is the “why now”? What changed (capability, market, regulation, distribution) that makes this timely?

## Tier 4 — Execution readiness
14) What data can we use (and what can’t we use)? Who owns governance and retention policies?
15) What eval/quality bar must we hit before expanding rollout? What is the baseline today?
16) Who are the owners/DRIs for product, eng, ML, security, legal/compliance, and support?

## Default assumptions (use only if missing)
- Horizon: 6 months; rollout: internal → beta → GA.
- Form factor: start with copilot before agent unless action-taking is a hard requirement.
- Guardrails: no sensitive data leakage, predictable latency, cost cap, clear user control/undo.

