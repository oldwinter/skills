# Templates

Use these templates to produce a **Technology Evaluation Pack** as either:
- A single document with sections, or
- Multiple files (recommended) under a folder like `docs/tech-evals/<initiative>/`.

## 1) Evaluation Brief (template)

### Summary
- **Decision to make:** (adopt / replace / build / defer)
- **Candidate technology:** (vendor/product/version; links)
- **Owner:** (DRI)
- **Decision deadline:** (date)
- **Stakeholders:** (security, eng, data, legal, ops, end users)

### Problem and context
- **Problem statement (1 sentence):**
- **Who experiences the pain:** (personas/teams)
- **Current approach/stack:** (what exists today)
- **What’s broken / too slow / too expensive / too risky:**
- **Non-goals:** (3–5 bullets)

### Success and constraints
- **Success metrics (leading):**
- **Success metrics (lagging):**
- **Hard constraints:** (privacy/compliance, data residency, deployment model, integrations)
- **Deal breakers:** (explicit “no” criteria)
- **Assumptions:** (explicit; mark as to-verify)

## 2) Options & Criteria Matrix (template)

### Options
List options including **status quo**:
- Option A: Status quo
- Option B: Vendor 1
- Option C: Vendor 2
- Option D: Build
- Option E: Hybrid

### Criteria (example set)
Use a 1–5 score (or pass/fail) and add weights if needed.

| Criterion | Weight | How we measure | A: Status quo | B: Vendor 1 | C: Vendor 2 | D: Build | Notes |
|---|---:|---|---:|---:|---:|---:|---|
| Problem fit |  |  |  |  |  |  |  |
| Workflow impact (ROI) |  |  |  |  |  |  |  |
| Time-to-value |  |  |  |  |  |  |  |
| Integration complexity |  |  |  |  |  |  |  |
| Security/privacy/compliance |  |  |  |  |  |  |  |
| Reliability/operability |  |  |  |  |  |  |  |
| Total cost of ownership |  |  |  |  |  |  |  |
| Lock-in / exit path |  |  |  |  |  |  |  |

### Integration + data fit notes (required)
- **Required integrations:** (SSO, RBAC, audit logs, APIs/webhooks, data pipelines)
- **Data flow (inputs → processing → outputs):**
- **Migration effort:** (backfills, schema changes, downtime tolerance)
- **Exit plan:** (export formats, deletion, switching costs)

## 3) Build vs Buy Analysis (template)

### Decision frame
- **What we would build (bounded scope):**
- **What we would buy (vendor scope):**
- **What we would not do (non-goals):**

### Bandwidth / TCO ledger
Model “bandwidth” as cost (not just dollars).

| Cost area | Build (estimate) | Buy (estimate) | Notes |
|---|---:|---:|---|
| Initial build/implementation |  |  |  |
| Ongoing maintenance/upgrades |  |  |  |
| On-call/incident response |  |  |  |
| Security/compliance work |  |  |  |
| Vendor management/procurement |  |  |  |
| Opportunity cost |  |  |  |

### Core competency check
- Is this a differentiator for our business? Why/why not?
- If we build, do we have the expertise to do it well?
- If we buy, are we comfortable with vendor dependency and roadmap control?

## 4) Proof-of-Value Pilot Plan (template)

### Hypotheses
- H1:
- H2:
- H3:

### Scope and timeline
- **Pilot scope (in/out):**
- **Pilot duration:** (time-boxed)
- **Pilot users:** (who + how many)
- **Environment:** (sandbox/staging/production slice)

### Measurement
- **Success metrics + thresholds:**
- **Data collection plan:** (logs, analytics, surveys, time studies)
- **Evaluation method:** (A/B, before/after, rubric scoring, red-team suite)

### Operational + safety plan
- **Permissions model:** (who can do what)
- **Human approval points:** (what requires review)
- **Rollback plan:** (how to revert)
- **Data deletion/retention plan:** (if pilot is stopped)

### Exit criteria (binary)
- Adopt if:
- Iterate if:
- Reject if:

## 5) Risk & Guardrails Review (template)

### Risk register (top 5–10)

| Risk | Likelihood | Impact | Owner | Mitigation | Status (ok / monitor / blocker) |
|---|---:|---:|---|---|---|
|  |  |  |  |  |  |

### Security/privacy/compliance prompts
- What data is processed (PII, secrets, IP)? Where does it flow?
- Required controls: SSO, RBAC, audit logs, encryption, retention/deletion, data residency.
- Evidence to request: SOC2/ISO, pen test summary, DPA, sub-processors, incident process.

### AI-specific guardrails guidance (if relevant)
- Do not rely on “guardrails catch everything” as a primary security layer.
- Assume determined attackers will try prompt injection / jailbreaks.
- Prefer defense-in-depth: least privilege, logging, human approvals, eval/red-team, safe fallbacks.

## 6) Decision Memo (template)

### Recommendation
- **Decision:** (adopt vendor X / build / defer)
- **Why this option wins:** (3–5 bullets)
- **Key trade-offs:** (what we give up)

### Evidence summary
- What evidence supports the recommendation (pilot results, demos, references)?
- What assumptions remain unverified?

### Adoption plan (if adopting)
- Scope of rollout (teams/products)
- Timeline and milestones
- Owners/DRIs
- Training/change management
- Monitoring (quality, cost, reliability)

### Rollback / exit plan
- How we revert if quality/cost/risk is unacceptable
- Data export/deletion steps
- Contract/renewal guardrails (avoid accidental lock-in)

### Risks / Open questions / Next steps
- **Risks:** (top risks + owner)
- **Open questions:** (what must be answered next)
- **Next steps:** (1–5 concrete actions with owners/dates)

