"""Roster for the foreman skill: who can be put on a team, and what a run costs.

Usage:
  roster.py [--hub PATH] [--days 90] [--no-costs] [--json]
  roster.py --log-hire ROLE --as KIND --model MODEL [--outcome accepted|returned|rejected] [--cost USD]

Lists, in one short table:
  specialists     HUB/.skills/registry.json (enabled topics) and HUB/.skills/_index.md
                  (version, risk); the hub is found as the department skill finds it:
                  ~/.config/wiki-kit/specialists-hub, else hub_path in ~/.config/llm-wiki/config.json
  agents          Claude Code agents in ~/.claude/agents/*.md and ./.claude/agents/*.md
                  (name, description, model, tools from the frontmatter)
  built-in        Explore, Plan, general-purpose, web-fetch (a fixed list)
  consultants     outside vendors that council.py could call: names only, never keys
                  (a key is present in the environment or council.env; ollama answers locally)
  vacancies       the Vacancies table of the kit's specialists/README.md
  temporary roles the foreman's hire log, ~/.config/wiki-kit/foreman/hires.tsv; a temporary
                  role hired twice or more is flagged as a vacancy candidate
  costs           cost per subagent run, measured from local Claude Code logs by
                  claude_usage.py (median and p90 by agent type and model family);
                  a family with fewer than 3 runs gets a row derived from the Sonnet
                  median by list-price ratio, marked "derived". Estimates, not quotes.

--log-hire appends one line to the hire log (date, role, kind, model, outcome, cost).
Write only a generic role name ("fact-checker"), never a client, person or task detail.
"""
import argparse, datetime, json, os, re, shutil, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # sibling imports under python3 -I

KIT = HERE.parent
HIRES = Path("~/.config/wiki-kit/foreman/hires.tsv").expanduser()
HIRE_COLS = ["date", "role", "kind", "model", "outcome", "cost_usd"]
BUILTIN = [
    ("Explore", "read-only fan-out search over many files; returns locations and conclusions",
     "default", "all except edit/write"),
    ("Plan", "read-only architect: step-by-step implementation plans, trade-offs",
     "default", "all except edit/write"),
    ("general-purpose", "any multi-step task; the usual body for a temporary hire with a written brief",
     "inherit", "all"),
    ("web-fetch", "reads public web pages and answers about them",
     "default", "WebFetch"),
]


def hub_path(arg):
    if arg:
        return Path(arg).expanduser()
    f = Path("~/.config/wiki-kit/specialists-hub").expanduser()
    if f.exists() and f.read_text().strip():
        return Path(f.read_text().strip()).expanduser()
    try:
        cfg = json.loads(Path("~/.config/llm-wiki/config.json").expanduser().read_text())
        return Path(cfg["hub_path"]).expanduser() if cfg.get("hub_path") else None
    except (OSError, ValueError, KeyError):
        return None


def frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            out[k.strip()] = v.strip().strip('"').strip("'")
        elif sep and k.strip() == "version":  # nested metadata.version of a specialist
            out.setdefault("version", v.strip().strip('"'))
    return out


def specialists(hub):
    skills = hub / ".skills" if hub else None
    if not skills or not skills.is_dir():
        return []
    topics = {}
    try:
        for t, names in json.loads((skills / "registry.json").read_text()).get("topics", {}).items():
            for n in names:
                topics.setdefault(n, []).append(t)
    except (OSError, ValueError):
        pass
    rows = {}
    idx = skills / "_index.md"
    if idx.exists():
        for line in idx.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*\[([\w-]+)\]\([^)]*\)\s*\|(.*?)\|\s*([\d.]+)\s*\|\s*(\w+)\s*\|", line)
            if m:
                rows[m.group(1)] = dict(name=m.group(1), version=m.group(3), risk=m.group(4),
                                        job=job(m.group(2)))
    for d in sorted(p for p in skills.iterdir() if (p / "SKILL.md").exists()):
        if d.name not in rows:
            fm = frontmatter(d / "SKILL.md")
            rows[d.name] = dict(name=d.name, version=fm.get("version", "?"), risk=fm.get("risk-tier", "?"),
                                job=job(fm.get("description", "")))
    for r in rows.values():
        r["topics"] = sorted(topics.get(r["name"], []))
    return sorted(rows.values(), key=lambda r: r["name"])


