#!/usr/bin/env python3
"""Generate the parts list of a large plugin or skill collection for the tool catalog.

Usage:
  catalog_parts.py CLONE --repo OWNER/NAME --version V -o FILE [--date YYYY-MM-DD]

Reads a read-only clone and writes a raw `data` file for `catalog/raw/data/`
(docs/catalog-design.md, "Large collections"): one row per part,
`Part | Kind | Description | README sections | Path`.

Parts: every `SKILL.md` (kind skill, named by its frontmatter `name`, else its
folder), every `*.md` in a `commands/` folder (command), every `*.md` in an
`agents/` folder (agent), every `hooks/hooks.json` (hook, with its events).
Descriptions come from the parts' own frontmatter (first sentence, at most 300
characters); nothing is written by a model. README sections: the headings of
the clone's README.md under which a link to the part (its folder or file)
appears, else under which the part's name appears in backticks or bold.

Deterministic: the same clone, arguments and date give the same file. Stdlib
only; the frontmatter reader is the one of skill_check.py.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".github"}
DESC_MAX = 300
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK = re.compile(r"\]\(([^)\s]+)\)")


def load_skill_check():
    spec = importlib.util.spec_from_file_location("skill_check", HERE / "skill_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def walk(root: Path):
    out = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]) or not p.is_file():
            continue
        out.append(rel)
    return out


def one_line(text: str) -> str:
    text = " ".join(text.split())
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    first = m.group(1) if m else text
    if len(first) > DESC_MAX:
        first = first[: DESC_MAX - 1].rstrip() + "…"
    return first.replace("|", "\\|")


def front(sc, path: Path) -> dict:
    fields, _ = sc.parse_frontmatter(path.read_text(encoding="utf-8", errors="replace").splitlines())
    return {k: v for k, (v, _q) in (fields or {}).items()}


def find_parts(root: Path, sc) -> list[dict]:
    parts = []
    for rel in walk(root):
        p = root / rel
        if rel.name == "SKILL.md":
            f = front(sc, p)
            parts.append({"name": f.get("name") or rel.parent.name, "kind": "skill",
                          "desc": f.get("description", ""), "path": rel.parent.as_posix() + "/",
                          "file": rel.as_posix()})
        elif rel.suffix == ".md" and rel.parent.name in ("commands", "agents") and rel.name.lower() != "readme.md":
            f = front(sc, p)
            kind = "command" if rel.parent.name == "commands" else "agent"
            parts.append({"name": f.get("name") or rel.stem, "kind": kind,
                          "desc": f.get("description", ""), "path": rel.as_posix(), "file": rel.as_posix()})
        elif rel.name == "hooks.json" and rel.parent.name == "hooks":
            try:
                events = sorted(json.loads(p.read_text(encoding="utf-8")).get("hooks", {}))
            except (ValueError, AttributeError):
                events = []
            parts.append({"name": "hooks: " + (", ".join(events) or "unreadable"), "kind": "hook",
                          "desc": "Hook definitions for " + (", ".join(events) or "no readable events") + ".",
                          "path": rel.as_posix(), "file": rel.as_posix()})
    parts.sort(key=lambda d: (d["kind"], d["name"].lower(), d["path"]))
    return parts


def readme_sections(root: Path) -> list[tuple[str, str]]:
    """[(heading path, section text)] for the clone's README.md, each heading with its own text only."""
    readme = next((root / n for n in ("README.md", "readme.md", "Readme.md") if (root / n).exists()), None)
    if not readme:
        return []
    sections, stack, buf = [], [], []
    in_code = False

    def flush():
        if stack:
            sections.append((" > ".join(t for _l, t in stack), "\n".join(buf)))

    for line in readme.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING.match(line)
        if m:
            flush()
            buf = []
            level, title = len(m.group(1)), re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", r"\1", m.group(2)).strip()
            title = re.sub(r"^[^\w(]+", "", title).strip()  # leading emoji
            title = re.sub(r"\s*\(\d[^)]*\)$", "", title)  # trailing count, "(32 skills)"
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        else:
            buf.append(line)
    flush()
    return sections


