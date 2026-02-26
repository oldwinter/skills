# Justfile 语法参考手册

本文档提供 Justfile 语法的完整参考。

## 基础语法

### 简单 Recipe

```just
# 注释：描述这个 recipe 的用途
recipe-name:
    echo "Hello, World!"
```

### 带参数的 Recipe

```just
# 构建指定目标
build target:
    cargo build --target {{target}}

# 带默认值的参数
greet name="World":
    echo "Hello, {{name}}!"

# 可变参数
test *args:
    cargo test {{args}}

# 带 + 的参数（至少一个）
deploy +servers:
    for server in {{servers}}; do ssh $server "deploy"; done
```

### 依赖关系

```just
# 简单依赖
all: build test

build:
    cargo build

test:
    cargo test

# 带参数的依赖
push: (build "release")

build mode="debug":
    cargo build --{{mode}}
```

## 变量与设置

### 变量定义

```just
# 简单变量
version := "1.0.0"
name := "myapp"

# 环境变量
export DATABASE_URL := "postgres://localhost/mydb"

# 从命令获取
git_hash := `git rev-parse --short HEAD`
date := `date +%Y-%m-%d`

# 条件变量
mode := if env("CI") == "true" { "release" } else { "debug" }
```

### 全局设置

```just
# 设置默认 shell
set shell := ["bash", "-cu"]

# 加载 .env 文件
set dotenv-load

# 导出所有变量到环境
set export

# 允许位置参数
set positional-arguments

# 错误时退出
set fallback := false

# Windows 兼容
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
```

## 高级特性

### 条件执行

```just
# if 表达式
foo := if "2" == "2" { "yes" } else { "no" }

# 条件 recipe
install:
    {{ if os() == "macos" { "brew install" } else { "apt install" } }} mypackage
```

### 内置函数

```just
# 系统信息
current_os := os()                    # "macos", "linux", "windows"
current_arch := arch()                # "x86_64", "aarch64"
home := env("HOME")                   # 环境变量
num_cpus := num_cpus()                # CPU 核心数

# 路径操作
dir := justfile_directory()           # justfile 所在目录
parent := parent_directory(dir)       # 父目录
file := file_name("/path/to/file")    # "file"
stem := file_stem("/path/to/file.txt") # "file"
ext := extension("/path/to/file.txt")  # "txt"

# 字符串操作
upper := uppercase("hello")           # "HELLO"
lower := lowercase("HELLO")           # "hello"
trimmed := trim("  hello  ")          # "hello"
replaced := replace("hello", "l", "L") # "heLLo"

# 路径连接
full_path := join(justfile_directory(), "src", "main.rs")

# UUID 生成
id := uuid()

# SHA256 哈希
hash := sha256("content")
file_hash := sha256_file("path/to/file")
```

### 私有 Recipe

```just
# 以 _ 开头的 recipe 不会在 just --list 中显示
_helper:
    echo "This is a helper"

public: _helper
    echo "This uses the helper"
```

### 文档注释

```just
# 这是普通注释，不会显示在 --list 中

## 这是文档注释，会显示在 --list 中
build:
    cargo build

# [doc('自定义文档说明')]
[doc('构建生产版本')]
build-prod:
    cargo build --release
```

### 别名

```just
alias b := build
alias t := test

build:
    cargo build

test:
    cargo test
```

### 分组

```just
# [group('development')]
[group('development')]
dev:
    cargo run

[group('development')]
watch:
    cargo watch

[group('testing')]
test:
    cargo test

[group('testing')]
lint:
    cargo clippy
```

### 跨平台

```just
[linux]
install:
    apt install mypackage

[macos]
install:
    brew install mypackage

[windows]
install:
    choco install mypackage
```

### 确认提示

```just
[confirm]
deploy:
    echo "Deploying to production..."

[confirm("Are you sure you want to delete all data?")]
clean-db:
    rm -rf data/
```

### 工作目录

```just
[working-directory("frontend")]
build-frontend:
    npm run build
```

### 无回显执行

```just
quiet-recipe:
    @echo "This line is not echoed before execution"

# 整个 recipe 静默
[no-cd]
silent:
    @echo "Silent mode"
```

### 脚本模式

```just
# 多行脚本（每行单独执行）
multi-line:
    line1
    line2
    line3

# 合并为单个脚本执行
[script]
as-script:
    #!/usr/bin/env bash
    set -euo pipefail
    for i in 1 2 3; do
        echo $i
    done

# Python 脚本
[script("python3")]
python-script:
    import sys
    print(f"Python version: {sys.version}")
```

### 模块化

```just
# 导入其他 justfile
import "other.just"

# 带前缀导入
mod frontend "frontend/justfile"

# 使用: just frontend::build
```

## 常用模式

### Docker 操作

```just
set dotenv-load

image := "myapp"
tag := `git rev-parse --short HEAD`

# 构建镜像
build:
    docker build -t {{image}}:{{tag}} .

# 运行容器
run *args:
    docker run --rm -it {{image}}:{{tag}} {{args}}

# 推送镜像
push: build
    docker push {{image}}:{{tag}}

# 进入容器
shell:
    docker run --rm -it {{image}}:{{tag}} /bin/sh
```

### Kubernetes 操作

```just
namespace := "default"
context := "minikube"

# 应用配置
apply:
    kubectl --context={{context}} -n {{namespace}} apply -f k8s/

# 查看 pods
pods:
    kubectl --context={{context}} -n {{namespace}} get pods

# 查看日志
logs pod:
    kubectl --context={{context}} -n {{namespace}} logs -f {{pod}}

# 进入 pod
exec pod:
    kubectl --context={{context}} -n {{namespace}} exec -it {{pod}} -- /bin/sh
```

### 数据库操作

```just
set dotenv-load

# 数据库迁移
migrate:
    alembic upgrade head

# 回滚迁移
rollback:
    alembic downgrade -1

# 创建迁移
migration name:
    alembic revision --autogenerate -m "{{name}}"

# 数据库 shell
db-shell:
    psql $DATABASE_URL
```

### 测试与 CI

```just
# 运行所有检查
ci: lint test build

# 代码检查
lint:
    cargo clippy -- -D warnings
    cargo fmt --check

# 运行测试
test *args:
    cargo test {{args}}

# 测试并生成覆盖率
coverage:
    cargo tarpaulin --out Html

# 构建
build:
    cargo build --release
```

## 命令行使用

```bash
# 列出所有 recipes
just --list
just -l

# 运行默认 recipe
just

# 运行指定 recipe
just build

# 带参数运行
just build release

# 干运行（只打印命令）
just --dry-run build
just -n build

# 显示 recipe 内容
just --show build

# 格式化 justfile
just --fmt

# 检查格式
just --fmt --check

# 选择 recipe（交互式）
just --choose

# 使用其他 justfile
just -f other.just build

# 设置变量
just version=2.0.0 build

# 查看变量
just --evaluate

# 导出为 JSON
just --dump --dump-format json
```

## Makefile 到 Justfile 转换对照

| Makefile | Justfile |
|----------|----------|
| `.PHONY: target` | 不需要，默认就是 phony |
| `$(VAR)` | `{{var}}` |
| `$@` | 使用 recipe 名称 |
| `$<` | 使用具体文件名 |
| `VAR ?= default` | `var := env("VAR", "default")` |
| `export VAR` | `export VAR := "value"` |
| `include file.mk` | `import "file.just"` |
| `ifeq ($(OS),Linux)` | `[linux]` 属性 |
| `$(shell cmd)` | `` `cmd` `` |
| `@echo` | `@echo` (相同) |
| `.SILENT:` | `[no-exit-message]` 或 `@` |
