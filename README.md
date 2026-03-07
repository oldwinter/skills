# Skills Repository

A comprehensive collection of skills for multiple AI agents (Codex, Claude Code, Cursor, etc.), organized by category.

---

## Directory Structure

```
skills/
├── AGENTS.md              # Agent instructions (CLAUDE.md → symlink)
├── README.md
├── base-skills/           # Foundational / cross-domain skills (6 skills)
├── devops-skills/         # DevOps and infrastructure (16 skills)
├── lenny-skills/          # Lenny / Refound AI skill packs (119 skills)
│   ├── leadership-skills/ #   Leadership & management (29 skills)
│   ├── marketing-skills/  #   Marketing & content (25 skills)
│   ├── product-skills/    #   Product management & growth (37 skills)
│   ├── sales-skills/      #   Sales & GTM (8 skills)
│   └── (direct skills)    #   Career, AI, communication, etc. (20 skills)
├── meta-skills/           # Skills about skills — creation, sync, review (6 skills)
├── obsidian-skills/       # Obsidian note-taking & vault management (6 skills)
└── tools-skills/          # Tooling & automation helpers (5 skills)
```

## Skills by Category

### Base Skills (6 skills)
Foundational skills used across many workflows:
- **context7** — Library documentation lookup via Context7 API
- **firecrawl** — Web scraping, search, and crawling (LLM-optimized markdown)
- **humanizer-zh** — Remove AI-generated patterns from Chinese text
- **remotion-best-practices** — Best practices for Remotion video creation in React
- **supabase-postgres-best-practices** — Postgres performance optimization from Supabase
- **ui-ux-pro-max** — UI/UX design intelligence (50 styles, 9 stacks, shadcn/ui)

### DevOps Skills (16 skills)
Infrastructure, CI/CD, cloud operations, and environment management:
- **argocd-cli** — GitOps deployments with ArgoCD
- **aws-api-billing-service-onboarding** — AWS billing/quota monitoring integration
- **aws-cli** — AWS service management via CLI
- **aws-cost-explorer** — AWS cost and usage analysis
- **aws-support-case** — AWS Support case management (bilingual)
- **cloudflare-deploy** — Deploy to Cloudflare Workers/Pages
- **github-cli** — GitHub operations via `gh` CLI
- **gitlab-cli** — GitLab operations via `glab` CLI
- **kargo-cli** — Progressive delivery with Kargo
- **kubectl-cli** — Kubernetes cluster operations
- **release-skills** — Universal release workflow (Node.js, Python, Rust, etc.)
- **simplex-cli** — Simplex Router admin CLI
- **sync-ci-to-staging** — Sync CI configs to staging
- **sync-ci-to-staging-prod** — Sync CI configs to staging and production
- **sync-env** — Sync CI environment configs with safety gates
- **sync-to-prod** — Promote staging configuration to production

