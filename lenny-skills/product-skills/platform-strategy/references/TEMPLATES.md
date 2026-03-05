# Templates

Use these templates to produce the **Platform Strategy Pack** as structured sections (in chat or as files).

## 1) Platform Product Charter (template)

**Platform name:**  
**Platform type:** Internal / External / Hybrid  
**Primary users:** (who, size, segments)  
**Top jobs-to-be-done (3–5):**
- …

**User promise (1 sentence):**  

**Non-goals (3–5):**
- …

**Why now (evidence):**
- …

**Constraints:**
- Security/privacy/compliance:
- Reliability/SLOs:
- Budget/resourcing:
- Timeline/deadline:

**Assumptions (explicit):**
- …

**Success metrics (2–4 outcomes + 3–6 inputs):**
- Outcome metrics:
  - …
- Input/leading metrics:
  - …

## 2) Platform Surface & Interface Map (template)

### 2a) Surface inventory
| Capability | Owner | Consumer(s) | Interface (API/SDK/UI/CLI) | Paved road? (Y/N) | SLA/SLO | Status | Notes |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

### 2b) Boundary contract
- **Platform owns (defaults):** …
- **Domain teams own (customization):** …
- **Shared responsibilities:** …

### 2c) Default decisions (“paved road”)
List decisions the platform will make by default so consumers don’t have to:
- AuthN/AuthZ:
- Logging/observability:
- Deployment/release:
- Data access:
- Guardrails (if AI):

## 3) Lifecycle Stage & Open/Close Strategy (template)

### 3a) Stage diagnosis
Choose one stage and justify with evidence:
- **Step 0 — Conditions met:** market/organization conditions exist for a platform
- **Step 1 — Moat:** defensibility/unique assets exist for the platform owner
- **Step 2 — Open:** third parties build; incentives + governance support ecosystem growth
- **Step 3 — Close:** platform tightens control to monetize/protect core; manage partner expectations

| Stage | Evidence (bullets) | What we should do now | What to avoid |
|---|---|---|---|
|  |  |  |  |

### 3b) Open/close decisions (this quarter)
- Decision 1:
  - Options:
  - Recommendation:
  - Rationale:
  - Risks/mitigations:

## 4) Moat & Ecosystem Model (template)

### 4a) Participants + incentives
| Participant | What they want | What they contribute | Incentive we provide | Friction today |
|---|---|---|---|---|
|  |  |  |  |  |

### 4b) Compounding loop(s)
Write at least one loop as a causal chain:
- Loop A: A → B → C → A

**Leading indicators (measurable):**
- …

### 4c) Seeding plan + investment gates
- Seed actions (2–5):
  - …
- Investment gates (signals that justify more spend):
  - …

## 5) Governance & Policy Plan (template)

**What is open now:**  
**What remains closed (and why):**  

**Access + permissions model:**  
**Quotas/limits + abuse prevention:**  
**Support model:** (channels, SLAs, escalation, incident comms)  
**Docs + examples:** (what must exist before “public”)  
**Versioning + deprecation policy:**  
**Parity rules:** (first-party vs third-party access)  
**Pricing/packaging (if applicable):**  

## 6) AI context system plan (template, if relevant)

**AI use cases:**  
**Context sources:** (repos, docs, tickets, DBs)  
**Context storage/retrieval:** (indexing, freshness, permissions)  
**Experiences:** autocomplete / chat / agents / workflows (what’s shared vs separate)  
**Guardrails:** least privilege, audit logs, human approvals  
**Evaluation & monitoring:** offline evals, red-team, online metrics, incident playbook  

## 7) Metrics & Operating Model (template)

### 7a) Metrics
- North-star outcome metric:
- Input metrics (adoption, productivity, reliability):
- Guardrails (cost, abuse, privacy incidents):

### 7b) Operating model
- Platform PM/owner:
- Intake + prioritization process:
- Release/versioning cadence:
- Documentation ownership:
- Support/on-call model:
- Feedback loop (how signals reach the roadmap):

## 8) 12‑month Roadmap (template)

Use 3 horizons and keep it realistic.

### Now (0–3 months)
- …

### Next (3–6 months)
- …

### Later (6–12 months)
- …

**Dependencies:**  
**Resourcing assumptions:**  
**Rollback/exit paths:**  

