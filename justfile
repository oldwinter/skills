# Skills repository task runner

default: check

# README list, frontmatter names, and personal paths all match the tree
check: check-readme-map check-skill-contracts test-readme-map test-doctor

# Local toolchain health: python3, bash, git, just, CLAUDE.md symlink
doctor:
    python3 scripts/doctor

check-readme-map:
    python3 scripts/check-readme-map

check-skill-contracts:
    python3 scripts/check-skill-contracts

test-readme-map:
    bash scripts/test-check-readme-map

test-doctor:
    bash scripts/test-doctor

# Skill test suites (unittest; slower, not part of check)
test-skills:
    python3 -m unittest discover -s agent-autoresearch/tests -q
    python3 -m unittest discover -s obsidian-skills/canvas-atlas/tests -q
