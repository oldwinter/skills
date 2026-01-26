# Source Summary (Refound/Lenny → Agent Skill)

Source: `sources/refound/raw/designing-surveys/SKILL.md`

The original skill is an **insight collection** (tactical advice from multiple product leaders) with a partial set of highlighted insights and a pointer to deeper guest notes that are not present in the raw source folder.

This skill pack converts the available insights into an **execution contract**: clear scope, input/output contracts, a step-by-step workflow, and reusable templates/checklists for a PM to ship a decision-ready survey.

## Preserved core insights → rules, checks, artifacts

### 1) Force prioritization + measure frequency (Nicole Forsgren)
- **Insight (preserved):** Diagnostics should force prioritization (e.g., top 3 barriers) and include frequency to weight impact.
- **Rule:** For driver/funnel/friction surveys, use “pick top 3” diagnostics and capture frequency/impact for weighting.
- **Check:** Can you produce a ranked list of issues weighted by frequency/impact (not just a popularity list)?
- **Artifact:** Forced-ranking + frequency blocks in `references/TEMPLATES.md` (Common question blocks D) and checklist items C.

### 2) Use behavior as a “survey” when possible (Chris Hutchins)
- **Insight (preserved):** Ad/landing funnel metrics can validate messaging/expectations without asking opinions.
- **Rule:** If the real question is “does this message work?”, prefer a behavioral test (CTR/conversion) over a self-report survey.
- **Check:** Is there a measurable funnel (impression → click → sign-up) tied to the decision?
- **Artifact:** Launch guidance + alternative method in `references/WORKFLOW.md` Step 6.

### 3) Profile people early; keep onboarding surveys short (Elena Verna)
- **Insight (preserved):** Onboarding profiling helps distinguish buyer vs user and prevents irrelevant outreach.
- **Rule:** For onboarding surveys, ask only the minimum profile questions needed to personalize onboarding/routing, and keep to ~3–4 screens.
- **Check:** Can you name the immediate product/ops decision each profile question enables?
- **Artifact:** Onboarding profiling block in `references/TEMPLATES.md` (Common question blocks E) + checklist items A/C.

### 4) Survey “best customers” with fresh memory (Gia Laudi)
- **Insight (preserved):** For journey/trigger research, survey best customers who signed up 3–6 months ago.
- **Rule:** For “why they adopted” questions, target recent-but-stable best customers and ask about the trigger moment and prior alternatives.
- **Check:** Does the sampling definition ensure respondents remember the switch story?
- **Artifact:** Sampling guidance in `references/WORKFLOW.md` Step 2 and trigger-moment block in `references/TEMPLATES.md` (Common question blocks F).

### 5) NPS is often flawed; prefer CSAT and good scales (Judd Antin)
- **Insight (preserved):** NPS has known survey-science issues; CSAT is often more precise and better correlated; scales must render well on mobile.
- **Rule:** Default to CSAT (1–7) with clear labeling; if NPS is required, pair it with a diagnostic follow-up and treat it as one signal.
- **Check:** Are all scale points visible on mobile and are endpoints labeled clearly?
- **Artifact:** CSAT/NPS templates in `references/TEMPLATES.md` + instrument QA checklist items D.

