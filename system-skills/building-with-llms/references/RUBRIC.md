# Rubric (score 1–5 per category)

Suggested bar for “ship-ready”: average ≥ 4.0 and no category below 3.

## 1) Problem framing and boundaries
1 = Vague goal; no non-goals; no success definition  
3 = Clear job statement; some constraints; partial success/guardrails  
5 = Crisp job + non-goals; measurable success + guardrails; top failure modes named

## 2) Prompt + tool contract quality
1 = Prompt is generic; tools undefined; output format unclear  
3 = Prompt has rules; tools described; some examples  
5 = Contract is testable: DO/DO NOT rules, uncertainty behavior, schema, examples, and safety constraints for each tool

## 3) Context strategy correctness
1 = “Just stuff context”; no source-of-truth concept  
3 = Some retrieval/tool plan; partial conflict handling  
5 = Clear context pipeline with authority, freshness, conflict handling, and grounding expectations

## 4) Evaluation rigor (offline)
1 = No evals; only ad hoc manual testing  
3 = Basic test set and rubric; thresholds unclear  
5 = Test set covers failure modes + red team; rubric + thresholds + automated checks; bugs become tests

## 5) Production readiness
1 = No budgets/monitoring; no fallback  
3 = Some monitoring; partial budgets; basic rollback  
5 = Budgets + monitoring + fallbacks + logging are complete; prompt versioning and incident hooks exist

## 6) Iteration loop and engineering plan
1 = “We’ll iterate” without a loop  
3 = Basic prototype and feedback plan  
5 = Tight loop: reproduce→label→test→fix→measure; safe use of coding agents with review gates and rollback

