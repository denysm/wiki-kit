"""Convert .eml files to verbatim-style Markdown raw sources (.local.md), with no LLM.

Usage: mail2md.py <plan.json>
plan.json: [{"src": "/abs/x.eml", "out": "/abs/raw/notes/YYYY-MM-DD-mail-slug.local.md",
             "source": "~/<cloud-drive>/Projects/<project>/mail/x.eml",
             "tags": ["project-a"]}]
Per message: headers (date, from, to, cc, subject), plain-text body (HTML is converted
when there is no plain part), attachment names (inline signature images are dropped).
Quoted reply history is kept: later replies are often the only copy of earlier mails.
Cleanup: "[cid:...]" markers, trailing whitespace, runs of blank lines.
Real credentials are replaced with [REDACTED:secret]; the count is printed.
Run: python3 -I mail2md.py plan.json   (HTML-only mail needs: uv run --no-project --with markdownify)
"""
import email
import json
import re
import sys
from datetime import date
from email import policy
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path

HOME = str(Path.home())
TODAY = date.today().isoformat()
SECRET = re.compile(
    r"(?i)\b(password|passcode|passwd|pwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?"
    r"(?!<|\$|\[REDACTED|\*{3}|xxx|your|example|placeholder|none|null|true|false|/|~)[^\s'\"<>]{6,}")
CONN = re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:(?![$<{]|\*{3}|\[REDACTED)[^\s@/]{3,}@")


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def names(header):
    out = []
    for name, addr in getaddresses([str(header or "")]):
        out.append(name.strip() or addr)
    return ", ".join(out)


def body_text(m):
    part = m.get_body(preferencelist=("plain",))
    if part is not None:
        return part.get_content()
    part = m.get_body(preferencelist=("html",))
    if part is None:
        return ""
    try:
        from markdownify import markdownify
        return markdownify(part.get_content(), heading_style="ATX")
    except ImportError:
        return re.sub(r"<[^>]+>", " ", part.get_content())


def clean(t):
    t = re.sub(r"\[cid:[^\]]*\]", "", t)
    t = "\n".join(line.rstrip() for line in t.replace("\r\n", "\n").split("\n"))
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def redact(t):
    n = 0

    def sub(mt):
        nonlocal n
        n += 1
        return mt.group(0).split(mt.group(1))[0] + mt.group(1) + ": [REDACTED:secret]"

    t = SECRET.sub(sub, t)

    def sub2(mt):
        nonlocal n
        n += 1
        return "[REDACTED:secret]@"

    return CONN.sub(sub2, t), n


def convert(item):
    src, out = Path(item["src"]), Path(item["out"])
    if out.exists():
        print(f"skip (exists) {out.name}")
        return 0
    m = email.message_from_binary_file(src.open("rb"), policy=policy.default)
    try:
        d = parsedate_to_datetime(m["date"]).date().isoformat()
    except Exception:
        d = "unknown"
    atts = [p.get_filename() for p in m.walk()
            if p.get_filename() and not re.match(r"(image\d+|Outlook-signature.*)\.(png|jpg|gif)$", p.get_filename())]
    subject = str(m["subject"] or src.stem)
    body, n = redact(clean(body_text(m)))
    source = item.get("source") or src.as_posix().replace(HOME, "~")
    fm = ["---", f"title: {q(subject)}", f"source: {q(source)}", "type: notes", f"ingested: {TODAY}",
          f"tags: [{', '.join(item.get('tags', []))}, mail]", f"authors: [{names(m['from'])}]",
          f"source_date: {d}", "sensitivity: confidential", "---", "",
          f"# {subject}", "",
          f"- Date: {m['date']}", f"- From: {names(m['from'])}", f"- To: {names(m['to'])}"]
    if m["cc"]:
        fm.append(f"- Cc: {names(m['cc'])}")
    if atts:
        fm.append("- Attachments: " + ", ".join(atts))
    fm += ["", body, ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(fm), encoding="utf-8")
    print(f"{len(body):>7} chars  {n} redacted  {out.name}")
    return n


if __name__ == "__main__":
    total = sum(convert(i) for i in json.load(open(sys.argv[1])))
    print(f"redacted secrets: {total}")
