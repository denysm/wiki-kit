#!/usr/bin/env python3
"""Stage file sources from inventory.tsv into a topic inbox.

Usage:
  stage.py --inventory inventory.tsv --topic career --out topics/career/inbox
  stage.py ... --kinds chat-md --dry-run

Takes rows with decision=ingest for --topic whose path is a file (not an
`export.json#id` chat; those go through chat2md.py). Conversion by kind:
docx/doc/rtf -> textutil txt saved as .md; pdf -> pdf2txt (PDFKit, built from
pdf2txt.swift next to this script); md/txt/yaml/chat-md -> copied as is.
Existing targets are skipped. Prints one line per row.
"""
from __future__ import annotations

import argparse
import os
import csv
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Root of the originals that inventory.tsv paths are relative to.
SRC = Path(os.environ.get("WIKI_KIT_SOURCES", "~/Projects/private-sources")).expanduser()
COPY = {"md", "txt", "yaml", "yml", "chat-md"}
TEXTUTIL = {"docx", "doc", "rtf"}


def pdf_tool() -> Path:
    exe = HERE / "pdf2txt"
    if not exe.exists():
        subprocess.run(["swiftc", "-O", str(HERE / "pdf2txt.swift"), "-o", str(exe)], check=True)
    return exe


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", type=Path, required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--kinds", help="comma-separated kinds to take (default: all file kinds)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    kinds = set(args.kinds.split(",")) if args.kinds else None
    args.out.mkdir(parents=True, exist_ok=True)

    n = 0
    for r in csv.DictReader(args.inventory.open(encoding="utf-8"), delimiter="\t"):
        if r["decision"] != "ingest" or r["topic"] != args.topic or "#" in r["path"]:
            continue
        kind = r["kind"]
        if kinds and kind not in kinds:
            continue
        src = SRC / r["path"]
        if kind in COPY:
            dst = args.out / src.name
        elif kind in TEXTUTIL or kind == "pdf":
            dst = args.out / (src.stem + ".md")
        else:
            print(f"SKIP {r['n']} unsupported kind {kind}: {r['path']}", file=sys.stderr)
            continue
        if dst.exists():
            print(f"exists {dst.name}")
            continue
        print(f"{r['n']}\t{kind}\t-> {dst.name}")
        if args.dry_run:
            continue
        if kind in COPY:
            shutil.copy2(src, dst)
        elif kind in TEXTUTIL:
            subprocess.run(["textutil", "-convert", "txt", "-output", str(dst), str(src)], check=True)
        else:
            subprocess.run([str(pdf_tool()), str(src), str(dst)], check=True)
        n += 1
    print(f"staged {n} file(s) into {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
