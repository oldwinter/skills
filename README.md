# oldwinter/skills

我在用的 agent skills，大多是自己写的，少数是改过名的 fork。只收在用的：第三方 skill 直接从上游装，不在这里留副本。

## 装

按需安装单个 skill，不要整包安装：这个仓库只收在用的 skill，整包会把互为替代的条目一起装进去。

```bash
npx --yes skills@latest add oldwinter/skills --skill done change-evidence --full-depth
```

`obsidian-skills/` 是嵌套目录，装其中的 skill 必须带 `--full-depth`；要指定 harness 加 `--agent`，要装到全局加 `--global`：

```bash
npx --yes skills@latest add oldwinter/skills --skill to-note vault-moc canvas-atlas --global --agent claude-code --full-depth
```

- `done` 只在显式 `/done` 或 `$done` 时使用；安装后不要去掉它的 `disable-model-invocation: true`。
- `tdd-pstack` / `teach-pstack` 是上游 `tdd` / `teach` 的改名 fork，和同名上游能力二选一，不要同时安装。
- 装完在新会话里确认目标 skills 目录下有该 skill；模型上下文里看不到 `done` 属于预期。

### Loop 套装（唯一要整组装的一组）

`loop-kit` 是底座，另外三个是它驱动的一拍循环，四个必须装在同一个 skills 目录下（它们互相用相对路径引用）。一键装齐：

```bash
npx --yes skills@latest add oldwinter/skills --skill loop-kit loop-triage-github loop-watch-social loop-nightly-review --agent claude-code
```

然后在目标项目里初始化一次（幂等，可重复跑）：

```bash
python3 .claude/skills/loop-kit/scripts/loopkit.py init
python3 .claude/skills/loop-kit/scripts/loopkit.py doctor
```

`init` 从 `git remote` 认出仓库名，要覆盖就加 `--repo owner/name`；它会写 `.loop/config.json`、`LESSONS.md`、验收规则文件、`AGENTS.md` 里的接线块，并在仓库外建状态目录和 Reply Desk。`doctor` 逐行 `PASS`/`WARN`/`FAIL`/`SKIP`，有 `FAIL` 就别急着开定时器。之后每个循环一个会话：

```text
/loop 30m /loop-triage-github
/loop 60m /loop-watch-social
/loop /loop-nightly-review
```

调度器换成别的 harness 也行，见 `loop-kit/references/harnesses.md`（Claude Code `/loop`、DSH 定时任务、cron、systemd、任务计划程序）。

## Skills

每个 skill 二选一，规则和两处标记见 [AGENTS.md](AGENTS.md) 的 **Skill invocation**：

- **自动引用**（model-invoked）——模型可在合适时机自行触发；`SKILL.md` 不写 `disable-model-invocation`，`agents/openai.yaml` 里 `policy.allow_implicit_invocation: true`。
- **手动引用**（user-invoked）——只有你显式 `/name` 或 `$name` 才会跑；`SKILL.md` 写 `disable-model-invocation: true`，`agents/openai.yaml` 里 `policy.allow_implicit_invocation: false`。

### 自动引用（模型可自行触发）

- **agent-harness-repair** — 诊断并修复本机 coding-agent CLI/harness 安装：自更新、npm/pnpm 鉴权、hook、PATH、MCP、配置解析。
- **change-evidence** — 给 UI/UX 和前端改动录屏取证，覆盖复现、改后行为和验收。
- **longform-fiction** — 长篇小说规划、起草与扩写：故事圣经、章节合同、并行写手、连续性合并、字数验收门。
- **tdd-pstack** — pstack 的 bug 修复 TDD：先写失败的回归测试再修（pstack-claude `tdd` 的改名 fork；与上游 `tdd` 二选一安装）。
- **teach-pstack** — pstack 的 teach：借 `how` 和 `why` 把代码讲明白（pstack-claude `teach` 的改名 fork；与上游 `teach` 二选一安装）。
- **windows-leftover-cleanup** — 清理已卸载软件或已消失磁盘留下的 Windows 残留：卸载项、Steam 库配置、防火墙规则、服务注册、文件关联、路径缓存和空目录。
- **canvas-atlas** — 把代码仓库、笔记或研究材料整理成可逐层阅读的 Obsidian Canvas 知识地图。
- **to-note** — 把内容存成 Obsidian 库里的 Markdown 笔记。
- **vault-moc** — 在已有 Obsidian 库中生成或刷新 MOC 索引笔记，用真实 wikilink/backlink 取证。

