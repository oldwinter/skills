---
name: sync-ci-to-staging
description: Sync CI environment business configurations to staging with safe deployment guidance.
---

# Sync CI to Staging Skill

此 skill 提供将 Kubernetes kustomization 配置从 CI 环境同步到 Staging 环境的工作流，用于 simplex-gitops 仓库。

## ⚠️ 关键：Staging 环境部署策略

**Staging 环境可以自动同步，但需要谨慎操作。**

工作流程：
1. ✅ 更新 kustomization.yaml（可自动化）
2. ✅ 提交并推送到 GitLab（可自动化）
3. ⚙️ **ArgoCD 同步到 staging 集群 - 可以自动，但建议确认**

推送变更后，告知用户：
- 变更已推送到仓库
- Staging ArgoCD 应用会自动检测变更并同步（如果配置了自动同步）
- 如果未配置自动同步，用户需要手动触发同步

```bash
# 查看待同步的变更（安全，只读）
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging

# 手动同步（如果需要）
argocd app sync simplex-aws-staging
```

## 环境差异白名单

以下配置项在各环境间预期不同，同步时应**跳过**，不需要关注：

| 白名单项 | 原因 |
|----------|------|
| `database.default.link` | 各环境独立 RDS 实例 |
| `redis.default.address` | 各环境独立 MemoryDB |
| `mongodb.default.uri` | 各环境独立 DocumentDB |
| `rabbitmq.default.url` | 各环境独立 MQ broker |
| `stripe.publishableKey` / `secretKey` / `webhookSecret` | CI 用 test keys，Staging 用 live keys |
| `payment.*.stripePriceId` | 不同 Stripe 账户的 Price ID |
| `campaign.sendEmails.redirectEnabled` | CI=true（安全模式），Staging=false |

> `kubernetes/scripts/compare-configs.py` 已内置此白名单，diff 时自动标记为 "expected"。

## 文件位置

```
kubernetes/overlays/aws-ci/kustomization.yaml        # CI 配置
kubernetes/overlays/aws-staging/kustomization.yaml   # Staging 配置
kubernetes/overlays/aws-ci/configs/                  # CI 服务配置文件
kubernetes/overlays/aws-staging/configs/             # Staging 服务配置文件
```

## 快速命令

### 查看 YAML 配置差异（推荐，支持白名单）

```bash
# 在 kubernetes/ 目录下运行
cd kubernetes

# 对比 simplex-api 配置（默认，只显示差异）
make config-diff

# 对比指定服务
make config-diff SVC=simplex-gateway
make config-diff SVC=simplex-router-backend

# 显示白名单项详情
python3 scripts/compare-configs.py --diff-only --show-expected

# JSON 格式输出（适合脚本处理）
python3 scripts/compare-configs.py --json --diff-only

# 列出所有可对比的服务
make list-services
```

### 查看镜像差异

```bash
# 使用同步脚本
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 或使用 make 目标（如果在 kubernetes/ 目录）
make compare-ci-staging-images
```

### 查看配置差异（patches/目录级别）

```bash
# 比较所有配置（ConfigMaps, Secrets 等）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py

# 详细差异（包含文件内容变更）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed

# 只显示安全可同步的配置（排除 secrets, ingress）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only

# 比较特定文件
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --file anotherme-agent-env-configmap.yaml --detailed
```

### 同步镜像

```bash
# 同步特定服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,anotherme-agent

# 同步所有镜像（先 dry-run）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all --dry-run

# 同步所有镜像（应用变更）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all
```

## 同步工作流

### 步骤 0：审查所有差异（推荐）

在同步任何内容之前，全面了解所有差异：

```bash
# 比较镜像
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 比较配置（仅安全可审查的）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only
```

这将显示：
- 🔄 **镜像标签差异**：服务版本不同
- 📝 **ConfigMap 差异**：配置变更（包含详细差异）
- 🔐 **环境特定配置**：不应同步的内容
- ➕ **新资源**：CI 中新增但 staging 中没有的配置

### 步骤 1：比较环境

运行 diff 命令查看 CI 和 Staging 之间的差异：

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff
```

这将显示：
- 🔄 **标签不同**：版本不同的服务
- ✅ **标签相同**：已同步的服务
- ⚠️ **仅 CI**：只在 CI 中的服务
- ⚠️ **仅 STAGING**：只在 Staging 中的服务

### 步骤 2：审查并选择服务

决定推广哪些服务。常见模式：

```bash
# 推广单个关键服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front --dry-run

# 推广前端服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,front-homepage --dry-run

# 推广所有 AI 服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images anotherme-agent,anotherme-api,anotherme-search,anotherme-worker --dry-run

# 推广所有内容
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all --dry-run
```

### 步骤 3：应用变更

审查 dry-run 输出后，应用变更：

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images <services>
```

### 步骤 4：提交并推送

