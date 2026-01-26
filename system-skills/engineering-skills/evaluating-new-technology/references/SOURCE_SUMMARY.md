# Source Summary (what was preserved + how it was transformed)

## Source
- `sources/refound/raw/evaluating-new-technology/SKILL.md`
- Category: **AI & Technology**

Note: The source header references “22 product leaders (27 insights)”, but the local raw file includes 5 guest insights. This pack preserves those and generalizes them into a reusable evaluation workflow.

## Preserved insights → rules, checks, artifacts

### 1) “Tools solve problems, not the other way around.” (Austin Hay)
- **Rule:** Start every evaluation with a tool-agnostic problem statement and explicit non-goals.
- **Check:** You can explain the decision without naming the tool.
- **Artifact:** Evaluation brief (problem, users, non-goals).

### 2) “Build vs buy: mental bandwidth matters.” (Dhanji R. Prasanna)
- **Rule:** Model engineering bandwidth/opportunity cost as a first-class cost in build vs buy.
- **Check:** The analysis names who maintains the system 12 months out (on-call, upgrades).
- **Artifact:** Build vs buy analysis (bandwidth/TCO ledger).

### 3) “Evaluate tools by the workflows and ROI they enable.” (Naomi Ionita)
- **Rule:** Score options on workflow impact and measurable ROI, not feature checklists.
- **Check:** Every criterion is measurable or falsifiable in a pilot.
- **Artifact:** Options & criteria matrix + pilot plan.

### 4) “AI guardrails marketing is often misleading.” (Sander Schulhoff)
- **Rule:** Treat “100% safe / catches everything” claims as hypotheses; assume determined attackers.
- **Check:** Risk review includes defense-in-depth and a plan to test guardrails in a pilot/red-team.
- **Artifact:** Risk & guardrails review + pilot plan evaluation method.

### 5) “Stack thinking: data hub + analytics + lifecycle.” (Hila Qu)
- **Rule:** Evaluate tool fit in the context of your stack layers and integration plan.
- **Check:** Pack includes a documented data/control flow and migration plan.
- **Artifact:** Options matrix integration notes.

## What this pack adds (manufactured layers)
- A concrete **input/output contract** and an 8-step workflow (artifact-driven).
- Templates for each deliverable and quality gates (checklists + rubric).
- Pilot structure with binary exit criteria and rollback/data deletion guidance.

