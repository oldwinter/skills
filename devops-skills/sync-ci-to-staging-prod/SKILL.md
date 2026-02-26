---
name: sync-ci-to-staging-prod
description: Sync CI business configurations to staging and production with production safety gates.
---

# Sync CI to Staging + Production Skill

此 skill 将 CI 环境的**业务功能配置**一次性同步到 Staging 和 Production 两个环境。
适用于 CI 上验证通过的新功能配置需要同时推广到 Staging 和 Prod 的场景。

**Triggers**: "sync ci to staging and prod", "sync configs to all envs", "promote ci config", "同步ci配置到staging和prod"

## ⚠️ 关键原则

1. **只同步业务功能配置**（feature flags、积分费率、套餐结构、队列定义、邮件模板等）
2. **白名单内的配置永远不同步**（基础设施连接、Stripe 凭据、安全开关等）
3. **Staging 可自动化**，**Production 必须手动确认 ArgoCD sync**

## 环境差异白名单（不同步）

以下配置项在各环境间预期不同，同步时**必须跳过**：

| 白名单项 | CI | Staging | Prod | 原因 |
|----------|-----|---------|------|------|
| `database.default.link` | CI RDS | Staging RDS | Prod RDS | 各环境独立数据库 |
| `redis.default.address` | `k8s-ci` | `k8s-staging` | `k8s-prod` | 各环境独立 MemoryDB |
| `mongodb.default.uri` | CI DocDB | Staging DocDB | Prod DocDB | 各环境独立 DocumentDB |
| `rabbitmq.default.url` | CI MQ | Staging MQ | Prod MQ | 各环境独立 MQ broker |
| `stripe.publishableKey` | `pk_test_*` | `pk_live_*` | `pk_live_*` | CI 用测试密钥 |
| `stripe.secretKey` | `sk_test_*` | `sk_live_*` | `sk_live_*` | CI 用测试密钥 |
| `stripe.webhookSecret` | CI endpoint | Staging endpoint | Prod endpoint | 各环境独立 webhook |
| `payment.*.stripePriceId` | test Price ID | live Price ID | live Price ID | 不同 Stripe 账户 |
| `campaign.sendEmails.redirectEnabled` | `true` | `false` | `false` | CI 安全重定向 |

> `kubernetes/scripts/compare-configs.py` 已内置此白名单。

## 工作流

### Step 0: 全面对比（必须）

```bash
cd kubernetes

# 查看 3 环境配置差异（自动应用白名单）
python3 scripts/compare-configs.py --diff-only

# 如果有 "需要关注的差异项"（红色），说明有业务配置不一致，需要同步
# 如果只有 "白名单内预期不同"（蓝色），说明已同步完毕

# 查看白名单项详情（可选）
python3 scripts/compare-configs.py --diff-only --show-expected

# 对比其他服务
python3 scripts/compare-configs.py -s simplex-gateway --diff-only
python3 scripts/compare-configs.py -s simplex-router-backend --diff-only
```

### Step 1: 确认同步范围

基于 Step 0 的输出，确认哪些差异需要从 CI 同步到 Staging/Prod。

**典型的可同步项（业务功能）：**
- 邮件模板 ID（`resend.welcomeTemplateId`, `resend.verificationCodeTemplateId` 等）
- 邮件发送人（`resend.from`）
- 积分费率（`credit.rates.*`, `credit.signalRates.*`）
- 新用户赠送（`credit.newUserGrant`, `credit.newUserGrantWithInvite`）
- 套餐结构（`payment.plans[]` 结构、金额、描述、并发数）
- RabbitMQ 队列定义（`rabbitmq.default.queues.*` 新队列）
- Worker 并发（`worker.concurrency`）

**不可同步项（白名单）：** 见上方白名单表格。

### Step 2: 执行同步

#### 方式 A: 手动编辑（推荐用于 configs/ 下的 YAML 文件）

对于 `configs/simplex-api/config.yaml` 等文件，手动将 CI 的新配置项添加到 Staging 和 Prod：

