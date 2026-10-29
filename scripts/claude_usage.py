"""Estimate Claude Code token spend from local session logs.

Usage: claude_usage.py [--project SUBSTR] [--since YYYY-MM-DD] [--top N] <report> [...]
Reports: summary, sessions, days, tools, events, all (default: all), brief.

`brief --session last` is the short per-answer report (see CLAUDE.md): cost of the last
answer, of the session, of today and of the month, plus rule-based savings tips. It keeps
the previous total in ~/.cache/wiki-kit/usage_last.json to compute the per-answer delta.

Reads ~/.claude/projects/**/*.jsonl (main sessions and subagents/), deduplicates
streamed messages by message id and prices them at Claude API list prices.
Corporate billing may meter differently; the proportions still hold.

The `tools` report attributes context growth to tool results. A tool result
stays in context for every later call of the same session, so its real cost is
its size times the number of calls that re-read it ("carried" tokens).
"""
import argparse, collections, glob, json, os, sys

# $/MTok (input, output, cache read). Cache writes cost 2x input with the 1-hour TTL
# and 1.25x with the 5-minute one; logs without the split are counted as 1-hour (Claude
# Code's default). Source: claude-api skill pricing table, cached 2026-10-06.
PRICES = {
    "claude-fable-5-1": (10, 50, 0.25), "claude-fable-5": (10, 50, 0.25),
    "claude-opus-5-5": (4, 20, 0.20), "claude-opus-5": (5, 25, 0.50),
    "claude-opus-4-8": (5, 25, 0.50), "claude-sonnet-5-5": (2, 10, 0.20),
    "claude-sonnet-5": (2, 10, 0.20), "claude-sonnet-4-6": (3, 15, 0.30),
    "claude-haiku-5-5": (0.10, 0.50, 0.01), "claude-haiku-4-5": (1, 5, 0.10),
}
CHARS_PER_TOKEN = 3.5  # rough; mixed Russian/English text and JSON


def price(model):
    for k in sorted(PRICES, key=len, reverse=True):
        if model and model.startswith(k):
            return PRICES[k]
    return None


def call_cost(c):
    p = price(c["model"])
    if not p:
        return 0.0
    i, o, cr = p
    return (c["inp"] * i + write_cost(c, i) + c["cr"] * cr + c["out"] * o) / 1e6


def write_cost(c, i):
    return c["cw1h"] * i * 2 + (c["cw"] - c["cw1h"]) * i * 1.25


def text_len(content):
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(b.get("text", "")) if isinstance(b, dict) else len(str(b)) for b in content)
    return len(json.dumps(content or ""))


def label(name, inp):
    if name in ("Read", "Write", "Edit"):
        return f"{name} {os.path.basename(inp.get('file_path', ''))}"
    if name == "Bash":
        return "Bash " + inp.get("command", "").split("\n")[0][:60]
    if name == "Skill":
        return f"Skill {inp.get('skill')}"
    if name in ("Agent", "Task"):
        return f"Agent [{inp.get('model') or 'inherit'}] {inp.get('description', '')}"
    return name


