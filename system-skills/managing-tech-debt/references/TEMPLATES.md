# Templates

Use these templates to produce a **Tech Debt Management Pack**. Output in-chat by default, or write to files if requested.

## 1) Context snapshot
**System(s) in scope:**  
**Owner(s):**  
**Stakeholders / decision-maker(s):**  
**Time horizon + deadlines:**  
**Primary pains (top 3):**  
**User-visible symptoms (top 3):**  
**Constraints:** (capacity, compliance, freeze windows, uptime/SLO)  
**Success definition:** (what changes; measurable if possible)  
**Assumptions:** (if any)  

## 2) Tech Debt Register (table)
| ID | Area | Debt item | Symptoms | User impact | Risk (reliability/security) | Velocity tax | Effort (range) | Dependencies | Owner | Recommended strategy |
|---:|------|-----------|----------|-------------|------------------------------|--------------|----------------|--------------|-------|----------------------|
| 1 | | | | | | | | | | |

## 3) Scoring model + prioritized list
### Scoring model
- User impact (1–5):
- Reliability risk (1–5):
- Security/compliance risk (1–5):
- Velocity tax (1–5):
- Effort (1–5 or t-shirt):
- Notes on sequencing/dependencies:

### Prioritized list (top 10)
| Rank | Debt ID | Score summary | Why now | Milestone/next action |
|-----:|--------:|---------------|--------|------------------------|
| 1 | | | | |

## 4) Strategy decision memo (refactor vs migrate vs rebuild vs deprecate)
**Decision to make:**  
**Context / problem:**  
**Options considered:** (A/B/C)  
**Evaluation criteria:** (impact, risk, time-to-value, migration complexity, dual-run cost, operability, maintainability)  
**Recommendation:**  
**Rationale:** (evidence + constraints)  
**Migration phases (if applicable):**
1) Phase 0 (instrumentation / prep):
2) Phase 1 (thin-slice / adapter / parallel path):
3) Phase 2 (cutover plan):
4) Phase 3 (decommission plan):
**Dual-run plan:** (what runs in parallel; expected duration; staffing/on-call impact)  
**Rollback plan:** (how to revert; triggers)  
**Risks / mitigations:**  

## 5) Execution plan (milestones)
| Milestone | Outcome | Scope | Owner | ETA (range) | Acceptance criteria | Stop/rollback condition |
|-----------|---------|-------|-------|-------------|---------------------|--------------------------|
| M1 | | | | | | |

Capacity model:
- Default: reserve __% of sprint capacity for debt (adjust as needed)
- One-time spikes: instrumentation/migration windows

## 6) Metrics plan
**Baseline (today):**  
- Incident rate / severity:
- MTTR:
- p95 latency (key endpoints):
- Deploy frequency:
- Lead time / cycle time:
- Support volume (if relevant):

**Targets (by horizon):**  
**Leading indicators:** (e.g., build time, test flakiness, deploy success rate)  
**Guardrails:** (e.g., error rate, latency, cost)  
**Instrumentation gaps + owners:**  
**Small tests to validate value:** (what, how long, success criteria)  

## 7) Stakeholder cadence
**Audience:**  
**Cadence:** weekly / biweekly / monthly  
**Update format:** 5 bullets + metrics snapshot + risks + asks  
**Decision gates:** (e.g., approve rebuild, approve cutover, approve decommission)  

## 8) Risks / Open questions / Next steps
**Risks:**  
**Open questions:**  
**Next steps (1–3):**  

