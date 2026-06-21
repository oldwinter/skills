# 项目模板 Justfile 集合

本文档提供各类项目的 Justfile 模板。

## Python 项目模板

```just
# Python 项目 Justfile
set dotenv-load
set shell := ["bash", "-cu"]

# 项目信息
project := "myproject"
python := "python3"

# 默认任务
default: dev

# === 开发 ===

# 启动开发服务器
dev:
    {{python}} -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 运行脚本
run *args:
    {{python}} {{args}}

# 进入 Python shell
shell:
    {{python}} -i

# === 依赖管理 ===

# 安装依赖 (使用 uv)
install:
    uv pip install -r requirements.txt

# 安装开发依赖
install-dev:
    uv pip install -r requirements-dev.txt

# 更新依赖
update:
    uv pip compile requirements.in -o requirements.txt
    uv pip sync requirements.txt

# 添加依赖
add package:
    echo "{{package}}" >> requirements.in
    uv pip compile requirements.in -o requirements.txt

# === 测试 ===

# 运行测试
test *args:
    pytest {{args}}

# 测试并生成覆盖率报告
coverage:
    pytest --cov={{project}} --cov-report=html
    @echo "打开 htmlcov/index.html 查看报告"

# 运行单个测试文件
test-file file:
    pytest {{file}} -v

# === 代码质量 ===

# 代码格式化
fmt:
    ruff format .
    ruff check --fix .

# 代码检查
lint:
    ruff check .
    mypy {{project}}

# 全部检查
check: fmt lint test

# === 数据库 ===

# 数据库迁移
migrate:
    alembic upgrade head

# 创建迁移
migration name:
    alembic revision --autogenerate -m "{{name}}"

# 回滚迁移
rollback:
    alembic downgrade -1

# === Docker ===

# 构建镜像
docker-build:
    docker build -t {{project}}:latest .

# 运行容器
docker-run:
    docker run --rm -it -p 8000:8000 {{project}}:latest

# === 清理 ===

# 清理缓存
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    rm -rf .coverage htmlcov dist build *.egg-info
```

## Node.js 项目模板

```just
# Node.js 项目 Justfile
set dotenv-load
set shell := ["bash", "-cu"]

# 包管理器 (npm, yarn, pnpm)
pm := "npm"

# 默认任务
default: dev

# === 开发 ===

# 启动开发服务器
dev:
    {{pm}} run dev

# 启动生产服务器
start:
    {{pm}} run start

# 监听模式
watch:
    {{pm}} run watch

# === 构建 ===

# 构建项目
build:
    {{pm}} run build

# 构建生产版本
build-prod:
    NODE_ENV=production {{pm}} run build

# === 依赖 ===

# 安装依赖
install:
    {{pm}} install

# 添加依赖
add *packages:
    {{pm}} install {{packages}}

# 添加开发依赖
add-dev *packages:
    {{pm}} install -D {{packages}}

# 更新依赖
update:
    {{pm}} update

# 检查过期依赖
outdated:
    {{pm}} outdated

# === 测试 ===

# 运行测试
test:
    {{pm}} run test

# 测试监听模式
test-watch:
    {{pm}} run test -- --watch

# 测试覆盖率
coverage:
    {{pm}} run test -- --coverage

# === 代码质量 ===

# 代码检查
lint:
    {{pm}} run lint

# 代码格式化
fmt:
    {{pm}} run format

# 类型检查
typecheck:
    {{pm}} run typecheck

# 全部检查
check: lint typecheck test

# === 清理 ===

# 清理
clean:
    rm -rf node_modules dist build .cache .next .nuxt

# 重新安装
reinstall: clean install
```

## Go 项目模板

```just
# Go 项目 Justfile
set dotenv-load
set shell := ["bash", "-cu"]

# 项目信息
project := "myapp"
main := "./cmd/{{project}}"

# 构建信息
version := `git describe --tags --always --dirty 2>/dev/null || echo "dev"`
commit := `git rev-parse --short HEAD 2>/dev/null || echo "unknown"`
date := `date -u +"%Y-%m-%dT%H:%M:%SZ"`
ldflags := "-s -w -X main.version={{version}} -X main.commit={{commit}} -X main.date={{date}}"

# 默认任务
default: run

# === 开发 ===

# 运行项目
run *args:
    go run {{main}} {{args}}

# 监听模式 (需要 air)
watch:
    air

# === 构建 ===

# 构建
build:
    go build -ldflags "{{ldflags}}" -o bin/{{project}} {{main}}

# 构建所有平台
build-all:
    GOOS=linux GOARCH=amd64 go build -ldflags "{{ldflags}}" -o bin/{{project}}-linux-amd64 {{main}}
    GOOS=darwin GOARCH=amd64 go build -ldflags "{{ldflags}}" -o bin/{{project}}-darwin-amd64 {{main}}
    GOOS=darwin GOARCH=arm64 go build -ldflags "{{ldflags}}" -o bin/{{project}}-darwin-arm64 {{main}}
    GOOS=windows GOARCH=amd64 go build -ldflags "{{ldflags}}" -o bin/{{project}}-windows-amd64.exe {{main}}

# 安装
install:
    go install -ldflags "{{ldflags}}" {{main}}

# === 依赖 ===

# 整理依赖
tidy:
    go mod tidy

# 下载依赖
download:
    go mod download

# 更新依赖
update:
    go get -u ./...
    go mod tidy

# === 测试 ===

# 运行测试
test *args:
    go test -v ./... {{args}}

# 测试覆盖率
coverage:
    go test -coverprofile=coverage.out ./...
    go tool cover -html=coverage.out -o coverage.html

# 基准测试
bench:
    go test -bench=. -benchmem ./...

# === 代码质量 ===

# 代码格式化
fmt:
    go fmt ./...
    goimports -w .

# 代码检查
lint:
    golangci-lint run

# 静态分析
vet:
    go vet ./...

# 全部检查
check: fmt vet lint test

# === 生成 ===

# 生成代码
generate:
    go generate ./...

# === 清理 ===

# 清理
clean:
    rm -rf bin/ coverage.out coverage.html
    go clean -cache
```