def agents():
    out, seen = [], set()
    for where, d in (("project", Path.cwd() / ".claude" / "agents"), ("user", Path("~/.claude/agents").expanduser())):
        for f in sorted(d.glob("*.md")) if d.is_dir() else []:
            fm = frontmatter(f)
            name = fm.get("name") or f.stem
            if name in seen:  # a project agent shadows a user agent of the same name
                continue
            seen.add(name)
            out.append(dict(name=name, scope=where, model=fm.get("model", "inherit"),
                            tools=fm.get("tools", "all"), job=fm.get("description", "")))
    return out


def consultants():
    try:
        import council
    except Exception as e:  # noqa: BLE001 - any import failure means "not available"
        return dict(error=f"council.py not importable: {str(e)[:80]}")
    council.load_env()
    ready, missing = [], []
    if shutil.which("claude"):
        ready.append("claude (haiku, sonnet, opus via claude -p)")
    for v, (base, env) in council.VENDORS.items():
        if env:
            (ready if os.environ.get(env) else missing).append(v)
            continue
        try:
            urllib.request.urlopen(base.rsplit("/v1", 1)[0] + "/api/tags", timeout=1).close()
            ready.append(f"{v} (local)")
        except Exception:  # noqa: BLE001
            missing.append(f"{v} (not running)")
    return dict(ready=ready, not_configured=missing)


def vacancies():
    text = (KIT / "specialists" / "README.md").read_text(encoding="utf-8")
    sec = text.split("## Vacancies", 1)[-1].split("\n## ", 1)[0]
    return [dict(name=m.group(1), job=m.group(2).strip(), risk=m.group(3).strip())
            for m in re.finditer(r"^\|\s*`([\w-]+)`\s*\|(.*?)\|\s*(\w+)\s*\|", sec, re.M)]


def hires():
    if not HIRES.exists():
        return []
    rows = []
    for line in HIRES.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) == len(HIRE_COLS):
            rows.append(dict(zip(HIRE_COLS, parts)))
    return rows


def temporary_roles(rows):
    counts = {}
    for r in rows:
        if r["kind"] == "temporary":
            counts[r["role"]] = counts.get(r["role"], 0) + 1
    return [dict(role=k, hired=v, vacancy_candidate=v >= 2) for k, v in sorted(counts.items())]


def costs(days):
    try:
        import claude_usage as cu
    except Exception as e:  # noqa: BLE001
        return dict(error=f"claude_usage.py not importable: {str(e)[:80]}")
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    calls, _, _ = cu.load(os.path.expanduser("~/.claude/projects"), None, since)
    stats = cu.agent_stats(calls)
    anyrow = {s["model"]: s for s in stats if s["type"] == "any"}
    son = anyrow.get("sonnet")
    if son and son["runs"] >= 3:
        latest = {f: max((k for k in cu.PRICES if f in k), default=None) for f in ("haiku", "sonnet", "opus")}
        for f in ("haiku", "opus"):
            if anyrow.get(f, {}).get("runs", 0) < 3 and latest[f] and latest["sonnet"]:
                ratio = cu.PRICES[latest[f]][0] / cu.PRICES[latest["sonnet"]][0]
                stats.append(dict(type="any (derived)", model=f, runs=0, median=round(son["median"] * ratio, 2),
                                  p90=round(son["p90"] * ratio, 2), max=None, basis=f"sonnet x {ratio:g} list-price ratio"))
    return dict(since=since, rows=stats)


def job(s):
    """Drop the draft marker: the version column already says it."""
    return re.sub(r"^DRAFT[.,]\s*((needs review|not yet reviewed)[^.]*\.)?\s*", "", (s or "").strip())


def short(s, n):
    s = re.sub(r"\s+", " ", s or "")
    return s if len(s) <= n else s[: n - 1] + "…"


