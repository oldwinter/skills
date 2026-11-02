# Consumer Catalog

A catalog is a reviewed requirements map, not an executable script. Store it in
the **target checkout**, for example `.skills-doctor.json`, and select it with
`--catalog .skills-doctor.json`. Without one, the runner reports inventory hints
and keeps all skills unverified.

Start with [catalog.example.json](catalog.example.json). It is a fictional
`example` skill, not a map of this library or an organization. Replace its skill
name, source paths, capability details and profiles after reading the real skill.
The CLI does not create or overwrite a catalog automatically.

## Schema

The top-level keys are exactly `version` (integer 1), `capabilities`, and `skills`.
Each capability requires these fields:

| Field | Meaning |
|---|---|
| `tools` | Required local executable names, AND within the list; no arguments or shell commands |
| `permission` | Specific operator scopes/roles/resource access needed |
| `owner` | Who can grant or clarify that access |
| `remediation` | Minimum action needed to remove the blocker |
| `probe` | Fixed implementation identifier from the list below |
| `approval` | Human authorization required for the real operation |
| `runtime` | Unverified package/version/remote/agent dependencies; nonempty keeps overall status unverified |

Use empty `tools` for non-CLI capabilities such as an external skill package or
agent MCP tool, with `manual` probe and explicit runtime requirements.
Supported probes:

- `local`: PATH discovery only, not version or execution validation.
- `manual`: no automatic access test.
- `lark-contact`, `lark-send`, `lark-groups`.
- `gitlab-read`, `gitlab-admin`, `github-org`.
- `aws-identity`, `kube-read`, `kube-write`.

Each skill has exactly `sources` and `profiles`. Sources must exist inside the
target checkout and include the discovered `SKILL.md`. A profile is an AND list
of required capability IDs; a nested list represents OR alternatives:

```json
{
  "profiles": {
    "account-only": ["contact-read", ["admin-api", "delegated-host-admin"]],
    "report-only": ["report-read"]
  }
}
```

This snippet illustrates profile shape, not a complete valid catalog.
Use separate profiles when selecting different systems, read versus write work,
or an already-completed external step materially changes prerequisites.

Catalog skill names must exactly cover discovery scope. `--skill` selects what
to diagnose but does not relax catalog coverage. Narrow `--skills-dir` when a
catalog intentionally covers only part of a checkout. Symlinked child skill
directories and scratch/dependency directories are not walked; paths and sources
escaping the target root are rejected. Duplicate identifiers require narrowing
the directory scope.

## Live Targets

| Family | Required flags | Remaining limits |
|---|---|---|
| Lark | `--live lark` | User scopes only; contact/group resource access needs separate review |
| GitLab | `--live gitlab --gitlab-host <origin-host>` | Host must match checkout origin and API identity; no SSH fallback |
| GitHub | `--live github --github-org <org>` | Organization owner/classic scope; fine-grained permission can remain unknown |
| AWS | `--live aws --aws-profile <name> --aws-account <expected-id>` | STS identity does not verify action permissions |
| Kubernetes | `--live kube --kube-context <name> --namespace <name>` | Only the displayed RBAC verbs/resources are checked |

Names of private targets, identities and raw responses are not printed in
reports. Reports can still contain sensitive source filenames or custom
permission descriptions from the consuming catalog. Review them before sharing.

## Update Discipline

1. Read the changed skill branch and its references.
2. Update the consumer catalog, keeping private organization policy local.
3. Run `--validate-catalog` and an offline report for the affected profile.
4. Review lexical tool hints against the source; examples, remote commands and
   prohibited operations are not automatically local prerequisites.
5. Run only the bounded live probes the operator has authorized.

Catalog validation proves schema and coverage, not that human-curated permission
claims are complete or correct.