### 手动引用（只在显式 `/name` 或 `$name` 时触发）

- **done** — 收尾一次改动：验证、提交、开并合并 PR/MR、对齐 issue（只在 `$done` / `/done` 时用）。
- **add-just-doctor** — 给仓库加 `just doctor`，检查本地 env 文件和它依赖的服务。
- **agent-autoresearch** — 与 harness 无关的 autoresearch 循环：改、量、留或回退、记录。
- **loop-kit** — 维护循环的公共底座：写 `.loop/config.json`、生成 `LESSONS.md` 与验收规则模板、接线 `AGENTS.md`，带 Reply Desk（对外动作的人工审批闸门）、`doctor` 自检和 tick 锁。装 loop 套装的第一个入口。
- **loop-triage-github** — GitHub 维护循环的一拍：只读自己的 PR，先复现、先写会失败的测试再修，跟到 CI/评审/合并，所有对外动作先落 Reply Desk 等批准；附事件监听脚本 `watch-prs.py`。
- **loop-watch-social** — 社区反馈循环的一拍：X/Discord/Reddit 先收集，用小模型过滤后再进主会话，修复真正上线后才回帖；对外回复同样走 Reply Desk。
- **loop-nightly-review** — 复盘循环的一拍：每晚看合并进 main 的提交，把踩过的坑写进 `LESSONS.md`，同一教训在 3 个不同日子出现就升级成硬规则，并顺手开一次清理 PR。

## Statistics

- **Skill directories**: 16
- **Unique names**: 16

## 归档

