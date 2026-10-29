#!/usr/bin/env python3
"""Small benchmark of LLMs on the operator's own tasks, with cost, latency and blind cross-family judges.

Usage:
  model_bench.py TASKS.json --topic TOPIC_DIR --models M1,M2,... --judges J1,J2 --out DIR [--workers 8]
  model_bench.py TASKS.json --out DIR --report-only
  model_bench.py TASKS.json --out DIR --models NEW --dry-run      # delta: missing calls and their cost
  model_bench.py TASKS.json --out DIR --report-only --judges J1,J2 --export-stats   # seed council.py --route
  add --wait-offpeak to bulk runs with DeepSeek members: waits for the half-price window

TASKS.json: {"system", "tasks": [{"id", "kind": "auto"|"judge", "prompt", "checks"|"reference"+"rubric"}]}.
Prompts may include {{file:REL}} (path relative to TOPIC_DIR). Members use council.py syntax
VENDOR:MODEL[@EFFORT]. Answers are cached in DIR/answers.json (re-runs skip done pairs);
judge scores in DIR/scores.json; the table goes to DIR/report.md (with $/task and the number of tasks
where a non-Claude model matches the best Claude answer: the complement to a Claude subscription).
auto: each check {"n", "any"|"all"|"none": [regex]} is tested on the answer line "N: ...".
judge: every judge scores all anonymous answers 0-10 against the reference; a judge never scores
its own family (anthropic, openai, google, deepseek, ... from the vendor or OpenRouter prefix).
Optional task fields: "images": [paths] (photos, downscaled and cached), "web": true (search allowed),
"turns": [follow-up user messages] (multi-turn; the judged text is the whole dialogue).
code: the first ```python block of the answer runs in a temp dir (python -I, empty env, 20 s timeout)
followed by "tests": [python expressions; helpers D = datetime module, raises(fn, exc)]; score = share of expressions that evaluate truthy.
A member that lacks a needed capability gets "skip": excluded from its average, shown as coverage.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import council  # noqa: E402

FAMILY = {"claude": "anthropic", "openai": "openai", "gemini": "google", "deepseek": "deepseek"}
JUDGE_SYS = ("You are a strict, fair grader. You will get a task, a reference (what a good answer contains) "
             "and several anonymous answers. Score each answer 0-10 against the reference and rubric. "
             "Ignore length and order. Return ONLY JSON: {\"A\": score, \"B\": score, ...}.")


def family(member: str) -> str:
    vendor, model, _ = council.split_member(member)
    if vendor == "openrouter":
        return {"meta-llama": "meta", "anthropic": "anthropic"}.get(model.split("/")[0], model.split("/")[0])
    return FAMILY.get(vendor, vendor)


def render(prompt: str, topic: Path | None) -> str:
    return re.sub(r"\{\{file:([^}]+)\}\}", lambda m: (topic / m.group(1)).read_text(encoding="utf-8"), prompt)


def line_for(text: str, n: int) -> str:
    for ln in text.splitlines():
        m = re.match(rf"\s*\**{n}\**\s*[:.)]\s*(.*)", ln)
        if m:
            return m.group(1)
    return ""


def auto_score(text: str, checks: list[dict]) -> float:
    ok = 0
    for c in checks:
        ln = line_for(text, c["n"])
        good = bool(ln)
        if "any" in c:
            good &= any(re.search(p, ln, re.I) for p in c["any"])
        if "all" in c:
            good &= all(re.search(p, ln, re.I) for p in c["all"])
        if "none" in c:
            good &= not any(re.search(p, ln, re.I) for p in c["none"])
        ok += good
    return 10 * ok / len(checks)


RUNNER = """
import datetime as D, json, sys


def raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


ns = {"D": D, "raises": raises}
code, tests = json.load(sys.stdin)
try:
    exec(code, ns)
except Exception as e:
    print(json.dumps([False] * len(tests))); sys.exit()
res = []
for t in tests:
    try:
        res.append(bool(eval(t, ns)))
    except Exception:
        res.append(False)
