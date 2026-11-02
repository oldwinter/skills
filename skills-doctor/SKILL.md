---
name: skills-doctor
description: Use when diagnosing the tools, operator identities, API scopes, resource roles, runtime dependencies, or approvals needed to execute skills, especially when handing a workflow to a teammate.
---

# Skills Doctor

Diagnose prerequisites, not business outcomes. Run under the intended operator's
own account. An administrator's successful run does not establish a colleague's
readiness.

## 1. Inventory The Target

Locate this installed skill's [bundled runner](scripts/doctor.py) and select the
checkout containing the skills to diagnose:

```bash
python3 <installed-skill>/scripts/doctor.py --repo-root <checkout> --all
python3 <installed-skill>/scripts/doctor.py --repo-root <checkout> --skill <name>
```

The runner uses Python 3.10+ and the standard library. It defaults to the caller's
working directory, not its own installation. Discovery uses the first existing
`.claude/skills`, `.agents/skills`, or `.codex/skills` directory, falling back to
the checkout root. Set repeatable `--skills-dir` paths to override that scope;
use `--skills-dir .` for a whole skill-library checkout.

Without a catalog, each skill remains **unverified**. Inline command mentions
are candidates, not proof of required tools or permissions. Offline discovery
does not run those commands, load `.env`, inspect credentials, or contact services.

Done: name the selected skills and distinguish observed tool hints from reviewed
requirements. Report unresolved dependencies rather than guessing.

## 2. Review Requirements

Read the selected skill, its relevant references, and required external skills.
For each execution branch, identify:

- Local executables and interpreter/package versions.
- Operator identity, API scopes, resource roles, and network reachability.
- External skill packages, agent Web/MCP tools, browser sessions and remote runtimes.
- The separate human approval needed for actual business operations.

Record the requirements in a target-local catalog using the
[catalog contract and example](references/catalog.md). Keep private hosts,
employee data, credentials, device paths and live reports in the consuming
repository, not in this reusable skill. A narrower branch must reflect the task:
onboarding marketing employees need not require host or AWS administration;
already-provisioned VPN access need not require VPN administrator rights.

```bash
python3 <installed-skill>/scripts/doctor.py --repo-root <checkout> \
  --catalog .skills-doctor.json --validate-catalog
python3 <installed-skill>/scripts/doctor.py --repo-root <checkout> \
  --catalog .skills-doctor.json --skill <name> --profile <branch>
```

Done: every selected capability has evidence sources, a granting owner, and a
repair action. Employee access being provisioned is distinct from the operator
permissions needed to provision it.

## 3. Probe Only The Authorized Scope

Read the target repository's live-safety instructions first. Live checks require
an explicitly selected skill, a reviewed catalog, and selected probe families:

```bash
python3 <installed-skill>/scripts/doctor.py --repo-root <checkout> \
  --catalog .skills-doctor.json --skill <name> --profile <branch> \
  --live github --github-org <organization>
```

For exact flags, evidence and limitations, read
[the diagnostic contract](references/diagnostic-contract.md).
Available probes cover Lark user scopes, GitLab administrator access/token scope,
GitHub organization ownership/token scope, AWS identity, and specific Kubernetes
RBAC actions. AWS identity alone does not prove IAM or billing permissions.

Manual capabilities stay unverified. The runner never attempts SSH/sudo/Rails
fallbacks, grants, login flows, messages, invitations or deployments.

Done: each capability is verified for its stated evidence, known blocked, or
explicitly unverified. Do not execute the business workflow merely to test access.

## 4. Hand Off

Report the tools, roles, remaining blockers, owners and minimum next actions.
Keep current-operator findings separate from the colleague's requirements.
Tool installation, logins, credential consent, privilege grants and business
operations require their own authorization. Use colleague-owned credentials;
administrator token/key/session copying is not a repair.

The default output is Markdown; `--format json` emits the same diagnostic data.
Use a private, ignored location for saved reports. Exit 2 means known blockers
or invalid input; exit 3 means unresolved checks; exit 0 is not business approval.

## Maintenance

The reusable skill ships the runner, fixed probes, and synthetic tests. Consumer
catalogs remain consumer-owned; the public example contains no organization
inventory. After changing the runner, run:

```bash
python3 -m unittest discover -s <installed-skill>/tests -p 'test_*.py'
```
