# Source summary (Refound/Lenny)

Source: `sources/refound/raw/building-with-llms/SKILL.md`

The source skill is insight-heavy: tactical advice on building with LLMs from many product leaders. The provided excerpt includes 5 representative insights (the original references more).

## Preserved insights → execution rules

### 1) Prompt engineering remains critical (Sander Schulhoff)
- **Rule:** Always produce a testable **prompt + tool contract** with explicit DO/DO NOT rules, examples, and “how to behave when uncertain.”
- **Check:** A reviewer can predict behavior for representative inputs; the contract is validated via an eval set (not vibes).
- **Artifact:** `references/TEMPLATES.md` (Prompt + tool contract) + checklist items in `references/CHECKLISTS.md`.

### 2) Data quality and debugging mindset matter (Karina Nguyen)
- **Rule:** Treat data and evals as a debugger: label failures, identify conflicting sources, and add tests for each discovered bug.
- **Check:** The evaluation plan covers top failure modes and explicitly handles conflicting/ambiguous data.
- **Artifact:** `references/TEMPLATES.md` (Data + evaluation plan) + rubric criteria in `references/RUBRIC.md`.

### 3) Command-line AI agents are high-leverage, even for non-coders (Dan Shipper)
- **Rule:** Include an explicit plan for safe “agent-assisted execution” (file operations, terminal commands, batch analysis) with approval gates and least privilege.
- **Check:** The build plan constrains agent actions, avoids secrets, and requires review/validation before changes ship.
- **Artifact:** `references/TEMPLATES.md` (Using coding agents safely) + checklist D in `references/CHECKLISTS.md`.

### 4) LLMs deliver high ROI on routine engineering tasks (Logan Kilpatrick)
- **Rule:** Use coding agents for “lower-hanging fruit” tasks, but keep the blast radius small and validated (tests/evals + review).
- **Check:** Agent outputs are verified by automated checks and human review; changes are traceable (prompt/dataset/versioning).
- **Artifact:** Build + iteration plan template + production readiness checklist.

### 5) Building software shifts toward supervising code-generating systems (Bret Taylor)
- **Rule:** Treat the LLM as a code-generating machine that must be operated: constraints, contracts, monitoring, and rollback are first-class.
- **Check:** The pack includes budgets, monitoring, fallback/rollback, and an incident response hook (not just prompts).
- **Artifact:** Launch + monitoring plan template + production readiness checklist and rubric.

