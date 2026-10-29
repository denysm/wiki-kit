#!/usr/bin/env python3
"""Pull fenced code blocks out of chat transcripts into files outside the wiki.

Usage:
  extract_code.py OUT_DIR CHAT.md [CHAT.md ...] [--copy FILE ...]

A block whose only line looks like a path (api/llm_client.py) names the next
block. Otherwise the first line `# path` / `// path` / `<!-- path -->` is used;
unnamed blocks go to _unnamed/. When a name repeats, the last version is the
file itself and earlier ones are kept in _history/<name>.vN. Each chat gets
its own subfolder; --copy files are copied as-is to OUT_DIR/extra/.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

FENCE = re.compile(r"^```([\w+-]*)\s*\n(.*?)^```\s*$", re.M | re.S)
PATHLIKE = re.compile(r"^[A-Za-z_][\w.\-]*(?:/[\w.\-]+)*\.(?:py|yml|yaml|html|sql|json|md|toml|txt|sh|js|css|env|cfg|ini|conf|cron|Dockerfile)$")
PRECEDE = re.compile(r"`?([A-Za-z_][\w.\-]*(?:/[\w.\-]+)*\.(?:py|yml|yaml|html|sql|json|md|toml|txt|sh|js|css|env|cfg|conf)|Dockerfile)`?\s*[:)*]*\s*$")
HEAD = re.compile(r"^(?:#|//|--|<!--)\s*([\w.\-]+(?:/[\w.\-]+)*\.\w{1,8})\s*(?:-->)?\s*$")
EXT = {"python": "py", "bash": "sh", "yaml": "yml", "javascript": "js", "json": "json", "html": "html",
       "sql": "sql", "env": "env", "cron": "cron", "markdown": "md", "text": "txt", "txt": "txt"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    ap.add_argument("chats", nargs="+", type=Path)
    ap.add_argument("--copy", nargs="*", type=Path, default=[])
    args = ap.parse_args()
    for chat in args.chats:
        base = args.out / chat.stem.split("-chat-")[-1][:40]
        text = chat.read_text(encoding="utf-8")
        pending: str | None = None
        seen: dict[str, int] = {}
        named = unnamed = 0
        for m in FENCE.finditer(text):
            lang, body = m.group(1).lower(), m.group(2)
            lines = body.strip().splitlines()
            if len(lines) == 1 and PATHLIKE.match(lines[0].strip()):
                pending = lines[0].strip()
                continue
            name = pending
            pending = None
            if not name and lines and (h := HEAD.match(lines[0].strip())):
                name = h.group(1)
            if not name:
                before = text[:m.start()].rstrip().splitlines()[-1:] or [""]
                if (pm := PRECEDE.search(before[0].strip(" #*>-"))) and len(before[0]) < 90:
                    name = pm.group(1)
            if not name:
                unnamed += 1
                if len(body.strip()) < 40:
                    continue
                name = f"_unnamed/{unnamed:03d}.{EXT.get(lang, 'txt')}"
            else:
                named += 1
            dest = base / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if name in seen and not name.startswith("_unnamed/"):
                hist = base / "_history" / f"{name}.v{seen[name]}"
                hist.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(dest, hist)
            seen[name] = seen.get(name, 0) + 1
            dest.write_text(body, encoding="utf-8")
        print(f"{chat.name}: {named} named blocks, {len(seen)} files, {unnamed} unnamed -> {base}")
    for f in args.copy:
        d = args.out / "extra"
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, d / f.name)
        print(f"copied {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
