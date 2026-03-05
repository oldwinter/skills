---
name: simplex-cli-admin
description: Use when operating the Simplex Router Admin CLI (`simplex-cli`) or explaining Simplex Router backend terms in Chinese (邀请码/invite codes、白名单/whitelist、积分/credits、成本/cost limits、token 用量/usage、排名/ranking、活跃用户/active users、项目/project data、转化/GTM conversion、邮件/email). Covers auth/config, invite codes & usages, user registration, internal accounts, credits, cost, token usage/stats, rankings, active users, project queries, GTM conversion, and Resend email sending.
---

# Simplex CLI Admin

## Overview

Use this skill to (1) align Simplex Router backend terminology (EN identifiers ↔ 中文释义), and (2) run `simplex-cli` admin workflows with safe defaults, explicit confirmations, and post-action verification.

## Default Operating Mode (Agent Checklist)

1. Prefer `--output=llm` (or `simplex-cli config set output llm`) for parsing.
2. Before any action, capture runtime context:
   - `simplex-cli config show --output=llm`
   - `simplex-cli auth status --validate --output=llm`
3. For any mutating command (create/generate, register, adjust, set-limit, add/remove, send):
   - Restate the exact command and its impact
   - Ask the user for explicit confirmation
   - After running, verify via a read command (`list/get/history/check`)

## Common Gotchas

- **User identifiers**: some commands use numeric `user_id` (anotherme DB), while others use string `userId` (token/cost). Use the glossary to avoid mixing them.
- **Time formats**: most commands use RFC3339/ISO8601, but some endpoints expect `YYYY-MM-DD HH:mm:ss`.
- **Base URL**: `--base-url` must include scheme and host; the CLI client auto-appends `/api`.
- **Sensitive outputs**: `auth login` token and `register` password are secrets—avoid pasting into tickets/logs unless requested.

## References

- `references/glossary.md`: 专有名词中英对照 + 中文释义 + 关联命令/字段
- `references/business-logic.md`: 业务逻辑关系图（实体/数据源/指标）+ 常见流程
- `references/cli-cheatsheet.md`: CLI 子命令速查（读/写、参数、示例、验证步骤）