print(json.dumps(res))
"""


def code_score(text: str, tests: list[str]) -> float:
    import subprocess
    import tempfile
    m = re.search(r"```(?:python|py)?\s*\n(.*?)```", text, re.S)
    if not m:
        return 0.0
    with tempfile.TemporaryDirectory() as d:  # no API keys: empty environment
        try:
            r = subprocess.run([sys.executable, "-I", "-c", RUNNER], input=json.dumps([m.group(1), tests]),
                               capture_output=True, text=True, cwd=d, env={"PATH": "/usr/bin:/bin"}, timeout=20)
            res = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            return 0.0
    return 10 * sum(res) / len(tests)


def load(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tasks", type=Path)
    ap.add_argument("--topic", type=Path)
    ap.add_argument("--models", default="")
    ap.add_argument("--judges", default="claude:opus,openai:gpt-6.1-sol")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--export-stats", action="store_true", help="seed council.py learned stats from this bench")
    ap.add_argument("--dry-run", action="store_true", help="count missing calls and estimate their cost, then exit")
    ap.add_argument("--wait-offpeak", action="store_true", help="sleep until DeepSeek off-peak (half price) first")
    a = ap.parse_args()
    council.load_env()
    spec = json.loads(a.tasks.read_text())
    tasks = {t["id"]: t for t in spec["tasks"]}
    a.out.mkdir(parents=True, exist_ok=True)
    ans_f, sc_f = a.out / "answers.json", a.out / "scores.json"
    answers, scores = load(ans_f), load(sc_f)
    prices = council.load_prices()
    members = [m.strip() for m in a.models.split(",") if m.strip()] or sorted({k.split("|")[0] for k in answers})
    judges = [j.strip() for j in a.judges.split(",") if j.strip()]
    council.add_openrouter_prices(members + judges, prices)

    if not a.report_only:
        todo = [(m, t) for m in members for t in tasks if f"{m}|{t}" not in answers or "error" in answers[f"{m}|{t}"]]
        council.add_openrouter_prices(members, prices)  # also loads OpenRouter input modalities
        print(f"{len(todo)} calls to make", file=sys.stderr)
        if a.dry_run:
            unpriced = sorted({m for m, _ in todo if not council.price_call(m, 1, 0, 1, prices)[0]
                               and not m.startswith("claude:")})
            print(f"estimate ≈${estimate(todo, answers, prices):.4f} for answers (judging not included)"
                  + (f"; no price for {', '.join(unpriced)}" if unpriced else ""), file=sys.stderr)
            return 0
        if a.wait_offpeak:
            council.wait_offpeak([m for m, _ in todo] + judges)

        def run(pair):
            m, t = pair
            task = tasks[t]
            return pair, council.ask(m, spec["system"], render(task["prompt"], a.topic), prices,
                                     images=tuple(task.get("images", ())), web=task.get("web", False),
                                     turns=[render(x, a.topic) for x in task.get("turns", [])])

        with cf.ThreadPoolExecutor(a.workers) as ex:
            for (m, t), r in ex.map(run, todo):
                answers[f"{m}|{t}"] = r
                council.save_text(ans_f, json.dumps(answers, ensure_ascii=False, indent=1))
                council.ledger([dict(r, member=f"{m}|{t}")], "model_bench")  # per answer: a power cut loses no paid row
                print(f"{m:45} {t:10} {'ERR ' + r['error'][:60] if 'error' in r else 'SKIP' if 'skip' in r else money(r.get('cost'))} {r['sec']}s",
                      file=sys.stderr)

        for t, task in tasks.items():
            if task["kind"] != "judge":
                continue
            for j in judges:
                key = f"{t}|{j}"
                pool = [m for m in members if "text" in answers.get(f"{m}|{t}", {}) and family(m) != family(j)]
                if key in scores and set(scores[key]["scores"]) >= set(pool):
                    continue
                rnd = random.Random(f"{t}{j}")
                rnd.shuffle(pool)
                labels = {f"A{i + 1}": m for i, m in enumerate(pool)}
                body = (f"# Task\n{render(task['prompt'], a.topic)}\n\n# Reference\n{task['reference']}\n\n"
                        f"# Rubric\n{task['rubric']}\n\n# Answers\n"
                        + "\n\n".join(f"## {k}\n{answers[f'{m}|{t}']['text']}" for k, m in labels.items())
                        + "\n\nReturn JSON with keys " + ", ".join(labels))
                r = council.ask(j, JUDGE_SYS, body, prices)
                council.ledger([dict(r, member=f"judge {j}|{t}")], "model_bench judge")
                if "error" in r:
                    print(f"judge {j} on {t}: {r['error'][:100]}", file=sys.stderr); continue
                js = re.search(r"\{.*\}", r["text"], re.S)
                try:
                    raw = json.loads(js.group(0)) if js else {}
                except ValueError:
                    raw = {}
                scores[key] = {"scores": {labels[k]: float(v) for k, v in raw.items() if k in labels},
                               "cost": r.get("cost"), "cost_note": r.get("cost_note"), "sec": r["sec"]}
                council.save_text(sc_f, json.dumps(scores, ensure_ascii=False, indent=1))
                print(f"judge {j:30} {t:10} scored {len(scores[key]['scores'])}/{len(pool)} {money(r.get('cost'))}",
                      file=sys.stderr)

    report(a.out, spec, tasks, members, judges, answers, scores)
    if a.export_stats:
        export_stats(a.out, a.topic.name if a.topic else "", tasks, members, judges, answers, scores)
    return 0


def estimate(todo: list[tuple[str, str]], answers: dict, prices: dict) -> float:
    """Price missing calls at each task's median in/out tokens over models already answered (delta runs)."""
    import statistics
    usage: dict[str, list[tuple[int, int]]] = {}
    for k, r in answers.items():
        if "in" in r:
            usage.setdefault(k.split("|")[1], []).append((r["in"], r["out"]))
    total = 0.0
    for m, t in todo:
        u = usage.get(t) or [(2000, 2000)]
        tin, tout = statistics.median(x[0] for x in u), statistics.median(x[1] for x in u)
        total += council.price_call(m, int(tin), 0, int(tout), prices)[0] or 0
    return total


