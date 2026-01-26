# Workflow (Expanded Guidance)

This file expands `../SKILL.md` with heuristics, options, and common failure modes.

## Core idea
A design system is an **operational system**: it reduces the cost of producing and changing UI by turning decisions into reusable primitives (tokens + components) plus guardrails (docs + governance).

This skill operationalizes 4 core ideas from the source:
1) **Separate logic from styling** using blockframes so hi-fi becomes fast and predictable.
2) **Plan for aesthetic shifts** (depth/texture/motion; AI-enhanced UI) by modeling the right tokens.
3) **Treat the system as an adoption lever** (often bottom-up) with champions and a clear operational “hook”.
4) **Design for non-experts**: the system should be easy to use correctly without a massive brand book.

## Step 1 — Define audiences and success signals
Heuristic: list “users” of the system explicitly. A single system often has multiple audiences:
- Designers (speed + consistency)
- Engineers (clear APIs + fewer edge cases)
- PMs (predictable patterns)
- Non-designers (templates and guardrails)

Failure mode: writing a “design system doc” without defining who it serves or how success is measured.

## Step 2 — Audit with an eye for the operational hook
Don’t start by building “a full component library”. Start by identifying:
- the **operational blocker** (what makes teams slow or inconsistent)
- a first slice that is **high leverage** (reused, user-visible, and pattern-setting)

Common operational hooks:
- enterprise customization (themes/white-label)
- scaling design output across multiple teams
- reducing UI bugs and review churn
- speeding up hi-fi production after lo-fi alignment

Failure mode: a broad wishlist with no narrow first slice.

## Step 3 — Blockframes: lock the heavy thinking first
Blockframes are **low-fidelity but system-aware** wireframes.
They encode structure and intent without debating pixels.

Recommended blockframe spec:
- layout grid + spacing scale (token names, not raw px)
- component placeholders labeled with intended component name
- state annotations (loading/empty/error) for key blocks

Why it works: once the system contracts are clear, hi-fi execution becomes “fill in the system” instead of re-inventing the UI each time.

Failure mode: skipping lo-fi alignment and trying to solve flow + aesthetics simultaneously.

## Step 4 — Token model: make style changeable
If you expect a visual evolution (e.g., moving beyond flat design), model the tokens that unlock it:
- elevation/shadow tokens
- surface/background tokens (layering)
- border/outline tokens (focus states)
- motion tokens (duration/easing) + reduced-motion rules

Rule of thumb: if a visual attribute will change across themes/eras, it should be tokenized.

Failure mode: hard-coded stylistic decisions inside components (makes re-skins expensive).

## Step 5 — Component model and roadmap
Tiering helps prevent “big bang” design systems:
- **Primitives**: buttons, inputs, typography, icons, spacing, elevation surfaces
- **Composites**: forms, tables, cards, menus
- **Patterns/recipes**: full page layouts and common flows

Roadmap heuristics:
- prioritize primitives that appear everywhere
- ship 1–2 “golden path” components end-to-end with docs and states
- explicitly list states (hover/focus/disabled/loading/empty/error)

Failure mode: building many components without docs, states, or usage rules.

## Step 6 — Make it usable by non-experts (teach by structure)
Design the system so it’s hard to do the wrong thing:
- sensible defaults and constrained variants
- “recipes” (copy/paste layouts)
- usage guidance that is example-first (do/don’t)

If your system requires a 60-page brand book to use, it will be used incorrectly.

Failure mode: docs are long and abstract; no starter templates; users cargo-cult styles.

## Step 7 — Governance + adoption (treat it like a product)
Adoption doesn’t happen because you publish components; it happens because:
- a real operational blocker is removed
- contribution is easy and safe
- champions exist and help teams migrate

Minimum governance elements:
- decision rights (who decides tokens/variants)
- contribution workflow (proposal → review → release)
- release cadence + versioning + changelog
- office hours / champion program

Failure mode: “no one owns it,” so it becomes stale or fragmented.

## Common failure modes (quick list)
- No operational hook → low adoption.
- Tokens are vague or inconsistent → every component becomes bespoke.
- Component APIs reflect implementation quirks, not user needs.
- Missing states/a11y rules → regressions and rework.
- No migration plan → old UI never transitions.