### Lenny Skills (119 skills)
Skill packs from [Refound AI](https://refoundai.com/lenny-skills/) covering product, leadership, marketing, sales, career, and more.

#### Direct Skills (20 skills)
AI strategy, career, communication, and cross-cutting topics:
- **ai-evals** — AI evaluation plans with benchmarks and rubrics
- **ai-evaluation-evals** — AI evaluation workflows
- **ai-product-strategy** — AI product strategy packs
- **building-a-promotion-case** — Promotion case and packet preparation
- **career-transitions** — Career pivot planning and execution
- **changelog-generator** — Git-based changelog generation
- **conducting-interviews** — Structured behavioral interview execution
- **continuous-learning** — Extract reusable patterns from sessions
- **continuous-learning-v2** — Instinct-based learning system with confidence scoring
- **docs-update** — Update docs when code changes
- **evaluating-candidates** — Evidence-based hiring decisions
- **finding-mentors-and-sponsors** — Mentor/sponsor network building
- **finding-mentors-sponsors** — Mentor & sponsor plan pack
- **fundraising** — Early-stage fundraising process
- **giving-presentations** — Presentation planning and delivery
- **managing-imposter-syndrome** — Imposter syndrome management
- **negotiating-offers** — Job offer negotiation
- **onboarding-new-hires** — New hire onboarding design
- **personal-productivity** — Personal productivity system
- **writing-job-descriptions** — Outcome-based job descriptions

#### Leadership Skills (29 skills)
Team management, decision processes, and organizational design:
- **building-team-culture**, **coaching-pms**, **collect-incomplete-tasks**
- **cross-functional-collaboration**, **delegating-work**, **designing-team-rituals**
- **energy-management**, **engineering-culture**, **evaluating-trade-offs**
- **having-difficult-conversations**, **managing-timelines**, **managing-up**
- **organizational-design**, **organizational-transformation**
- **planning-under-uncertainty**, **post-mortems-and-retrospectives**
- **post-mortems-retrospectives**, **running-decision-processes**
- **running-design-reviews**, **running-effective-1-1s**, **running-effective-11s**
- **running-effective-meetings**, **running-offsites**
- **setting-okrs-and-goals**, **setting-okrs-goals**
- **stakeholder-alignment**, **strategic-compact**, **systems-thinking**, **team-rituals**

#### Marketing Skills (25 skills)
SEO, content, brand, community, launch marketing, and media creation:
- **audit-website**, **baoyu-article-illustrator**, **baoyu-comic**
- **baoyu-compress-image**, **baoyu-cover-image**, **baoyu-danger-gemini-web**
- **baoyu-danger-x-to-markdown**, **baoyu-format-markdown**, **baoyu-image-gen**
- **baoyu-infographic**, **baoyu-markdown-to-html**, **baoyu-post-to-wechat**
- **baoyu-post-to-x**, **baoyu-slide-deck**, **baoyu-url-to-markdown**
- **baoyu-xhs-images**, **brand-storytelling**, **community-building**
- **content-marketing**, **launch-marketing**, **marketplace-liquidity**
- **media-relations**, **seo-aeo-audit**, **seo-audit**, **seo-geo**

#### Product Skills (37 skills)
Product discovery, strategy, growth, and execution:
- **analyzing-user-feedback**, **behavioral-product-design**
- **coaching-product-managers**, **competitive-analysis**
- **conducting-user-interviews**, **defining-product-vision**
- **designing-growth-loops**, **designing-surveys**
- **developing-product-taste**, **dogfooding**
- **linear-cli**, **marketplace-liquidity-management**
- **measuring-product-market-fit**, **platform-strategy**
- **positioning-and-messaging**, **positioning-messaging**
- **pricing-strategy**, **prioritizing-roadmap**
- **problem-definition**, **product-led-sales**, **product-led-sales-strategy**
- **product-operations**, **product-taste-intuition**
- **research**, **retention-and-engagement**, **retention-engagement**
- **scoping-and-cutting**, **scoping-cutting**
- **shipping-products**, **startup-ideation**, **startup-pivoting**
- **usability-testing**, **user-onboarding**, **working-backwards**
- **writing-north-star-metrics**, **writing-prds**, **writing-specs-designs**

#### Sales Skills (8 skills)
Sales team building, enterprise deals, qualification, and partnerships:
- **building-sales-team**, **enterprise-sales**, **founder-sales**
- **partnership-and-bd**, **partnership-bd**
- **sales-compensation**, **sales-compensation-design**, **sales-qualification**

### Meta Skills (6 skills)
Skills about creating, reviewing, and managing skills:
- **find-skills** — Discover and install agent skills
- **lenny-skillpack-creator** — Convert Lenny skills to skill pack format
- **skill-creator** — Guide for creating new skills
- **skill-review** — Skill quality review
- **skills-readme-updater** — Update README.md from skill metadata
- **sync-skills-manager** — Sync skills between repo and system directories

### Obsidian Skills (6 skills)
Note-taking and knowledge management with Obsidian:
- **excalidraw-diagram** — Generate Excalidraw diagrams from text
- **json-canvas** — Create and edit JSON Canvas files
- **mdbase** — Manage markdown-as-database collections
- **obsidian-bases** — Obsidian Bases (`.base` files) with views and filters
- **obsidian-cli-automation** — Terminal automation for Obsidian vaults
- **obsidian-markdown** — Obsidian Flavored Markdown syntax

### Tools Skills (5 skills)
Automation and tooling helpers:
- **agent-browser** — Browser automation CLI for AI agents
- **justfile** — Justfile creation and management
- **mermaid-visualizer** — Text-to-Mermaid diagram generation
- **notebooklm** — Google NotebookLM automation
- **project-guidelines-example** — Project guidelines template

## Statistics

- **Total Skills**: 158 (unique by directory name)
- **Top-level Categories**: 7 (`base-skills`, `devops-skills`, `lenny-skills`, `meta-skills`, `obsidian-skills`, `tools-skills`, plus `lenny-skills` sub-categories)

## Multi-Agent Global Paths

| Agent | Global path |
|------|-------------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Amp | `~/.config/agents/skills/` |
| Cursor | `~/.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| OpenCode | `~/.config/opencode/skills/` |

Runtime install directory: `~/.claude/skills/` (other agents symlink into it).

```bash
npx skills add . --skill '*' --global \
  --agent claude-code \
  --agent codex \
  --agent amp \
  --agent cursor \
  --agent gemini-cli \
  --agent opencode \
  --yes
```

## Adding New Skills

```bash
npx skills add owner/repo@skill-name -g -y
```

## Justfile

This repository now includes a root [`justfile`](justfile) for the common day-to-day workflows.

Install `just`:

```bash
brew install just
```

Common commands:

```bash
just help
just test-sync
just validate-skill obsidian-skills/obsidian-bases
just obsidian-import
just obsidian-export
just obsidian-sync
just sync-status
just sync-diff
```

`just validate-skill` and `just validate-skillpack` require `PyYAML` because they wrap the repository validator scripts.

Override the default Obsidian vault path when needed:

```bash
OBSIDIAN_VAULT=/path/to/vault just obsidian-sync
```

## License

Skills are sourced from various providers:
- **Lenny Skills**: From [Refound AI](https://refoundai.com/lenny-skills/)
- **Custom Skills**: Created for this repository
- **Community Skills**: From the Claude Code community

---

**Last Updated**: 2026-03-05
**Total Skills**: 158
