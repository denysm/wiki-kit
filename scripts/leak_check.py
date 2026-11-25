#!/usr/bin/env python3
"""Leak check for a repository that must hold no data; the kit's pre-push hook runs it.

Usage:
  leak_check.py [--repo DIR] [--rev REV] [--history [--base REV ...]]
                [--names FILE] [--more-names FILE ...] [--patterns FILE] [--allow FILE]
                [--private-repo]

Checks the committed tree of REV (default HEAD), not the working copy:
  1. forbidden paths: topics/, raw/, inbox/, *.local.md (except catalog/raw/ and
     catalog/wiki/topics/, the public tool catalog); skipped with --private-repo,
     for the owner's private repositories that may hold a wiki of their own;
  2. private names: every line of --names (default
     ~/.config/wiki-kit/private-names.txt) is a case-insensitive regex, as in
     `grep -iEf`; file names are checked too; each --more-names list is added
     to it (a missing file is skipped: the kit's hook passes its kit-only list,
     names that private repositories may carry but this public one may not);
  3. secrets, internal hosts and infrastructure ids: the raw_check.py rules,
     with its internal-domains list.
--history also checks the lines added and the messages of the commits in REV
that are not in any --base (no --base: the whole history), because a leak
removed by a later commit still travels with the push.
Retired history: .leak-retired, written after a history rewrite, is read from
REV, from every --base found here and from the working copy at --repo. Its
lines: `before <ISO time with offset>`, `path <hash>` and `line <hash>` (the
first 24 hex digits of the SHA-256 of a dropped path, or of a dropped line
without its leading and trailing spaces).
  - a file at a listed path, or a line whose hash is listed, is refused in REV
    and, with --history, in every commit checked;
  - with --history and a --base found here, a commit not in any base and
    authored before the `before` time is refused: a clone made before the
    rewrite would bring the old history back by a merge or a rebase, which
    keep author dates. Without a base the dates are not compared.
A line of .leak-retired that does not parse, or a file with no `before`, is a
problem, so the rule never turns itself off in silence.

Matched values are never printed: only file or commit, line and kind.
Known false positives (code that describes secrets) are listed in .leak-allow
at the repository root, one `path kind count` per line; a file must then hold
exactly that many hits of that kind. Private names and forbidden paths cannot
be allowed; the one exception is the `Copyright (c) YEAR ...` line of LICENSE,
which names the copyright holder. Exit 0 clean, 1 findings.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import hashlib
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = Path.home() / ".config/wiki-kit/private-names.txt"
FORBIDDEN = re.compile(r"(^|/)(topics|raw|inbox)/|\.local\.md$")
# The public tool catalog is an llm-wiki topic: its raw/ and wiki/topics/ are public by design
# (docs/catalog-design.md). Private-name and secret checks still apply there.
CATALOG_OK = re.compile(r"^catalog/(raw|wiki/topics)/")


def forbidden_path(p: str) -> bool:
    """A data path; catalog/raw/ and catalog/wiki/topics/ pass unless the rest is a data path again."""
    if not FORBIDDEN.search(p):
        return False
    m = CATALOG_OK.match(p)
    return not m or p.endswith(".local.md") or bool(FORBIDDEN.search(p[m.end():]))
OWNER_LINE = re.compile(r"^Copyright \(c\) \d{4}(-\d{4})? \S")


def load_raw_check():
    spec = importlib.util.spec_from_file_location("raw_check", HERE / "raw_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], input=data, check=True,
                          capture_output=True).stdout


def tree(repo: Path, rev: str) -> dict[str, str]:
    """Path -> text of every text blob in REV (binary and non-UTF-8 files skipped)."""
    paths = [p for p in git(repo, "ls-tree", "-r", "-z", "--name-only", rev).decode().split("\0") if p]
    out = git(repo, "cat-file", "--batch", data="".join(f"{rev}:{p}\n" for p in paths).encode())
    files, pos = {}, 0
    for p in paths:
        end = out.index(b"\n", pos)
        size = int(out[pos:end].split()[2])
        blob = out[end + 1:end + 1 + size]
        pos = end + 2 + size
        if b"\0" in blob:
            continue
        try:
            files[p] = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return files


def known_bases(repo: Path, bases: list[str]) -> list[str]:
    """The bases present here; a base not fetched would make git log fail, so more is checked instead."""
    known = []
    for base in bases:
        if subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{base}^{{commit}}"],
                          capture_output=True).returncode == 0:
            known.append(base)
        else:
            print(f"warning: base {base} is not in this repository (fetch first?); "
                  "checking without it", file=sys.stderr)
    return known


GIT_ESCAPES = {"a": 7, "b": 8, "t": 9, "n": 10, "v": 11, "f": 12, "r": 13, '"': 34, "\\": 92}


def git_unquote(name: str) -> str:
    """A path as git prints it: possibly C-quoted, possibly with git's trailing TAB."""
    name = name.rstrip("\t")
    if name.startswith('"') and name.endswith('"') and len(name) > 1:
        raw, i, s = bytearray(), 0, name[1:-1]
        while i < len(s):
            if s[i] == "\\" and i + 1 < len(s):
                if s[i + 1].isdigit():
                    raw.append(int(s[i + 1:i + 4], 8))
                    i += 4
                    continue
                raw.append(GIT_ESCAPES.get(s[i + 1], ord(s[i + 1])))
                i += 2
                continue
            raw += s[i].encode("utf-8")
            i += 1
        name = raw.decode("utf-8", errors="replace")
    return name


