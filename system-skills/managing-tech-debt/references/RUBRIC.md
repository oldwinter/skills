# Rubric (Score 1–4 per dimension)

Use this rubric to score the Tech Debt Management Pack. Target: **≥ 20/28** with no 1s in “Safety & feasibility”.

## 1) Decision clarity (1–4)
1 = Unclear what decision/action changes.  
2 = Some decisions implied but not explicit.  
3 = Decisions explicit; outputs aligned.  
4 = Decisions explicit; trade-offs and stakeholders are aligned on next actions.

## 2) Evidence & signals (1–4)
1 = Pure opinion; no signals.  
2 = Some anecdotes; weak linkage to symptoms.  
3 = Symptoms and at least some measurable signals (or clear instrumentation plan).  
4 = Clear baselines, confidence levels, and measurement plan for impact.

## 3) Register completeness (1–4)
1 = List of items with missing owners/impact/effort.  
2 = Register exists but inconsistent schema.  
3 = Consistent schema; owners, impact, effort ranges, dependencies captured.  
4 = Register enables immediate planning and can be maintained as an operating artifact.

## 4) Prioritization quality (1–4)
1 = Ranked list with no rationale.  
2 = Rationale exists but inconsistent or subjective.  
3 = Transparent scoring and defensible top priorities.  
4 = Prioritization accounts for sequencing and includes “enabler” work and stop conditions.

## 5) Strategy correctness (refactor vs rebuild) (1–4)
1 = Rebuild/refactor recommended without criteria.  
2 = Options listed but incomplete criteria.  
3 = Options + criteria + recommendation; acknowledges uncertainty.  
4 = Includes migration phases, dual-run costs, cutover/decommission, rollback, and clear success metrics.

## 6) Execution feasibility (1–4)
1 = Plan is vague or unrealistic.  
2 = Milestones exist but weak acceptance criteria.  
3 = Incremental milestones with owners, acceptance criteria, capacity assumptions.  
4 = Sequenced plan with measurable milestones, risks mitigations, and immediate next step.

## 7) Safety & robustness (1–4)
1 = Encourages risky/irreversible actions without safeguards.  
2 = Some safeguards but missing rollback/confirmation gates.  
3 = Explicit safety gates; no secrets; rollback guidance included where relevant.  
4 = Strong least-privilege posture, explicit human checkpoints for one-way-door actions, and clear rollback triggers.

