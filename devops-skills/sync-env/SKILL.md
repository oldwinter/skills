---
name: sync-env
description: Sync CI environment configurations to staging and optionally to production, with safety gates and whitelist-aware diffing.
---

# Sync Environment Skill

将 CI 环境的 Kubernetes kustomization 配置同步到 Staging，可选同步到 Production。
适用于 simplex-gitops 仓库。

**Triggers**: "sync ci to staging", "sync to staging", "sync to prod", "promote to production",
"同步ci到staging", "同步到生产", "sync configs", "promote images"

## Promotion Path

```
CI (aws-ci)
  ↓ 默认：同步到 staging
Staging (aws-staging)
  ↓ 可选：同步到 production（需明确指定 --target prod 或 --target all）
Production (aws-prod)
```

## ⚠️ 部署策略

| 环境 | 策略 | 说明 |
|------|------|------|
| Staging | 可自动同步 | 推送后 ArgoCD 可自动检测并同步 |
| Production | **必须手动** | 推送后需用户手动触发 ArgoCD sync |

**永远不要自动执行 `argocd app sync simplex-aws-prod`。**

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

> `kubernetes/scripts/compare-configs.py` 已内置此白名单，diff 时自动标记为 "expected"。

## 文件位置

```
kubernetes/overlays/aws-ci/kustomization.yaml        # CI 配置
kubernetes/overlays/aws-staging/kustomization.yaml   # Staging 配置
kubernetes/overlays/aws-prod/kustomization.yaml      # Production 配置
kubernetes/overlays/aws-ci/configs/                  # CI 服务配置文件
kubernetes/overlays/aws-staging/configs/             # Staging 服务配置文件
kubernetes/overlays/aws-prod/configs/                # Production 服务配置文件
```

## 快速命令

### 查看 YAML 配置差异（推荐，支持白名单）

```bash
cd kubernetes

# 对比 simplex-api 配置（默认，只显示差异）
make config-diff

# 对比指定服务
make config-diff SVC=simplex-gateway
make config-diff SVC=simplex-router-backend

# 显示白名单项详情
python3 scripts/compare-configs.py --diff-only --show-expected

# JSON 格式输出
python3 scripts/compare-configs.py --json --diff-only

# 列出所有可对比的服务
make list-services
```

### 查看镜像差异

```bash
# CI vs Staging（默认）
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --diff

# CI vs Production
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --diff --target prod

# Staging vs Production
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --diff --target prod --source staging
```

### 查看配置差异（patches/目录级别）

```bash
# 比较所有配置（CI vs Staging）
python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py

# 详细差异（包含文件内容变更）
python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py --detailed

# 只显示安全可同步的配置（排除 secrets, ingress）
python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py --detailed --safe-only

# 比较特定文件
python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py --file anotherme-agent-env-configmap.yaml --detailed
```

### 同步镜像

```bash
# 同步特定服务到 staging（默认）
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images front,anotherme-agent

# 同步所有镜像到 staging（先 dry-run）
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all --dry-run
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all

# 同步到 production
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all --target prod --dry-run
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all --target prod

# 同时同步到 staging 和 production
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all --target all --dry-run
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all --target all
```

## 同步工作流

### Step 0：全面对比（必须）

```bash
cd kubernetes

# 查看 3 环境配置差异（自动应用白名单）
python3 scripts/compare-configs.py --diff-only

# 如果有 "需要关注的差异项"（红色），说明有业务配置不一致
# 如果只有 "白名单内预期不同"（蓝色），说明已同步完毕

# 查看镜像差异
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --diff

# 查看配置差异（仅安全可审查的）
python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py --detailed --safe-only
```

### Step 1：确认同步范围

基于 Step 0 的输出，确认哪些差异需要同步。

**典型的可同步项（业务功能）：**
- 邮件模板 ID（`resend.welcomeTemplateId` 等）
- 积分费率（`credit.rates.*`, `credit.signalRates.*`）
- 新用户赠送（`credit.newUserGrant`, `credit.newUserGrantWithInvite`）
- 套餐结构（`payment.plans[]` 结构、金额、描述、并发数）
- RabbitMQ 队列定义（`rabbitmq.default.queues.*` 新队列）
- Worker 并发（`worker.concurrency`）

**不可同步项：** 见上方白名单表格。

### Step 2：审查并选择服务

```bash
# 推广单个关键服务
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images front --dry-run

# 推广前端服务
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images front,front-homepage --dry-run

# 推广所有 AI 服务
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images anotherme-agent,anotherme-api,anotherme-search,anotherme-worker --dry-run

# 推广所有内容
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --all --dry-run
```

### Step 3：应用变更

审查 dry-run 输出后，应用变更：

```bash
# 只同步到 staging（默认）
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images <services>

# 同步到 production
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images <services> --target prod

# 同时同步到 staging 和 production
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --images <services> --target all
```

### Step 4：手动同步配置（如果需要）

#### 方式 A: 手动编辑 configs/ 下的 YAML 文件（推荐）

```bash
# 打开文件对比编辑
# CI (源):    kubernetes/overlays/aws-ci/configs/simplex-api/config.yaml
# Staging:    kubernetes/overlays/aws-staging/configs/simplex-api/config.yaml
# Prod:       kubernetes/overlays/aws-prod/configs/simplex-api/config.yaml
```

