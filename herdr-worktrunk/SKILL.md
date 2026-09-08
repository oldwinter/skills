---
name: herdr-worktrunk
description: "Automate task environments with Worktrunk and Herdr: prepare dependencies through project hooks, start and health-check per-worktree dev services, resume agents, and report Git plus delivery status. Use for herdr-worktrunk, Worktrunk/Herdr integration, or opening a ready-to-work task environment. Herdr session operations require a Herdr-managed pane."
---

# Herdr Worktrunk

把“打开任务”执行到环境可用。Worktrunk 编排项目初始化、服务启动和 Git 状态，Herdr 承载 agent。复用项目命令，不维护第二份任务数据库。

## 选择入口

| 用户意图 | 执行结果 |
| --- | --- |
| 接入工作自动化 | 识别项目命令，配置 `.config/wt.toml`，验证初始化、服务和恢复 |
| 打开任务并开始工作 | 创建或复用 checkout，完成必要准备，验证服务，再派发任务 |
| 只打开目录 | 只准备 checkout 和 Herdr 布局，跳过 hooks、服务和 agent |
| 恢复任务 | 重查状态，只补缺失步骤，保留未提交内容 |
| 查看状态 | 联合报告 Git、环境、agent 和交付状态，不执行修复 |
| 验证交付 | 执行项目验证命令，核对当前代码和已有 PR 证据 |

输入为仓库、任务分支或 checkout 路径，以及可选 base、标题、agent 类型和任务内容。从上下文推导已知值，新任务按仓库约定选择稳定分支名。多个已有任务匹配时列出候选再确认。已有授权覆盖的初始化不重复询问。

用目标主机、Git common directory 和精确分支识别任务，以真实 checkout 路径匹配 Herdr。Detached checkout 按明确路径恢复。标题和 pane 序号不能替代身份。

## 前置检查

1. 读取目标仓库的 `AGENTS.md`，检查 branch、worktree、dirty 和现有任务归属。
2. 用 `wt --version` 确认 Worktrunk。Windows 的 `wt` 可能是 Windows Terminal，此时检查并使用 `git-wt`。以安装版本的 `switch -h`、`hook -h`、`config -h` 为准。
3. 所有命令在目标仓库所在主机运行。在任何 Herdr 会话查询或控制前确认 `HERDR_ENV=1`。不在 Herdr 中时可以继续配置和验证 Worktrunk，但报告尚未接入终端，不连接外部聚焦会话。
4. 加载已安装的 `herdr/SKILL.md`；缺失时读 `herdr --skill`。确认 `herdr worktree open --help` 可用。该 Skill 不需要安装 shell integration。

命令块中的 `repo`、`branch`、`base`、`checkout`、`workspace_id` 和 `title` 是解析后的输入，每次工具调用显式传入并保持引用。任务正文通过 agent prompt 的独立参数传递，不拼接进 shell 命令。

## 接入项目自动化

首次接入或准备不完整时，读取 [项目自动化配置](references/automation.md)。完成以下工作后再宣称项目已接入：

- 从 `justfile`、包管理器、lockfile、开发文档和已有容器配置识别准备、准备状态检查、开发服务、健康检查及验证命令。文档任务没有服务需求时记为“不适用”。
- `.config/wt.toml` 是项目的 Worktrunk 编排真源。hooks 和 aliases 调用已有项目命令；缺少命令时在项目授权范围内补最小入口。不另写重复安装脚本或全局 hooks。
- `pre-start` 承载 agent 必需的阻塞准备，`post-start` 承载后台服务。依赖顺序放在同一来源的 pipeline，不能假定同表命令或用户、项目 hooks 之间会串行。
- 给服务配置按仓库和分支推导的端口、URL 和健康检查。哈希端口仍可能碰撞，启动前验证端口归属，不能把另一个服务的 HTTP 200 当成本任务就绪。
- 验证新建能用、重复打开不重复准备或启动、准备失败不派发、服务退出能单独恢复。留下真实命令结果，不只检查 TOML 语法。

已有自动化时直接复用。先检查 `wt config show` 和 `wt hook show` 的有效定义，也检查目标基线上的配置。配置可能含私密值，报告仅保留命令名和状态。主 checkout 未提交的配置不会自动出现在新 worktree，必须确认目标 checkout 拥有配置及调用文件；不要替用户隐式 commit。

## 打开工作环境

同一任务由一个控制者顺序打开，此 Skill 不提供并发调度锁。已有 orchestrator job 的 checkout 继续由该 job 管理。

1. 先运行“查看状态”。已有 checkout 时直接检查准备和服务状态，不再次执行 `wt switch`，避免重复 hooks。
2. 没有 checkout 时区分已有分支和新分支。新分支的 base 优先用户指定值，其次仓库默认分支，先验证 ref 存在。需要最新基线时按授权 fetch；未刷新的 ref 不称为最新。
3. 正常工作环境先审阅本次有效的 `pre-switch`、`pre-start`、`post-start`、`post-switch` 及调用文件。全部符合授权且调用目录与目标基线配置一致时，让 Worktrunk 原生执行 hooks：

   ```bash
   wt -C "$repo" switch --create "$branch" --base "$base" --no-cd --format=json --yes
   ```

   已有分支去掉 `--create` 和 `--base`。这里的 `--yes` 仅适用于已审阅的本次命令，不批准未来 hook 变更。
