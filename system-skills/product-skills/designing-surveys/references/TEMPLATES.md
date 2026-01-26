# Templates (Designing Surveys)

Copy/paste templates for the **Survey Pack** deliverables.

## 1) Survey Pack (outline)

### A) Context snapshot
- Decision to inform (by date):
- Survey type:
- Primary audience:
- Distribution channel(s):
- Constraints (time, n, regions, privacy):
- Known context / existing evidence:

### B) Survey brief
- Goal (1 sentence):
- Hypotheses / unknowns:
- Target population + sampling frame:
- Segment cuts (must-have comparisons):
- Timing + cadence (one-off vs recurring):
- Incentive (if any):
- Success criteria (response rate, completion, decision readiness):
- Data/privacy notes:

### C) Questionnaire (question list)
Provide a numbered list or table with:
- Question ID (Q01…)
- Question text
- Response type (single choice, multi, scale, text)
- Options / scale labels
- Required? (Y/N)
- Logic (if any)
- Rationale (what decision it supports)

### D) Survey instrument table (implementation-ready)
Same as questionnaire, but formatted for building in a tool (copy/paste).

### E) Analysis + reporting plan
- Primary metric(s) and how computed:
- Segment cuts:
- Diagnostic ranking method:
- Open-ended coding plan:
- Decision thresholds:
- Reporting format + audience:

### F) Launch plan + QA checklist
- Pilot plan:
- Launch schedule:
- Reminder plan:
- Monitoring plan:
- Close-the-loop plan:

### G) Risks / Open questions / Next steps

---

## 2) Survey brief (copy/paste)

**Decision to inform (by date):**  
**Goal:**  
**Primary audience:**  
**Survey type:**  
**Channels:**  
**Sampling frame:**  
**Segment cuts:**  
**Incentive:**  
**Success criteria:**  
**Privacy/compliance constraints:**  
**Assumptions:**  

---

## 3) Questionnaire table (copy/paste)

| ID | Section | Question | Type | Options / Scale | Required | Logic | Rationale |
|---:|---|---|---|---|:---:|---|---|
| Q01 |  |  |  |  |  |  |  |

ID guidance:
- Use stable IDs (Q01, Q02…) so analysis and iteration stay consistent.
- For matrix questions, still assign IDs per row if you’ll analyze them independently.

---

## 4) Survey instrument table (CSV-like skeleton)

Columns:
- `id,section,question,type,options,required,logic,notes`

Example row (scale):
- `Q01,CSAT,Overall how satisfied are you with <X>?,scale_1_7,"1 Not at all satisfied|2|3|4|5|6|7 Extremely satisfied",Y,,Primary satisfaction metric`

---

## 5) Analysis + reporting plan (copy/paste)

**Primary metric(s):**
- Metric:
- Calculation:

**Cuts (predefined):**
- Segment 1:
- Segment 2:

**Diagnostics:**
- If using “pick top 3”, compute:
  - % selected in top-3
  - weighted score = (% selected) × (frequency/impact weight)

**Open-ended coding:**
- Tag list v0 (10–20 tags):
- Coding rules:
- Output: top themes + example quotes + differences by segment

**Decision thresholds:**
- If CSAT < __ for segment __, then __
- If barrier weighted score > __, then __

**Reporting:**
- Format:
- Audience:
- Decisions to capture:

---

## 6) Launch plan (copy/paste)

**Pilot (recommended):**
- Who:
- n:
- What you’re looking for:
- Changes you’ll make after pilot:

**Launch schedule:**
- Start:
- End:
- Reminder(s):

**Monitoring:**
- Response rate target:
- Completion rate target:
- Drop-off watchpoints:
- Segment mix watchpoints:

**Close the loop:**
- What respondents will hear back:
- When:
- Channel:

---

## 7) Common question blocks (copy/paste)

### A) CSAT (recommended default)
- CSAT: “Overall, how satisfied are you with <experience>?”
  - Scale: 1–7 (label endpoints; ensure mobile visibility)
- Follow-up (text): “What is the primary reason for your score?”

### B) NPS (only if required)
- NPS: “How likely are you to recommend <product> to a friend or colleague?”
  - Scale: 0–10 (show all options on mobile)
- Follow-up (text or single choice): “What is the primary reason?”

### C) PMF (Sean Ellis)
- “How would you feel if you could no longer use <product>?”
  - Very disappointed / Somewhat disappointed / Not disappointed
- “What is the primary benefit you receive from <product>?” (text)

### D) Forced prioritization (top barriers)
- “What are your top 3 barriers to <job>?” (pick up to 3)
  - Option list + Other (text)
- “How often do these barriers affect you?” (per selected barrier; daily/weekly/monthly/rarely)
- Optional: “How severe is the impact?” (blocks work / slows me down / minor)

### E) Onboarding profiling (buyer vs user)
- Role:
- Department/function:
- Company size:
- Primary use case:
- “Are you evaluating for yourself or for a team?”

### F) Trigger moment (best customers cohort)
- “What was happening in your work/life that made you start looking for a solution like this?”
- “What did you try before <product>?”
- “What was the moment you decided to try <product>?”

