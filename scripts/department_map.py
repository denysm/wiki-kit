#!/usr/bin/env python3
"""Map of the specialist department: a tree of divisions with a graph of handoffs.

The front desk (`skills/department`) reads this one level at a time instead of
every specialist's description, so the department can grow without limit.

  department_map.py [--hub HUB]                 top level: divisions with what they cover
  department_map.py [--hub HUB] --node PATH     one node: its subdivisions and specialists
                                                (job, version, risk, triggers, handoffs, topics);
                                                PATH may also be a specialist name
  department_map.py --check [--hub HUB]         check the tree; exit 1 on errors

Nodes: the table in the kit's `specialists/divisions.md`, plus personal ones in
`~/.config/wiki-kit/divisions.local.md` (same columns; read with a hub only, and
kept out of `.skills/`, where the llm-wiki validator refuses unknown files). Leaves: every package that has
`metadata.division: "<path>"` in its SKILL.md frontmatter. Edges: specialist
names in backticks under the package's "Do not use when" heading.

Without --hub, the map reads the configured hub (`~/.config/wiki-kit/specialists-hub`,
else hub_path in `~/.config/llm-wiki/config.json`), so it also shows personal
specialists that are not in the kit; with no hub it reads the kit. --check
without --hub checks the kit (as CI does): every package has a known division,
every subdivision has its parent, no handoff names a missing specialist, no node
has more than 12 children, the Staff table of `specialists/README.md` matches the
packages, and the front desk's description names no specialist.

Stdlib only; Python 3.9+.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
sys.path.insert(0, str(HERE))
from skill_check import NAME_RE, parse_frontmatter  # noqa: E402
from roster import hub_path  # noqa: E402

MAX_CHILDREN = 12
DIVISIONS = KIT / "specialists" / "divisions.md"
STAFF = KIT / "specialists" / "README.md"
DESK = KIT / "skills" / "department" / "SKILL.md"
LOCAL_DIVISIONS = Path("~/.config/wiki-kit/divisions.local.md").expanduser()
PATH_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*(/[a-z0-9]+(-[a-z0-9]+)*)*$")
TICK_RE = re.compile(r"`([^`\s]+)`")
HANDOFF_HEAD = re.compile(r"^(#+)\s+Do not use when\s*$", re.IGNORECASE)


def table_rows(text, first_col):
    """Rows of the first Markdown table whose header starts with `first_col`, as dicts."""
    rows, header = [], None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            if header and rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if cells and cells[0].lower() == first_col:
                header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def read_divisions(hub):
    """{path: {title, covers, triggers, source}} from the kit table and the hub's local table."""
    nodes, errors = {}, []
    sources = [(DIVISIONS, "kit")]
    if hub:
        sources.append((LOCAL_DIVISIONS, "local"))
    for f, src in sources:
        if not f.exists():
            if src == "kit":
                errors.append(f"{f} is missing")
            continue
        for r in table_rows(f.read_text(encoding="utf-8"), "path"):
            p = r.get("path", "").strip("`")
            if not PATH_RE.match(p):
                errors.append(f"{f.name}: bad division path {p!r}")
                continue
            if p in nodes:
                errors.append(f"{f.name}: division {p} is defined twice")
                continue
            nodes[p] = dict(title=r.get("title", p), covers=r.get("covers", ""),
                            triggers=r.get("triggers", ""), source=src)
    return nodes, errors


def handoffs(lines, own):
    """Backticked names under the 'Do not use when' heading, except the package's own."""
    out, level = [], None
    for line in lines:
        m = re.match(r"^(#+)\s", line)
        if level is None:
            h = HANDOFF_HEAD.match(line)
            if h:
                level = len(h.group(1))
            continue
        if m and len(m.group(1)) <= level:
            break
        for t in TICK_RE.findall(line):
            if NAME_RE.match(t) and t != own and t not in out:
                out.append(t)
    return out


def split_description(desc):
    """(job, triggers) from a description: drops a leading 'DRAFT...' sentence."""
    m = re.search(r"\b(Triggers?\b|Use when\b)", desc)
    job, trig = (desc[:m.start()], desc[m.start():]) if m else (desc, "")
    job = re.sub(r"^DRAFT[^.]*\.\s*", "", job.strip())
    return job.strip(), trig.strip()


