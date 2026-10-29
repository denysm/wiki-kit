"""Convert a WebVTT meeting transcript to a Markdown raw source (.local.md), with no LLM.

Usage: vtt2md.py <plan.json>
plan.json: [{"src": "/abs/x.vtt", "out": "/abs/raw/notes/YYYY-MM-DD-meeting-slug.local.md",
             "title": "...", "source": "~/Library/.../x.vtt", "source_date": "YYYY-MM-DD|unknown",
             "tags": ["project-a"], "authors": ["unknown"], "gap": 6.0, "chunk": 60}]
Cue fragments are merged into paragraphs: a new paragraph starts after a pause longer than
`gap` seconds (default 6) or, at a sentence end, once it is `chunk` seconds long (default 45); every paragraph carries the start time [mm:ss]. Speaker tags
(<v Name>) are kept as "Name:" when the file has them. Duplicated consecutive cues are dropped.
Real credentials are replaced with [REDACTED:secret] (same patterns as mail2md.py).
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

HOME = str(Path.home())
TODAY = date.today().isoformat()
SECRET = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?"
    r"(?!<|\$|\[REDACTED|\*{3}|xxx|your|example|placeholder|none|null|true|false|/|~)[^\s'\"<>]{6,}")
TS = re.compile(r"(\d+):(\d\d):(\d\d)\.(\d+) --> (\d+):(\d\d):(\d\d)\.(\d+)")


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def cues(text):
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        lines = [l for l in block.split("\n") if l.strip()]
        for i, l in enumerate(lines):
            mt = TS.search(l)
            if mt:
                g = mt.groups()
                body = " ".join(lines[i + 1:])
                spk = re.match(r"<v ([^>]+)>", body)
                body = re.sub(r"</?[^>]+>", "", body).strip()
                if body:
                    yield secs(*g[:4]), secs(*g[4:]), (spk.group(1) if spk else None), body
                break


def convert(item):
    src, out = Path(item["src"]), Path(item["out"])
    if out.exists():
        print(f"skip (exists) {out.name}")
        return
    gap = float(item.get("gap", 6))
    chunk = float(item.get("chunk", 45))
    paras, cur, last_end, last_spk, last_text = [], None, -99, None, None
    for start, end, spk, body in cues(src.read_text(encoding="utf-8", errors="replace")):
        if body == last_text:
            continue
        last_text = body
        long_run = cur is not None and (start - cur[0] > chunk and cur[2][-1].rstrip().endswith((".", "?", "!")) or start - cur[0] > 2 * chunk)
        if cur is None or start - last_end > gap or spk != last_spk or long_run:
            cur = [start, spk, [body]]
            paras.append(cur)
        else:
            cur[2].append(body)
        last_end, last_spk = end, spk
    n = 0
    lines = []
    for start, spk, parts in paras:
        txt = " ".join(parts)
        txt, k = SECRET.subn(lambda m: m.group(0).split(m.group(1))[0] + m.group(1) + ": [REDACTED:secret]", txt)
        n += k
        mm, ss = divmod(int(start), 60)
        lines.append(f"[{mm:02d}:{ss:02d}] " + (f"{spk}: " if spk else "") + txt)
    source = item.get("source") or src.as_posix().replace(HOME, "~")
    dur = int(last_end)
    fm = ["---", f"title: {q(item['title'])}", f"source: {q(source)}", "type: notes", f"ingested: {TODAY}",
          f"tags: [{', '.join(item.get('tags', []))}, meeting-transcript]",
          f"authors: [{', '.join(item.get('authors', ['unknown']))}]",
          f"source_date: {item.get('source_date', 'unknown')}", "sensitivity: confidential", "---", "",
          f"# {item['title']}", "",
          f"> Auto-generated transcript, {dur // 60} min, {len(paras)} paragraphs. No speaker names in the file "
          "unless shown; recognition errors are likely (names, technical terms).", "", "\n\n".join(lines), ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(fm), encoding="utf-8")
    print(f"{len(paras)} paragraphs, {n} redacted  {out.name}")


if __name__ == "__main__":
    for i in json.load(open(sys.argv[1])):
        convert(i)
