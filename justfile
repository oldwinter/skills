# Skills repository task runner

default: check

# README list, frontmatter names, and personal paths all match the tree
check: check-readme-map check-skill-contracts test-readme-map

check-readme-map:
    python3 scripts/check-readme-map

check-skill-contracts:
    python3 scripts/check-skill-contracts

test-readme-map:
    bash scripts/test-check-readme-map
