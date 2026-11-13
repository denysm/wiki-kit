#!/usr/bin/env python3
"""Search over a wiki root: SQLite FTS5 (BM25, standard library only), optionally fused with
vectors from a local embedding server.

Usage:
  search.py index ROOT...                       # (re)build or refresh the index, incrementally
  search.py query "text" [--also "translation" ...] [--root ROOT ...] [--kind raw|wiki|output ...]
                         [--topic NAME ...] [--path TEXT] [-n 10] [--json] [--long] [--mode MODE]
  search.py recall "task" [--also ...] [--root ROOT] [--topic NAME ...] [-n 4]
                                                # past work orders, lessons, other material
  search.py langs [ROOT ...]                    # languages of the sources, by share of chunks
  search.py eval FILE [--variants FILE] [-n 10] [--mode MODE] [-v]
  search.py embed-setup [--preset NAME] [--url URL] [--off]  # write the vectors config, then test it
  search.py embed-check                         # test the embedding server named in the config

ROOT is a folder with wikis.json (a hub: topics live in topics/<name>/) or a folder
with _index.md and raw/ (a single wiki, for example a customer repository's .wiki/).
Only .md files in raw/, wiki/ and output/ are indexed, in chunks cut at headings (long
sections are cut further), each with its line range, heading, kind and topic.

`query` without --root uses the root found by walking up from the current folder.
It refreshes a stale index first (by file mtime and size). Several roots are searched
together only when you name each one with --root; roots of different customers must
not be mixed. Default output is one short block per hit: path:line, heading, score,
one snippet line. --long prints the whole chunk, --json prints records. --path keeps
hits whose path contains the text (for example `work-orders`).

Another language: words match words, so a question in one language finds sources in
another poorly. Pass --also with the question translated into each other language the
sources use (`search.py langs` lists them): every phrasing is searched and the rankings
are fused. On the owner's question set this was the largest single gain for questions
asked in another language than their source (docs/PROJECT-CONTEXT.md has the figures).

Vectors (optional): with an embedding server named in ~/.config/wiki-kit/search.json,
chunks also get vectors and the default mode "auto" fuses words and vectors; without the
file everything works on words alone. Any server with an OpenAI-style /v1/embeddings
endpoint works (Ollama, llama.cpp's llama-server, LM Studio). Chunk text, including
*.local.md files, is sent to it, so it must run on this machine: `url` has to point to
localhost unless the config also says "remote_ok": true for a host you control.
Quickest setup: install Ollama, `ollama pull embeddinggemma-2:270m-q8_0-text`, then
`search.py embed-setup` (writes the config below and tests it) and `search.py index ROOT`.

  {"embeddings": {"url": "http://127.0.0.1:11434/v1/embeddings",
                  "model": "embeddinggemma-2:270m-q8_0-text",
                  "query": "task: search result | query: {text}",
                  "document": "title: {title} | text: {text}",
                  "dims": 256}}

`query` and `document` are the model's prompts ({title} is the file title or "none").
`dims` keeps the first N numbers of each vector, only for models trained for it (such as
EmbeddingGemma); leave it out otherwise. Vectors are rebuilt when the model, prompts or
dims change, and when a probe sentence embeds differently (checked daily and on `index`:
the model file was replaced under the same name). `index` embeds everything; `query`
embeds at most 256 new chunks and otherwise uses the vectors it has (run `index` after a
large import). When the server is down, search falls back to words and says so.

The index is a cache, one database per root, in ~/.cache/wiki-kit/search/ (mode 600;
WIKI_KIT_SEARCH_CACHE overrides the folder, WIKI_KIT_SEARCH_CONFIG the config file). It
holds the text of *.local.md files and their vectors, so it never goes into a repository.
Delete it at any time; the next call rebuilds it.

Morphology: word search fuses two rankings (reciprocal rank fusion): exact words, and
stems (two letters cut off a word of 5+ letters, at least four kept) matched by prefix,
so Russian and French inflections (серверами / сервер) find each other without losing
exact hits. --mode plain|prefix|hybrid|vector|fused|auto is for comparison; auto is
fused (words and vectors) when vectors are configured, else hybrid (words only).

eval FILE: tab-separated lines `question<TAB>root<TAB>expected file relative to root`,
optionally `<TAB>kind<TAB>cross` (further columns and lines starting with # are ignored).
Several acceptable files are joined with `|`. A question counts as found at rank k when
an expected file is among the first k distinct files of the answer. --variants FILE adds
phrasings, as --also does: `question<TAB>variant[<TAB>variant...]`, the question exactly
as in FILE.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import operator
import os
import re
import sqlite3
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

VERSION = 4
CACHE = Path(os.environ.get("WIKI_KIT_SEARCH_CACHE") or Path.home() / ".cache" / "wiki-kit" / "search")
CONFIG = Path(os.environ.get("WIKI_KIT_SEARCH_CONFIG") or Path.home() / ".config" / "wiki-kit" / "search.json")
KINDS = ("raw", "wiki", "output")
MAX_CHUNK = 1800          # characters; longer sections are cut at blank lines
MAX_EMBED_CHARS = 8000    # characters of one chunk sent to the embedding server
QUERY_EMBED_LIMIT = 256   # a query embeds at most this many new chunks; `index` embeds all
MODES = ("plain", "prefix", "hybrid", "vector", "fused", "auto")
DEFAULT_MODE = "auto"
PROBE = "Probe sentence that checks the embedding model is unchanged. Проверка модели. Vérification."
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
LANG_WORDS = {  # frequent words that mark a language; enough to tell the language of a chunk
    "en": "the and is of to with that for are this was be have not it on".split(),
    "fr": "les des est une pour dans avec sont qui sur pas nous cette être le et du au par".split(),
    "de": "der die und ist nicht mit das den für auf ein eine sind wird zu von".split(),
    "es": "el los las que una para con por del está como más pero son y".split(),
    "it": "il che della per una sono con non gli del delle questo nel di".split(),
    "pt": "uma para com não dos das são pelo mais como mas está foi em".split(),
    "pl": "się nie jest że na do to jak przez dla oraz być są".split(),
    "ru": "и в не на что это как для по из который или если так он с".split(),
    "uk": "і та що це як для на не з до який або якщо також у".split(),
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
            got = c.execute("SELECT v FROM meta WHERE k = 'version'").fetchone()
            c.close()
        except sqlite3.Error:
            got = None
        if not got or got[0] != want:
            path.unlink()
    db = sqlite3.connect(path)
    os.chmod(path, 0o600)
    db.executescript(
        "CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);"
        "CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, mtime_ns INTEGER, size INTEGER);"
        "CREATE TABLE IF NOT EXISTS chunks(id INTEGER PRIMARY KEY, path TEXT, kind TEXT, topic TEXT, title TEXT,"
        " heading TEXT, line_a INTEGER, line_b INTEGER);"
        "CREATE INDEX IF NOT EXISTS chunks_path ON chunks(path);"
        "CREATE TABLE IF NOT EXISTS vec(id INTEGER PRIMARY KEY, v BLOB);"
    )
    if not db.execute("SELECT 1 FROM meta WHERE k = 'version'").fetchone():
        db.execute("INSERT INTO meta VALUES ('version', ?)", (want,))
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
        ids = [(r[0],) for r in db.execute("SELECT id FROM chunks WHERE path=?", (rel,))]
        db.executemany("DELETE FROM fts WHERE rowid=?", ids)
        db.executemany("DELETE FROM vec WHERE id=?", ids)
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


# ---------------------------------------------------------------- vectors (optional)

class EmbedError(Exception):
    pass


def embed_config() -> dict | None:
    """The `embeddings` section of the config file, or None when vectors are not set up."""
    try:
        cfg = json.loads(CONFIG.read_text(encoding="utf-8")).get("embeddings")
    except FileNotFoundError:
        return None
    except (OSError, ValueError, AttributeError) as e:
        sys.exit(f"bad config {CONFIG}: {e}")
    if not cfg:
        return None
    for k in ("url", "model"):
        if not cfg.get(k):
            sys.exit(f"{CONFIG}: embeddings.{k} is missing")
    host = urllib.parse.urlparse(cfg["url"]).hostname or ""
    if host not in ("localhost", "127.0.0.1", "::1") and not cfg.get("remote_ok"):
        sys.exit(f"{CONFIG}: embeddings.url points to {host}; chunk text would leave this machine. "
                 f'Use a local server, or add "remote_ok": true for a host you control.')
    cfg.setdefault("query", "{text}")
    cfg.setdefault("document", "{text}")
    return cfg


def signature(cfg: dict) -> str:
    return json.dumps({k: cfg.get(k) for k in ("model", "query", "document", "dims")}, sort_keys=True)


def unit(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def pack(v) -> bytes:
    return struct.pack(f"<{len(v)}e", *v)          # float16: half the size, enough for ranking


def unpack(b: bytes):
    return struct.unpack(f"<{len(b) // 2}e", b)


def embed(cfg: dict, texts: list[str], timeout: float = 300, batch: int = 16, workers: int = 4) -> list:
    """Unit vectors for already formatted texts, cut to `dims` when the config says so."""
    def post(part):
        body = json.dumps({"model": cfg["model"], "input": part}).encode()
        req = urllib.request.Request(cfg["url"], data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            raise EmbedError(f"HTTP {e.code}: {e.read().decode(errors='replace')[:160]}") from None
        except (urllib.error.URLError, OSError, ValueError) as e:
            raise EmbedError(str(getattr(e, "reason", e))) from None
        out = [None] * len(part)
        for item in d.get("data") or []:
            out[item["index"]] = item["embedding"]
        if any(v is None for v in out):
            raise EmbedError("the server returned fewer vectors than inputs")
        return out

    parts = [texts[i:i + batch] for i in range(0, len(texts), batch)]
    with ThreadPoolExecutor(max(1, min(workers, len(parts)))) as ex:
        vecs = [v for part in ex.map(post, parts) for v in part]
    dims = cfg.get("dims")
    return [unit(v[:dims] if dims else v) for v in vecs]


def doc_text(cfg: dict, title: str, text: str) -> str:
    return cfg["document"].replace("{title}", title or "none").replace("{text}", text[:MAX_EMBED_CHARS])


def query_text(cfg: dict, text: str) -> str:
    return cfg["query"].replace("{text}", text)


def refresh_vectors(root: Path, cfg: dict, limit: int | None = None, progress: bool = False,
                    timeout: float = 300) -> int:
    """Embed chunks that have no vector yet. Return how many are still missing (0 = all done)."""
    db = sqlite3.connect(db_path(root))
    try:
        meta = dict(db.execute("SELECT k, v FROM meta WHERE k LIKE 'emb_%'"))
        sig, now = signature(cfg), time.time()
        if meta.get("emb_sig") != sig:
            probe = embed(cfg, [PROBE], timeout)[0]
            db.execute("DELETE FROM vec")
            db.executemany("INSERT OR REPLACE INTO meta VALUES (?, ?)",
                           [("emb_sig", sig), ("emb_probe", pack(probe).hex()), ("emb_checked", str(now))])
            db.commit()
        elif progress or now - float(meta.get("emb_checked") or 0) > 86400:
            probe = embed(cfg, [PROBE], timeout)[0]
            old = unpack(bytes.fromhex(meta.get("emb_probe") or ""))
            if len(old) != len(probe) or sum(map(operator.mul, old, probe)) < 0.99:
                db.execute("DELETE FROM vec")
                db.execute("INSERT OR REPLACE INTO meta VALUES ('emb_probe', ?)", (pack(probe).hex(),))
                print("search: the embedding model answers differently now; rebuilding vectors", file=sys.stderr)
            db.execute("INSERT OR REPLACE INTO meta VALUES ('emb_checked', ?)", (str(now),))
            db.commit()
        todo = db.execute("SELECT c.id, c.title, f.text FROM chunks c JOIN fts f ON f.rowid = c.id "
                          "LEFT JOIN vec v ON v.id = c.id WHERE v.id IS NULL ORDER BY c.id").fetchall()
        if limit is not None and len(todo) > limit:
            return len(todo)
        step, t0 = 256, time.time()
        for i in range(0, len(todo), step):
            part = todo[i:i + step]
            vecs = embed(cfg, [doc_text(cfg, title, text) for _, title, text in part], timeout)
            db.executemany("INSERT OR REPLACE INTO vec VALUES (?, ?)",
                           [(cid, pack(v)) for (cid, _, _), v in zip(part, vecs)])
            db.commit()
            if progress:
                print(f"  vectors {i + len(part)}/{len(todo)}, {time.time() - t0:.0f}s", file=sys.stderr, flush=True)
        return 0
    finally:
        db.close()


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


def filters(kinds, topics, path) -> tuple[list[str], list]:
    where, args = [], []
    if kinds:
        where.append("c.kind IN (%s)" % ",".join("?" * len(kinds)))
        args += kinds
    if topics:
        where.append("c.topic IN (%s)" % ",".join("?" * len(topics)))
        args += topics
    if path:
        where.append("instr(c.path, ?) > 0")
        args.append(path)
    return where, args


def fuse(lists, limit: int, k: int = 60) -> list[dict]:
    """Reciprocal rank fusion of hit lists, keyed by chunk (root, path, first line)."""
    fused, by_key = {}, {}
    for hits in lists:
        for rank, h in enumerate(hits):
            key = (h["root"], h["path"], h["line"])
            by_key.setdefault(key, h)
            fused[key] = fused.get(key, 0) + 1.0 / (k + rank)
    top = sorted(fused, key=lambda x: -fused[x])[:limit]
    return [dict(by_key[x], score=round(fused[x] * 100, 2)) for x in top]


def search_root(root: Path, text: str, mode: str, kinds, topics, limit: int, path: str | None = None):
    """Word search (plain, prefix or hybrid) on an index that refresh() has brought up to date."""
    if mode == "hybrid":  # exact words and stem prefixes, fused
        return fuse([search_root(root, text, m, kinds, topics, limit * 3, path) for m in ("plain", "prefix")],
                    limit)
    expr = match_expr(text, mode)
    if not expr:
        return []
    where, args = filters(kinds, topics, path)
    db = sqlite3.connect(db_path(root))
    # bm25 column weights: heading 4, title 2, text 1
    sql = (f"SELECT c.path, c.kind, c.topic, c.heading, c.line_a, c.line_b, bm25(fts, 4.0, 2.0, 1.0) AS s, "
           f"snippet(fts, 2, '[', ']', ' … ', 24), fts.text "
           f"FROM fts JOIN chunks c ON c.id = fts.rowid WHERE {' AND '.join(['fts MATCH ?'] + where)} "
           f"ORDER BY s LIMIT ?")
    try:
        rows = db.execute(sql, [expr] + args + [limit]).fetchall()
    except sqlite3.OperationalError as e:
        sys.exit(f"search failed: {e}")
    finally:
        db.close()
    return [{"root": str(root), "path": r[0], "kind": r[1], "topic": r[2], "heading": r[3], "line": r[4],
             "line_end": r[5], "score": round(-r[6], 2), "snippet": " ".join(r[7].split()), "text": r[8]}
            for r in rows]


def vector_hits(root: Path, cfg: dict, text: str, kinds, topics, limit: int, path: str | None = None,
                timeout: float = 30):
    q = embed(cfg, [query_text(cfg, text)], timeout)[0]
    where, args = filters(kinds, topics, path)
    db = sqlite3.connect(db_path(root))
    try:
        rows = db.execute("SELECT c.id, v.v FROM vec v JOIN chunks c ON c.id = v.id"
                          + (" WHERE " + " AND ".join(where) if where else ""), args)
        mul = operator.mul
        top = heapq.nlargest(limit, ((sum(map(mul, q, unpack(b))), cid) for cid, b in rows))
        if not top:
            return []
        meta = {r[0]: r[1:] for r in db.execute(
            "SELECT c.id, c.path, c.kind, c.topic, c.heading, c.line_a, c.line_b, f.text FROM chunks c "
            "JOIN fts f ON f.rowid = c.id WHERE c.id IN (%s)" % ",".join("?" * len(top)), [c for _, c in top])}
    finally:
        db.close()
    out = []
    for s, cid in top:
        p, kind, topic, heading, a, b, body = meta[cid]
        lines = body.splitlines()
        rest = lines[1:] if lines and lines[0].lstrip().startswith("#") else lines
        out.append({"root": str(root), "path": p, "kind": kind, "topic": topic, "heading": heading, "line": a,
                    "line_end": b, "score": round(s, 4), "snippet": " ".join(" ".join(rest).split())[:240],
                    "text": body})
    return out


def note(msg: str, _seen=set()):
    if msg not in _seen:
        _seen.add(msg)
        print(f"search: {msg}", file=sys.stderr)


def search(root: Path, text: str, mode: str, kinds, topics, limit: int, also=(), path=None, cfg=None):
    """Words (every phrasing in text and `also`) and, when configured, vectors of `text`, fused."""
    if mode == "auto":
        mode = "fused" if cfg else "hybrid"
    if mode in ("vector", "fused") and not cfg:
        sys.exit(f"--mode {mode} needs an embeddings section in {CONFIG}")
    refresh(root)
    lists = []
    phrasings = [text] + [a for a in also if a.strip() and a != text]
    depth = limit * 3 if (len(phrasings) > 1 or mode != "hybrid") else limit  # deeper lists only for fusion
    if mode != "vector":
        word_mode = "hybrid" if mode == "fused" else mode
        found = [search_root(root, p, word_mode, kinds, topics, depth, path) for p in phrasings]
        lists.append(fuse(found, depth) if len(found) > 1 else found[0])
    if mode in ("vector", "fused"):
        try:
            pending = refresh_vectors(root, cfg, limit=QUERY_EMBED_LIMIT, timeout=60)
            if pending:
                note(f"{pending} chunks have no vectors yet; run: search.py index {root}")
            lists.append(vector_hits(root, cfg, text, kinds, topics, depth, path))
        except EmbedError as e:
            if mode == "vector":
                sys.exit(f"embedding server: {e}")
            note(f"embedding server unavailable ({e}); words only")
    if len(lists) == 1:
        return lists[0][:limit]
    return fuse(lists, limit)


# ---------------------------------------------------------------- languages

def chunk_lang(text: str) -> str | None:
    words = WORD.findall(text.lower())[:300]
    best, score = None, 0
    for lg, ws in LANG_SETS.items():
        s = sum(w in ws for w in words)
        if s > score:
            best, score = lg, s
    if best in ("ru", "uk"):
        low = text.lower()
        best = "uk" if len(re.findall("[іїєґ]", low)) > len(re.findall("[ыэъё]", low)) else "ru"
    return best if score >= 3 else None


LANG_SETS = {lg: set(ws) for lg, ws in LANG_WORDS.items()}


def root_langs(root: Path, share: float = 0.05) -> list[tuple[str, float]]:
    """Languages holding at least `share` of a root's chunks (rough, by frequent words)."""
    refresh(root)
    db = sqlite3.connect(db_path(root))
    counts, n = {}, 0
    for (t,) in db.execute("SELECT text FROM fts"):
        lg = chunk_lang(t)
        if lg:
            counts[lg] = counts.get(lg, 0) + 1
            n += 1
    db.close()
    return sorted(((lg, c / n) for lg, c in counts.items() if c / n >= share), key=lambda x: -x[1]) if n else []


