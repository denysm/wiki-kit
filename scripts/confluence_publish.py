"""Publish a set of Markdown files as Confluence pages, with no LLM.

Usage:
  uv run --no-project --with markdown python -I confluence_publish.py DIR --space KEY \
      --page home=123456 --page guide=234567 [--state FILE] [--apply]
      [--profile NAME] [--confluence-url URL]

Each DIR/*.md file (sorted by name) starts with a YAML-like block:
  ---
  title: Page title
  parent: <key of an existing page (--page) or of another file in DIR>
  key: <short key other files link to>
  ---
Links written as [text](page:<key>) or [text](page:<key>#anchor) become links to that page.
Files without the block (for example a Jira comment draft) are skipped.

Without --apply: dry run. Prints each page's title, parent, size and unresolved links.
With --apply: pass 1 creates missing pages with a stub body (or finds an existing page with
the same title in the space), pass 2 writes every body with all links resolved. Page ids are
kept in --state (default DIR/.published.json), so a re-run updates the same pages.

Host and token as in atlassian_export.py (Confluence Server/Data Center, personal access
token): flag, environment or a profile in ~/.config/wiki-kit/atlassian.json; the token from
CONFLUENCE_TOKEN or the macOS Keychain (see atlassian_config.py).
"""
import argparse, glob, json, os, re, sys, urllib.error, urllib.parse, urllib.request

import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling import under python3 -I
import atlassian_config  # noqa: E402

CFG = {}  # set in main() from flags, environment and profile
CONFLUENCE = ""
UA = "confluence_publish/1.0"
LINK = re.compile(r"\]\(page:([\w-]+)(#[^)]*)?\)")


def token():
    return atlassian_config.token("confluence", CFG)


def call(method, path, body=None, **params):
    url = CONFLUENCE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token()}", "Accept": "application/json",
        "Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path}: HTTP {e.code}: {e.read().decode()[:500]}")


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    meta = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    meta = {k.strip(): v.strip().strip('"') for k, v in meta.items()}
    for k in ("title", "parent", "key"):
        if not meta.get(k):
            sys.exit(f"{path}: missing '{k}' in header")
    meta["body"], meta["file"] = text[m.end():], os.path.basename(path)
    return meta


def url(page_id):
    return f"{CONFLUENCE}/pages/viewpage.action?pageId={page_id}"


def render(body, ids):
    unresolved = []

    def sub(m):
        key, anchor = m.group(1), m.group(2) or ""
        if key not in ids:
            unresolved.append(key)
            return m.group(0)
        return f"]({url(ids[key])}{anchor})"

    md = LINK.sub(sub, body)
    html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"],
                             output_format="xhtml")
    return html, unresolved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--space", required=True)
    ap.add_argument("--page", action="append", default=[], help="key=pageId of an existing page")
    ap.add_argument("--state")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--profile", help="profile in ~/.config/wiki-kit/atlassian.json")
    ap.add_argument("--confluence-url")
    a = ap.parse_args()
    global CFG, CONFLUENCE
    CFG = atlassian_config.settings(a.profile, confluence_url=a.confluence_url)
    CONFLUENCE = atlassian_config.require(CFG, "confluence_url")
    state_path = a.state or os.path.join(a.dir, ".published.json")
    ids = dict(p.split("=", 1) for p in a.page)
    if os.path.exists(state_path):
        ids.update(json.load(open(state_path)))
    pages = [p for p in (parse(f) for f in sorted(glob.glob(os.path.join(a.dir, "*.md")))) if p]
    keys = set(ids) | {p["key"] for p in pages}
    bad = False
    for p in pages:
        _, unresolved = render(p["body"], {k: "0" for k in keys})
        status = "update" if p["key"] in ids else "create"
        print(f"{p['file']}: {status} '{p['title']}' under {p['parent']}, {len(p['body'])} chars"
              + (f", UNRESOLVED links: {sorted(set(unresolved))}" if unresolved else ""))
        if p["parent"] not in keys:
            print(f"  ERROR: parent '{p['parent']}' unknown"); bad = True
        bad = bad or bool(unresolved)
    if bad:
        sys.exit("fix the errors above")
    if not a.apply:
        print("dry run; add --apply to publish")
        return
    for p in pages:  # pass 1: make sure every page exists, parents first (files are sorted)
        if p["key"] in ids:
            continue
        found = call("GET", "/rest/api/content", spaceKey=a.space, title=p["title"]).get("results", [])
        if found:
            ids[p["key"]] = found[0]["id"]
        else:
            r = call("POST", "/rest/api/content", {
                "type": "page", "title": p["title"], "space": {"key": a.space},
                "ancestors": [{"id": ids[p["parent"]]}],
                "body": {"storage": {"value": "<p>Publishing…</p>", "representation": "storage"}}})
            ids[p["key"]] = r["id"]
        json.dump({k: v for k, v in ids.items() if k in {q["key"] for q in pages}},
                  open(state_path, "w"), indent=1)
    for p in pages:  # pass 2: write the bodies with every link resolved
        html, _ = render(p["body"], ids)
        cur = call("GET", f"/rest/api/content/{ids[p['key']]}", expand="version")
        call("PUT", f"/rest/api/content/{ids[p['key']]}", {
            "id": ids[p["key"]], "type": "page", "title": p["title"],
            "ancestors": [{"id": ids[p["parent"]]}],
            "version": {"number": cur["version"]["number"] + 1},
            "body": {"storage": {"value": html, "representation": "storage"}}})
        print(f"{p['file']}: {url(ids[p['key']])}")


if __name__ == "__main__":
    main()
