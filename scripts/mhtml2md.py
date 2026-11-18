"""Convert Confluence Cloud pages saved by a browser as .mhtml to verbatim Markdown raw sources, no LLM.

Usage:
  mhtml2md.py <out_dir> <src.mhtml|src.md> [...] --instance <name> [--space-name S] [--tags t1,t2]
              [--tag-rule keyword=tag ...]
              [--ingested YYYY-MM-DD] [--sensitivity confidential] [--dry-run]
Run: uv run --no-project --with markdownify --with beautifulsoup4 python -I mhtml2md.py ...

For each .mhtml: parses the MIME container, takes the real page URL from the
`Snapshot-Content-Location` header (the ajs-page-id / ajs-page-title meta tags go stale after
SPA navigation and are ignored), strips the Confluence chrome (side navigation, menus, byline
buttons) and converts the page body: headings, lists, tables, code, panels, status lozenges
(as [TEXT]), Jira issue links, mentions, comments. Folder pages become their child listing;
Confluence database pages (content lives in an iframe part) become a table. Images become
`![alt](file name)`; nothing is embedded. Output name: YYYY-MM-DD-confluence-<slug>.local.md.
Real credentials are replaced with [REDACTED:secret]; the count is printed. Frontmatter follows
the raw/ convention; unknown author or date is written "unknown". A page whose body is not in
the snapshot gets "[content not captured in the browser snapshot]". Run raw_check.py afterwards.
A plain .md file (Confluence markdown export) is copied with the same frontmatter.
"""
import argparse, datetime, email, re, sys
from email import policy
from pathlib import Path
from urllib.parse import urlparse, unquote

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify

NOT_CAPTURED = "[content not captured in the browser snapshot]"

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), None),
    (re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"), None),
    (re.compile(r"\b(?:glpat|ghp|gho|ghs|xox[bpas]|sk-ant|sk)-[A-Za-z0-9_\-]{20,}"), None),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{10,}"), None),
    (re.compile(r"(://[^\s:/@]+:)([^\s@/<>{}$]{3,})(@)"), 2),
    (re.compile(r"(?i)\b(password|passwd|pwd|secret[_ ]?key|aws_secret_access_key|api[_-]?key|token)\b"
                r"(\s*[:=]\s*[\"']?)([^\s\"'<>{}$,;|]{8,})"), 3),
]
PLACEHOLDER = re.compile(r"^(<.*>|\$\{?.*|\{\{.*|x{3,}|\*{3,}|\.{3}|your[_-].*|changeme|redacted.*|\[REDACTED.*|var\..*|[A-Z][A-Z0-9_]{3,})$", re.I)


def redact(text):
    n = 0

    def sub_group(pat, grp):
        def f(m):
            nonlocal n
            val = m.group(grp)
            if PLACEHOLDER.match(val) or val.lower().startswith(("http", "var.", "local.", "data.")):
                return m.group(0)
            n += 1
            return m.group(0).replace(val, "[REDACTED:secret]", 1) if grp != 0 else "[REDACTED:secret]"
        return f
    for pat, grp in SECRET_PATTERNS:
        text = pat.sub(sub_group(pat, grp or 0), text)
    return text, n


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def slugify(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:60].strip("-") or "page"


def load_mhtml(path):
    msg = email.message_from_binary_file(open(path, "rb"), policy=policy.default)
    parts = []
    for p in msg.walk():
        if p.get_content_type() == "text/html":
            raw = p.get_payload(decode=True) or b""
            parts.append(raw.decode(p.get_content_charset() or "utf-8", errors="replace"))
    loc = msg.get("Snapshot-Content-Location") or ""
    return loc, msg.get("Date") or "", parts


