"""Claude Science results -> a wiki inbox, without a model.

Usage:
  science2inbox.py projects
  science2inbox.py list PROJECT [--all] [--wiki ROOT]
  science2inbox.py copy PROJECT ARTIFACT... --to INBOX [--data] [--force]

Claude Science (the desktop app) keeps each organization's state in
~/.claude-science/orgs/<org>/: a SQLite database (operon-cli.db) with projects,
artifacts and their versions, and the files under artifacts/<project>/. This
script reads both and never writes there: copy, never move, out of an
application folder.

PROJECT is a project id (proj_…) or a unique part of its name. ARTIFACT is a
file name as Science shows it (bpprc_verification_report.md) or a unique part
of it. `list` shows final artifacts (Science's agent output, not intermediate
files) with their latest version; --all adds intermediate files and uploads.
With --wiki it marks artifacts that already reached that wiki: W when a raw or
inbox file's frontmatter has `science_artifact: <id>`, w when its frontmatter
names the artifact's file (a copy that came another way, for example exported
to OneDrive and ingested from there).

`copy` writes the latest version of each artifact as
INBOX/<date>-claude-science-<name>.md with frontmatter (title, source,
authors: [Claude Science], source_date, science_project, science_artifact,
science_version) for /wiki:ingest. It skips W and w artifacts unless --force.
Text artifacts (Markdown, plain text) are copied as they are. Data files stay
in Science unless --data is given: then CSV, TSV and JSON files up to 1 MB are
copied verbatim inside a fenced block. Other files (figures, archives, Office
documents) always stay in Science; the report names them so the raw note can
point to them. Each copied file ends with a "Claude Science reviewer checks"
section: the warn and fail verdicts Science's reviewer recorded for exactly
that version (table verification_checks: claim, verdict, severity, status,
evidence), so the ingest sees what Science itself doubted. Pass and
inconclusive verdicts are only counted. The layout of ~/.claude-science is the app's own and may change
between versions; the script stops with a message if it does.
"""
import argparse, datetime, glob, os, re, sqlite3, sys

HOME = os.path.expanduser("~/.claude-science")
TEXT = ("text/markdown", "text/plain")
DATA = {"text/csv": "csv", "text/tab-separated-values": "tsv", "application/json": "json"}
DATA_MAX = 1_000_000


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
    sql = """select a.id, a.filename, a.is_user_upload, a.is_ephemeral, v.id version_id, v.version_number, v.content_type,
                    v.size_bytes, v.storage_path, v.is_intermediate, v.created_at, v.agent_name
             from artifacts a join artifact_versions v on v.id = a.latest_version_id
             where a.project_id = ? order by v.created_at"""
    rows = con.execute(sql, (pid,)).fetchall()
    if not everything:
        rows = [r for r in rows if not r["is_intermediate"] and not r["is_user_upload"] and not r["is_ephemeral"]]
    return rows


def wiki_state(root):
    """Science ids found in raw/ and inbox/ frontmatter, and each file's frontmatter for name matches."""
    ids, heads = set(), []
    for sub in ("raw", "inbox"):
        for dirpath, _, names in os.walk(os.path.join(root, sub)):
            for n in names:
                if n.endswith(".md"):
                    path = os.path.join(dirpath, n)
                    with open(path, encoding="utf-8", errors="replace") as f:
                        head = f.read(4000)
                    m = re.match(r"---\n(.*?)\n---", head, re.S)
                    fm = m.group(1) if m else head
                    ids.update(re.findall(r"^science_artifact:\s*(\S+)", fm, re.M))
                    heads.append((os.path.relpath(path, root), fm))
    return ids, heads


def named_in(filename, heads):
    """The first wiki file whose frontmatter names this artifact's file, or None."""
    pat = re.compile(r"(?<![\w.-])" + re.escape(filename) + r"(?![\w.-])")
    return next((path for path, fm in heads if pat.search(fm)), None)