def money(x) -> str:
    return "n/a" if x is None else f"${x:.4f}"


def task_score(m: str, t: str, tasks: dict, answers: dict, scores: dict, judges: list[str]) -> float | None:
    """0-10 score of one answer, or None when it failed / was not judged."""
    r = answers.get(f"{m}|{t}")
    if not r or "text" not in r:
        return None
    if tasks[t]["kind"] == "auto":
        return auto_score(r["text"], tasks[t]["checks"])
    if tasks[t]["kind"] == "code":
        return code_score(r["text"], tasks[t]["tests"])
    js = [scores[f"{t}|{j}"]["scores"][m] for j in judges if f"{t}|{j}" in scores and m in scores[f"{t}|{j}"]["scores"]]
    return sum(js) / len(js) if js else None


def export_stats(out: Path, topic: str, tasks, members, judges, answers, scores) -> None:
    """Seed council.py learned stats (kind = task type) from this bench; replaces this bench's earlier rows."""
    source = f"bench:{out.name}"
    keep = [r for r in council.stats_read() if r["source"] != source]
    council.stats_write(keep)
    n = 0
    for t, task in tasks.items():
        scored = {m: v for m in members if (v := task_score(m, t, tasks, answers, scores, judges)) is not None}
        council.stats_add(out.name, source, task.get("type", t), topic, scored,
                          {m: answers[f"{m}|{t}"].get("cost") for m in scored}, bool(task.get("web")))
        n += len(scored)
    print(f"exported {n} scores from {len(tasks)} tasks to {council.STATS}", file=sys.stderr)


def report(out: Path, spec, tasks, members, judges, answers, scores) -> None:
    tids = list(tasks)
    rows = []
    for m in members:
        cells, cost, sec, reas, outt, errs, skips = [], 0.0, 0.0, 0, 0, 0, 0
        priced = True
        for t in tids:
            r = answers.get(f"{m}|{t}")
            if r and "skip" in r:
                cells.append("skip"); skips += 1; continue
            if not r or "error" in r:
                cells.append(None); errs += 1; continue
            cost += r.get("cost") or 0
            priced &= r.get("cost") is not None
            sec += r["sec"]; reas += r.get("reasoning") or 0; outt += r.get("out") or 0
            cells.append(task_score(m, t, tasks, answers, scores, judges))
        got = [c for c in cells if isinstance(c, float)]
        n = len(tids) - skips
        avg = sum(got) / n if n else 0  # failed tasks count as 0, skipped ones are left out
        sub = "subscription" if m.startswith("claude:") else ("" if priced else "partly unpriced")
        rows.append((avg, m, cells, cost, sec, reas, outt, errs, sub, f"{n}/{len(tids)}"))
    rows.sort(reverse=True)
    # complement to the Claude subscription: tasks where a model matches the best Claude answer
    best_claude = [max([c for _, m, cells, *_ in rows if m.startswith("claude:") for c in [cells[i]]
                        if isinstance(c, float)], default=None) for i in range(len(tids))]
    vs = {m: sum(isinstance(c, float) and b is not None and c >= b for c, b in zip(cells, best_claude))
          for _, m, cells, *_ in rows}
    head = ["| # | model | " + " | ".join(tids)
            + " | avg | coverage | cost | $/task | ≥best Claude | sec | out tok (reasoning) | errors |",
            "|---" * (len(tids) + 10) + "|"]
    cell = lambda c: "—" if c is None else "skip" if c == "skip" else f"{c:.1f}"
    lines = [f"| {i + 1} | {m} | " + " | ".join(cell(c) for c in cells)
             + f" | **{avg:.1f}** | {cov} | {money(cost)} {sub} | {money(cost / max(1, int(cov.split('/')[0]) - errs))}"
             + f" | {'—' if m.startswith('claude:') else vs[m]} | {sec:.0f} | {outt} ({reas}) | {errs} |"
             for i, (avg, m, cells, cost, sec, reas, outt, errs, sub, cov) in enumerate(rows)]
    jcost = sum(v.get("cost") or 0 for v in scores.values() if v.get("cost_note") != "subscription")
    txt = "\n".join([f"# Model bench ({spec.get('created')}, tasks v{spec.get('version')})", "",
                     "Scores 0-10: auto = share of correct checks; judge = mean of cross-family judges "
                     f"({', '.join(judges)}). Failed task = 0 in avg; skip (no vision / no web) is left out "
                     "of avg and shown in coverage. Cost/sec are sums over tasks.", ""]
                    + head + lines + ["", f"Judge cost (paid API): {money(jcost)}", ""])
    (out / "report.md").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    sys.exit(main())
