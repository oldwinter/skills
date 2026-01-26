# Templates (copy/paste)

## 1) Feature brief

### Decision / context
- **What we’re building:**  
- **Who it’s for:**  
- **Workflow step:**  
- **Why now:**  

### Job statement (one sentence)
“The LLM must …”

### Non-goals (3–5)
-  

### Success metrics (1–3) + guardrails (2–5)
- Success:  
- Guardrails (safety/trust/cost/latency):  

### Top failure modes (3–5)
-  

### Constraints
- Privacy/compliance:  
- Latency:  
- Cost:  
- Reliability:  
- Regions/platform:  

## 2) System design sketch

### Pattern + autonomy
- Pattern: assistant | copilot | tool-using agent
- Human control points (review/approve/override):

### Architecture (text diagram)
- User/UI →  
- Orchestrator/service →  
- LLM call(s) →  
- Tools (APIs) →  
- Data sources (RAG) →  
- Storage/logs →

### Context strategy
- Instructions hierarchy (system/developer/user/attachments):
- Retrieval (if any): sources, filters, ranking, citations strategy
- Tool use (if any): tool list, permissions, confirmations, rate limits
- Conflict handling: what happens when sources disagree?

### Budgets + failure handling
- Cost budget:
- Latency budget:
- Fallbacks (model/prompt/cache/human):
- Refusal/abstain behavior:

## 3) Prompt + tool contract

### System prompt
- Role:
- Goal:
- Non-goals:
- Policies (DO/DO NOT):
- How to behave when uncertain:
- Style/format rules:
- Privacy/safety rules:

### Output schema
- Format: freeform | JSON | markdown | tool calls
- JSON schema (if applicable):

### Tools (if applicable)
For each tool:
- **Name:**
- **Purpose:**
- **Inputs:**
- **Outputs:**
- **Side effects:**
- **Safety constraints:**
- **Confirmation required?:** yes/no

### Examples (at least 3)
Include:
- normal case
- tricky case
- refusal/abstain case

## 4) Data + evaluation plan

### Eval goals
- What we’re optimizing for:
- What we must avoid:

### Test set design
Create a table:
- Case ID
- Input
- Expected traits (not necessarily a single “golden” output)
- References/source of truth
- Difficulty / failure mode tag

### Rubric
Define 3–7 criteria with 1–5 scoring and clear anchors (see [RUBRIC.md](RUBRIC.md)).

### Automated checks (where possible)
- Schema validity
- Citation presence/format
- Forbidden strings/content
- Tool-call constraints

### Acceptance thresholds
- Minimum pass rate / average rubric score:
- “Must-pass” cases:

### Red-team suite
Include:
- prompt injection attempts
- data exfiltration requests
- unsafe/forbidden requests
- tool misuse attempts

## 5) Build + iteration plan

### Thin-slice prototype
- Minimal end-to-end slice:
- What’s mocked vs real:
- Instrumentation to add on day 1:

### Debug loop (prompt/data)
- When a failure occurs: reproduce → label → add to test set → fix prompt/context/tooling → re-run eval
- Track changes in a changelog (prompt version, dataset version, model version)

### Using coding agents safely
- Allowed operations (read-only vs write):
- Approval gates (before running commands, before modifying files):
- Diff size limit (suggestion):
- Tests to run:
- Code review checklist:

## 6) Launch + monitoring plan

### Rollout
- Rollout tiers: internal → beta → GA
- Exit criteria per tier:
- Rollback plan:

### Logging + monitoring
- Log fields: request ID, prompt version, model, latency, token counts, cost estimate, tool calls, safety flags, user feedback
- Dashboards: quality, escalation, latency, cost, abuse
- Alerts: thresholds and on-call owner

### Incident hooks
- What constitutes a P0/P1 incident:
- Triage steps:
- Comms template owner:

## 7) Risks / open questions / next steps

### Risks (with mitigations)
- Risk:
  - Mitigation:

### Open questions
-  

### Next steps (prioritized)
1)  

