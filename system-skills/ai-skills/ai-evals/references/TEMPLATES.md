# Templates

Copy/paste the following templates when producing an **AI Evals Pack**.

## 1) Eval PRD (Evaluation Requirements)

### 1. Overview
- **Decision:** (ship/no-ship | compare A vs B | regression gate)
- **System under test (SUT):** (what the AI does; inputs → outputs)
- **Users/workflow:** (where it appears; human review points)
- **Constraints:** (privacy/compliance, safety policy, languages, cost/latency budgets)

### 2. Scope and non-goals
- **In scope:**
- **Out of scope:**

### 3. Target behaviors (requirements)
- **Must do (3–10):**
- **Must not do (3–10):**

### 4. Metrics and acceptance thresholds
- **Primary metric(s):**
- **Secondary metric(s):**
- **Blocking thresholds (must-pass):**
- **Non-blocking targets:**

### 5. Evaluation approach
- **Judge type(s):** (human | LLM judge | automated checks)
- **Scoring mode:** (absolute | pairwise)
- **Run cadence:** (one-time | per release | daily)

### 6. Data plan
- **Data sources:** (logs, synthetic, curated)
- **Privacy handling:** (redaction/anonymization rules)
- **Coverage targets:** (segments, languages, edge/safety)

### 7. Ownership + timeline
- **Owners:** (PM/Eng/ML/QA)
- **Timeline:** (dates or milestones)

## 2) Golden set schema (recommended JSONL fields)

Use either a markdown table or JSONL. Recommended fields:
- `id` (string)
- `input` (string or structured object)
- `context` (optional: retrieved passages, tool outputs, policy constraints)
- `expected` (optional: expected label/fields; for open-ended tasks rely on rubric)
- `tags` (list of strings; include scenario + severity)
- `severity` (`low` | `medium` | `high` | `critical`)
- `notes` (string; what this case is testing)

Example (JSONL):
```json
{"id":"CASE_001","input":"...","expected":{"must_include":["..."],"must_not_include":["..."]},"tags":["billing","refund","high_severity"],"severity":"high","notes":"Tests refund policy compliance."}
```

## 3) Open coding worksheet (error analysis)

| Case ID | Observed output (summary) | What’s wrong (1 sentence) | Proposed labels | Severity | Root-cause hypothesis | New/updated test? |
|---|---|---|---|---|---|---|
| CASE_001 | … | … | … | high | … | add |

## 4) Rubric (scoring guide)

Define 3–7 dimensions. Example dimensions:
- **Task success:** does it solve the user’s ask?
- **Correctness/grounding:** factual, consistent with provided context
- **Completeness:** covers required parts; no key omissions
- **Safety/compliance:** refuses unsafe; no disallowed content; no PII leakage
- **Format/structure:** valid JSON/schema; follows output constraints

Rubric template:
| Dimension | Score scale | “Pass” definition | “Fail” definition | Notes/examples |
|---|---|---|---|---|
| Task success | 0–2 | … | … | … |

## 5) LLM-as-judge prompt (skeleton)

Use this only if LLM-as-judge is acceptable and data is safe to share with the judge model.

**System:** You are a strict evaluator. Follow the rubric. Do not be lenient. Output valid JSON only.

**User:**
- **Rubric:** <paste rubric table or bullet definitions>
- **Input:** <test case input + any context>
- **Model output:** <candidate output>

Return JSON:
```json
{
  "scores": {"task_success": 0, "correctness": 0, "safety": 0, "format": 0},
  "overall_pass": false,
  "reasons": ["..."],
  "tags": ["..."]
}
```

## 6) Results report (decision-ready)

### Summary
- **What was evaluated:** (version, prompt, model)
- **Overall result:** (pass/fail vs thresholds)
- **Top regressions:** (3–5 bullets)
- **Top improvements:** (3–5 bullets)

### Metrics
- **Overall:** (table)
- **By tag/segment:** (table; include critical tags)

### Failure review
- **Top failure categories:** (from taxonomy)
- **Representative examples:** (1–2 per category)
- **Recommended fixes:** (prompt/tooling/data)

### Decision + next iteration
- **Decision recommendation:** (ship/no-ship; what to change)
- **New tests to add:** (list)
- **Risks / Open questions / Next steps**

