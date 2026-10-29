#!/usr/bin/env python3
"""Inventory candidate sources before anything is ingested.

Usage:
  inventory.py SRC_ROOT -o inventory.tsv [--exclude DIR]... [--patterns FILE]

One row per candidate: plain files, plus one row per conversation inside a
Claude or ChatGPT export (path is `export.json#<conversation id>`, which
chat2md.py --inventory understands). Images and audio are folded into one row
per folder. `personal-docs/` is excluded by default and never opened.

Columns: n, path, kind, date, size, msgs, topic, duplicate_of, decision, reason,
secrets, title. topic and decision are guesses for the operator to edit:
decision is ingest | split | skip | review. duplicate_of is an exact copy
(same bytes, or same conversation id); `~path` marks a near variant (same
name stem). secrets is the raw_check hit count; values are never written.

The aligned table is also printed to stdout (titles shortened).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chat2md  # noqa: E402
import raw_check  # noqa: E402

EXCLUDE = {"personal-docs"}
IGNORE_NAMES = {".DS_Store"}
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".wav", ".mp3", ".m4a", ".ogg", ".webm", ".mp4"}
META_JSON = {"export_manifest.json", "message_feedback.json", "shared_conversations.json", "user.json",
             "user_settings.json", "users.json", "login_history.json"}
COLUMNS = ["n", "path", "kind", "date", "size", "msgs", "topic", "duplicate_of", "decision", "reason", "secrets", "title"]

# First match wins. Keys are regexes over "title + file name", lowercased.
# Generic defaults; your own rules (names, places, employer) go in RULES_FILE, outside the repository.
RULES_FILE = Path("~/.config/wiki-kit/inventory.json").expanduser()
CAREER = r"resume|\bcv\b|linkedin|career|\bjob|recruit|interview|hiring|vacanc|salary|cover.?letter|" \
         r"резюме|ваканс|карьер|собесед|работодат|зарплат|рекрут|найм"
PERSONAL_BUCKETS = [
    # Employer and client work stays out of a personal wiki, so it is matched before anything personal.
    ("work", "skip", r"sprint \d|effort estimation|\bpitch|\bpoc\b|engagement|client|клиент"),
    ("health", "review", r"health|symptom|doctor|medic|patient|здоров|симптом|лекарств|врач|болезн|лечени"),
    ("family-school", "ingest", r"school|teacher|child|kids|школ|учител|ребен|ребён|детей|родител"),
    ("housing-money", "ingest", r"mortgage|rent|tax|invest|недвижим|квартир|ипотек|кредит|налог|инвест"),
    ("relocation-admin", "ingest", r"visa|passport|residence|consulat|паспорт|консульск|\bвиз[аы]\b|внж|гражданств"),
    ("shopping", "review", r"\bbuy\b|which .{0,20} to choose|купить|покупк|выбор"),
    ("travel-outdoor", "review", r"trip|travel|hotel|hike|поездк|поход|отел"),
    ("tech", "review", r"claude|chatgpt|\bllm|android|\bssh\b|\bmac\b|python"),
]
PREPARED = {}  # folder prefix -> topic for notes already written for one topic (ingest, check)
if RULES_FILE.exists():
    _rules = json.loads(RULES_FILE.read_text(encoding="utf-8"))
    CAREER = _rules.get("career", CAREER)
    PERSONAL_BUCKETS = [tuple(b) for b in _rules.get("buckets", PERSONAL_BUCKETS)]
    PREPARED = _rules.get("prepared", PREPARED)


def guess_topic(text: str) -> tuple[str, str, str]:
    """Return (topic, decision, bucket)."""
    t = text.lower()
    if re.search(CAREER, t):
        return "career", "ingest", "career"
    for bucket, decision, rx in PERSONAL_BUCKETS:
        if re.search(rx, t):
            return ("-" if bucket == "work" else "personal"), decision, bucket
    return "personal", "review", "unsorted"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    out = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
    except (zipfile.BadZipFile, KeyError):
        return ""
    return re.sub(r"<[^>]+>", " ", xml)


def stem_key(name: str) -> str:
    s = Path(name).stem.lower()
    s = re.sub(r"^\(\d+\)\s*", "", s)
    s = re.sub(r"([-_ ]v?\d)$", "", s)
    return re.sub(r"[^a-z0-9а-я]+", "", s)


def fdate(path: Path, fm: dict | None = None) -> str:
    if fm and fm.get("source_date"):
        return fm["source_date"]
    m = re.match(r"(\d{4}-\d{2}-\d{2})", path.name)
    if m:
        return m.group(1)
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return mtime.date().isoformat() if mtime.year >= 2000 else ""  # zip extracts carry 1980-01-01


def human(n: int) -> str:
    for unit in ("B", "K", "M", "G"):
        if n < 1024 or unit == "G":
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024
    return str(n)


class Inventory:
    def __init__(self, root: Path, exclude: set[str], extra):
        self.root, self.exclude, self.extra = root, exclude, extra
        self.rows: list[dict] = []
        self.by_hash: dict[str, str] = {}
        self.md_by_uuid: dict[str, str] = {}

    def rel(self, p: Path) -> str:
        return str(p.relative_to(self.root))

    def add(self, **kw) -> dict:
        row = {c: "" for c in COLUMNS} | kw
        self.rows.append(row)
        return row

    def secrets(self, text: str) -> int:
        return sum(raw_check.redact(text, self.extra)[1].values()) if text else 0

    def files(self):
        for p in sorted(self.root.rglob("*")):
            parts = p.relative_to(self.root).parts
            if p.is_file() and parts[0] not in self.exclude and p.name not in IGNORE_NAMES:
                yield p

    def run(self):
        media = defaultdict(lambda: [0, 0])
        exports = []
        for p in self.files():
            ext = p.suffix.lower()
            if ext in MEDIA_EXT:
                key = self.rel(p.parent)
                key = re.sub(r"/[0-9a-f-]{20,}/audio$", "/*/audio", key)
                media[(key, "audio" if ext in {".wav", ".mp3", ".m4a", ".ogg", ".webm"} else "image")][0] += 1
                media[(key, "audio" if ext in {".wav", ".mp3", ".m4a", ".ogg", ".webm"} else "image")][1] += p.stat().st_size
                continue
            self.file_row(p, exports)
        for (folder, kind), (count, size) in sorted(media.items()):
            self.add(path=folder + "/", kind=f"{kind} x{count}", size=size, decision="skip", topic="-",
                     reason="media; chats keep [image] markers" if kind == "image" else "voice audio; chats keep the transcripts")
        for p in exports:
            self.conversation_rows(p)
        self.mark_duplicates()

    def file_row(self, p: Path, exports: list):
        rel, ext, size = self.rel(p), p.suffix.lower(), p.stat().st_size
        h = sha256(p)
        dup = self.by_hash.get(h, "")
        self.by_hash.setdefault(h, rel)
        top = rel.split("/")[0]
        row = self.add(path=rel, size=size, date=fdate(p), duplicate_of=dup, title=p.stem)

        if dup:
            row.update(kind=ext.lstrip("."), decision="skip", reason="exact copy", topic="-")
            return
        if p.name in META_JSON or p.name == "_index.tsv" or p.name.startswith("manifest-"):
            row.update(kind="meta", decision="skip", reason="export metadata", topic="-")
        elif ext == ".zip":
            try:
                n = len(zipfile.ZipFile(p).namelist())
            except zipfile.BadZipFile:
                n = "?"
            small = size < 100_000 and "linkedin" in p.name.lower()
            row.update(kind="zip", topic="career" if small else "-", decision="review" if small else "skip",
                       reason=f"{n} member(s); " + ("small LinkedIn export, check what it holds" if small
                                                    else "archive of an extracted copy"))
        elif re.match(r"conversations(-\d+)?\.json$", p.name):
            exports.append(p)
            row.update(kind="export", topic="-", decision="split", reason="one row per conversation below (chat2md)")
        elif p.name == "chat.html":
            row.update(kind="html", topic="-", decision="skip", reason="HTML view of the ChatGPT conversations JSON")
        elif top in ("README.md",) or p.name == "llm-wiki-portable-playbook.md":
            row.update(kind="md", topic="-", decision="skip", reason="method/handoff note, not a source")
        elif ext == ".md":
            self.md_row(p, row)
        elif ext == ".json" and "/memories/" in f"/{rel}":
            text = p.read_text(encoding="utf-8")
            row.update(kind="memory", topic="personal", decision="review", secrets=self.secrets(text),
                       reason="Claude memory snapshot; may hold work context", title="Claude memories")
        elif ext == ".json" and "/projects/" in f"/{rel}":
            self.project_row(p, row)
        elif ext == ".json" and p.name == "artifact.json":
            meta = json.loads(p.read_text(encoding="utf-8"))
            row.update(kind="meta", topic="-", decision="skip", reason="artifact metadata",
                       title=meta.get("title") or meta.get("name") or "")
        elif ext in (".html", ".htm"):
            meta_file = p.parent.parent / "artifact.json"
            title = ""
            if meta_file.exists():
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                title = meta.get("title") or meta.get("name") or ""
            topic, decision, bucket = guess_topic(f"{title} {p.name}")
            row.update(kind="artifact", topic=topic, decision="review", title=title or p.stem,
                       reason=f"Claude artifact (HTML); bucket {bucket}",
                       secrets=self.secrets(p.read_text(encoding="utf-8", errors="replace")))
        elif ext == ".webarchive":
            row.update(kind="webarchive", topic="career", decision="review",
                       reason="binary Safari archive of the LinkedIn page; PDF profile may cover it")
        elif ext in (".docx", ".pdf", ".txt", ".yaml", ".yml"):
            text = docx_text(p) if ext == ".docx" else ("" if ext == ".pdf" else p.read_text(encoding="utf-8", errors="replace"))
            topic, decision, bucket = guess_topic(f"{p.name} {rel}")
            if top == "career":
                topic, decision = "career", "ingest"
            row.update(kind=ext.lstrip("."), topic=topic, decision=decision,
                       reason=("as Markdown extract" if ext in (".docx", ".pdf") else "") + ("" if top == "career" else f"; bucket {bucket}"),
                       secrets="n/a" if ext == ".pdf" else self.secrets(text))
        else:
            row.update(kind=ext.lstrip(".") or "file", topic="-", decision="review", reason="unknown type")

    def md_row(self, p: Path, row: dict):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        title = fm.get("title") or p.stem
        msgs = len(re.findall(r"^### (?:User|Claude|ChatGPT)\b", text, re.M))
        m = re.search(r"claude\.ai/chat/([0-9a-f-]{36})", fm.get("source", ""))
        if m:
            other = self.md_by_uuid.setdefault(m.group(1), self.rel(p))
            if other != self.rel(p):
                row["duplicate_of"] = other
        rel = self.rel(p)
        topic, decision, bucket = guess_topic(title)
        reason = f"bucket {bucket}"
        prefix = next((k for k in PREPARED if rel.startswith(k)), None)
        if prefix:
            topic, decision, reason = PREPARED[prefix], "ingest", f"prepared {PREPARED[prefix]} note (check)"
            if "poisk-idey" in p.name or "ideas" in title.lower():
                decision, reason = "review", "idea search: career or personal?"
        if msgs and msgs <= 2 and len(text) < 2500:
            decision, reason = "skip", f"trivial ({msgs} msgs)"
        if row["duplicate_of"]:
            decision, reason = "skip", "same conversation"
        row.update(kind="chat-md" if msgs else "md", date=fdate(p, fm), msgs=msgs or "", topic=topic,
                   decision=decision, reason=reason, title=title, secrets=self.secrets(text))

    def project_row(self, p: Path, row: dict):
        data = json.loads(p.read_text(encoding="utf-8"))
        name = data.get("name") or p.stem
        prompt = data.get("prompt_template") or ""
        docs = data.get("docs") or []
        topic, decision, bucket = guess_topic(name)
        empty = not prompt.strip() and not docs
        row.update(kind="project", title=name, topic=topic if not empty else "-",
                   decision="skip" if empty else "review",
                   reason="empty project stub" if empty else f"Claude project: prompt {len(prompt)} chars, {len(docs)} doc(s)",
                   secrets=self.secrets(json.dumps(data, ensure_ascii=False)))

    def conversation_rows(self, export: Path):
        rel = self.rel(export)
        exported = chat2md.export_date(export)
        for c in chat2md.load_export(export):
            text = chat2md.render(c, exported)
            dup = self.md_by_uuid.get(c["id"], "") if c["app"] == "claude" else ""
            topic, decision, bucket = guess_topic(c["title"])
            reason = f"bucket {bucket}"
            user_turns = sum(1 for who, _, _ in c["turns"] if who == "User")
            if not c["turns"]:
                decision, reason = "skip", "empty"
            elif user_turns <= 1 and len(text) < 2500:
                decision, reason = "skip", f"trivial ({len(c['turns'])} msgs)"
            if dup:
                decision, reason = "skip", "already converted"
            self.add(path=f"{rel}#{c['id']}", kind=f"{c['app']}-chat",
                     date=c["created"].date().isoformat() if c["created"] else "",
                     size=len(text.encode()), msgs=len(c["turns"]), topic=topic if not dup else "-",
                     duplicate_of=dup, decision=decision, reason=reason, title=c["title"],
                     secrets=self.secrets(text))

    def mark_duplicates(self):
        groups = defaultdict(list)
        for r in self.rows:
            if r["decision"] != "skip" and "#" not in r["path"] and not r["path"].endswith("/"):
                groups[stem_key(Path(r["path"]).name)].append(r)
        for rows in groups.values():
            if len(rows) < 2:
                continue
            rows.sort(key=lambda r: (r["date"], int(r["size"] or 0)), reverse=True)
            keep = rows[0]
            for r in rows[1:]:
                r["duplicate_of"] = "~" + keep["path"]
                r["decision"] = "review"
                r["reason"] = (r["reason"] + "; " if r["reason"] else "") + "older/smaller variant"


def print_table(rows: list[dict]):
    cols = ["n", "decision", "topic", "date", "size", "msgs", "secrets", "kind", "title", "reason"]
    view = []
    for r in rows:
        v = dict(r)
        v["size"] = human(int(r["size"])) if str(r["size"]).isdigit() else r["size"]
        v["title"] = (r["title"] or r["path"])[:48]
        v["reason"] = (r["reason"] + (f" [dup {r['duplicate_of']}]" if r["duplicate_of"] else ""))[:70]
        view.append(v)
    width = {c: max(len(c), *(len(str(v[c])) for v in view)) for c in cols}
    print("  ".join(c.ljust(width[c]) for c in cols))
    for v in view:
        print("  ".join(str(v[c]).ljust(width[c]) for c in cols))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True, help="TSV to write")
    ap.add_argument("--exclude", action="append", default=[], help="top-level folder to skip (personal-docs always)")
    ap.add_argument("--patterns", type=Path, help="extra internal patterns for raw_check")
    ap.add_argument("--no-table", action="store_true", help="do not print the table")
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    inv = Inventory(root, EXCLUDE | set(args.exclude), raw_check.load_patterns(args.patterns))
    inv.run()
    for i, r in enumerate(inv.rows, 1):
        r["n"] = i
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(inv.rows)
    if not args.no_table:
        print_table(inv.rows)
    counts = defaultdict(int)
    for r in inv.rows:
        counts[r["decision"]] += 1
    print(f"\n{len(inv.rows)} rows -> {args.out}  " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