def clean_text(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def img_name(img):
    alt0 = (img.get("alt") or "").strip()
    if alt0 and not alt0.startswith(("http", "data:")):
        return alt0
    mq = re.search(r"[?&#]name=([^&]+)", img.get("src") or "")
    if mq:
        return unquote(mq.group(1))
    for k in ("data-image-src", "data-media-id", "src"):
        v = img.get(k) or ""
        if v and not v.startswith("data:"):
            return unquote(v.split("?")[0].rsplit("/", 1)[-1])
    return img.get("alt") or "image"


def prepare(root):
    """Normalize Confluence renderer markup in place into plain semantic HTML."""
    for t in root(["script", "style", "svg", "noscript", "iframe"]):
        t.decompose()
    for t in root.select("[data-testid=anchor-button], [data-testid=copy-link-button], "
                         "[data-testid=reactions-container], [data-testid=comment-container]"):
        t.decompose()
    for t in root.select('[role=presentation] > button:empty'):
        t.decompose()
    # images
    for img in root.find_all("img"):
        alt = (img.get("alt") or "").strip()
        src = img.get("src") or ""
        if "/aa-avatar/" in src or "emoji" in src:        # user avatars, emoji
            img.decompose()
            continue
        nm = img_name(img)
        img.replace_with(NavigableString(f"![{alt or nm}]({nm})"))
    # status lozenges -> [TEXT]
    for sp in root.select(".status-lozenge-span, [data-prosemirror-node-name=status]"):
        txt = clean_text(sp.get_text())
        sp.replace_with(NavigableString(f"[{txt}] " if txt else ""))
    # headings: renderer wraps text in anchors/wrappers; keep tag, flatten
    # panels (info/note/warning) -> blockquote
    for pn in root.select(".ak-editor-panel"):
        content = pn.select_one(".ak-editor-panel__content") or pn
        bq = root.new_tag("blockquote")
        for ch in list(content.children):
            bq.append(ch.extract())
        pn.replace_with(bq)
    # code blocks
    for cb in root.select("[data-ds--code--code-block], [data-testid=renderer-code-block], .code-block"):
        lines = cb.select("[data-ds--code--row], .linenumber ~ *")
        code = cb.find("code")
        text = (code or cb).get_text("\n" if False else "")
        if code is not None:
            rows = code.find_all(attrs={"data-ds--code--row": True}, recursive=True)
            text = "\n".join(r.get_text("") for r in rows) if rows else code.get_text("")
        pre = root.new_tag("pre")
        c = root.new_tag("code")
        c.string = text
        pre.append(c)
        cb.replace_with(pre)
    # Jira issue macro / inline smart cards / links with trailing "Preview" buttons
    for sp in root.find_all("span"):
        if sp.decomposed if hasattr(sp, "decomposed") else False:
            continue
        t = clean_text(sp.get_text())
        if t == "Preview" and not sp.find("a"):
            sp.decompose()
        elif t == "UNDEFINED" and sp.find_parent("a"):
            sp.decompose()
    for b in root.find_all("button"):
        t = clean_text(b.get_text())
        if not t or t in ("Preview", "Copy", "Add a reaction") or t.startswith("Open image"):
            b.decompose()
        else:
            b.unwrap()
    for sp in root.select("[data-testid=smart-block-title-resolved-view]"):
        pass
    # expand macros: keep title as bold line
    for tag in root.find_all(attrs={"role": "img"}):
        if not tag.get_text(strip=True):
            tag.decompose()
    # emoji spans
    for e in root.select("[data-testid=emoji-wrapper], .emoji-common-node"):
        e.replace_with(NavigableString(e.get("aria-label") or e.get("title") or e.get_text() or ""))
    # tables: drop sticky helper duplicates
    for t in root.select("[data-testid=sticky-table-fixed], [data-testid^=sticky-scrollbar]"):
        t.decompose()


def to_md(node):
    for t in node.find_all("code"):
        pass
    md = markdownify(str(node), heading_style="ATX", bullets="-", code_language="")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def table_md(table):
    rows = []
    for tr in table.find_all("tr"):
        cells = [clean_text(c.get_text(" ")).replace("|", "\\|") for c in tr.find_all(["th", "td"])]
        rows.append(cells)
    return rows


def rows_to_md(rows):
    if not rows:
        return ""
    w0 = max(len(r) for r in rows)
    rows = [r + [""] * (w0 - len(r)) for r in rows]
    keep = [i for i in range(w0) if any(r[i] for r in rows[1:]) or rows[0][i]]
    keep = [i for i in keep if any(r[i] for r in rows)]
    rows = [[r[i] for i in keep] for r in rows]
    if rows and rows[0] and rows[0][0] == "" and any(rows[0]):
        rows[0][0] = "#"
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + " --- |" * w]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def parse_url(loc):
    u = urlparse(loc)
    m = re.search(r"/spaces/([^/]+)/(pages|folder|database)/(\d+)", u.path)
    if not m:
        return loc.split("?")[0], "", "page", ""
    space, kind, pid = m.groups()
    return f"{u.scheme}://{u.netloc}{u.path}", space, {"pages": "page"}.get(kind, kind), pid


