"""Export Confluence pages and Jira issues to verbatim .local.md raw sources, with no LLM.

Usage:
  atlassian_export.py confluence <page_id> [<page_id> ...] --out DIR [--tree] [--tags t1,t2] [--files DIR]
  atlassian_export.py jira --jql "project = KEY" --out DIR [--tags t1,t2] [--files DIR]
  common: [--profile NAME] [--confluence-url URL] [--jira-url URL] [--title-suffix TEXT]
Run: uv run --no-project --with markdownify --with beautifulsoup4 python -I atlassian_export.py ...

Attachments: every export lists them in an "## Attachments" section (name, type, size,
author, date, URL). With --files DIR the files themselves are downloaded to
DIR/confluence/<pageId>/ and DIR/jira/<KEY>/ (up to --max-mb each, default 25) and the
section also gives the local path. DIR must be outside every wiki (binary files never go
into one): use the folder where the project's originals are archived. Images keep their file name as alt text; the "Contents"
macro is dropped. Confluence labels go to frontmatter, inline comments are marked as such,
Jira remote links (Confluence pages, external URLs) and subtasks are listed.
Confluence pages also get a version history and page restrictions (when the server exposes
them); Jira issues get a change history (status, assignee, sprint, ...).

--convert (needs --files): attachment contents become their own raw sources next to the
page, named <page-file>--att-<name>.local.md: .pptx/.docx/.pdf/.md/.txt/.csv/.json via
doc2md.py (run through uv with python-pptx, python-docx, pypdf), .drawio diagrams as a node
and edge list (no LLM). Text files over --max-text-kb are skipped. Spreadsheets and images
are not converted (analyse them with Python code when needed). Images are described on
demand by describe_images.py; the "## Images" section it adds is kept on re-export.
A page is re-exported when its version or its attachments (name, version, size) change.

Replaces MCP-driven export by agents (~950k tokens for one project's full export).
Writes frontmatter with source, url,
authors, source_date, page_version (Confluence) or issues (Jira), then the
body as Markdown and the comments. Jira issues are grouped into one file per
epic (epic first, then its children); issues without an epic get their own file.

Incremental: a Confluence page whose file already records the same
page_version, or a Jira file whose recorded `jira_updated` matches, is skipped.
Changed sources are overwritten; the file is a verbatim copy, never edited by hand.

Hosts, Keychain item names and the title suffix: flags, environment or a profile in
~/.config/wiki-kit/atlassian.json; tokens from CONFLUENCE_TOKEN / JIRA_TOKEN or the macOS
Keychain, never from files (see atlassian_config.py). Secrets in page text are not redacted here:
run raw_check.py on the output and redact real credentials it reports.
"""
import argparse, base64, datetime, hashlib, json, os, re, subprocess, sys, tempfile, urllib.parse, urllib.request, zlib

from bs4 import BeautifulSoup
from markdownify import markdownify

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling import under python3 -I
import atlassian_config  # noqa: E402

CFG = {}  # set in main() from flags, environment and profile
CONFLUENCE = JIRA = TITLE_SUFFIX = ""
TODAY = datetime.date.today().isoformat()
# A Cloudflare front end can answer 403 to the default "Python-urllib/x.y" agent.
UA = "atlassian_export/1.0"


def token(service):
    return atlassian_config.token(service, CFG)


def get(base, path, service, **params):
    url = base + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token(service)}",
                                               "Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def slug(s, n=60):
    s = re.sub(r"[^\w\s-]", "", s.lower(), flags=re.UNICODE)
    return re.sub(r"[\s_-]+", "-", s).strip("-")[:n].rstrip("-")


def md(html):
    soup = BeautifulSoup(html or "", "html.parser")
    for t in soup.select(".toc-macro"):
        t.decompose()
    for img in soup.find_all("img"):
        if not (img.get("alt") or "").strip():
            src = img.get("data-image-src") or img.get("src") or ""
            img["alt"] = urllib.parse.unquote(src.split("?")[0].rsplit("/", 1)[-1])
    return markdownify(str(soup), heading_style="ATX", bullets="-").strip()


def human(n):
    n = float(n or 0)
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024


def fetch(url, service, dest, max_mb):
    """Download one attachment; returns a note: local path, 'unchanged', or why it was skipped."""
    if os.path.exists(dest):
        return dest
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token(service)}",
                                               "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            size = int(r.headers.get("Content-Length") or 0)
            if size > max_mb * 1024 * 1024:
                return f"skipped: {human(size)} > {max_mb} MB"
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                while chunk := r.read(1 << 20):
                    fh.write(chunk)
    except Exception as e:
        return f"download failed: {e}"
    return dest


