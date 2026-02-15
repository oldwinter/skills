---
name: docker-kubectl-deploy
description: Build Docker images, push to a registry, and deploy/update Kubernetes workloads with kubectl (set image + rollout). Use when asked to run docker build/push, publish images, update a Deployment image, rollout restart, or “部署到K8s/更新环境/发布镜像”.
---

# Docker Kubectl Deploy

使用 `docker build` → `docker push` → `kubectl set image` 的固定流程，把新镜像发布到 Kubernetes 环境，并等待滚动更新完成。

## Quick Start
- 确认本机已配置：`docker`、已 `docker login` 对应镜像仓库；`kubectl`、已配置目标集群 `kubeconfig`
- 需要的信息：镜像仓库（不带 tag）、K8s 的 `context/namespace/deployment/container`、tag（可选）
- 优先使用脚本：`bash scripts/build_push_kubectl.sh --help`

## Workflow (推荐)
1. 选择镜像引用：`<image-repo>:<tag>`（tag 默认自动生成）
2. Build：`docker build -t <image-repo>:<tag> ...`
3. Push：`docker push <image-repo>:<tag>`
4. Deploy：`kubectl set image deployment/<deployment> <container>=<image-repo>:<tag> -n <namespace>`
5. 验证：`kubectl rollout status deployment/<deployment> -n <namespace>`

## 常用命令（不使用脚本时）
```bash
docker build -t IMAGE_REPO:TAG -f Dockerfile .
docker push IMAGE_REPO:TAG

kubectl -n NAMESPACE set image deployment/DEPLOYMENT CONTAINER=IMAGE_REPO:TAG
kubectl -n NAMESPACE rollout status deployment/DEPLOYMENT --timeout=120s
```

## Safety Checks
- 部署前先核对目标环境：`kubectl config current-context`、`kubectl -n <ns> get deploy <name>`
- 生产环境变更：先向用户确认 `kube-context/namespace/image/tag`，再执行

## Scripts
### `scripts/build_push_kubectl.sh`
Build 镜像、push 到仓库、然后用 `kubectl set image` 更新 Deployment 并等待 rollout 完成。
