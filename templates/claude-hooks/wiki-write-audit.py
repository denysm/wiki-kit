#!/usr/bin/env python3
"""Claude Code PostToolUse hook for Write|Edit in a wiki hub.

1. Appends one JSON line per write to <project>/.claude/audit/writes.jsonl
   (add `.claude/audit/` to the hub's .gitignore).
2. For .md files inside a raw/, wiki/ or output/ folder runs the kit's
   raw_check.py. If that exits non-zero (secrets, internal hosts), the hook
   prints the findings to stderr and exits 2, so Claude sees them and fixes
   the file.

The kit location comes from $WIKI_KIT_DIR (default ~/Projects/wiki-kit).
"""
import datetime
import json
import os
import subprocess
import sys

KIT = os.path.expanduser(os.environ.get("WIKI_KIT_DIR", "~/Projects/wiki-kit"))
SCRIPT = os.path.join(KIT, "scripts", "raw_check.py")
CHECKED_DIRS = {"raw", "wiki", "output"}

try:
    ev = json.load(sys.stdin)
except Exception:
    sys.exit(0)
path = (ev.get("tool_input") or {}).get("file_path", "")
if not path:
    sys.exit(0)
root = os.environ.get("CLAUDE_PROJECT_DIR") or ev.get("cwd") or os.getcwd()
rel = os.path.relpath(path, root)

audit = os.path.join(root, ".claude", "audit")
os.makedirs(audit, exist_ok=True)
with open(os.path.join(audit, "writes.jsonl"), "a") as f:
    f.write(json.dumps({
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "tool": ev.get("tool_name"),
        "path": rel,
        "session": (ev.get("session_id") or "")[:8],
    }) + "\n")

if path.endswith(".md") and CHECKED_DIRS & set(rel.split(os.sep)[:-1]) and os.path.exists(SCRIPT):
    r = subprocess.run([sys.executable, "-I", SCRIPT, path], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"raw_check found something in {rel} (values are not shown, only kind and line):\n"
              + r.stdout.strip()[:1500], file=sys.stderr)
        sys.exit(2)
sys.exit(0)