def attachments_md(items, files_dir, sub, service, max_mb):
    """items: dicts with name, type, size, author, date, url. Returns Markdown lines."""
    if not items:
        return [], []
    got = []
    rows = ["## Attachments" if sub == "page" else "### Attachments", "",
            "| File | Type | Size | Author | Date | Local copy |", "|---|---|---|---|---|---|"]
    for a in items:
        local = "—"
        if files_dir:
            safe = re.sub(r"[^\w.() -]", "_", a["name"], flags=re.UNICODE)
            local = fetch(a["url"], service, os.path.join(files_dir, a["dir"], safe), max_mb)
            if local.startswith("/"):
                got.append((a, local))
                local = "`" + local.replace(os.path.expanduser("~"), "~") + "`"
        rows.append(f"| [{a['name']}]({a['url']}) | {a['type']} | {human(a['size'])} | {a['author']} | {a['date']} | {local} |")
    return rows + [""], got


CONVERTIBLE = {".pptx", ".docx", ".pdf", ".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".drawio"}
PLAN = []  # doc2md items, run once at the end


def drawio_md(path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(path).getroot()
    out = []
    for d in (tree.iter("diagram") if tree.tag == "mxfile" else [tree]):
        model = d.find("mxGraphModel") if d.tag == "diagram" else d
        if model is None and (d.text or "").strip():
            try:
                raw = zlib.decompress(base64.b64decode(d.text.strip()), -15).decode("utf-8")
                model = ET.fromstring(urllib.parse.unquote(raw))
            except Exception:
                model = None
        if model is None:
            continue
        cells = {c.get("id"): c for c in model.iter("mxCell")}
        def label(c):
            v = c.get("value") or ""
            return re.sub(r"\s+", " ", BeautifulSoup(v, "html.parser").get_text(" ")).strip()
        out += [f"## Diagram: {d.get('name', 'page')}", "", "### Nodes", ""]
        for c in cells.values():
            if c.get("vertex") and label(c):
                par = cells.get(c.get("parent"))
                pl = label(par) if par is not None else ""
                out.append(f"- {label(c)}" + (f" (in {pl})" if pl else ""))
        out += ["", "### Edges", ""]
        for c in cells.values():
            if c.get("edge"):
                a, b = cells.get(c.get("source")), cells.get(c.get("target"))
                if a is not None and b is not None and (label(a) or label(b)):
                    out.append(f"- {label(a) or '?'} -> {label(b) or '?'}" + (f" [{label(c)}]" if label(c) else ""))
        out.append("")
    return "\n".join(out)


def convert_attachments(got, page_path, title, source, tags, out, max_text_kb):
    """Turn downloaded attachments into raw sources beside the page file."""
    stem = page_path[:-len(".local.md")]
    for a, local in got:
        ext = os.path.splitext(local)[1].lower()
        if ext not in CONVERTIBLE:
            continue
        if ext in {".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml"} and os.path.getsize(local) > max_text_kb * 1024:
            print(f"skip    {a['name']}: text over {max_text_kb} KB")
            continue
        tgt = f"{stem}--att-{slug(os.path.splitext(a['name'])[0], 50)}.local.md"
        if recorded(tgt, "att_size") == str(a["size"]):
            continue
        if os.path.exists(tgt):
            os.remove(tgt)
        if ext == ".drawio":
            body = drawio_md(local)
            fm = ["---", f"title: {yaml_str(title + ' — attachment ' + a['name'])}", f"source: {yaml_str(source + '/attachment/' + a['name'])}",
                  "type: data", f"ingested: {TODAY}", f"tags: [{', '.join(tags + ['attachment', 'diagram'])}]",
                  f"summary: {yaml_str(summary(body))}", f"authors: [{a['author']}]", f"source_date: {a['date']}",
                  f"att_size: {a['size']}", "---", "", f"# {a['name']}", "", body, ""]
            open(tgt, "w", encoding="utf-8").write("\n".join(fm))
            print("new     " + tgt)
        else:
            PLAN.append({"src": local, "out": tgt, "title": title + " — attachment " + a["name"],
                         "type": "articles", "tags": tags + ["attachment"], "source_date": a["date"],
                         "authors": [a["author"]], "source": source + "/attachment/" + a["name"],
                         "extra": {"att_size": str(a["size"])}})


def run_plan():
    if not PLAN:
        return
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(PLAN, fh)
    r = subprocess.run(["uv", "run", "--no-project", "--with", "python-pptx", "--with", "python-docx",
                        "--with", "pypdf", "python", "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc2md.py"),
                        fh.name], capture_output=True, text=True)
    os.unlink(fh.name)
    for it in PLAN:
        print(("new     " if os.path.exists(it["out"]) else "FAILED  ") + it["out"])
    if r.returncode:
        print(r.stderr[-800:], file=sys.stderr)


def yaml_str(s):
    return json.dumps(s or "", ensure_ascii=False)


def summary(text):
    t = re.sub(r"\s+", " ", re.sub(r"[#>*_`|\[\]]", " ", text)).strip()
    return t[:240] + ("…" if len(t) > 240 else "")


def recorded(path, key):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh):
            if n and line.strip() == "---":
                break
            if line.startswith(key + ":"):
                return line.split(":", 1)[1].strip().strip('"')
    return None


