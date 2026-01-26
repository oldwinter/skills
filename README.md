# Skills Repository

A comprehensive collection of skills for Claude Code, organized by category.

## Directory Structure

```
skills/
├── coding-common-skills/    # General coding and development skills (6 skills)
├── devops-skills/           # DevOps and infrastructure skills (12 skills)
├── obsidian-skills/         # Obsidian note-taking skills (5 skills)
├── system-skills/           # System-wide skills synced from ~/.agents/skills (102 skills)
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

### System Skills (102 skills)
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

#### Communication Skills (2 skills)
- **fundraising**, **giving-presentations**, **written-communication**

#### Marketing Skills (6 skills)
- **brand-storytelling**, **community-building**, **content-marketing**
- **launch-marketing**, **media-relations**, **marketplace-liquidity**

#### Sales Skills (6 skills)
- **building-sales-team**, **enterprise-sales**, **founder-sales**
- **partnership-bd**, **sales-compensation**, **sales-qualification**

#### Engineering Skills (6 skills)
- **design-engineering**, **design-systems**, **evaluating-new-technology**
- **managing-tech-debt**, **platform-infrastructure**, **technical-roadmaps**

#### Tools Skills (8 skills)
- **lenny-skillpack-creator**, **sync-skills-manager**
- Plus: changelog-generator, justfile, skill-creator, skills-readme-updater
- vercel-react-best-practices, web-design-guidelines

#### Sync Tool
- **sync-skills-manager** - Sync skills between system and repository

## Statistics

- **Total Skills**: 136+
- **Categories**: 6 main categories
- **System Skills**: 102 skills in 11 subcategories
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
# Preview changes
./system-skills/sync-skills-manager/sync-skills.sh diff

# Pull new skills from system to repo
./system-skills/sync-skills-manager/sync-skills.sh pull

# Push all repo skills to system
./system-skills/sync-skills-manager/sync-skills.sh push

# Or use npx add-skill directly
npx add-skill . --all --global
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
**Total Skills**: 136+
