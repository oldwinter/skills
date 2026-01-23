# Skills Repository

A comprehensive collection of skills for Claude Code, organized by category.

## 📂 Directory Structure

```
skills/
├── coding-common-skills/    # General coding and development skills (6 skills)
├── devops-skills/           # DevOps and infrastructure skills (12 skills)
├── lenny-skills/            # Product management & leadership skills (90 skills)
├── obsidian-skills/         # Obsidian note-taking skills (5 skills)
├── writing-skills/          # Writing and content skills (1 skill)
├── _archive/                # Archived/temporary files
└── README.md                # This file
```

## 📚 Skills by Category

### 🖥️ Coding Common Skills (6 skills)
General development tools and best practices:
- **changelog-generator** - Automatically create changelogs from git commits
- **justfile** - Command automation with Just
- **skill-creator** - Create new skills for Claude Code
- **skills-readme-updater** - Auto-update skills documentation
- **vercel-react-best-practices** - React/Next.js performance optimization
- **web-design-guidelines** - UI/UX best practices and accessibility

### ⚙️ DevOps Skills (12 skills)
Infrastructure, CI/CD, and cloud operations:
- **api-billing-service-onboarding** - AWS billing/quota monitoring integration
- **argocd-cli** - GitOps deployments with ArgoCD
- **aws-cli** - AWS service management
- **aws-cost-explorer** - AWS cost analysis
- **aws-support-case** - AWS Support case management (NEW)
- **eks-user-rbac** - EKS user RBAC management (NEW)
- **eksctl** - AWS EKS cluster management
- **github-cli** - GitHub operations via CLI
- **gitlab-cli** - GitLab operations via CLI
- **kargo-cli** - Progressive delivery with Kargo
- **kubectl** - Kubernetes cluster operations
- **sync-to-prod** - Environment synchronization

### 🎯 Lenny Skills (90 skills)
Product management and leadership skills from [Lenny's Newsletter](https://refoundai.com/lenny-skills/):

#### Product Management (22 skills)
Writing North Star Metrics, Defining Product Vision, Prioritizing Roadmap, Setting OKRs & Goals, Competitive Analysis, Writing PRDs, Problem Definition, Writing Specs & Designs, Scoping & Cutting, Working Backwards, Conducting User Interviews, Designing Surveys, Analyzing User Feedback, Usability Testing, Shipping Products, Managing Timelines, Developing Product Taste, Product Operations, Behavioral Product Design, Startup Ideation, Dogfooding, Startup Pivoting

#### Leadership (14 skills)
Running Effective 1:1s, Having Difficult Conversations, Delegating Work, Managing Up, Running Decision Processes, Planning Under Uncertainty, Evaluating Trade-offs, Post-mortems & Retrospectives, Cross-functional Collaboration, Systems Thinking, Energy Management, Coaching Product Managers, Organizational Design, Organizational Transformation

#### Hiring & Teams (6 skills)
Writing Job Descriptions, Conducting Interviews, Evaluating Candidates, Onboarding New Hires, Building Team Culture, Designing Team Rituals

#### AI & Technology (6 skills)
AI Product Strategy, Building with LLMs, Evaluating New Technology, Platform Strategy, Vibe Coding, AI Evaluation (Evals)

#### Communication (5 skills)
Giving Presentations, Written Communication, Stakeholder Alignment, Running Offsites, Running Effective Meetings

#### Growth (6 skills)
Measuring Product-Market Fit, Designing Growth Loops, Pricing Strategy, Retention & Engagement, Marketplace Liquidity Management, User Onboarding

#### Marketing (6 skills)
Positioning & Messaging, Brand Storytelling, Launch Marketing, Content Marketing, Community Building, Media Relations

#### Career (7 skills)
Building a Promotion Case, Negotiating Offers, Finding Mentors & Sponsors, Career Transitions, Managing Imposter Syndrome, Personal Productivity, Fundraising Strategy

#### Sales & GTM (7 skills)
Founder Sales, Building Sales Team, Enterprise Sales, Partnership & BD, Product-Led Sales Strategy, Sales Compensation Design, Sales Qualification

#### Engineering (5 skills)
Technical Roadmaps, Managing Tech Debt, Platform & Infrastructure, Engineering Culture, Design Engineering

#### Design (2 skills)
Design Systems, Running Design Reviews

[View all Lenny Skills →](./lenny-skills/README.md)

### 📝 Obsidian Skills (5 skills)
Note-taking and knowledge management:
- **json-canvas** - Work with Obsidian Canvas files
- **obsidian-bases** - Obsidian fundamentals
- **obsidian-dashboard** - Vault statistics and overview
- **obsidian-markdown** - Advanced markdown features
- **tasknotes** - Task management integrated with Obsidian (NEW)

### ✍️ Writing Skills (1 skill)
Content creation and refinement:
- **humanizer-zh** - Remove AI-generated patterns from Chinese text

## 📊 Statistics

- **Total Skills**: 114
- **Categories**: 5 main categories
- **Lenny Skills**: 90 product management & leadership skills
- **DevOps Tools**: 12 infrastructure and cloud skills
- **Development Tools**: 6 coding and best practice skills
- **Obsidian Skills**: 5 note-taking and knowledge management skills

## 🚀 Usage

All skills are installed in `~/.claude/skills/` and can be used directly with Claude Code.

To use a skill, reference it in your conversation with Claude Code, for example:
- "Use the changelog-generator skill to create a changelog"
- "Help me with writing-north-star-metrics"
- "Run kubectl to check pod status"

## 🔄 Maintenance

This repository is synchronized with the local `~/.claude/skills/` directory. Any changes made here will be reflected in your Claude Code installation.

## 📄 License

Skills are sourced from various providers:
- **Lenny Skills**: From [Refound AI](https://refoundai.com/lenny-skills/)
- **Custom Skills**: Created for this repository
- **Community Skills**: From the Claude Code community

---

**Last Updated**: 2026-01-23
**Total Skills**: 114
