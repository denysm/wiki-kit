"""Convert a standalone HTML document to a verbatim Markdown raw source, with no LLM.

Usage:
  html2md.py <src.html> <out.md> [--source S] [--url U] [--authors "A, B"]
             [--source-date YYYY-MM-DD] [--tags t1,t2] [--title T] [--sensitivity S]
Run: uv run --no-project --with markdownify --with beautifulsoup4 python -I html2md.py ...

For SharePoint, Teams and other exports that arrive as one self-contained .html.
Drops <script>, <style>, <nav>, <footer> and the usual table-of-contents macros;
keeps headings, tables and lists. Images become links with their file name as alt
text; the files themselves are not downloaded (originals stay where they are archived).
Frontmatter follows the raw/ convention: unknown author or date is written
"unknown", never guessed. Run raw_check.py on the output.
"""
import argparse, datetime, re, sys
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

p = argparse.ArgumentParser()
p.add_argument("src")
p.add_argument("out")
p.add_argument("--source", default="")
p.add_argument("--url", default="")
p.add_argument("--authors", default="unknown")
p.add_argument("--source-date", default="unknown")
p.add_argument("--tags", default="")
p.add_argument("--title", default="")
p.add_argument("--sensitivity", default="")
a = p.parse_args()

soup = BeautifulSoup(Path(a.src).read_text(encoding="utf-8", errors="replace"), "html.parser")
for t in soup(["script", "style", "nav", "footer", "noscript"]):
    t.decompose()
for t in soup.select(".toc-macro, .toc, #toc"):
    t.decompose()
for img in soup.find_all("img"):
    if not (img.get("alt") or "").strip():
        src = img.get("data-image-src") or img.get("src") or ""
        img["alt"] = src.split("?")[0].rsplit("/", 1)[-1]

title = a.title or (soup.title.get_text(strip=True) if soup.title else Path(a.src).stem)
body = markdownify(str(soup.body or soup), heading_style="ATX", bullets="-").strip()
body = re.sub(r"\n{3,}", "\n\n", body)
if not body:
    sys.exit(f"{a.src}: no text after cleanup")

summary = next((l.strip() for l in body.splitlines()
                if l.strip() and not l.lstrip().startswith(("#", "|", "-", "!"))), title)


def yaml_str(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


fm = ["---",
      f"title: {yaml_str(title)}",
      f"source: {yaml_str(a.source or Path(a.src).name)}"]
if a.url:
    fm.append(f"url: {yaml_str(a.url)}")
fm += ["type: articles",
       f"ingested: {datetime.date.today().isoformat()}",
       f"tags: [{a.tags}]" if a.tags else "tags: []",
       f"summary: {yaml_str(summary[:300])}",
       f"authors: [{a.authors}]",
       f"source_date: {a.source_date}"]
if a.sensitivity:
    fm.append(f"sensitivity: {a.sensitivity}")
fm += ["---", "", f"# {title}", "",
       f"> Verbatim Markdown conversion of `{Path(a.src).name}`, converted "
       f"{datetime.date.today().isoformat()}. The original stays in its system; see `source`.", ""]

out = Path(a.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(fm + [body]) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(body.splitlines())} body lines)")
