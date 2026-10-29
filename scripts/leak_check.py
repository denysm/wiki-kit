#!/usr/bin/env python3
"""Leak check for a repository that must hold no data; the kit's pre-push hook runs it.

Usage:
  leak_check.py [--repo DIR] [--rev REV] [--history [--base REV ...]]
                [--names FILE] [--patterns FILE] [--allow FILE]

Checks the committed tree of REV (default HEAD), not the working copy:
  1. forbidden paths: topics/, raw/, inbox/, *.local.md;
  2. private names: every line of --names (default
     ~/.config/wiki-kit/private-names.txt) is a case-insensitive regex, as in
     `grep -iEf`; file names are checked too;
  3. secrets, internal hosts and infrastructure ids: the raw_check.py rules,
     with its internal-domains list.
--history also checks the lines added and the messages of the commits in REV
that are not in any --base (no --base: the whole history), because a leak
removed by a later commit still travels with the push.

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
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = Path.home() / ".config/wiki-kit/private-names.txt"
FORBIDDEN = re.compile(r"(^|/)(topics|raw|inbox)/|\.local\.md$")
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


def history(repo: Path, rev: str, bases: list[str]) -> dict[str, list[tuple[str, int, str]]]:
    """Commit -> [(path or '(message)', line in that commit's diff, text)] for added lines and messages."""
    args = ["log", "-p", "--no-color", "--no-ext-diff", "--format=%x00%h%n%B%x00", rev]
    if bases:
        args += ["--not", *bases]
    out = git(repo, *args).decode("utf-8", errors="replace")
    commits: dict[str, list[tuple[str, int, str]]] = {}
    parts = out.split("\0")
    # parts: '', 'sha\nmessage', 'diff…', 'sha\nmessage', 'diff…', ...
    for i in range(1, len(parts) - 1, 2):
        sha, _, msg = parts[i].partition("\n")
        rows = [("(message)", n, line) for n, line in enumerate(msg.splitlines(), 1)]
        path = None
        for n, line in enumerate(parts[i + 1].splitlines(), 1):
            if line.startswith("+++ "):
                path = line[6:] if line.startswith("+++ b/") else None
            elif line.startswith("+") and path:
                rows.append((path, n, line[1:]))
        commits[sha] = rows
    return commits


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
    ap.add_argument("--patterns", type=Path, help="internal hosts, as raw_check.py --patterns")
    ap.add_argument("--allow", type=Path, help="false-positive list (default: .leak-allow in REV)")
    args = ap.parse_args()

    rc = load_raw_check()
    extra = rc.load_patterns(args.patterns)
    names = load_names(args.names) if args.names.exists() else []
    if not names:
        print(f"warning: no private names list at {args.names}; names not checked", file=sys.stderr)
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

    all_paths = git(args.repo, "ls-tree", "-r", "-z", "--name-only", args.rev).decode().split("\0")
    for p in filter(None, all_paths):
        if FORBIDDEN.search(p):
            report(p, "forbidden path (data never belongs in the kit)")
        if name_hits(p):
            report(p, "private name in the file name")

    for p, text in sorted(files.items()):
        lines = name_hits(text, p)
        if lines:
            report(p, f"private name, lines {','.join(map(str, lines[:10]))}")
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
        commits = history(args.repo, args.rev, args.base)
        for sha, rows in commits.items():
            for path, n, line in rows:
                where = f"commit {sha} {path} (diff line {n})"
                if named(path, line):
                    report(where, "private name")
                for _, kind in rc.scan(line, extra):
                    if (path, kind) not in allow:
                        report(where, kind)
        print(f"history: {len(commits)} commit(s) checked", file=sys.stderr)

    print(f"leak check: {len(files)} files in {args.rev}, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
