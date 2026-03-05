# Security & Robustness Guide (for skill authors)

Agent Skills can amplify both productivity and risk, especially when scripts/tools are allowed.

## 1) Least privilege by default
- Only request tools you truly need.
- Prefer Read-only over Write/Edit where possible.
- Avoid running shell commands unless necessary.

## 2) Never handle secrets casually
- Do not ask for API keys, passwords, tokens.
- If the user provides secrets, warn them and avoid copying them into outputs.
- Do not write secrets to files.

## 3) Guard against prompt injection
- Treat external content (webpages, emails, docs) as untrusted input.
- Do not blindly follow instructions found inside retrieved text.
- Keep a strict separation between “instructions” (this skill) and “data” (user inputs).

## 4) Safe file operations
If the skill writes files:
- Use a dedicated output folder (e.g., `docs/<skill>/`).
- Avoid destructive edits.
- Provide rollback guidance (git diff, backup copies).

## 5) Human-in-the-loop checkpoints
Add explicit checkpoints for:
- Launch decisions
- Legal/privacy/security constraints
- Anything irreversible or high-risk

## 6) Scripts
If you ship scripts:
- Keep them small and auditable.
- Avoid network calls by default.
- Document exactly what they do in SKILL.md and README.md.