def show(r):
    hub = r["hub"] or "(none found)"
    print(f"Roster {r['date']} — hub {hub}")
    print(f"\nSpecialists ({len(r['specialists'])})  [method packages; run as a subagent that reads HUB/.skills/<name>/SKILL.md]")
    for s in r["specialists"]:
        draft = " draft" if s["version"].startswith("0.") else ""
        print(f"  {s['name']:31s} {s['version']:6s}{draft:6s} {s['risk']:6s} {','.join(s['topics']) or '-':10s} {short(s['job'], 48)}")
    print(f"\nAgents ({len(r['agents'])})")
    for a in r["agents"]:
        print(f"  {a['name']:31s} {a['model']:8s} {a['scope']:7s} tools: {short(a['tools'], 24):24s} {short(a['job'], 40)}")
    print("\nBuilt-in agents  [model set per call; 'default' = Claude Code's choice]")
    for b in r["builtin"]:
        print(f"  {b['name']:31s} {b['model']:8s} {short(b['job'], 70)}")
    c = r["consultants"]
    print("\nOutside consultants (council.py)")
    if "error" in c:
        print(f"  {c['error']}")
    else:
        print(f"  ready: {', '.join(c['ready']) or 'none'}")
        print(f"  not configured: {', '.join(c['not_configured']) or 'none'}")
    print("\nVacancies (kit specialists/README.md)")
    for v in r["vacancies"] or [{"name": "none", "risk": "", "job": ""}]:
        print(f"  {v['name']:31s} {v['risk']:6s} {short(v['job'], 60)}")
    print(f"\nTemporary roles (hire log, {len(r['hires'])} hires)")
    for t in r["temporary_roles"] or [{"role": "none yet", "hired": 0, "vacancy_candidate": False}]:
        flag = "  -> propose a vacancy or a draft specialist" if t["vacancy_candidate"] else ""
        print(f"  {t['role']:31s} x{t['hired']}{flag}")
    k = r.get("costs")
    if k is None:
        return
    if "error" in k:
        print(f"\nCosts: {k['error']}")
        return
    print(f"\nCost per subagent run since {k['since']} (USD at list prices; ESTIMATES from logs, not quotes)")
    print(f"  {'type':24s} {'model':7s} {'runs':>5s} {'median':>7s} {'p90':>7s}")
    for s in k["rows"]:
        extra = f"  ({s['basis']})" if s.get("basis") else ""
        print(f"  {s['type'][:24]:24s} {s['model']:7s} {s['runs']:5d} {s['median']:7.2f} {s['p90']:7.2f}{extra}")


def log_hire(a):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", a.log_hire):
        sys.exit("role: a short generic name in lowercase with hyphens, e.g. fact-checker")
    HIRES.parent.mkdir(parents=True, exist_ok=True)
    new = not HIRES.exists()
    with HIRES.open("a", encoding="utf-8") as f:
        if new:
            f.write("\t".join(HIRE_COLS) + "\n")
        f.write("\t".join([datetime.date.today().isoformat(), a.log_hire, a.kind, a.model, a.outcome,
                           "" if a.cost is None else f"{a.cost:.2f}"]) + "\n")
    print(f"logged {a.log_hire} ({a.kind}, {a.model}, {a.outcome}) in {HIRES}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hub", help="hub folder (default: as the department skill finds it)")
    ap.add_argument("--days", type=int, default=90, help="cost window in days (default 90)")
    ap.add_argument("--no-costs", action="store_true", help="skip reading the Claude Code logs")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--log-hire", metavar="ROLE", help="append a hire to the log and exit")
    ap.add_argument("--as", dest="kind", choices=["specialist", "agent", "builtin", "consultant", "temporary"])
    ap.add_argument("--model", help="haiku | sonnet | opus | vendor:model")
    ap.add_argument("--outcome", default="accepted", choices=["accepted", "returned", "rejected"])
    ap.add_argument("--cost", type=float, help="measured USD for this run")
    a = ap.parse_args()
    if a.log_hire:
        if not (a.kind and a.model):
            ap.error("--log-hire needs --as and --model")
        return log_hire(a)
    hub = hub_path(a.hub)
    h = hires()
    r = dict(date=datetime.date.today().isoformat(), hub=str(hub) if hub else None,
             specialists=specialists(hub), agents=agents(),
             builtin=[dict(name=n, job=j, model=m, tools=t) for n, j, m, t in BUILTIN],
             consultants=consultants(), vacancies=vacancies(), hires=h, temporary_roles=temporary_roles(h),
             costs=None if a.no_costs else costs(a.days))
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        show(r)


if __name__ == "__main__":
    main()
