# Templates (copy/paste)

## 1) Vibe Coding Brief

### Demo promise (one sentence)
“In <timebox>, we will demo <hero scenario> for <target user>.”

### Context
- **What we’re prototyping:**  
- **Target user:**  
- **Where it fits (internal/customer/concept):**  
- **Demo audience:**  

### Non-goals (3–5)
-  

### Success criteria (demo-ready)
- The user can:  
- The demo shows:  
- Reliability requirement (what must not break):  

### Constraints
- Timebox:
- Platform preference:
- Data sensitivity / compliance:
- Tools allowed (read/write/terminal):

### Fake vs real (decisions)
- Data: mock | real (minimum: )
- Integrations: stub | live (minimum: )
- Auth: none | fake | real (minimum: )

## 2) Prototype Spec (minimum build contract)

### User flow (hero scenario)
1)  
2)  
3)  

### Screens / components (MVP)
- Screen/component:
  - Purpose:
  - Inputs:
  - Outputs:
  - Edge cases:

### Data model (prototype-level)
- Entities:
- Example data (mock):

### Integrations (if any)
- API/file/database:
  - What it’s used for:
  - What can be stubbed:
  - Failure handling:

### Acceptance criteria (observable)
- [ ]  
- [ ]  

### Out of scope
-  

## 3) Build Plan + Task Board (vertical slices)

Create 3–8 slices. Each slice must end with a runnable, user-visible improvement.

| Slice | User-visible behavior | Agent prompt (short) | Validation (steps/tests) | Notes |
|------:|------------------------|----------------------|--------------------------|-------|
| 1 | | | | |
| 2 | | | | |

## 4) Prompt Pack (safe vibe coding)

### Prompt A — Scaffold a runnable thin slice
Context:
- Goal: <demo promise>
- Platform/stack: <constraints>
- Keep it minimal and runnable.

Instructions:
- Propose a plan (3–6 bullets) before writing code.
- Keep changes small and localized; avoid broad refactors.
- List files you will create/modify.
- Include exact run commands.
- Do not add secrets, keys, or credentials.
- If anything is risky or destructive, stop and ask for confirmation.

Output:
1) Plan
2) File list
3) Patch/diff (or file contents)
4) Run instructions
5) Quick manual test steps

### Prompt B — Implement the next vertical slice
Inputs:
- Current state: <what works now>
- Next slice: <one user-visible behavior>
- Acceptance criteria:

Constraints:
- Keep existing behavior working.
- Prefer simple solutions over “best practice” architecture.

Output:
- Plan + diff + validation steps.

### Prompt C — Debug a break (fast triage)
Inputs:
- Error message / symptom:
- Steps to reproduce:

Instructions:
- Start with the smallest change likely to fix it.
- Suggest 1–3 hypotheses; pick the most likely.
- Provide a verification step after the fix.

## 5) Demo Script + Runbook

### Runbook (how to run)
- Prereqs:
- Setup:
- Run command:
- Where to open it:
- Known limitations:

### Demo talk track (3–5 minutes)
1) Context (who/why):
2) Hero scenario walkthrough:
3) “What’s real vs faked”:
4) What we learned:
5) Next steps:

### Backup plan (if it breaks)
- Screenshot/video fallback:
- Alternate flow:

## 6) Risks / Open questions / Next steps

### Risks (with mitigations)
- Risk:
  - Mitigation:

### Open questions
-  

### Next steps (prioritized)
1)  
2)  

