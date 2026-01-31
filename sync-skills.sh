#!/bin/bash

# Bidirectional Skills Sync Script
# Syncs skills between this repository and Claude Code's plugin system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_PLUGINS_DIR="$HOME/.claude/plugins/marketplaces"
USER_PLUGIN_NAME="user-skills"
USER_PLUGIN_DIR="$CLAUDE_PLUGINS_DIR/$USER_PLUGIN_NAME"

# Skill categories in the repository
SKILL_CATEGORIES=(
    "coding-common-skills"
    "devops-skills"
    "obsidian-skills"
    "system-skills"
    "writing-skills"
)

echo -e "${BLUE}=== Claude Skills Bidirectional Sync ===${NC}"
echo -e "Repository: ${GREEN}$REPO_ROOT${NC}"
echo -e "Plugin Dir: ${GREEN}$USER_PLUGIN_DIR${NC}"
echo ""

# Function to create user plugin structure if it doesn't exist
create_user_plugin() {
    if [ ! -d "$USER_PLUGIN_DIR" ]; then
        echo -e "${YELLOW}Creating user plugin directory...${NC}"
        mkdir -p "$USER_PLUGIN_DIR/.claude-plugin"

        # Create plugin.json
        cat > "$USER_PLUGIN_DIR/.claude-plugin/plugin.json" <<EOF
{
  "name": "user-skills",
  "version": "1.0.0",
  "description": "User custom skills synced from repository",
  "author": "User",
  "skills": []
}
EOF
        echo -e "${GREEN}✓ Created user plugin structure${NC}"
    fi
}

# Function to sync from repo to Claude
sync_to_claude() {
    echo -e "${BLUE}Syncing from repository to Claude...${NC}"

    create_user_plugin

    local synced_count=0
    local updated_count=0
    local skipped_count=0

    for category in "${SKILL_CATEGORIES[@]}"; do
        local category_path="$REPO_ROOT/$category"

        if [ ! -d "$category_path" ]; then
            echo -e "${YELLOW}⚠ Category not found: $category${NC}"
            continue
        fi

        # Find all SKILL.md files recursively in this category
        while IFS= read -r -d '' skill_md; do
            local skill_dir=$(dirname "$skill_md")
            local skill_name=$(basename "$skill_dir")

            # Get the relative path from category to skill
            local rel_path="${skill_dir#$category_path/}"

            # Create target directory structure preserving the hierarchy
            local target_dir="$USER_PLUGIN_DIR/plugins/$category/skills/$rel_path"
            mkdir -p "$target_dir"

            # Check if we need to sync
            local needs_sync=false
            if [ ! -f "$target_dir/SKILL.md" ]; then
                needs_sync=true
            elif ! cmp -s "$skill_md" "$target_dir/SKILL.md"; then
                needs_sync=true
                updated_count=$((updated_count + 1))
            else
                skipped_count=$((skipped_count + 1))
            fi

            if [ "$needs_sync" = true ]; then
                # Sync the entire skill directory
                rsync -a --delete "$skill_dir/" "$target_dir/"
                echo -e "${GREEN}✓${NC} Synced: $category/$rel_path"
                synced_count=$((synced_count + 1))
            fi
        done < <(find "$category_path" -name "SKILL.md" -print0)
    done

    echo ""
    echo -e "${GREEN}Sync to Claude complete:${NC}"
    echo -e "  New/Updated: $synced_count"
    echo -e "  Unchanged: $skipped_count"
}

# Function to sync from Claude to repo
sync_from_claude() {
    echo -e "${BLUE}Syncing from Claude to repository...${NC}"

    if [ ! -d "$USER_PLUGIN_DIR" ]; then
        echo -e "${YELLOW}⚠ No user plugin directory found. Nothing to sync back.${NC}"
        return
    fi

    local synced_count=0
    local updated_count=0

    # Find all skills in the user plugin
    if [ -d "$USER_PLUGIN_DIR/plugins" ]; then
        for category_dir in "$USER_PLUGIN_DIR/plugins"/*; do
            if [ ! -d "$category_dir" ]; then
                continue
            fi

            local category=$(basename "$category_dir")

            if [ -d "$category_dir/skills" ]; then
                # Find all SKILL.md files recursively
                while IFS= read -r -d '' skill_md; do
                    local skill_dir=$(dirname "$skill_md")

                    # Get the relative path from skills directory
                    local rel_path="${skill_dir#$category_dir/skills/}"

                    # Create target directory in repo preserving hierarchy
                    local target_dir="$REPO_ROOT/$category/$rel_path"
                    mkdir -p "$target_dir"

                    # Check if we need to sync
                    local needs_sync=false
                    if [ ! -f "$target_dir/SKILL.md" ]; then
                        needs_sync=true
                    elif ! cmp -s "$skill_md" "$target_dir/SKILL.md"; then
                        needs_sync=true
                        updated_count=$((updated_count + 1))
                    fi

                    if [ "$needs_sync" = true ]; then
                        # Sync the entire skill directory
                        rsync -a --delete "$skill_dir/" "$target_dir/"
                        echo -e "${GREEN}✓${NC} Synced back: $category/$rel_path"
                        synced_count=$((synced_count + 1))
                    fi
                done < <(find "$category_dir/skills" -name "SKILL.md" -print0)
            fi
        done
    fi

    echo ""
    if [ $synced_count -eq 0 ]; then
        echo -e "${GREEN}No changes to sync back to repository${NC}"
    else
        echo -e "${GREEN}Sync from Claude complete:${NC}"
        echo -e "  New/Updated: $synced_count"
    fi
}

# Function to show status
show_status() {
    echo -e "${BLUE}=== Sync Status ===${NC}"
    echo ""

    echo -e "${YELLOW}Repository Skills:${NC}"
    for category in "${SKILL_CATEGORIES[@]}"; do
        local category_path="$REPO_ROOT/$category"
        if [ -d "$category_path" ]; then
            local count=$(find "$category_path" -name "SKILL.md" | wc -l | tr -d ' ')
            echo -e "  $category: $count skills"
        fi
    done

    echo ""
    echo -e "${YELLOW}Claude Plugin Skills:${NC}"
    if [ -d "$USER_PLUGIN_DIR/plugins" ]; then
        for category_dir in "$USER_PLUGIN_DIR/plugins"/*; do
            if [ -d "$category_dir" ]; then
                local category=$(basename "$category_dir")
                local count=$(find "$category_dir" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
                echo -e "  $category: $count skills"
            fi
        done
    else
        echo -e "  ${YELLOW}No user plugin directory found${NC}"
    fi
}

# Main execution
case "${1:-both}" in
    to-claude)
        sync_to_claude
        ;;
    from-claude)
        sync_from_claude
        ;;
    both)
        sync_from_claude
        echo ""
        sync_to_claude
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {to-claude|from-claude|both|status}"
        echo ""
        echo "  to-claude    - Sync from repository to Claude"
        echo "  from-claude  - Sync from Claude to repository"
        echo "  both         - Bidirectional sync (default)"
        echo "  status       - Show sync status"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