## DevOps/运维模板

```just
# DevOps 运维 Justfile
set dotenv-load
set shell := ["bash", "-cu"]

# 环境配置
env := env("ENV", "dev")
namespace := env("NAMESPACE", "default")

# Kubernetes 上下文
k := if env == "prod" { "kubectl --context=prod" } else { "kubectl --context=dev" }

# === Docker ===

# 构建镜像
build tag="latest":
    docker build -t myapp:{{tag}} .

# 推送镜像
push tag="latest":
    docker push myapp:{{tag}}

# 构建并推送
release tag: (build tag) (push tag)

# === Kubernetes ===

# 应用配置
apply:
    {{k}} apply -k overlays/{{env}}

# 查看 pods
pods:
    {{k}} -n {{namespace}} get pods

# 查看日志
logs pod *args:
    {{k}} -n {{namespace}} logs -f {{pod}} {{args}}

# 进入 pod
exec pod:
    {{k}} -n {{namespace}} exec -it {{pod}} -- /bin/sh

# 重启部署
restart deployment:
    {{k}} -n {{namespace}} rollout restart deployment/{{deployment}}

# 查看部署状态
status:
    {{k}} -n {{namespace}} get deploy,pod,svc

# 端口转发
port-forward svc port:
    {{k}} -n {{namespace}} port-forward svc/{{svc}} {{port}}

# === Terraform ===

# 初始化
tf-init:
    cd terraform && terraform init

# 计划
tf-plan:
    cd terraform && terraform plan -var-file={{env}}.tfvars

# 应用
tf-apply:
    cd terraform && terraform apply -var-file={{env}}.tfvars

# 销毁
[confirm("确定要销毁基础设施吗?")]
tf-destroy:
    cd terraform && terraform destroy -var-file={{env}}.tfvars

# === 监控 ===

# 查看资源使用
top:
    {{k}} top nodes
    {{k}} top pods -n {{namespace}}

# 查看事件
events:
    {{k}} -n {{namespace}} get events --sort-by='.lastTimestamp'

# === SSH ===

# SSH 到服务器
ssh host:
    ssh -o StrictHostKeyChecking=no {{host}}

# 批量执行命令
ssh-cmd host cmd:
    ssh {{host}} "{{cmd}}"
```

## 通用开发模板

```just
# 通用开发 Justfile
set dotenv-load
set shell := ["bash", "-cu"]

# 项目信息
project := file_stem(justfile_directory())
version := `git describe --tags --always 2>/dev/null || echo "0.0.0"`

# 默认任务
default:
    @just --list

# === 常用 ===

# 启动开发环境
dev:
    @echo "TODO: 配置开发启动命令"

# 构建项目
build:
    @echo "TODO: 配置构建命令"

# 运行测试
test:
    @echo "TODO: 配置测试命令"

# === Git ===

# 查看状态
status:
    git status -sb

# 快速提交
commit msg:
    git add -A
    git commit -m "{{msg}}"

# 提交并推送
push msg: (commit msg)
    git push

# 拉取最新
pull:
    git pull --rebase

# 创建分支
branch name:
    git checkout -b {{name}}

# === 文档 ===

# 生成文档
docs:
    @echo "TODO: 配置文档生成命令"

# 启动文档服务器
docs-serve:
    @echo "TODO: 配置文档服务器命令"

# === 辅助 ===

# 打开项目目录
open:
    {{ if os() == "macos" { "open ." } else { "xdg-open ." } }}

# 统计代码行数
loc:
    tokei . || cloc . || find . -name "*.py" -o -name "*.js" -o -name "*.go" | xargs wc -l

# 查找大文件
large-files:
    find . -type f -size +1M -exec ls -lh {} \; | sort -k5 -h

# 清理 .DS_Store
clean-ds:
    find . -name ".DS_Store" -delete

# 显示项目信息
info:
    @echo "项目: {{project}}"
    @echo "版本: {{version}}"
    @echo "目录: {{justfile_directory()}}"
    @echo "系统: {{os()}} / {{arch()}}"
```

## 数据科学/ML 模板

```just
# 数据科学项目 Justfile
set dotenv-load
set shell := ["bash", "-cu"]

# Python 环境
python := ".venv/bin/python"
pip := ".venv/bin/pip"

# 默认任务
default: notebook

# === 环境 ===

# 创建虚拟环境
venv:
    python3 -m venv .venv
    {{pip}} install -U pip

# 安装依赖
install: venv
    {{pip}} install -r requirements.txt

# === Jupyter ===

# 启动 Jupyter Lab
notebook:
    {{python}} -m jupyter lab

# 启动 Jupyter Notebook
nb:
    {{python}} -m jupyter notebook

# 转换 notebook 为脚本
convert file:
    {{python}} -m jupyter nbconvert --to script {{file}}

# === 数据 ===

# 下载数据
download:
    @echo "TODO: 配置数据下载命令"

# 数据预处理
preprocess:
    {{python}} scripts/preprocess.py

# === 训练 ===

# 训练模型
train *args:
    {{python}} train.py {{args}}

# 评估模型
eval:
    {{python}} evaluate.py

# === MLflow ===

# 启动 MLflow UI
mlflow:
    {{python}} -m mlflow ui --port 5000

# === 清理 ===

# 清理
clean:
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -delete
    rm -rf .ipynb_checkpoints
```
