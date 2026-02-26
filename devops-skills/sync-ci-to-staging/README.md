# Sync CI to Staging Skill

将 Kubernetes 配置从 CI 环境同步到 Staging 环境的工具。

## 概述

这个 skill 提供了两个主要工具：

1. **镜像同步** (`sync_images.py`) - 自动同步容器镜像标签
2. **配置比较** (`compare_configs.py`) - 识别配置文件差异

## 快速开始

### 1. 查看差异

```bash
# 查看镜像标签差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 查看配置差异（仅安全可审查的）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --safe-only
```

### 2. 同步镜像

```bash
# 同步特定服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,anotherme-agent

# 同步所有服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all --dry-run
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all
```

### 3. 提交和推送

```bash
cd /path/to/simplex-gitops
git add kubernetes/overlays/aws-staging/kustomization.yaml
git commit -m "chore: 从 CI 推广到 staging"
git push
```

## 文档

- **[SKILL.md](SKILL.md)** - 完整的 skill 文档和工作流
- **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** - 快速参考指南
- **[README-CONFIG-SYNC.md](README-CONFIG-SYNC.md)** - 配置同步详细指南

## 工具

### sync_images.py

**功能：**
- 比较 CI 和 Staging 的镜像标签
- 选择性或批量同步镜像标签
- Dry-run 模式

**选项：**
- `--diff` - 显示差异
- `--images SERVICE1,SERVICE2` - 同步特定服务
- `--all` - 同步所有服务
- `--dry-run` - 只显示更改，不写入文件

### compare_configs.py

**功能：**
- 比较 ConfigMaps 和 Secrets
- 检测新增或删除的资源
- 安全性分类
- 详细的 diff 输出

**选项：**
- `--detailed` - 显示详细差异
- `--safe-only` - 只显示安全可同步的配置
- `--file FILENAME` - 比较特定文件

## 示例

### 推广单个服务

```bash
# 1. 查看差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 2. Dry-run
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front --dry-run

# 3. 应用
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front

# 4. 提交
cd /path/to/simplex-gitops
git add -A && git commit -m "chore: 推广 front 到 staging"
git push
```

### 推广所有 AI 服务

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py \
  --images anotherme-agent,anotherme-api,anotherme-search,anotherme-worker \
  --dry-run
```

### 审查配置差异

```bash
# 查看所有安全可审查的配置差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --safe-only

# 查看特定文件的详细差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py \
  --file anotherme-agent-env-configmap.yaml --detailed
```

## 安全注意事项

### ✅ 可以自动同步
- 容器镜像标签

### ⚠️ 需要手动审查
- ConfigMaps（业务逻辑配置）
- 环境变量（选择性同步）

### ❌ 永不同步
- Secrets（环境特定的敏感信息）
- Ingress（域名配置）
- 基础设施配置（gateway、router、api-cm0）

## 环境

- **源环境：** aws-ci (CI 环境)
- **目标环境：** aws-staging (Staging 环境)
- **仓库：** simplex-gitops

## 相关 Skills

- **sync-to-prod** - Staging 到 Production 的同步
- **kubectl** - Kubernetes 集群操作
- **argocd-cli** - ArgoCD 部署管理
