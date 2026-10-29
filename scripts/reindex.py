#!/usr/bin/env python3
"""Rebuild the derived _index.md files of a topic wiki from file frontmatter.

Usage:
  reindex.py TOPIC_DIR [--change "text"]

Rewrites the Contents tables of raw/<type>/_index.md, raw/_index.md,
wiki/<category>/_index.md, wiki/_index.md and the master _index.md (plus its
Statistics block). Recent Changes lines are kept; --change prepends one dated
line to every index whose contents changed. Uses only the stdlib: frontmatter is
parsed line by line (title, summary, tags, ingested/updated).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

TODAY = date.today().isoformat()
RAW_TYPES = ["articles", "papers", "repos", "notes", "data"]
WIKI_CATS = ["concepts", "topics", "references", "theses"]


def frontmatter(p: Path) -> dict:
    text = p.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def cell(s: str, n: int = 160) -> str:
    s = s.replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def link(name: str) -> str:
    return f"[{name}](<{name}>)" if " " in name else f"[{name}]({name})"


def rows(files: list[Path], base: Path, date_key: str) -> list[str]:
    out = []
    for f in sorted(files):
        fm = frontmatter(f)
        tags = fm.get("tags", "").strip("[]")
        out.append(f"| {link(str(f.relative_to(base)))} | {cell(fm.get('summary', ''))} | {cell(tags, 80)} | "
                   f"{fm.get(date_key) or fm.get('ingested') or ''} |")
    return out


def pointers(base: Path, names: list[str], _=None) -> list[str]:
    """Root indexes (raw/, wiki/) list category indexes, not files (lint contract)."""
    out = []
    for n in names:
        if (base / n).exists():
            k = len([f for f in (base / n).glob("*.md") if f.name != "_index.md"])
            out.append(f"| [{n}/_index.md]({n}/_index.md) | {n}: {k} file(s) | | {TODAY} |")
    return out


def write_index(path: Path, title: str, desc: str, table: list[str], change: str | None, extra: str = "") -> None:
    recent = []
    if path.exists():
        old = path.read_text(encoding="utf-8")
        m = re.search(r"## Recent Changes\n\n(.*)", old, re.S)
        if m:
            recent = [l for l in m.group(1).splitlines() if l.startswith("- ")]
        old_table = re.search(r"## Contents\n\n(.*?)\n\n", old + "\n\n", re.S)
        same = old_table and old_table.group(1).splitlines()[2:] == table
    else:
        same = False
    if change and not same:
        recent.insert(0, f"- {TODAY}: {change}")
    body = (f"# {title}\n\n> {desc}\n\nLast updated: {TODAY}\n\n{extra}## Contents\n\n"
            "| File | Summary | Tags | Updated |\n|------|---------|------|---------|\n"
            + "".join(r + "\n" for r in table)
            + "\n## Recent Changes\n\n" + "\n".join(recent[:30]) + "\n")
    path.write_text(body, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic", type=Path)
    ap.add_argument("--change")
    args = ap.parse_args()
    t = args.topic.resolve()
    name = frontmatter(t / "config.md").get("title", t.name)

    raw_all, wiki_all = [], []
    for ty in RAW_TYPES:
        d = t / "raw" / ty
        files = [f for f in d.glob("*.md") if f.name != "_index.md"] if d.exists() else []
        raw_all += files
        if d.exists():
            write_index(d / "_index.md", f"raw/{ty} Index", f"raw/{ty} of the {name} wiki", rows(files, d, "ingested"), args.change)
    write_index(t / "raw" / "_index.md", "raw Index", f"raw of the {name} wiki", pointers(t / "raw", RAW_TYPES, len), args.change)
    for c in WIKI_CATS:
        d = t / "wiki" / c
        files = [f for f in d.glob("*.md") if f.name != "_index.md"] if d.exists() else []
        wiki_all += files
        if d.exists():
            write_index(d / "_index.md", f"wiki/{c} Index", f"wiki/{c} of the {name} wiki", rows(files, d, "updated"), args.change)
    write_index(t / "wiki" / "_index.md", "wiki Index", f"wiki of the {name} wiki", pointers(t / "wiki", WIKI_CATS, len), args.change)

    log = (t / "log.md").read_text(encoding="utf-8") if (t / "log.md").exists() else ""
    last = lambda op: (re.findall(rf"^## \[(\d{{4}}-\d\d-\d\d)\] {op} ", log, re.M) or ["never"])[-1]
    outputs = [f for f in (t / "output").rglob("*.md") if f.name != "_index.md"] if (t / "output").exists() else []
    stats = (f"## Statistics\n\n- Sources: {len(raw_all)} raw documents\n- Articles: {len(wiki_all)} compiled wiki articles\n"
             f"- Outputs: {len(outputs)} generated artifacts\n- Last compiled: {last('compile')}\n- Last lint: {last('lint')}\n\n"
             "## Quick Navigation\n\n- [All Sources](raw/_index.md)\n- [Concepts](wiki/concepts/_index.md)\n"
             "- [Topics](wiki/topics/_index.md)\n- [References](wiki/references/_index.md)\n- [Outputs](output/_index.md)\n\n")
    desc = frontmatter(t / "config.md").get("description", "")
    write_index(t / "_index.md", f"{name} Index", desc, rows(wiki_all, t, "updated"), args.change, extra=stats)
    print(f"reindexed {t.name}: {len(raw_all)} sources, {len(wiki_all)} articles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
