"""Summarize standalone Plotly HTML charts as Markdown raw sources, with no LLM.

Usage: plotlyhtml2md.py <plan.json>
plan.json: [{"src": "/abs/x.html", "out": "/abs/raw/.../name.md", "title": "...",
             "source": "~/Library/.../x.html", "source_date": "YYYY-MM-DD|unknown",
             "tags": [...], "authors": [...]}]
A chart saved with fig.write_html() holds its data in a Plotly.newPlot("id", data, layout) call
(multi-MB, mostly numbers). The extract keeps what a reader needs: title, axis titles,
annotations, number of traces and points, per-trace name and size (largest first, at most
`top` traces, default 15), a sample of point labels, and the layout's text items. Coordinates
are not copied. The HTML itself stays in its original location.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

HOME = str(Path.home())
TODAY = date.today().isoformat()
DEC = json.JSONDecoder()


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def text_of(x):
    return x.get("text", "") if isinstance(x, dict) else (x or "")


def figures(h):
    for m in re.finditer(r'Plotly\.newPlot\(\s*"([^"]+)"\s*,\s*', h):
        s = h[m.end():]
        data, k = DEC.raw_decode(s)
        s = s[k:].lstrip(", \n")
        layout, _ = DEC.raw_decode(s)
        yield data, layout


def npoints(t):
    for key in ("text", "hovertext", "x", "y"):
        v = t.get(key)
        if isinstance(v, list):
            return len(v)
    return 0


def labels(t, n=6):
    for key in ("text", "hovertext"):
        v = t.get(key)
        if isinstance(v, list):
            return [str(i) for i in v[:n]]
    return []


def convert(item, top=15):
    src, out = Path(item["src"]), Path(item["out"])
    if out.exists():
        print(f"skip (exists) {out.name}")
        return
    h = src.read_text(encoding="utf-8", errors="replace")
    body = []
    for fi, (data, layout) in enumerate(figures(h), 1):
        sizes = sorted(((npoints(t), t) for t in data), key=lambda p: -p[0])
        total = sum(n for n, _ in sizes)
        body += [f"## Figure {fi}: {text_of(layout.get('title')) or '(no title)'}", "",
                 f"- Axes: x = {text_of((layout.get('xaxis') or {}).get('title'))}, "
                 f"y = {text_of((layout.get('yaxis') or {}).get('title'))}",
                 f"- {len(data)} traces, {total} points in total; trace types: "
                 + ", ".join(sorted({str(t.get('type')) for t in data}))]
        ann = [re.sub(r"<[^>]+>", " ", text_of(a)).strip() for a in layout.get("annotations", []) if text_of(a)]
        if ann:
            body.append("- Annotations: " + "; ".join(ann[:10]))
        body += ["", f"Traces by size (largest {min(top, len(sizes))} of {len(sizes)}):", ""]
        for n, t in sizes[:top]:
            lab = labels(t)
            body.append(f"- {t.get('name') or '(unnamed)'} — {t.get('type')}, {n} points"
                        + (f"; e.g. {', '.join(lab)}" if lab else ""))
        if len(sizes) > top:
            small = [n for n, _ in sizes[top:]]
            body.append(f"- … {len(small)} more traces of {min(small)}–{max(small)} points")
        body.append("")
    if not body:
        print(f"no Plotly figure found in {src.name}")
        return
    source = item.get("source") or src.as_posix().replace(HOME, "~")
    fm = ["---", f"title: {q(item['title'])}", f"source: {q(source)}", "type: notes", f"ingested: {TODAY}",
          f"tags: [{', '.join(item.get('tags', []))}, chart]",
          f"authors: [{', '.join(item.get('authors', ['unknown']))}]",
          f"source_date: {item.get('source_date', 'unknown')}", "---", "",
          f"# {item['title']}", "",
          f"> Summary of the Plotly chart in `{src.name}` ({src.stat().st_size // 1024} KB), extracted {TODAY}. "
          "Coordinates are not copied; open the original for the picture.", ""] + body
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(fm), encoding="utf-8")
    print(f"{len(body)} lines  {out.name}")


if __name__ == "__main__":
    for i in json.load(open(sys.argv[1])):
        convert(i)
