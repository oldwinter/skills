# Source Summary (Refound/Lenny → Skill Pack)

## Source
- Refound/Lenny skill: `sources/refound/raw/managing-tech-debt/SKILL.md`
- Category/persona inferred: **Engineering**

## What the source emphasized (preserved as rules/checks)
1) **Migrations are usually underestimated** and teams must support the old system while building the new one.  
→ Converted into: required migration phases, dual-run cost callout, and decommission/rollback checks (see [CHECKLISTS.md](CHECKLISTS.md)).

2) **Technical debt is often visible to users** as fragmented interfaces and weak integration.  
→ Converted into: “user-visible debt symptoms” step and register fields that capture user impact (see [WORKFLOW.md](WORKFLOW.md), Step 2).

3) Sometimes the current solution lacks required **operational flexibility**, making a rebuild necessary.  
→ Converted into: strategy decision memo criteria that include operational capabilities and constraints (see [TEMPLATES.md](TEMPLATES.md), Strategy memo).

4) Preventing future debt requires thinking **1–2 years ahead** and putting foundations in early.  
→ Converted into: execution-plan guidance to include enablers (observability, interfaces, schemas) and future-proofing checks.

5) Tech debt projects are underfunded because they’re hard to measure; you need **custom metrics** and **small tests**.  
→ Converted into: a metrics plan with baselines/targets, proxy metrics, and small validation tests (see [TEMPLATES.md](TEMPLATES.md), Metrics plan).

## Known limitations
- The provided source file includes a small subset of insights; this pack fills missing “how-to” and “artifact” layers using standard engineering planning practice.

