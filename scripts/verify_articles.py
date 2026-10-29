#!/usr/bin/env python3
"""Second-pass check of wiki articles against their `sources:`: claims without support, gaps, contradictions.

Usage:
  verify_articles.py TOPIC_DIR [ARTICLE...] [--changed [REV]] [--since YYYY-MM-DD]
                     [--verifier V:M,...] [--budget 0.30] [--cap 60000] [--dry-run] [--wait-offpeak]

Articles: the ones given, else wiki/**/*.md changed against REV in the topic's git (default HEAD,
untracked included) with --changed, else those with `updated:` >= --since (default today).
Each article goes with its sources to council.py's VERIFY prompt (default deepseek:deepseek-flash,
cross-family to Claude, ≈$0.01-0.04 per article, half at DeepSeek off-peak). Sources over --cap tokens are cut to the paragraphs
that share the most terms with the article (the verifier is told so). Topic `work` and packets with
secret hits are checked by claude:sonnet on the subscription instead (council.guard).
Reports go to TOPIC/output/verify/DATE/<article>.md plus summary.md; every article is a journal
run (kind wiki-compile) for `council.py --mark` / `--journal`. Stops before --budget is exceeded.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import council  # noqa: E402

LOCAL_VERIFIER = "claude:sonnet"
VERIFY_OUT = 15000  # expected output tokens per article, for the estimate and --budget


def front(text: str) -> tuple[dict, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    head = m.group(1)
    # sources list ends at the next top-level key
    block = head.split("sources:", 1)[1] if "sources:" in head else ""
    block = block.split("\n", 1)[1] if "\n" in block else ""
    srcs = []
    for line in block.splitlines():
        if not line.startswith((" ", "-")):
            break
        if line.strip().startswith("-"):
            srcs.append(line.strip()[1:].strip().strip('"'))
    upd = re.search(r"^updated:\s*(\S+)", head, re.M)
    return {"sources": srcs, "updated": upd.group(1) if upd else ""}, text[m.end():]


def terms(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"\w{5,}|\d[\d.,]*\d|\d", text)}


def excerpt(src: str, article_terms: set[str], cap_chars: int) -> str:
    """Keep the paragraphs richest in the article's terms, in original order, up to cap_chars."""
    paras = [p for p in re.split(r"\n\s*\n", src) if p.strip()]
    ranked = sorted(range(len(paras)), key=lambda i: -len(terms(paras[i]) & article_terms))
    keep, size = set(), 0
    for i in ranked:
        if size + len(paras[i]) > cap_chars:
            continue
        keep.add(i); size += len(paras[i])
    return "\n\n".join(paras[i] if i in keep else "[...]" for i in sorted(keep | {i - 1 for i in keep if i}))


