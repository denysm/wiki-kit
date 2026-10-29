#!/usr/bin/env python3
"""Move staged inbox files into raw/ with llm-wiki frontmatter.

Usage:
  ingest.py TOPIC_DIR --meta meta.json [--dry-run]
  ingest.py TOPIC_DIR --until 2025-10-31     # one wave: files named up to that date

meta.json maps an inbox file name to {"type", "title", "tags", "summary"} and
optional "slug", "date" (YYYY-MM-DD prefix, default today), "source", and any
extra frontmatter keys. A file that already starts with frontmatter (chat2md
output, chat-md copies) keeps its text and file name; meta, if given, is ignored
for it. Other files get frontmatter + "# Title" + the original text (YAML is
fenced). Originals go to inbox/.processed/. Then reindex.py runs and one log
line per source is appended to TOPIC_DIR/log.md.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
sys.path.insert(0, str(HERE))
from chat2md import slugify, yq  # noqa: E402
from reindex import frontmatter  # noqa: E402


def yaml_list(v) -> str:
    return "[" + ", ".join(v) + "]" if isinstance(v, list) else str(v)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic", type=Path)
    ap.add_argument("--meta", type=Path)
    ap.add_argument("--until", help="only inbox files whose name starts with a date <= this (YYYY-MM-DD)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    t = args.topic.resolve()
    inbox = t / "inbox"
    meta = json.loads(args.meta.read_text(encoding="utf-8")) if args.meta else {}
    done = inbox / ".processed"
    log = []

    for src in sorted(p for p in inbox.iterdir() if p.is_file() and not p.name.startswith(".")):
        if args.until and not (src.name[:10] <= args.until and src.name[:4].isdigit()):
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        if text.startswith("---\n"):
            fm = frontmatter(src)
            ty, title, name, out = fm.get("type", "notes"), fm.get("title", src.stem), src.name, text
        elif src.name in meta:
            m = dict(meta[src.name])
            ty, title = m.pop("type"), m.pop("title")
            name = f"{m.pop('date', TODAY)}-{m.pop('slug', None) or slugify(title, 48)}.md"
            body = f"```yaml\n{text.rstrip()}\n```\n" if src.suffix in (".yaml", ".yml") else text.strip() + "\n"
            head = {"title": yq(title), "source": yq(m.pop("source", str(src.name))), "type": ty,
                    "ingested": TODAY, "tags": yaml_list(m.pop("tags", [])), "summary": yq(m.pop("summary", ""))}
            head.update({k: (yaml_list(v) if isinstance(v, list) else yq(str(v)) if isinstance(v, str) else v)
                         for k, v in m.items()})
            out = "---\n" + "".join(f"{k}: {v}\n" for k, v in head.items()) + f"---\n\n# {title}\n\n{body}"
        else:
            print(f"SKIP no meta: {src.name}", file=sys.stderr)
            continue
        dst = t / "raw" / ty / name
        if dst.exists():
            print(f"SKIP exists: raw/{ty}/{name}", file=sys.stderr)
            continue
        print(f"{src.name} -> raw/{ty}/{name}")
        if args.dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out, encoding="utf-8")
        done.mkdir(exist_ok=True)
        shutil.move(str(src), done / src.name)
        log.append(f"## [{TODAY}] ingest | {title} (raw/{ty}/{name})\n")

    if log and not args.dry_run:
        with (t / "log.md").open("a", encoding="utf-8") as f:
            f.writelines(log)
        subprocess.run([sys.executable, "-I", str(HERE / "reindex.py"), str(t), "--change", f"Ingested {len(log)} source(s)"], check=True)
    print(f"ingested {len(log)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