def extract(loc, snap, parts, instance, tags_extra, space_name=""):
    url, space, kind, pid = parse_url(loc)
    soup = BeautifulSoup(parts[0], "html.parser")
    for t in soup(["script", "style", "svg"]):
        t.decompose()
    main = soup.select_one("[role=main]") or soup.body
    # title
    h1 = main.select_one("[data-testid=title-text]") or main.find("h1")
    crumb = soup.select_one("[data-testid*=breadcrumb]")
    crumb_txt = clean_text(crumb.get_text(" ")) if crumb else ""
    if not crumb_txt:
        m0 = re.match(r"^(.*? / .*?)(?: Edited .*| Share Copy.*)", clean_text(main.get_text(" ")))
        crumb_txt = m0.group(1) if m0 else ""
    title = clean_text(h1.get_text(" ")) if h1 else ""
    if not title and crumb_txt and " / " in crumb_txt:
        title = crumb_txt.split(" / ")[-1]
    if not title:
        space_part = f"(?: - {re.escape(space_name)})?" if space_name else ""
        title = re.sub(rf"{space_part} - Confluence$", "", (soup.title.string or "").strip())
    # byline
    by = soup.select_one("[data-testid=byline-single-line]") or soup.select_one("[data-testid=content-title-and-byline]")
    authors = []
    if by:
        for sp in by.find_all("span"):
            t = clean_text(sp.get_text())
            if t.startswith("By ") and len(sp.find_all("span")) == 0:
                authors.append(t[3:])
    if not authors:
        m1 = re.search(r"\bBy ([A-Z][^\n]*?) (?:Name Collaborators|Last edited|\d+ min|Add a reaction)", clean_text(main.get_text(" ")))
        if m1:
            authors.append(m1.group(1))
    mt = clean_text(main.get_text(" "))
    em = re.search(r"\bEdited ((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}(?:, \d{4})?|\w+ \w+ ago|yesterday|today)", mt)
    edited_label = em.group(1) if em else ""
    version = ""
    mv = re.search(r"\bVersion (\d+)\b", mt)
    if mv:
        version = mv.group(1)

    body, note = "", ""
    content = soup.select_one("#content .ak-renderer-document") or soup.select_one(".ak-renderer-document")
    if content is not None:
        prepare(content)
        # header table-of-contents / children macros are plain text already
        body = to_md(content)
        # byline owner for pages is the "By" line; page comments below
    elif kind == "folder":
        tbl = main.find("table")
        rows = []
        if tbl:
            for tr in tbl.find_all("tr"):
                cells = [clean_text(c.get_text(" ")) for c in tr.find_all(["th", "td"])]
                if not cells:
                    continue
                cells[0] = re.sub(r"\s*More actions.*$", "", cells[0])
                rows.append([c for c in cells if c != "Actions"][:3])
        if rows:
            body = "Folder contents (listing as shown):\n\n" + rows_to_md(rows)
        else:
            body = NOT_CAPTURED
    elif kind == "database":
        db = None
        for ptxt in parts[1:]:
            s2 = BeautifulSoup(ptxt, "html.parser")
            for t in s2(["script", "style", "svg"]):
                t.decompose()
            g = s2.select_one("[role=grid]") or s2.find("table")
            if g:
                db = g
                break
        if db is not None:
            rows = table_md(db)
            rows = [r for r in rows if any(r)]
            # drop leading row-number column when the header cell is empty
            if rows and rows[0] and rows[0][0] == "" and all(len(r) == len(rows[0]) for r in rows):
                pass
            body = "Confluence database (rows as shown in the snapshot):\n\n" + rows_to_md(rows)
            note = f"{len(rows) - 1} rows"
        else:
            body = NOT_CAPTURED
    if not body.strip():
        body = NOT_CAPTURED
    # comments
    comments = ""
    cm = soup.select_one("[data-testid=object-comments-list-container]")
    if cm is not None and cm.get_text(strip=True):
        prepare(cm)
        comments = to_md(cm)
    return dict(url=url, space=space, kind=kind, pid=pid, title=title, crumb=crumb_txt, authors=authors,
                edited_label=edited_label, version=version, body=body, comments=comments, note=note)


