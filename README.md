# Claude Code Skills

这是我的 Claude Code Skills 集合，用于扩展 Claude 的能力，提供专业领域的工作流和工具集成。

## Skills 列表

### 云基础设施 (Cloud Infrastructure)

| Skill | 描述 |
|-------|------|
| **aws-cli** | This skill should be used when users need to interact with AWS services via CLI |
| **aws-cost-explorer** | This skill should be used when users need to query AWS cost and usage details... |
| **eksctl** | This skill should be used when users need to manage AWS EKS clusters via eksc... |

### Kubernetes & GitOps

| Skill | 描述 |
|-------|------|
| **argocd-cli** | This skill should be used when users need to manage GitOps deployments via Ar... |
| **kargo-cli** | This skill should be used when users need to manage progressive delivery via ... |
| **kubectl** | This skill should be used when users need to interact with Kubernetes cluster... |
| **sync-to-prod** | This skill should be used when users need to sync/promote configuration from ... |

### 代码仓库 (Repository Management)

| Skill | 描述 |
|-------|------|
| **changelog-generator** | Automatically creates user-facing changelogs from git commits by analyzing co... |
| **github-cli** | This skill should be used when users need to interact with GitHub via the gh CLI |
| **gitlab-cli** | This skill should be used when users need to interact with GitLab via the gla... |

### 开发工具 (Development Tools)

| Skill | 描述 |
|-------|------|
| **justfile** | This skill should be used when users want to create, convert, or manage Justf... |
| **skill-creator** | Guide for creating effective skills |
| **skills-readme-updater** | This skill should be used after creating or modifying skills to update the ma... |

### 内容处理 (Content Processing)

| Skill | 描述 |
|-------|------|
| **humanizer-zh** | 去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。 基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的... |
| **obsidian-dashboard** | This skill should be used when users want to generate comprehensive statistic... |

## 目录结构

```
~/.claude/skills/
├── README.md                 # 本文件
├── argocd-cli/
├── aws-cli/
├── aws-cost-explorer/
├── changelog-generator/
├── eksctl/
├── github-cli/
├── gitlab-cli/
├── humanizer-zh/
├── justfile/
├── kargo-cli/
├── kubectl/
├── obsidian-dashboard/
├── skill-creator/
├── skills-readme-updater/
└── sync-to-prod/
```

## 使用方式

Skills 会在对话中根据上下文自动触发，也可以通过 `/skill-name` 手动调用。

## 添加新 Skill

使用 `skill-creator` 来创建新的 skill：

```bash
# 初始化新 skill
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path ~/.claude/skills

# 编辑 SKILL.md 和相关文件

# 验证并打包
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ~/.claude/skills/<skill-name>

# 更新 README
python3 ~/.claude/skills/skills-readme-updater/scripts/update_readme.py
```

---

*最后更新: 2026-01-19*
