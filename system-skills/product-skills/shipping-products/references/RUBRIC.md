# Rubric (Shipping & Launch Pack)

Score each dimension from **1–5**.

- **5 (Excellent):** decision-ready; owners and thresholds explicit; low ambiguity
- **3 (Adequate):** usable but missing some specifics; moderate ambiguity
- **1 (Poor):** generic advice; missing key owners/criteria; high ambiguity

## Dimensions

1) **Clarity of release**
- 5: One-liner, audience, platforms/regions, and non-goals are explicit.
- 3: Mostly clear, but scope boundaries are fuzzy.
- 1: Unclear what is shipping or to whom.

2) **Rollout + rollback quality**
- 5: Phased rollout with eligibility, kill switch, rollback steps, and stop-the-line triggers.
- 3: Rollout exists, rollback is vague or missing triggers.
- 1: “Ship to everyone” with no rollback plan.

3) **Quality bar (PQL)**
- 5: Measurable stop-ship criteria with owners; known risks and mitigations listed.
- 3: Checklist exists but includes vague items; ownership unclear.
- 1: No explicit quality bar.

4) **Measurement + monitoring**
- 5: Success metrics + guardrails defined; dashboards/alerts owned; thresholds explicit.
- 3: Metrics exist, but monitoring/alerts are incomplete.
- 1: No plan to detect regressions or success.

5) **Comms + enablement**
- 5: Internal and external comms (if needed) are ready; docs/support enablement included.
- 3: Comms drafted but incomplete; enablement missing details.
- 1: No comms plan.

6) **Execution readiness**
- 5: Launch runbook with timeline, roles, and escalation path; go/no-go is checklist-based.
- 3: Some execution notes, but roles/timing unclear.
- 1: No runbook; launch is ad hoc.

7) **Learning loop**
- 5: Post-launch review scheduled; hypotheses and follow-ups defined; PQL update plan included.
- 3: Retro mentioned but not actionable.
- 1: No plan to learn or improve.

## Passing bar (recommended)
- **No open “stop-ship” items** on [CHECKLISTS.md](CHECKLISTS.md).
- Average score **≥ 4.0** across dimensions 1–7.
- If risk is high (permissions, money movement, availability), require: rollout+rollback = 5 and monitoring = 5.

