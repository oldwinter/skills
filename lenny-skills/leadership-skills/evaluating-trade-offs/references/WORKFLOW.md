# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with additional heuristics and decision-quality defaults.

## Rigor dial (choose the minimum process that matches stakes)

- **Quick (30–60 min):** reversible decisions, small stakes. Focus on criteria, order-of-magnitude impact, and a review date.
- **Standard (2–4 hours):** meaningful resource allocation or customer impact. Add all-in cost/opportunity cost and a minimal validation plan.
- **Deep (multi-day):** one-way-door decisions with high stakes. Consider using `running-decision-processes` for decision rights, stakeholder alignment, and a full decision log.

## Preserved insights (converted into rules)

### 1) All-in cost + opportunity cost (avoid narrow ROI thinking)
Rule:
- Evaluate each option using **all-in cost** (cash + people time + engineering + maintenance + coordination), not just the obvious line item.
- Compare against the *next-best* use of the same resources (opportunity cost).

Practical moves:
- If an option needs engineering, include: integration, migrations, QA, on-call, and long-term maintenance.
- If an option needs headcount, include: recruiting time, ramp, management overhead, and coordination.

### 2) Order-of-magnitude over false precision
Rule:
- Use ranges and confidence. Prefer 10× comparisons over 1–2% “differences” when uncertainty is high.

Practical moves:
- Use **best / expected / worst** (or min/likely/max) ranges.
- Record the top 2–3 assumptions that drive the decision; don’t spread effort evenly across minor details.

### 3) Thought experiments first (think more, build less)
Rule:
- Most “experiments” should start as thought experiments. Only build when the result could change the decision.

Practical moves:
- Run a pre-mortem: “This failed—what happened?”
- Design the cheapest test that could falsify your biggest assumption (data pull, 5 customer calls, timeboxed spike).

### 4) “Worse first” is normal—plan the dip
Rule:
- Many good decisions have a short-term downside before long-term upside. If you choose a “worse first” path, plan the dip explicitly.

Practical moves:
- Identify the likely short-term degradation (e.g., support load, velocity slowdown, revenue dip).
- Define leading indicators and mitigations so the team doesn’t panic and reverse prematurely.

### 5) Sunk costs don’t justify future spend
Rule:
- For continuation decisions: ignore sunk costs and ask, “Would we start this today with what we know now?”

Practical moves:
- Define stop/continue triggers and a review date.
- If stopping, decide what to salvage (code reuse, learnings, comms) and how to prevent repeat failure modes.

## Communication heuristic (trade-offs don’t land without narrative)

Include a short “trade-off narrative” in the pack:
- What we’re optimizing for and why.
- What we are *not* optimizing for (and the cost of that choice).
- What changes tomorrow (who does what, what stops, what starts).
- When we’ll review and what would cause a change of course.

