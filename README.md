# Skills Repository

A comprehensive collection of skills for multiple AI agents (Codex, Claude Code, Cursor, etc.), organized by category.

---

## Canonical Edit Path

To avoid duplicate edits and sync drift:

- Treat `system-skills/` as the canonical source for synchronized/global skills.
- Treat `coding-common-skills/`, `devops-skills/`, `obsidian-skills/`, `writing-skills/` as curated collections and compatibility copies.
- Before large sync operations, run `./sync-skills-3way.sh status`.

Related docs:
- Sources and provenance: `SKILLS_SOURCES_README.md`
- Directory consolidation strategy: `DIRECTORY_STRATEGY_README.md`

## Quick Install (New Machine)

**On a new computer, run these commands to install skills:**

```bash
# 1. Clone this repository
git clone https://github.com/oldwinter/skills.git ~/Code/skills
cd ~/Code/skills

# 2. Run the 3-way incremental sync (recommended)
./sync-skills-3way.sh sync

# 3. (Optional) Symlink the canonical skills dir into other agents (recommended)
npx skills add ~/.agents/skills --global --skill '*' \
  --agent claude-code \
  --agent codex \
  --agent amp \
  --agent cursor \
  --agent antigravity \
  --agent droid \
  --agent gemini-cli \
  --agent opencode \
  --yes
```

That's it! All skills will be available from the canonical directory `~/.agents/skills/`.

---

## Directory Structure

```
skills/
├── AGENTS.md
├── README.md
├── SYNC_README.md
├── SKILLS_SOURCES_README.md
├── DIRECTORY_STRATEGY_README.md
├── sync-skills.sh
├── sync-skills-3way.sh
├── coding-common-skills/    # General coding and development skills (6 skills)
├── devops-skills/           # DevOps and infrastructure skills (11 skills)
├── obsidian-skills/         # Obsidian note-taking skills (6 skills)
├── system-skills/           # System-wide skills synced from ~/.agents/skills (189 skills)
└── writing-skills/          # Writing and content skills (1 skill)
```

## Skills by Category

### Coding Common Skills (6 skills)
General development tools and best practices:
- **changelog-generator** - Automatically create changelogs from git commits
- **justfile** - Command automation with Just
- **skill-creator** - Create new skills for Claude Code
- **skills-readme-updater** - Auto-update skills documentation
- **vercel-react-best-practices** - React/Next.js performance optimization
- **web-design-guidelines** - UI/UX best practices and accessibility

### DevOps Skills (11 skills)
Infrastructure, CI/CD, and cloud operations:
- **api-billing-service-onboarding** - AWS billing/quota monitoring integration
- **argocd-cli** - GitOps deployments with ArgoCD
- **aws-cli** - AWS service management
- **aws-cost-explorer** - AWS cost analysis
- **aws-support-case** - AWS Support case management
- **eksctl** - AWS EKS cluster management
- **github-cli** - GitHub operations via CLI
- **gitlab-cli** - GitLab operations via CLI
- **kargo-cli** - Progressive delivery with Kargo
- **kubectl** - Kubernetes cluster operations
- **sync-to-prod** - Environment synchronization

### Obsidian Skills (6 skills)
Note-taking and knowledge management:
- **json-canvas** - Work with Obsidian Canvas files
- **obsidian-bases** - Obsidian fundamentals
- **obsidian-cli-automation** - Terminal automation for Obsidian
- **obsidian-dashboard** - Vault statistics and overview
- **obsidian-markdown** - Advanced markdown features
- **tasknotes** - Task management integrated with Obsidian

### Writing Skills (1 skill)
Content creation and refinement:
- **humanizer-zh** - Remove AI-generated patterns from Chinese text

### System Skills (189 skills)
Skills synced from `~/.agents/skills/`, organized into categories:

#### AI Skills (7 skills)
- **ai-evals**, **ai-evaluation-evals**, **ai-product-strategy**
- **building-with-llms**, **fundraising-strategy**, **mermaid-visualizer**
- **vibe-coding**

#### Product Skills (31 skills)
- **analyzing-user-feedback**, **behavioral-product-design**, **coaching-product-managers**
- **competitive-analysis**, **conducting-user-interviews**, **defining-product-vision**
- **designing-growth-loops**, **designing-surveys**, **developing-product-taste**
- **dogfooding**, **measuring-product-market-fit**, **platform-strategy**
- **positioning-messaging**, **pricing-strategy**, **prioritizing-roadmap**
- **problem-definition**, **product-led-sales**, **product-led-sales-strategy**
- **product-operations**, **product-taste-intuition**, **retention-engagement**
- **scoping-cutting**, **shipping-products**, **startup-ideation**
- **startup-pivoting**, **usability-testing**, **user-onboarding**
- **working-backwards**, **writing-north-star-metrics**, **writing-prds**
- **writing-specs-designs**

#### Leadership Skills (23 skills)
- **building-team-culture**, **coaching-pms**, **cross-functional-collaboration**
- **delegating-work**, **energy-management**, **engineering-culture**
- **evaluating-trade-offs**, **having-difficult-conversations**, **managing-timelines**
- **managing-up**, **organizational-design**, **organizational-transformation**
- **planning-under-uncertainty**, **post-mortems-retrospectives**, **running-decision-processes**
- **running-design-reviews**, **running-effective-1-1s**, **running-effective-meetings**
- **running-offsites**, **setting-okrs-goals**, **stakeholder-alignment**
- **systems-thinking**, **team-rituals**

