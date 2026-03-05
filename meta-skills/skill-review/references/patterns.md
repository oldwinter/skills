# Skill Review Patterns and Examples

## Review Triggers

User phrases that should trigger this skill:
- "复盘" / "review" / "retrospect"
- "总结" / "summarize" / "总结一下"
- "有什么问题" / "what issues"
- "改进" / "improve" / "优化"
- "需要改进的地方" / "what needs improvement"

## Skills Analysis Checklist

### For Each Skill, Check:

**Completeness:**
- [ ] All commands documented correctly
- [ ] All options listed with actual flags
- [ ] Examples match actual command behavior
- [ ] Error handling documented

**Accuracy:**
- [ ] Commands work as documented
- [ ] Options exist as described
- [ ] Examples produce expected results
- [ ] No outdated information

**Usability:**
- [ ] Clear workflow guidance
- [ ] Common pitfalls documented
- [ ] Workarounds provided for known issues
- [ ] Progressive disclosure (basics + advanced)

**Language:**
- [ ] Chinese terms properly explained
- [ ] Code examples copy-pasteable
- [ ] Output formats documented
- [ ] ID formats clearly shown

## Issue Taxonomy

| Category | Description | Example |
|----------|-------------|---------|
| WRONG_CMD | Command doesn't exist | `tn create --priority high` |
| WRONG_OPT | Option doesn't exist | `tn search --json` |
| SILENT_FAIL | Command succeeds but does nothing | `update --add-projects` |
| DIFF_BEHAV | Works differently than expected | `∑` symbol parsing |
| MISSING_DOC | Important info not documented | `.md` extension requirement |
| OUTDATED | Information is stale | Old command syntax |
| CONFUSING | Unclear or ambiguous | Project naming convention |

## Improvement Templates

### Issue: Wrong Command
```markdown
### [Issue]
Command `X` doesn't support option `Y`.

### Evidence
```
$ tn X --Y
error: unknown option '--Y'
```

### Fix
Use natural language instead:
```
tn "task description with Y"
```

### Location
SKILL.md - "[Section Name]"
```

### Issue: Silent Failure
```markdown
### [Issue]
Command `X` returns success but has no effect.

### Evidence
```
$ tn update <id> --add-projects "project"
✓ Task updated successfully
# But projects field is still empty
```

### Root Cause
API bug / incomplete implementation.

### Workaround
Create task with project from the start:
```
tn "task +Project_Name @work"
```

### Location
SKILL.md - "Common Pitfalls" section
```

### Issue: Parsing Problem
```markdown
### [Issue]
Special characters cause parsing issues.

### Evidence
`∑` symbol causes the project name to be cut off.

### Workaround
Use underscore instead: `拓扑灵犀_infra建设`

### Location
SKILL.md - "Projects Management"
```

## Review Report Format

```markdown
## Skills Review - [Date]

### Session Summary
- Skills used: [list]
- Commands executed: [count]
- Success rate: [X%]

### [Skill Name]
**Overall Assessment:** [Good / Needs Work / Critical Issues]

**Metrics:**
- Commands documented: N
- Commands tested: N
- Success rate: X%

**Issues Found:**
1. [Type] [Severity] - [One-line description]
   - Impact: [What happens]
   - Fix: [How to address]

**Improvements:**
1. [File] - [Change description]
2. ...

**Still Missing:**
1. [What's needed]
2. ...

### [Next Skill]
... (same format)
```

## Quick Wins vs Deep Dives

### Quick Wins (< 5 min)
- Fix typos in examples
- Add missing option to documentation
- Clarify confusing wording
- Add missing error message

### Deep Dives (> 15 min)
- Rewrite entire section
- Add new reference document
- Create helper scripts
- Test all commands systematically
```

## Follow-up Actions

After completing review:

1. **Apply fixes immediately** for critical/high issues
2. **Create tickets** for medium/low issues
3. **Track** improvements in a changelog
4. **Schedule** next review after skill usage
