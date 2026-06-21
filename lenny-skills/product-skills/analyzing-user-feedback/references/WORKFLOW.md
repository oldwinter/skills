# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with additional guidance and heuristics.

## Step 1 — Intake + decision framing
Anchor on a decision, not curiosity.

Output a **Context snapshot**:
- Product + area/workflow
- Decision to support + deadline
- Time window and expected volume
- Segments that matter
- Constraints (PII, internal-only, tools)
- Confidence target (quick directional vs high-confidence)

Heuristic: if you can’t name the decision, you’ll produce a “theme list” that doesn’t change anything.

## Step 2 — Source inventory + sampling plan
Inventory sources and define what is **in** and **out**.

Common sources:
- Support tickets/chats (Intercom, Zendesk)
- Sales/CS notes (Gong, Salesforce notes)
- Research notes (interviews, usability tests)
- Surveys (open-ends, NPS/CSAT)
- Reviews (G2, App Store, Reddit/community)
- Product usage signals (funnels, activation drop-offs)
- Logs/traces (especially for AI products)

Sampling strategies:
- **Stratified sampling** by segment (plan tier, persona) and lifecycle stage
- **Event-based sampling** around launches/incidents
- **Top-volume buckets** first (highest ticket categories)

Avoid: only sampling “loud” users without acknowledging bias.

## Step 3 — First-pass read-through (open coding)
Before building a taxonomy, read and annotate.

Goal: surface “what’s wrong” in the customer’s words:
- Confusion and misunderstanding
- Trust/safety concerns
- Setup/integration failures
- Performance/latency
- Missing capabilities (true gaps vs expectation mismatch)

Principle: optimize for finding **reasons users won’t use the product**, not reasons they will.

## Step 4 — Taxonomy + codebook
Create a tagging system that supports the decision.

Recommended dimensions:
- **Theme/topic** (primary + secondary)
- **Lifecycle stage** (onboarding, activation, daily use, renewal)
- **Severity/impact** (e.g., 1–4 scale)
- **User segment** (persona, tier, platform)
- **Root cause type** (bug, UX, docs, pricing, expectation, integration, model quality)

Keep the tag list small at first (10–20) and allow “Other/Needs review”.

## Step 5 — Normalize and tag the table
Normalize each item into a row.

Minimum fields:
- Source + date (or date bucket)
- Segment/lifecycle stage (if known)
- Verbatim excerpt (redacted if needed)
- Tags (primary theme + severity + root cause)
- Link/ID (optional)

If you can’t tag everything, prioritize:
- High-severity items
- High-frequency buckets
- Key segments

## Step 6 — Theme synthesis + quantification
Synthesis should answer:
- What are the top themes?
- Who is impacted (segments)?
- How bad is it (severity/impact)?
- Why is it happening (root causes)?
- What evidence supports this (quotes/examples)?

Quantify carefully:
- Use counts as directional unless sampling is representative.
- Separate “volume” (how often) from “impact” (how bad).

## Step 7 — Recommendations + learning plan
Translate into actions with time horizons:
- **Now:** bug fixes, docs, UX tweaks, support macros
- **Next:** feature improvements, workflow redesigns, messaging/positioning adjustments
- **Later:** bigger bets validated by follow-up research

Also produce open questions + the fastest way to answer them (targeted interviews, usability test, data instrumentation).

## Step 8 — Share-out + feedback loop + storage
Ensure insights persist and don’t get lost.

Feedback loop should define:
- Cadence (weekly/monthly)
- Owners (PM/ProdOps/Support/Eng)
- Engineering participation (e.g., rotate an engineer into support triage)
- Where insights live (docs/wiki/research repository) and how to query them later
- Update triggers (launches, incident spikes, churn upticks)

Before finalizing:
- Run [CHECKLISTS.md](CHECKLISTS.md)
- Score with [RUBRIC.md](RUBRIC.md)
- Add **Risks / Open questions / Next steps**