#### Career Skills (11 skills)
- **building-a-promotion-case**, **career-transitions**, **conducting-interviews**
- **evaluating-candidates**, **finding-mentors-and-sponsors**, **finding-mentors-sponsors**
- **managing-imposter-syndrome**, **negotiating-offers**, **onboarding-new-hires**
- **personal-productivity**, **writing-job-descriptions**

#### Communication Skills (4 skills)
- **fundraising**, **giving-presentations**, **writing-specs-and-designs**
- **written-communication**

#### Marketing Skills (8 skills)
- **audit-website**, **brand-storytelling**, **community-building**
- **content-marketing**, **launch-marketing**, **marketplace-liquidity**
- **media-relations**, **seo-audit**

#### Sales Skills (8 skills)
- **building-sales-team**, **enterprise-sales**, **founder-sales**
- **partnership-and-bd**, **partnership-bd**, **sales-compensation**
- **sales-compensation-design**, **sales-qualification**

#### Engineering Skills (7 skills)
- **design-engineering**, **design-systems**, **evaluating-new-technology**
- **managing-tech-debt**, **platform-and-infrastructure**, **platform-infrastructure**
- **technical-roadmaps**

#### DevOps Skills (11 skills)
- **api-billing-service-onboarding**, **argocd-cli**, **aws-cli**
- **aws-cost-explorer**, **aws-support-case**, **eksctl**
- **github-cli**, **gitlab-cli**, **kargo-cli**
- **kubectl**, **sync-to-prod**

#### Tools Skills (71 skills)
- **agent-browser**, **baoyu-article-illustrator**, **baoyu-comic**
- **baoyu-compress-image**, **baoyu-cover-image**, **baoyu-danger-gemini-web**
- **baoyu-danger-x-to-markdown**, **baoyu-format-markdown**, **baoyu-image-gen**
- **baoyu-infographic**, **baoyu-markdown-to-html**, **baoyu-post-to-wechat**
- **baoyu-post-to-x**, **baoyu-slide-deck**, **baoyu-url-to-markdown**
- **baoyu-xhs-images**, **changelog-generator**, **ci-fix**
- **cloudflare-deploy**, **context7**, **create-pull-request**
- **designing-team-rituals**, **docker-kubectl-deploy**, **docs-update**
- **documentation-lookup**, **e2e-test-automation**, **excalidraw-diagram**
- **find-skills**, **firecrawl**, **gh-fix-ci**
- **github-bug-report-triage**, **github-issue-dedupe**, **humanizer**
- **justfile**, **lenny-skillpack-creator**, **linear**
- **linear-cli**, **marketplace-liquidity-management**, **mcp-builder**
- **openai-docs**, **pearcleaner-cli**, **playwright**
- **positioning-and-messaging**, **post-mortems-and-retrospectives**, **postgres**
- **release-skills**, **remotion-best-practices**, **research**
- **retention-and-engagement**, **running-effective-11s**, **scheduler**
- **scoping-and-cutting**, **seo-aeo-audit**, **seo-geo**
- **setting-okrs-and-goals**, **skill-creator**, **skill-installer**
- **skills-readme-updater**, **slack-qa-investigate**, **simplex-cli-admin**, **supabase-postgres-best-practices**
- **sync-ci-to-staging**, **sync-ci-to-staging-prod**, **terraform-style-check**
- **ui-ux-pro-max**, **vercel-deploy**, **vercel-react-best-practices**
- **web-accessibility-audit**, **web-design-guidelines**, **web-performance-audit**
- **webapp-testing**

#### Obsidian Skills (7 skills)
- **json-canvas**, **notebooklm**, **obsidian-bases**
- **obsidian-cli-automation**, **obsidian-dashboard**, **obsidian-markdown**
- **tasknotes**

#### Sync Tooling (1 skill)
- **sync-skills-manager**

## Statistics

- **Unique Skills**: 190 (by skill identifier / directory name)
- **System Skills**: 189 skills in 11 subcategories + sync tooling
- **Curated Folders**: 24 skills (includes intentional duplicates)
- **Top-level Categories**: 5 skill folders

## Usage

Canonical install directory: `~/.agents/skills/` (other agents can symlink into it).

To use a skill, reference it in your conversation with Claude Code, for example:
- "Use the changelog-generator skill to create a changelog"
- "Help me with writing-north-star-metrics"
- "Run kubectl to check pod status"

## Sync Commands

```bash
# 3-way incremental sync (recommended)
./sync-skills-3way.sh sync
# (equivalent)
./system-skills/sync-skills-manager/sync-skills-3way.sh sync

# 3-way status
./sync-skills-3way.sh status
# (equivalent)
./system-skills/sync-skills-manager/sync-skills-3way.sh status

# Preview changes
./system-skills/sync-skills-manager/sync-skills.sh diff

# Pull new skills from system to repo (incremental sync)
./system-skills/sync-skills-manager/sync-skills.sh pull

# Push all repo skills to system (for new machine setup)
./sync-skills-3way.sh sync

# Or use the helper script
./system-skills/sync-skills-manager/sync-skills.sh push
```

## Adding New Skills

```bash
# Install a skill from GitHub
npx skills add owner/repo@skill-name -g -y

# Sync it to this repository
./sync-skills-3way.sh sync

# Commit and push
git add -A && git commit -m "Add new skill" && git push
```

## Maintenance

This repository is synchronized with the local `~/.agents/skills/` directory. Any changes made here will be reflected in your Claude Code installation.

## License

Skills are sourced from various providers:
- **Lenny Skills**: From [Refound AI](https://refoundai.com/lenny-skills/)
- **Custom Skills**: Created for this repository
- **Community Skills**: From the Claude Code community

---

**Last Updated**: 2026-02-25
**Unique Skills**: 190
