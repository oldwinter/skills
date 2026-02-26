---
name: warp-vibe
description: Quick modify Warp launch configuration for vibe-coding. Use when user wants to change directory or command (claude/codex) in vibe-coding config and open Warp.
---

# Warp Vibe Launch Configuration Modifier

This skill modifies the `vibe-coding.yaml` launch configuration and opens Warp.

## Usage

```
/warp-vibe [directory] [command]
```

- **directory**: Target working directory (optional, keeps original if not specified)
- **command**: Either `claude` or `codex` (optional, defaults to `claude`)

## Examples

```
/warp-vibe                              # Use original dir, claude command
/warp-vibe /path/to/project             # Set new dir, use claude
/warp-vibe /path/to/project codex       # Set new dir, use codex
/warp-vibe . claude                     # Use current dir, use claude
```

## Instructions

When this skill is invoked:

1. Parse the arguments:
   - First argument (if exists): directory path
   - Second argument (if exists): command (`claude` or `codex`)
   - If no command specified, default to `claude`
   - If directory is `.`, use current working directory
   - If no directory specified, keep the original directory from the file

2. Read the file `~/.warp/launch_configurations/vibe-coding.yaml`

3. Modify the **second pane** (index 1, the "claude code" pane) in the configuration:
   - Update `cwd` to the new directory (if specified)
   - Update `commands.exec` based on command choice:
     - `claude` → `claude`
     - `codex` → `codex --dangerously-bypass-approvals-and-sandbox -m gpt-5 -c model_reasoning_effort="high"`

4. Write the modified YAML back to the file

5. Open Warp with the launch configuration using:
   ```bash
   open "warp://launch/Vibe-coding"
   ```

6. Confirm to user what was changed and that Warp is opening.
