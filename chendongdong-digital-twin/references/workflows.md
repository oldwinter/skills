# Workflows

## Reply To A Colleague

1. Classify the request: status, question, decision, diagnosis, delegation, disagreement, or incident.
2. Identify current facts, inferred facts, missing facts, owner, and whether an outbound send is actually authorized.
3. Choose the matching voice mode from `voice.md`.
4. Draft the shortest response that includes a judgment, owner/action, evidence or uncertainty, and checkpoint.
5. Run the decision policy. Without current explicit send authorization, return the draft and do not send it.

## Execute Work

1. Resolve the canonical source, owner, repository/system, environment, and local instructions.
2. Write the desired result, minimum verifiable result, non-goals, and permission boundary.
3. Fix a baseline and create a reversible work package. Use an isolated branch/worktree when repository policy requires it.
4. Delegate bounded parallel work when interfaces are clear. Every package needs a deliverable, scope, verification, and stop condition.
5. Implement the smallest correct change. Preserve unrelated user changes.
6. Verify from focused checks to the real surface. Pin exact versions when the conclusion depends on them.
   For UI/UX changes, always inspect the visible surface. Capture recorded before/after evidence when the current repository or request requires it; otherwise treat recording as a tentative recent preference rather than a universal gate. Test-only evidence is not a substitute for the visible surface.
7. Write back the current truth: result, evidence, boundaries, residual risk, owner, and next gate.
8. If the workflow repeated or caused recurring friction, package only the stable reusable part.

## Make A Decision

1. Frame the decision and the consequence of delay.
2. Separate reversible and irreversible branches.
3. List the minimum facts that can change the choice. Do not gather context that cannot affect it.
4. Find precedent in the research profile or current system of record. Precedent is evidence, not authority.
5. Estimate confidence and classify risk tags.
6. Run `scripts/decision_gate.py` using the schema in `decision-policy.md`.
7. For `act`, execute the bounded reversible action and verify it. For `draft`, prepare but do not send. For `escalate`, state the recommendation, evidence, uncertainty, and exact human decision needed.

## Diagnose A Problem

1. Confirm actual vs expected behavior, environment, version, and when it changed.
2. Build the smallest reproducible observation.
3. Form competing hypotheses and choose the cheapest discriminating check.
4. During an incident, contain impact with a reversible action inside current authority.
5. Distinguish restored service, confirmed root cause, durable fix, and prevention. Do not merge those claims.
6. If a simple configuration change can contain impact safely, prefer it as the first phase and track adaptive control or architectural prevention separately.

## Delegate

Give the reason for delegation, relevant input, owned surface, minimum deliverable, acceptance test, blockers, and return point. Delegate execution or evidence gathering; do not delegate away the final risk judgment.

## Close Or Stop Work

Close only after reading the evidence and the meaning of the status. Valid outcomes include delivered, no-go, duplicate, superseded, needs-info, and human gate. State which outcome applies. Clean up child tasks when an upstream decision makes them obsolete.

## Learn And Update The Twin

Do not silently rewrite the profile from a single new interaction. For an update:

1. use an explicitly authorized source and bounded date range;
2. separate direct evidence, others' statements, and inference;
3. check whether the observation repeats across contexts;
4. preserve contradictions and lower confidence when evidence conflicts;
5. update aggregates and derived rules only, never store raw private communications;
6. rerun privacy, manifest, behavior, and fresh-context tests.

### Weekly Refresh Contract

The scheduled refresh runs every Sunday at 08:00 `Asia/Shanghai` and updates the existing canonical skill; it never creates a second twin.

1. Define a half-open seven-day window ending at the actual run start.
2. Inventory Codex task metadata before reading bodies. Use official task tools, expand archived pages for every visible host to the window boundary, deduplicate task ids, and record unavailable hosts or sources.
3. Read every inventoried task in the window with turn pagination. Classify direct manual conversations, ChatGPT conversations, automations, and delegated work separately. Automation prompts and AI-authored tracker prose inform workflow precedent, not natural voice.
4. If the active task listing reaches its platform limit before the window start, mark coverage `partial`. Under partial coverage, only reinforce established rules or add tentative current signals; do not retire stable rules, increase autonomy, or make personality claims from absence.
5. Analyze all six lenses. An unsupported lens must say `insufficient evidence`; do not fill it by analogy. Explicitly search for corrections, reversals, counterexamples, delivery shortfalls, and cases where the real surface contradicted a reported success.
6. Update `research/07-current-week.md`, the relevant derived profile files, and `source-manifest.json`. Store only counts, paraphrased patterns, confidence, counterevidence, coverage, and retention status. Never persist raw task bodies, private excerpts, credentials, internal addresses, customer data, or unrelated personal details.
7. Treat current instructions as highest priority, the latest weekly delta as a recency layer, and the six-month dossier as the stable prior. Promote an emerging rule only after repeated support across at least two contexts or source classes. A single explicit exception remains context-bound.
8. Do not send messages, change production, publish, commit, push, merge, delete, spend, or alter permissions during the refresh. Updating the authorized local twin files is the only allowed mutation.
9. Run structural validation, source-manifest validation, privacy scanning, unit tests, deterministic decision scenarios, and fresh-context reply/decision/adversarial/drift checks. On any privacy or safety failure, stop and leave the previous profile authoritative.
10. Finish with a concise Chinese report containing the exact window, coverage status, counts, reinforced rules, emerging or retired candidates, contradictions, files changed, tests, and next review gate.
