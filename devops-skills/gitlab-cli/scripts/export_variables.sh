#!/bin/bash
# 导出项目或 group 的变量到文件
# 用法: ./export_variables.sh [--group GROUP_NAME] [--repo REPO_PATH] [output_file]
# 示例:
#   ./export_variables.sh --repo simplexai/api vars.env
#   ./export_variables.sh --group simplexai group_vars.env

set -e

GROUP=""
REPO=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --group|-g)
            GROUP="$2"
            shift 2
            ;;
        --repo|-r)
            REPO="$2"
            shift 2
            ;;
        *)
            OUTPUT="$1"
            shift
            ;;
    esac
done

if [ -z "$OUTPUT" ]; then
    OUTPUT="variables_$(date +%Y%m%d_%H%M%S).env"
fi

echo "📦 导出变量到 $OUTPUT"

if [ -n "$GROUP" ]; then
    echo "# Group: $GROUP" > "$OUTPUT"
    echo "# Exported: $(date)" >> "$OUTPUT"
    glab variable export --group "$GROUP" >> "$OUTPUT"
elif [ -n "$REPO" ]; then
    echo "# Repo: $REPO" > "$OUTPUT"
    echo "# Exported: $(date)" >> "$OUTPUT"
    glab variable export -R "$REPO" >> "$OUTPUT"
else
    echo "# Current Repo" > "$OUTPUT"
    echo "# Exported: $(date)" >> "$OUTPUT"
    glab variable export >> "$OUTPUT"
fi

echo "✅ 已导出到 $OUTPUT"
echo "⚠️ 文件可能包含敏感信息，请妥善保管。"
