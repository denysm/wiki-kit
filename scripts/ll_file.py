#!/usr/bin/env python3
"""File a lessons-learned note into its wiki in one call: notes index row, log line,
state bullets, commit. Dry run unless --apply: prints what it would change.

  ll_file.py NOTE [--articles M] [--theme TEXT]
             [--state TEXT ...] [--state-section TITLE] [--readme PATH]
             [--names FILE] [--commit [--push] [--co-author LINE] [--message TEXT]] [--apply]

NOTE is <wiki root>/raw/notes/YYYY-MM-DD-ll-<slug>.md (or .local.md), already written.
From its frontmatter (title, summary, tags, ingested/updated, source_date, lesson_count):

- raw/notes/_index.md gets the row `llm-wiki lint` would generate for it, in file-name
  order, and its "Last updated" date; the file is created if missing;
- <wiki root>/log.md gets
  `## [source_date] ll | "<theme>" → raw/notes/<file> (N lessons, M articles updated)`;
  <theme> is the title without "Lessons Learned: " (or --theme), M is --articles (0);
- --state TEXT (repeatable) appends a bullet to the last `## ` section of the hub
  README.md (the outermost wiki root above NOTE; --readme for another file);
  --state-section TITLE appends to the section `## TITLE` instead, created at the end
  if missing;
- --commit adds only these files (a git-ignored *.local.md note is skipped) and commits
  `ll: <topic> — N lessons: <theme>` (+ `; docs: README state`) with a Co-Authored-By
  line (--co-author, else $WIKI_KIT_CO_AUTHOR, else "Claude <noreply@anthropic.com>";
  "" for none); --push pushes after it. Other staged changes stay out of the commit.

A row whose link already points to NOTE, a log line naming it and a bullet already in
the section are left alone, so a second run adds nothing.

Writes from a script bypass the Write/Edit audit hook, so the script applies its rules
itself: raw_check.py (sibling module) scans NOTE and every --state text, and adds the
--wiki structure rules for NOTE (--names FILE as in raw_check.py). A secret or internal
host (in *.local.md: a secret), or a structure error, refuses the run with exit 2 and
writes nothing. Writes are logged to the audit log like the hook does.

Exit codes: 0 done (or dry run), 1 bad input or git failure, 2 refused by the checks.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling import under python3 -I
import raw_check  # noqa: E402
from wiki_write_audit import LOG as AUDIT_LOG, find_root  # noqa: E402

NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-ll-[\w.-]+\.md$")
LINK_RE = re.compile(r"\]\((<([^>\n]+)>|([^)\n]+))\)")
LESSON_RE = re.compile(r"(?m)^## Lesson \d+\b")
SESSION_RE = re.compile(r"\bsession ([0-9a-f]{8})\b")
DEFAULT_CO_AUTHOR = "Claude <noreply@anthropic.com>"


# --- frontmatter and index row exactly as llm-wiki lint (v1.0.0) builds them ----------

def _split_inline_list(value: str) -> list[str]:
    parts, current, quote = [], [], None
    for char in value:
        if char in {"'", '"'}:
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            current.append(char)
        elif char == "," and quote is None:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    parts.append("".join(current).strip())
    return parts


def _scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [_scalar(p) for p in _split_inline_list(inner)] if inner else []
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data, key = {}, None
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and key:
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(_scalar(line[4:]))
            continue
        if line.startswith(" ") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        key = k.strip()
        data[key] = _scalar(v) if v.strip() else []
    return data


def cell(value) -> str:
    return re.sub(r"\s+", " ", str(value)).replace("|", "\\|").strip()


def link_dest(path: str) -> str:
    return f"<{path}>" if any(c.isspace() for c in path) or ")" in path else path


def index_row(name: str, fm: dict) -> str:
    tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
    updated = fm.get("updated") or fm.get("ingested") or fm.get("created") or ""
    return (f"| [{cell(fm.get('title') or Path(name).stem)}]({link_dest(name)}) | "
            f"{cell(fm.get('summary') or '')} | {cell(', '.join(map(str, tags)))} | {cell(updated)} |")


INDEX_HEAD = ("# Notes Index\n\n> Generated by local llm-wiki lint.\n\nLast updated: {today}\n\n"
              "## Contents\n\n| File | Summary | Tags | Updated |\n|------|---------|------|---------|\n")


# --- planning: each returns (new text or None when unchanged, report line) --------------

def plan_index(path: Path, name: str, row: str, today: str):
    text = path.read_text(encoding="utf-8") if path.exists() else INDEX_HEAD.format(today=today)
    lines = text.split("\n")
    rows = [(i, (m.group(2) or m.group(3))) for i, l in enumerate(lines)
            if l.startswith("| [") and (m := LINK_RE.search(l))]
    for i, dest in rows:
        if dest == name:
            same = lines[i] == row
            return None, "row present, skipped" + ("" if same else " (differs from frontmatter; left as is)")
    after = [i for i, dest in rows if "/" not in dest and dest > name]
    if after:
        at = after[0]
    elif rows:
        at = rows[-1][0] + 1
    else:
        at = next(i for i, l in enumerate(lines) if l.startswith("|---")) + 1
    lines.insert(at, row)
    lines = [f"Last updated: {today}" if l.startswith("Last updated: ") else l for l in lines]
    return "\n".join(lines), ("created, " if not path.exists() else "") + f"+1 row at line {at + 1}"


def plan_log(path: Path, name: str, line: str):
    text = path.read_text(encoding="utf-8") if path.exists() else "# Wiki Activity Log\n"
    target = f"raw/notes/{name}"
    if any(" ll |" in l and target in l for l in text.splitlines()):
        return None, "line present, skipped"
    return text.rstrip("\n") + "\n\n" + line + "\n", "+1 line"


def plan_state(path: Path, bullets: list[str], section: str | None):
    lines = path.read_text(encoding="utf-8").rstrip("\n").split("\n")
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    if section:
        found = [i for i in heads if lines[i].strip() == "## " + section.strip()]
        start = found[-1] if found else None
    else:
        if not heads:
            raise SystemExit(f"{path}: no '## ' section to append to; pass --state-section")
        start = heads[-1]
    if start is None:
        new = [b for b in dict.fromkeys(bullets)]
        lines += ["", "## " + section.strip(), ""] + new
        where = f'new section "{section.strip()}"'
    else:
        end = next((h for h in heads if h > start), len(lines))
        present = {l.strip() for l in lines[start:end]}
        new = [b for b in dict.fromkeys(bullets) if b.split("\n")[0].strip() not in present]
        pos = end
        while pos > start + 1 and not lines[pos - 1].strip():
            pos -= 1
        block = [*new, ""] if new and pos < len(lines) and lines[pos].startswith("## ") else new
        lines[pos:pos] = block
        where = f'section "{lines[start][3:].strip()}"'
    skipped = len(set(bullets)) - len(new)
    report = f"{where}: +{len(new)} bullet(s)" + (f", {skipped} present, skipped" if skipped else "")
    return ("\n".join(lines) + "\n" if new else None), report


# --- checks, git, audit ----------------------------------------------------------------

def check(note: Path, text: str, states: list[str], names: list[str]) -> list[str]:
    """Return refusal reasons (values never shown); print warnings."""
    refuse = []
    extra = raw_check.load_patterns(None)
    for n, sev, rule, excerpt in raw_check.wiki_findings(note, text, names):
        msg = f"{note.name}:{n}: {sev} {rule}" + (f": {excerpt}" if excerpt else "")
        (refuse.append(msg) if sev == "error" else print("warning", msg))
    hits = raw_check.scan(text, extra)
    if note.name.endswith(".local.md"):
        hits = [h for h in hits if h[1] not in raw_check.INTERNAL_KINDS]
    if hits:
        refuse.append(f"{note.name}: " + ", ".join(f"{k} (line {n})" for n, k in hits[:12]))
    for i, s in enumerate(states, 1):
        hits = raw_check.scan(s, extra)
        if hits:
            refuse.append(f"--state #{i}: " + ", ".join(sorted({k for _, k in hits})))
    return refuse


def git(repo: Path, *args: str, check_rc: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check_rc and r.returncode:
        raise SystemExit(f"git {' '.join(args[:2])} failed: {(r.stderr or r.stdout).strip()[-400:]}")
    return r


def audit(paths: list[Path], session: str) -> None:
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        with AUDIT_LOG.open("a", encoding="utf-8") as f:
            for p in paths:
                root = find_root(p)
                if root is None:
                    continue
                f.write(json.dumps({"ts": ts, "tool": "ll_file.py",
                                    "root": str(root).replace(str(Path.home()), "~", 1),
                                    "path": str(p.relative_to(root)), "session": session},
                                   ensure_ascii=False) + "\n")
    except OSError as e:  # the audit log must never block filing
        print(f"audit log: {e}", file=sys.stderr)


def plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note", type=Path, help="raw/notes/YYYY-MM-DD-ll-<slug>.md, already written")
    ap.add_argument("--articles", type=int, default=0, help="articles updated from these lessons (log line)")
    ap.add_argument("--theme", help='session theme for the log and commit (default: title without "Lessons Learned: ")')
    ap.add_argument("--state", action="append", default=[], help="bullet for the state section (repeatable)")
    ap.add_argument("--state-section", help="append to the section '## TITLE' (created if missing)")
    ap.add_argument("--readme", type=Path, help="state file (default: README.md of the outermost wiki root)")
    ap.add_argument("--names", type=Path, help="customer/prospect names for the raw_check --wiki rule")
    ap.add_argument("--commit", action="store_true", help="commit only the touched files")
    ap.add_argument("--push", action="store_true", help="with --commit: git push afterwards")
    ap.add_argument("--co-author", help="Co-Authored-By value; empty string for none")
    ap.add_argument("--message", help="first line of the commit message instead of the generated one")
    ap.add_argument("--apply", action="store_true", help="write and commit; without it only print the plan")
    a = ap.parse_args()

    note = Path(os.path.abspath(a.note))
    if not note.is_file():
        print(f"not a file: {a.note}", file=sys.stderr)
        return 1
    if not NAME_RE.match(note.name) or note.parent.name != "notes" or note.parent.parent.name != "raw":
        print(f"expected <wiki root>/raw/notes/YYYY-MM-DD-ll-<slug>.md, got {a.note}", file=sys.stderr)
        return 1
    wiki = note.parents[2]
    text = note.read_text(encoding="utf-8")
    fm = frontmatter(text)
    missing = [k for k in ("title", "summary", "source_date", "lesson_count") if not fm.get(k)]
    if missing:
        print(f"{note.name}: frontmatter lacks {', '.join(missing)}", file=sys.stderr)
        return 1
    try:
        count = int(fm["lesson_count"])
    except ValueError:
        print(f"{note.name}: lesson_count is not a number", file=sys.stderr)
        return 1
    headings = len(LESSON_RE.findall(text))
    if headings != count:
        print(f"warning: lesson_count {count}, but {headings} '## Lesson N' headings")
    names = ([n.strip() for n in a.names.read_text(encoding="utf-8").splitlines()
              if n.strip() and not n.startswith("#")] if a.names else [])
    bullets = [s.strip() if s.strip().startswith("- ") else "- " + s.strip() for s in a.state if s.strip()]
    bullets = [b.replace("\n", "\n  ") for b in bullets]

    refuse = check(note, text, a.state, names)
    if refuse:
        print("refused by raw_check rules, nothing written (values not shown):")
        print("\n".join("  " + r for r in refuse))
        return 2

    title = str(fm["title"])
    theme = a.theme or re.sub(r"(?i)^lessons learned:\s*", "", title)
    today = datetime.date.today().isoformat()
    repo_r = git(wiki, "rev-parse", "--show-toplevel", check_rc=False)
    repo = Path(repo_r.stdout.strip()) if repo_r.returncode == 0 else None
    base = repo or wiki
    rel = lambda p: os.path.relpath(p, base)  # noqa: E731

    log_line = (f'## [{fm["source_date"]}] ll | "{theme}" → raw/notes/{note.name} '
                f'({plural(count, "lesson")}, {plural(a.articles, "article")} updated)')
    index = note.parent / "_index.md"
    changes: dict[Path, str] = {}
    new, msg = plan_index(index, note.name, index_row(note.name, fm), today)
    print(f"index  {rel(index)}: {msg}")
    if new is not None:
        changes[index] = new
    log = wiki / "log.md"
    new, msg = plan_log(log, note.name, log_line)
    print(f"log    {rel(log)}: {msg}" + (f"\n       {log_line}" if new is not None else ""))
    if new is not None:
        changes[log] = new
    readme = None
    if bullets:
        hub = next((p for p in reversed(note.parents) if (p / "wikis.json").is_file()), wiki)
        readme = Path(os.path.abspath(a.readme)) if a.readme else hub / "README.md"
        if not readme.is_file():
            print(f"no state file {readme}; pass --readme", file=sys.stderr)
            return 1
        new, msg = plan_state(readme, bullets, a.state_section)
        print(f"state  {rel(readme)}: {msg}")
        if new is not None:
            changes[readme] = new

    if a.apply:
        for p, t in changes.items():
            p.write_text(t, encoding="utf-8")
        m = SESSION_RE.search(title)
        audit(list(changes), m.group(1) if m else "")

    if a.commit:
        if repo is None:
            print(f"commit: {wiki} is not in a git repository", file=sys.stderr)
            return 1
        repo = repo.resolve()
        paths = list(dict.fromkeys(p.resolve() for p in [note, index, log] + ([readme] if readme else [])))
        inside = [p for p in paths if repo in p.parents]
        for p in paths:
            if p not in inside:
                print(f"commit: {p} is outside {repo}, not committed")
        ignored = {p for p in inside if git(repo, "check-ignore", "-q", str(p), check_rc=False).returncode == 0}
        files = [str(p.relative_to(repo)) for p in inside if p not in ignored]
        topic = wiki.parent.name if wiki.name == ".wiki" else wiki.name
        head = a.message or (f"ll: {topic} — {plural(count, 'lesson')}: {theme}"
                             + ("; docs: README state" if readme in changes else ""))
        co = a.co_author if a.co_author is not None else os.environ.get("WIKI_KIT_CO_AUTHOR", DEFAULT_CO_AUTHOR)
        message = head + (f"\n\nCo-Authored-By: {co}" if co else "")
        if not a.apply:
            print(f"commit (dry run) {len(files)} file(s) if changed: {head}")
        else:
            git(repo, "add", "--", *files)
            if git(repo, "diff", "--cached", "--quiet", "--", *files, check_rc=False).returncode == 0:
                print("commit: nothing to commit")
            else:
                git(repo, "commit", "-q", "-m", message, "--", *files)
                sha = git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
                print(f"commit {sha} in {repo.name}: {head}")
                if a.push:
                    r = git(repo, "push", "-q", check_rc=False)
                    if r.returncode:
                        print(f"push refused: {(r.stderr or r.stdout).strip()[-600:]}", file=sys.stderr)
                        return 1
                    print("pushed")
    if not a.apply:
        print("dry run: nothing written" + ("" if changes else ", nothing to change") + "; add --apply to write")
    else:
        print(f"applied: {len(changes)} file(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
