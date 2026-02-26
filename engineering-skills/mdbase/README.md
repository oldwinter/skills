# mdbase — Typed Markdown Collections

An [Agent Skill](https://agentskills.io) that teaches AI coding assistants to work with **mdbase collections** — folders of markdown files with YAML frontmatter treated as typed, queryable data.

## What is mdbase?

mdbase turns a folder of markdown files into a lightweight, typed database:

- **`mdbase.yaml`** at the root marks a folder as a collection
- **`_types/`** contains type definitions with field schemas
- **`.md` files** are records with YAML frontmatter validated against their type

No build step, no server, no dependencies. Just markdown files and an AI assistant that understands the schema.

## Installation

### Tools with native Agent Skills support

Clone this repo into the skills directory for your tool. The directory **must** be named `mdbase`.

| Tool | Location | Command |
|------|----------|---------|
| **Claude Code** (project) | `.claude/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git .claude/skills/mdbase` |
| **Claude Code** (global) | `~/.claude/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git ~/.claude/skills/mdbase` |
| **GitHub Copilot** | `.github/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git .github/skills/mdbase` |
| **OpenAI Codex** (project) | `.codex/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git .codex/skills/mdbase` |
| **OpenAI Codex** (global) | `~/.codex/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git ~/.codex/skills/mdbase` |
| **Cursor** | `.cursor/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git .cursor/skills/mdbase` |
| **Gemini CLI** | `.gemini/skills/mdbase/` | `git clone https://github.com/calluma/mdbase-skill.git .gemini/skills/mdbase` |

### Tools using adapter files

For tools that don't support the Agent Skills standard, copy the appropriate self-contained adapter file:

| Tool | Install |
|------|---------|
| **Windsurf** | `cp adapters/windsurf.md .windsurf/rules/mdbase.md` |
| **Amazon Q** | `cp adapters/amazonq.md .amazonq/rules/mdbase.md` |
| **Aider** | `aider --read path/to/mdbase-skill/adapters/aider.md` |
| **Gemini Code Assist** | `cp adapters/gemini.md GEMINI.md` |

## Usage

Once installed, the skill activates automatically when your AI assistant detects an `mdbase.yaml` file in your project. You can ask it to:

- **Initialize** a new collection with types
- **Create** records with proper frontmatter
- **Query** records using the expression language
- **Validate** the collection against type schemas
- **Refactor** types and update all references

## File structure

```
mdbase-skill/
├── SKILL.md              # Agent Skills entry point (instructions)
├── references/
│   └── spec.md           # Full mdbase specification (loaded on demand)
├── adapters/
│   ├── windsurf.md       # Self-contained adapter for Windsurf
│   ├── amazonq.md        # Self-contained adapter for Amazon Q
│   ├── aider.md          # Self-contained adapter for Aider
│   └── gemini.md         # Self-contained adapter for Gemini Code Assist
├── README.md
└── LICENSE
```

## License

MIT
