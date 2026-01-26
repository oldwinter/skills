#!/bin/bash
# 查看多个项目的 MR 概览
# 用法: ./mr_overview.sh [--state STATE] [project1] [project2] ...
# 示例: ./mr_overview.sh --state opened simplexai/api simplexai/front

set -e

STATE="opened"
PROJECTS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --state|-s)
            STATE="$2"
            shift 2
            ;;
        *)
            PROJECTS+=("$1")
            shift
            ;;
    esac
done

if [ ${#PROJECTS[@]} -eq 0 ]; then
    # 获取所有项目
    mapfile -t PROJECTS < <(glab repo list --per-page 100 2>/dev/null | awk '{print $1}')
fi

echo "📋 Merge Request 概览 (状态: $STATE)"
echo "================================"

TOTAL=0
for repo in "${PROJECTS[@]}"; do
    MRS=$(glab mr list -R "$repo" --state "$STATE" 2>/dev/null | grep -c "^!" || echo "0")
    if [ "$MRS" != "0" ]; then
        echo "$repo: $MRS 个 MR"
        TOTAL=$((TOTAL + MRS))
    fi
done

echo "================================"
echo "总计: $TOTAL 个 $STATE 状态的 MR"