# ---------------------------------------------------------------- commands

def cmd_index(args) -> int:
    cfg = embed_config()
    for r in args.roots:
        root = check_root(r)
        t = time.time()
        s = refresh(root)
        size = db_path(root).stat().st_size / 1e6
        print(f"{root}: {s['files']} files, +{s['files_new_or_changed']} new/changed, -{s['files_removed']} removed, "
              f"+{s['chunks_added']} chunks, {time.time() - t:.2f}s, index {size:.1f} MB ({db_path(root)})")
        if cfg:
            t = time.time()
            try:
                refresh_vectors(root, cfg, progress=True)
                print(f"  vectors up to date ({cfg['model']}), {time.time() - t:.1f}s, "
                      f"index {db_path(root).stat().st_size / 1e6:.1f} MB")
            except EmbedError as e:
                print(f"  vectors not refreshed: embedding server: {e}")
        print("  languages: " + ", ".join(f"{lg} {p:.0%}" for lg, p in root_langs(root)))
    return 0


def cmd_langs(args) -> int:
    roots = [check_root(r) for r in args.roots] or [find_root(Path.cwd()) or sys.exit("no wiki root here")]
    for root in roots:
        print(f"{root}: " + ", ".join(f"{lg} {p:.0%}" for lg, p in root_langs(root)))
    return 0


