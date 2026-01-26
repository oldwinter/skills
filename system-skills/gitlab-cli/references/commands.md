# GitLab CLI (glab) 命令速查手册

本文档提供 glab CLI 常用命令的快速参考。

## 环境配置

- **GitLab 服务器**: `192.168.10.117:6001`
- **协议**: SSH (Git 操作) / HTTP (API 调用)
- **SSH 端口**: 2222

## 仓库管理 (repo)

### 列出项目
```bash
# 列出所有项目
glab repo list

# 列出指定数量
glab repo list --per-page 20

# 搜索项目
glab repo search "keyword"
```

### 创建项目
```bash
# 在当前用户下创建
glab repo create my-project

# 在指定 group 下创建
glab repo create my-project --group simplexai

# 创建私有项目
glab repo create my-project --private

# 创建并初始化 README
glab repo create my-project --readme
```

### 查看项目
```bash
# 查看当前项目信息
glab repo view

# 查看指定项目
glab repo view simplexai/my-project

# 在浏览器中打开
glab repo view --web
```

### 克隆项目
```bash
# 克隆单个项目
glab repo clone simplexai/my-project

# 克隆整个 group 的所有项目
glab repo clone -g simplexai
```

### 删除项目
```bash
# 删除项目 (需确认)
glab repo delete my-project

# 强制删除 (跳过确认)
glab repo delete my-project --yes
```

### 项目成员管理
```bash
# 列出项目成员
glab repo members list

# 添加成员 (access level: 10=Guest, 20=Reporter, 30=Developer, 40=Maintainer, 50=Owner)
glab repo members add --user username --access-level 30

# 移除成员
glab repo members delete username
```

## CI/CD 管理 (ci)

### Pipeline 操作
```bash
# 查看当前分支 pipeline 状态
glab ci status

# 列出所有 pipeline
glab ci list

# 查看 pipeline 详情 (交互式)
glab ci view

# 获取 pipeline JSON
glab ci get

# 运行新 pipeline
glab ci run

# 在指定分支运行
glab ci run --branch main

# 带变量运行
glab ci run --variables "KEY1:value1" --variables "KEY2:value2"

# 取消运行中的 pipeline
glab ci cancel

# 删除 pipeline
glab ci delete <pipeline-id>

# 重试失败的 job
glab ci retry <job-id>
```

### Job 操作
```bash
# 列出 pipeline 的所有 jobs
glab ci trace

# 查看特定 job 的日志 (实时)
glab ci trace <job-id>

# 触发手动 job
glab ci trigger <job-id>

# 下载 artifacts
glab ci artifact <ref> <job-name>
```

### CI 配置验证
```bash
# 验证 .gitlab-ci.yml 语法
glab ci lint

# 验证指定文件
glab ci lint --path path/to/.gitlab-ci.yml
```

## Merge Request 管理 (mr)

### 创建 MR
```bash
# 交互式创建
glab mr create

# 自动填充标题和描述
glab mr create --fill

# 指定目标分支
glab mr create --target-branch main

# 创建草稿 MR
glab mr create --draft

# 完整示例
glab mr create --title "feat: add new feature" --description "Description here" --target-branch main --label "feature"
```

### 列出 MR
```bash
# 列出所有打开的 MR
glab mr list

# 列出所有状态
glab mr list --state all

# 列出已合并的
glab mr list --state merged

# 按作者筛选
glab mr list --author username

# 按标签筛选
glab mr list --label "bug,urgent"
```

### 查看 MR
```bash
# 查看 MR 详情
glab mr view <mr-id>

# 在浏览器打开
glab mr view <mr-id> --web

# 查看 MR diff
glab mr diff <mr-id>
```

### 审核与合并
```bash
# 批准 MR
glab mr approve <mr-id>

# 撤销批准
glab mr revoke <mr-id>

# 合并 MR
glab mr merge <mr-id>

# 合并并删除源分支
glab mr merge <mr-id> --remove-source-branch

# Squash 合并
glab mr merge <mr-id> --squash

# Rebase 后合并
glab mr merge <mr-id> --rebase
```

### MR 操作
```bash
# 添加评论
glab mr note <mr-id> -m "Your comment"

# 关闭 MR
glab mr close <mr-id>

# 重新打开
glab mr reopen <mr-id>

# 更新 MR
glab mr update <mr-id> --title "New title" --description "New desc"

# Checkout MR 到本地
glab mr checkout <mr-id>

# Rebase MR
glab mr rebase <mr-id>
```