def kept_images(prev):
    """The '## Images' section added by describe_images.py survives a re-export."""
    if not prev:
        return []
    m = re.search(r"\n(## Images\n.*?)(?=\n## |\Z)", open(prev, encoding="utf-8").read(), re.S)
    return ["", m.group(1).rstrip(), ""] if m else []


def existing_by_source(out, source):
    """Find a file in out that already exports this source (names change when titles change)."""
    for f in os.listdir(out):
        if f.endswith(".local.md"):
            p = os.path.join(out, f)
            with open(p, encoding="utf-8") as fh:
                head = fh.read(2000)
            if f'source: "{source}"' in head:
                return p
    return None


# ---------------- Confluence ----------------

def confluence_page(pid, out, tags, stats, files_dir=None, max_mb=25, convert=False, max_text_kb=300):
    p = get(CONFLUENCE, f"/rest/api/content/{pid}", "confluence",
            expand="body.export_view,version,history,space,ancestors")
    space = p["space"]["key"]
    source = f"confluence:{space}/pageId={pid}"
    prev = existing_by_source(out, source)
    version = p["version"]["number"]
    atts, start = [], 0
    while True:
        r = get(CONFLUENCE, f"/rest/api/content/{pid}/child/attachment", "confluence",
                expand="version,metadata", start=start, limit=100)
        for a in r["results"]:
            ext = a.get("extensions", {})
            atts.append({"name": a["title"], "type": ext.get("mediaType", "?"), "size": ext.get("fileSize", 0),
                         "author": a["version"]["by"].get("displayName", "unknown"),
                         "date": a["version"]["when"][:10], "dir": os.path.join("confluence", pid),
                         "url": CONFLUENCE + a["_links"]["download"], "ver": a["version"]["number"]})
        if r["size"] < r["limit"]:
            break
        start += r["limit"]
    sig = hashlib.sha1("|".join(f"{a['name']}:{a['ver']}:{a['size']}" for a in sorted(atts, key=lambda a: a["name"])).encode()).hexdigest()[:12]
    if prev and recorded(prev, "page_version") == str(version) and recorded(prev, "attachments_sig") == sig:
        stats["skipped"] += 1
        return
    comments = get(CONFLUENCE, f"/rest/api/content/{pid}/child/comment", "confluence",
                   expand="body.export_view,history,extensions.inlineProperties", depth="all",
                   limit=200).get("results", [])
    labels = [l["name"] for l in get(CONFLUENCE, f"/rest/api/content/{pid}/label", "confluence",
                                     limit=200).get("results", [])]
    try:
        versions = get(CONFLUENCE, f"/rest/experimental/content/{pid}/version", "confluence",
                       limit=200).get("results", [])
    except Exception:
        versions = []
    try:
        rs = get(CONFLUENCE, f"/rest/api/content/{pid}/restriction/byOperation", "confluence",
                 expand="restrictions.user,restrictions.group")
        restr = []
        for op, v in rs.items():
            if not isinstance(v, dict):
                continue
            who = [u.get("displayName", "?") for u in v.get("restrictions", {}).get("user", {}).get("results", [])]
            who += [g.get("name", "?") for g in v.get("restrictions", {}).get("group", {}).get("results", [])]
            if who:
                restr.append(f"{op}: {', '.join(who)}")
    except Exception:
        restr = []
    body = md(p["body"]["export_view"]["value"])
    parent = p["ancestors"][-1]["id"] if p.get("ancestors") else None
    lines = ["---",
             f"title: {yaml_str(p['title'] + TITLE_SUFFIX)}",
             f"source: {yaml_str(source)}",
             f"url: {yaml_str(CONFLUENCE + '/pages/viewpage.action?pageId=' + pid)}",
             "type: articles",
             f"ingested: {TODAY}",
             f"tags: [{', '.join(tags + ['confluence'])}]",
             f"summary: {yaml_str(summary(body))}",
             f"authors: [{p['version']['by'].get('displayName', 'unknown')}]",
             f"source_date: {p['version']['when'][:10]}",
             f"created: {p['history']['createdDate'][:10]}",
             f"page_version: {version}",
             f"attachments_sig: {sig}"]
    if labels:
        lines.append(f"labels: [{', '.join(labels)}]")
    if restr:
        lines.append(f"restrictions: {yaml_str('; '.join(restr))}")
    if parent:
        lines.append(f"parent: {yaml_str(f'confluence:{space}/pageId={parent}')}")
    lines += ["---", "", f"# {p['title']}", "", body, ""]
    rows, got = attachments_md(atts, files_dir, "page", "confluence", max_mb)
    lines += rows
    if versions:
        lines += ["## Version history", "", "| Version | Author | Date | Message |", "|---|---|---|---|"]
        for v in sorted(versions, key=lambda v: v.get("number", 0), reverse=True):
            lines.append(f"| {v.get('number')} | {(v.get('by') or {}).get('displayName', 'unknown')} | "
                         f"{(v.get('when') or '')[:10]} | {(v.get('message') or '').replace('|', '/')} |")
        lines.append("")
    if comments:
        lines += ["## Comments", ""]
        for c in comments:
            who = c.get("history", {}).get("createdBy", {}).get("displayName", "unknown")
            when = c.get("history", {}).get("createdDate", "")[:10]
            inl = (c.get("extensions", {}).get("inlineProperties") or {}).get("originalSelection")
            lines += [f"### {who}, {when}" + (" (inline comment)" if "inlineProperties" in c.get("extensions", {}) else ""), ""]
            if inl:
                lines += [f"> On text: {inl}", ""]
            lines += [md(c["body"]["export_view"]["value"]), ""]
    path = prev or os.path.join(out, f"{TODAY}-confluence-{slug(p['title'])}.local.md")
    lines += kept_images(prev)
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    stats["updated" if prev else "new"] += 1
    print(("updated " if prev else "new     ") + path)
    if convert:
        convert_attachments(got, path, p["title"], source, tags, out, max_text_kb)