2026-10-13 起这个仓库只留在用的 skill。整理前的完整快照在 tag [`archive/2026-10-13`](https://github.com/oldwinter/skills/tree/archive/2026-10-13)，里面还有 Lenny、华术、mattpocock、OpenAI 等第三方副本，这些已经删除，要用就从上游装。

下面这些是自己写的或改过的，暂时不用，只存在那个 tag 里：

- [`automation-memory`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/automation-memory) — Resolve and maintain recurring Codex automation memory safely.
- [`chendongdong-digital-twin`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/chendongdong-digital-twin) — Evidence-based Chen Dongdong operating perspective for drafting colleague replies, executing work in his preferred workflow…
- [`herdr-worktrunk`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/herdr-worktrunk) — Automate task environments with Worktrunk and Herdr: prepare dependencies through project hooks, start and health-check…
- [`lark-reimbursement`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/lark-reimbursement) — 采购报销前提醒并核验采购申请已获批准，再根据飞书文档和凭证创建或修正费用报销单，上传附件并回读核验。普通审批处理使用 lark-approval。
- [`oldwinter-mode`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/oldwinter-mode) — oldwinter's agent style.
- [`planning-with-files-zh`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/planning-with-files-zh) — 基于 Manus 风格的文件规划系统，用于组织和跟踪复杂任务的进度。创建 task_plan.md、findings.md 和 progress.md 三个文件。当用户要求规划、拆解或组织多步骤项目、研究任务或需要超过5次工具调用的工作时使用。支持…
- [`windows-storage-audit`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/windows-storage-audit) — Scan Windows disks from their roots, explain physical storage use and cleanup feasibility, then execute scoped cleanup with…
- [`yansu-agent-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/yansu-agent-cli) — Use the bundled Yansu CLI to sync project knowledge/context/skills and run Yansu workflow commands.
- [`browser`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/browser) — This skill should be used for browser automation tasks using Chrome DevTools Protocol (CDP).
- [`supergoal`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/supergoal) — Plan and autonomously build a software task end-to-end.
- [`tools-skills/lev8-multi-case-pressure-test`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/tools-skills/lev8-multi-case-pressure-test) — Run Lev8 multi-case browser pressure tests from CSV or tabular case files.
- [`tools-skills/justfile`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/tools-skills/justfile) — This skill should be used when users want to create, convert, or manage Justfiles for command automation.
- [`obsidian-skills/obsidian-cli-automation`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/obsidian-skills/obsidian-cli-automation) — Use when users need terminal automation for Obsidian, including note and vault operations, daily notes, tasks, properties…
- [`devops-skills/argocd-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/argocd-cli) — This skill should be used when users need to manage GitOps deployments via ArgoCD CLI.
- [`devops-skills/aws-api-billing-service-onboarding`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-api-billing-service-onboarding) — This skill should be used when the user requests to add a new third-party API service to the AWS billing/quota monitoring system.
- [`devops-skills/aws-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-cli) — This skill should be used when users need to interact with AWS services via CLI.
- [`devops-skills/aws-cost-explorer`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-cost-explorer) — This skill should be used when users need to query AWS cost and usage details for a specific date.
- [`devops-skills/aws-support-case`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/aws-support-case) — This skill should be used when users need to manage AWS Support cases via CLI.
- [`devops-skills/github-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/github-cli) — This skill should be used when users need to interact with GitHub via the gh CLI.
- [`devops-skills/gitlab-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/gitlab-cli) — This skill should be used when users need to interact with GitLab via the glab CLI.
- [`devops-skills/kargo-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/kargo-cli) — This skill should be used when users need to manage progressive delivery via Kargo CLI.
- [`devops-skills/kubectl-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/kubectl-cli) — This skill should be used when users need to interact with Kubernetes clusters via kubectl CLI.
- [`devops-skills/simplex-cli`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/simplex-cli) — Use when operating the Simplex Router Admin CLI (`simplex-cli`) or explaining Simplex Router backend terms in Chinese (邀请码/invite…
- [`devops-skills/sync-env`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/sync-env) — Sync CI environment configurations to staging and optionally to production, with safety gates and whitelist-aware diffing.
- [`devops-skills/release-skills`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/devops-skills/release-skills) — Universal release workflow.
- [`meta-skills/lenny-skillpack-creator`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/lenny-skillpack-creator) — Converts a Refound/Lenny Skill into a high-density, agent-executable Skill Pack (Agent Skills standard).
- [`meta-skills/skill-review`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/skill-review) — Skills retrospective and improvement.
- [`meta-skills/skills-readme-updater`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/skills-readme-updater) — This skill should be used after creating or modifying skills to update the main README.md file.
- [`meta-skills/sync-skills-manager`](https://github.com/oldwinter/skills/tree/archive/2026-10-13/meta-skills/sync-skills-manager) — Manage synchronization workflows between repository skills and local system skill directories.

取回一个：

```bash
git checkout archive/2026-10-13 -- <path>
```

## 校验

```bash
just check        # README 列表、frontmatter/描述/相对链接/openai.yaml/个人路径审计 + 脚本夹具测试
just doctor       # 本地工具链健康：python3 / bash / git / just / CLAUDE.md 符号链接
just test-skills  # skill 自带的 unittest 套件（agent-autoresearch、canvas-atlas、longform-fiction、loop-kit、loop-triage-github）
```

`doctor` 每行一个检查项，状态为 `PASS` / `WARN` / `FAIL` / `SKIP`；有任何 `FAIL` 时退出码非零。`bash` 行会显示实际解析到的路径：Windows 上跑 `scripts/test-*` 用 Git Bash，WSL 的 `bash` 不共享文件系统。本仓库没有本地环境文件和环境化服务，对应行恒为 `SKIP`。

## License

[MIT](LICENSE). Skills are written for this repository unless a skill's own `LICENSE` or `NOTICE.md` says otherwise — the `tdd-pstack` and `teach-pstack` forks carry their own upstream MIT license and attribution.
