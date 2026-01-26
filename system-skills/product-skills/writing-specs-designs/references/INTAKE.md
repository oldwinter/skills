# Intake (Question Bank)

Ask **up to 5 questions at a time**, then proceed. If answers remain missing, state assumptions explicitly and offer 2–3 options.

## Minimum set (use first)
1) What product + target user/persona is this for?
2) What problem are we solving and **why now**?
3) What is the primary use case (happy path) and the 2–3 most important edge cases?
4) What platform(s) are in scope (web/iOS/Android) and what constraints exist (timeline, dependencies, policy/legal/privacy)?
5) What does success look like (1–3 metrics) and what guardrails matter (quality, trust, cost, latency)?

## Artifact selection (keep it minimal)
Choose the lightest artifact set that matches the decision:
- **Spec & Design Doc Pack (default):** you need shared clarity + build-ready interaction guidance.
- **Spec & Design Doc Pack + Prototype Brief emphasis:** the outcome depends on “feel” (interaction quality, microcopy, timing, motion, real data).

## Helpful follow-ups (pick what’s relevant)

### Users + scenarios
- Who is the primary user? Secondary users/admins?
- What is the “moment of value” and where do users currently drop off?
- What current workaround exists?
- What permissions/roles apply?

### Flow + UX constraints
- Entry points to the flow (where does it start)?
- What are required states: empty/loading/error/offline?
- What accessibility and localization constraints apply?
- What are the non-negotiable UI/brand constraints (if any)?

### Mobile-specific (tap economy)
- Which screen(s) are on the critical path to value?
- What is the maximum acceptable **taps to value** (tap budget)?
- Where will attention be most fragile (notifications, app switching, interruptions)?

### Prototype guidance (when “feel” matters)
- What decision should the prototype enable (choose between variants, validate timing, validate comprehension)?
- What fidelity is required (lo-fi, hi-fi, or in-code)?
- Can the prototype use **realistic data** (even if mocked) to avoid misleading “empty” demos?
- What is the timebox and who will review it?

### Measurement + rollout
- What leading indicator moves first if this works?
- What guardrail metrics must not regress?
- What needs to be logged/instrumented (events, properties)?
- What rollout plan is required (internal/beta/GA) and what’s the rollback trigger?

