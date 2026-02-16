# Skills Repository

A comprehensive collection of skills for Claude Code, organized by category.

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

**On a new computer, run these 3 commands to install all skills:**

```bash
# 1. Clone this repository
git clone https://github.com/oldwinter/skills.git ~/code/skills
cd ~/code/skills

# 2. Install npx add-skill (if not already installed)
npm install -g add-skill

# 3. Install ALL skills to system (for all AI agents)
npx add-skill . --all --global
```

That's it! All 116+ skills will be installed to `~/.agents/skills/` and available to Claude Code, Cline, Cursor, and other AI agents.

---

## Directory Structure

```
skills/
├── coding-common-skills/    # General coding and development skills (6 skills)
├── devops-skills/           # DevOps and infrastructure skills (12 skills)
├── obsidian-skills/         # Obsidian note-taking skills (5 skills)
├── system-skills/           # System-wide skills synced from ~/.agents/skills (116 skills)
├── writing-skills/          # Writing and content skills (1 skill)
├── _archive/                # Archived/temporary files
└── README.md                # This file
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

### DevOps Skills (12 skills)
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

### Obsidian Skills (5 skills)
Note-taking and knowledge management:
- **json-canvas** - Work with Obsidian Canvas files
- **obsidian-bases** - Obsidian fundamentals
- **obsidian-dashboard** - Vault statistics and overview
- **obsidian-markdown** - Advanced markdown features
- **tasknotes** - Task management integrated with Obsidian

### Writing Skills (1 skill)
Content creation and refinement:
- **humanizer-zh** - Remove AI-generated patterns from Chinese text

### System Skills (116 skills)
Skills synced from `~/.agents/skills/`, organized into categories:

#### AI Skills (4 skills)
- **ai-evals** - AI evaluation and benchmarking
- **ai-product-strategy** - AI product planning
- **building-with-llms** - LLM integration patterns
- **vibe-coding** - AI-assisted coding practices

#### Product Skills (28 skills)
- **analyzing-user-feedback**, **behavioral-product-design**, **competitive-analysis**
- **conducting-user-interviews**, **defining-product-vision**, **designing-growth-loops**
- **designing-surveys**, **dogfooding**, **measuring-product-market-fit**
- **platform-strategy**, **positioning-messaging**, **pricing-strategy**
- **prioritizing-roadmap**, **problem-definition**, **product-led-sales**
- **product-operations**, **product-taste-intuition**, **retention-engagement**
- **scoping-cutting**, **shipping-products**, **startup-ideation**
- **startup-pivoting**, **usability-testing**, **user-onboarding**
- **working-backwards**, **writing-north-star-metrics**, **writing-prds**
- **writing-specs-designs**

#### Leadership Skills (23 skills)
- **building-team-culture**, **coaching-pms**, **cross-functional-collaboration**
- **delegating-work**, **energy-management**, **engineering-culture**
- **evaluating-trade-offs**, **having-difficult-conversations**
- **managing-timelines**, **managing-up**, **organizational-design**
- **organizational-transformation**, **planning-under-uncertainty**
- **post-mortems-retrospectives**, **running-decision-processes**
- **running-design-reviews**, **running-effective-1-1s**, **running-effective-meetings**
- **running-offsites**, **setting-okrs-goals**, **stakeholder-alignment**
- **systems-thinking**, **team-rituals**

#### Career Skills (10 skills)
- **building-a-promotion-case**, **career-transitions**, **conducting-interviews**
- **evaluating-candidates**, **finding-mentors-sponsors**, **managing-imposter-syndrome**
- **negotiating-offers**, **onboarding-new-hires**, **personal-productivity**
- **writing-job-descriptions**

#### Communication Skills (3 skills)
- **fundraising**, **giving-presentations**, **written-communication**

#### Marketing Skills (8 skills)
- **audit-website**, **brand-storytelling**, **community-building**
- **content-marketing**, **launch-marketing**, **media-relations**
- **marketplace-liquidity**, **seo-audit**

#### Sales Skills (6 skills)
- **building-sales-team**, **enterprise-sales**, **founder-sales**
- **partnership-bd**, **sales-compensation**, **sales-qualification**

#### Engineering Skills (6 skills)
- **design-engineering**, **design-systems**, **evaluating-new-technology**
- **managing-tech-debt**, **platform-infrastructure**, **technical-roadmaps**

#### Tools Skills (14 skills)
- **agent-browser**, **changelog-generator**, **justfile**
- **lenny-skillpack-creator**, **remotion-best-practices**
- **skill-creator**, **skills-readme-updater**, **supabase-postgres-best-practices**
- **sync-skills-manager**, **sync-to-prod**, **ui-ux-pro-max**
- **vercel-react-best-practices**, **web-design-guidelines**

#### Obsidian Skills (6 skills)
- **json-canvas**, **notebooklm**, **obsidian-bases**
- **obsidian-dashboard**, **obsidian-markdown**, **tasknotes**

## Statistics

- **Total Skills**: 116+
- **Categories**: 6 main categories
- **System Skills**: 116 skills in 11 subcategories
- **DevOps Tools**: 12 infrastructure and cloud skills
- **Development Tools**: 6 coding and best practice skills
- **Obsidian Skills**: 5 note-taking and knowledge management skills

## Usage

All skills are installed in `~/.agents/skills/` and can be used directly with Claude Code.

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
npx add-skill . --all --global

# Or use the helper script
./system-skills/sync-skills-manager/sync-skills.sh push
```

## Adding New Skills

```bash
# Install a skill from GitHub
npx add-skill owner/repo/skill-name --global --yes

# Sync it to this repository
./system-skills/sync-skills-manager/sync-skills.sh pull

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

**Last Updated**: 2026-01-27
**Total Skills**: 116+