def cmd_query(args) -> int:
    roots = [check_root(r) for r in args.root] if args.root else []
    if not roots:
        found = find_root(Path.cwd())
        if not found:
            sys.exit("no wiki root here; give --root ROOT")
        roots = [found]
    cfg = None if args.mode in ("plain", "prefix", "hybrid") else embed_config()
    lists = [search(root, args.text, args.mode, args.kind, args.topic, args.n, args.also or (), args.path, cfg)
             for root in roots]
    hits = lists[0] if len(lists) == 1 else fuse(lists, args.n)
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


RECALL = (("Past work orders", "/work-orders/"), ("Lessons", "-ll-"), ("Other material", None))


def cmd_recall(args) -> int:
    """What a root already holds about a task: past work orders, lessons, other material."""
    root = check_root(args.root) if args.root else find_root(Path.cwd())
    if not root:
        sys.exit("no wiki root here; give --root ROOT")
    cfg = None if args.mode in ("plain", "prefix", "hybrid") else embed_config()
    shown = set()
    for title, part in RECALL:
        best = []
        for h in search(root, args.text, args.mode, [], args.topic, 40, args.also or (), part, cfg):
            name = Path(h["path"]).name
            if h["path"] in shown or (part is None and ("/work-orders/" in h["path"] or "-ll-" in name)):
                continue
            shown.add(h["path"])
            best.append(h)
            if len(best) == args.n:
                break
        print(f"{title}:" + ("" if best else " none"))
        for h in best:
            print(f"  {h['path']}:{h['line']}  {h['heading'][:70]}  ({h['score']})")
            print(f"      {h['snippet'][:160]}")
    return 0