def read_packages(root):
    pkgs = {}
    for f in sorted(root.glob("*/SKILL.md")):
        lines = f.read_text(encoding="utf-8").splitlines()
        fields, err = parse_frontmatter(lines)
        fields = fields or {}
        job, trig = split_description(fields.get("description", ("", False))[0])
        pkgs[f.parent.name] = dict(
            name=f.parent.name, file=f, error=err,
            division=fields.get("metadata.division", ("", False))[0].strip().strip("/"),
            version=fields.get("metadata.version", ("?", False))[0],
            risk=fields.get("metadata.risk-tier", ("?", False))[0],
            job=job, triggers=trig, out=handoffs(lines, f.parent.name))
    return pkgs


def read_topics(hub):
    topics = {}
    try:
        reg = json.loads((hub / ".skills" / "registry.json").read_text(encoding="utf-8"))
        for t, names in reg.get("topics", {}).items():
            for n in names:
                topics.setdefault(n, []).append(t)
    except (OSError, ValueError, AttributeError, TypeError):
        pass
    return topics


def parent(path):
    return path.rsplit("/", 1)[0] if "/" in path else ""


def placed(division, nodes):
    """True when the division and every ancestor of it are nodes, so the tree reaches it."""
    while division:
        if division not in nodes:
            return False
        division = parent(division)
    return True


def orphans(nodes):
    """Errors for subdivisions whose parent row is missing."""
    return [f"division {p} ({'divisions.local.md' if nodes[p]['source'] == 'local' else 'divisions.md'}) "
            f"has no parent row {parent(p)}" for p in nodes if parent(p) and parent(p) not in nodes]


def children(node, nodes, pkgs):
    subs = [p for p in nodes if parent(p) == node]
    specs = sorted(n for n, p in pkgs.items() if p["division"] == node and node)
    return subs, specs


def count_under(node, pkgs):
    return sum(1 for p in pkgs.values() if p["division"] == node or p["division"].startswith(node + "/"))


def short(text, limit=220):
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def show_top(nodes, pkgs, where):
    tops = [p for p in nodes if "/" not in p]
    print(f"Department ({where}): {plural(len(pkgs), 'specialist')} in {plural(len(tops), 'division')}")
    for p in tops:
        n = nodes[p]
        subs = [f"{s} ({nodes[s]['title']})" for s in nodes if s.startswith(p + "/")]
        extra = f", subdivisions: {', '.join(subs)}" if subs else ""
        print(f"\n{p}  {n['title']}  [{plural(count_under(p, pkgs), 'specialist')}{extra}]")
        print(f"  covers: {n['covers']}")
        if n["triggers"]:
            print(f"  triggers: {n['triggers']}")
    loose = sorted(n for n, p in pkgs.items() if not placed(p["division"], nodes))
    if loose:
        print("\nnot placed in a division (read their descriptions):")
        for n in loose:
            p = pkgs[n]
            print(f"  {n} {p['version']}: {short(p['job'])}"
                  + (f"  (division {p['division']} is not reachable in the tree)" if p["division"] else ""))
    print("\nNext: --node <path> for one division.")


def show_specialist(name, pkgs, topics, indent="  "):
    p = pkgs[name]
    draft = " draft" if p["version"].startswith("0.") else ""
    tps = ", ".join(sorted(topics.get(name, []))) or "not enabled for a topic"
    print(f"{indent}{name}  {p['version']}{draft}, risk {p['risk']}, topics: {tps}")
    print(f"{indent}  job: {short(p['job'])}")
    if p["triggers"]:
        print(f"{indent}  {p['triggers']}")
    if p["out"]:
        print(f"{indent}  hands over to: {', '.join(p['out'])}")


def show_node(node, nodes, pkgs, topics):
    if node in pkgs and node not in nodes:
        p = pkgs[node]
        print(f"specialist in {p['division'] or '(no division)'}")
        show_specialist(node, pkgs, topics, indent="")
        incoming = sorted(n for n, q in pkgs.items() if node in q["out"])
        if incoming:
            print(f"  receives from: {', '.join(incoming)}")
        print(f"  method: {p['file']}")
        return 0
    if node not in nodes:
        print(f"no division or specialist {node!r}; divisions: {', '.join(sorted(nodes))}", file=sys.stderr)
        return 2
    n = nodes[node]
    print(f"{node}  {n['title']}: {n['covers']}")
    subs, specs = children(node, nodes, pkgs)
    if subs:
        print("\nsubdivisions:")
        for s in subs:
            print(f"  {s}  {nodes[s]['title']}  [{plural(count_under(s, pkgs), 'specialist')}]: {nodes[s]['covers']}")
            if nodes[s]["triggers"]:
                print(f"    triggers: {nodes[s]['triggers']}")
    if specs:
        print("\nspecialists:")
        for name in specs:
            show_specialist(name, pkgs, topics)
    if not subs and not specs:
        print("\n(empty: no specialist here yet)")
    if parent(node):
        print(f"\nup: --node {parent(node)}")
    return 0