```bash
cd /path/to/simplex-gitops
git add kubernetes/overlays/aws-staging/kustomization.yaml
git commit -m "chore: 从 CI 推广 <services> 到 staging"
git push
```

**重要：推送后 ArgoCD 会检测变更。**

### 步骤 5：Staging 同步（自动或手动）

推送完成后，staging 环境的同步取决于 ArgoCD 配置：

**如果配置了自动同步：**
```bash
# 查看同步状态
argocd app get simplex-aws-staging
argocd app wait simplex-aws-staging --health
```

**如果需要手动同步：**
```bash
# 查看待同步的变更
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging

# 手动触发同步
argocd app sync simplex-aws-staging
```

或通过 ArgoCD Web UI 手动点击 Sync 按钮：
- URL: http://192.168.10.117:31006
- 找到 `simplex-aws-staging` 应用
- 点击 "SYNC" 按钮

## 可能需要同步的配置部分

该 skill 现在提供两个互补的工具：

1. **`sync_images.py`** - 处理镜像标签同步（主要用例）
2. **`compare_configs.py`** - 识别配置差异（新功能）

### 自动配置差异检测

`compare_configs.py` 脚本自动识别以下内容的差异：

#### 1. patches/ 中的 ConfigMaps 和 Secrets

脚本将每个文件分类为：

| 类别 | 示例 | 同步建议 |
|----------|----------|-------------------|
| ✅ **安全可审查** | `*-env-configmap.yaml` | 仔细审查，可能需要选择性同步 |
| 🔐 **Secrets** | `*-secrets.yaml` | 永不同步 - 环境特定 |
| 🌐 **Ingress** | `ingress.yaml` | 永不同步 - 域名不同 |
| ⚙️ **基础设施** | `gateway-cm0-*`, `router-cm0-*`, `api-cm0-*` | 通常是环境特定的 |

**使用方法：**
```bash
# 显示所有配置差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py

# 显示详细差异（包含文件内容变更）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed

# 只显示安全可审查的配置
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only

# 比较特定文件
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --file anotherme-agent-env-configmap.yaml --detailed
```

**输出包括：**
- 🔄 有差异的文件（按安全性分类）
- ➕ CI 中新增的文件
- ➖ CI 中删除的文件
- ✅ 相同的文件
- 📝 详细的变更分析（添加/删除/修改的键）
- 💡 同步建议

#### 2. kustomization.yaml 中的新资源

脚本还比较 `resources:` 和 `patches:` 部分：
- ➕ CI 中新增的资源
- ➖ CI 中删除的资源
- 📋 共同的资源

### 常见配置差异

基于分析，典型差异包括：

| 配置文件 | 常见差异 | 同步？ |
|-------------|-------------------|-------|
| `anotherme-agent-env-configmap.yaml` | MQ_HOST, REDIS_URL, API keys | ⚠️ 选择性 |
| `anotherme-search-env-configmap.yaml` | LLM presets, RABBITMQ_URL, API keys | ⚠️ 选择性 |
| `frontend-env.yaml` | API_URL, APP_ENV | ❌ 永不（环境特定） |
| `simplex-cron-env-configmap.yaml` | RABBITMQ_URL | ⚠️ 选择性 |
| `anotherme-agent-secrets.yaml` | 所有 secret 值 | ❌ 永不 |
| `ingress.yaml` | 主机名, TLS 配置 | ❌ 永不 |
| `*-cm0-configmap.yaml` | 基础设施设置 | ❌ 通常不 |

### 手动同步 ConfigMaps（必要时）

对于识别为安全可审查的配置，可以在仔细审查后手动同步：

```bash
# 1. 先查看详细差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py \
  --file anotherme-agent-env-configmap.yaml --detailed

# 2. 手动审查应同步哪些键
# 有些键如 REDIS_URL, MQ_HOST 是环境特定的
# 其他如功能标志或 LLM presets 可能需要同步

# 3. 如果需要，手动编辑 staging 文件
vim kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml

# 4. 提交并推送
git add kubernetes/overlays/aws-staging/patches/
git commit -m "chore: 从 CI 同步特定配置键"
git push
```

### 旧手动模式（仍然有效）

#### 镜像标签（主要同步目标）

位于 `images:` 部分。这是 `sync_images.py` 脚本自动处理的内容。

#### ConfigMap Patches（需要手动审查）

`patches/` 目录中的文件可能包含环境特定的值：

| Patch 文件 | 用途 | 同步考虑 |
|------------|---------|-------------------|
| `api-cm0-configmap.yaml` | API 配置 | 通常是环境特定的，不同步 |
| `gateway-cm0-configmap.yaml` | Gateway 配置 | 通常是环境特定的 |
| `anotherme-agent-env-configmap.yaml` | Agent 配置 | 可能需要选择性同步 |
| `anotherme-agent-secrets.yaml` | Agent secrets | 永不同步，环境特定 |
| `anotherme-search-env-configmap.yaml` | Search 配置 | 可能需要选择性同步 |
| `simplex-cron-env-configmap.yaml` | Cron 配置 | 通常是环境特定的 |
| `simplex-router-cm0-configmap.yaml` | Router 配置 | 通常是环境特定的 |
| `frontend-env.yaml` | 前端环境变量 | 通常是环境特定的 |
| `ingress.yaml` | Ingress 规则 | 永不同步，域名不同 |