注意事项：
- 复制业务逻辑配置时，保持目标文件的白名单值不变
- `stripePriceId`: Staging/Prod 使用各自的 live Price ID，不要覆盖
- 新增的 pro 套餐需要先在 Stripe Live Dashboard 创建对应 Price

#### 方式 B: 手动同步 ConfigMap Patches

```bash
# 1. 查看详细差异
python3 ~/.cursor/skills/sync-env/scripts/compare_configs.py \
  --file anotherme-agent-env-configmap.yaml --detailed

# 2. 手动编辑特定键（推荐）
vim kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml

# 3. 验证变更
git diff kubernetes/overlays/aws-staging/patches/
```

### Step 5：提交并推送

```bash
cd /path/to/simplex-gitops

# 只同步了 staging
git add kubernetes/overlays/aws-staging/
git commit -m "chore: 从 CI 推广 <services> 到 staging"
git push

# 同时同步了 staging 和 prod
git add kubernetes/overlays/aws-staging/ kubernetes/overlays/aws-prod/
git commit -m "chore: sync CI business configs to staging and production

Synced: <列出同步的配置项>
Whitelisted (not synced): infra connections, stripe keys, stripePriceId, campaign.redirectEnabled"
git push
```

### Step 6：部署

**Staging（可自动）：**
```bash
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging
# 如需手动同步:
argocd app sync simplex-aws-staging
```

**Production（必须手动确认）：**
```bash
# 查看变更（只读，安全）
argocd app get simplex-aws-prod
argocd app diff simplex-aws-prod

# ⛔ 用户明确要求后才执行
argocd app sync simplex-aws-prod
```

## 可能需要同步的配置部分

### 自动配置差异检测

`compare_configs.py` 脚本自动识别以下内容的差异：

| 类别 | 示例 | 同步建议 |
|------|------|----------|
| ✅ **安全可审查** | `*-env-configmap.yaml` | 仔细审查，可能需要选择性同步 |
| 🔐 **Secrets** | `*-secrets.yaml` | 永不同步 - 环境特定 |
| 🌐 **Ingress** | `ingress.yaml` | 永不同步 - 域名不同 |
| ⚙️ **基础设施** | `gateway-cm0-*`, `router-cm0-*`, `api-cm0-*` | 通常是环境特定的 |

### 不应同步的配置

| 配置 | 原因 |
|------|------|
| 副本数 | CI 运行更少的副本，Staging/Prod 使用 base 默认值 |
| 节点池分配 | CI: `ci`/`singleton-ci`, Staging: `staging`/`singleton-staging`, Prod: `production`/`singleton-production` |
| 存储类 | Prod 使用 `gp3`, Staging 使用 `ebs-gp3-auto` |
| 高可用设置 | Prod 有 `topologySpreadConstraints`、`terminationGracePeriodSeconds: 60` |

## 同步后验证

### 检查 ArgoCD 状态（只读，安全）

```bash
# Staging
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging

# Production
argocd app get simplex-aws-prod
argocd app diff simplex-aws-prod
```

### 手动同步（用户必须明确请求）

```bash
# Staging
argocd app sync simplex-aws-staging

# ⛔ Production - 仅在用户明确要求时执行
argocd app sync simplex-aws-prod
```

### 检查部署的版本

```bash
# CI namespace
k1 get pods -n ci -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'

# Staging namespace
k2 get pods -n staging -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'

# Production namespace
k1 get pods -n production -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'
```

### 验证清单

```bash
kubectl kustomize kubernetes/overlays/aws-ci > /tmp/ci-manifests.yaml
kubectl kustomize kubernetes/overlays/aws-staging > /tmp/staging-manifests.yaml
kubectl kustomize kubernetes/overlays/aws-prod > /tmp/prod-manifests.yaml
diff /tmp/ci-manifests.yaml /tmp/staging-manifests.yaml
diff /tmp/staging-manifests.yaml /tmp/prod-manifests.yaml
```

## 常用 Make 命令

```bash
cd kubernetes

# 对比所有服务配置
make config-diff                               # simplex-api（默认）
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

## 故障排除

### 脚本未找到仓库

确保你在 simplex-gitops 目录中或明确设置路径：

```bash
cd /path/to/simplex-gitops
python3 ~/.cursor/skills/sync-env/scripts/sync_images.py --diff
```

### CI 中未找到镜像

服务可能使用不同的镜像名称格式（Aliyun vs ECR）。检查 kustomization 文件中的两种格式。

### ArgoCD 未同步

```bash
# 查看应用状态（只读）
argocd app get simplex-aws-staging --show-operation
argocd app get simplex-aws-prod --show-operation

# 刷新应用检测最新变更（只读，安全）
argocd app refresh simplex-aws-staging
argocd app refresh simplex-aws-prod

# 手动同步 - staging
argocd app sync simplex-aws-staging

# ⛔ 手动同步 production - 仅在用户明确要求时执行
argocd app sync simplex-aws-prod
```

## 服务类别参考

| 类别 | 服务 |
|------|------|
| AI 核心 | `anotherme-agent`, `anotherme-api`, `anotherme-search`, `anotherme-worker` |
| 前端 | `front`, `front-homepage` |
| 后端 | `simplex-cron`, `simplex-gateway-api`, `simplex-gateway-worker` |
| 数据 | `data-search-api`, `crawler` |
| 基础设施 | `litellm`, `node-server`, `simplex-router`, `simplex-router-backend`, `simplex-router-fronted` |
