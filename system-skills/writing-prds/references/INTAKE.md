# Intake (Question Bank)

Ask **up to 5 questions at a time**, then proceed. If answers remain missing, state assumptions explicitly and offer 2–3 options.

## Minimum set (use first)
1) What product + primary user segment is this for?
2) What problem are we solving and **why now**?
3) What decision needs to be made (build now vs later, scope, approach) and who is the DRI/approver?
4) What does success look like (1–3 metrics) and what guardrails matter (quality, trust, cost, latency)?
5) Constraints: deadline, dependencies, platform (web/mobile), policy/legal/privacy constraints.

## Artifact selection
Choose the lightest artifact set that matches the decision:
- **PR/FAQ only:** you need narrative alignment and a “should we do this?” decision.
- **PRD only:** the narrative is already aligned; you need execution-ready requirements.
- **PR/FAQ → PRD:** you need both narrative alignment and delivery clarity.
- **PRD + Prompt Set + Eval Spec:** AI feature where behavior must be testable and continuously evaluated.

## Helpful follow-ups (pick what’s relevant)

### Users + use cases
- Primary user persona(s) and their “job to be done”?
- Primary use case (happy path) and top 3 edge cases?
- Current workaround (what do users do today)?
- Who is harmed if we get this wrong (trust/safety risk)?

### Scope + constraints
- What is explicitly **out of scope** for v1?
- Hard constraints (time, headcount, platform, compliance)?
- Dependencies (teams/systems) and required approvals?

### Requirements details
- What are the must-have behaviors vs nice-to-have?
- Non-functional requirements: latency, uptime, privacy, accessibility, localization?
- Migration/backwards compatibility needs?

### Metrics + instrumentation
- What leading indicator will change first?
- What guardrail metrics must not regress?
- Where will data come from (events, logs, BI tables) and what’s missing today?

### Rollout + comms
- Target launch window and launch tiers (internal/beta/GA)?
- Rollback plan if metrics regress?
- Customer-facing messaging (docs, support, marketing) needed?

### AI-specific (if applicable)
- Model type and architecture assumptions (LLM, RAG, tools, fine-tune)? (High level only; no secrets.)
- What must the model never do (policy, privacy, safety)?
- Concrete examples: 5 good outputs + 5 bad outputs?
- Evaluation approach: offline golden set, LLM judge, human review, online A/B?
- Tolerance for hallucinations/errors (what’s acceptable vs critical)?

