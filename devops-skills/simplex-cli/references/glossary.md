# Simplex Router / `simplex-cli` 术语表（Glossary）

> 目的：把后端/CLI 的英文标识（命令、字段、表、指标）与中文释义对齐，并标注它们的业务关系与常见坑点。

## 0) 速记：最容易混淆的标识符

- `user_id`（**int64**）：`anotherme.users.id`（账号库的数值主键）。常见于：`credit`、`invite usages`、`active-users`、`project`、`whitelist`。
- `userId`（**string**）：`token_usage.user_id` / `user_cost_totals.user_id` / `user_token_totals.user_id`（用量/成本库的字符串标识）。常见于：`user usage <userId>`、`stats`、`cost <userId>`。
- `email`：检索键（如 `user get`、`project query`、`whitelist add/remove` 等），但 **不等同于** 上述两类 userId。

## 1) CLI / 配置 / 输出

| Term（EN/标识） | 中文 | 含义/备注 | 关联（命令/字段） |
|---|---|---|---|
| `simplex-cli` | 管理员 CLI | Simplex Router 后台管理命令行工具 | 所有命令入口 |
| `base_url` / `--base-url` | 后端地址 | 必须包含 scheme+host；CLI 客户端会自动拼接 `/api` | `config set base-url …` |
| `token` / `--token` | JWT 令牌 | 登录后写入配置；用于 `Authorization: Bearer <token>` | `auth login/logout/status` |
| `config.yaml` | 配置文件 | 默认 `~/.simplex/inner-management/config.yaml`；缺失会自动初始化默认值 | `config show/init/set` |
| `--config` / `SIMPLEX_CLI_CONFIG` | 配置路径 | 覆盖默认配置文件路径 | 全局 flag / env |
| `output` / `--output` | 输出格式 | `table`（默认）、`json`、`llm`（推荐给 agent 解析） | 全局 flag / config |
| `--insecure` | 跳过 TLS 校验 | 仅在 HTTPS 场景生效；用于自签证书环境排障 | 全局 flag |
| `timeout_seconds` / `--timeout` | 超时 | HTTP 超时（秒） | 全局 flag / config |

## 2) Auth / JWT

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `JWT` | JWT | 登录后获得的 token；`auth status --validate` 会发起受保护请求校验 | `auth login/status` |
| `expireAt` | 过期时间 | token 过期时间（若服务返回） | `auth login` 输出 |
| `publicKey` | RSA 公钥 | 登录前拉取公钥并加密密码 | `GET /auth/public-key` |

## 3) Invite Codes（邀请码）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `invite code` / `InviteCode` | 邀请码 | 8 位字符串，用于注册/增长投放等 | `invite *`, `register *` |
| `code` | 邀请码内容 | `create` 时会自动转大写 | `invite create --code=…` |
| `type`=`single_use` | 单次使用 | 通常最大使用次数为 1 | `invite create/generate --type=single_use` |
| `type`=`referral` | 多次/推荐 | 通常允许多次使用（默认极大上限） | `invite create/generate --type=referral` |
| `status`=`active/used/disabled/expired` | 状态 | 按状态筛选/治理 | `invite list --status=…` |
| `maxUses` / `usedCount` | 最大/已用次数 | 用量控制与观测 | `invite list` 输出 |
| `channel` | 渠道 | 例如 `marketing` | `invite create/generate --channel=…` |
| `tag` | 标签 | 便于分类 | `invite list --tag=…` |
| `createdBy` | 创建人 | 操作审计字段 | `invite create/generate --created-by=…` |
| `validFrom` / `validTo` | 生效/过期时间 | **格式为** `YYYY-MM-DD HH:mm:ss` | `invite create/generate` |
| `ownerUserId` | 归属用户ID | 可选；通常为 `anotherme.users.id` | `invite list --owner-user-id=…` |

## 4) Invite Code Usages（邀请码使用记录）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `invite_code_usages` | 使用记录表 | 一个邀请码可能被多个用户使用（聚合展示） | `invite usages` |
| `usedAt` | 使用时间 | **筛选格式为** `YYYY-MM-DD HH:mm:ss` | `invite usages --start-time/--end-time` |
| `excludeWhitelist` | 排除白名单 | 默认 **true（排除内部账号）** | `invite usages --exclude-whitelist=true` |
| `singleUseCount` / `referralCount` | 类型计数 | 按邀请码去重统计数量 | `invite usages` 输出 |

## 5) User Registration（用户注册）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `register` | 注册 | 使用邀请码为邮箱注册账号 | `register user/batch` |
| `username` | 用户名 | 可选；为空时从邮箱前缀推导并做规范化 | `register user --username=…` |
| `password` | 明文密码 | **仅成功时返回**；属于敏感信息 | `register *` 输出 |
| `inviteCode` | 注册邀请码 | 必填，长度 8 | `register * --invite-code=…` |

## 6) Waitlist（等待名单）

> 说明：Waitlist 是后端能力，CLI 里可能未提供对应命令（取决于版本）。

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `waitlist` | 等待名单 | 潜在用户申请入口与内部审批 | `POST /john-waitlist`, `GET /v1/internal/waitlist` |
| `status`=`pending/approved/rejected` | 申请状态 | 内部审批状态机 | `PUT /v1/internal/waitlist/:id/status` |
| `profileUrl` | 个人/公司主页 | 例如 LinkedIn / 官网 | waitlist 字段 |
| `useCases` | 使用场景 | 用户选择的用例标签 | waitlist 字段 |

