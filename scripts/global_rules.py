#!/usr/bin/env python3
"""Install the kit's personal rules for all projects into ~/.claude/CLAUDE.md.
Dry run unless --apply: prints what it would change.

  global_rules.py [--template FILE] [--target FILE] [--external DIR] [--apply]

--template defaults to templates/global-CLAUDE.md of this kit, --target to
~/.claude/CLAUDE.md (Claude Code reads it in every project on this computer).

- No target: it is created from the template.
- A target exists: every `## ` section of the template whose heading the target
  lacks (compared without case and surrounding spaces) is appended at its end, in
  template order. Sections already there are left as they are, even when their
  text differs from the template, and the target's own sections are never touched.
  Before the change the target is copied to <target>.bak-YYYYmmdd-HHMMSS.

In the template, `{KIT}` becomes this kit's folder and `{EXTERNAL}` the folder of
read-only third-party clones: --external DIR, else $WIKI_KIT_EXTERNAL, else
~/Projects/external; a path under the home folder is written with `~`.

Safe to run again: a target that has every heading is not written. Prints one line.
Exit 0 done (or nothing to do), 2 the template is missing or unreadable.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent


def sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split Markdown into the text before the first `## ` heading and
    (heading, block) pairs; headings inside ``` fences do not count."""
    head: list[str] = []
    out: list[tuple[str, list[str]]] = []
    fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            out.append((line[3:].strip(), [line]))
        elif out:
            out[-1][1].append(line)
        else:
            head.append(line)
    return "".join(head), [(h, "".join(b).rstrip("\n") + "\n") for h, b in out]


def tilde(p: Path) -> str:
    p = p.expanduser().resolve()
    try:
        return "~/" + p.relative_to(Path.home()).as_posix()
    except ValueError:
        return p.as_posix()


def key(heading: str) -> str:
    return " ".join(heading.split()).casefold()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--template", type=Path, default=KIT / "templates" / "global-CLAUDE.md")
    ap.add_argument("--target", type=Path, default=Path.home() / ".claude" / "CLAUDE.md")
    ap.add_argument("--external", type=Path, help="folder of read-only third-party clones ($EXTERNAL in catalog cards)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    external = a.external or Path(os.environ.get("WIKI_KIT_EXTERNAL") or "~/Projects/external")

    try:
        tpl = a.template.read_text(encoding="utf-8")
    except OSError as e:
        print(f"global rules: cannot read the template {a.template}: {e.strerror}", file=sys.stderr)
        return 2
    tpl = tpl.replace("{KIT}", tilde(KIT)).replace("{EXTERNAL}", tilde(external))
    _, tpl_sections = sections(tpl)
    target = a.target.expanduser()
    verb = "" if a.apply else "would be "

    if not target.exists():
        if a.apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(tpl, encoding="utf-8")
        print(f"global rules: {target} {verb}created ({len(tpl_sections)} sections)")
        return 0

    cur = target.read_text(encoding="utf-8")
    have = {key(h) for h, _ in sections(cur)[1]}
    missing = [(h, b) for h, b in tpl_sections if key(h) not in have]
    if not missing:
        print(f"global rules: {target} already has all {len(tpl_sections)} sections")
        return 0
    if a.apply:
        backup = target.with_name(f"{target.name}.bak-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(target, backup)
        body = cur.rstrip("\n") + "\n\n" + "\n".join(b for _, b in missing)
        target.write_text(body, encoding="utf-8")
    names = "; ".join(h for h, _ in missing)
    print(f"global rules: {len(missing)} sections {verb}added to {target}: {names}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
