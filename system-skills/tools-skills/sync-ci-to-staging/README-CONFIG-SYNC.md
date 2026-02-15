# Sync CI to Staging - 配置同步详细指南

## 概述

这个工具提供了从 CI 环境到 Staging 环境同步配置的能力。除了镜像标签同步（主要用例），还包括配置文件差异检测。

## 工具组成

### 1. `sync_images.py` - 镜像标签同步

**用途：** 将 CI 环境的容器镜像标签同步到 Staging 环境。

**功能：**
- 比较 CI 和 Staging 的镜像标签
- 选择性同步特定服务
- 批量同步所有服务
- Dry-run 模式查看变更

**典型用法：**

```bash
# 查看差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# Dry-run 同步特定服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,anotherme-agent --dry-run

# 实际同步
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,anotherme-agent

# 同步所有服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all
```

### 2. `compare_configs.py` - 配置差异检测

**用途：** 识别 CI 和 Staging 环境之间的配置差异。

**功能：**
- 比较 ConfigMaps 和 Secrets
- 检测新增或删除的资源
- 详细的 diff 输出
- 安全性分类（哪些配置可以同步，哪些不能）

**典型用法：**

```bash
# 查看所有配置差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py

# 详细差异（包含文件内容变更）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed

# 只显示安全可同步的配置
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only

# 比较特定文件
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --file anotherme-agent-env-configmap.yaml --detailed
```

## 配置同步安全性

### 自动分类

脚本会自动将配置文件分为以下几类：

#### ✅ 安全可审查

- **文件：** `*-env-configmap.yaml`
- **建议：** 仔细审查后可选择性同步
- **示例：** `anotherme-agent-env-configmap.yaml`

#### 🔐 Secrets（永不同步）

- **文件：** `*-secrets.yaml`
- **原因：** 环境特定的敏感信息
- **建议：** 永不在环境间同步

#### 🌐 Ingress（永不同步）

- **文件：** `ingress.yaml`
- **原因：** 域名配置环境特定
- **建议：** 永不同步

#### ⚙️ 基础设施配置（通常不同步）

- **文件：** `gateway-cm0-*`, `router-cm0-*`, `api-cm0-*`
- **原因：** 环境特定的基础设施设置
- **建议：** 通常不同步

## 配置同步工作流

### 步骤 1：识别差异

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only
```

这将显示：
- 🔄 有差异的文件（按安全性分类）
- ➕ CI 中新增的文件
- ➖ CI 中删除的文件
- 📝 详细的变更分析

### 步骤 2：审查特定文件

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py \
  --file anotherme-agent-env-configmap.yaml --detailed
```

输出示例：
```
🔄 配置不同 (1 个文件):

  ✅ anotherme-agent-env-configmap.yaml (ConfigMap)
     📝 ConfigMap (同步前仔细审查)
     ➕ 新增键: LLM_PRESET_NEW
     🔄 已修改: 3 个键更改了值

------------------------------------------------------------
--- staging/anotherme-agent-env-configmap.yaml
+++ ci/anotherme-agent-env-configmap.yaml
@@ -15,7 +15,7 @@
-    LLM_PRESET: "default"
+    LLM_PRESET: "optimized"
...
------------------------------------------------------------
```

### 步骤 3：决定是否同步

审查差异后，确定哪些键应该同步：

**环境特定的键（不同步）：**
- `REDIS_URL`
- `MQ_HOST`
- `DATABASE_URL`
- `API_URL`

**业务逻辑/功能标志（可能需要同步）：**
- `LLM_PRESET`
- `FEATURE_FLAG_*`
- `MAX_TOKENS`
- 算法参数

### 步骤 4：手动同步配置

有两种方式：

#### 方式 A：复制整个文件（很少使用）

```bash
cp kubernetes/overlays/aws-ci/patches/file.yaml \
   kubernetes/overlays/aws-staging/patches/file.yaml
```

#### 方式 B：选择性同步（推荐）

```bash
# 1. 编辑 staging 文件
vim kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml

# 2. 只更新需要同步的键
# 保持环境特定的值不变

# 3. 验证变更
git diff kubernetes/overlays/aws-staging/patches/anotherme-agent-env-configmap.yaml
```

### 步骤 5：提交和推送

```bash
git add kubernetes/overlays/aws-staging/patches/
git commit -m "chore: 从 CI 同步配置更新"
git push
```

## 常见配置差异示例

### ConfigMap 差异

