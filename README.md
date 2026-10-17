# oldwinter/skills

我在用的 agent skills，大多是自己写的，少数是改过名的 fork。只收在用的：第三方 skill 直接从上游装，不在这里留副本。

## 装

```bash
npx skills add oldwinter/skills
```

只装某一个：

```bash
npx --yes skills@latest add oldwinter/skills --global --skill done --agent '*' --yes --full-depth
```

## Skills

### Standalone Skills

- **add-just-doctor** — 给仓库加 `just doctor`，检查本地 env 文件和它依赖的服务。
- **agent-autoresearch** — 与 harness 无关的 autoresearch 循环：改、量、留或回退、记录。
- **change-evidence** — 给 UI/UX 和前端改动录屏取证，覆盖复现、改后行为和验收。
- **done** — 收尾一次改动：验证、提交、开并合并 PR/MR、对齐 issue（只在 `$done` / `/done` 时用）。
- **tdd-pstack** — pstack 的 bug 修复 TDD：先写失败的回归测试再修（pstack-claude `tdd` 的改名 fork）。
- **teach-pstack** — pstack 的 teach：借 `how` 和 `why` 把代码讲明白（pstack-claude `teach` 的改名 fork）。

### Obsidian Skills

- **canvas-atlas** — 把代码仓库、笔记或研究材料整理成可逐层阅读的 Obsidian Canvas 知识地图。
- **to-note** — 把内容存成 Obsidian 库里的 Markdown 笔记。

## Statistics

- **Skill directories**: 8
- **Unique names**: 8

## 归档

2026-10-13 起这个仓库只留在用的 skill。整理前的完整快照在 tag [`archive/2026-10-13`](https://github.com/oldwinter/skills/tree/archive/2026-10-13)，里面还有 Lenny、华术、mattpocock、OpenAI 等第三方副本，这些已经删除，要用就从上游装。

下面这些是自己写的或改过的，暂时不用，只存在那个 tag 里：

- [`automation-memory`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/automation-memory) — Resolve and maintain recurring Codex automation memory safely. MUST use whenever prompts include Automation:, 
- [`chendongdong-digital-twin`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/chendongdong-digital-twin) — Evidence-based Chen Dongdong operating perspective for drafting colleague replies, executing work in his prefe
- [`herdr-worktrunk`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/herdr-worktrunk) — Automate task environments with Worktrunk and Herdr: prepare dependencies through project hooks, start and health-check per-worktree dev services, report Git and delivery status.
- [`lark-reimbursement`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/lark-reimbursement) — 采购报销前提醒并核验采购申请已获批准，再根据飞书文档和凭证创建或修正费用报销单，上传附件并回读核验。普通审批处理使用 lark-approval。
- [`oldwinter-mode`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/oldwinter-mode) — oldwinter's agent style. Terse Chinese-first replies, config-level autonomy behind declared gates, fixed orche
- [`planning-with-files-zh`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/planning-with-files-zh) — 基于 Manus 风格的文件规划系统，创建 task_plan.md、findings.md 和 progress.md 跟踪复杂任务进度，支持 /clear 后会话恢复。
- [`windows-storage-audit`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/windows-storage-audit) — Scan Windows disks from their roots, explain physical storage use and cleanup feasibility, then execute scoped
- [`yansu-agent-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/yansu-agent-cli) — Use the bundled Yansu CLI to sync project knowledge/context/skills and run Yansu workflow commands.
- [`browser`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/browser) — This skill should be used for browser automation tasks using Chrome DevTools Protocol (CDP). Triggers when use
- [`supergoal`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/supergoal) — Plan and autonomously build a software task end-to-end. Triggered by `/supergoal`, "plan and ship X", "superch
- [`tools-skills/lev8-multi-case-pressure-test`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/tools-skills/lev8-multi-case-pressure-test) — Run Lev8 multi-case browser pressure tests from CSV or tabular case files. Use when Codex needs to launch mult
- [`tools-skills/justfile`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/tools-skills/justfile) — This skill should be used when users want to create, convert, or manage Justfiles for command automation. It h
- [`obsidian-skills/obsidian-cli-automation`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/obsidian-skills/obsidian-cli-automation) — Use when users need terminal automation for Obsidian, including note and vault operations, daily notes, tasks,
- [`devops-skills/argocd-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/argocd-cli) — This skill should be used when users need to manage GitOps deployments via ArgoCD CLI. It covers application s
- [`devops-skills/aws-api-billing-service-onboarding`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-api-billing-service-onboarding) — This skill should be used when the user requests to add a new third-party API service to the AWS billing/quota
- [`devops-skills/aws-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-cli) — This skill should be used when users need to interact with AWS services via CLI. It covers all AWS services in
- [`devops-skills/aws-cost-explorer`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-cost-explorer) — This skill should be used when users need to query AWS cost and usage details for a specific date. It supports
- [`devops-skills/aws-support-case`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-support-case) — This skill should be used when users need to manage AWS Support cases via CLI. It handles listing cases (recen
- [`devops-skills/github-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/github-cli) — This skill should be used when users need to interact with GitHub via the gh CLI. It covers repository managem
- [`devops-skills/gitlab-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/gitlab-cli) — This skill should be used when users need to interact with GitLab via the glab CLI. It covers repository manag
- [`devops-skills/kargo-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/kargo-cli) — This skill should be used when users need to manage progressive delivery via Kargo CLI. It covers freight mana
- [`devops-skills/kubectl-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/kubectl-cli) — This skill should be used when users need to interact with Kubernetes clusters via kubectl CLI. It covers pod 
- [`devops-skills/simplex-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/simplex-cli) — Use when operating the Simplex Router Admin CLI (`simplex-cli`) or explaining Simplex Router backend terms in 
- [`devops-skills/sync-env`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/sync-env) — Sync CI environment configurations to staging and optionally to production, with safety gates and whitelist-aw
- [`devops-skills/release-skills`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/release-skills) — Universal release workflow. Auto-detects version files and changelogs. Supports Node.js, Python, Rust, Claude 
- [`meta-skills/lenny-skillpack-creator`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/lenny-skillpack-creator) — Converts a Refound/Lenny Skill into a high-density, agent-executable Skill Pack (Agent Skills standard). Outpu
- [`meta-skills/skill-review`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/skill-review) — |
- [`meta-skills/skills-readme-updater`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/skills-readme-updater) — This skill should be used after creating or modifying skills to update the main README.md file. It scans all s
- [`meta-skills/sync-skills-manager`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/sync-skills-manager) — Manage synchronization workflows between repository skills and local system skill directories.

取回一个：

```bash
git checkout archive/2026-10-13 -- <path>
```

## 校验

```bash
just check        # README 列表、frontmatter、私有路径审计 + 脚本夹具测试
just doctor       # 本地工具链健康：python3 / bash / git / just / CLAUDE.md 符号链接
just test-skills  # skill 自带的 unittest 套件（agent-autoresearch、canvas-atlas，约 30s）
```

`doctor` 每行一个检查项，状态为 `PASS` / `WARN` / `FAIL` / `SKIP`；有任何 `FAIL` 时退出码非零。本仓库没有本地环境文件和环境化服务，对应行恒为 `SKIP`。

## License

Skills are written for this repository unless a skill's own `LICENSE` or `NOTICE.md` says otherwise.
