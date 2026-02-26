# Intake (Planning Under Uncertainty)

Ask **up to 5 questions at a time**. Prefer questions that change the decision, the experiments, or the trigger thresholds.

## Quick-start (pick the most important 5)

1) **What decision are we trying to make — and by when?**
   - Stop / pivot / scale / commit to build / rollback?
   - What happens if we wait?

2) **What does success look like (and what must not get worse)?**
   - Success metric(s):
   - Guardrails (“must not worsen”):
   - Minimum acceptable outcome:

3) **What’s fixed vs flexible?**
   - Non-negotiable constraints (compliance, brand, quality, budget):
   - What can move (scope, time, resources, quality, market segment)?

4) **What are the top unknowns/assumptions?**
   - List the top 3–5 “things that would change the plan”.
   - What signals/data do we already have?

5) **Who are the stakeholders and decision owners?**
   - Who decides stop/pivot/scale?
   - Who needs to be informed weekly vs escalated immediately?

## Deeper clarifiers (ask only if needed)

### Wartime vs peacetime
- Are we stabilizing an incident / preventing further damage, or exploring for growth?
- What’s the rollback capability and tolerance for customer impact?

### Feasible experiments
- What experiments are possible (customer calls, prototypes, A/B tests, ops drills)?
- What is the fastest test we can run within 48 hours / 1 week / 2 weeks?
- What data instrumentation exists (and what’s missing)?

### Baseline + segmentation
- What’s the baseline (last good week/month)? Any seasonality?
- Which segment is impacted most? Any known confounders?

### Capacity + dependencies
- Who is available to run tests and analyze results?
- Any dependencies on other teams/vendors/reviews?

## Default assumptions (if the user can’t answer)
- Optimize for **learning first**: commit to the next learning milestone, not a final delivery date.
- Prefer **reversible decisions** and small bets where possible.
- Use a weekly learning/decision cadence with a written decision log.
- Add explicit buffers (time/capacity) proportional to uncertainty (higher uncertainty → larger buffer).

