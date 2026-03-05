# Source summary (Refound/Lenny)

Source: `sources/refound/raw/ai-product-strategy/SKILL.md`

The source skill is insight-heavy and framed as tactical AI product strategy advice from many product leaders. The provided excerpt includes 5 representative guest insights (the original references more).

## Preserved insights → execution rules

### 1) AI shifts user roles toward higher-level thinking (Inbal S)
- **Rule:** Always include a “workflow + role shift” section: what the user does today vs what changes with AI.
- **Check:** You can name the workflow step(s) the AI changes and the new user responsibilities (review, approval, escalation).
- **Artifact:** Workflow/role-shift notes in the Strategy Thesis ([TEMPLATES.md](TEMPLATES.md)).

### 2) AI products are empirical; you must watch real usage (Nick Turley)
- **Rule:** Strategy must include an empirical learning plan: experiments + instrumentation + iteration cadence.
- **Check:** Every key assumption has a test, metric, owner, and timebox.
- **Artifact:** Empirical Learning Plan template ([TEMPLATES.md](TEMPLATES.md)) + quality gate ([CHECKLISTS.md](CHECKLISTS.md)).

### 3) Agents introduce security risks; treat “agentic security” as first-class (Sander Schulhoff)
- **Rule:** If the product can take actions, you must define a permissions model, prompt-injection/tool-misuse mitigations, audit logs, and rollback.
- **Check:** Every action capability has explicit approvals, least-privilege permissions, and an abuse case.
- **Artifact:** Autonomy Policy table + risk checklist ([TEMPLATES.md](TEMPLATES.md), [CHECKLISTS.md](CHECKLISTS.md)).

### 4) Non-determinism and agency-control trade-offs are core product decisions (Aishwarya N. Reganti + Kiriti Badam)
- **Rule:** Explicitly choose the minimum autonomy needed (assistant → copilot → agent) and design human control points.
- **Check:** The pack distinguishes “suggest” vs “act,” and includes eval/monitoring for non-deterministic behavior.
- **Artifact:** Autonomy Policy + Eval Plan sections ([TEMPLATES.md](TEMPLATES.md)).

### 5) AI strategy must account for the trio: data, models, and compute (Fei-Fei Li)
- **Rule:** Include a data plan, an eval plan, and explicit cost/latency budgets; avoid “infinite capability” assumptions.
- **Check:** The System Plan names data sources, governance constraints, and budgets that make the strategy economically viable.
- **Artifact:** System Plan template ([TEMPLATES.md](TEMPLATES.md)) + rubric items ([RUBRIC.md](RUBRIC.md)).

