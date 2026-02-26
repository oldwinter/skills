# Examples (Expanded)

These examples show what a “good” Growth Loop Design Pack looks like (structure + level of specificity), plus a boundary case.

## Example 1 — B2B SaaS (integration/partner loop)

**Context snapshot**
- Product: AI onboarding assistant for HR teams
- Stage: early growth (some PMF in mid-market)
- Goal: +30% WAU in 90 days (mid-market segment)
- Constraints: limited engineering (2 devs), brand-safe only

**Selected loop (integration/partner loop)**
- Input: HRIS marketplace listing views
- Action: Install integration → run “first value” onboarding
- Output: “integration active” → internal referrals + co-marketing exposure
- Feedback: more installs and listings views

**First experiments**
- Add a “guided setup” flow that cuts time-to-first-integration by 50%
- Create 3 co-marketing assets with top partners; measure listing → install conversion

## Example 2 — B2C (viral/content loop)

**Context snapshot**
- Product: mobile photo editor for creators
- Stage: early PMF (retention decent for power users)
- Goal: 3× MAU in 8 weeks
- Constraint: no paid budget; platform policy compliance required

**Selected loop (share-to-social loop)**
- Input: active creators editing photos
- Action: export with share prompt
- Output: shared content on IG/TikTok with deep link
- Feedback: new users install → become creators → share

**First experiments**
- A/B test share UX (timing + CTA), measure share_rate and install_from_share
- Add templates that increase “export worthy” outcomes; measure export_rate

## Boundary example — Not a loop problem

Prompt: “Write our landing page headlines.”

Response: This is primarily messaging/copywriting. Ask whether the user wants:
- a messaging framework + copy drafts, or
- loop design + distribution mechanics

If it’s copy, use `copywriting` (or a messaging-focused skill) rather than this one.

