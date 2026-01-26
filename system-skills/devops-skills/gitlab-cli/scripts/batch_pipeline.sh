#!/bin/bash
# 批量触发多个项目的 Pipeline
# 用法: ./batch_pipeline.sh [branch] [project1] [project2] ...
# 示例: ./batch_pipeline.sh main simplexai/api simplexai/front

set -e

BRANCH="${1:-main}"
shift

if [ $# -eq 0 ]; then
    echo "用法: $0 [branch] [project1] [project2] ..."
    echo "示例: $0 main simplexai/api simplexai/front"
    exit 1
fi

echo "🚀 批量触发 Pipeline (分支: $BRANCH)"
echo "================================"

for repo in "$@"; do
    echo -n "触发 $repo ... "
    if glab ci run -R "$repo" --branch "$BRANCH" 2>/dev/null; then
        echo "✅ 成功"
    else
        echo "❌ 失败"
    fi
done

echo "================================"
echo "✅ 完成"