def tags_for(title, tags_extra, instance, rules):
    t = title.lower()
    tags = [instance, "confluence"]
    for key, tag in rules:
        if key.lower() in t and tag not in tags:
            tags.append(tag)
    return tags + [x for x in tags_extra if x not in tags]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("srcs", nargs="+")
    ap.add_argument("--instance", required=True, help="Confluence Cloud instance name (<name>.atlassian.net)")
    ap.add_argument("--space-name", default="",
                    help="space name Confluence puts in the browser title ('<page> - <space> - Confluence'); stripped from fallback titles")
    ap.add_argument("--tag-rule", action="append", default=[], metavar="keyword=tag",
                    help="add tag when keyword occurs in the page title (repeatable)")
    ap.add_argument("--tags", default="")
    ap.add_argument("--ingested", default=datetime.date.today().isoformat())
    ap.add_argument("--sensitivity", default="confidential")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    out_dir = Path(a.out_dir)
    extra = [t for t in a.tags.split(",") if t]
    used, total_redacted = set(), 0
    for src in a.srcs:
        p = Path(src)
        if p.suffix.lower() != ".mhtml":
            print(f"skip {p.name}: not .mhtml (handle .md separately)")
            continue
        loc, date_hdr, parts = load_mhtml(p)
        if not parts:
            print(f"{p.name}: no text/html part")
            continue
        d = extract(loc, date_hdr, parts, a.instance, extra, a.space_name)
        try:
            snap = datetime.datetime.strptime(date_hdr, "%a, %d %b %Y %H:%M:%S %z").date().isoformat()
        except ValueError:
            snap = "unknown"
        slug = slugify(d["title"])
        base, i = slug, 2
        while slug in used:
            slug = f"{base[:57]}-{i}"
            i += 1
        used.add(slug)
        body, n1 = redact(d["body"])
        comments, n2 = redact(d["comments"])
        total_redacted += n1 + n2
        year = snap[:4] if snap != "unknown" else ""
        sd = "unknown"
        if d["edited_label"]:
            lab = d["edited_label"]
            if re.match(r"[A-Z][a-z]{2} \d{1,2}, \d{4}$", lab):
                sd = datetime.datetime.strptime(lab, "%b %d, %Y").date().isoformat()
            elif re.match(r"[A-Z][a-z]{2} \d{1,2}$", lab) and year:
                sd = datetime.datetime.strptime(f"{lab} {year}", "%b %d %Y").date().isoformat()
        vlab = ""
        mv = re.search(r"(?:^|\b)(V\d+|v\d+)\b", d["title"])
        if mv:
            vlab = mv.group(1).lower()
        body_plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)
        body_plain = re.sub(r"[*_`]", "", body_plain)
        first = next((l.strip() for l in body_plain.splitlines()
                      if len(l.strip()) > 25 and not l.lstrip().startswith(("#", "|", "-", "!", "```", ">", "Parent page", "Related"))), d["title"])
        kind_word = {"page": "Confluence page", "folder": "Confluence folder", "database": "Confluence database"}[d["kind"]]
        summary = f"{kind_word} \"{d['title']}\" in space {d['space']}: " + re.sub(r"\s+", " ", first)[:200]
        if body.strip() == NOT_CAPTURED:
            summary = f"{kind_word} \"{d['title']}\" in space {d['space']}; body not captured in the browser snapshot."
        fm = ["---", f"title: {yaml_str(d['title'])}",
              "source: " + yaml_str("confluence:%s/%s/%s=%s" % (a.instance, d["space"], d["kind"], d["pid"])),
              f"url: {yaml_str(d['url'])}", "type: articles", f"ingested: {a.ingested}",
              "tags: [" + ", ".join(tags_for(d["title"], extra, a.instance, [tuple(r.rsplit("=", 1)) for r in a.tag_rule])) + "]",
              f"summary: {yaml_str(summary)}",
              "authors: [" + (", ".join(yaml_str(x) for x in d["authors"]) if d["authors"] else "unknown") + "]",
              f"source_date: {sd}"]
        if d["edited_label"]:
            fm.append(f"edited_label: {yaml_str(d['edited_label'])}")
        fm.append(f"snapshot_date: {snap}")
        if d["version"]:
            fm.append(f"page_version: {d['version']}")
        if vlab:
            fm.append(f"version_label: {yaml_str(vlab)}")
        if d["crumb"] and d["crumb"].count(" / ") >= 2:
            fm.append(f"parent: {yaml_str(d['crumb'])}")
        fm += [f"sensitivity: {a.sensitivity}", "---", "", f"# {d['title']}", "",
               f"> Verbatim Markdown conversion of a browser snapshot (`{p.name}`, saved {snap}). "
               f"The original stays in Confluence; see `url`.", "", ""]
        text = "\n".join(fm) + body + "\n"
        if comments:
            text += "\n## Comments\n\n" + comments + "\n"
        out = out_dir / f"{a.ingested}-confluence-{slug}.local.md"
        words = len(re.findall(r"\S+", body))
        if not a.dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
        print(f"{out.name} | {d['title']} | {d['kind']} | {sd} | ~{words}w | red={n1 + n2} {d['note']}")
    print(f"redactions total: {total_redacted}")


if __name__ == "__main__":
    main()