def cmd_eval(args) -> int:
    rows = []
    for line in Path(args.file).expanduser().read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            p = line.split("\t")
            if len(p) >= 3:
                rows.append((p[0], p[1], p[2], p[4] if len(p) > 4 else "", p[3] if len(p) > 3 else ""))
    variants = {}
    if args.variants:
        for line in Path(args.variants).expanduser().read_text(encoding="utf-8").splitlines():
            p = line.split("\t")
            if len(p) > 1 and not line.startswith("#"):
                variants[p[0]] = [x for x in p[1:] if x.strip()]
    cfg = None if args.mode in ("plain", "prefix", "hybrid") else embed_config()
    hit5 = hit10 = 0
    by = {}
    for q, root, expected, cross, kind in rows:
        r = check_root(root)
        hits = search(r, q, args.mode, [], [], 60, variants.get(q, ()), None, cfg)
        files = []
        for h in hits:
            if h["path"] not in files:
                files.append(h["path"])
        ranks = [files.index(e) + 1 for e in expected.split("|") if e in files]
        rank = min(ranks) if ranks else 0
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
    mode = args.mode if args.mode != "auto" else ("fused" if cfg else "hybrid")
    print(f"mode={mode}{' +variants' if variants else ''} questions={n} "
          f"recall@5={hit5}/{n}={hit5 / n:.2f} recall@10={hit10}/{n}={hit10 / n:.2f}")
    for key, (k, a, b) in sorted(by.items()):
        print(f"  {key}: n={k} recall@5={a / k:.2f} recall@10={b / k:.2f}")
    return 0


