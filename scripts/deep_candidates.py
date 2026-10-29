#!/usr/bin/env python3
"""List ChatGPT chats worth a deep extraction pass.

Usage:
  deep_candidates.py HUB_DIR [-o deep_candidates.tsv]

A chat (raw/notes/*chatgpt-chat*.md in any topic) is a candidate if raw size
>= 15 KB or >= 8 user turns. For each: size, user turns, citing articles,
article KB attributed to it (article size / its number of sources) and the
coverage ratio. A wave is assigned by title keywords ("waves" in ~/.config/wiki-kit/inventory.json).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Wave -> title keywords, from ~/.config/wiki-kit/inventory.json ("waves"); kept outside the
# repository because the keywords name your own chats.
_rules = Path("~/.config/wiki-kit/inventory.json").expanduser()
WAVES = json.loads(_rules.read_text(encoding="utf-8")).get("waves", {}) if _rules.exists() else {}


def wave_of(title: str) -> str:
    t = title.lower()
    for w, keys in WAVES.items():
        if any(k in t for k in keys):
            return w
    return "-"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hub", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=None)
    args = ap.parse_args()
    hub = args.hub.resolve()
    out = args.out or hub / "deep_candidates.tsv"

    cites: dict[str, list[tuple[int, int]]] = {}
    for art in hub.glob("topics/*/wiki/**/*.md"):
        if art.name == "_index.md":
            continue
        t = art.read_text(encoding="utf-8")
        fm = t.split("\n---", 1)[0]
        srcs = re.findall(r'^  - "?(raw/[^"\n]+)"?$', fm, re.M)
        for s in srcs:
            cites.setdefault(f"{art.relative_to(hub).parts[1]}/{s}", []).append((len(t.encode()), len(srcs)))

    rows = []
    for raw in sorted(hub.glob("topics/*/raw/notes/*chatgpt-chat*.md")):
        topic = raw.relative_to(hub).parts[1]
        t = raw.read_text(encoding="utf-8")
        size = len(t.encode())
        users = len(re.findall(r"^### User\b", t, re.M))
        m = re.search(r'^title: "?(.*?)"?$', t, re.M)
        title = m.group(1) if m else raw.stem
        c = cites.get(f"{topic}/raw/notes/{raw.name}", [])
        art_kb = sum(a / n for a, n in c) / 1024
        if size < 15 * 1024 and users < 8:
            continue
        rows.append((wave_of(title), topic, size / 1024, users, len(c), art_kb, art_kb / (size / 1024),
                     title, f"topics/{topic}/raw/notes/{raw.name}"))

    rows.sort(key=lambda r: (r[0] == "-", r[0], -r[2]))
    with out.open("w", encoding="utf-8") as f:
        f.write("wave\ttopic\tsize_kb\tuser_turns\tarticles\tarticle_kb\tcoverage\ttitle\tpath\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]:.0f}\t{r[3]}\t{r[4]}\t{r[5]:.1f}\t{r[6]:.3f}\t{r[7]}\t{r[8]}\n")
    by = {}
    for r in rows:
        by.setdefault(r[0], []).append(r)
    for w in sorted(by, key=lambda x: (x == "-", x)):
        print(f"\n== Волна {w}: {len(by[w])} чатов, {sum(r[2] for r in by[w]):.0f} КБ")
        for r in by[w]:
            print(f"  {r[2]:5.0f} КБ  {r[3]:3d} реплик  покрытие {r[6]:.2f}  [{r[1]}] {r[7][:70]}")
    print(f"\nвсего {len(rows)} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
