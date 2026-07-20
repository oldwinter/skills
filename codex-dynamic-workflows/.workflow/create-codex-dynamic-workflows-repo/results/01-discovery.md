# Discovery Result

Accepted:
- Pi reference repo is a TypeScript Pi extension with parser/runtime/tool/display/subagent modules and tests.
- User-facing concepts to preserve: `agent`, `parallel`, `pipeline`, `phase`, structured output, progress display, abort, deterministic workflow boundaries.
- Codex adaptation should be a skill plus durable workflow artifacts, not a false claim of a native Pi-style tool.

Risk:
- Pi package metadata declares MIT, but no root `LICENSE` was found in the cloned reference. This repo avoids copying Pi runtime code and includes attribution in `NOTICE.md`.

Verification:
- Reference repos cloned to `/tmp/pi-dynamic-workflows-ref` and `/tmp/dannymac-skills-ref`.
