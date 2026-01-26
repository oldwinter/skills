# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with extra guidance and decision heuristics.

## Step 1 — Intake + constraints
Output a **Context snapshot**:
- Product / audience / segment
- Value moment
- Business model + strategic goal
- Time horizon
- What’s measurable today (latency, gaps)
- Stakeholders + decisions the metric should govern

## Step 2 — North Star Narrative (qualitative model first)
Write a short narrative that clarifies:
- What value is delivered (customer POV)
- Who receives it
- What “success” looks like
- What’s **in** and **out** of scope
- How the North Star will be used as a tie-breaker

Rule of thumb: if you can’t explain the value model clearly, the metric will be fragile or gameable.

## Step 3 — Candidate metric generation
Generate 3–5 candidates that measure **delivered value**, not internal activity.

Heuristics to consider (pick what fits):
- **Value delivery count:** “# customers experiencing the value moment”
- **Value delivery frequency:** “value moments per customer per week”
- **Depth/quality-adjusted value:** “successful outcomes that meet a quality bar”
- **Friction reduction:** “% of customers with zero critical failures/support tickets”

Avoid defaulting to lagging outcomes (e.g., retention) as the only operating metric.

## Step 4 — Stress test + choose
Use the checklists/rubric to assess each candidate for:
- **Customer value:** does it represent real value delivered?
- **Controllability:** can teams move it in weeks/quarters?
- **Measurability:** is the definition unambiguous and instrumentable?
- **Gaming risk:** what perverse incentives could it create?
- **Ecosystem impact:** who/what might be harmed?
- **Comms:** will people understand and remember it?

Select one metric (or a primary + explicit guardrails), and document why.

## Step 5 — Metric spec
Write a spec so it can be computed consistently:
- Name and definition
- Formula + time window
- Inclusion/exclusion rules (e.g., what counts as “active”)
- Segmentation slices (e.g., by plan, region, cohort)
- Data source + latency + owner
- Example calculation

## Step 6 — Driver tree (inputs + guardrails)
Create:
- 3–7 **drivers** (first-order components)
- 1–3 **leading input/proxy metrics** per driver
- 1–2 **guardrails** overall (quality, trust, margin, customer harm)

Make sure every input metric has at least one realistic lever to pull (initiative/experiment).

## Step 7 — Validation + rollout
Plan:
- Sanity checks (does the metric move when expected?)
- Correlation/leadingness checks (do inputs predict the outcome?)
- Dashboard + review cadence (weekly metric review; monthly spec review)
- Ownership (who maintains definition, who drives initiatives)
- Decision rules (“when metric X moves, we do Y”)

## Step 8 — Quality gate + finalize
Run [CHECKLISTS.md](CHECKLISTS.md) and [RUBRIC.md](RUBRIC.md), then finalize the North Star Metric Pack with:
- Risks
- Open questions
- Next steps (owners + dates if possible)

