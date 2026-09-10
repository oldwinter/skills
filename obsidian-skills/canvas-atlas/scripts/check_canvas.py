#!/usr/bin/env python3
"""Read-only validation of native Canvas files and their vault-local references."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NoReturn


def reject_constant(value: str) -> NoReturn:
    raise ValueError(f"Nonstandard JSON constant: {value}")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--vault", type=Path, required=True, help="Root used by file nodes")
parser.add_argument("files", type=Path, nargs="+", help="Canvas paths, relative to vault")
args = parser.parse_args()
root = args.vault.resolve()
errors = []
pending = [(root / item).resolve() for item in args.files]
loaded = set()
embeds = {}
required = {"text": "text", "file": "file", "link": "url", "group": None}
sides = ("top", "right", "bottom", "left")
counts = {"canvases": 0, "nodes": 0, "edges": 0, "references": 0}

while pending:
    filename = pending.pop()
    if filename in loaded:
        continue
    loaded.add(filename)
    if not filename.is_relative_to(root):
        errors.append(f"Canvas outside vault: {filename}")
        continue
    location = filename.relative_to(root).as_posix()
    try:
        data = json.loads(filename.read_text(encoding="utf-8"), parse_constant=reject_constant)
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{location}: {exc}")
        continue
    if not isinstance(data, dict):
        errors.append(f"{location}: root must be an object")
        continue
    nodes, edges = data.get("nodes", []), data.get("edges", [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        errors.append(f"{location}: nodes and edges must be arrays")
        continue
    counts["canvases"] += 1
    counts["nodes"] += len(nodes)
    counts["edges"] += len(edges)
    ids, node_ids = set(), set()
    references = []
    embeds[filename] = set()
    for kind, items in (("node", nodes), ("edge", edges)):
        for index, item in enumerate(items):
            at = f"{location} {kind}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{at}: must be an object")
                continue
            identifier = item.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in ids:
                errors.append(f"{at}: missing or duplicate id")
            else:
                ids.add(identifier)
                if kind == "node":
                    node_ids.add(identifier)
            if "color" in item and (not isinstance(item["color"], str) or not re.fullmatch(r"[1-6]|#[0-9a-fA-F]{6}", item["color"])):
                errors.append(f"{at}: invalid color")
            if kind == "edge":
                for key in ("fromNode", "toNode"):
                    if not isinstance(item.get(key), str) or item[key] not in node_ids:
                        errors.append(f"{at}: dangling {key}")
                for key in ("fromSide", "toSide"):
                    if key in item and item[key] not in sides:
                        errors.append(f"{at}: invalid {key}")
                for key in ("fromEnd", "toEnd"):
                    if key in item and item[key] not in ("none", "arrow"):
                        errors.append(f"{at}: invalid {key}")
                continue
            for key in ("x", "y", "width", "height"):
                value = item.get(key)
                if type(value) not in (int, float) or not -sys.float_info.max <= value <= sys.float_info.max or (key in ("width", "height") and value <= 0):
                    errors.append(f"{at}: invalid {key}")
            node_type = item.get("type")
            if not isinstance(node_type, str) or node_type not in required:
                errors.append(f"{at}: invalid node type")
                continue
            key = required[node_type]
            if key is not None and not isinstance(item.get(key), str):
                errors.append(f"{at}: missing string {key}")
                continue
            if node_type == "file":
                references.append((item["file"], True, at))
                if "subpath" in item and (not isinstance(item["subpath"], str) or not item["subpath"].startswith("#")):
                    errors.append(f"{at}: invalid subpath")
            elif node_type == "text":
                for match in re.finditer(r"(!?)\[\[([^\]]+)\]\]", item["text"]):
                    target = match[2].split("|", 1)[0].split("#", 1)[0]
                    if target:
                        references.append((target, bool(match[1]), at))
    for reference, embedded, at in references:
        if "\0" in reference:
            errors.append(f"{at}: NUL character in file reference")
            continue
        target = (root / reference).resolve()
        if not target.suffix and not target.is_file():
            target = target.with_suffix(".md")
        counts["references"] += 1
        if Path(reference).is_absolute() or not target.is_relative_to(root):
            errors.append(f"{at}: reference outside vault: {reference}")
        elif not target.is_file():
            errors.append(f"{at}: missing file: {reference}")
        elif target.suffix == ".canvas":
            pending.append(target)
            if embedded:
                embeds[filename].add(target)

for origin in embeds:
    stack = list(embeds[origin])
    seen = set()
    while stack:
        target = stack.pop()
        if target == origin:
            errors.append(f"{origin.relative_to(root)}: cyclic Canvas embedding")
            break
        if target not in seen:
            seen.add(target)
            stack.extend(embeds.get(target, ()))

print(json.dumps({"valid": not errors, **counts, "errors": errors}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
