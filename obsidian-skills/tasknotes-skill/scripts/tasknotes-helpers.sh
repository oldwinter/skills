#!/bin/bash
# TaskNotes helper scripts for common operations

# Find task ID by search query (returns first match)
# Note: tn search does NOT support --json, parse output manually
tn-find() {
    local query="$1"
    if [ -z "$query" ]; then
        echo "Usage: tn-find <query>" >&2
        return 1
    fi
    # Parse task ID from search output
    tn search "$query" 2>/dev/null | grep -oP 'ID: \K.*\.md' | head -1
}

# Find or create task - returns task ID
# Usage: tn-find-or-create "task title" [--priority high] [--tags tag1,tag2]
tn-find-or-create() {
    local title="$1"
    shift
    local priority="" tags=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --priority)
                priority="$2"
                shift 2
                ;;
            --tags)
                tags="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1" >&2
                return 1
                ;;
        esac
    done

    # Search for existing task
    local task_id=$(tn-find "$title")

    if [ -n "$task_id" ]; then
        echo "Found existing task: $task_id"
        echo "$task_id"
        return 0
    fi

    # Build creation command
    local cmd="tn \"$title\""
    if [ -n "$priority" ]; then
        cmd="$cmd high priority"
    fi
    if [ -n "$tags" ]; then
        cmd="$cmd #${tags//,/#}"
    fi

    # Create new task (tn create does NOT support --json)
    echo "Creating new task: $title"
    eval "$cmd" >/dev/null 2>&1
    # Get the task ID by searching for it
    task_id=$(tn-find "$title")

    if [ -n "$task_id" ]; then
        echo "Created task: $task_id"
        echo "$task_id"
    else
        echo "Failed to create task" >&2
        return 1
    fi
}

# Update task status
tn-status() {
    local task_id="$1"
    local status="$2"
    if [ -z "$task_id" ] || [ -z "$status" ]; then
        echo "Usage: tn-status <taskId> <status>" >&2
        return 1
    fi
    tn update "$task_id" --status "$status"
}

# Start timer on task
tn-timer-start() {
    local task_id="$1"
    if [ -z "$task_id" ]; then
        echo "Usage: tn-timer-start <taskId>" >&2
        return 1
    fi
    tn timer start --task "$task_id"
}

# List today's tasks with details
tn-today() {
    tn list --today --json 2>/dev/null | jq -r '.data.tasks[] | "\(.id) | \(.status) | \(.priority // "-") | \(.title)"'
}

# Quick complete task by title search
tn-quick-complete() {
    local query="$1"
    if [ -z "$query" ]; then
        echo "Usage: tn-quick-complete <query>" >&2
        return 1
    fi
    local task_id=$(tn-find "$query")
    if [ -n "$task_id" ]; then
        tn complete "$task_id"
    else
        echo "Task not found: $query" >&2
        return 1
    fi
}

# Export task list to JSON for scripting
tn-export() {
    local filter="${1:-}"
    local output_file="${2:-}"

    if [ -n "$filter" ]; then
        tn list --filter "$filter" --json > "$output_file"
    else
        tn list --json > "$output_file"
    fi
}
