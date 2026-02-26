# Templates (copy/paste)

## 1) Trade-off brief

**Decision (one sentence):**  
**Decision owner:**  
**Decision date:**  
**Why now:**  
**Time horizon:** (e.g., 90 days / 12 months / 3 years)

**Context (2–5 bullets):**
- …

**Constraints / non-negotiables:**
- …

**Options (2–4):**
- Option A:
- Option B:
- Option C (optional):
- Do nothing (optional):

**Success metrics (1–3):**
- …

**Guardrails (2–5):** (trust, reliability, cost, latency, support load, brand, compliance)
- …

## 2) Options + criteria matrix (decision table)

Define 4–8 criteria. Prefer ordinal scoring (e.g., Low/Med/High) when uncertainty is high.

| Criterion | Definition (observable) | Weight (opt) | Option A | Option B | Notes / assumptions |
|---|---|---:|---|---|---|
|  |  |  |  |  |  |

## 3) All-in cost + opportunity cost table

Include hidden costs: integration/migrations, QA, on-call, maintenance, coordination, tooling, and switching costs.

| Cost area | Option A | Option B | Notes |
|---|---:|---:|---|
| Engineering build |  |  |  |
| Maintenance / on-call |  |  |  |
| Headcount time (non-eng) |  |  |  |
| Tools/vendors |  |  |  |
| Coordination / change mgmt |  |  |  |
| Risk cost (if fails) |  |  |  |

**Opportunity cost (what gets displaced):**
- If we pick Option A, we stop/defer: …
- If we pick Option B, we stop/defer: …

## 4) Impact ranges (order-of-magnitude)

Use ranges and confidence. Avoid fake precision; record the assumptions that drive the model.

| Option | Expected upside range | Expected downside range | Time-to-impact | Confidence (L/M/H) | Key assumptions (top 2–3) |
|---|---|---|---|---|---|
| A |  |  |  |  |  |
| B |  |  |  |  |  |

**10× check:** Which option is plausibly an order of magnitude better if assumptions hold? Which is only marginally better?

## 5) Worse-first + mitigation plan

**If we choose the “worse first” path, what dip do we expect?**
- Expected dip: …
- Why it’s worth it: …

**Leading indicators (watch weekly):**
- …

**Mitigations (what we do to manage the dip):**
- …

**Communication plan:**
- Who needs to know: …
- Message: …

## 6) Stop/continue triggers (sunk-cost reset)

**Sunk-cost reset question:** If we weren’t already doing this, would we start today? Why/why not?

**Review date:**  
**Owner:**  

**Continue if (leading indicators):**
- …

**Stop/pivot if (kill criteria):**
- …

**If we stop, what do we salvage?**
- …

## 7) Recommendation memo (final)

**Recommendation:** Choose Option A / B / C  
**Confidence:** Low / Medium / High  
**Rationale (3–6 bullets):**
- …

**Key trade-offs (explicit):**
- We optimize for: …
- We accept costs: …
- We are not optimizing for: …

**Risks (with mitigations):**
- Risk: … → Mitigation: …

**Open questions (that could change the decision):**
- …

**Next steps (owner + date):**
- …

