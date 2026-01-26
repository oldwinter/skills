# Templates (Managing Timelines)

Copy/paste these templates to produce a Timeline Management Pack.

## 1) Timeline Management Pack (full outline)

```md
# Timeline Management Pack — <project / initiative>

## 1) Deadline & commitment model
- Date type: (fixed external / fixed internal / target / window)
- Why now:
- Decision owner (date/scope trade-offs):
- Commitment ladder:
  - Commitment (what we will deliver) + date:
  - Forecast (best estimate) + date:
  - Target (directional) + date:
- Confidence: (H/M/L) + top 3 risks:
- What is variable (scope/resources/quality/date):

## 2) Phase plan (with decision gates)
| Phase | Start | End | Output(s) | Decision gate (what must be true to proceed) | Date type (commit/forecast/target) |
|---|---:|---:|---|---|---|
| Discovery |  |  |  |  |  |
| Solutioning |  |  |  |  |  |
| Build |  |  |  |  |  |
| Launch |  |  |  |  |  |

Next commitment date (re-forecast checkpoint):

## 3) Milestone tracker + RAG
RAG definitions:
- Green:
- Yellow:
- Red:

| Milestone | Deliverable | Owner | Target date | Confidence (H/M/L) | RAG | Dependencies | Notes / next decision |
|---|---|---|---:|---|---|---|---|
|  |  |  |  |  |  |  |  |

## 4) Governance cadence
- Update cadence: (weekly default)
- Forum(s): (weekly review, standup, async doc)
- Weekly review agenda:
  1) RAG review (yellow/red)
  2) Decisions needed (by when)
  3) Scope changes + trades
  4) Next week plan
- Escalation triggers (what makes something yellow/red):
- Decision log link/location:

## 5) Scope & change-control plan
- Non-goals (explicitly out):
- Cut list (pre-approved trade-offs):
  - Cut first:
  - Cut next:
  - Never cut (non-negotiables):
- Freeze points:
  - Scope freeze:
  - Code freeze:
  - QA / launch readiness freeze:
- Change control rule (“trade, don’t add”):
  - Decision owner:
  - Evaluation criteria:
  - What gets traded off first:

## 6) Stakeholder comms pack
Weekly update template:
- Status (RAG):
- What changed since last update:
- This week’s progress:
- Next week’s plan:
- Risks (top 3):
- Decisions needed (owner + deadline):
- Scope changes (what we traded):

Escalation note template (when red):
- What is red and why:
- Impact if unchanged:
- Options:
  1) Cut scope:
  2) Add resources:
  3) Move date:
  4) Reduce quality (if allowed):
- Recommended option + decision needed by:

## 7) Risks / Open questions / Next steps
**Risks:**
- ...

**Open questions:**
- ...

**Next steps (owners + dates):**
- ...
```

## 2) Commitment language snippets (copy/paste)

```md
### Date language
- Commitment: “We will deliver <X> by <D> provided <assumptions>. If <risk> happens, we will <trade-off>.”
- Forecast: “Based on what we know today, we expect <D>. Confidence: <H/M/L>. Next update: <date>.”
- Target: “Our goal is <D>. We will confirm a commitment after <gate>.”
```

## 3) Decision log (simple)

```md
| Date | Decision | Decision owner | Context / rationale | Follow-ups (owner/date) |
|---:|---|---|---|---|
|  |  |  |  |  |
```

## 4) Risk register

```md
| Risk | Impact | Probability | Mitigation | Owner | Trigger / early signal | Status |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
```

## 5) Change request (for scope control)

```md
### Change request
- Request:
- Why now:
- User impact:
- Cost (rough):
- Suggested trade-off (what to cut/defer):
- Decision owner:
- Decision needed by:
```

## 6) AI/ML outer-loop milestone prompts (only if applicable)
- Evaluation harness + acceptance metrics defined?
- Data readiness + privacy review complete?
- Safety/guardrails + fallback behavior defined?
- Monitoring + alerting + on-call/runbook ready?
- Gradual rollout plan (canary/beta) + rollback plan?

