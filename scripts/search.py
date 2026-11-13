#!/usr/bin/env python3
"""Full-text search over a wiki root: SQLite FTS5, BM25, standard library only.

Usage:
  search.py index ROOT...                       # (re)build or refresh the index, incrementally
  search.py query "text" [--root ROOT ...] [--kind raw|wiki|output ...] [--topic NAME ...]
                         [-n 10] [--json] [--long]
  search.py eval FILE [-n 10] [--mode MODE]     # recall@5 and recall@10 on a question set

ROOT is a folder with wikis.json (a hub: topics live in topics/<name>/) or a folder
with _index.md and raw/ (a single wiki, for example a customer repository's .wiki/).
Only .md files in raw/, wiki/ and output/ are indexed, in chunks cut at headings (long
sections are cut further), each with its line range, heading, kind and topic.

`query` without --root uses the root found by walking up from the current folder.
It refreshes a stale index first (by file mtime and size). Several roots are searched
together only when you name each one with --root; roots of different customers must
not be mixed. Default output is one short block per hit: path:line, heading, score,
one snippet line. --long prints the whole chunk, --json prints records.

The index is a cache, one database per root, in ~/.cache/wiki-kit/search/ (mode 600).
It holds the text of *.local.md files, so it never goes into a repository. Delete it
at any time; the next call rebuilds it.

Morphology: the default mode "hybrid" fuses two rankings (reciprocal rank fusion): exact
words, and stems (two letters cut off a word of 5+ letters, at least four kept) matched by
prefix, so Russian and French inflections (серверами / сервер) find each other without
losing exact hits. --mode plain|prefix|hybrid is for comparison. Measured on a local
question set, hybrid beat exact-only, prefix-only, Porter stemming and a trigram index.

eval FILE: tab-separated lines `question<TAB>root<TAB>expected file relative to root`
(further columns and lines starting with # are ignored). A question counts as found at
rank k when the expected file is among the first k distinct files of the answer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

VERSION = 3
CACHE = Path.home() / ".cache" / "wiki-kit" / "search"
KINDS = ("raw", "wiki", "output")
MAX_CHUNK = 1800          # characters; longer sections are cut at blank lines
MODES = ("plain", "prefix", "hybrid")
DEFAULT_MODE = "hybrid"
WORD = re.compile(r"\w+", re.U)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
STOP = {
    "the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are", "was", "were", "what", "which",
    "who", "how", "when", "where", "why", "does", "do", "did", "with", "by", "at", "from", "that", "this", "it",
    "и", "в", "на", "с", "по", "что", "как", "какой", "какая", "какие", "какое", "где", "когда", "кто", "для",
    "из", "от", "до", "за", "это", "ли", "не", "к", "о", "об", "про", "или", "а", "но", "у",
    "le", "la", "les", "un", "une", "des", "du", "de", "et", "est", "que", "qui", "quel", "quelle", "quels",
    "quelles", "dans", "pour", "par", "sur", "au", "aux", "en", "ce", "se", "ne", "pas",
}


# ---------------------------------------------------------------- roots

def find_root(start: Path) -> Path | None:
    for p in [start, *start.parents]:
        if (p / "wikis.json").is_file() or ((p / "_index.md").is_file() and (p / "raw").is_dir()):
            return p
    return None


def check_root(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if (p / "wikis.json").is_file() or ((p / "_index.md").is_file() and (p / "raw").is_dir()):
        return p
    sys.exit(f"not a wiki root (needs wikis.json, or _index.md and raw/): {p}")


def wiki_dirs(root: Path):
    """Yield (topic, folder) for every wiki folder under a root."""
    if (root / "wikis.json").is_file():
        topics = root / "topics"
        if topics.is_dir():
            for t in sorted(topics.iterdir()):
                if t.is_dir() and not t.name.startswith("."):
                    yield t.name, t
        yield "hub", root
    else:
        name = root.parent.name if root.name.startswith(".") else root.name
        yield name, root


def scan_files(root: Path):
    """Yield (relative path, kind, topic, absolute path) for every indexable file."""
    for topic, base in wiki_dirs(root):
        for kind in KINDS:
            d = base / kind
            if not d.is_dir():
                continue
            for dirpath, dirnames, filenames in os.walk(d):
                dirnames[:] = sorted(x for x in dirnames if not x.startswith("."))
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        f = Path(dirpath) / fn
                        yield str(f.relative_to(root)), kind, topic, f


def db_path(root: Path) -> Path:
    h = hashlib.sha1(str(root).encode()).hexdigest()[:10]
    return CACHE / f"{root.name.lstrip('.') or 'root'}-{h}.db"


# ---------------------------------------------------------------- chunking

def parse_frontmatter_title(lines: list[str]) -> tuple[str, int]:
    """Return (title, index of the first line after the frontmatter)."""
    if not lines or lines[0].strip() != "---":
        return "", 0
    title = ""
    for i in range(1, min(len(lines), 80)):
        if lines[i].strip() == "---":
            return title, i + 1
        m = re.match(r"^title:\s*(.*)$", lines[i])
        if m:
            title = m.group(1).strip().strip("\"'")
    return "", 0


def chunk(text: str):
    """Yield (heading, first line, last line, text); line numbers are 1-based."""
    lines = text.splitlines()
    title, start = parse_frontmatter_title(lines)
    heading, h_start, buf = title, start + 1, []
    fence = False
    out = []

    def flush(end_line):
        body = "\n".join(buf).strip()
        if body:
            out.append((heading, h_start, end_line, body))

    for i in range(start, len(lines)):
        line = lines[i]
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        m = None if fence else HEADING.match(line)
        if m:
            flush(i)
            heading, h_start, buf = m.group(2), i + 1, [line]
        else:
            buf.append(line)
    flush(len(lines))

    for heading, a, b, body in out:
        if len(body) <= MAX_CHUNK:
            yield heading, a, b, title, body
            continue
        # cut a long section into pieces at line boundaries, keep exact line numbers
        cur, cur_len, cur_a = [], 0, a
        for n, line in enumerate(body.splitlines(), a):
            if cur_len + len(line) > MAX_CHUNK and cur and (not line.strip() or cur_len > MAX_CHUNK * 1.4):
                yield heading, cur_a, n - 1, title, "\n".join(cur)
                cur, cur_len, cur_a = [], 0, n
            cur.append(line)
            cur_len += len(line) + 1
        if cur:
            yield heading, cur_a, b, title, "\n".join(cur)


# ---------------------------------------------------------------- index

TOKENIZER = "unicode61 remove_diacritics 2"


def open_db(root: Path) -> sqlite3.Connection:
    CACHE.mkdir(parents=True, exist_ok=True)
    os.chmod(CACHE, 0o700)
    path = db_path(root)
    want = str(VERSION)
    if path.exists():
        try:
            c = sqlite3.connect(path)
            got = c.execute("SELECT v FROM meta").fetchone()
            c.close()
        except sqlite3.Error:
            got = None
        if not got or got[0] != want:
            path.unlink()
    db = sqlite3.connect(path)
    os.chmod(path, 0o600)
    db.executescript(
        "CREATE TABLE IF NOT EXISTS meta(v TEXT);"
        "CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, mtime_ns INTEGER, size INTEGER);"
        "CREATE TABLE IF NOT EXISTS chunks(id INTEGER PRIMARY KEY, path TEXT, kind TEXT, topic TEXT, title TEXT,"
        " heading TEXT, line_a INTEGER, line_b INTEGER);"
        "CREATE INDEX IF NOT EXISTS chunks_path ON chunks(path);"
    )
    if not db.execute("SELECT 1 FROM meta").fetchone():
        db.execute("INSERT INTO meta VALUES (?)", (want,))
        db.execute(f"CREATE VIRTUAL TABLE fts USING fts5(heading, title, text, tokenize='{TOKENIZER}')")
        db.commit()
    return db


def refresh(root: Path) -> dict:
    db = open_db(root)
    known = {p: (m, s) for p, m, s in db.execute("SELECT path, mtime_ns, size FROM files")}
    seen, todo = set(), []
    for rel, kind, topic, f in scan_files(root):
        seen.add(rel)
        st = f.stat()
        if known.get(rel) != (st.st_mtime_ns, st.st_size):
            todo.append((rel, kind, topic, f, st))
    gone = [p for p in known if p not in seen]

    def drop(rel):
        ids = [r[0] for r in db.execute("SELECT id FROM chunks WHERE path=?", (rel,))]
        db.executemany("DELETE FROM fts WHERE rowid=?", [(i,) for i in ids])
        db.execute("DELETE FROM chunks WHERE path=?", (rel,))
        db.execute("DELETE FROM files WHERE path=?", (rel,))

    for rel in gone:
        drop(rel)
    n_chunks = 0
    for rel, kind, topic, f, st in todo:
        drop(rel)
        text = f.read_text(encoding="utf-8", errors="replace")
        for heading, a, b, title, body in chunk(text):
            cur = db.execute("INSERT INTO chunks(path, kind, topic, title, heading, line_a, line_b)"
                             " VALUES (?,?,?,?,?,?,?)", (rel, kind, topic, title, heading, a, b))
            db.execute("INSERT INTO fts(rowid, heading, title, text) VALUES (?,?,?,?)",
                       (cur.lastrowid, heading, title, body))
            n_chunks += 1
        db.execute("INSERT INTO files VALUES (?,?,?)", (rel, st.st_mtime_ns, st.st_size))
    db.commit()
    stats = {"files_new_or_changed": len(todo), "files_removed": len(gone), "chunks_added": n_chunks,
             "files": len(seen)}
    db.close()
    return stats


# ---------------------------------------------------------------- query

def terms(text: str) -> list[str]:
    seen, out = set(), []
    for w in WORD.findall(text.lower()):
        if w in STOP or w in seen or (len(w) < 2 and not w.isdigit()):
            continue
        seen.add(w)
        out.append(w)
    return out


def stem(w: str) -> str:
    return w[: max(4, len(w) - 2)] if len(w) >= 5 else w


def match_expr(text: str, mode: str) -> str:
    ts = terms(text)
    if not ts:
        return ""
    if mode == "prefix":
        parts = [f'"{stem(t)}"*' if len(t) >= 5 else f'"{t}"' for t in ts]
    else:
        parts = [f'"{t}"' for t in ts]
    return " OR ".join(parts)


def search_root(root: Path, text: str, mode: str, kinds, topics, limit: int):
    if mode == "hybrid":  # reciprocal rank fusion of exact and stem-prefix matching
        fused, by_key = {}, {}
        for m in ("plain", "prefix"):
            for rank, h in enumerate(search_root(root, text, m, kinds, topics, limit * 3)):
                k = (h["path"], h["line"])
                by_key.setdefault(k, h)
                fused[k] = fused.get(k, 0) + 1.0 / (60 + rank)
        top = sorted(fused, key=lambda k: -fused[k])[:limit]
        return [dict(by_key[k], score=round(fused[k] * 100, 2)) for k in top]
    refresh(root)
    expr = match_expr(text, mode)
    if not expr:
        return []
    db = sqlite3.connect(db_path(root))
    where, args = [f"fts MATCH ?"], [expr]
    if kinds:
        where.append("c.kind IN (%s)" % ",".join("?" * len(kinds)))
        args += kinds
    if topics:
        where.append("c.topic IN (%s)" % ",".join("?" * len(topics)))
        args += topics
    # bm25 column weights: heading 4, title 2, text 1
    sql = (f"SELECT c.path, c.kind, c.topic, c.heading, c.line_a, c.line_b, bm25(fts, 4.0, 2.0, 1.0) AS s, "
           f"snippet(fts, 2, '[', ']', ' … ', 24), fts.text "
           f"FROM fts JOIN chunks c ON c.id = fts.rowid WHERE {' AND '.join(where)} "
           f"ORDER BY s LIMIT ?")
    try:
        rows = db.execute(sql, args + [limit]).fetchall()
    except sqlite3.OperationalError as e:
        sys.exit(f"search failed: {e}")
    finally:
        db.close()
    return [{"root": str(root), "path": r[0], "kind": r[1], "topic": r[2], "heading": r[3], "line": r[4],
             "line_end": r[5], "score": round(-r[6], 2), "snippet": " ".join(r[7].split()), "text": r[8]}
            for r in rows]


def cmd_index(args) -> int:
    for r in args.roots:
        root = check_root(r)
        t = time.time()
        s = refresh(root)
        size = db_path(root).stat().st_size / 1e6
        print(f"{root}: {s['files']} files, +{s['files_new_or_changed']} new/changed, -{s['files_removed']} removed, "
              f"+{s['chunks_added']} chunks, {time.time() - t:.2f}s, index {size:.1f} MB ({db_path(root)})")
    return 0


def cmd_query(args) -> int:
    roots = [check_root(r) for r in args.root] if args.root else []
    if not roots:
        found = find_root(Path.cwd())
        if not found:
            sys.exit("no wiki root here; give --root ROOT")
        roots = [found]
    hits = []
    for root in roots:
        hits += search_root(root, args.text, args.mode, args.kind, args.topic, args.n)
    hits.sort(key=lambda h: -h["score"])
    hits = hits[: args.n]
    if args.json:
        for h in hits:
            h.pop("text", None) if not args.long else None
        print(json.dumps(hits, ensure_ascii=False, indent=1))
        return 0
    if not hits:
        print("no hits")
        return 1
    for h in hits:
        where = f"{h['root']}/" if len(roots) > 1 else ""
        print(f"{where}{h['path']}:{h['line']}  [{h['kind']}] {h['heading'][:70]}  ({h['score']})")
        print("    " + (h["text"] if args.long else h["snippet"][:200]).replace("\n", "\n    "))
    return 0


def cmd_eval(args) -> int:
    rows = []
    for line in Path(args.file).expanduser().read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            p = line.split("\t")
            if len(p) >= 3:
                rows.append((p[0], p[1], p[2], p[4] if len(p) > 4 else "", p[3] if len(p) > 3 else ""))
    hit5 = hit10 = 0
    by = {}
    for q, root, expected, cross, kind in rows:
        r = check_root(root)
        hits = search_root(r, q, args.mode, [], [], 60)
        files = []
        for h in hits:
            if h["path"] not in files:
                files.append(h["path"])
        rank = files.index(expected) + 1 if expected in files else 0
        hit5 += 0 < rank <= 5
        hit10 += 0 < rank <= 10
        for key in (f"cross={cross}", kind):
            if key.endswith("=") or not key:
                continue
            b = by.setdefault(key, [0, 0, 0])
            b[0] += 1
            b[1] += 0 < rank <= 5
            b[2] += 0 < rank <= 10
        if args.verbose:
            print(f"{'ok ' if rank else 'MISS'} rank={rank or '-':>2}  {q[:70]}  -> {expected[-60:]}")
    n = len(rows)
    print(f"mode={args.mode} questions={n} recall@5={hit5}/{n}={hit5 / n:.2f} recall@10={hit10}/{n}={hit10 / n:.2f}")
    for key, (k, a, b) in sorted(by.items()):
        print(f"  {key}: n={k} recall@5={a / k:.2f} recall@10={b / k:.2f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("index", help="build or refresh the index of each root")
    pi.add_argument("roots", nargs="+")
    pq = sub.add_parser("query", help="search")
    pq.add_argument("text")
    pq.add_argument("--root", action="append", help="wiki root; repeat to search several (named explicitly)")
    pq.add_argument("--kind", action="append", choices=KINDS)
    pq.add_argument("--topic", action="append")
    pq.add_argument("-n", type=int, default=10)
    pq.add_argument("--json", action="store_true")
    pq.add_argument("--long", action="store_true", help="print the whole chunk")
    pq.add_argument("--mode", default=DEFAULT_MODE, choices=MODES, help=argparse.SUPPRESS)
    pe = sub.add_parser("eval", help="recall@5 and recall@10 on a TSV question set")
    pe.add_argument("file")
    pe.add_argument("--mode", default=DEFAULT_MODE, choices=MODES, help=argparse.SUPPRESS)
    pe.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    return {"index": cmd_index, "query": cmd_query, "eval": cmd_eval}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