4. 只打开目录、目标配置未审阅或混有超出授权的 hooks 时，用 `--no-hooks` 且不传 `--yes`。需要工作环境时，在目标 checkout 审阅配置并执行符合授权的具名准备和服务 hooks，完成下节验收。不能跳过 hooks 后仍报告环境就绪。
5. 从 switch JSON 的 `path` 读取路径并核对 Git 注册信息。错误或超时后先重查，分支或目录可能已创建。路径占用、错误仓库、prunable 项和分支不符时保留现场，不用 force、clobber 或 prune 修掉冲突。
6. 按“环境准备与恢复”验证依赖和服务。失败就报告阶段、退出码及相关日志，不启动依赖该环境的实现任务。
7. 用 `herdr worktree list --cwd "$repo"` 在 `.result.worktrees` 按路径找 `open_workspace_id`。已有 ID 就复用并用 workspace get 核对 checkout；没有时执行：

   ```bash
   herdr worktree open --cwd "$repo" --path "$checkout" --label "$title" --no-focus
   ```

8. 从 `.result.workspace`、`.result.tab`、`.result.root_pane` 取 IDs。Herdr 可能同时打开父仓库 workspace，记录新建对象。checkout 始终由 Worktrunk 创建，Herdr 只负责打开。
9. 用户要求开始工作时，按 Herdr Skill 在已核对的空闲 shell pane 启动所选 agent，传入任务、checkout、服务 URL 和验证命令。沿用项目或当前任务的 agent 选择。已有 agent 时检查身份，working 不重复派发，blocked 检查阻塞，unknown 检查现场。

默认一个实现 pane。服务已由 hook 管理时，不在 Herdr 再启动第二份服务；可以增加日志或验证 pane。另一写入 agent 使用独立 checkout。后台使用 `--no-focus`，用户明确要求切换时才 focus。

## 环境准备与恢复

先跑项目只读准备检查，核对依赖、lockfile、运行时版本和生成配置。空 marker 或目录存在不足以证明准备完成。

| 实际状态 | 下一步 |
| --- | --- |
| 准备和服务均就绪 | 复用，不重跑 hooks 或重启进程 |
| 准备缺失或过期，没有活跃写入者 | 执行具名 `pre-start` hook，成功后重跑准备检查 |
| 准备过期且 agent 正在工作 | 报告冲突并协调暂停，不能并发改写依赖 |
| 必需准备失败 | 保留 checkout，记录失败，阻止后续服务和任务派发 |
| 服务未运行、准备已就绪 | 仅执行对应 `post-start` hook，再等待健康检查 |
| 端口由其他 checkout 或未知进程占用 | 不接管、不杀进程；使用项目支持的端口覆盖，同步启动、URL 和检查 |
| workspace 已关闭 | 重新 open 同一 checkout，先检查 hook 服务是否仍运行 |
| checkout 缺失、分支仍在 | 报告缺失；有重建意图才创建，旧未提交内容无法从分支恢复 |

恢复命令示例为 `wt -C "$checkout" hook pre-start project:prepare --yes` 和 `wt -C "$checkout" hook post-start project:dev --yes`。名称以实际配置为准，先审阅该名称匹配到的全部命令，只执行需要的阶段。

`post-start` 返回仅表示启动已安排。以有截止时间的健康探测验收，默认最多等待 60 秒；项目有明确启动预算时采用项目值。确认响应及进程或实例身份属于目标 checkout。超时后检查 `wt config state logs get --format=json` 中本任务的日志，区分仍启动中、已退出和错误服务，不盲目再次启动。

## 联合状态与交付验证

状态查询默认使用：

```bash
git -C "$repo" worktree list --porcelain
wt -C "$repo" list --format=json
herdr worktree list --cwd "$repo"
```

Worktrunk schema 1 是数组，路径在 `path`；schema 2 使用 `items`，路径在 `worktree.path`。先检查结构，分支行可以没有 checkout。不要为了读取状态修改全局配置。严格离线只读时用 Git 替代可能执行配置命令的展示列，PR 和 CI 记为未查询。

按路径关联 Herdr，仅读取本任务的 pane 和 agent。表格报告分支、dirty、领先落后、准备状态、服务 URL 与健康结果、agent 状态、验证结果和 PR/CI。未知、不适用和失败分别表达。状态操作不修复环境、不启动进程、不跑昂贵测试。

用户要求验证交付时执行项目原有检查或已配置的 `wt verify` alias。记录命令、退出码、HEAD 与 dirty 状态。新改动会使旧检查过期；脏工作区只记录 HEAD 不足以绑定证据，还需文件内容摘要或 diff。需要远程状态时按用户意图查询 `wt list --full` 或 forge CLI，核对 PR head SHA 与本地 HEAD。

Herdr 的 `done`、hook 启动成功和端口监听都不是完成证明。派发后核对可见任务、实际产物和验证结果。若返回 settled 却没有产物，先检查 agent get、终端和文件；确认上一轮未执行且没有活跃工作后才重试，不能按固定延时重复发送。

关闭 workspace、停止服务、删除 checkout、删除分支、commit、push 和 merge 分别遵循用户已有授权。关闭 Herdr 不一定停止 hook 服务。`wt merge` 可能 squash、rebase 和清理，不作为隐式验收按钮。队列或批量派发加载 `herdr-orchestrator`，不能同时为同一任务创建 checkout。

## 验证 Skill 变更

运行平台 Skill validator。使用隔离临时仓库执行 [自动化验收场景](references/automation.md#验收场景)，保存真实命令结果。未执行的 agent、远程和并发场景明确列出，不以文档检查替代运行证据。
