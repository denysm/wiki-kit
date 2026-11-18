"""Convert a Jira Cloud CSV export into verbatim Markdown raw sources, grouped by epic.

Usage: jiracsv2md.py CSV ROOT --project KEY --site https://<instance>.atlassian.net
       [--date YYYY-MM-DD] [--board URL] [--label TEXT] [--tags t1,t2] [--tag-rule REGEX=tag ...]

Writes ROOT/raw/articles/<date>-jira-<proj>-<epickey>-<slug>.local.md per epic (epic plus every
descendant via Parent key chains), <date>-jira-<proj>-unparented-<component>.local.md for issues
without an epic ancestor, and <date>-jira-<proj>-index.local.md. No summarizing: fields and
text are copied verbatim; only real credentials become [REDACTED:secret] (count is printed).
Repeated CSV columns are read by index. Deterministic; stdlib only.
"""
import argparse, csv, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime

# Credential patterns come from raw_check.py next to this script, so the export and the
# checker agree.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling import under python3 -I
from raw_check import INTERNAL_KINDS, MARK, SECRET_PATTERNS, URL_RE  # noqa: E402

# A verbatim .local.md export keeps infrastructure ids (buckets, ARNs, instance ids):
# only real credentials are redacted.
CREDENTIALS = [(k, rx, g) for k, rx, g in SECRET_PATTERNS if k not in INTERNAL_KINDS]
# Placeholders and variable references are not credentials ($VAR, ${VAR}, ***, xxx, <token>).
PLACEHOLDER = re.compile(r"(?i)^(?:[$<{%]|\*{3}|x{3}|your|example|placeholder|none|null|true|false|changeme)")
URL_PASSWORD = re.compile(r"^([a-z][a-z0-9+.-]*://[^\s:/@]+:)([^\s@/]+)(@)", re.I)

csv.field_size_limit(10**9)
REDACTIONS = 0


def redact(t):
    global REDACTIONS
    if not t:
        return t

    def sub_url(m):
        global REDACTIONS
        u = URL_PASSWORD.match(m.group(0))
        if not u or u.group(2).startswith(("[REDACTED", "$", "<", "{", "***")):
            return m.group(0)
        REDACTIONS += 1
        return u.group(1) + MARK + m.group(0)[u.end(2):]

    t = URL_RE.sub(sub_url, t)
    for _kind, rx, grp in CREDENTIALS:
        def sub(m, grp=grp):
            global REDACTIONS
            if grp and PLACEHOLDER.match(m.group(grp)):
                return m.group(0)
            REDACTIONS += 1
            if grp == 0:
                return MARK
            s, e = m.span(grp)
            return m.group(0)[: s - m.start()] + MARK + m.group(0)[e - m.start():]
        t = rx.sub(sub, t)
    return t


def iso(v):
    v = (v or "").strip()
    if not v:
        return None
    for f in ("%d/%b/%y %I:%M %p", "%d/%b/%y"):
        try:
            return datetime.strptime(v, f).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def dt(v):
    v = (v or "").strip()
    if not v:
        return "—"
    i = iso(v)
    return f"{i} ({v})" if i else v


def slug(s, n=50):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].strip("-") or "x"