## 7) Accounts & Whitelist（账号与白名单/内部账号）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `accounts`（命令） | 账号列表 | CLI 用 `user list/get` 查询账号库用户 | `user list/get` |
| `internal_accounts` / `whitelist` | 白名单/内部账号 | 用于过滤内部同事账号在统计中的影响 | `whitelist *`, `excludeWhitelist` |
| `isInternal` | 是否白名单 | 在 `user list` 输出；也可用于筛选 | `user list --is-internal=true` |
| `addedAt` | 加入白名单时间 | 仅白名单用户有值 | `user list --wide` |

## 8) Credits（积分/余额）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `credit` | 积分系统 | 余额/充值/扣减/流水 | `credit list/adjust/history` |
| `balance` | 余额 | 当前可用积分 | `credit list` |
| `amount` | 总额 | 累计积分总额（语义依赖后端实现） | `credit list` |
| `transaction_id` | 交易ID | 幂等键；可重复调用避免重复扣费/充值 | `credit adjust --transaction-id=…` |
| `type`=`recharge/deduction/system_grant/refund/initial` | 交易类型 | 充值/扣除/系统赠送/退款/初始化 | `credit adjust/history` |
| `related_id` | 关联业务ID | 可选；用于把积分流水与业务事件关联 | `credit adjust --related-id=…` |

## 9) Token Usage / Cost（用量与成本）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `promptTokens` | 输入 token | prompt 使用量 | `user usage`, `stats` |
| `completionTokens` | 输出 token | completion 使用量 | `user usage`, `stats` |
| `cachedTokens` | 缓存 token | 命中缓存的 token 量 | token usage 字段 |
| `modelName` | 模型名 | 例如 `gpt-4` | token usage 字段 |
| `cost` | 成本 | 精度 8 位小数 | `user usage`, `stats` |
| `sessionId` (string) | 会话ID（字符串） | token_usage 表里的会话标识，可能为空 | `user usage --session-id=…` |
| `user_token_totals` | 用户汇总 | 按用户聚合的 token/cost 统计 | `stats top`, `user_token_totals` |
| `user_cost_totals` | 用户成本汇总 | 总成本 + 成本上限 + 剩余可用成本 | `cost list/get/set-limit` |
| `totalCostLimit` | 成本上限 | 类似预算；调整后会重算 `remainingCost` | `cost set-limit` |

## 10) Sessions / Projects / Tables（会话/项目/表格/导出）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `chat_sessions` | 聊天会话 | 一次对话会话的记录；与项目/用户关联 | `project`, `ranking`, `active-users` |
| `projects` | 项目 | 用户的“项目/工作区”；包含 `share_id` | `active-users`, `project query` |
| `shareId` | 分享ID | UUID；对外分享链接的一部分 | `projects.share_id` |
| `share link` / `linkUrl` | 分享链接 | `baseUrl + "/share/" + shareId` | `project query`, `active-users` |
| `dynamic_tables` | 动态表格 | 生成的结构化表格；含 `schema`、`rowCount`、`exportUrl` | `ranking`, `active-users` |
| `rowCount` | 行数 | 表格行数；用于 `matchedRows`、活跃用户 `totalRowCount` | `ranking`, `active-users` |
| `exportUrl` | 导出链接 | 导出文件 URL；用于统计导出/价值完成 | `ranking`, `gtm`, `project query` |

## 11) Analytics（统计/排名/活跃/转化）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `stats overview/today/top` | 快速统计 | 用量总览/今日/Top 用户 | `stats *` |
| `ranking` / `score` | 排名/得分 | 评分规则：`createChatCount > 0` 得 1 分；`exportCount > 0` 得 3 分 | `ranking list` |
| `createChatCount` | 新增对话次数 | 在时间范围内新增会话数 | `ranking list --start-time/--end-time` |
| `matchedRows` | 匹配结果行数 | 在时间范围内的“匹配结果行”总数（实现依赖后端聚合） | `ranking` 指标 |
| `exportCount` | 导出次数 | `dynamic_tables.export_url` 非空计数 | `ranking` 指标 |
| `lastActiveAt` | 最近活跃 | `chat_sessions.updated_at` 最大值 | `ranking` 指标 |
| `signupAt` | 注册时间 | `users.created_at` | `ranking` 指标 |
| `active users` | 活跃用户 | 在时间范围内有消息的会话/项目（会按项目拆行） | `active-users list` |
| `totalRowCount` | 项目总行数 | 该用户该项目下所有动态表的 `rowCount` 求和 | `active-users list` |
| `GTM conversion` | 转化漏斗 | Stage: 注册成功 → 首次激活（创建对话）→ 价值完成（导出/生成邮件） | `gtm conversion` |
| `conversion_rate` | 转化率 | 相对上一阶段的百分比（%） | `gtm conversion` |
| `retention` | 留存 | **实现口径可能为**：时间范围内创建 ≥2 个项目的用户 | `gtm conversion` |
| `excludeInternal` | 排除内部账号 | 默认 true（排除白名单） | `gtm conversion --exclude-internal=true` |

## 12) Email（邮件）

| Term | 中文 | 含义/备注 | 关联 |
|---|---|---|---|
| `Resend` | 邮件服务 | 通过 Resend 发送邮件 | `email send` |
| `from/to/subject/html/text` | 发件人/收件人/主题/正文 | `to` 支持逗号分隔 | `email send --to=a@x,b@y` |

