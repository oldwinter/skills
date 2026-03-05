# Intake (Questions)

Ask up to 5 questions at a time. If answers are missing, proceed with explicit assumptions and offer 2–3 options.

## A) System under test (SUT)
1) What is the AI feature’s job (one sentence), and what is explicitly out of scope?
2) What are the inputs and outputs (format, length, structured schema, tools)?
3) Who is the user and what workflow/UI does this sit in (human review vs fully automated)?

## B) Decision + stakes
4) What decision must the eval support (ship/no-ship, compare A vs B, regression gate, vendor choice)?
5) What are the highest-cost failures (legal/compliance, safety, trust, financial, brand)?

## C) Target behaviors + failure modes
6) List 3–10 “must-do” behaviors and 3–10 “must-not-do” behaviors.
7) What are known current failures (top 10 examples, or categories)?

## D) Data + coverage
8) Do you have real examples/logs we can use? If yes, can they be anonymized/redacted?
9) What languages, locales, and segments must be covered?
10) What coverage matters most: happy-path performance, long-tail edge cases, adversarial/safety, or structured correctness?

## E) Judging constraints
11) Are humans available to judge? How many, and how much time?
12) Is LLM-as-judge acceptable? Any restrictions (data sensitivity, provider)?
13) Do we need explainability for scores (auditability)?

## F) Operational constraints
14) Budget/time for eval runs (one-time vs continuous)? Required cadence (daily, per release, per prompt change)?
15) What is the “pass” threshold (overall and/or per critical tag)? Any “must be zero” categories?

## G) Output preferences
16) Do you want the AI Evals Pack as chat output only, or written as files? If files, what path?

