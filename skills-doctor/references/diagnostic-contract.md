# Diagnostic Contract

## Output And Exit Status

`--format json` emits a versioned report; the default Markdown contains the same
requirements, evidence states, owners, and remedies. Standard output is the only
report destination. For a private local artifact:

```bash
mkdir -p .local/skills-doctor
umask 077
python3 <installed-skill>/scripts/doctor.py --repo-root <checkout> --all --format json > .local/skills-doctor/inventory.json
```

| Exit | Meaning |
|---|---|
| 0 | All selected declared prerequisites verified, or catalog validation passed. Not authorization or workflow success. |
| 2 | Known required capability failure, invalid scope, or catalog/schema/coverage error. |
| 3 | No known required failure, but one or more prerequisites remain unverified. |

Read the JSON summary even on exit 2 or 3. `any_of` alternatives are OR; separate
requirement rows are AND. A denied GitLab API path with an unverified Rails path
is unverified overall, not success and not proof that both paths are denied.
Targets, raw responses, account IDs, and identities are omitted; an identity
fingerprint lets repeated runs be correlated without publishing the identity.

`verified` on an access check describes only its stated evidence. Additional
runtime requirements keep the aggregate unverified. For example, Node being
installed does not establish that the FeiLian helper can resolve `playwright-core`
or launch its Chromium installation.

## Probe Boundaries

Offline mode discovers tools with `PATH` lookup and reads only the catalog and
skill documents. It does not import third-party packages, inspect credential
files, source environment files, query remote endpoints, or run skill examples.

Live mode requires explicitly named skills and probe families. Commands are
hardcoded in the bundled `scripts/skills_doctor/probes.py`; the catalog cannot supply an
executable command. Each command has a 1-30 second timeout, no input prompt, a
bounded retained response, and a per-run cache. Raw responses use private,
automatically removed temporary files and are never printed, even on errors.

| Family | Read-only evidence | What remains unproven |
|---|---|---|
| Lark | Verified **user** login and required scopes | Contact visibility, tenant/app range, DM acceptance and per-group membership/invite rules |
| GitLab | Repository/API host match, active identity; admin settings read plus active PAT `api` scope for user administration | Alternative SSH/Rails path; non-PAT write scopes; individual project access for generic read workflows |
| GitHub | Active owner membership in the selected organization plus classic token organization-write scope | Fine-grained token member-write permission when scopes are not exposed; invitation acceptance |
| AWS | Explicit profile and expected account match | Every action-specific IAM permission, SCP, boundary and billing-account entitlement |
| Kubernetes | Explicit context/namespace and `auth can-i` for the displayed actions | Other verbs/resources, admission policy, runtime health, and execution approval |

AWS profile selection removes ambient access-key variables from the child
process so another account cannot silently override the requested profile.
Kubernetes authorization reviews do not create or mutate workloads.

The doctor never calls host sudo, SSH, Rails, `auth login`, Terraform plan/apply,
ArgoCD sync, Kargo promotion, password reset, group invite, or message send.
Repository-specific `just doctor` implementations are separate diagnostics;
their configuration and safety contract do not transfer to this runner.

## Catalog Maintenance

Each capability declares local executables, permission, access owner, repair
instruction, a fixed probe identifier, execution approval, and any unverified
target/runtime dependencies. Skill entries link existing evidence files and
declare execution profiles. A profile is a list of required capability IDs;
an array in that list is a choice of alternative capability IDs.
External skill packages, agent web/MCP tools, and remote-host runtimes are manual
capabilities: they cannot be inferred from a local CLI being on `PATH`.

The catalog validator rejects unknown keys/probes/capabilities, missing evidence,
paths escaping the repository, and missing or stale skill entries. Tool hints
are lexical discovery aids; prose mentions and optional branches can be false
positives. Follow the source before changing a requirement.

When transferring a workflow, review all four independent boundaries:

1. Local tools and the selected helper's runtime dependencies.
2. Operator identity and authentication scope.
3. Resource-specific authorization and network reachability.
4. Human approval for the actual operation.

A doctor report never supplies the fourth boundary.
