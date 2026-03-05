# Workflow (Expanded)

This file expands `../SKILL.md` with extra guidance and heuristics.

## Core heuristics (from the source skill)
- **Treat attention as scarce (especially on mobile):** explicitly optimize the critical path (taps to value).
- **The spec output is a diagram:** a low‑fidelity drawing that makes the “moving pieces” and feasibility visible.
- **Prototype to evaluate feel:** static mocks often miss timing, friction, and comprehension.
- **Draw badly on purpose:** rough sketches invite collaboration and faster alignment than polished wireframes.
- **Prefer real software prototypes when needed:** messy throwaway code can be the fastest path to truth.

## Step 1 — Choose artifacts
Rules of thumb:
- If the team is confused about structure or feasibility, prioritize the **low‑fidelity diagram + flows/states**.
- If the decision depends on interaction nuance (“feel”), prioritize the **prototype brief** and timebox it.
- Avoid “doc sprawl”: produce the minimum set that makes the decision and build executable.

## Step 2 — Context snapshot
Capture:
- Problem + why now
- Audience/DRI/approver
- Platforms and constraints
- Success metrics + guardrails
- Dependencies and assumptions

Heuristic: if you can’t state success clearly, design details will churn.

## Step 3 — Scope boundaries (+ tap budget)
Good spec boundaries include:
- Goals and non-goals
- Out of scope (explicit exclusions)
- Assumptions (labeled) and dependencies

Mobile tap budget technique:
- Identify the **first value event**
- Count taps from entry → value
- Set a target and list “tap removals” (combine screens, default choices, progressive disclosure)

## Step 4 — Low‑fidelity diagram (“moving pieces”)
What to include:
- Key screens/states or system components (≤10)
- Data/hand-offs and decision points
- Where UX ambiguity becomes engineering ambiguity

Common failure mode: over-specifying pixel details while under-specifying states and edge cases.

## Step 5 — Flows + states
Minimum set:
- One happy-path flow diagram
- A state table for each critical screen/component (empty/loading/error/success)
- Top edge cases (permissions, interruptions, retries, partial completion)

Heuristic: if you can’t role-play it, it’s not specific enough yet.

## Step 6 — Prototype brief (when “feel” matters)
Prototype types:
- **Lo-fi:** validate structure and comprehension quickly.
- **Hi-fi:** validate microcopy, hierarchy, and basic motion/timing.
- **In-code:** validate performance, interaction nuance, and real-world constraints.

Rules:
- Use realistic data wherever possible; “lorem ipsum” can hide real failure modes.
- Timebox and treat throwaway prototypes as disposable by default.
- Define what question the prototype answers and what outcome counts as “good”.

## Step 7 — Requirements + acceptance criteria
Make requirements falsifiable:
- Use must/should/could labels
- Include acceptance criteria, edge cases, and non-functional constraints
- Link requirements back to flows/states

Common failure mode: “requirements” that are actually aspirations.

## Step 8 — Quality gate + finalize
Before circulation:
- Run [CHECKLISTS.md](CHECKLISTS.md) and score [RUBRIC.md](RUBRIC.md)
- Ensure Risks/Open questions/Next steps exist
- Clearly mark decisions vs assumptions and who owns open questions

