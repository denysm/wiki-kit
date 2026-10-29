#!/usr/bin/env python3
"""Find knowledge phrases in topic raw/ files, print hits with context (input for ADRs).

Usage: decisions_scan.py TOPIC_DIR... [--kind decision,principle,plan,idea|all] [--context N] [--max-per-file N]
Kinds are the PKIS knowledge types (decision, principle, plan, idea); default: decision.
Output (stdout): per file, the frontmatter title and each matching line, tagged [kind], with N lines around it.
"""
import argparse
import re
from pathlib import Path

KINDS = {
    "decision": [
        r"\bрешил[аио]?\b", r"\bрешили\b", r"\bвыбрал[аио]?\b", r"\bвыбрали\b",
        r"\bоткатил[аио]?\b", r"\bоткатили\b", r"\bостановил(ся|ась|ись)\s+на\b",
        r"\bwe decided\b", r"\bi decided\b", r"\bdecided to\b", r"\blet'?s use\b",
        r"\bwe chose\b", r"\bi chose\b", r"\bwent with\b", r"\brolled back\b",
    ],
    "principle": [
        r"\bпринцип\w*", r"\bправило\b", r"\bправила\b", r"\bникогда не\b",
        r"\bprinciples?\b", r"\brule of thumb\b", r"\bgolden rule\b",
    ],
    "plan": [
        r"\bплан(ы|а|у|ом|е)?\b", r"\bпланиру\w+", r"\bследующи[йе] шаг\w*", r"\bсобираюсь\b",
        r"\bnext steps?\b", r"\broadmap\b", r"\bi plan\b", r"\bwe plan\b",
    ],
    "idea": [
        r"\bиде(я|ю|и|ей)\b", r"\bа что если\b", r"\bwhat if\b", r"\bideas?\b",
    ],
}


def title_of(text):
    m = re.search(r"^title:\s*\"?(.+?)\"?\s*$", text, re.M)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topics", nargs="+")
    ap.add_argument("--context", type=int, default=1)
    ap.add_argument("--max-per-file", type=int, default=6)
    ap.add_argument("--width", type=int, default=300)
    ap.add_argument("--kind", default="decision", help="comma list of %s, or all" % ",".join(KINDS))
    a = ap.parse_args()
    kinds = list(KINDS) if a.kind == "all" else a.kind.split(",")
    rxs = {k: re.compile("|".join(KINDS[k]), re.I) for k in kinds}
    total = 0
    for t in a.topics:
        for p in sorted(Path(t, "raw").rglob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            hits = [(i, k) for i, l in enumerate(lines) for k, rx in rxs.items() if rx.search(l)]
            if not hits:
                continue
            total += len(hits)
            print(f"\n=== {p} | {title_of(text)} | hits={len(hits)}")
            for i, k in hits[: a.max_per_file]:
                lo, hi = max(0, i - a.context), min(len(lines), i + a.context + 1)
                snippet = " / ".join(l.strip() for l in lines[lo:hi] if l.strip())
                print(f"  L{i + 1} [{k}]: {snippet[: a.width]}")
    print(f"\nTOTAL hits: {total}")


if __name__ == "__main__":
    main()
