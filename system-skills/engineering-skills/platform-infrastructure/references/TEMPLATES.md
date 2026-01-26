# Templates

Use these templates to produce the **Platform & Infrastructure Improvement Pack**.

## 1) Context snapshot

### Context snapshot
- **System(s) in scope:**
- **Users/customers:**
- **Primary pains (1–3):**
- **Time horizon / deadline:**
- **Stakeholders / decision-maker(s):**
- **Constraints (security/compliance, staffing, risk tolerance):**
- **Assumptions (explicit):**
- **Success definition (measures):**
- **Non-goals / out of scope:**

## 2) Shared capabilities inventory + platformization plan

### Shared capabilities inventory (table)
| Capability | Current duplication (where/how) | Consumer teams/services | Proposed platform contract (API/schema/SDK) | Migration approach | Expected impact | Risks |
|---|---|---:|---|---|---|---|
|  |  |  |  |  |  |  |

### Platformization decisions
- **What becomes a shared primitive (and why):**
- **What remains product-specific (and why):**
- **Ownership model (platform team vs shared ownership):**
- **Versioning + backwards compatibility plan:**

## 3) Quality attributes spec (SLOs/SLIs + privacy/safety)

### Quality attributes spec
- **Reliability targets:** (availability/error rate)  
- **Performance targets:** (p95/p99 latency, throughput)  
- **Privacy/safety requirements:** (encryption, residency, retention, audit)  
- **Operability requirements:** (dashboards, alerts, runbooks, on-call)  
- **Cost guardrails:** (budgets, top drivers, caps)  

### Proposed SLOs/SLIs (table)
| User journey / API | SLI | SLO target | Measurement method | Owner | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 4) Scaling “doomsday clock” + capacity plan

### Doomsday clock (table)
| Component/limit | Metric | Current | Trigger threshold | Estimated lead time to mitigate | Mitigation project | Owner |
|---|---|---:|---:|---|---|---|
|  |  |  |  |  |  |  |

### Capacity plan
- **Top scaling risks:**
- **Proposed scaling projects (sequenced):**
- **Feature-freeze / priority policy when triggers fire:**

## 5) Instrumentation plan (observability + server-side analytics)

### Observability gaps
| Area | Current state | Gap | Proposed instrumentation | Owner | Priority |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Server-side analytics event contract
- **Canonical identity fields:** (user_id, account_id, anonymous_id) + merge rules
- **Delivery semantics:** (at-least-once vs exactly-once), dedupe strategy
- **Schema/versioning:** how event changes are managed
- **Data QA checks:** schema validation, volume anomaly checks, null-rate checks

### Event taxonomy (starter table)
| Event name | When emitted (server action) | Required properties | Identity fields | Consumers (teams) | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 6) Discoverability plan (optional, web platforms)

### Discoverability plan
- **Indexability rules:** (noindex, robots, canonical)
- **Sitemap strategy:** categories, pagination, freshness cadence
- **Internal linking rules:** “related content”, avoid orphan pages
- **Validation plan:** crawl simulation, sample URLs, monitoring

## 7) Execution roadmap

### Roadmap (table)
| Milestone | Scope | Acceptance criteria | Owner | Dependencies | ETA range | Rollout/rollback |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 8) Risks / Open questions / Next steps

### Risks
- 

### Open questions
- 

### Next steps
- 