```bash
# 打开 3 个文件对比编辑
# CI (源):
#   kubernetes/overlays/aws-ci/configs/simplex-api/config.yaml
# Staging (目标):
#   kubernetes/overlays/aws-staging/configs/simplex-api/config.yaml
# Prod (目标):
#   kubernetes/overlays/aws-prod/configs/simplex-api/config.yaml
```

**注意事项：**
- 复制业务逻辑配置时，保持目标文件的白名单值不变
- `stripePriceId`: Staging/Prod 使用各自的 live Price ID，不要覆盖
- 新增的 pro 套餐需要先在 Stripe Live Dashboard 创建对应 Price，再填入 ID

#### 方式 B: 镜像标签同步（kustomization.yaml）

```bash
# 查看镜像差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 同步到 Staging
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all --dry-run
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all

# 同步到 Prod（需要用 staging-to-prod 脚本）
python3 ~/.cursor/skills/sync-staging-to-prod/scripts/sync_images.py --all --dry-run
python3 ~/.cursor/skills/sync-staging-to-prod/scripts/sync_images.py --all
```

### Step 3: 验证同步结果

```bash
cd kubernetes

# 再次运行对比，确认无残留差异
python3 scripts/compare-configs.py --diff-only

# 期望输出：
#   不同: 0  |  白名单(预期不同): N  |  部分缺失: 0
```

### Step 4: 提交并推送

```bash
cd /path/to/simplex-gitops
git add kubernetes/overlays/aws-staging/ kubernetes/overlays/aws-prod/
git commit -m "chore: sync CI business configs to staging and production

Synced: <列出同步的配置项>
Whitelisted (not synced): infra connections, stripe keys, stripePriceId, campaign.redirectEnabled"
git push
```

### Step 5: 部署

**Staging（可自动）：**
```bash
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging
# 如需手动同步:
argocd app sync simplex-aws-staging
```

**Production（必须手动）：**
```bash
# 查看变更（只读，安全）
argocd app get simplex-aws-prod
argocd app diff simplex-aws-prod

# ⛔ 用户明确要求后才执行
argocd app sync simplex-aws-prod
```

## 常用 Make 命令

```bash
cd kubernetes

# 对比所有服务配置
make config-diff                               # simplex-api (默认)
make config-diff SVC=simplex-gateway
make config-diff SVC=simplex-router-backend
make list-services                             # 列出所有可对比的服务

# 镜像版本对比
make compare-images                            # 快速 bash 对比
make compare-images-detail                     # 详细 Python 对比
```

## 配置文件映射

| 服务 | CI 配置路径 | Staging 配置路径 | Prod 配置路径 |
|------|-----------|-----------------|--------------|
| simplex-api | `overlays/aws-ci/configs/simplex-api/config.yaml` | `overlays/aws-staging/configs/simplex-api/config.yaml` | `overlays/aws-prod/configs/simplex-api/config.yaml` |
| simplex-gateway | `overlays/aws-ci/configs/gateway/config.yaml` | `overlays/aws-staging/configs/gateway/config.yaml` | `overlays/aws-prod/configs/gateway/config.yaml` |
| simplex-router-backend | `overlays/aws-ci/configs/simplex-router-backend/config-backend.yaml` | `overlays/aws-staging/configs/simplex-router-backend/config-backend.yaml` | `overlays/aws-prod/configs/simplex-router-backend/config-backend.yaml` |

## 服务类别

| 类别 | 服务 |
|------|------|
| AI Core | `anotherme-agent`, `anotherme-api`, `anotherme-search`, `anotherme-worker` |
| Frontend | `front`, `front-homepage` |
| Backend | `simplex-cron`, `simplex-gateway-api`, `simplex-gateway-worker` |
| Data | `data-search-api`, `crawler` |
| Infrastructure | `litellm`, `node-server`, `simplex-router`, `simplex-router-backend`, `simplex-router-fronted` |

## Promotion Path

```
CI (aws-ci)
  ↓ 本 Skill: 一次同步到 staging + prod
Staging (aws-staging) + Production (aws-prod)
```

也可以分步：
```
CI (aws-ci)
  ↓ sync-ci-to-staging skill
Staging (aws-staging)
  ↓ sync-staging-to-prod skill
Production (aws-prod)
```
