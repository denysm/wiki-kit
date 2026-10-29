"""Convert a draw.io PNG export (with embedded diagram XML) to a Markdown raw source, with no LLM.

Usage: uv run --no-project --with beautifulsoup4 python -I drawiopng2md.py <plan.json>
plan.json: [{"src": "/abs/x.drawio.png", "out": "/abs/raw/notes/....local.md", "title": "...",
             "source": "~/Library/.../x.drawio.png", "source_date": "YYYY-MM-DD|unknown",
             "tags": [...], "authors": [...]}]
A "File > Export > PNG > Include a copy of my diagram" PNG carries the whole diagram in a tEXt
chunk "mxfile". The text lists nodes (with their container) and edges (with labels), reusing
drawio_md from atlassian_export.py. Pictures without the chunk are reported and skipped.
"""
import base64
import importlib.util
import json
import re
import struct
import sys
import tempfile
import urllib.parse
import zlib
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
HOME = str(Path.home())


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def mxfile(png):
    d = Path(png).read_bytes()
    i = 8
    while i < len(d):
        n, t = struct.unpack(">I4s", d[i:i + 8])
        body = d[i + 8:i + 8 + n]
        if t == b"tEXt" and body.startswith(b"mxfile\0"):
            return urllib.parse.unquote(body.split(b"\0", 1)[1].decode("latin-1"))
        if t == b"iTXt" and body.startswith(b"mxfile\0"):
            return urllib.parse.unquote(body.split(b"\0", 5)[-1].decode("utf-8"))
        i += 12 + n
    return None


def load_drawio_md():
    spec = importlib.util.spec_from_file_location("atlassian_export", HERE / "atlassian_export.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.drawio_md


def convert(item, drawio_md):
    src, out = Path(item["src"]), Path(item["out"])
    if out.exists():
        print(f"skip (exists) {out.name}")
        return
    xml = mxfile(src)
    if not xml:
        print(f"no embedded diagram in {src.name}: describe it with describe_images.py instead")
        return
    with tempfile.NamedTemporaryFile("w", suffix=".drawio", delete=False, encoding="utf-8") as t:
        t.write(xml)
    body = drawio_md(t.name)
    Path(t.name).unlink()
    source = item.get("source") or src.as_posix().replace(HOME, "~")
    fm = ["---", f"title: {q(item['title'])}", f"source: {q(source)}", "type: notes", f"ingested: {TODAY}",
          f"tags: [{', '.join(item.get('tags', []))}, diagram]",
          f"authors: [{', '.join(item.get('authors', ['unknown']))}]",
          f"source_date: {item.get('source_date', 'unknown')}", "sensitivity: confidential", "---", "",
          f"# {item['title']}", "",
          f"> Nodes and edges extracted {TODAY} from the diagram embedded in `{src.name}`. "
          "Layout, colours and icons are not captured.", "", body, ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(fm), encoding="utf-8")
    print(f"{len(body)} chars  {out.name}")


if __name__ == "__main__":
    f = load_drawio_md()
    for i in json.load(open(sys.argv[1])):
        convert(i, f)
