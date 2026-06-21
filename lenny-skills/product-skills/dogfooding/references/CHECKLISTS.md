# Checklists

Use these to validate the Dogfooding Pack and outcomes before finalizing.

## A) Scope + realism checklist
- [ ] The pack names the target **persona** and 1–3 **core workflows**
- [ ] Scenarios are end-to-end and have a clear “done” definition
- [ ] At least one scenario starts from an empty/new user state
- [ ] If the product is for creators, a real “creator commitment” exists (publish cadence + done definition)

## B) Safety + environment checklist
- [ ] Environment choice is explicit (prod vs staging) and justified
- [ ] Data handling rules are explicit (avoid real customer data unless safe/approved)
- [ ] No steps require credentials/secrets beyond normal product access
- [ ] Any privacy/security-risk issues are treated as S0 blockers

## C) Capture quality checklist (no vibes)
- [ ] Each logged issue includes repro steps + expected vs actual + evidence
- [ ] Each issue is tagged to a scenario and step
- [ ] Severity scale is defined and consistently applied
- [ ] Workarounds are recorded (so “success” isn’t hiding pain)

## D) Triage + actionability checklist
- [ ] Weekly triage cadence is defined (owner + meeting agenda)
- [ ] Top 3–5 issues have disposition + owner + next action
- [ ] “Won’t fix (why)” is recorded to prevent re-litigating
- [ ] “Fix now” list is realistically sized for the time box

## E) Ship gate checklist
- [ ] Ship gate is scenario-based (complete end-to-end) not ticket-based
- [ ] Fixes are re-verified by running the scenario again
- [ ] The report includes shipped + verified fixes (not just plans)

## F) Reporting checklist
- [ ] Weekly report includes decisions (fix now/schedule/won’t fix)
- [ ] Includes **Risks**, **Open questions**, **Next steps**
- [ ] Next dogfooding cycle focus is proposed (scenarios or segment)

