# Workflow (Expanded)

This file expands the steps from `../SKILL.md` with heuristics and common failure modes for teams building with LLMs.

## Step 1 — Frame the job, boundary, and “good”
Heuristics:
- If the request is “add AI,” force a one-sentence job statement and explicit non-goals.
- Define “good” as measurable behavior, not vibes (rubric + acceptance thresholds).

Failure modes:
- Shipping a demo with no success metric or guardrails.
- “Magic assistant” scope creep because non-goals weren’t written down.

## Step 2 — Choose the minimum viable autonomy pattern
Heuristics:
- Start with the minimum autonomy that still delivers value.
- Put humans at the control points where mistakes are expensive or irreversible.

Failure modes:
- Calling something an “agent” without a permissions model or undo.
- Tool use without confirming side effects (e.g., ticket creation, email sending).

## Step 3 — Design context strategy (prompting → RAG → tools)
Heuristics:
- Prefer authoritative sources over “stuffed context.”
- Treat conflicting context as a first-class failure mode; define tie-breakers.

Failure modes:
- RAG that retrieves irrelevant context (no reranking, no grounding checks).
- “Context soup” where the model can’t tell what to trust.

## Step 4 — Draft prompt + tool contract
Heuristics:
- Prompting does not go away: encode DO/DO NOT rules, examples, and “how to behave when uncertain.”
- Make tool contracts explicit: inputs, outputs, constraints, and safe defaults.

Failure modes:
- A prompt that reads like marketing copy instead of operational instructions.
- Tools that allow destructive actions without confirmations or logs.

## Step 5 — Build eval set + rubric (debug like software)
Heuristics:
- Use evals as your debugger: every bug should produce a new test.
- Start with a small, high-signal set (20–50 cases) before scaling.

Failure modes:
- No evals → changes regress silently.
- Only testing happy paths; ignoring adversarial and edge cases.

## Step 6 — Prototype thin slice + safe coding-agent loop
Heuristics:
- Use coding agents for “lower-hanging fruit” tasks, but supervise: small diffs, tests, review.
- Treat the agent like a junior engineer with infinite speed, not infinite correctness.

Failure modes:
- Letting the agent refactor broadly; losing control of blast radius.
- Copying secrets into prompts or logs.

## Step 7 — Production readiness
Heuristics:
- Set budgets first (latency/cost), then design within them.
- Add graceful degradation: fallback prompts/models, cached results, “ask a human.”

Failure modes:
- No cost guardrails → success becomes financially unsustainable.
- No monitoring → you discover failures via angry users.

## Step 8 — Quality gate + finalize
Heuristics:
- Use the checklist and rubric; don’t “feel” done.
- Convert open questions into concrete next experiments.

Failure modes:
- A pack that sounds smart but can’t be executed.
- Risks aren’t owned; next steps aren’t prioritized.