def load(root, project, since):
    calls, results, events = [], [], []
    for f in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
        if project and project not in f:
            continue
        sub = "/subagents/" in f
        sess = (f.split("/subagents/")[0] if sub else f[:-6]).rsplit("/", 1)[-1][:8]
        agent = os.path.basename(f)[:-6] if sub else "main"
        seen, tools, file_calls, file_results = set(), {}, [], []
        for line in open(f, encoding="utf-8"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            ts = d.get("timestamp") or ""
            if since and ts and ts[:10] < since:
                continue
            if d.get("type") == "system" and "refusal" in str(d.get("subtype", "")):
                events.append(dict(sess=sess, agent=agent, ts=ts, kind=d["subtype"],
                                   category=d.get("apiRefusalCategory"), model=d.get("originalModel")))
            m = d.get("message") or {}
            content = m.get("content") if isinstance(m.get("content"), list) else []
            if d.get("type") == "assistant":
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        tools[b["id"]] = (b["name"], label(b["name"], b.get("input") or {}))
                u = m.get("usage")
                mid = m.get("id") or d.get("uuid")
                if u and mid not in seen and m.get("model") != "<synthetic>":
                    seen.add(mid)
                    cw = u.get("cache_creation_input_tokens", 0) or 0
                    split = u.get("cache_creation")
                    cw1h = (split.get("ephemeral_1h_input_tokens", 0) or 0) if split else cw
                    file_calls.append(dict(sess=sess, agent=agent, sub=sub, ts=ts, model=m.get("model"),
                                           inp=u.get("input_tokens", 0), out=u.get("output_tokens", 0),
                                           cw=cw, cw1h=cw1h,
                                           cr=u.get("cache_read_input_tokens", 0)))
            elif d.get("type") == "user":
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        name, lab = tools.get(b.get("tool_use_id"), ("?", "?"))
                        file_results.append(dict(sess=sess, agent=agent, name=name, label=lab,
                                                 tokens=text_len(b.get("content")) / CHARS_PER_TOKEN,
                                                 after=len(file_calls)))
        n = len(file_calls)
        p = price(file_calls[-1]["model"]) if file_calls else None
        for r in file_results:
            r["carried"] = r["tokens"] * max(n - r["after"], 0)
            r["cost"] = (r["tokens"] * p[0] * 2 + r["carried"] * p[2]) / 1e6 if p else 0
        calls += file_calls
        results += file_results
    for c in calls:
        c["cost"] = call_cost(c)
    return calls, results, events


def table(title, groups, total, top):
    print(f"\n== {title}")
    print(f"{'':58s} {'calls':>6s} {'cache_wr':>9s} {'cache_rd':>9s} {'output':>8s} {'$':>8s} {'%':>5s}")
    for k, g in sorted(groups.items(), key=lambda x: -x[1]["cost"])[:top]:
        print(f"{str(k)[:58]:58s} {g['n']:6d} {g['cw']/1e6:8.2f}M {g['cr']/1e6:8.1f}M "
              f"{g['out']/1e3:7.0f}k {g['cost']:8.2f} {100*g['cost']/total:5.1f}")


def group(calls, key):
    g = collections.defaultdict(collections.Counter)
    for c in calls:
        x = g[key(c)]
        x["n"] += 1
        for f in ("cw", "cr", "out", "cost"):
            x[f] += c[f]
    return g


def brief(calls, results, events, project, session):
    import datetime
    sess = max((c for c in calls), key=lambda c: c["ts"])["sess"] if session == "last" else session
    mine = [c for c in calls if c["sess"].startswith(sess)]
    if not mine:
        sys.exit("no calls for that session")
    sid = mine[0]["sess"]
    total = sum(c["cost"] for c in mine)
    state_file = os.path.expanduser("~/.cache/wiki-kit/usage_last.json")
    try:
        state = json.load(open(state_file))
    except (OSError, ValueError):
        state = {}
    prev = state.get(sid)
    delta = total - prev if prev is not None else None
    state[sid] = total
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    json.dump(state, open(state_file, "w"))
    main_calls = [c for c in mine if not c["sub"]]
    sub = sum(c["cost"] for c in mine if c["sub"])
    ctx = [c["inp"] + c["cw"] + c["cr"] for c in sorted(main_calls, key=lambda c: c["ts"])]
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    day = sum(c["cost"] for c in calls if c["ts"][:10] == today)
    month = sum(c["cost"] for c in calls if c["ts"][:7] == today[:7])
    by_model = collections.Counter()
    for c in mine:
        by_model[c["model"]] += c["cost"]
    print(f"Session {sid}: ${total:.2f} ({len(mine)} calls, subagents ${sub:.2f}); "
          + (f"last answer ≈ ${delta:.2f}; " if delta is not None else "first measurement; ")
          + f"today ${day:.2f}; month ${month:.2f} (project {project or 'all'}, list prices)")
    print("Models: " + ", ".join(f"{k} ${v:.2f}" for k, v in by_model.most_common(3))
          + f"; context now {ctx[-1]//1000 if ctx else 0}k tokens")
    tips = []
    if ctx and ctx[-1] > 150_000:
        tips.append(f"Context is {ctx[-1]//1000}k (>150k): note the state in README.md and start a new session.")
    elif ctx and ctx[-1] > 100_000:
        tips.append(f"Context is {ctx[-1]//1000}k: finish this task, commit, then /clear.")
    if total and sub / total > 0.4:
        tips.append(f"Subagents are {100*sub/total:.0f}% of the session: give them narrow scope, model sonnet/haiku, no re-reading.")
    opus = sum(v for k, v in by_model.items() if k and "opus" in k or k and "fable" in k)
    if total and opus / total > 0.7 and total > 2:
        tips.append("Mostly Opus/Fable: keep Opus for planning and review, move reading/copying to Sonnet agents or scripts.")
    r = [x for x in results if x["sess"] == sid]
    if r:
        top = max(r, key=lambda x: x["cost"])
        if top["cost"] > 0.3:
            tips.append(f"Biggest tool result: {top['label'][:60]} (~{top['tokens']/1e3:.0f}k tokens, ${top['cost']:.2f} carried): "
                        "use head/grep/offset or a script summary.")
    if any(e["sess"] == sid for e in events):
        tips.append("Safeguard fallback happened in this session: finish the step and start a new session.")
    if delta is not None and delta > 1.5:
        tips.append(f"This answer cost ${delta:.2f}: split big tasks, one task per session.")
    print("Tips: " + (" | ".join(tips) if tips else "nothing to fix right now."))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--project", help="substring of the project folder, e.g. wiki-internal")
    ap.add_argument("--since", help="YYYY-MM-DD (UTC)")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--session", help="session id prefix or 'last' (for the brief report)")
    ap.add_argument("reports", nargs="*", default=["all"])
    a = ap.parse_args()
    calls, results, events = load(a.root, a.project, a.since)
    if not calls:
        sys.exit("no calls found")
    if "brief" in a.reports:
        brief(calls, results, events, a.project, a.session or "last")
        return
    total = sum(c["cost"] for c in calls)
    want = set(a.reports)
    every = "all" in want

    if every or "summary" in want:
        by_type = collections.Counter()
        for c in calls:
            p = price(c["model"])
            if p:
                by_type["cache write"] += write_cost(c, p[0]) / 1e6
                by_type["cache read"] += c["cr"] * p[2] / 1e6
                by_type["output"] += c["out"] * p[1] / 1e6
                by_type["input"] += c["inp"] * p[0] / 1e6
        sub = sum(c["cost"] for c in calls if c["sub"])
        print(f"Total ≈ ${total:.2f} over {len(calls)} calls; subagents ${sub:.2f} ({100*sub/total:.0f}%)")
        print("By token type: " + ", ".join(f"{k} ${v:.2f} ({100*v/total:.0f}%)" for k, v in by_type.most_common()))
        table("by model", group(calls, lambda c: c["model"]), total, a.top)

    if every or "sessions" in want:
        table("by session / main vs subagents / model",
              group(calls, lambda c: (c["sess"], "sub" if c["sub"] else "main", c["model"])), total, a.top)
        print("\n== context size per main session (tokens re-read on every call)")
        for s in sorted({c["sess"] for c in calls}):
            cs = [c for c in calls if c["sess"] == s and not c["sub"]]
            if cs:
                ctx = [c["inp"] + c["cw"] + c["cr"] for c in cs]
                print(f"{s}  {cs[0]['ts'][:16]}  calls {len(cs):4d}  start {ctx[0]//1000:4d}k  "
                      f"avg {sum(ctx)//len(ctx)//1000:4d}k  max {max(ctx)//1000:4d}k  ${sum(c['cost'] for c in cs):7.2f}")
        subs = collections.defaultdict(list)
        for c in calls:
            if c["sub"]:
                subs[(c["sess"], c["agent"])].append(c)
        if subs:
            starts = [v[0]["inp"] + v[0]["cw"] + v[0]["cr"] for v in subs.values()]
            print(f"\nsubagents: {len(subs)}, start context avg {sum(starts)//len(starts)//1000}k "
                  f"(fixed overhead paid by each), avg cost ${sum(c['cost'] for v in subs.values() for c in v)/len(subs):.2f}")

    if every or "days" in want:
        table("by day (UTC)", group(calls, lambda c: c["ts"][:10]), total, a.top)

    if every or "tools" in want:
        for title, key in (("tool results by tool", lambda r: r["name"]),
                           ("largest single tool results (by carried cost)", lambda r: (r["sess"], r["label"]))):
            g = collections.defaultdict(collections.Counter)
            for r in results:
                x = g[key(r)]
                x["n"] += 1
                x["tok"] += r["tokens"]
                x["carried"] += r["carried"]
                x["cost"] += r["cost"]
            print(f"\n== {title}  (tokens ≈ chars/{CHARS_PER_TOKEN})")
            print(f"{'':70s} {'n':>5s} {'tokens':>8s} {'carried':>9s} {'$':>8s}")
            for k, x in sorted(g.items(), key=lambda kv: -kv[1]["cost"])[:a.top]:
                print(f"{str(k)[:70]:70s} {x['n']:5d} {x['tok']/1e3:7.0f}k {x['carried']/1e6:8.1f}M {x['cost']:8.2f}")

    if every or "events" in want:
        print("\n== safeguard refusals / model fallbacks")
        for e in sorted(events, key=lambda e: e["ts"]):
            print(f"{e['ts'][:16]} {e['sess']} {e['agent'][:14]:14s} {e['kind']:28s} {e['category']} {e['model'] or ''}")
        if not events:
            print("none")


if __name__ == "__main__":
    main()
