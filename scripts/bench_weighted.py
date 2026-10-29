#!/usr/bin/env python3
"""Weight a model_bench run by how often each task type occurs in the operator's real chats.

Usage: bench_weighted.py TASKS.json RUN_DIR CHAT_TASKS.tsv --judges J1,J2 [--extra wiki=10,calc=2]

Type weight = share of messages with that `primary` type in CHAT_TASKS.tsv (chat_tasks.py);
--extra adds types absent from chats (percent points). Tasks of one type are averaged first.
A failed task scores 0; a skipped one (no vision / no web) is left out, and `covered`
shows the weight share the model can serve. `gap` = weighted mean over tasks of
(score - best Claude score), for non-Claude models: > 0 means it beats the subscription there.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_bench import auto_score, code_score, load  # noqa: E402


def cell(r, task, t, judges, scores, m):
    if r is None or "error" in r:
        return 0.0
    if "skip" in r:
        return None
    if task["kind"] == "auto":
        return auto_score(r["text"], task["checks"])
    if task["kind"] == "code":
        return code_score(r["text"], task["tests"])
    js = [scores[f"{t}|{j}"]["scores"][m] for j in judges
          if f"{t}|{j}" in scores and m in scores[f"{t}|{j}"]["scores"]]
    return sum(js) / len(js) if js else 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tasks", type=Path)
    ap.add_argument("run", type=Path)
    ap.add_argument("chats", type=Path)
    ap.add_argument("--judges", required=True)
    ap.add_argument("--extra", default="")
    a = ap.parse_args()
    tasks = {t["id"]: t for t in json.loads(a.tasks.read_text())["tasks"]}
    answers, scores = load(a.run / "answers.json"), load(a.run / "scores.json")
    judges = a.judges.split(",")
    w = collections.Counter()
    for r in csv.DictReader(a.chats.open(), delimiter="\t"):
        w[r["primary"]] += int(r["msgs"] or 0)
    tot = sum(w.values())
    weight = {k: 100 * v / tot for k, v in w.items()}
    for kv in filter(None, a.extra.split(",")):
        k, v = kv.split("=")
        weight[k] = float(v)
    by_type = collections.defaultdict(list)
    for t, task in tasks.items():
        by_type[task["type"]].append(t)
    members = sorted({k.split("|")[0] for k in answers})
    grid = {m: {t: cell(answers.get(f"{m}|{t}"), task, t, judges, scores, m) for t, task in tasks.items()}
            for m in members}
    best_claude = {t: max((grid[m][t] for m in members if m.startswith("claude:") and grid[m][t] is not None),
                          default=None) for t in tasks}
    rows = []
    for m in members:
        num = den = gap_num = gap_den = 0.0
        for typ, ts in by_type.items():
            wt = weight.get(typ, 0)
            got = [grid[m][t] for t in ts if grid[m][t] is not None]
            if not got:
                continue
            num += wt * sum(got) / len(got); den += wt
            gaps = [grid[m][t] - best_claude[t] for t in ts if grid[m][t] is not None and best_claude[t] is not None]
            if gaps:
                gap_num += wt * sum(gaps) / len(gaps); gap_den += wt
        allw = sum(weight.get(typ, 0) for typ in by_type)
        cost = sum(answers[f"{m}|{t}"].get("cost") or 0 for t in tasks
                   if f"{m}|{t}" in answers and "text" in answers[f"{m}|{t}"])
        rows.append((num / den if den else 0, m, 100 * den / allw, None if m.startswith("claude:")
                     else gap_num / gap_den if gap_den else None, cost))
    rows.sort(reverse=True)
    print(f"| model | weighted score | covered weight | gap vs best Claude | cost of run |\n|---|---|---|---|---|")
    for s, m, cov, gap, cost in rows:
        print(f"| {m} | {s:.2f} | {cov:.0f}% | {'—' if gap is None else f'{gap:+.2f}'} | ${cost:.3f} |")
    print("\nweights (%): " + ", ".join(f"{k} {weight.get(k, 0):.1f}" for k in by_type))
    return 0


if __name__ == "__main__":
    sys.exit(main())