def changed(topic: Path, rev: str) -> list[Path]:
    git = lambda *a: subprocess.run(["git", "-C", str(topic), *a], capture_output=True, text=True).stdout.splitlines()
    root = Path(git("rev-parse", "--show-toplevel")[0])
    names = git("diff", "--name-only", rev, "--", "wiki") + git("ls-files", "--others", "--exclude-standard", "--full-name", "--", "wiki")
    return sorted({(root / n) if not Path(n).is_absolute() else Path(n) for n in names} & set(topic.glob("wiki/**/*.md")))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic", type=Path)
    ap.add_argument("articles", nargs="*", type=Path)
    ap.add_argument("--changed", nargs="?", const="HEAD", metavar="REV")
    ap.add_argument("--since", default=date.today().isoformat())
    ap.add_argument("--verifier", default="deepseek:deepseek-flash,openai:gpt-6-luna")
    ap.add_argument("--budget", type=float, default=0.30, help="stop before paid cost exceeds this (USD)")
    ap.add_argument("--cap", type=int, default=60000, help="max source tokens per article (all sources) before excerpting")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait-offpeak", action="store_true", help="sleep until DeepSeek off-peak (half price) first")
    a = ap.parse_args()
    council.load_env()
    topic = a.topic.resolve()
    if a.articles:
        arts = [p.resolve() for p in a.articles]
    elif a.changed:
        arts = changed(topic, a.changed)
    else:
        arts = [p for p in sorted(topic.glob("wiki/**/*.md")) if front(p.read_text(encoding="utf-8"))[0].get("updated", "") >= a.since]
    arts = [p for p in arts if not p.name.startswith("_")]
    if not arts:
        print("no articles to verify", file=sys.stderr); return 0
    prices = council.load_prices()
    verifiers = [m.strip() for m in a.verifier.split(",") if m.strip()]
    council.add_openrouter_prices(verifiers, prices)
    if a.wait_offpeak and not a.dry_run:
        council.wait_offpeak(verifiers)
    out_dir = topic / "output" / "verify" / date.today().isoformat()
    spent, rows = 0.0, []
    for art in arts:
        text = art.read_text(encoding="utf-8")
        meta, _ = front(text)
        at = terms(text)
        srcs = {s: (topic / s).read_text(encoding="utf-8", errors="replace") if (topic / s).is_file() else None
                for s in meta.get("sources", [])}
        total = sum(len(v) for v in srcs.values() if v)
        cut = council.tokens_estimate("x" * total) > a.cap  # --cap is for all sources of one article
        parts = []
        for s, src in srcs.items():
            if src is None:
                parts.append(f"# Source: {s}\n(missing file)"); continue
            if cut:
                src = excerpt(src, at, int(a.cap * 3 * len(src) / total))
            parts.append(f"# Source: {s}\n{src}")
        note = ("Sources were cut to the passages that share terms with the article; '[...]' marks gaps, so say "
                "'not in excerpt' rather than 'contradicts' when support may sit in a gap.\n\n") if cut else ""
        body = note + "\n\n".join(parts + [f"# Answer to check (wiki article {art.relative_to(topic)})\n{text}"])
        members = verifiers
        try:
            council.guard(verifiers, body, topic.name, "wiki-compile")
        except council.Blocked as e:
            members = [LOCAL_VERIFIER]
            print(f"{art.name}: {str(e).split('.')[0]} -> {LOCAL_VERIFIER}", file=sys.stderr)
        # verifier output is mostly reasoning: 6-30K tokens in the first runs (2026-10-26)
        est = council.price_call(members[0], council.tokens_estimate(body), 0, VERIFY_OUT, prices)[0] or 0
        rel = art.relative_to(topic)
        if a.dry_run:
            print(f"{rel}  ≈{council.tokens_estimate(body)} tok  {members[0]}  ≈${est:.4f}{'  (excerpted)' if cut else ''}")
            spent += est; continue
        if spent + est > a.budget:
            print(f"stop: next article ≈${est:.4f} would exceed --budget {a.budget} (spent ${spent:.4f})", file=sys.stderr)
            break
        res = []
        for m in members:
            res.append(council.ask(m, council.VERIFY, body, prices))
            if "text" in res[-1]:
                break
        r = res[-1]
        council.ledger(res, f"verify_articles {rel}")
        paid = sum(x.get("cost") or 0 for x in res if x.get("cost_note") != "subscription")
        spent += paid
        txt = r.get("text", "")
        vd = re.search(r"##\s*Verdict\s*\n+\W*(ok|minor|major)", txt, re.I)
        verdict = vd.group(1).lower() if vd else ("error" if "error" in r else "?")
        flagged = len(re.findall(r"not in (?:sources|excerpt)|contradicts", txt, re.I))
        run = council.journal_add("verify", [r["member"]], paid, f"article {rel}", "wiki-compile", topic.name, verdict)
        out_dir.mkdir(parents=True, exist_ok=True)
        rep = out_dir / (art.stem + ".md")
        council.save_text(rep, f"# Verify: {rel}\n\nDate: {date.today()} · script: verify_articles.py · verifier: {r['member']} · "
                          f"run: {run} · cost: {council.money(paid)}{' · sources excerpted' if cut else ''}\n\n"
                          + (txt or f"ERROR: {r.get('error', '')}") + "\n")
        rows.append((str(rel), verdict, flagged, paid, run, r["member"]))
        print(f"{rel}: {verdict}, {flagged} flagged, {council.money(paid)}, run {run}", file=sys.stderr)
    if a.dry_run:
        print(f"{len(arts)} articles, estimate ≈${spent:.4f} (budget {a.budget})"); return 0
    if rows:
        summ = out_dir / "summary.md"
        old = summ.read_text(encoding="utf-8") if summ.exists() else \
            "# Verify summary\n\n| article | verdict | flagged | cost | run | verifier |\n|---|---|---|---|---|---|\n"
        council.save_text(summ, old + "".join(f"| {r[0]} | {r[1]} | {r[2]} | {council.money(r[3])} | {r[4]} | {r[5]} |\n"
                                              for r in rows))
        print(f"spent ${spent:.4f}; reports in {out_dir}; mark runs: council.py --mark RUN error|nothing --by claude",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
