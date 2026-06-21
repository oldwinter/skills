# Plan Schema

Use this schema when a machine-readable workflow plan helps coordination. Keep `plan.md` as the human source of truth.

```json
{
  "goal": "string",
  "success_criteria": ["string"],
  "constraints": ["string"],
  "risks": [
    {
      "risk": "string",
      "approval_required": true,
      "mitigation": "string"
    }
  ],
  "budgets": {
    "max_concurrent_agents": 4,
    "max_total_agents": 12,
    "time_minutes": null,
    "token_budget": null
  },
  "packets": [
    {
      "id": "01-discovery",
      "objective": "string",
      "context": "string",
      "files_or_sources": ["string"],
      "ownership": "string",
      "do": ["string"],
      "do_not": ["string"],
      "expected_output": "string",
      "verification": ["string"],
      "status": "pending",
      "assignee": "parent|subagent|simulated",
      "result": "results/01-discovery.md or null"
    }
  ],
  "integration_policy": {
    "owner": "parent",
    "conflict_resolution": "Inspect authoritative sources before choosing.",
    "final_output": "string"
  },
  "verification": [
    {
      "check": "string",
      "command": "string or null",
      "required": true,
      "status": "pending",
      "evidence": "string"
    }
  ],
  "reusable_artifacts": ["string"]
}
```

Suggested defaults:

- `max_concurrent_agents`: 2-4 for normal work.
- `max_total_agents`: 6-12 unless the user approves a larger run.
- Packet IDs: prefix with two digits so files sort naturally.
- Status values: `pending`, `in_progress`, `complete`, `blocked`, `skipped`.
- `state.slug` should match the `.workflow/<slug>` directory name.
- Packet IDs in `state.json` should be unique and match non-empty files under `packets/`.
- Packet `result` paths should be relative `results/*.md` paths whose stem matches the packet ID.
- Use `scripts/verify_workflow.py .workflow/<slug> --require-all-results` before final fan-in.