def diff_path(name: str) -> str | None:
    """The path of a `+++ ` header: `b/...`; None for /dev/null."""
    name = git_unquote(name)
    return name[2:] if name.startswith("b/") else None


def history(repo: Path, rev: str, bases: list[str]) -> dict[str, tuple[int, list[tuple[str, int, str]], set[str]]]:
    """Commit -> (author time, [(path or '(message)', line in that commit's diff, text)] for added
    lines and messages, paths added or changed, binary and empty files included) for the commits
    of REV not in any of BASES (all present here)."""
    # the same output whatever the pusher's git config: fixed prefixes (diff.noprefix), no rename or
    # copy detection (a renamed file shows its lines), the root commit's diff (log.showRoot)
    args = ["-c", "core.quotePath=false", "log", "-p", "--raw", "--no-color", "--no-ext-diff", "--no-renames",
            "--root", "--src-prefix=a/", "--dst-prefix=b/", "--format=%x00%h %at%n%B%x00", rev]
    if bases:
        args += ["--not", *bases]
    out = git(repo, *args).decode("utf-8", errors="replace")
    commits: dict[str, tuple[int, list[tuple[str, int, str]], set[str]]] = {}
    parts = out.split("\0")
    # parts: '', 'sha time\nmessage', 'diff…', 'sha time\nmessage', 'diff…', ...
    for i in range(1, len(parts) - 1, 2):
        head, _, msg = parts[i].partition("\n")
        sha, _, at = head.partition(" ")
        rows = [("(message)", n, line) for n, line in enumerate(msg.splitlines(), 1)]
        path, in_header, changed = None, False, set()
        for n, line in enumerate(parts[i + 1].splitlines(), 1):
            if line.startswith(":") and "\t" in line:  # --raw: `:mode mode sha sha STATUS\tpath`; no hunk line starts with ':'
                status, _, name = line.partition("\t")
                if not status.endswith("D"):
                    changed.add(git_unquote(name))
            elif line.startswith("diff --git "):     # a file's header runs from here to its first hunk
                path, in_header = None, True
            elif in_header:
                if line.startswith("+++ "):
                    path = diff_path(line[4:])
                elif line.startswith("@@"):
                    in_header = False
            elif line.startswith("+") and path:
                rows.append((path, n, line[1:]))
        commits[sha] = (int(at), rows, changed)
    return commits


