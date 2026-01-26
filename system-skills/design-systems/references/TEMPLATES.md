# Templates

Use these templates to produce a **Design System Operating Pack**. Output in-chat by default, or write to files if requested.

## 1) Context snapshot
**Product / area in scope:**  
**Platforms in scope:**  
**Primary system users:** (designers/engineers/PMs/non-designers)  
**Why now:**  
**Success signals:** (adoption, speed, consistency, bug reduction)  
**Current state:** (Figma/code/docs/governance)  
**Constraints:** (timeline, staffing, a11y/compliance, theming/enterprise)  
**Assumptions:**  

## 2) Design system charter
**Mission (1 sentence):**  
**Problem statement:** (what it fixes operationally)  
**Audiences:** (who it’s for)  
**Scope (in):**  
**Scope (out):**  
**Principles:** (3–5)  
**Anti-goals:** (what you won’t optimize for)  
**Decision-maker(s):**  
**Interfaces:** (Design ↔ Eng ↔ PM)  
**Release cadence:** (weekly/biweekly/monthly)  
**Success metrics:**  

## 3) UI audit + operational blockers
### Inventory (sample table)
| Area/flow | What’s inconsistent today | Operational impact | Proposed system fix (token/component/pattern) | Priority |
|----------:|---------------------------|--------------------|-----------------------------------------------|---------|
| | | | | P0/P1/P2 |

### Operational hook (write 3 bullets)
- Primary blocker:
- Secondary blocker:
- “First slice” to ship:

## 4) Blockframe-to-component map
### Blockframe spec (copy/paste)
- Grid/layout:
- Spacing scale (token names):
- Component placeholders labeled:
- State annotations (loading/empty/error):
- Notes for accessibility/keyboard flow (if relevant):

### Mapping table
| Blockframe section | Intended component/pattern | Tokens used | States required | Notes |
|-------------------|----------------------------|------------|----------------|------|
| | | | | |

## 5) Token model + token backlog
### Token taxonomy (example structure)
| Category | Token examples | Usage rules | A11y/behavior notes |
|---------|----------------|------------|---------------------|
| Color (semantic) | `color.text.primary` | Use semantic tokens, not raw values | Contrast targets |
| Spacing | `space.1..space.8` | No ad-hoc px | Grid alignment |
| Type | `font.size.*` | Use scale | Minimum size |
| Radius | `radius.sm/md/lg` | Consistent rounding | — |
| Elevation | `elevation.1..elevation.5` | Use for depth/layering | Avoid excessive shadows |
| Motion | `motion.duration.*` | Consistent durations | Reduced motion rules |

### Token backlog
| ID | Token / change | Why | Dependencies | Owner | Priority | Notes |
|---:|----------------|-----|--------------|-------|---------|------|
| 1 | | | | | P0/P1/P2 | |

## 6) Component inventory + roadmap
### Component tiering
- **Primitives:**  
- **Composites:**  
- **Patterns/recipes:**  

### Backlog table
| ID | Component/pattern | Tier | Reuse | User impact | Complexity/risk | Dependencies | Owner | Milestone |
|---:|-------------------|------|-------|------------|-----------------|--------------|-------|----------|
| 1 | | | High/Med/Low | High/Med/Low | High/Med/Low | | | M1 |

### Milestones
| Milestone | Outcome | Scope | Acceptance criteria | Rollback/stop condition |
|-----------|---------|-------|---------------------|--------------------------|
| M1 | | | | |

## 7) Documentation + enablement plan
### Doc set (minimum)
- Quickstart: “How to build a screen using the system”
- Component pages: usage + variants + states + do/don’t
- Recipes: common layouts and flows
- Contribution guide: how to request/add/change

### Enablement plan
| Audience | Common mistakes | Guardrails to add | Enablement tactic |
|---------|------------------|-------------------|-------------------|
| Non-designers | | | templates, office hours |
| Designers | | | reviews, libraries |
| Engineers | | | Storybook, PR checklist |

## 8) Governance + adoption plan
### Decision rights (lightweight RACI)
| Area | Responsible | Approver | Consulted | Informed |
|------|-------------|----------|-----------|----------|
| Tokens | | | | |
| Components | | | | |
| Visual direction | | | | |

### Contribution workflow (copy/paste)
1) Request/proposal (problem + screenshots + desired outcome)
2) Triage (P0/P1/P2; assign owner)
3) Spec (states, tokens, a11y; acceptance criteria)
4) Review (design + engineering)
5) Release (version + changelog)
6) Adoption (migration notes + office hours)

### Champion plan
| Champion/team | Why they’ll adopt | What they get | Ask | Support needed |
|--------------|-------------------|---------------|-----|----------------|
| | | | | |

## 9) Risks / Open questions / Next steps
**Risks:**  
**Open questions:**  
**Next steps (1–3):**  

