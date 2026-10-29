"""Create an empty llm-wiki root by copying the skeleton of an existing empty topic.

Usage: scaffold_wiki.py <template_root> <new_root> <title> <description> <scope> [<convention> ...]
Refuses to write into an existing wiki root (one that already has _index.md).
"""
import shutil
import sys
from pathlib import Path

TODAY = __import__("datetime").date.today().isoformat()
tpl, root = Path(sys.argv[1]), Path(sys.argv[2])
title, desc, scope = sys.argv[3], sys.argv[4], sys.argv[5]
conventions = sys.argv[6:]

if (root / "_index.md").exists():
    sys.exit(f"refusing: {root} already holds a wiki")

# index files and Obsidian config, copied verbatim
for f in tpl.rglob("*"):
    if not f.is_file():
        continue
    rel = f.relative_to(tpl)
    if rel.name == "_index.md" and rel.parent != Path(".") or rel.parts[0] == ".obsidian":
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)

(root / "inbox" / ".processed").mkdir(parents=True, exist_ok=True)

conv = "\n".join(f"- {c}" for c in conventions) if conventions else "- Follow the hub `CLAUDE.md` rules."
(root / "config.md").write_text(f"""---
title: "{title}"
description: "{desc}"
created: {TODAY}
freshness_threshold: 70
---

# Wiki Configuration

## Scope

{scope}

## Conventions

{conv}
""", encoding="utf-8")

schema = (tpl / "schema.md").read_text(encoding="utf-8")
first_title = schema.split('title: "', 1)[1].split('"', 1)[0]
schema = schema.replace(first_title, f"{title} Topic Guide", 1)
schema = schema.replace(f"# {first_title}", f"# {title} Topic Guide", 1)
schema = schema.replace("created: 2026-10-15", f"created: {TODAY}").replace("updated: 2026-10-15", f"updated: {TODAY}")
(root / "schema.md").write_text(schema, encoding="utf-8")

(root / "_index.md").write_text(f"""# {title} Index

> {desc}

Last updated: {TODAY}

## Statistics

- Sources: 0 raw documents
- Articles: 0 compiled wiki articles
- Inventory records: 0 tracked items
- Datasets: 0 manifests
- Outputs: 0 generated artifacts
- Last compiled: never
- Last lint: never

## Quick Navigation

- [All Sources](raw/_index.md)
- [Concepts](wiki/concepts/_index.md)
- [Topics](wiki/topics/_index.md)
- [References](wiki/references/_index.md)
- [Theses](wiki/theses/_index.md)
- [Outputs](output/_index.md)

## Contents

| File | Summary | Tags | Updated |
|------|---------|------|---------|

## Recent Changes

- {TODAY}: Wiki initialized
""", encoding="utf-8")

(root / "log.md").write_text(f"""# Wiki Activity Log

## [{TODAY}] init | Wiki initialized
""", encoding="utf-8")

print("created", root)