OLLAMA_URL = "http://127.0.0.1:11434/v1/embeddings"
PRESETS = {  # measured on the owner's question set (docs/PROJECT-CONTEXT.md); model names as in Ollama
    "embeddinggemma-2": {"model": "embeddinggemma-2:270m-q8_0-text",
                         "query": "task: search result | query: {text}",
                         "document": "title: {title} | text: {text}", "dims": 256},
    "bge-m3": {"model": "bge-m3:567m", "query": "{text}", "document": "{text}"},
}


def cmd_embed_setup(args) -> int:
    """Write (or remove) the embeddings section of the config, then test the server."""
    data = {}
    if CONFIG.exists():
        try:
            data = json.loads(CONFIG.read_text(encoding="utf-8"))
        except ValueError:
            sys.exit(f"{CONFIG} is not valid JSON; fix or delete it first")
    if args.off:
        data.pop("embeddings", None)
    else:
        cfg = dict(PRESETS[args.preset], url=args.url or OLLAMA_URL)
        if args.model:
            cfg["model"] = args.model
        data["embeddings"] = cfg
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.off:
        print(f"{CONFIG}: embeddings removed; search uses words only")
        return 0
    print(f"wrote {CONFIG} ({args.preset})")
    return cmd_embed_check(args)


def cmd_embed_check(args) -> int:
    cfg = embed_config()
    if not cfg:
        print(f"no embeddings section in {CONFIG}: search uses words only")
        return 1
    try:
        t = time.time()
        v = embed(cfg, [query_text(cfg, "hello"), doc_text(cfg, "", "Bonjour. Привет.")], timeout=120)
    except EmbedError as e:
        print(f"{cfg['url']} ({cfg['model']}): {e}")
        return 1
    sim = sum(map(operator.mul, v[0], v[1]))
    print(f"{cfg['url']} ({cfg['model']}): ok, {len(v[0])} dims, {(time.time() - t) * 1000:.0f} ms for 2 texts, "
          f"similarity of the test pair {sim:.2f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("index", help="build or refresh the index (and vectors, when configured) of each root")
    pi.add_argument("roots", nargs="+")
    pq = sub.add_parser("query", help="search")
    pq.add_argument("text")
    pq.add_argument("--also", action="append", help="another phrasing, e.g. a translation; repeat for several")
    pq.add_argument("--root", action="append", help="wiki root; repeat to search several (named explicitly)")
    pq.add_argument("--kind", action="append", choices=KINDS)
    pq.add_argument("--topic", action="append")
    pq.add_argument("--path", help="keep hits whose path contains this text")
    pq.add_argument("-n", type=int, default=10)
    pq.add_argument("--json", action="store_true")
    pq.add_argument("--long", action="store_true", help="print the whole chunk")
    pq.add_argument("--mode", default=DEFAULT_MODE, choices=MODES)
    pr = sub.add_parser("recall", help="past work orders, lessons and other material about a task")
    pr.add_argument("text")
    pr.add_argument("--also", action="append", help="another phrasing, e.g. a translation; repeat for several")
    pr.add_argument("--root", help="wiki root (default: found from the current folder)")
    pr.add_argument("--topic", action="append")
    pr.add_argument("-n", type=int, default=4, help="files per section (default 4)")
    pr.add_argument("--mode", default=DEFAULT_MODE, choices=MODES)
    pl = sub.add_parser("langs", help="languages of the sources, by share of chunks")
    pl.add_argument("roots", nargs="*")
    pe = sub.add_parser("eval", help="recall@5 and recall@10 on a TSV question set")
    pe.add_argument("file")
    pe.add_argument("--variants", help="TSV: question, then other phrasings of it")
    pe.add_argument("--mode", default=DEFAULT_MODE, choices=MODES)
    pe.add_argument("-v", "--verbose", action="store_true")
    sub.add_parser("embed-check", help="test the embedding server named in the config")
    ps = sub.add_parser("embed-setup", help="write the embeddings section of the config for a measured model")
    ps.add_argument("--preset", default="embeddinggemma-2", choices=PRESETS)
    ps.add_argument("--url", help=f"OpenAI-style embeddings endpoint (default: Ollama, {OLLAMA_URL})")
    ps.add_argument("--model", help="model name on that server, if it differs from the preset")
    ps.add_argument("--off", action="store_true", help="remove the section: words only")
    args = ap.parse_args()
    return {"index": cmd_index, "query": cmd_query, "recall": cmd_recall, "langs": cmd_langs, "eval": cmd_eval,
            "embed-check": cmd_embed_check, "embed-setup": cmd_embed_setup}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
