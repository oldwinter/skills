# Checklists

Use this checklist before finalizing the pack.

## A) Scope + contracts
- [ ] “When to use / When NOT to use” is explicit and matches the request.
- [ ] Inputs are sufficient; missing info is handled via explicit assumptions.
- [ ] Deliverables are explicit and ordered.

## B) Platformization quality
- [ ] Shared capability candidates have 2+ consumers or clear near-term reuse.
- [ ] Each shared capability has a proposed contract (API/schema/SDK) and ownership model.
- [ ] Migration/rollout plan exists (compatibility, versioning, deprecation).

## C) Infrastructure quality attributes
- [ ] Reliability and performance targets are measurable (SLOs/SLIs or proxy metrics).
- [ ] Privacy/safety requirements are spelled out (encryption, residency, retention, access controls).
- [ ] Operability is covered (dashboards, alerts, on-call ownership, runbooks).
- [ ] Cost guardrails are included (budgets, top drivers, caps/alerts).

## D) Scaling readiness (“doomsday clock”)
- [ ] Top limits are enumerated with current values (or explicit estimates).
- [ ] Trigger thresholds fire early enough given mitigation lead time.
- [ ] Each trigger has an owner and a named mitigation project.
- [ ] Clear policy exists for reprioritization/feature freeze if triggers fire.

## E) Instrumentation + analytics
- [ ] Observability gaps are identified with owners and priorities.
- [ ] Canonical events are captured server-side where possible.
- [ ] Identity strategy is defined (user/account/anonymous) with merge rules.
- [ ] Data quality checks are defined (schema, volume anomalies, null rates, dedupe).

## F) Discoverability (if applicable)
- [ ] “Discoverability plan” is explicitly marked applicable or not.
- [ ] Sitemap and internal-linking rules prevent orphan pages.
- [ ] Indexability controls (noindex/canonicals/robots) are intentional.

## G) Execution readiness
- [ ] Roadmap milestones have acceptance criteria and owners.
- [ ] Dependencies and rollout/rollback plans are included.
- [ ] Risks, open questions, and next steps are present and actionable.

