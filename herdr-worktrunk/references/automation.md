# 配置项目的 Worktrunk 自动化

## 复用项目入口

先查看现有任务入口及其实现。下面的 TOML 适用于已经提供这些 `just` 命令的项目；命令名不是此 Skill 对所有项目的要求。

| 项目命令 | 行为契约 |
| --- | --- |
| `just bootstrap` | 完成依赖和非敏感本地配置准备，可重复执行；失败返回非零 |
| `just prepared` | 只读核对当前 lockfile、工具版本和必要产物，过期返回非零 |
| `just dev PORT` | 前台启动服务，绑定指定端口，拒绝自动换端口 |
| `just ready PORT` | 有超时的只读健康检查，验证本 checkout 的服务身份 |
| `just check` | 项目已有测试、构建或质量检查 |

项目使用 npm、pnpm、uv 或其他工具时替换为已验证的现有命令。遵循现有 lockfile，不引入另一套依赖管理。没有开发服务的项目省略 dev、ready 和 URL。

## 最小项目配置

在 `.config/wt.toml` 中合并配置，不覆盖已有 hooks。端口表达式在启动、健康检查和 URL 中保持一致。`vars.port` 是 Worktrunk 的分支级覆盖值，未设置时使用仓库与分支哈希。

```toml
[pre-start]
prepare = "just bootstrap"

[post-start]
dev = "just dev {{ vars.port | default((repo ~ '-' ~ branch) | hash_port) }}"

[aliases]
prepared = "just prepared"
ready = "just ready {{ vars.port | default((repo ~ '-' ~ branch) | hash_port) }}"
verify = "just check"

[list]
url = "http://127.0.0.1:{{ vars.port | default((repo ~ '-' ~ branch) | hash_port) }}"
```

准备有依赖顺序时使用 `[[pre-start]]` pipeline。一个表的多个命令可能并发；用户与项目 hooks 分别编排，不能跨来源依赖顺序。

普通 `post-start` 服务在后台运行并写入 Worktrunk 日志，关闭 Herdr workspace 后可能继续运行。已有进程管理器时复用。安装版本支持且项目选择以 checkout 删除作为服务终点时，可用 `wt step tether -- ...` 包装服务。它属于实验性能力，需单独实测目标平台，不默认引入，也不通过删除 checkout 来重启服务。

哈希端口不保证无冲突。读取最终端口：

```bash
wt -C "$checkout" step eval "{{ vars.port | default((repo ~ '-' ~ branch) | hash_port) }}"
```

检查监听进程和 checkout 归属。项目支持覆盖时，选择确认空闲的端口，通过 `wt config state vars set port=...` 记录在本任务分支，再重新计算 URL 并启动。不要只改一次启动命令，让状态与检查仍指向旧端口。

## 审阅与执行

用 `wt config show --format=json` 定位生效配置，用 `wt hook show --format=json` 检查实际 hooks。原生 switch 也会运行 switch hooks。审阅调用脚本、作用目录和参数后，才对本次已授权命令使用 `--yes`。

首次配置尚未提交时，不假定新分支已有配置。可在获授权的目标 checkout 加入同一配置并显式运行 start hooks，验证后交由现有 Git 流程处理。不要为触发自动化修改用户主分支或提交无关文件。

新建工作环境由 `wt switch` 自动执行已审阅 hooks。`pre-start` 非零即停止后续流程；checkout 可能已存在，恢复时先查询现状。

已有环境按以下顺序操作：

1. 执行 `wt --yes prepared`，按实际状态决定是否运行 `wt hook pre-start project:prepare --yes`。
2. 执行 `wt --yes ready`，服务健康则复用。
3. 服务缺失时，确认无活跃启动进程和端口冲突，再执行 `wt hook post-start project:dev --yes`。
4. 在启动预算内重试健康检查，通过后才启动依赖服务的 agent 任务。
5. 工作完成后执行 `wt --yes verify`。它只调用 `just check`，不隐式提交、合并或删除。

项目 alias 需要批准时，已审阅且授权的调用把全局 `--yes` 放在 alias 名之前，例如 `wt -C "$checkout" --yes ready`。放在 alias 名后可能被当作业务参数转发。

命令都在目标 checkout 执行，或显式带 `-C "$checkout"`。恢复前审阅所选 hooks 和 aliases；同名用户与项目 hook 都可能执行，具名调用用 `project:` 或 `user:` 限定来源。

## 可选缓存复用

安装耗时明显时才考虑 `wt step copy-ignored`。由项目定义 `.worktreeinclude`，仅允许明确的可重建缓存，再用 `--require-include --dry-run` 查看清单。排除 `.env`、token、私有 session、数据库和 PID 文件；不用 `--force` 覆盖现有内容。

复制必须先于依赖校验或安装。按目标 lockfile 和工具版本校验，不能把源目录存在视为目标就绪。已有共享包缓存时优先使用已有机制。

## 验收场景

使用临时仓库及独立用户配置，服务只监听 loopback。示例项目可用 Python 标准库和 `just`，无需安装真实应用依赖。准备命令读取版本输入，生成对应产物并记录调用次数；健康端点返回 checkout、准备版本和 PID，不能只返回固定 OK。

| 场景 | 验收条件 |
| --- | --- |
| 新建任务 | 原生 switch 自动 prepare 并安排 dev；健康检查看到正确 checkout 与准备版本 |
| 两个任务 | 独立 checkout 和服务实例，冲突明确报告，内容不串用 |
| 重复打开 | 检查通过，prepare 次数和服务 PID 不变 |
| 准备失败 | pre-start 非零，dev 未启动，不派发 agent；保留 checkout |
| 修复后恢复 | 只重跑失败的 prepare，再启动 dev；分支和 checkout 不变 |
| 服务退出 | 只重启 dev，prepare 次数不增加 |
| 错误服务 | HTTP 200 但 checkout 身份不同，ready 必须失败 |
| 验证交付 | verify 执行真实检查并传播非零退出码，refs 不变 |
| 只读状态 | 查询不改变任务文件、refs 或服务 PID |

终端联动验收用 `herdr worktree open` 接入已就绪 checkout，再实际派发一个检查健康端点的有限任务。核对 agent 产物与环境身份，workspace 存在不算通过。只停止本轮启动且已核对身份的测试服务，保留报告。

参考：[Worktrunk hooks](https://worktrunk.dev/hook/)、[配置与 aliases](https://worktrunk.dev/config/)、[开发服务示例](https://worktrunk.dev/tips-patterns/)。CLI 语法以安装版本为准。
