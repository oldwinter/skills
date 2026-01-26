# Workflow (Expanded Guidance)

This file expands `../SKILL.md` with heuristics, options, and common failure modes.

## Core idea
Design engineering is a **bridge function**: it reduces the gap between intent (design) and reality (shipped UI) by owning:
- high-fidelity prototyping when it accelerates learning
- production-quality UI implementation when it reduces rework
- a repeatable design-to-code contract (tokens, components, review gates)

## Step 1 — Define the “why now” and success signals
Common success signals:
- shorter cycle time from design-ready → shipped
- fewer “UI polish” bugs and less rework
- higher consistency across surfaces (components, spacing, typography)
- improved accessibility coverage and fewer regressions

Failure mode: treating design engineering as a “nice-to-have polish layer” instead of a system that reduces waste.

## Step 2 — Pick an operating model intentionally
Common models:
- **Embedded:** design engineer sits with a product squad to ship key flows end-to-end.
- **Platform/design system:** design engineer focuses on components, tokens, and documentation.
- **Tiger team:** short-term high-impact push (new IA, redesign, major UI migration) with clear end date.

Heuristic:
- If your problem is **inconsistency + repeated rework**, start with platform/design system.
- If your problem is **one critical flow needs high craft**, start embedded/tiger team.

Failure mode: unclear boundaries (“Design owns quality” but can’t ship; “Eng owns UI” but can’t interpret design).

## Step 3 — Start with a leverage map, not a component wishlist
Prioritize by:
- **user impact** (top tasks/flows)
- **reuse** (components used in many places)
- **risk** (complex interaction states, performance/a11y pitfalls)

Avoid: starting with low-leverage components just because they’re easy.

## Step 4 — Create a prototype ladder and label “throwaway vs shippable”
Recommended ladder (adjust):
1) **Lo-fi** (paper/wireframes): explore IA and flow.
2) **Hi-fi** (design mock): lock key layout/visual rules.
3) **Coded prototype**: validate interaction fidelity and constraints.
4) **Production**: maintainable, tested, measurable.

Rule of thumb: if a coded prototype uses production components/tokens, treat it as “shippable” and apply the quality bar; otherwise label it throwaway.

Failure mode: shipping prototypes as production without quality gates (“it worked on my machine” UI).

## Step 5 — The design-to-code contract (what prevents rework)
The fastest teams define the contract for a component/flow:
- required states (loading/empty/error/disabled/focus/hover)
- spacing/typography tokens (no ad-hoc pixels)
- a11y requirements (keyboard, focus order, ARIA as applicable)
- responsiveness and i18n truncation rules
- acceptance criteria + screenshots for PRs

Failure mode: “pixel perfect” without a system; every change is bespoke.

## Step 6 — Make delivery incremental and pattern-setting
Prefer milestone sequencing:
1) establish tokens + linting conventions (if missing)
2) ship 1–2 “golden path” components with docs and tests
3) scale to the next tier of components/flows

Failure mode: trying to rebuild the whole UI library at once.

## Step 7 — Quality gates that don’t slow you down
Quality gates should be lightweight and automatable where possible:
- PR template includes screenshots and states checklist
- Storybook previews (or equivalent) for visual review
- basic accessibility checks per component
- visual regression tests if available (optional)

Failure mode: quality depends on a single person’s taste; the bar is not documented.

