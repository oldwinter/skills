# `simplex-cli` Cheatsheet（给 AI agent 的速查）

## 1) 建议的“开局三连”

```bash
simplex-cli version
simplex-cli config show --output=llm
simplex-cli auth status --validate --output=llm
```

> agent 默认推荐把输出设为 `llm`：`simplex-cli config set output llm`

如果本机没有安装 `simplex-cli`，可在源码仓库里构建（产物路径可自定义）：

```bash
cd cli
go build -o simplex-cli ./cmd/simplex-cli
./simplex-cli version
```

## 2) 全局参数（Persistent Flags）

- `--config <path>`：配置文件路径（默认 `~/.simplex/inner-management/config.yaml`）
- `--base-url <url>`：后端地址（必须含 `http(s)://`；CLI 会自动拼接 `/api`）
- `--token <jwt>`：覆盖配置文件里的 token
- `--output table|json|llm`：覆盖输出格式
- `--insecure`：跳过 TLS 校验（仅 HTTPS）
- `--timeout <seconds>`：HTTP 超时（秒）

环境变量（与配置同名，前缀 `SIMPLEX_CLI_`）也会生效，例如：`SIMPLEX_CLI_BASE_URL`、`SIMPLEX_CLI_TOKEN`、`SIMPLEX_CLI_OUTPUT`。

## 3) 时间格式速查

| 场景 | 参数 | 格式 |
|---|---|---|
| token usage / stats / ranking / active-users / gtm | `--start-time/--end-time` | RFC3339 / ISO8601（例：`2026-02-04T00:00:00Z`） |
| invite usages / waitlist list（内部） | `startTime/endTime` | `YYYY-MM-DD HH:mm:ss`（例：`2026-02-04 00:00:00`） |

## 4) 读 vs 写（运行前确认）

**读（查询/统计）**：通常可直接运行并汇总结果。  
**写（会修改状态/发送外部动作）**：必须先让用户确认“将要执行的命令”。

常见写操作：
- `invite create|generate`
- `register user|batch`
- `credit adjust`
- `cost set-limit`
- `whitelist add|add-batch|remove|remove-batch`
- `email send`
- `auth login/logout`、`config set/init`（会写本地配置文件）

## 5) 常用命令模板（按任务）

### 5.1 登录与配置

```bash
simplex-cli config init --base-url https://staging-inner-ui.lev8.com/ --force
simplex-cli auth login --username <admin>
simplex-cli auth status --validate
```

非交互式登录：

```bash
echo -n "<PASSWORD>" | simplex-cli auth login --username <admin> --password-stdin
```

### 5.2 邀请码（Invite）

读：

```bash
simplex-cli invite list --status=active --page=1 --size=20 --output=llm
simplex-cli invite usages --code=ABCDEFGH --page=1 --page-size=20 --output=llm
```

写（先确认）：

```bash
simplex-cli invite create --code=ABCDEFGH --type=single_use --channel=marketing --created-by=ops
simplex-cli invite generate --count=50 --type=single_use --channel=marketing --created-by=ops
```

### 5.3 用户注册（Register）

```bash
simplex-cli register user --email=alice@example.com --invite-code=ABCDEFGH --output=llm
simplex-cli register batch --emails=a@example.com,b@example.com --invite-code=ABCDEFGH --output=llm
```

注意：成功时会返回 `password`（敏感）。

### 5.4 白名单（Whitelist / Internal accounts）

```bash
simplex-cli whitelist list --q="@example.com" --page=1 --size=20 --output=llm
simplex-cli whitelist check --emails=a@example.com,b@example.com --output=llm
```

写（先确认）：

```bash
simplex-cli whitelist add --email=user@example.com --username=user1
simplex-cli whitelist add-batch --emails=a@example.com,b@example.com
simplex-cli whitelist remove --email=user@example.com
simplex-cli whitelist remove-batch --emails=a@example.com,b@example.com
```

### 5.5 积分（Credit）

```bash
simplex-cli credit list --keyword="@example.com" --order-by=balance --order=desc --output=llm
simplex-cli credit history --user-id=123 --page=1 --size=10 --output=llm
```

写（先确认）：

```bash
simplex-cli credit adjust --user-id=123 --amount=1000 --type=recharge --description="promo" --output=llm
```

### 5.6 成本（Cost）

```bash
simplex-cli cost list --sort=total_cost --sort-order=desc --output=llm
simplex-cli cost get <userId:string> --output=llm
```

写（先确认）：

```bash
simplex-cli cost set-limit --user-id=<userId:string> --limit=100.0 --output=llm
```

### 5.7 用户与用量（User + Usage）

账号查询（anotherme，数值 `id`）：

```bash
simplex-cli user list --q="@example.com" --output=llm
simplex-cli user get "alice@example.com" --output=llm
```

用量查询（token/cost，字符串 `userId`）：

```bash
simplex-cli user usage <userId:string> --start-time=2026-02-04T00:00:00Z --end-time=2026-02-04T23:59:59Z --output=llm
simplex-cli user usage <userId:string> --sessions --output=llm
```

### 5.8 统计（Stats）

```bash
simplex-cli stats overview --output=llm
simplex-cli stats today --output=llm
simplex-cli stats top --limit=10 --by=tokens --output=llm
```

### 5.9 排名（Ranking）

```bash
simplex-cli ranking list --sort-field=score --sort-order=desc --output=llm
simplex-cli ranking list --start-time=2026-01-01T00:00:00Z --end-time=2026-02-01T00:00:00Z --exclude-whitelist=true --output=llm
```

### 5.10 活跃用户（Active users）

```bash
simplex-cli active-users list --start-time=2026-02-01T00:00:00Z --end-time=2026-02-28T23:59:59Z --exclude-whitelist=true --output=llm
```

### 5.11 项目数据（Project query）

```bash
simplex-cli project query alice@example.com --page=1 --page-size=10 --output=llm
```

### 5.12 GTM 转化（GTM conversion）

```bash
simplex-cli gtm conversion --exclude-internal=true --output=llm
simplex-cli gtm conversion --start-time=2024-01-01T00:00:00Z --end-time=2024-12-31T23:59:59Z --output=llm
```

### 5.13 邮件（Email / Resend）

写（先确认）：

```bash
simplex-cli email send --to=a@example.com,b@example.com --subject="Hello" --text="Body content" --output=llm
```
