#!/usr/bin/env python3
"""Claude Code PostToolUse hook (user level) for Write|Edit: audit and secret check in wiki roots.

Install once in ~/.claude/settings.json (merge into an existing "hooks" block):

  "hooks": {"PostToolUse": [{"matcher": "Write|Edit", "hooks": [{"type": "command",
      "command": "python3 -I \\"$HOME/<path to the kit>/scripts/wiki_write_audit.py\\""}]}]}

Behaviour:
- From the written file's path it walks up to $HOME looking for a wiki root (a folder with
  wikis.json, or with _index.md and raw/; the outermost one wins, so a topic inside a hub
  belongs to the hub). Outside any wiki it exits 0 at once and writes no log.
- Inside a wiki it appends one line to ~/.cache/wiki-kit/audit/writes.jsonl:
  ts, tool, root, path relative to the root, session.
- For .md files under raw/, wiki/ or output/ it checks the text with the kit's raw_check.py
  rules. A finding makes the hook exit 2, and Claude sees the message (kinds and line
  numbers, never values). In *.local.md files (verbatim exports from corporate systems)
  internal hosts, URLs, cloud ARNs and account ids are expected and not findings; secrets are.
"""
from __future__ import annotations

import datetime
import json
import os
import sys
from pathlib import Path

LOG = Path.home() / ".cache" / "wiki-kit" / "audit" / "writes.jsonl"
CHECKED_DIRS = {"raw", "wiki", "output"}
MESSAGE = ("скажи пользователю; вне raw/ замени значение на [REDACTED:secret]; "
           "в raw/ правь только с согласия пользователя")


def find_root(path: Path) -> Path | None:
    home, found = Path.home().resolve(), None
    for p in path.parents:
        if p == home or home not in p.parents:
            break
        if (p / "wikis.json").is_file() or ((p / "_index.md").is_file() and (p / "raw").is_dir()):
            found = p
    return found


def check(path: Path, rel_parts: tuple) -> list[tuple[int, str]]:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import raw_check
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    extra = raw_check.load_patterns(None)
    hits = raw_check.scan(text, extra)
    if path.name.endswith(".local.md"):
        kinds = {k for _, k in hits} - raw_check.INTERNAL_KINDS
        hits = [h for h in hits if h[1] in kinds]
    return hits


def main() -> int:
    try:
        ev = json.load(sys.stdin)
        fp = (ev.get("tool_input") or {}).get("file_path", "")
        if not fp:
            return 0
        path = Path(fp)
        if not path.is_absolute():
            path = Path(ev.get("cwd") or os.getcwd()) / path
        path = Path(os.path.abspath(path))
        root = find_root(path)
        if root is None:
            return 0
        rel = path.relative_to(root)
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": datetime.datetime.now().isoformat(timespec="seconds"),
                "tool": ev.get("tool_name"),
                "root": str(root).replace(str(Path.home()), "~", 1),
                "path": str(rel),
                "session": (ev.get("session_id") or "")[:8],
            }, ensure_ascii=False) + "\n")
        if path.suffix == ".md" and CHECKED_DIRS & set(rel.parts[:-1]) and path.exists():
            hits = check(path, rel.parts)
            if hits:
                kinds = ", ".join(f"{k} (line {n})" for n, k in hits[:12])
                print(f"raw_check found in {rel}: {kinds}{' …' if len(hits) > 12 else ''}. "
                      f"Values are not shown. {MESSAGE}", file=sys.stderr)
                return 2
    except Exception as e:  # a broken hook must never block work
        print(f"wiki_write_audit: {type(e).__name__}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
