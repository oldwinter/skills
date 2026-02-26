---
name: skill-review
description: |
  Skills retrospective and improvement. Use when:
  - User asks to "review", "retrospect", "summarize" or "复盘" skills
  - User wants to analyze skills issues from the conversation
  - User requests skills optimization or improvement
  - End of conversation or after significant skill usage
---

# Skills Retrospective

Review and improve skills based on conversation experience.

## When to Trigger

This skill activates when user asks for:
- "复盘 skills" / "review skills" / "总结 skills"
- "Skills 有什么问题" / "What issues with skills"
- "Improve skills" / "优化 skills"
- "Skills 需要改进的地方"

## Retrospective Workflow

### Step 1: Identify Skills Used

List all skills loaded in this conversation:
- `tasknotes-skill` - TaskNotes CLI integration
- `skill-creator` - Base skill creation guidance

### Step 2: Analyze Issues

For each skill, identify:
1. **Command failures** - What commands failed and why
2. **Missing content** - What should have been documented but wasn't
3. **Incorrect guidance** - What advice was wrong or misleading
4. **Edge cases** - What scenarios weren't covered
5. **User confusion** - Where user got confused

### Step 3: Prioritize Improvements

| Priority | Issue Type | Action |
|----------|------------|--------|
| Critical | Wrong/misleading info | Fix immediately |
| High | Missing critical info | Add to SKILL.md |
| Medium | Edge case not covered | Add to troubleshooting |
| Low | Clarity improvement | Refine wording |

### Step 4: Document Findings

Create a summary in this format:
```markdown
## Skills Review - [Date]

### [Skill Name]
**Issues Found:**
1. [Issue description] - [Root cause]
2. ...

**Improvements Made:**
1. [Change] - [Location]
2. ...

**Still Missing:**
1. [What's still needed]
```

## Common Issues to Watch For

### Command Option Mismatches
- Check `tn --help` for actual options
- `create` doesn't support `--priority`, `--tags`, etc.
- `update --add-projects` may silently fail

### Path Handling
- Chinese punctuation in paths (。) requires exact matching
- `.md` extension may or may not be required
- Use `tn list --json` to get exact IDs

### Natural Language Parsing
- `∑` symbol causes parsing issues → use `_` instead
- Project names with `-` may be misinterpreted
- Test with simple cases first

## Actionable Improvements

### Immediate Actions
1. Update SKILL.md with workaround for `update --add-projects`
2. Document project naming convention (underscore vs sum symbol)
3. Add exact ID extraction patterns

### Documentation Updates
1. Add "Gotchas" section for known issues
2. Include command output examples
3. Document batch operation risks

## Output Format

When presenting improvements:

```markdown
## Skills Review

### tasknotes-skill
| Issue | Root Cause | Fix |
|-------|------------|-----|
| `--add-projects` silent fail | API bug | Use `_` in project name during creation |
| `∑` parsing issue | Parser limitation | Use `拓扑灵犀_infra建设` instead |

### skill-creator
| Issue | Root Cause | Fix |
|-------|------------|-----|
| Missing skill-review | New requirement | Created skill-review |

## Files Modified
- `/Users/oldwinter/.claude/skills/tasknotes-skill/SKILL.md`
- `/Users/oldwinter/.claude/skills/skill-review/SKILL.md`
```

## Integration with Previous Session

If this is a continuation of a previous session:
1. Read the previous skills review (if exists)
2. Verify improvements were actually implemented
3. Note any regression or new issues
4. Build on previous findings
