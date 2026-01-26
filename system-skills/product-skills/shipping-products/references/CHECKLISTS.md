# Checklists

Use these checklists to decide go/no-go and to improve your shipping system over time.

## A) Stop-ship Product Quality List (PQL)

Mark each item as ✅ / ⚠️ / ❌ and include an owner for any ⚠️/❌.

### Correctness + UX
- [ ] Happy path is end-to-end and verified
- [ ] Key edge cases are tested (list them explicitly)
- [ ] UX states exist: loading, empty, error, permissions-denied
- [ ] Copy/labels are understandable to target users (no internal jargon)

### Security / privacy / compliance
- [ ] Data access and permissions reviewed
- [ ] Privacy/compliance requirements met (e.g., consent, retention)
- [ ] Threat/abuse considerations reviewed for high-risk releases

### Reliability / performance
- [ ] Performance tested for expected load (latency, throughput)
- [ ] Failure modes understood (timeouts, retries, rate limits)
- [ ] Rollback/revert plan is feasible within acceptable time

### Observability
- [ ] Key events/metrics instrumented (success + failure)
- [ ] Dashboard exists and has an owner
- [ ] Alerts configured with thresholds and routing

### Support readiness
- [ ] Help docs / release notes drafted
- [ ] Support macros / troubleshooting notes prepared
- [ ] Known issues documented with workarounds

### Launch readiness
- [ ] Rollout plan defined (phases + eligibility)
- [ ] Kill switch/flag plan validated (who can toggle, how fast)
- [ ] Go/no-go criteria defined and accepted by DRI

## B) Launch day runbook checklist
- [ ] Roles assigned (incident lead, comms lead, eng lead, support lead)
- [ ] Timeline defined (T-7d, T-1d, T0, T+1h, T+24h)
- [ ] Dashboards and links are in one place
- [ ] Escalation path documented (names + contact method)
- [ ] Stop-the-line triggers defined and agreed

## C) External launch checklist (if applicable)
- [ ] Customer messaging aligned (what/why/how)
- [ ] Release notes published (or scheduled)
- [ ] Docs/help center updated
- [ ] Sales/CS enablement complete (FAQs, talk track)
- [ ] Legal/PR review complete (if required)

## D) Post-launch checklist
- [ ] Success metrics reviewed against targets
- [ ] Guardrails checked for regressions
- [ ] Feedback gathered from Support/Sales/CS + users
- [ ] Incidents/issues documented with owners
- [ ] PQL updated based on escapes

