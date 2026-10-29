"""Convert an .xlsx workbook to a Markdown raw source with one table per sheet, with no LLM.

Usage: uv run --no-project --with openpyxl python -I xlsx2md.py <plan.json>
plan.json: [{"src": "/abs/x.xlsx", "out": "/abs/raw/.../name.local.md", "title": "...",
             "source": "~/Library/.../x.xlsx", "source_date": "YYYY-MM-DD|unknown",
             "tags": [...], "authors": [...], "note": "free text for the header", "extra": {"k": "v"}}]
Cached cell values are used (what Excel last showed), not formulas; cells whose cached value is an
error (#REF!, #N/A) or empty while the formula exists are listed in a "Broken formulas" section.
Hidden sheets are marked. Comments are listed per sheet. Workbook properties (creator, last
modified by, dates) go to the header: they are the only version information an .xlsx keeps.
Cells are cut at 600 characters; long cells keep a "…" marker.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

import openpyxl

HOME = str(Path.home())
TODAY = date.today().isoformat()


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cell(v):
    if v is None:
        return ""
    s = str(v).replace("\r", "").replace("\n", "<br>").replace("|", "\\|")
    return s if len(s) <= 600 else s[:600] + "…"


def convert(item):
    src, out = Path(item["src"]), Path(item["out"])
    if out.exists():
        print(f"skip (exists) {out.name}")
        return
    vals = openpyxl.load_workbook(src, data_only=True)
    forms = openpyxl.load_workbook(src, data_only=False)
    p = vals.properties
    body = []
    for ws in vals:
        wf = forms[ws.title]
        rows = [r for r in ws.iter_rows(values_only=True)]
        while rows and not any(c is not None for c in rows[-1]):
            rows.pop()
        ncol = max((max((i for i, c in enumerate(r) if c is not None), default=-1) + 1 for r in rows), default=0)
        body += [f"## Sheet: {ws.title}" + (" (hidden)" if ws.sheet_state != "visible" else ""), "",
                 f"{len(rows)} rows × {ncol} columns, range {ws.dimensions}", ""]
        broken, comments = [], []
        for r in wf.iter_rows():
            for c in r:
                v = ws[c.coordinate].value
                if c.comment:
                    comments.append(f"- {c.coordinate}: {cell(c.comment.text)}")
                if isinstance(c.value, str) and c.value.startswith("=") and (v is None or str(v).startswith("#") or "#REF!" in c.value):
                    broken.append(f"- {c.coordinate}: `{c.value[:80]}` → {v if v is not None else 'empty'}")
        # leading title rows (single non-empty cell) stay as text; the first row with >=3 filled cells is the header
        i = 0
        while i < len(rows) and sum(c is not None for c in rows[i]) < 3:
            if any(c is not None for c in rows[i]):
                body.append(" ".join(cell(c) for c in rows[i] if c is not None))
            i += 1
        body.append("")
        if i < len(rows):
            hdr = [cell(c) or f"col{j + 1}" for j, c in enumerate(rows[i][:ncol])]
            body += ["| " + " | ".join(hdr) + " |", "|" + "---|" * ncol]
            for r in rows[i + 1:]:
                if any(c is not None for c in r):
                    body.append("| " + " | ".join(cell(c) for c in list(r[:ncol]) + [None] * (ncol - len(r[:ncol]))) + " |")
        body.append("")
        if broken:
            body += ["### Broken formulas", "", *broken[:40], ""]
            if len(broken) > 40:
                body += [f"… {len(broken) - 40} more", ""]
        if comments:
            body += ["### Comments", "", *comments, ""]
    source = item.get("source") or src.as_posix().replace(HOME, "~")
    fm = ["---", f"title: {q(item['title'])}", f"source: {q(source)}", "type: data", f"ingested: {TODAY}",
          f"tags: [{', '.join(item.get('tags', []))}]",
          f"authors: [{', '.join(item.get('authors', ['unknown']))}]",
          f"source_date: {item.get('source_date', 'unknown')}"]
    for k, v in (item.get("extra") or {}).items():
        fm.append(f"{k}: {v}")
    fm += ["---", "", f"# {item['title']}", "",
           f"> Extracted {TODAY} from `{src.name}`. Workbook properties: creator {p.creator}, last modified by "
           f"{p.lastModifiedBy}, created {p.created}, modified {p.modified}. Cached values, not formulas."
           + (f" {item['note']}" if item.get("note") else ""), ""] + body
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(fm), encoding="utf-8")
    print(f"{len(body)} lines  {out.name}")


if __name__ == "__main__":
    for i in json.load(open(sys.argv[1])):
        convert(i)