def ys(s):
    return json.dumps(s or "", ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("root")
    ap.add_argument("--project", required=True, help="Jira project key")
    ap.add_argument("--date", default=datetime.now().date().isoformat(), help="ingest/export date")
    ap.add_argument("--site", required=True, help="Jira site URL, https://<instance>.atlassian.net")
    ap.add_argument("--board", help="board URL for the index and unparented files (default: project page)")
    ap.add_argument("--label", help="source label (default: jira:<instance>/<KEY> (CSV export <date>))")
    ap.add_argument("--tags", default="", help="comma-separated tags added to every file")
    ap.add_argument("--tag-rule", action="append", default=[], metavar="REGEX=tag",
                    help="add tag when REGEX matches a component name of the group (repeatable)")
    a = ap.parse_args()
    a.site = a.site.rstrip("/")
    inst = re.sub(r"\.atlassian\.net$", "", re.sub(r"^https?://", "", a.site))
    a.board = a.board or f"{a.site}/jira/software/projects/{a.project}"
    a.label = a.label or f"jira:{inst}/{a.project} (CSV export {a.date})"
    base_tags = [inst, "jira", a.project.lower()] + [t.strip() for t in a.tags.split(",") if t.strip()]
    rules = [tuple(r.rsplit("=", 1)) for r in a.tag_rule]
    out = os.path.join(a.root, "raw", "articles")
    os.makedirs(out, exist_ok=True)
    rows = list(csv.reader(open(a.csv, encoding="utf-8-sig", newline="")))
    H, data = rows[0], rows[1:]
    ix = defaultdict(list)
    for i, h in enumerate(H):
        ix[h].append(i)

    def one(r, name):
        for i in ix.get(name, []):
            if r[i].strip():
                return r[i].strip()
        return ""

    def many(r, name):
        return [r[i].strip() for i in ix.get(name, []) if r[i].strip()]

    P = a.project.lower()
    issues = {}
    for r in data:
        r = r + [""] * (len(H) - len(r))
        k = one(r, "Issue key")
        issues[k] = dict(r=r, key=k, type=one(r, "Issue Type"), parent=one(r, "Parent key"),
                         comps=many(r, "Components"), created=iso(one(r, "Created")),
                         updated=iso(one(r, "Updated")), sprints=many(r, "Sprint"),
                         status=one(r, "Status"), summary=one(r, "Summary"))
    num = lambda k: int(k.rsplit("-", 1)[1])
    orphans, cycles = [], []

    def root_of(k):
        seen = set(); cur = k
        while True:
            i = issues[cur]
            if i["type"] == "Epic":
                return cur, True
            p = i["parent"]
            if not p or p in seen:
                return cur, False
            if p not in issues:
                orphans.append((k, p)); return cur, False
            seen.add(cur); cur = p

    groups = defaultdict(list); epic_of = {}
    for k in issues:
        rt, is_epic = root_of(k)
        if is_epic:
            groups[("epic", rt)].append(k)
        else:
            c = issues[rt]["comps"]
            groups[("unp", slug(c[0]) if c else "no-component")].append(k)
    # sprint order: by earliest created of issues having it
    sp_first = {}
    for i in issues.values():
        for s in i["sprints"]:
            if i["created"] and (s not in sp_first or i["created"] < sp_first[s]):
                sp_first[s] = i["created"]
    sp_order = sorted(sp_first, key=lambda s: (sp_first[s], s))

    def issue_md(i):
        r = i["r"]; k = i["key"]
        def f(n, v): return f"- **{n}:** {v or '—'}"
        L = [f"### {k} — {redact(i['summary'])}", ""]
        L += [f("Type", i["type"]), f("Status", i["status"]), f("Priority", one(r, "Priority")),
              f("Resolution", one(r, "Resolution")), f("Assignee", one(r, "Assignee")),
              f("Reporter", one(r, "Reporter")), f("Created", dt(one(r, "Created"))),
              f("Updated", dt(one(r, "Updated"))), f("Resolved", dt(one(r, "Resolved"))),
              f("Due", dt(one(r, "Due date"))), f("Sprint(s)", "; ".join(i["sprints"])),
              f("Components", ", ".join(i["comps"])), f("Labels", ", ".join(many(r, "Labels"))),
              f("Parent", (i["parent"] + " " + one(r, "Parent summary")).strip()),
              f("Fix versions", ", ".join(many(r, "Fix versions")))]
        for n in ("Custom field (Story Points)", "Custom field (Story point estimate)", "Original estimate",
                  "Remaining Estimate", "Time Spent", "Custom field (Start date)", "Team Name"):
            v = one(r, n)
            if v:
                L.append(f("Start date" if "Start" in n else n.replace("Custom field (", "").rstrip(")"),
                           dt(v) if "Start" in n else v))
        if i["type"] == "Epic":
            for n in ("Custom field (Epic Name)", "Custom field (Epic Status)"):
                v = one(r, n)
                if v: L.append(f(n[14:-1], v))
        links = []
        for h, idxs in ix.items():
            m = re.match(r"(Inward|Outward) issue link \((.*)\)", h)
            if m:
                for j in idxs:
                    if r[j].strip():
                        links.append(f"{m.group(2)} ({m.group(1).lower()}) {r[j].strip()}")
        L.append("- **Issue links:** " + ("; ".join(links) if links else "—"))
        att = []
        for v in many(r, "Attachment"):
            p = v.split(";", 2)
            if len(p) == 3 and ";" in p[2]:
                nm, _ = p[2].rsplit(";", 1)
                att.append(f"{nm} ({dt(p[0])}, {p[1]})")
            else:
                att.append(v)
        L.append("- **Attachments:** " + ("; ".join(att) if att else "—"))
        for n, lbl in (("Custom field (Identifiant)", "Identifiant"), ("Custom field (Domain)", "Domain"),
                       ("Custom field (Type)", "Requirement type"), ("Custom field (Source)", "Source"),
                       ("Custom field (Justification)", "Justification"),
                       ("Custom field (Control measure)", "Control measure"),
                       ("Custom field (DoD (Definition of Done))", "Definition of Done")):
            v = one(r, n)
            if v:
                L += ["", f"{lbl}:", "", redact(v)]
        d = one(r, "Description")
        L += ["", "Description:", "", redact(d) if d else "—", ""]
        cs = many(r, "Comment")
        if cs:
            L += ["Comments:", ""]
            for c in cs:
                m = re.match(r"^(\d\d/\w{3}/\d\d \d+:\d\d [AP]M);([^;]*);(.*)$", c, re.S)
                if m:
                    t = redact(m.group(3)).replace("\n", "\n  ")
                    L.append(f"- {dt(m.group(1))} {m.group(2)}: {t}")
                else:
                    L.append("- " + redact(c).replace("\n", "\n  "))
            L.append("")
        return L

    def mix(keys, fld):
        c = Counter(issues[k][fld] for k in keys)
        return ", ".join(f"{n} {v}" for n, v in c.most_common())

    written = []; idx_epics = []; idx_unp = []
    for (kind, g), keys in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1] if x[0][0] == "unp" else num(x[0][1]))):
        if kind == "epic":
            keys.sort(key=lambda k: (k != g, num(k)))
        else:
            keys.sort(key=num)
        mem = [issues[k] for k in keys]
        latest = max((m["updated"] for m in mem if m["updated"]), default="unknown")
        comps = Counter(c for m in mem for c in m["comps"])
        tags = list(base_tags)
        cj = " ".join(comps)
        for rx, tg in rules:
            if re.search(rx, cj) and tg not in tags:
                tags.append(tg)
        sps = sorted({s for m in mem for s in m["sprints"]}, key=sp_order.index)
        types = Counter(m["type"] for m in mem)
        if kind == "epic":
            e = issues[g]
            title = f"Jira {g}: {redact(e['summary'])}"
            url = f"{a.site}/browse/{g}"
            fn = f"{a.date}-jira-{P}-{g.lower()}-{slug(e['summary'])}.local.md"
            rep = one(e["r"], "Reporter") or "unknown"
            summ = (f"Epic {g} \"{e['summary']}\" (status {e['status']}) with {len(keys) - 1} descendant issues "
                    f"({', '.join(f'{v} {n}' for n, v in types.most_common() if n != 'Epic')}); status mix: {mix(keys, 'status')}.")
            idx_epics.append((g, e, len(keys) - 1, sps, comps))
        else:
            title = f"Jira {a.project} unparented issues: {g}"
            url = a.board
            fn = f"{a.date}-jira-{P}-unparented-{g}.local.md"
            rep = "unknown"
            summ = (f"{len(keys)} {a.project} issues without an epic ancestor, component group {g} "
                    f"({', '.join(f'{v} {n}' for n, v in types.most_common())}); status mix: {mix(keys, 'status')}.")
            idx_unp.append((g, keys, comps, sps))
        fm = ["---", f"title: {ys(title)}", f"source: {ys(a.label)}", f"url: {ys(url)}", "type: articles",
              f"ingested: {a.date}", f"tags: [{', '.join(tags)}]", f"summary: {ys(redact(summ))}",
              f"authors: [{rep}]", f"source_date: {latest}", f"issue_keys: {len(keys)}",
              "sensitivity: confidential", "---", "", f"# {title}", ""]
        body = [l for m in mem for l in issue_md(m)]
        open(os.path.join(out, fn), "w", encoding="utf-8").write("\n".join(fm + body))
        written.append(fn)

    # index
    allk = list(issues)
    cr = sorted(i["created"] for i in issues.values() if i["created"])
    I = ["---", f"title: {ys('Jira ' + a.project + ' index: epics and unparented groups')}", f"source: {ys(a.label)}",
         f"url: {ys(a.board)}", "type: articles", f"ingested: {a.date}", "tags: [" + ", ".join(dict.fromkeys(base_tags + [tg for _, tg in rules])) + "]",
         f"summary: {ys(f'Index of {len(allk)} {a.project} issues in {len(idx_epics)} epics and {len(idx_unp)} unparented groups, created {cr[0]} to {cr[-1]}.')}",
         "authors: [unknown]", f"source_date: {max(i['updated'] for i in issues.values() if i['updated'])}",
         f"issue_keys: {len(allk)}", "sensitivity: confidential", "---", "", f"# Jira {a.project} index", "",
         "## Epics", "", "| Key | Summary | Status | Component | Children | Created | Sprints |", "|---|---|---|---|---|---|---|"]
    for g, e, n, sps, comps in idx_epics:
        sp = f"{sps[0]} … {sps[-1]}" if len(sps) > 1 else (sps[0] if sps else "—")
        cm = ", ".join(e["comps"]) or ", ".join(c for c, _ in comps.most_common(2)) or "—"
        I.append(f"| {g} | {e['summary'].replace('|', '/')} | {e['status']} | {cm} | {n} | {e['created']} | {sp} |")
    I += ["", "## Unparented groups", "", "| Group | Issues | Types | Sprints |", "|---|---|---|---|"]
    for g, keys, comps, sps in idx_unp:
        I.append(f"| {g} | {len(keys)} | {mix(keys, 'type')} | {', '.join(sps) or '—'} |")
    I += ["", "## Counts", "", "By type: " + mix(allk, "type"), "", "By status: " + mix(allk, "status"), "",
          "By sprint (issues listed in the sprint): " + ", ".join(f"{s} {sum(1 for i in issues.values() if s in i['sprints'])}" for s in sp_order), ""]
    open(os.path.join(out, f"{a.date}-jira-{P}-index.local.md"), "w", encoding="utf-8").write("\n".join(I))
    written.append("index")
    print(f"files: {len(written)} (epics {len(idx_epics)}, unparented {len(idx_unp)}); issues {len(allk)}; "
          f"created {cr[0]}..{cr[-1]}; redactions {REDACTIONS}; orphans {len(orphans)}")
    for k, p in orphans[:10]:
        print("orphan", k, "missing parent", p)
    nums = sorted(num(k) for k in issues)
    print("key range", nums[0], nums[-1])
    for g, e, n, _, _ in sorted(idx_epics, key=lambda x: -x[2])[:15]:
        print(g, n, e["status"], "|", e["summary"][:60], "|", ",".join(e["comps"]))
    for g, keys, _, _ in idx_unp:
        print("unparented", g, len(keys))


if __name__ == "__main__":
    main()