RETIRED_FILE = ".leak-retired"
HASH = re.compile(r"[0-9a-f]{24}")


def fingerprint(text: str) -> str:
    """The hash .leak-retired lists for a path or a line: 24 hex digits of its SHA-256."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:24]


class Retired:
    """What the .leak-retired files say: the latest `before` time, and the dropped paths and lines."""

    def __init__(self) -> None:
        self.cutoff: int | None = None
        self.cutoff_text = ""
        self.paths: set[str] = set()
        self.lines: set[str] = set()
        self.errors: list[str] = []

    def add(self, source: str, text: str) -> None:
        before = False
        for n, raw in enumerate(text.lstrip("\ufeff").splitlines(), 1):
            ln = raw.strip()
            if not ln or ln.startswith("#"):
                continue
            kind, _, value = ln.partition(" ")
            value = value.strip()
            if kind == "before":
                try:  # Python 3.9 reads neither `Z` nor `+0500`: write them as `+00:00` and `+05:00`
                    iso = re.sub(r"Z$", "+00:00", value)
                    iso = re.sub(r"([+-]\d\d)(\d\d)$", r"\1:\2", iso)
                    when = datetime.fromisoformat(iso)
                    if when.tzinfo is None:
                        raise ValueError(value)
                except ValueError:
                    self.errors.append(f"{source} line {n}: `before` needs an ISO time with its offset")
                    continue
                before = True
                if self.cutoff is None or int(when.timestamp()) > self.cutoff:
                    self.cutoff, self.cutoff_text = int(when.timestamp()), value
            elif kind in ("path", "line") and HASH.fullmatch(value):
                (self.paths if kind == "path" else self.lines).add(value)
            else:
                self.errors.append(f"{source} line {n}: expected `before <time>`, `path <hash>` or `line <hash>`")
        if not before:
            self.errors.append(f"{source}: no `before` line")


def load_names(path: Path) -> list[re.Pattern]:
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    return [re.compile(ln, re.I) for ln in lines if ln and not ln.startswith("#")]


def load_allow(text: str | None) -> dict[tuple[str, str], int]:
    allow = {}
    for ln in (text or "").splitlines():
        f = ln.split("#", 1)[0].split()
        if len(f) == 3 and f[2].isdigit():
            allow[(f[0], f[1])] = int(f[2])
    return allow


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--history", action="store_true", help="also check commits of REV not in any --base")
    ap.add_argument("--base", action="append", default=[], help="commit already pushed (repeatable)")
    ap.add_argument("--names", type=Path, default=NAMES)
    ap.add_argument("--private-repo", action="store_true",
                    help="a private repository: data paths allowed; names, secrets and hosts still checked")
    ap.add_argument("--more-names", type=Path, action="append", default=[],
                    help="another names list added to --names; skipped when missing (repeatable)")
    ap.add_argument("--patterns", type=Path, help="internal hosts, as raw_check.py --patterns")
    ap.add_argument("--allow", type=Path, help="false-positive list (default: .leak-allow in REV)")
    args = ap.parse_args()

    rc = load_raw_check()
    extra = rc.load_patterns(args.patterns)
    names = load_names(args.names) if args.names.exists() else []
    more_names = [n for more in args.more_names if more.exists() for n in load_names(more)]
    if not names:
        rest = "only the --more-names lists are checked" if more_names else "names not checked"
        print(f"warning: no private names list at {args.names}; {rest}", file=sys.stderr)
    names += more_names
    files = tree(args.repo, args.rev)
    allow = load_allow(args.allow.read_text(encoding="utf-8") if args.allow else files.get(".leak-allow"))
    problems = 0

    def report(where: str, what: str) -> None:
        nonlocal problems
        problems += 1
        print(f"{where}: {what}")

    def named(path: str, line: str) -> bool:
        if path == "LICENSE" and OWNER_LINE.match(line):
            return False
        return any(p.search(line) for p in names)

    def name_hits(text: str, path: str = "") -> list[int]:
        return [n for n, line in enumerate(text.splitlines(), 1) if named(path, line)]

    retired = Retired()
    if RETIRED_FILE in files:
        retired.add(f"{RETIRED_FILE} in {args.rev}", files[RETIRED_FILE])
    work_copy = args.repo / RETIRED_FILE
    if work_copy.is_file():
        retired.add(f"{RETIRED_FILE} in the working copy", work_copy.read_text(encoding="utf-8"))
    bases = known_bases(args.repo, args.base) if args.history else []
    for base in bases:  # what the remote already has also says what was dropped
        try:
            text = git(args.repo, "show", f"{base}:{RETIRED_FILE}").decode("utf-8")
        except subprocess.CalledProcessError:
            continue
        retired.add(f"{RETIRED_FILE} in base {base[:12]}", text)

    all_paths = git(args.repo, "ls-tree", "-r", "-z", "--name-only", args.rev).decode().split("\0")
    for p in filter(None, all_paths):
        if not args.private_repo and forbidden_path(p):
            report(p, "forbidden path (data never belongs in the kit)")
        if name_hits(p):
            report(p, "private name in the file name")
        if fingerprint(p) in retired.paths:
            report(p, f"path dropped from this history ({RETIRED_FILE})")

    for p, text in sorted(files.items()):
        lines = name_hits(text, p)
        if lines:
            report(p, f"private name, lines {','.join(map(str, lines[:10]))}")
        dropped = [n for n, line in enumerate(text.splitlines(), 1) if fingerprint(line.strip()) in retired.lines]
        if dropped:
            report(p, f"line dropped from this history ({RETIRED_FILE}), lines {','.join(map(str, dropped[:10]))}")
        kinds = Counter(k for _, k in rc.scan(text, extra))
        for kind, n in sorted(kinds.items()):
            if allow.get((p, kind)) != n:
                hit_lines = sorted({ln for ln, k in rc.scan(text, extra) if k == kind})
                report(p, f"{kind}={n} lines {','.join(map(str, hit_lines[:10]))}"
                          + (f" (.leak-allow expects {allow[(p, kind)]})" if (p, kind) in allow else ""))
    for (p, kind), n in sorted(allow.items()):
        if p not in files:
            print(f"note: .leak-allow lists {p}, which is not in {args.rev}", file=sys.stderr)

    if args.history:
        commits = history(args.repo, args.rev, bases)
        old = [sha for sha, (at, _, _) in commits.items()
               if bases and retired.cutoff is not None and at < retired.cutoff]
        if old:
            report(f"{len(old)} commit(s) ({', '.join(old[:5])}{', ...' if len(old) > 5 else ''})",
                   f"authored before {retired.cutoff_text}, when this history was rewritten ({RETIRED_FILE}): "
                   "they may bring the old history back. Keep your own work on a local branch you do not push, "
                   "run git fetch origin && git reset --hard origin/<branch>, then redo only your own "
                   "changes on top; never re-apply the old commits")
        for sha, (at, rows, changed) in commits.items():
            for path in sorted(changed | {path for path, _, _ in rows if path != "(message)"}):
                if fingerprint(path) in retired.paths:
                    report(f"commit {sha} {path}", f"path dropped from this history ({RETIRED_FILE})")
            for path, n, line in rows:
                if path != "(message)" and fingerprint(line.strip()) in retired.lines:
                    report(f"commit {sha} {path} (diff line {n})", f"line dropped from this history ({RETIRED_FILE})")
                where = f"commit {sha} {path} (diff line {n})"
                if named(path, line):
                    report(where, "private name")
                for _, kind in rc.scan(line, extra):
                    if (path, kind) not in allow:
                        report(where, kind)
        print(f"history: {len(commits)} commit(s) checked", file=sys.stderr)

    for err in dict.fromkeys(retired.errors):
        report(RETIRED_FILE, err)
    print(f"leak check: {len(files)} files in {args.rev}, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
