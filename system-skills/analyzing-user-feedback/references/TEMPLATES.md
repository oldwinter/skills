# Templates (Copy/Paste)

Use these templates to produce the **User Feedback Analysis Pack**.

## 0) Context snapshot (bullets)
- Product:
- Area/workflow in scope:
- Decision to support + deadline:
- Time window:
- Sources included:
- Sources excluded (and why):
- Segments that matter:
- Constraints (PII/internal-only):
- Time box + confidence target:
- Stakeholders/audience:
- Assumptions / unknowns:

## 1) Source inventory + sampling plan
| Source | What it contains | Time window | Volume (est.) | Sampling method | Segment coverage | Notes / access constraints |
|---|---|---|---:|---|---|---|
| Support tickets | | | | | | |
| Interviews | | | | | | |
| Surveys | | | | | | |
| Reviews/community | | | | | | |
| Usage/logs | | | | | | |

## 2) Normalized feedback table schema (CSV/Sheet)
Recommended columns:
- `item_id` (ticket ID / link / synthetic ID)
- `source` (support, survey, review, interview, sales, logs)
- `date` (or date bucket)
- `segment` (persona/tier/platform; “unknown” if missing)
- `lifecycle_stage` (onboarding/activation/daily/renewal)
- `verbatim_excerpt` (redacted; no PII)
- `primary_theme`
- `secondary_themes` (optional)
- `severity` (1–4)
- `root_cause_type` (bug/ux/docs/pricing/expectation/integration/model_quality/other)
- `impact_notes` (what breaks / what’s at risk)
- `evidence_link` (optional)

## 3) Taxonomy + codebook template

### Themes (10–20 to start)
| Theme | Definition | Includes | Excludes | Example excerpt (redacted) |
|---|---|---|---|---|
| | | | | |

### Severity scale (example)
- **1 = Minor:** annoyance; workaround exists; low impact
- **2 = Moderate:** slows task; some users blocked; support burden
- **3 = Major:** core workflow impaired; high churn/conversion risk
- **4 = Critical:** data loss/security risk; widespread outage; must-fix

### Tagging rules
- Choose **one primary theme** per item.
- Use secondary themes only if they add decision-making value.
- If unsure, tag as `Needs review` and add a short note.

## 4) Themes & evidence report

### Theme 1 — <name>
**Summary:** <1–2 sentences>  
**Who is impacted:** <segments/lifecycle stages>  
**Frequency:** <count or %; note sampling limitations>  
**Severity/impact:** <what breaks; risks>  
**Root causes (hypotheses):**
- …
**Representative evidence (redacted):**
- “...” (source/date)
- “...” (source/date)
**Confidence:** High / Medium / Low (and why)

## 5) Recommendations + learning plan

### Recommended actions (ranked)
| Rank | Action | Type (bug/ux/docs/product/messaging) | Theme(s) | Expected impact | Owner (if known) | Time horizon | Evidence |
|---:|---|---|---|---|---|---|---|
| 1 | | | | | | | |

### Open questions (to de-risk)
1) Question:
   - Why it matters:
   - Fastest way to answer:
   - Data needed:

## 6) Feedback loop plan
| Activity | Cadence | Owner(s) | Inputs | Output | Notes |
|---|---|---|---|---|---|
| Feedback intake + tagging | | | | Updated table | |
| Theme review | | | | Updated themes | |
| Engineering support rotation | | | | Faster fixes + shared context | |
| Stakeholder share-out | | | | Monthly VoC update | |

## 7) Risks / Open questions / Next steps (required)

### Risks
- …

### Open questions
- …

### Next steps
1) …
2) …

