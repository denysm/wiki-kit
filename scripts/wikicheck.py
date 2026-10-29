#!/usr/bin/env python3
"""Check compiled articles of a topic wiki before lint.

Usage:
  wikicheck.py TOPIC_DIR [--today YYYY-MM-DD] [--fresh] [--inbox-days N] [--suggest N]

For every wiki/**/*.md article: required frontmatter (volatility, verified,
confidence, summary, non-empty sources that exist), See Also targets exist, and
every See Also link A->B has a link back B->A. Prints problems; exit 1 if any.
--suggest N lists the top N See Also candidates: article pairs with no link either
way that share >= 2 linked articles, ranked by Adamic-Adar (a shared hub counts
less). Advice only, never an error; read both articles before adding a link.

Lifecycle rules taken from PKIS (Knowledge Object, 2025-12-21):
  - no source -> no article (empty sources is an error);
  - no summary -> not stable (missing summary is an error);
  - last_reviewed -> `verified` older than the volatility half-life
    (hot 30, warm 90, cold 365 days, as in the librarian) is a warning;
  - inbox lives no longer than 14 days: older unprocessed inbox files are warnings.
--fresh restores the compile-wave rule: every article must be verified today.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from datetime import date
from itertools import combinations
from pathlib import Path

HALF_LIFE = {"hot": 30, "warm": 90, "cold": 365}


def see_also(text: str) -> set[str]:
    part = text.split("## See Also", 1)[1].split("## Sources", 1)[0] if "## See Also" in text else ""
    return set(re.findall(r"\[\[([^|\]]+)\|", part))


def field(fm: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*\"?(.*?)\"?\s*$", fm, re.M)
    return m.group(1) if m else ""


def article_links(p: Path, text: str, arts: dict[str, Path]) -> set[str]:
    """Slugs of other articles linked anywhere in the text: [[slug|...]] or [x](rel.md)."""
    out = {m.strip() for m in re.findall(r"\[\[([^|\]#]+)", text)}
    for m in re.findall(r"\]\(([^)#\s]+\.md)", text):
        q = (p.parent / m).resolve()
        if q.stem in arts and arts[q.stem] == q:
            out.add(q.stem)
    return (out & arts.keys()) - {p.stem}


def suggest_see_also(arts: dict[str, Path], top: int) -> None:
    nb: dict[str, set[str]] = {s: set() for s in arts}
    for s, p in arts.items():
        for t in article_links(p, p.read_text(encoding="utf-8"), arts):
            nb[s].add(t); nb[t].add(s)
    pairs = []
    for a, b in combinations(sorted(arts), 2):
        common = nb[a] & nb[b]
        if b not in nb[a] and len(common) >= 2:
            pairs.append((sum(1 / math.log(len(nb[c])) for c in common), len(common), a, b))
    pairs.sort(reverse=True)
    print(f"See Also candidates: {len(pairs)} unlinked pair(s) sharing >= 2 articles, top {min(top, len(pairs))}:")
    for score, n, a, b in pairs[:top]:
        print(f"  {score:.2f} ({n} shared)  {a} <-> {b}")


def inbox_warnings(root: Path, today: date, max_days: int) -> int:
    n = 0
    for p in sorted((root / "inbox").glob("*")):
        if p.name.startswith(".") or not p.is_file():
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
        born = date.fromisoformat(m.group(1)) if m else date.fromtimestamp(p.stat().st_mtime)
        if (today - born).days > max_days:
            print(f"warn: inbox/{p.name}: waiting {(today - born).days} days (> {max_days})"); n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic", type=Path)
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--fresh", action="store_true", help="require verified == today (compile waves)")
    ap.add_argument("--inbox-days", type=int, default=14)
    ap.add_argument("--suggest", type=int, default=0, metavar="N", help="show top N See Also candidates")
    args = ap.parse_args()
    today = date.fromisoformat(args.today)
    root = args.topic.resolve()
    arts = {p.stem: p for p in (root / "wiki").rglob("*.md") if p.name != "_index.md"}
    bad = warn = 0
    for slug, p in sorted(arts.items()):
        rel = p.relative_to(root)
        t = p.read_text(encoding="utf-8")
        fm = t.split("\n---", 1)[0]
        for key in ("volatility", "confidence", "verified", "summary"):
            if not field(fm, key):
                print(f"{rel}: missing {key}:"); bad += 1
        if "sources:" not in fm:
            print(f"{rel}: missing sources:"); bad += 1
        verified = field(fm, "verified")
        if verified:
            try:
                age = (today - date.fromisoformat(verified)).days
            except ValueError:
                print(f"{rel}: bad verified date {verified}"); bad += 1
            else:
                if args.fresh and age:
                    print(f"{rel}: verified {verified}, expected {args.today}"); bad += 1
                limit = HALF_LIFE.get(field(fm, "volatility"), HALF_LIFE["warm"])
                if age > limit:
                    print(f"warn: {rel}: stale, verified {age} days ago (> {limit})"); warn += 1
        srcs = re.findall(r'^  - "?(raw/[^"\n]+)"?$', fm, re.M)
        if not srcs:
            print(f"{rel}: empty sources"); bad += 1
        for s in srcs:
            if not (root / s).exists():
                print(f"{rel}: missing source {s}"); bad += 1
        links = see_also(t)
        if not links:
            print(f"{rel}: no See Also"); bad += 1
        for tgt in links:
            if tgt not in arts:
                print(f"{rel}: See Also target missing: {tgt}"); bad += 1
            elif slug not in see_also(arts[tgt].read_text(encoding="utf-8")):
                print(f"missing backlink {tgt} -> {slug}"); bad += 1
    warn += inbox_warnings(root, today, args.inbox_days)
    if args.suggest:
        suggest_see_also(arts, args.suggest)
    print(f"checked {len(arts)} articles, {bad} problem(s), {warn} warning(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
