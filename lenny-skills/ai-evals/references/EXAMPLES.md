# Examples (Outputs)

These are examples of what a good **AI Evals Pack** contains. Use them as patterns, not as copy.

## Example 1 — RAG support assistant

**SUT:** Drafts customer-support replies using retrieved KB articles.  
**Decision:** Ship/no-ship for a new prompt + retrieval policy.  
**Constraints:** No PII leakage; must cite KB; must refuse unsafe requests.

Expected artifacts:
- Eval PRD with must-pass thresholds for safety + citation presence
- Golden set tagged by topic (billing, refunds, cancellations), plus adversarial cases (jailbreaks, prompt injection)
- Taxonomy separating grounding failures (wrong citation) from safety failures (PII leakage)
- Rubric with explicit scoring for grounding, safety, and actionability
- Judge plan: automated checks (citations present, forbidden strings) + LLM/human semantic scoring
- Results report format with per-tag metrics and blocking regressions

## Example 2 — JSON extraction

**SUT:** Extracts `vendor_name`, `amount`, `currency`, `due_date` from invoices into JSON.  
**Decision:** Compare Model A vs Model B.  
**Constraints:** Always valid JSON; prioritize recall for `amount` and `due_date`.

Expected artifacts:
- Golden set schema with structured expected fields
- Automated checks for JSON validity + required keys + type checks
- Rubric dimension for “field correctness” and “null handling”
- Report with per-field precision/recall and per-severity breakdown

## Boundary example — “Add AI”

**Request:** “Add AI to our product and choose the best model.”  
Response: first define the job and success metrics (`problem-definition` / `building-with-llms`), then return for eval design once the SUT is concrete.

