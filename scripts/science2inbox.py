"""Claude Science results -> a wiki inbox, without a model.

Usage:
  science2inbox.py projects
  science2inbox.py list PROJECT [--all] [--wiki ROOT]
  science2inbox.py copy PROJECT ARTIFACT... --to INBOX [--force]

Claude Science (the desktop app) keeps each organization's state in
~/.claude-science/orgs/<org>/: a SQLite database (operon-cli.db) with projects,
artifacts and their versions, and the files under artifacts/<project>/. This
script reads both and never writes there: copy, never move, out of an
application folder.

PROJECT is a project id (proj_…) or a unique part of its name. ARTIFACT is a
file name as Science shows it (bpprc_verification_report.md) or a unique part
of it. `list` shows final artifacts (Science's agent output, not intermediate
files) with their latest version; --all adds intermediate files and uploads.
With --wiki it marks artifacts that already reached that wiki (a raw or inbox
file whose frontmatter has `science_artifact: <id>`).

`copy` writes the latest version of each artifact as
INBOX/<date>-claude-science-<name>.md with frontmatter (title, source,
authors: [Claude Science], source_date, science_project, science_artifact,
science_version) for /wiki:ingest. Only text artifacts (Markdown, plain text)
are copied; data files stay in Science, and the report names them so the raw
note can point to them. The layout of ~/.claude-science is the app's own and
may change between versions; the script stops with a message if it does.
"""
import argparse, datetime, glob, os, re, sqlite3, sys

HOME = os.path.expanduser("~/.claude-science")
TEXT = ("text/markdown", "text/plain")


def org_dir():
    orgs = sorted(glob.glob(os.path.join(HOME, "orgs", "*", "operon-cli.db")))
    if not orgs:
        sys.exit(f"no Claude Science database under {HOME}/orgs/*/operon-cli.db")
    if len(orgs) > 1:
        sys.exit("several Claude Science organizations; this script handles one:\n  " + "\n  ".join(orgs))
    return os.path.dirname(orgs[0])


def connect(org):
    db = os.path.join(org, "operon-cli.db")
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.execute("select 1 from projects limit 1")
    except sqlite3.Error:
        con = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)
    con.row_factory = sqlite3.Row
    try:
        con.execute("select id, name from projects limit 1")
        con.execute("select filename, latest_version_id, is_user_upload, is_ephemeral from artifacts limit 1")
        con.execute("select version_number, content_type, size_bytes, storage_path, is_intermediate, created_at from artifact_versions limit 1")
    except sqlite3.Error as e:
        sys.exit(f"the Claude Science database layout changed ({e}); update this script")
    return con


def when(ms):
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc)


def project(con, q):
    rows = con.execute("select id, name from projects where archived_at is null").fetchall()
    hits = [r for r in rows if r["id"] == q] or [r for r in rows if q.lower() in r["name"].lower()]
    if len(hits) != 1:
        sys.exit(f"{q!r} matches {len(hits)} projects: " + ", ".join(f"{r['id']} ({r['name']})" for r in (hits or rows)))
    return hits[0]


def artifacts(con, pid, everything=False):
    sql = """select a.id, a.filename, a.is_user_upload, a.is_ephemeral, v.version_number, v.content_type,
                    v.size_bytes, v.storage_path, v.is_intermediate, v.created_at, v.agent_name
             from artifacts a join artifact_versions v on v.id = a.latest_version_id
             where a.project_id = ? order by v.created_at"""
    rows = con.execute(sql, (pid,)).fetchall()
    if not everything:
        rows = [r for r in rows if not r["is_intermediate"] and not r["is_user_upload"] and not r["is_ephemeral"]]
    return rows


def known_ids(root):
    ids = set()
    for sub in ("raw", "inbox"):
        for dirpath, _, names in os.walk(os.path.join(root, sub)):
            for n in names:
                if n.endswith(".md"):
                    with open(os.path.join(dirpath, n), encoding="utf-8", errors="replace") as f:
                        head = f.read(4000)
                    ids.update(re.findall(r"^science_artifact:\s*(\S+)", head, re.M))
    return ids