def check(nodes, node_errors, pkgs, kit_mode):
    errors, warnings = list(node_errors) + orphans(nodes), []
    where = "divisions.md" if kit_mode else "divisions.md or ~/.config/wiki-kit/divisions.local.md"
    for name, p in sorted(pkgs.items()):
        if p["error"]:
            errors.append(f"{name}: {p['error']}")
        if not p["division"]:
            errors.append(f'{name}: no metadata.division (add `  division: "<path>"` from divisions.md)')
        elif p["division"] not in nodes:
            errors.append(f"{name}: division {p['division']} is not in {where}")
        if name in nodes:
            errors.append(f"{name}: a specialist and a division share this name; --node cannot reach both")
        for t in p["out"]:
            if t not in pkgs:
                errors.append(f"{name}: hands over to `{t}`, which is not a specialist here")
    for p in [""] + sorted(nodes):
        subs, specs = children(p, nodes, pkgs)
        if len(subs) + len(specs) > MAX_CHILDREN:
            errors.append(f"{'division ' + p if p else 'the top level'} has {len(subs) + len(specs)} children, "
                          f"over {MAX_CHILDREN}: split it")
        if p and not subs and not specs:
            warnings.append(f"division {p} is empty")
    if kit_mode:
        staff = {r.get("name", "").strip("`"): r.get("division", "").strip("`")
                 for r in table_rows(STAFF.read_text(encoding="utf-8"), "division")}
        staff.pop("", None)
        for name in sorted(set(staff) | set(pkgs)):
            if name not in pkgs:
                errors.append(f"README Staff table lists `{name}`, which has no package")
            elif name not in staff:
                errors.append(f"{name}: missing from the README Staff table")
            elif pkgs[name]["division"] and staff[name] != pkgs[name]["division"]:
                errors.append(f"{name}: README Staff table says {staff[name]}, metadata says {pkgs[name]['division']}")
        fields, _ = parse_frontmatter(DESK.read_text(encoding="utf-8").splitlines())
        desc = (fields or {}).get("description", ("", False))[0]
        named = [n for n in pkgs if re.search(r"\b" + re.escape(n) + r"\b", desc)]
        if named:
            errors.append(f"front desk description names specialists ({', '.join(named)}): "
                          "keep it to divisions so its size stays constant")
        for p in sorted(x for x in nodes if "/" not in x):
            if p not in desc.lower() and nodes[p]["title"].lower() not in desc.lower():
                warnings.append(f"front desk description does not mention the top-level division {p}")
    for e in errors:
        print(f"ERROR {e}")
    for w in warnings:
        print(f"WARN  {w}")
    print(f"department map: {len(nodes)} divisions, {len(pkgs)} specialists, "
          f"{sum(len(p['out']) for p in pkgs.values())} handoffs: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def main(argv):
    ap = argparse.ArgumentParser(description="Tree of divisions and graph of handoffs of the specialist department.")
    ap.add_argument("--hub", help="hub folder (default: the configured hub; with --check: the kit)")
    ap.add_argument("--node", help="division path or specialist name to show")
    ap.add_argument("--check", action="store_true", help="check the tree; exit 1 on errors")
    a = ap.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):  # Windows pipes default to a legacy code page; -I ignores PYTHONUTF8
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    if a.hub:
        hub = Path(a.hub).expanduser()
        if not (hub / ".skills").is_dir():
            print(f"no .skills/ in {hub}", file=sys.stderr)
            return 2
    else:
        hub = None if a.check else hub_path(None)
        if hub and not (hub / ".skills").is_dir():
            hub = None
    root = hub / ".skills" if hub else KIT / "specialists"
    nodes, node_errors = read_divisions(hub)
    pkgs = read_packages(root)
    if a.check:
        return check(nodes, node_errors, pkgs, kit_mode=hub is None)
    for e in node_errors + orphans(nodes):
        print(f"warning: {e}", file=sys.stderr)
    topics = read_topics(hub) if hub else {}
    if a.node:
        return show_node(a.node.strip("/"), nodes, pkgs, topics)
    show_top(nodes, pkgs, f"hub {hub}" if hub else "kit")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
