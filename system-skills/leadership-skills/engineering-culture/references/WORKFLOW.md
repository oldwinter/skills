# Expanded Workflow Notes (Engineering Culture)

Use this file when you need more guidance than the step list in `SKILL.md`.

## A) Treat culture as a delivery system (capabilities model)
Map the current state across four capability buckets (from DevOps research and practice):
- **Technical capabilities:** CI reliability, automated testing, build/deploy automation, observability, feature flags.
- **Architectural capabilities:** loose coupling, clear ownership boundaries, stable interfaces, evolvable architecture.
- **Cultural capabilities:** ownership, collaboration, blameless learning, willingness to simplify, attention to customer impact.
- **Management/lean capabilities:** small batches, WIP limits, clear priorities, fast feedback loops, continuous improvement rituals.

Output: a **capability map** with evidence and gaps, not slogans.

## B) Evidence collection (keep it lightweight)
Prefer quick signals over heavy process:
- 2–5 anonymized examples per symptom
- A “value stream” timeline for 1–2 recent changes (idea→prod→learn)
- A minimal baseline of metrics (DORA if available; otherwise best-effort proxies)
- A quick coupling/ownership scan (where everything depends on everything)

If evidence is missing, label assumptions and propose an instrumentation spike as a backlog item.

## C) Conway’s Law analysis (org ↔ architecture fit)
1) Draw a simple map of teams and their dependencies (who blocks whom).
2) Draw a simple map of architecture ownership boundaries (what team owns what).
3) Identify misalignments:
   - multiple teams editing the same critical area
   - unclear owner for shared components
   - platform as a bottleneck without a product interface
4) Propose changes:
   - adjust boundaries/ownership
   - define explicit interfaces (APIs, contracts, SLAs)
   - standardize policies where inconsistent expectations create friction (leveling, on-call, code review, incident process)

## D) Clock speed (safe shipping + experimentation)
Define clock speed using a small set of concrete targets:
- Deploy frequency (or release frequency)
- Lead time for changes (idea→prod)
- Change failure rate + MTTR (guardrails)
- Experiment throughput (experiments shipped per week; time-to-learn)

Then identify bottlenecks and propose improvements:
- “Make CI boring”: reduce flakes, shorten builds, stabilize test suite
- Progressive delivery (canaries, feature flags, staged rollouts)
- Improve observability and rollback confidence
- Reduce batch size and normalize incrementalism

## E) Cross-functional workflow contract (shared toolchain)
The goal is not “make everyone code.” The goal is **shared visibility and shared operating rhythms**.

Define:
- Where work lives (issues, docs, PRs) and who is responsible for updates
- Expectations for PR descriptions, review SLAs, and decision logging
- How non-engineers contribute safely (issues, copy/config changes, feature flags, content via PRs)
- How experimentation is requested, built, launched, and analyzed (owner, approval, guardrails)

## F) AI-assisted development norms (humans as architects)
Make norms explicit so adoption increases quality rather than chaos:
- Allowed uses (boilerplate, tests, refactors, scaffolding, documentation, migration helpers)
- Required human checks (design intent, security/privacy, correctness, integration, performance)
- “No silent changes” rule: AI-authored code requires clear diffs, tests, and reviewer context
- Parallelization norms: async handoffs, spec-first tickets, multiple agents in parallel with a human integrator

## G) Rollout and reinforcement
Treat this like a change program, not a document:
- Pick 1–2 rituals to start (weekly delivery review, blameless retro, architecture/ownership review)
- Train on the workflow contract (especially for non-engineers if included)
- Add lightweight measurement and publish progress
- Make “standardization” explicit: what is optional vs required across teams

