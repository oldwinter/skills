---
name: collect-incomplete-tasks
description: 汇总指定日期范围内 Daily notes 中的未完成任务到当前 Daily note。当用户提到"汇总未完成任务"、"收集待办"、"统计任务"、"整理积压任务"、"backlog整理"时触发。支持指定时间范围（如"最近1周"、"最近1个月"、"从12月到现在"）。
---

# Collect Incomplete Tasks

汇总 Obsidian 笔记库中指定日期范围内 Daily notes 的未完成任务（`- [ ]`），按日期分组输出到当前 Daily note。

## 工作流程

### 1. 确定日期范围

根据用户请求解析日期范围：
- "最近1周" → 过去7天
- "最近1个月" → 过去30天
- "从 YYYY-MM-DD 到 YYYY-MM-DD" → 指定范围
- 无指定 → 默认最近1个月

### 2. 定位 Daily notes

Daily notes 路径格式：
```
Calendar/Daily notes/YYYY/YYYY-MM-DD.md
```

仅匹配标准格式的日期文件（`YYYY-MM-DD.md`），忽略其他笔记。

### 3. 提取未完成任务

搜索模式：`- [ ]`（未勾选的 checkbox）

使用 Grep 工具批量搜索：
```bash
# 搜索指定目录下的未完成任务
Grep pattern="- \[ \]" path="Calendar/Daily notes/2025/" output_mode="content"
```

### 4. 汇总输出

输出格式：
```markdown
## 近X天/周/月未完成任务汇总（起始日期 ~ 结束日期）

### YYYY-MM-DD
- [ ] 任务1
- [ ] 任务2

### YYYY-MM-DD
- [ ] 任务3

---

**统计：共 N 项未完成任务**
```

### 5. 写入目标文件

将汇总内容插入到当前 Daily note 的开头（frontmatter 之后）。

## 注意事项

- 保留任务中的 wikilinks（如 `[[笔记名]]`）
- 合并嵌套子任务到父任务（保持缩进）
- 去除重复任务（同一任务可能在多天出现）
- 跳过空行和无效格式
