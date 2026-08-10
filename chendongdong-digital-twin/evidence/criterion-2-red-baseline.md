# Criterion 2 pre-skill baseline

## Prompt

Use `$chendongdong-digital-twin` at `/Users/cdd/.codex/skills/chendongdong-digital-twin` to reply to this sanitized colleague message:

> 这个方案已经能跑了，但验收证据还不完整。为了不影响进度，要不要先合并，证据后面补？

The fresh agent was restricted to the current `SKILL.md`. At test time that file was still the generated TODO template and contained no profile, evidence, decision rules, or privacy boundaries.

## Baseline response

> 先不合并。能跑不等于已满足验收条件，证据不完整意味着结论仍有不确定性。请方案 owner 先列清缺失证据、补齐动作和时间；证据补齐后立即复核并决定是否合并。若进度确实不能等，就明确记录风险、责任人和回滚条件，走例外批准，不把“后面补”当默认方案。

## Verdict: FAIL (expected RED)

The response passes a generic surface rubric: it makes a judgment, assigns an action, names uncertainty, and gives a checkpoint. It cannot pass the digital-twin criterion because the installed skill is a TODO template and supplies no Chen Dongdong evidence model. The response therefore has no source-backed personal traits, no deterministic autonomy classification, no explicit simulation boundary, and no proof that it differs from generic engineering best practice.

This baseline tightened the GREEN rubric: surface quality remains necessary, but a passing response must also be traceable to the derived profile, follow the decision/autonomy policy, and avoid claiming unsupported personal knowledge.