## Issue 管理 (issue)

### 创建 Issue
```bash
# 交互式创建
glab issue create

# 指定标题和描述
glab issue create --title "Bug: something broken" --description "Details here"

# 带标签
glab issue create --title "Feature request" --label "enhancement,priority:high"

# 创建机密 issue
glab issue create --title "Security issue" --confidential
```

### 列出 Issue
```bash
# 列出打开的 issue
glab issue list

# 列出所有状态
glab issue list --state all

# 按标签筛选
glab issue list --label "bug"

# 按指派人筛选
glab issue list --assignee username
```

### Issue 操作
```bash
# 查看 issue
glab issue view <issue-id>

# 在浏览器打开
glab issue view <issue-id> --web

# 添加评论
glab issue note <issue-id> -m "Comment here"

# 关闭 issue
glab issue close <issue-id>

# 重新打开
glab issue reopen <issue-id>

# 更新 issue
glab issue update <issue-id> --title "New title" --add-label "in-progress"
```

## 变量管理 (variable)

### 项目变量
```bash
# 列出项目变量
glab variable list

# 获取变量值
glab variable get MY_VAR

# 设置变量
glab variable set MY_VAR "my_value"

# 设置受保护变量 (仅受保护分支可用)
glab variable set MY_VAR "value" --protected

# 设置 masked 变量 (日志中隐藏)
glab variable set MY_SECRET "secret" --masked

# 更新变量
glab variable update MY_VAR "new_value"

# 删除变量
glab variable delete MY_VAR

# 导出所有变量
glab variable export
```

### Group 变量
```bash
# 列出 group 变量
glab variable list --group simplexai

# 设置 group 变量
glab variable set MY_VAR "value" --group simplexai
```

## Release 管理 (release)

```bash
# 列出 releases
glab release list

# 创建 release
glab release create v1.0.0 --notes "Release notes here"

# 从文件读取 release notes
glab release create v1.0.0 --notes-file CHANGELOG.md

# 上传 assets
glab release create v1.0.0 --assets-links '[{"name":"binary","url":"https://..."}]'

# 查看 release
glab release view v1.0.0

# 删除 release
glab release delete v1.0.0
```

## API 直接调用 (api)

```bash
# GET 请求
glab api projects

# 获取指定项目
glab api projects/simplexai%2Fmy-project

# POST 请求
glab api projects --method POST --field name=new-project

# 带参数的 GET
glab api projects --field per_page=100

# 分页获取所有结果
glab api projects --paginate
```

## 其他常用命令

### 认证管理
```bash
# 查看认证状态
glab auth status

# 重新登录
glab auth login --hostname 192.168.10.117:6001

# 登出
glab auth logout
```

### 配置管理
```bash
# 查看配置
glab config list

# 设置默认编辑器
glab config set editor vim

# 设置默认 git 协议
glab config set git_protocol ssh
```

### Schedule 管理
```bash
# 列出定时任务
glab schedule list

# 创建定时任务
glab schedule create --description "Daily build" --ref main --cron "0 0 * * *"

# 运行定时任务
glab schedule run <schedule-id>

# 删除定时任务
glab schedule delete <schedule-id>
```

### 用户管理
```bash
# 查看当前用户
glab user show

# 查看指定用户
glab user show username
```

## 跨项目操作

使用 `-R` 或 `--repo` 参数指定项目：

```bash
# 查看其他项目的 MR
glab mr list -R simplexai/another-project

# 在其他项目运行 pipeline
glab ci run -R simplexai/another-project

# 查看其他项目的 issues
glab issue list -R simplexai/another-project
```

## 常用组合命令示例

```bash
# 查看所有项目的最新 pipeline 状态
for repo in $(glab repo list --per-page 100 | awk '{print $1}'); do
  echo "=== $repo ===" && glab ci status -R "$repo" 2>/dev/null || echo "No pipeline"
done

# 批量触发多个项目的 pipeline
for repo in simplexai/project1 simplexai/project2; do
  glab ci run -R "$repo" --branch main
done

# 导出项目的所有变量到文件
glab variable export > variables.env
```