def slug(s):
    s = re.sub(r"\.(md|txt|markdown)$", "", s, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def title_of(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return (m.group(1).strip() if m else fallback).replace('"', "'")


def cmd_projects(con, org, args):
    for r in con.execute("""select p.id, p.name, count(a.id) n, max(a.created_at) last
                            from projects p left join artifacts a on a.project_id = p.id
                            where p.archived_at is null group by p.id order by last"""):
        last = when(r["last"]).date() if r["last"] else "-"
        print(f"{r['id']:20} {r['n']:4} artifacts  last {last}  {r['name']}")


def cmd_list(con, org, args):
    p = project(con, args.project)
    known = known_ids(args.wiki) if args.wiki else set()
    rows = artifacts(con, p["id"], args.all)
    print(f"{p['id']} {p['name']}: {len(rows)} artifact(s)" + ("" if args.all else " (final only; --all for every file)"))
    for r in rows:
        flags = "".join(("I" if r["is_intermediate"] else "-", "U" if r["is_user_upload"] else "-",
                         "W" if r["id"] in known else "-"))
        print(f"  {flags} {when(r['created_at']).date()} v{r['version_number']:<2} {r['size_bytes'] // 1024:>6}k  "
              f"{r['content_type']:16} {r['filename']}")
    if args.wiki:
        print("  flags: I intermediate, U user upload, W already in the wiki")


def cmd_copy(con, org, args):
    p = project(con, args.project)
    rows = artifacts(con, p["id"], everything=True)
    os.makedirs(args.to, exist_ok=True)
    wiki_root = os.path.dirname(os.path.abspath(args.to.rstrip("/")))
    known = known_ids(wiki_root)
    for q in args.artifact:
        hits = [r for r in rows if r["filename"] == q] or [r for r in rows if q.lower() in r["filename"].lower()]
        if len(hits) != 1:
            print(f"skip  {q}: matches {len(hits)} artifacts" + (": " + ", ".join(r["filename"] for r in hits[:8]) if hits else ""))
            continue
        r = hits[0]
        if r["content_type"] not in TEXT:
            print(f"skip  {r['filename']}: {r['content_type']} stays in Science (name it in the raw note)")
            continue
        if r["id"] in known and not args.force:
            print(f"skip  {r['filename']}: already in the wiki (science_artifact {r['id']}); --force copies again")
            continue
        src = os.path.join(org, "artifacts", r["storage_path"])
        if not os.path.isfile(src):
            print(f"skip  {r['filename']}: file not found at artifacts/{r['storage_path']}")
            continue
        with open(src, encoding="utf-8", errors="replace") as f:
            text = f.read()
        made = when(r["created_at"])
        dst = os.path.join(args.to, f"{made.date()}-claude-science-{slug(r['filename'])}.md")
        if os.path.exists(dst) and not args.force:
            print(f"skip  {r['filename']}: {dst} exists")
            continue
        fm = "\n".join([
            "---",
            f'title: "{title_of(text, r["filename"])}"',
            f'source: "Claude Science, project {p["name"]}, artifact {r["filename"]} v{r["version_number"]}"',
            "authors: [Claude Science]",
            f"source_date: {made.date()}",
            f"science_project: {p['id']}",
            f"science_artifact: {r['id']}",
            f"science_version: {r['version_number']}",
            "---", "", ""])
        with open(dst, "w", encoding="utf-8") as f:
            f.write(fm + text)
        print(f"ok    {r['filename']} v{r['version_number']} -> {dst}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("projects")
    p = sub.add_parser("list"); p.add_argument("project"); p.add_argument("--all", action="store_true"); p.add_argument("--wiki")
    p = sub.add_parser("copy"); p.add_argument("project"); p.add_argument("artifact", nargs="+")
    p.add_argument("--to", required=True); p.add_argument("--force", action="store_true")
    args = ap.parse_args()
    org = org_dir()
    globals()["cmd_" + args.cmd](connect(org), org, args)


if __name__ == "__main__":
    main()
