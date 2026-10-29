#!/usr/bin/env python3
"""Print a compact digest of chat Markdown files for compilation planning.

Usage:
  digest.py FILE... [--user N] [--last N]

Per file: frontmatter title/date, the "Summary (by claude.ai)" section if any,
every user turn (first --user chars, default 600) and the last assistant turn
(first --last chars, default 1200). Tool-call lines are dropped.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--user", type=int, default=600)
    ap.add_argument("--last", type=int, default=1200)
    args = ap.parse_args()
    for f in args.files:
        t = f.read_text(encoding="utf-8")
        title = re.search(r'^title: "?(.*?)"?$', t, re.M)
        print(f"\n===== {f.name} | {title.group(1) if title else ''} | {len(t)} chars")
        m = re.search(r"## Summary \(by claude\.ai\)\n(.*?)\n## ", t, re.S)
        if m:
            print("SUMMARY:", m.group(1).strip())
        parts = re.split(r"\n(### (?:User|Claude|ChatGPT)[^\n]*)\n", t)
        turns = [(parts[i], re.sub(r"^\*\[tool:.*$", "", parts[i + 1], flags=re.M).strip()) for i in range(1, len(parts), 2)]
        for h, b in turns:
            if h.startswith("### User"):
                print(f"U {h[9:]}: {b[:args.user]}".replace("\n", " "))
        last = [b for h, b in turns if not h.startswith("### User") and b]
        if last:
            print("LAST A:", last[-1][: args.last].replace("\n", " "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
