# Rubric (score 1–5 per category)

Suggested bar for “demo-ready”: average ≥ 4.0 and no category below 3.

## 1) Demo clarity and scope control
1 = No demo promise; scope is “everything”  
3 = Demo promise exists; some non-goals; partial fake-vs-real decisions  
5 = Crisp demo promise; strong non-goals; explicit fake-vs-real; timebox is realistic

## 2) Prototype contract quality (spec + acceptance)
1 = Vague requirements; no acceptance criteria  
3 = Basic flow and acceptance criteria; missing edge cases  
5 = Clear flow, components, data shape, and observable acceptance criteria

## 3) Vibe coding execution loop quality
1 = Random prompting; no checkpoints; large diffs  
3 = Some structure; occasional validation; incomplete logging  
5 = Tight loop: plan→small diff→run/verify→log; failures become tasks; progress is predictable

## 4) Safety and robustness
1 = Secrets or risky operations; no rollback  
3 = Some guardrails; partial rollback/runbook  
5 = Least privilege; no secrets; confirmation gates for risky actions; rollback and runbook are clear

## 5) Demo readiness and handoff
1 = Only works on the creator’s machine; no demo narrative  
3 = Runs with help; basic demo script  
5 = Runs from clean start; demo script is clear; backup plan exists; next steps are prioritized

