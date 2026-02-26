# 快速参考：CI 到 Staging 同步

## 🚀 常用命令

### 1. 查看差异

```bash
# 镜像差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff

# 配置差异
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/compare_configs.py --detailed --safe-only
```

### 2. 同步镜像

```bash
# 同步特定服务
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,anotherme-agent

# 同步所有（先 dry-run）
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all --dry-run

# 同步所有
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all
```

### 3. 提交和推送

```bash
cd /path/to/simplex-gitops
git add kubernetes/overlays/aws-staging/kustomization.yaml
git commit -m "chore: 从 CI 推广镜像到 staging"
git push
```

### 4. 验证部署

```bash
# 查看 ArgoCD 状态
argocd app get simplex-aws-staging
argocd app diff simplex-aws-staging

# 手动同步（如果需要）
argocd app sync simplex-aws-staging
```

## 📋 常见场景

### 场景 1：推广单个服务

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front
```

### 场景 2：推广前端服务

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images front,front-homepage
```

### 场景 3：推广所有 AI 服务

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --images anotherme-agent,anotherme-api,anotherme-search,anotherme-worker
```

### 场景 4：推广所有内容

```bash
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all --dry-run
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --all
```

## 🔍 故障排除

### 脚本未找到仓库

```bash
cd /path/to/simplex-gitops
python3 ~/.cursor/skills/sync-ci-to-staging/scripts/sync_images.py --diff
```

### ArgoCD 未同步

```bash
argocd app refresh simplex-aws-staging
argocd app sync simplex-aws-staging
```

## ⚠️ 注意事项

1. **始终先运行 `--diff`** 查看将要更改的内容
2. **使用 `--dry-run`** 在应用更改前验证
3. **手动审查配置差异** - 不是所有配置都应同步
4. **Staging 可以自动同步**，但建议检查 ArgoCD 设置