def confluence_children(pid):
    ids, start = [], 0
    while True:
        r = get(CONFLUENCE, f"/rest/api/content/{pid}/child/page", "confluence", start=start, limit=100)
        ids += [x["id"] for x in r["results"]]
        if r["size"] < r["limit"]:
            return ids
        start += r["limit"]


# ---------------- Jira ----------------

def jira_fields():
    f = get(JIRA, "/rest/api/2/field", "jira")
    return {x["name"]: x["id"] for x in f}


def person(u):
    return f"{u['displayName']} ({u.get('emailAddress', '')})" if u else "—"


def issue_md(i, F, files_dir=None, max_mb=25):
    f, r = i["fields"], i.get("renderedFields") or {}
    def cf(name):
        v = f.get(F.get(name, "_none"))
        if isinstance(v, list):
            return ", ".join(re.sub(r".*name=([^,]+).*", r"\1", str(x)) if "name=" in str(x) else str(x.get("value", x) if isinstance(x, dict) else x) for x in v) or "—"
        return (v.get("value") if isinstance(v, dict) else v) or "—"
    remote = []
    try:
        for x in get(JIRA, f"/rest/api/2/issue/{i['key']}/remotelink", "jira"):
            o = x.get("object", {})
            remote.append(f"  - [{o.get('title', x.get('relationship', 'link'))}]({o.get('url', '')})")
    except Exception:
        pass
    links = []
    for l in f.get("issuelinks", []):
        o = l.get("outwardIssue") or l.get("inwardIssue")
        rel = l["type"]["outward"] if "outwardIssue" in l else l["type"]["inward"]
        links.append(f"  - {l['type']['name']} — {rel} {o['key']} \"{o['fields']['summary']}\" "
                     f"({o['fields']['issuetype']['name']}, {o['fields']['status']['name']})")
    out = [f"## {i['key']} — {f['summary']}", "",
           f"- **URL:** {JIRA}/browse/{i['key']}",
           f"- **Type:** {f['issuetype']['name']}",
           f"- **Status:** {f['status']['name']} (category: {f['status']['statusCategory']['name']})",
           f"- **Resolution:** {(f.get('resolution') or {}).get('name', '—')}",
           f"- **Priority:** {(f.get('priority') or {}).get('name', '—')}",
           f"- **Assignee:** {person(f.get('assignee'))}",
           f"- **Reporter:** {person(f.get('reporter'))}",
           f"- **Created:** {f['created'][:19].replace('T', ' ')}",
           f"- **Updated:** {f['updated'][:19].replace('T', ' ')}",
           f"- **Resolved:** {(f.get('resolutiondate') or '—')[:19].replace('T', ' ')}",
           f"- **Due date:** {f.get('duedate') or '—'}",
           f"- **Labels:** {', '.join(f.get('labels', [])) or '—'}",
           f"- **Components:** {', '.join(c['name'] for c in f.get('components', [])) or '—'}",
           f"- **Fix versions:** {', '.join(v['name'] for v in f.get('fixVersions', [])) or '—'}",
           f"- **Sprint(s):** {cf('Sprint')}",
           f"- **Story points:** {cf('Story Points')}",
           f"- **Epic Link:** {cf('Epic Link')}",
           f"- **Parent:** {(f.get('parent') or {}).get('key', '—')}",
           f"- **Subtasks:** {', '.join(x['key'] + ' ' + x['fields']['summary'] for x in f.get('subtasks', [])) or '—'}",
           "- **Issue links:**" + ("" if links else " —"), *links,
           "- **Remote links:**" + ("" if remote else " —"), *remote, "",
           "### Description", "", md(r.get("description")) or "-", ""]
    atts = [{"name": a["filename"], "type": a.get("mimeType", "?"), "size": a.get("size", 0),
             "author": (a.get("author") or {}).get("displayName", "unknown"), "date": a["created"][:10],
             "dir": os.path.join("jira", i["key"]), "url": a["content"]} for a in f.get("attachment", [])]
    rows, got = attachments_md(atts, files_dir, "issue", "jira", max_mb)
    out += rows
    GOT.extend((a, l, i["key"]) for a, l in got)
    comments = (f.get("comment") or {}).get("comments", [])
    rcomments = ((r.get("comment") or {}).get("comments")) or []
    if comments:
        out += ["### Comments", ""]
        for n, c in enumerate(comments):
            html = rcomments[n]["body"] if n < len(rcomments) else c["body"]
            out += [f"#### {c['author']['displayName']}, {c['created'][:10]}", "", md(html), ""]
    hist = []
    for h in sorted((i.get("changelog") or {}).get("histories", []), key=lambda h: h["created"]):
        for it in h["items"]:
            if it["field"] in ("status", "assignee", "resolution", "priority", "Sprint", "Fix Version", "Epic Link", "summary"):
                hist.append(f"- {h['created'][:16].replace('T', ' ')} {h['author']['displayName']}: {it['field']}: "
                            f"{it.get('fromString') or '—'} → {it.get('toString') or '—'}")
    if hist:
        out += ["### History", "", *hist, ""]
    return out


