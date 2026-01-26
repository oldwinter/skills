# Workflow Notes (Planning Under Uncertainty)

Use this as expanded guidance for the workflow in `skills/planning-under-uncertainty/SKILL.md`.

## Core concepts

### 1) Wartime humility: diagnose before acting
When the system is behaving unexpectedly (growth collapse, retention drop, reliability incident), prioritize **diagnosis**:
- Separate **symptoms** (“metric dropped”) from **causes** (why it dropped).
- Generate multiple plausible hypotheses (including uncomfortable ones).
- Define what evidence would falsify each hypothesis.

Bias toward reversible actions until uncertainty is reduced.

### 2) Experiments are about learning, not “wins”
A healthy experimentation culture:
- Defines a **hypothesis** up front.
- Treats a “failed” result as valuable if it changes a decision.
- Avoids measuring individuals by “win rate” (creates risk aversion).

Practical rule: every experiment must answer, “What will we do differently depending on the result?”

### 3) Build a reproducible testing process (“many shots at bat”)
Create a system that makes testing repeatable:
- A single place to store hypotheses and experiments (a portfolio table).
- A consistent review cadence (weekly by default; daily in crisis).
- Clear roles: who designs, runs, analyzes, decides.

Speed matters because uncertainty is unpredictable; process quality often dominates idea quality.

### 4) Data is a compass, not a GPS
Use data to check direction and falsify bad assumptions:
- Prefer **directional** decisions over false precision.
- Define “ridiculousness tests”: signals that tell you you’re wrong quickly.
- Pair metrics with **guardrails** so you don’t optimize the wrong thing.

### 5) Buffers + contingencies keep plans alive
Uncertainty demands:
- Time/capacity buffers (explicitly allocated).
- Contingency paths (Plan A/B/C) that can be activated quickly.
- Trigger thresholds that define when to pivot/rollback/escalate.

Good plans do not claim certainty; they state what you’ll do when uncertainty resolves in each direction.

## Step-by-step guidance (matches SKILL workflow)

### Step 1) Intake + mode setting
- Confirm the decision needed, the time horizon, and the “why now”.
- Decide the operating mode:
  - **Wartime:** stabilize and stop the bleeding; restrict changes; fast diagnosis and rollback/patch rules.
  - **Peacetime:** explore and learn; tolerate slower, higher-quality evidence building.

### Step 2) Diagnose reality
- Produce a short “situation report”:
  - What changed (release, traffic source, pricing, infra)?
  - What does the data show (trend, magnitude, segment)?
  - What do we *not* know yet?
- Generate hypotheses across categories: product, marketing, pricing, reliability, ops, external factors.

### Step 3) Uncertainty map
- Convert hypotheses into an uncertainty map:
  - Mark confidence (H/M/L) and impact.
  - Prioritize “high impact, low confidence” items.
- Add a validation method per item:
  - Customer calls, log analysis, A/B tests, usability tests, forced-choice surveys, market scans, etc.

### Step 4) Hypotheses + decision rules
- Write hypotheses in falsifiable form:
  - “If <condition>, then <measurable change> because <mechanism>.”
- For each hypothesis, define:
  - Primary signal (compass metric)
  - Guardrails
  - Decision rule (“If we see X by Y date, we will do Z”)

### Step 5) Reproducible testing process
- Build an experiment portfolio:
  - Mix fast/cheap tests and slower/high-confidence tests.
  - Ensure each test has an owner and a review date.
- Pick a cadence:
  - Wartime: daily or every 48 hours for top hypotheses.
  - Peacetime: weekly learning review, biweekly decision checkpoint.

### Step 6) Plan v0 with buffers + contingencies
- Plan v0 should commit to learning gates:
  - Phase 1: validate top unknowns
  - Phase 2: commit to a direction
  - Phase 3: build + rollout
- Add buffers:
  - Explicit time/capacity set aside for “unknown unknowns”
- Add contingencies:
  - Pre-decide what gets cut or changed if signals go bad.

### Step 7) Quality gate
- Ensure the pack can be executed without additional “interpretation meetings”.
- The final output should be readable by a stakeholder and runnable by the team.