#### 副本数

CI 通常运行更少的副本。Staging 使用 base 默认值或更高值。这是有意的，不应同步。

#### 节点池分配

- CI: `karpenter.sh/nodepool: ci` / `singleton-ci`
- Staging: `karpenter.sh/nodepool: staging` / `singleton-staging`

这些是环境特定的，不应同步。

#### 存储类

两个环境使用相似的模式，但可能有不同的存储类名称。通常不需要同步。

#### 高可用设置

Staging 可能有额外的 HA 配置：
- 跨 AZ 分布的 `topologySpreadConstraints`
- 优雅关闭的 `terminationGracePeriodSeconds: 60`

这些是 staging 特定的优化，不应同步到 CI。

## 手动同步模式

对于自动同步脚本未处理的配置：

### 同步特定 ConfigMap Patch

```bash
# 1. 使用新的 compare_configs.py 查看详细差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py \
  --file anotherme-agent-env-configmap.yaml --detailed

# 2. 仔细审查差异
# 识别哪些键是：
#   - 环境特定的（REDIS_URL, MQ_HOST, DATABASE_URL）
#   - 功能标志或业务逻辑（LLM_PRESET, 功能开关）
#   - API keys（环境间可能不同）

# 3. 如果合适，手动同步
# 选项 A：复制整个文件（很少合适）
cp kubernetes/overlays/aws-ci/patches/anotherme-agent-env-configmap.yaml \
   kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml

# 选项 B：手动编辑特定键（推荐）
vim kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml
# 只更新需要同步的键（例如 LLM_PRESET）
# 保持环境特定的值不变

# 4. 验证变更
git diff kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml
```

### 同步新资源

如果 CI 有 staging 需要的新资源（PV、PVC、ConfigMaps 等）：

```bash
# 1. 检查新资源
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py

# 查找 "NEW IN CI" 部分

# 2. 将资源文件复制到 aws-staging
cp kubernetes/overlays/aws-ci/patches/new-config.yaml \
   kubernetes/overlays/aws-staging/patches/

# 3. 添加到 aws-staging kustomization.yaml patches 部分
vim kubernetes/overlays/aws-staging/kustomization.yaml

# 4. 调整环境特定的值
vim kubernetes/overlays/aws-staging/patches/new-config.yaml
# 更新命名空间标签、URL、API 端点等

# 5. 验证清单
kubectl kustomize kubernetes/overlays/aws-staging > /tmp/staging-check.yaml
# 审查 /tmp/staging-check.yaml 的正确性
```

## 同步后验证

### 检查 ArgoCD 状态（只读，安全）

```bash
# 查看应用状态和待同步变更
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging
```

### 手动同步（用户必须明确请求）

```bash
# ⚠️ 仅在用户明确要求时执行
argocd app sync simplex-aws-staging
```

### 检查部署的版本

```bash
# Staging namespace
k2 get pods -n staging -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'

# CI namespace
k1 get pods -n ci -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'
```

### 验证清单

```bash
kubectl kustomize kubernetes/overlays/aws-staging > /tmp/staging-manifests.yaml
kubectl kustomize kubernetes/overlays/aws-ci > /tmp/ci-manifests.yaml
diff /tmp/ci-manifests.yaml /tmp/staging-manifests.yaml
```

## 故障排除

### 脚本未找到仓库

确保你在 simplex-gitops 目录中或明确设置路径：

```bash
cd /path/to/simplex-gitops
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff
```

### CI 中未找到镜像

服务可能使用不同的镜像名称格式（Aliyun vs ECR）。检查 kustomization 文件中的两种格式。

### ArgoCD 未同步

```bash
# 查看应用状态（只读）
argocd app get simplex-aws-staging --show-operation

# 刷新应用检测最新变更（只读，安全）
argocd app refresh simplex-aws-staging

# ⚠️ 手动同步 - 仅在用户明确要求时执行
argocd app sync simplex-aws-staging
```

## 服务类别参考

| 类别 | 服务 |
|----------|----------|
| AI 核心 | `anotherme-agent`, `anotherme-api`, `anotherme-search`, `anotherme-worker` |
| 前端 | `front`, `front-homepage` |
| 后端 | `simplex-cron`, `simplex-gateway-api`, `simplex-gateway-worker` |
| 数据 | `data-search-api`, `crawler` |
| 基础设施 | `litellm`, `node-server`, `simplex-router`, `simplex-router-backend`, `simplex-router-fronted` |
