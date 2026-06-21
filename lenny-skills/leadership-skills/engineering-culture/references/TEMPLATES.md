# Templates (Engineering Culture Operating System Pack)

Use these templates to produce concrete deliverables. Copy/paste and fill in.

## 1) Culture + Capability Snapshot (template)

### Context
- Scope (team/org):
- Products/systems in scope:
- Stage:
- Eng size + topology:
- Remote/hybrid:
- Decision owner(s):
- Timeline / forcing function:

### Symptoms (evidence)
- Symptom 1:
  - Evidence/examples (anonymized):
- Symptom 2:
  - Evidence/examples (anonymized):
- Symptom 3 (optional):

### Current delivery system snapshot
- Release/deploy cadence:
- CI/CD maturity (tests, build time, flakes, approvals):
- Rollback strategy:
- On-call / incident process:
- Toolchain (work tracking, docs, code hosting):

### Baseline metrics (best-effort)
- Deploy frequency:
- Lead time for changes:
- Change failure rate:
- MTTR:
- PR cycle time (optional):
- Experiment throughput (optional):
- DevEx sentiment signal (optional):
- Missing instrumentation:

### Capability map (evidence-based)
| Capability bucket | Current state | Evidence | Gap | Candidate initiative |
|---|---|---|---|---|
| Technical |  |  |  |  |
| Architectural |  |  |  |  |
| Cultural |  |  |  |  |
| Management/Lean |  |  |  |  |

### Priority shifts (2–4)
1) Shift:
   - Why now:
   - What changes in behavior:
   - Leading indicators (2–3):

## 2) Engineering Culture Code (v1) (template)

Write **3–7** principles. Each principle must include observable behaviors.

### Principle <n>: <Name>
- What it means:
- Behaviors we expect:
  - Do:
  - Do:
- Behaviors we avoid:
  - Don’t:
  - Don’t:
- Decision rules (how choices get made):
- Anti-patterns (how this fails):
- How we’ll know it’s working (signals/metrics):

## 3) Org ↔ Architecture Alignment Brief (template)

### Current org + operating model
- Teams and ownership (today):
- Cross-team dependencies (today):
- Where decisions happen (today):

### Architecture + ownership boundaries
- Key components/services:
- Ownership clarity:
- Coupling hotspots:

### Conway’s Law findings (misalignments)
- Misalignment:
  - Impact:
  - Evidence:

### Proposed changes (operating model)
- Team boundary/ownership change:
  - Rationale:
  - Transition plan:
  - Trade-offs:

### Standardization (where consistency matters)
- Leveling definitions (e.g., “senior” expectations):
- Code review standards:
- Incident/retro expectations:
- Release/deploy policy:
- On-call policy:

## 4) Clock Speed + DevEx Improvement Backlog (template)

### Clock speed targets (next 4–12 weeks)
- Target deploy/release cadence:
- Target lead time:
- Guardrails (change failure rate, MTTR, quality):
- Experiment throughput target (optional):

### Bottleneck map (value stream)
- Where work gets stuck:
- Root causes:

### Prioritized backlog
| Initiative | Lever (tech/arch/culture/lean) | Impact | Effort (S/M/L) | Dependencies | Owner | Metric/leading indicator |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

### First 2-week quick wins
- Win:
  - Owner:
  - Expected signal:

## 5) Cross-functional Workflow Contract (template)

### Toolchain + shared artifacts
- Source of truth for work tracking:
- Source of truth for decisions:
- Source of truth for code + changes:

### Work flow (idea → issue → PR → deploy → learn)
1) Intake/spec:
2) Build:
3) Review:
4) Release:
5) Learn:

### Working agreements
- PR expectations (description, tests, rollout notes):
- Review SLA and escalation path:
- Merge/deploy policy (who can deploy, approvals, rollbacks):
- Experiment policy (guardrails, analysis owner):

### Non-engineer participation (if desired)
- Allowed contributions (issues, docs, config, content via PRs):
- Safety rails (review, staging, feature flags):
- Training plan:

### AI-assisted development norms
- Allowed uses:
- Required human checks:
- Documentation expectations (specs, PR context):
- “No silent changes” rule:

## 6) Rollout + Measurement Plan (template)

### 30/60/90 plan
- Next 30 days:
- Days 31–60:
- Days 61–90:

### Rituals + cadence (reinforcement)
| Ritual | Cadence | Purpose | Owner | Output artifact |
|---|---|---|---|---|
|  |  |  |  |  |

### Metrics + guardrails
- Outcome metrics (2–4):
- Leading indicators (2–4):
- Guardrails (2–4):
- Instrumentation gaps + owners:

### Risks / Open questions / Next steps
- Risks:
- Open questions:
- Next steps (smallest next actions):

