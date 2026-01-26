#!/bin/bash
# 查看多个项目的 Pipeline 状态
# 用法: ./pipeline_status.sh [project1] [project2] ...
# 无参数时查看所有项目

set -e

if [ $# -eq 0 ]; then
    # 获取所有项目
    PROJECTS=$(glab repo list --per-page 100 2>/dev/null | awk '{print $1}')
else
    PROJECTS="$@"
fi

echo "📊 Pipeline 状态概览"
echo "================================"

for repo in $PROJECTS; do
    echo -n "$repo: "
    STATUS=$(glab ci status -R "$repo" 2>/dev/null | head -1 || echo "无 Pipeline")
    case "$STATUS" in
        *success*|*passed*) echo "✅ $STATUS" ;;
        *failed*) echo "❌ $STATUS" ;;
        *running*) echo "🔄 $STATUS" ;;
        *pending*) echo "⏳ $STATUS" ;;
        *canceled*) echo "⛔ $STATUS" ;;
        *) echo "➖ $STATUS" ;;
    esac
done

echo "================================"