```yaml
# CI
data:
  LLM_PRESET: "optimized"
  MAX_TOKENS: "8000"
  REDIS_URL: "redis://ci-redis:6379"

# Staging
data:
  LLM_PRESET: "default"       # 可能需要同步
  MAX_TOKENS: "4000"          # 可能需要同步
  REDIS_URL: "redis://staging-redis:6379"  # 永不同步
```

### 新增资源

```bash
➕ CI 中的新配置 (2 个文件):
  ✅ new-service-env-configmap.yaml - 📝 ConfigMap (同步前仔细审查)
  ⚠️  new-service-secrets.yaml - 🔐 Secrets (环境特定)
```

**处理方式：**
1. 复制 ConfigMap 到 staging
2. 调整环境特定的值
3. **不要**复制 Secrets（手动创建）

## 输出解读

### 配置比较输出

```
📁 Patches 目录比较
--------------------------------------------------------------------------------

🔄 配置不同 (3 个文件):

  ✅ anotherme-agent-env-configmap.yaml (ConfigMap)
     📝 ConfigMap (同步前仔细审查)
     ➕ 新增键: NEW_FEATURE_FLAG
     🔄 已修改: 5 个键更改了值

  ⚠️  anotherme-agent-secrets.yaml (Secret)
     🔐 Secrets (环境特定)
     🔄 已修改: 2 个键更改了值

  ⚠️  ingress.yaml (Ingress)
     🌐 Ingress (域名不同)
     🔄 10 行不同

➕ CI 中的新配置 (1 个文件):
  ✅ new-worker-env-configmap.yaml - 📝 ConfigMap (同步前仔细审查)

✅ 相同 (8 个文件):
  frontend-env.yaml
  gateway-cm0-configmap.yaml
  ...
```

### 建议部分

```
💡 建议:
--------------------------------------------------------------------------------

✅ 安全可审查以同步 (1 个文件):
  • anotherme-agent-env-configmap.yaml

  审查这些文件，如果合适则同步:
  python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_config.py --file <filename>

⚠️  环境特定配置 (2 个文件):
  • anotherme-agent-secrets.yaml - 🔐 Secrets (环境特定)
  • ingress.yaml - 🌐 Ingress (域名不同)

  这些通常不应在环境之间同步。

➕ 要添加到 staging 的新配置:
  • new-worker-env-configmap.yaml
```

## 最佳实践

### 1. 始终先查看差异

```bash
# 镜像差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 配置差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only
```

### 2. 使用 Dry-run

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front --dry-run
```

### 3. 选择性同步配置

不要盲目复制整个 ConfigMap：
- ✅ 审查每个键
- ✅ 只同步业务逻辑相关的配置
- ❌ 不要同步环境特定的值

### 4. 验证后再推送

```bash
# 验证 kustomization
kubectl kustomize kubernetes/overlays/aws-staging > /tmp/staging.yaml

# 查看 git diff
git diff kubernetes/overlays/aws-staging/

# 确认后推送
git push
```

### 5. 监控部署

```bash
# 查看 ArgoCD 状态
argocd app get simplex-aws-staging
argocd app wait simplex-aws-staging --health
```

## 故障排除

### 问题 1：脚本报错 "无法找到 simplex-gitops 仓库根目录"

**解决方案：**
```bash
cd /path/to/simplex-gitops
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py
```

### 问题 2：配置同步后服务无法启动

**原因：** 可能同步了环境特定的配置值

**解决方案：**
1. 检查服务日志查看错误
2. 对比 CI 和 Staging 的配置差异
3. 恢复环境特定的值

### 问题 3：新资源未出现在 ArgoCD

**原因：** 未添加到 kustomization.yaml

**解决方案：**
```bash
vim kubernetes/overlays/aws-staging/kustomization.yaml

# 在 patches 部分添加：
patches:
  - path: patches/new-config.yaml
```

## 总结

### 镜像同步（主要用例）

✅ **自动化：** 使用 `sync_images.py`
✅ **安全：** 支持 dry-run
✅ **灵活：** 可选择性同步

### 配置同步（需要手动）

⚠️ **谨慎操作：** 使用 `compare_configs.py` 识别差异
⚠️ **手动审查：** 确定哪些配置应该同步
⚠️ **选择性同步：** 不要复制整个文件

### 关键原则

1. **镜像标签** → 自动同步（使用脚本）
2. **业务配置** → 选择性手动同步
3. **环境配置** → 永不同步
4. **Secrets** → 永不同步
