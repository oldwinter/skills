# Workflow Notes (Managing Timelines)

Use this as expanded guidance for the workflow in `skills/managing-timelines/SKILL.md`.

## Core concepts

### 1) Deadline taxonomy (what kind of “date” is this?)

- **Fixed external deadline:** tied to an external event/contract/regulatory requirement. Date is effectively immovable; scope/resources are the levers.
- **Fixed internal deadline:** leadership commitment; may still be movable, but requires explicit re-decision.
- **Target date:** directional date to guide prioritization; can move as uncertainty resolves.
- **Window:** a range (“late March”) that can tighten over time; useful when uncertainty is high.

Rule of thumb: if missing details, treat it as a **target/window**, and explicitly say what would be required to turn it into a commitment.

### 2) Commitment ladder (use precise language)

Use three date types to avoid “date soup”:

- **Commitment:** “We will deliver X by D” (only for scoped work within control)
- **Forecast:** “Based on what we know, we expect D” (subject to change as risks resolve)
- **Target:** “We want D” (directional; used for prioritization)

Always attach: confidence + top risks + next decision point.

### 3) Phase-based planning (commit only within control)

Recommended lifecycle:

1) **Discovery** (reduce problem uncertainty)
   - Outputs: problem framing, user value, success metrics/guardrails, top risks, initial approach options
2) **Solutioning** (reduce solution uncertainty)
   - Outputs: chosen approach, UX/tech outline, dependency plan, estimate range, rollout approach
3) **Build** (execution)
   - Outputs: working increment(s), QA plan, release readiness checks
4) **Launch** (safe release)
   - Outputs: rollout/rollback plan, comms, monitoring, post-launch checks

Commitment pattern: commit to **Discovery/Solutioning end dates** first; commit to Build/Launch only after solutioning and estimation.

### 4) RAG (red/amber/green) is only useful with action

Define RAG so it triggers decisions:

- **Green:** on track; no decisions needed
- **Yellow:** risk emerging; needs a decision/assist within 1 week
- **Red:** cannot meet committed date without a change (scope/date/resources/quality); needs immediate decision

RAG should come with:
- “What changed since last update”
- “Decision needed” + deadline
- “Proposed trade-off” (cut/add/shift)

### 5) Protecting a real deadline (treat it like P0)

When a deadline is real:
- Reduce distractions: cancel/defer nonessential work and meetings
- Reduce WIP: prioritize throughput; avoid parallel half-finished work
- Enforce change control: **trade, don’t add**
- Make “cut candidates” explicit early, so you’re not forced into bad last-minute cuts

## AI/ML uneven cadence (demo vs production)

If AI/ML is involved, separate:
- **Time to first demo** (often short): prototype to validate direction
- **Time to production** (often longer): evaluation, safety, reliability, cost/latency, monitoring, fallback behavior, edge cases, compliance

Add explicit outer-loop milestones:
- Evaluation harness + acceptance metrics
- Data readiness + privacy review
- Guardrails + fallback plan
- Monitoring + incident response/runbook
- Gradual rollout + post-launch calibration

## Step-by-step guidance (matches SKILL workflow)

### Step 1) Intake + deadline classification
- Confirm “why now”, what is fixed, and who can change the date or scope.
- If the user says “hard deadline” but can’t name the external constraint, treat it as a target until confirmed.

### Step 2) Commitment model
- Convert any ambiguous “ship date” language into commit/forecast/target.
- Add a rule: **never present a forecast as a commitment**.

### Step 3) Phase plan + decision gates
- Define phase outputs as artifacts a stakeholder can review async.
- Set a “next commitment date” (e.g., “We will re-forecast on <date> after solutioning”).

### Step 4) Milestones + tracker
- Milestones should be deliverables (demo, spec sign-off, dependency secured, code complete, beta shipped).
- Add confidence (H/M/L) and dependency owners.

### Step 5) Governance + escalation
- Default cadence: weekly review with a short agenda:
  1) RAG review (what’s yellow/red)
  2) Decisions/asks
  3) Scope changes
  4) Next week plan
- Ensure “red” has a single escalation path and decision owner.

### Step 6) Scope + change control
- Define freeze points: scope freeze, code freeze, QA freeze (as appropriate).
- Pre-create a cut list so you can trade scope quickly without re-litigating.

### Step 7) Stakeholder comms
- Communicate in the commitment ladder language.
- Include explicit asks and deadlines for decisions (don’t bury them).

### Step 8) Quality gate
- Ensure the final pack answers: “What are we committing to, and what must happen next to keep the date true?”