def map_sections(parts: list[dict], sections: list[tuple[str, str]]) -> None:
    for part in parts:
        hits = []
        targets = {part["path"].rstrip("/"), part["file"]}
        name = re.escape(part["name"])
        spaced = name.replace(r"\-", r"[- ]")
        by_name = re.compile(r"(`%s`|\*\*%s\*\*|\[%s\]|(?<![\w/-])%s(?![\w/-]))" % (name, name, name, spaced)
                             if len(part["name"]) >= 3 else r"(`%s`|\*\*%s\*\*)" % (name, name), re.IGNORECASE)
        for heading, text in sections:
            links = {t.split("#")[0].lstrip("./").rstrip("/") for t in LINK.findall(text)}
            linked = any(t and (t in targets or t.startswith(part["path"]) or part["path"].rstrip("/").endswith(t)
                                and "/" in t) for t in links)
            if linked or (part["kind"] != "hook" and by_name.search(text)):
                leaf = heading.split(" > ")[-1]
                if leaf not in hits:
                    hits.append(leaf)
        part["sections"] = hits


def git_date(root: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cs"], capture_output=True,
                              text=True, check=True).stdout.strip() or "unknown"
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def render(parts, repo, version, date, source_date) -> str:
    owner_repo = repo.strip("/")
    counts = {k: sum(1 for p in parts if p["kind"] == k) for k in ("skill", "command", "agent", "hook")}
    count_text = ", ".join(f"{n} {k}{'s' if n != 1 else ''}" for k, n in counts.items() if n)
    # a version that starts with a digit is the tag without its "v"; any other version is the tag itself
    tag = "v" + version if version[:1].isdigit() else version
    lines = [
        "---",
        f'title: "Parts list: {owner_repo} {version}"',
        f'source: "https://github.com/{owner_repo}/tree/{tag}"',
        "type: data",
        f"ingested: {date}",
        "tags: [catalog, parts-list]",
        f'summary: "{len(parts)} parts of {owner_repo} at {version} ({count_text}), generated by catalog_parts.py from each part\'s own frontmatter."',
        "authors: [catalog_parts.py]",
        f"source_date: {source_date}",
        f"repo: {owner_repo}",
        f'version: "{version}"',
        "---",
        "",
        f"# Parts list: {owner_repo} {version}",
        "",
        f"Generated by `scripts/catalog_parts.py` from a clone at `{version}`; do not edit by hand. "
        f"{len(parts)} parts: {count_text}. Description: the first sentence of the part's own "
        "`description`. README sections: the README headings that link or name the part.",
        "",
        "| Part | Kind | Description | README sections | Path |",
        "|------|------|-------------|-----------------|------|",
    ]
    for p in parts:
        secs = "; ".join(s.replace("|", "\\|") for s in p["sections"]) or "none"
        lines.append(f"| `{p['name']}` | {p['kind']} | {one_line(p['desc']) or 'no description'} | {secs} | `{p['path']}` |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("clone", type=Path)
    ap.add_argument("--repo", required=True, help="GitHub OWNER/NAME")
    ap.add_argument("--version", required=True, help="the version read, as in the card")
    ap.add_argument("-o", "--output", type=Path, required=True)
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="ingested date (default: today)")
    args = ap.parse_args(argv)
    if not args.clone.is_dir():
        print(f"error: not a folder: {args.clone}", file=sys.stderr)
        return 2
    parts = find_parts(args.clone, load_skill_check())
    if not parts:
        print("error: no SKILL.md, commands/, agents/ or hooks/hooks.json found", file=sys.stderr)
        return 2
    map_sections(parts, readme_sections(args.clone))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(parts, args.repo, args.version, args.date, git_date(args.clone)), encoding="utf-8")
    unmapped = sum(1 for p in parts if not p["sections"])
    print(f"{args.output}: {len(parts)} parts, {unmapped} without a README section")
    return 0


if __name__ == "__main__":
    sys.exit(main())
