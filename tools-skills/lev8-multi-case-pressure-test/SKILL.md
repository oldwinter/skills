---
name: lev8-multi-case-pressure-test
description: Run Lev8 multi-case browser pressure tests from CSV or tabular case files. Use when Codex needs to launch multiple fresh Chrome tabs for Lev8/ci-app.lev8.com, submit one query per case, handle Search Plan / Run search plan follow-up loops, verify right-side live result tables, and produce a concise E2E pressure-test summary.
---

# Lev8 Multi-Case Pressure Test

Use this skill to execute controlled Lev8 end-to-end pressure tests with several cases running concurrently in Chrome.

## Required Pairing

Use `chrome:control-chrome` for browser work. Read that skill before touching Chrome, bootstrap the Codex Chrome Extension through its documented Node runtime, and call `browser.tabs.finalize({ keep })` once at the end.

Do not let many subagents control the same Chrome profile at the same time. If the user asks for "subagents" or "multiple tabs", use one Chrome control session to create and drive many fresh tabs concurrently, and optionally use a read-only subagent for checklist or report validation.

## Workflow

1. Parse cases.
   - For CSV, use `scripts/extract_cases.py`.
   - Default to the last CSV column as `query` unless the user names another column.
   - Treat physical line count as unreliable because quoted CSV fields can contain newlines.
   - Keep case metadata: `case_index`, `scenario_id`, `ID`, `query`, and `query_preview`.

2. Prepare Chrome.
   - Ignore existing task tabs for the actual run.
   - Use existing tabs only to infer the logged-in Lev8 workspace URL if the user did not provide it.
   - Prefer `https://ci-app.lev8.com/workspace/<workspace_id>` as the launch URL.
   - Name the session clearly, then create fresh tabs for this run.

3. Submit cases concurrently.
   - Create `N` new tabs, one per case.
   - Open the workspace URL in each tab.
   - Fill `div.chat-rich-input[contenteditable="true"]` with the query.
   - Click `button.send-button`.
   - Record the resulting session URL, title, tab id, and submit timestamp.

4. Monitor and continue.
   - Short-poll tabs; avoid one long tool call that can exceed the tool timeout.
   - Detect Search Plan with page text such as `Search setup`, `Search criteria`, or `Search Plan`.
   - Detect runnable plans with `button.search-plan-run` or visible text `Run search plan`.
   - When a runnable plan appears, click it and record `continued_after_plan=true`.
   - If the page asks for more info or only shows a shell, send a second-round prompt:

```text
Please proceed with the current request. If any details are missing or the query was truncated, make reasonable assumptions, choose a practical target result count, and generate a concrete search plan that I can run.
```

   - If that still stalls, resend the exact original query with this stricter prompt:

```text
Use this exact query as the task input: <QUERY>

Do not ask follow-up questions. If the text is incomplete, make reasonable assumptions from the title and query, choose a practical target count, and produce a runnable Search setup / Search criteria plan with a Run search plan button.
```

5. Verify right-side tables.
   - Count visible `table`, `[role="table"]`, `.ant-table`, `.ag-root`, `.rdg`, `.ReactVirtualized__Table`, `.table-container`, or `.grid` elements.
   - Record row-like elements from `tr`, `[role="row"]`, `.ant-table-row`, `.ag-row`, or `.rdg-row`.
   - Compare two samples 30-60 seconds apart to detect live updates through row count or table text changes.
   - Distinguish table frame only from populated table. Header-only tables still count as "right table seen" but not "populated results".

6. Report.
   - Keep the run tabs open as `handoff` unless the user asks to close them.
   - Summarize counts: submitted, search plan seen, continued, right table seen, populated table seen, dynamic updates observed, running, blocked, errors.
   - Include per-case session id and status.
   - Call out cases that are still running or stuck without table.

## Evidence Fields

Record at least:

- `case_index`
- `scenario_id`
- `ID`
- `query_preview`
- `tab_id`
- `session_id`
- `session_url`
- `submitted_at`
- `search_plan_seen`
- `continued_after_plan`
- `continued_at`
- `second_round_sent`
- `right_table_seen`
- `populated_table_seen`
- `row_count_or_rowish`
- `table_changed`
- `working`
- `final_status`
- `error_text`
- `notes`

Use statuses such as `success`, `running`, `blocked_needs_info`, `timeout_no_table`, `error`, and `partial_table_only`.

## Practical Guardrails

- Use explicit timeouts and short polling. If a browser-control call times out, reset/reconnect and reclaim the run tabs by session URL.
- Keep a case map from session id to case metadata so recovery is cheap.
- Do not inspect cookies, local storage, passwords, or Chrome profile files.
- Do not read or expose secrets.
- Do not close user tabs from earlier runs unless explicitly asked.
- Prefer concise progress updates every 30 seconds during long browser runs.

## Script

Use:

```bash
python3 /Users/cdd/.codex/skills/lev8-multi-case-pressure-test/scripts/extract_cases.py \
  /path/to/cases.csv --limit 10
```

The script outputs JSON with logical CSV record count, selected query column, and selected cases.