GOT = []  # (attachment, local path, issue key) collected while rendering Jira issues


def jira_export(jql, out, tags, stats, files_dir=None, max_mb=25, convert=False, max_text_kb=300):
    F = jira_fields()
    epic_field = F.get("Epic Link")
    issues, start = [], 0
    while True:
        r = get(JIRA, "/rest/api/2/search", "jira", jql=jql, startAt=start, maxResults=50,
                fields="*all", expand="renderedFields,changelog")
        issues += r["issues"]
        start += len(r["issues"])
        if start >= r["total"] or not r["issues"]:
            break
    by_key = {i["key"]: i for i in issues}
    groups = {}
    for i in issues:
        f = i["fields"]
        if f["issuetype"]["name"] == "Epic":
            root = i["key"]
        else:
            root = (epic_field and f.get(epic_field)) or (f.get("parent") or {}).get("key") or i["key"]
            if root not in by_key:
                root = i["key"]
        groups.setdefault(root, []).append(i)
    for root, members in groups.items():
        members.sort(key=lambda i: (i["key"] != root, int(i["key"].split("-")[1])))
        head = by_key[root]
        source = f"jira:{root}" + (" (epic) + child issues" if len(members) > 1 else "")
        latest = max(i["fields"]["updated"] for i in members)
        prev = existing_by_source(out, source)
        if prev and recorded(prev, "jira_updated") == latest:
            stats["skipped"] += 1
            continue
        hf = head["fields"]
        GOT.clear()
        body = [l for i in members for l in issue_md(i, F, files_dir, max_mb)]
        lines = ["---",
                 f"title: {yaml_str(f'Jira {root}: ' + hf['summary'])}",
                 f"source: {yaml_str(source)}",
                 f"url: {yaml_str(f'{JIRA}/browse/{root}')}",
                 "type: data",
                 f"ingested: {TODAY}",
                 f"tags: [{', '.join(tags + ['jira'])}]",
                 f"summary: {yaml_str(summary(md((head.get('renderedFields') or {}).get('description')) or hf['summary']))}",
                 f"authors: [{(hf.get('reporter') or {}).get('displayName', 'unknown')}]",
                 f"source_date: {latest[:10]}",
                 f"jira_updated: {latest}",
                 f"jql: {yaml_str(jql)}",
                 f"issues: [{', '.join(i['key'] for i in members)}]",
                 "---", "", f"# Jira {root}: {hf['summary']}", "", *body]
        path = prev or os.path.join(out, f"{TODAY}-jira-{root.lower()}-{slug(hf['summary'], 50)}.local.md")
        lines += kept_images(prev)
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        stats["updated" if prev else "new"] += 1
        print(("updated " if prev else "new     ") + path)
        if convert:
            for a, l, key in list(GOT):
                convert_attachments([({**a, "name": f"{key}-{a['name']}"}, l)], path, f"Jira {root}", f"jira:{root}", tags, out, max_text_kb)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("system", choices=["confluence", "jira"])
    ap.add_argument("ids", nargs="*", help="Confluence page ids")
    ap.add_argument("--jql")
    ap.add_argument("--tree", action="store_true", help="also export all descendant pages")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tags", default="")
    ap.add_argument("--files", help="download attachments here (outside the wiki)")
    ap.add_argument("--max-mb", type=int, default=25, help="skip attachments larger than this")
    ap.add_argument("--convert", action="store_true", help="turn attachment contents into raw sources (needs --files)")
    ap.add_argument("--max-text-kb", type=int, default=300, help="skip text attachments larger than this when converting")
    ap.add_argument("--profile", help="profile in ~/.config/wiki-kit/atlassian.json")
    ap.add_argument("--confluence-url")
    ap.add_argument("--jira-url")
    ap.add_argument("--title-suffix", help="appended to Confluence page titles")
    a = ap.parse_args()
    global CFG, CONFLUENCE, JIRA, TITLE_SUFFIX
    CFG = atlassian_config.settings(a.profile, confluence_url=a.confluence_url, jira_url=a.jira_url,
                                    confluence_title_suffix=a.title_suffix)
    CONFLUENCE, JIRA = CFG["confluence_url"], CFG["jira_url"]
    TITLE_SUFFIX = CFG["confluence_title_suffix"]
    atlassian_config.require(CFG, f"{a.system}_url")
    files = os.path.realpath(os.path.expanduser(a.files)) if a.files else None
    if a.convert and not files:
        sys.exit("--convert needs --files")
    if files and atlassian_config.inside_wiki(files):
        sys.exit("--files must not point into a wiki: binary files never go into it")
    os.makedirs(a.out, exist_ok=True)
    tags = [t for t in a.tags.split(",") if t]
    stats = {"new": 0, "updated": 0, "skipped": 0}
    if a.system == "confluence":
        todo, seen = list(a.ids), set()
        while todo:
            pid = todo.pop(0)
            if pid in seen:
                continue
            seen.add(pid)
            confluence_page(pid, a.out, tags, stats, files, a.max_mb, a.convert, a.max_text_kb)
            if a.tree:
                todo += confluence_children(pid)
    else:
        if not a.jql:
            sys.exit("--jql is required for jira")
        jira_export(a.jql, a.out, tags, stats, files, a.max_mb, a.convert, a.max_text_kb)
    run_plan()
    print(stats, file=sys.stderr)


if __name__ == "__main__":
    main()
