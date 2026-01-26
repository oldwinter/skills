# Templates (Copy/Paste)

Use these templates to produce a **PRD Pack**.

## 0) Context snapshot (bullets)
- Product:
- Target user/customer segment:
- Problem statement:
- Why now:
- Decision to make (and by when):
- DRI / approver:
- Constraints (timeline, platform, policy/legal, dependencies):
- Success metrics (1–3):
- Guardrails (2–5):
- Stakeholders/reviewers:

## 1) Artifact selection (choose the lightest set)
Fill this table:

| Artifact | Include? (Y/N) | Why | Audience | Owner | Due date |
|---|---:|---|---|---|---|
| PR/FAQ |  |  |  |  |  |
| PRD |  |  |  |  |  |
| Prompt Set (AI) |  |  |  |  |  |
| Eval Spec (AI) |  |  |  |  |  |

## 2) PR/FAQ template (optional)

### Press release
- **Release date:** <hypothetical date>
- **Headline:** <short, customer-readable>
- **Summary (2–3 sentences):** <what changed + who benefits>
- **Problem today:** <pain + evidence>
- **Solution:** <what the product does>
- **Customer quote:** “...”
- **Company/PM quote:** “...”
- **How it works (high level):** <3–6 bullets>
- **Who it’s for / who it’s not for:** <boundaries>
- **Pricing/packaging (if relevant):** <assumptions>

### FAQ (start with these)
1) Who is the target customer/user?
2) What’s the core user journey?
3) Why should we build this now?
4) What are the top alternatives/workarounds today?
5) What’s out of scope for v1?
6) What could go wrong (trust, safety, privacy, reliability)?
7) How will we measure success and adoption?
8) What are the major dependencies and risks?

## 3) PRD template

### 3.1 Overview
- **Title:**
- **Author:**
- **Last updated:**
- **Status:** Draft / Review / Approved
- **Links:** PR/FAQ, designs, prototype, research, analytics, tickets

### 3.2 Problem + why now
- **Problem statement:**
- **User pain evidence:** (data, anecdotes, tickets)
- **Why now:** (trigger/event; opportunity cost)

### 3.3 Goals, non-goals, out of scope
**Goals (measurable)**
- G1:
- G2:

**Non-goals (important, but not for this effort)**
- NG1:

**Out of scope (explicit exclusions)**
- OOS1:

### 3.4 Users + use cases
- Primary personas:
- Primary use case (happy path):
- Top edge cases:
- Permissions/roles assumptions:

### 3.5 Proposed solution (high level)
- Summary:
- Key product decisions:
  - Decision 1:
  - Decision 2:

### 3.6 Requirements (R1…Rn)
Write requirements so they are testable.

| ID | Requirement (must/should/could) | Acceptance criteria (what must be true) | Edge cases / notes |
|---|---|---|---|
| R1 |  |  |  |
| R2 |  |  |  |

### 3.7 UX flows / states
Describe the key flows and states (or link to diagrams):
- Entry points:
- Happy path:
- Error/empty states:
- Loading/performance expectations:
- Accessibility considerations:

### 3.8 Metrics + instrumentation
**Success metrics**
- M1:
- M2:

**Guardrails**
- Gd1:
- Gd2:

**Instrumentation plan**
| Metric | Definition | Data source | Event/table needed | Owner | Cadence |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### 3.9 Rollout + launch plan
- Launch tiers (internal/beta/GA):
- Target dates:
- Eligibility (who gets it):
- Comms (support/docs/marketing):
- Rollback plan:

### 3.10 Risks / open questions / next steps (required)
**Risks**
- …

**Open questions**
- …

**Next steps**
1) …

## 4) Prompt Set template (AI features)

### 4.1 Prompt inventory
Keep prompts versioned and named:

| Prompt name | Version | Purpose | Inputs | Output contract | Where used |
|---|---:|---|---|---|---|
|  |  |  |  |  |  |

### 4.2 Prompt spec (copy per prompt)
- **Prompt name:**
- **Version:**
- **Purpose:**
- **Inputs:** (what fields are required)
- **Output format:** (JSON schema or bullet structure)
- **Constraints/guardrails:** (tone, policy, privacy)
- **Tools/retrieval:** (high level)
- **Examples:** (2 good + 1 bad)

### 4.3 Versioning rules
- Any change to output format or guardrails increments version.
- Prompts must be linked to eval coverage (which tests validate them).

## 5) Eval Spec template (AI features)

### 5.1 What “correct” means
- Must-do behaviors:
- Must-not-do behaviors:
- Policy/privacy constraints:

### 5.2 Test set
Define a small-but-representative test set:
- Input cases (10–100, depending on maturity)
- Expected properties (not always a single “right answer”)
- Labels/tags (tone, safety, refusal, factuality, tool use)

### 5.3 Judge prompt (LLM-as-a-judge)
Define an evaluation prompt that returns a structured verdict:
- Output fields: pass/fail, score (1–5), rationale, violated rule IDs
- Include rubrics and failure mode definitions

### 5.4 Scoring + thresholds
- Primary score:
- Pass threshold:
- Critical failures (auto-fail):
- Regression policy (what blocks launch):

### 5.5 Operations
- Where eval runs (CI, scheduled, manual):
- Owner:
- Reporting dashboard/format:
- Red-team plan (top failure modes to test):

## 6) Circulation note (artifact quality)
Before you send the pack to stakeholders:
- Run [CHECKLISTS.md](CHECKLISTS.md)
- Ensure definitions are unambiguous (terms, metrics, R1…Rn)
- Ensure the doc stands alone (no meeting required to understand)

