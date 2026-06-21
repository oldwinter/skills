# Templates (Scoping & Cutting)

Copy/paste these templates to produce a Scoping & Cutting Pack.

## 1) Scoping & Cutting Pack (full outline)

```md
# Scoping & Cutting Pack — <short name>

## 1. Context snapshot
- Product:
- Target user/segment:
- Decision to make (ship/defer/stop) + DRI:
- Appetite / ship date:
- Constraints (tech/legal/privacy/dependencies/capacity):

## 2. Outcome + hypothesis (MVP = test)
**Outcome (user value):**
- ...

**Key hypothesis (or 2–3):**
- ...

**Success metric(s):**
- ...

**Guardrails (must not worsen):**
- ...

## 3. Appetite + success bar
- Time budget (appetite):
- Team:
- “Done means…” (acceptance bar, not full PRD):
- Non-negotiables:

## 4. Minimum Lovable Slice (MLS) spec
**Core end-to-end flow (happy path):**
1) ...

**Must-haves (ship in this appetite):**
- ...

**Explicit non-goals (won’t do now):**
- ...

**Assumptions:**
- ...

## 5. Cut list (keep / cut / defer)
| Item | Keep / Cut / Defer | Why (tie to outcome/appetite) | Risk impact | “Revisit when…” trigger |
|---|---|---|---|---|
|  |  |  |  |  |

## 6. Validation plan (Wizard-of-Oz / concierge / prototype)
**Top assumption(s) to validate (1–3):**
- ...

**Method:**
- Type: (Wizard-of-Oz / concierge / prototype / scripted demo)
- Audience:
- Script / flow:
- Data to collect:
- Success criteria:
- Failure criteria:
- Timeline:

## 7. Delivery plan + scope-change guardrails
**Milestones (fit inside appetite):**
- Week 1:
- Week 2:
- ...

**Scope-change policy (“trade, don’t add”):**
- Rule:
- Decision owner:
- How to evaluate requests:
- What gets traded off first:

## 8. Risks / Open questions / Next steps
**Risks:**
- ...

**Open questions:**
- ...

**Next steps (owners + dates):**
- ...
```

## 2) Cut-list decision prompts
- Does this item change the core outcome or only convenience?
- Is it needed for the happy path or only an edge case?
- Can we fake it (manual ops) for the first iteration?
- What’s the cost of being wrong if we defer it?
- What evidence says we need it now (vs “just in case”)?

## 3) Scope-change policy (short version)

```md
### Scope-change policy
- We treat time as fixed (appetite). Scope is the variable.
- New requests require trading off an equal-or-greater amount of work.
- Decision owner: <name/role>. Escalation: <name/role>.
- Default trade-offs: edge cases → integrations → advanced settings → polish (keep trust/safety bars intact).
```

