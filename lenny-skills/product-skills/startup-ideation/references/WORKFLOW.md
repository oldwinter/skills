# Expanded workflow & heuristics

This file expands the 8-step workflow in `../SKILL.md` with practical heuristics and guardrails.

## Core principles (rules + checks)

### Rule 1: Prefer off-the-beaten-path signals over imported ideas
- **Rule:** Favor ideas grounded in your lived experience, observed workflows, or privileged access.
- **Check:** Can you point to a specific moment/person/workflow where the pain is real?
- **Artifact:** “Signals” list + evidence bullets (see templates).

### Rule 2: Every idea must have a Why Now
- **Rule:** Every opportunity thesis must include an enabling shift (tech/behavior/regulation/distribution).
- **Check:** Could you convincingly explain why this is *more feasible* or *more needed* now than 3 years ago?
- **Artifact:** Shift scan + Why Now line per idea.

### Rule 3: Identify tarpits early
- **Rule:** Aggressively flag ideas where success depends on a miracle: winner-take-most dynamics, extreme cold start, brutal paid acquisition, low willingness to pay, or entrenched incumbents without a wedge.
- **Check:** Can you name the main structural reason this is hard, and a credible wedge that avoids it?
- **Artifact:** Tarpit notes + “wedge” section per idea.

### Rule 4: Turn “ideas” into testable theses
- **Rule:** An “idea” isn’t real until it has: customer, job, pain, Why Now, wedge, and a first test.
- **Check:** Could a stranger run the first test without inventing missing details?
- **Artifact:** Opportunity theses table.

## “Why Now” shift categories (prompts)
Use these prompts to generate shifts (then translate into opportunity theses):
- **Capability shift:** “A thing the computer can do now that it couldn’t before.”
- **Cost shift:** “It’s now cheap enough / fast enough to do X.”
- **Distribution shift:** “A new channel exists (or an old one changed) that makes acquisition different.”
- **Behavior shift:** “Users now expect/do X (remote work, mobile-first, creator economy, etc.).”
- **Regulatory shift:** “New rules create pain or unlock a market.”
- **Infrastructure shift:** “APIs/standards/platforms make integration possible.”

## Information diet plan (how to get off the beaten path)
The goal is to collect **non-obvious signals**.

### Sources to include
- 5–10 conversations with operators in your target domain (people doing the work)
- Niche forums/communities (industry Slack/Discord, subreddits, LinkedIn groups)
- Trade publications / analyst notes / technical blogs in the domain
- Public datasets (if relevant) + “what’s missing” notes
- “Edge” users: power users, admins, compliance, support, finance

### Anti-patterns
- Only reading generic tech news
- “Idea shopping” on social media without grounding in a workflow
- Copying well-known startups without a wedge (no unique insight/distribution)

## Tarpit patterns (non-exhaustive)
These aren’t “never do” categories, but they require a strong wedge.
- **Cold start marketplaces** without a credible supply/demand wedge
- **Consumer social** without novel distribution + retention loop
- **Ad-driven consumer** with no advantage in acquisition economics
- **Generic AI wrappers** with no proprietary data/workflow depth
- **Enterprise without credibility** (no domain proof, no procurement plan)

## Evidence standards (lightweight, early-stage)
Good early evidence can include:
- 5–10 consistent operator quotes
- Clear willingness-to-pay signals (budget owner pain, “we already pay for X”)
- Strong switching costs in current workaround (manual toil, risk, compliance)
- Tangible “pull” (requests for a pilot, LOIs, intros)

## Output format guidance
If producing files, write into a user-specified directory (e.g., `docs/startup-ideation/`) and avoid overwriting existing files without confirmation.

