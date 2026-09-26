# oldwinter/skills

散落在 Claude、Codex、Cursor 里的 agent skills，我收到这一处，免得用着用着就丢了。

这不是精选商店。有我自己写的，也有从 [Lenny / Refound](https://refoundai.com/lenny-skills/) 和社区搬来的。我在用，所以我在收。

同类如果也在多 agent 之间对不齐 skills，可以直接装。

## 装

```bash
npx skills add oldwinter/skills
```

只装某一个：

```bash
npx --yes skills@latest add oldwinter/skills --global --skill add-just-doctor --agent '*' --yes --full-depth
```

## 这仓库在干什么

skills 一散，各端各写各的，过两周就对不上。这里是我的唯一源头：仓库、本机 runtime、Obsidian 库三路同步。同步命令在 `general-tasks` 里，这个仓库自己也有 `just sync-status`。

完整目录是手写的两层地图：`*-skills/` 分类桶，加上仓库根上的 standalone skill。`npx skills add` 和 agent 按**目录名**解析。`skills-readme-updater` 扫的是本机 `~/.claude/skills/`，不是这份 README 的生成器。用 `just check-readme-map` 核对树和地图。

## 我是谁

[oldwinter](https://github.com/oldwinter)。白天做云计算，晚上在浇 [数字花园](https://notes.oldwinter.top)。

## Directory Structure

```
skills/
├── AGENTS.md
├── README.md
├── <43 root skill directories>  # standalone install names; list below
├── base-skills/                 # 6
├── devops-skills/               # 13
├── lenny-skills/                # 119
│   ├── leadership-skills/
│   ├── marketing-skills/
│   ├── product-skills/
│   └── sales-skills/
├── meta-skills/                 # 6
├── obsidian-skills/             # 8
└── tools-skills/                # 6
```

分类桶是分类真源。根目录那 43 个目录也是合法 skill 名；六个名字两边都有，根上的副本可能分叉。

## Skills by Category

### Standalone Skills

仓库根上带 `SKILL.md` 的目录（43）。装或改之前先看路径，不要只认分类桶。

- **add-just-doctor** — Add a repository `just doctor` that checks the local env file and service deps.
- **agent-browser** — Browser automation CLI for AI agents.
- **ast-grep** — Structural code search and analysis with ast-grep rules.
- **automation-memory** — Resolve and maintain recurring Codex automation memory.
- **browser** — Browser automation over Chrome DevTools Protocol.
- **browser-harness** — Direct browser control via CDP.
- **caveman** — Ultra-compressed communication mode.
- **change-evidence** — Screen-recorded acceptance evidence for user-facing UI/UX and frontend changes.
- **chendongdong-digital-twin** — Evidence-based Chen Dongdong operating perspective.
- **codex-dynamic-workflows** — Plan and run Codex-native dynamic workflows.
- **computer-use** — Drive local desktop apps through Orca computer-use.
- **darwin-skill** — Autonomous skill optimizer inspired by Karpathy's autoresearch.
- **diagnose** — Disciplined diagnosis loop for hard bugs and performance regressions.
- **excalidraw-diagram** — Generate Excalidraw diagrams from text.
- **find-skills** — Discover and install agent skills.
- **go-live** — 每次改完就部署到公开预览/生产 URL。
- **grill-me** — Interview a plan or design until the decision tree is resolved.
- **grill-with-docs** — Grill a plan against the domain model and update docs.
- **handoff** — Compact the current conversation into a handoff document.
- **herdr-worktrunk** — Prepare Herdr/Worktrunk task environments and verify delivery.
- **huashu-nuwa** — 从人名/主题生成可运行的人物 Skill。
- **improve-codebase-architecture** — Find deepening opportunities from CONTEXT.md and ADRs.
- **loop** — Recurring prompt loop (`$loop` only).
- **mermaid-visualizer** — Turn text into Mermaid diagrams.
- **obsidian-canvas-creator** — Create Obsidian Canvas files from text.
- **oldwinter-mode** — oldwinter's agent style: terse Chinese-first replies, gated autonomy, evidence-first shipping.
- **orca-cli** — Drive a running Orca editor (worktrees, terminals, embedded browser).
- **orchestration** — Multi-agent coordination through Orca orchestration.
- **planning-with-files-zh** — Manus 风格的文件规划（task_plan / findings / progress）。
- **prototype** — Build a throwaway prototype before committing to a design.
- **remotion-best-practices** — Best practices for Remotion video in React.
- **setup-matt-pocock-skills** — Wire engineering skills to this repo's issue tracker.
- **skill-creator** — Guide for creating new skills.
- **skillshare** — Sync AI CLI skills across many tools from one source.
- **supergoal** — Plan and autonomously build a software task end-to-end.
- **tdd** — Test-driven development with a red-green-refactor loop.
- **to-issues** — Break a plan into independently grabbable tracker issues.
- **to-prd** — Turn the current conversation into a PRD on the tracker.
- **triage** — Triage issues through a role-driven state machine.
- **windows-storage-audit** — Scan Windows disks and run authorized cleanup with before/after evidence.
- **write-a-skill** — Create skills with progressive disclosure and bundled resources.
- **yansu-agent-cli** — Sync project knowledge and run Yansu workflow commands.
- **zoom-out** — Zoom out to broader context or a higher-level view.

六个名字同时出现在根目录和分类桶：`agent-browser`、`excalidraw-diagram`、`find-skills`、`mermaid-visualizer`、`remotion-best-practices`、`skill-creator`。分类桶是分类真源；根目录副本可能分叉（`find-skills` 已经和 `meta-skills/find-skills` 分叉）。

### Base Skills (6 skills)
Foundational skills used across many workflows:
- **context7** — Library documentation lookup via Context7 API
- **firecrawl** — Web scraping, search, and crawling (LLM-optimized markdown)
- **humanizer-zh** — Remove AI-generated patterns from Chinese text
- **remotion-best-practices** — Best practices for Remotion video creation in React
- **supabase-postgres-best-practices** — Postgres performance optimization from Supabase
- **ui-ux-pro-max** — UI/UX design intelligence (50 styles, 9 stacks, shadcn/ui)

### DevOps Skills (13 skills)
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
- **sync-env** — Sync CI environment configs with safety gates

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
- **skills-readme-updater** — Intended to refresh skill listings; currently scans `~/.claude/skills/`, not this repo
- **sync-skills-manager** — Sync skills between repo and system directories

### Obsidian Skills (8 skills)
Note-taking and knowledge management with Obsidian:
- [canvas-atlas](obsidian-skills/canvas-atlas/SKILL.md) — Source-backed architecture maps with single-canvas and nested navigation modes
- **excalidraw-diagram** — Generate Excalidraw diagrams from text
- **json-canvas** — Create and edit JSON Canvas files
- **mdbase** — Manage markdown-as-database collections
- **obsidian-bases** — Obsidian Bases (`.base` files) with views and filters
- **obsidian-cli-automation** — Terminal automation for Obsidian vaults
- **obsidian-markdown** — Obsidian Flavored Markdown syntax
- **obsidian-note-capture** — Capture docs, research, and deliverables into oldwinter-notes

### Tools Skills (6 skills)
Automation and tooling helpers:
- **agent-browser** — Browser automation CLI for AI agents
- **justfile** — Justfile creation and management
- **lev8-multi-case-pressure-test** — Lev8 multi-case browser pressure tests from CSV/tabular cases
- **mermaid-visualizer** — Text-to-Mermaid diagram generation
- **notebooklm** — Google NotebookLM automation
- **project-guidelines-example** — Project guidelines template

## Statistics

- **Skill directories**: 201
- **Unique names**: 195
- **Root / standalone**: 43
- **Category buckets**: `base-skills` (6), `devops-skills` (13), `lenny-skills` (119), `meta-skills` (6), `obsidian-skills` (8), `tools-skills` (6)
- **Name collisions**: 6

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


## Canonical Runtime Sync

This repository also acts as the canonical source for operating-system-level global skills mirrored from `~/.agents/skills` and `~/.codex/skills`. The sync state lives in `global-skills-sync-state.json` and stores the last synced content hash for each runtime skill.

Sync is managed from `general-tasks`:

```bash
just global-skills-sync-status
just global-skills-sync-dry-run
just global-skills-sync-apply
```

The sync uses a three-way baseline: single-sided changes are copied to the other side, both-sided divergent changes are reported as conflicts, and missing skills are copied to the missing side. Runtime directories are copied by default; use `link_runtime=1` from `general-tasks` only when you want runtime entries symlinked to this repo.

`chendongdong-digital-twin/` is maintained in this repository as its sole source of truth. Its Codex runtime entry at `~/.codex/skills/chendongdong-digital-twin` must remain a symlink to this directory; edit and validate the repository copy, not the runtime path.

## Adding New Skills

```bash
npx skills add owner/repo@skill-name -g -y
```

Install only `add-just-doctor` globally on a new device:

```bash
npx --yes skills@latest add oldwinter/skills --global --skill add-just-doctor --agent '*' --yes --full-depth
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
just sync-status
just sync-diff
```

`just validate-skill` and `just validate-skillpack` require `PyYAML` because they wrap the repository validator scripts.

Obsidian sidecar import/export is still a plan in `docs/plans/2026-03-08-obsidian-skill-state-sync.md`. There is no `just obsidian-*` recipe until those scripts land in the tree.

## License

Skills are sourced from various providers:
- **Lenny Skills**: From [Refound AI](https://refoundai.com/lenny-skills/)
- **Custom Skills**: Created for this repository
- **Community Skills**: From the Claude Code community

---

**Last Updated**: 2026-09-16
**Skill directories**: 201
**Unique names**: 195