#!/usr/bin/env python3
"""Stage the inventory kinds stage.py skips, and write ingest meta for plain staged files.

Usage:
  extra2md.py --inventory inventory.tsv --topic personal --out topics/personal/inbox

Rows with decision=ingest for --topic:
  webarchive, artifact (html)  -> textutil txt
  zip                          -> each text member (csv/txt/md/json) in a fenced block
  memory (Claude memories json) -> conversations memory, project memories, memory files
  project (Claude project json) -> name, description, prompt, docs
Each becomes <date>-<slug>.md with frontmatter (type=notes), ready for ingest.py.
Files already staged by stage.py without frontmatter (docx/pdf/txt/md) get an entry
in OUT/.meta.json (title/date/source from the TSV) for `ingest.py --meta`.
"""
from __future__ import annotations

import argparse
import os
import csv
import json
import re
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ingest import slugify, yq  # noqa: E402

# Root of the originals that inventory.tsv paths are relative to.
SOURCE_PREFIX = os.environ.get("WIKI_KIT_SOURCES", "~/Projects/private-sources").rstrip("/")
SRC = Path(SOURCE_PREFIX).expanduser()
TODAY = date.today().isoformat()
TEXT_MEMBERS = (".csv", ".txt", ".md", ".json")


def textutil(p: Path) -> str:
    return subprocess.run(["textutil", "-convert", "txt", "-stdout", str(p)],
                          capture_output=True, text=True, check=True).stdout


def from_zip(p: Path) -> str:
    out = []
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            if name.lower().endswith(TEXT_MEMBERS):
                lang = Path(name).suffix.lstrip(".")
                out.append(f"## {name}\n\n```{lang}\n{z.read(name).decode('utf-8', 'replace').strip()}\n```\n")
    return "\n".join(out)


def from_memory(p: Path) -> str:
    d = json.loads(p.read_text(encoding="utf-8"))
    out = ["## Conversations memory\n", d.get("conversations_memory", "").strip(), ""]
    for pid, text in (d.get("project_memories") or {}).items():
        out += [f"## Project memory {pid}\n", text.strip(), ""]
    for f in d.get("memory_files") or []:
        out += [f"## Memory file {f.get('path', '')}\n", str(f.get("content", "")).strip(), ""]
    return "\n".join(out)


def from_project(p: Path) -> str:
    d = json.loads(p.read_text(encoding="utf-8"))
    out = [f"Project: **{d.get('name', '')}**", f"Description: {d.get('description', '')}",
           f"Created: {d.get('created_at', '')}; updated: {d.get('updated_at', '')}", ""]
    if d.get("prompt_template"):
        out += ["## Project prompt\n", d["prompt_template"].strip(), ""]
    for doc in d.get("docs") or []:
        out += [f"## Doc: {doc.get('filename', '')}\n", str(doc.get("content", "")).strip(), ""]
    return "\n".join(out)


CONVERT = {"webarchive": textutil, "artifact": textutil, "zip": from_zip,
           "memory": from_memory, "project": from_project}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", type=Path, required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    meta_path = a.out / ".meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    staged = {p.stem: p for p in a.out.iterdir() if p.is_file() and not p.name.startswith(".")}
    with a.inventory.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t")
                if r["decision"] == "ingest" and r["topic"] == a.topic and "#" not in r["path"]]
    for r in rows:
        src, kind, title = SRC / r["path"], r["kind"], r["title"] or Path(r["path"]).stem
        if kind in CONVERT:
            body = CONVERT[kind](src).strip()
            day = r["date"] or date.fromtimestamp(src.stat().st_mtime).isoformat()
            title = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", title)
            name = f"{day}-{slugify(title, 48)}.md"
            head = {"title": yq(title), "source": yq(f"{SOURCE_PREFIX}/{r['path']}"),
                    "type": "notes", "ingested": TODAY, "tags": f"[{kind}]", "summary": yq(""),
                    "source_date": day, "content_format": kind}
            fm = "---\n" + "".join(f"{k}: {v}\n" for k, v in head.items()) + "---\n\n"
            (a.out / name).write_text(fm + f"# {title}\n\n{body}\n", encoding="utf-8")
            print(f"{r['n']}\t{kind}\t-> {name} ({len(body)} chars)")
            continue
        p = staged.get(Path(r["path"]).stem)
        if p and not p.read_text(encoding="utf-8", errors="replace").startswith("---\n"):
            meta[p.name] = {"type": "articles", "title": title, "date": r["date"],
                            "source": f"{SOURCE_PREFIX}/{r['path']}",
                            "tags": [kind], "content_format": kind}
            print(f"{r['n']}\t{kind}\tmeta for {p.name}")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