def slug(s):
    s = re.sub(r"\.(md|txt|markdown|csv|tsv|json)$", "", s, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def title_of(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return (m.group(1).strip() if m else fallback).replace('"', "'")


def cell(s):
    return " ".join((s or "").split()).replace("|", "\\|") or "-"


def review_section(con, version_id, version_number):
    """Markdown section with Science's warn/fail reviewer checks for one artifact version."""
    try:
        rows = con.execute("""select verdict, severity, status, claim, evidence from verification_checks
                              where artifact_version_id = ? order by created_at""", (version_id,)).fetchall()
    except sqlite3.Error as e:
        return f"\n\n## Claude Science reviewer checks (v{version_number})\n\nNot read: {e}.\n"
    flagged = [r for r in rows if r["verdict"] in ("warn", "fail")]
    flagged.sort(key=lambda r: (r["verdict"] != "fail", {"high": 0, "medium": 1, "low": 2}.get(r["severity"], 3)))
    out = [f"\n\n## Claude Science reviewer checks (v{version_number})\n"]
    if not rows:
        out.append("No reviewer checks recorded for this version.")
        return "\n".join(out) + "\n"
    rest = len(rows) - len(flagged)
    out.append(f"Science's reviewer recorded {len(rows)} check(s) for this version: "
               f"{sum(r['verdict'] == 'fail' for r in rows)} fail, {sum(r['verdict'] == 'warn' for r in rows)} warn, "
               f"{rest} pass or inconclusive (not listed).")
    if flagged:
        out[-1] += (" Status is Science's own: resolved means the issue was addressed in the session, "
                    "not necessarily in this text.")
        out += ["", "| Verdict | Severity | Status | Claim | Evidence |", "|---|---|---|---|---|"]
        out += [f"| {r['verdict']} | {cell(r['severity'])} | {cell(r['status'])} | {cell(r['claim'])} | {cell(r['evidence'])} |"
                for r in flagged]
    return "\n".join(out) + "\n"


def cmd_projects(con, org, args):
    for r in con.execute("""select p.id, p.name, count(a.id) n, max(a.created_at) last
                            from projects p left join artifacts a on a.project_id = p.id
                            where p.archived_at is null group by p.id order by last"""):
        last = when(r["last"]).date() if r["last"] else "-"
        print(f"{r['id']:20} {r['n']:4} artifacts  last {last}  {r['name']}")


def cmd_list(con, org, args):
    p = project(con, args.project)
    known, heads = wiki_state(args.wiki) if args.wiki else (set(), [])
    rows = artifacts(con, p["id"], args.all)
    print(f"{p['id']} {p['name']}: {len(rows)} artifact(s)" + ("" if args.all else " (final only; --all for every file)"))
    for r in rows:
        seen = "W" if r["id"] in known else ("w" if heads and named_in(r["filename"], heads) else "-")
        flags = "".join(("I" if r["is_intermediate"] else "-", "U" if r["is_user_upload"] else "-", seen))
        print(f"  {flags} {when(r['created_at']).date()} v{r['version_number']:<2} {r['size_bytes'] // 1024:>6}k  "
              f"{r['content_type']:16} {r['filename']}")
    if args.wiki:
        print("  flags: I intermediate, U user upload, W already in the wiki, w its file name is in a wiki file's frontmatter")


def cmd_copy(con, org, args):
    p = project(con, args.project)
    rows = artifacts(con, p["id"], everything=True)
    os.makedirs(args.to, exist_ok=True)
    wiki_root = os.path.dirname(os.path.abspath(args.to.rstrip("/")))
    known, heads = wiki_state(wiki_root)
    for q in args.artifact:
        hits = [r for r in rows if r["filename"] == q] or [r for r in rows if q.lower() in r["filename"].lower()]
        if len(hits) != 1:
            print(f"skip  {q}: matches {len(hits)} artifacts" + (": " + ", ".join(r["filename"] for r in hits[:8]) if hits else ""))
            continue
        r = hits[0]
        kind = DATA.get(r["content_type"])
        if r["content_type"] not in TEXT and not (kind and args.data):
            print(f"skip  {r['filename']}: {r['content_type']} stays in Science"
                  + (" (--data copies it)" if kind else " (name it in the raw note)"))
            continue
        if kind and r["size_bytes"] > DATA_MAX:
            print(f"skip  {r['filename']}: {r['size_bytes'] // 1024}k is over the {DATA_MAX // 1000}k limit for --data")
            continue
        if r["id"] in known and not args.force:
            print(f"skip  {r['filename']}: already in the wiki (science_artifact {r['id']}); --force copies again")
            continue
        other = named_in(r["filename"], heads)
        if other and not args.force:
            print(f"skip  {r['filename']}: probably already in the wiki as {other} (its frontmatter names this file); --force copies anyway")
            continue
        src = os.path.join(org, "artifacts", r["storage_path"])
        if not os.path.isfile(src):
            print(f"skip  {r['filename']}: file not found at artifacts/{r['storage_path']}")
            continue
        with open(src, encoding="utf-8", errors="replace") as f:
            text = f.read()
        if kind:
            text = f"# {r['filename']}\n\nData file from Claude Science, copied verbatim.\n\n```{kind}\n{text.rstrip()}\n```\n"
        text = text.rstrip() + "\n" + review_section(con, r["version_id"], r["version_number"])
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
    p.add_argument("--to", required=True); p.add_argument("--data", action="store_true")
    p.add_argument("--force", action="store_true")
    args = ap.parse_args()
    org = org_dir()
    globals()["cmd_" + args.cmd](connect(org), org, args)


if __name__ == "__main__":
    main()
