# devops-skills

## OVERVIEW
DevOps, infrastructure, CI/CD, and cloud operations skills.

## SKILLS (16)
| Skill | Description |
|-------|-------------|
| `argocd-cli` | GitOps deployments with ArgoCD |
| `aws-api-billing-service-onboarding` | AWS billing/quota monitoring integration |
| `aws-cli` | AWS service management via CLI |
| `aws-cost-explorer` | AWS cost and usage analysis |
| `aws-support-case` | AWS Support case management (bilingual) |
| `cloudflare-deploy` | Deploy to Cloudflare Workers/Pages |
| `github-cli` | GitHub operations via `gh` CLI |
| `gitlab-cli` | GitLab operations via `glab` CLI |
| `kargo-cli` | Progressive delivery with Kargo |
| `kubectl-cli` | Kubernetes cluster operations |
| `release-skills` | Universal release workflow (Node.js, Python, Rust, etc.) |
| `simplex-cli` | Simplex Router admin CLI |
| `sync-ci-to-staging` | Sync CI configs to staging |
| `sync-ci-to-staging-prod` | Sync CI configs to staging and production |
| `sync-env` | Sync CI environment configs with safety gates |
| `sync-to-prod` | Promote staging configuration to production |

## WHERE TO LOOK
| Task | Location |
|------|----------|
| CLI runbooks | `devops-skills/*/SKILL.md` |
| Extended docs | `devops-skills/*/references/` |

## CONVENTIONS
- Skill entrypoint is `SKILL.md`.
- Many skills are "CLI wrapper" style (kubectl, AWS, ArgoCD, etc.).

## ANTI-PATTERNS
- Don't copy/paste production-impacting commands without checking the skill's DO/DO NOT guidance (some skills contain explicit "never run X automatically").
