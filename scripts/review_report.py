#!/usr/bin/env python3
"""Build review.md from inventory.tsv: decision=review rows grouped by category.

Usage: review_report.py INVENTORY_TSV -o REVIEW_MD
"""
import argparse
import csv
import re
from collections import defaultdict

CATEGORIES = [
    ("health", "Здоровье"),
    ("shopping", "Покупки"),
    ("language", "Язык"),
    ("travel-outdoor", "Поездки"),
    ("tech", "Техника"),
    ("unsorted", "Без категории"),
    ("other", "Прочее (не чаты: LinkedIn-архивы, docx, артефакты, memory, проекты)"),
]


def category(row):
    m = re.match(r"bucket (\S+)", row["reason"])
    return m.group(1) if m else "other"


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    with open(a.inventory, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if r["decision"] == "review"]
    groups = defaultdict(list)
    for r in rows:
        groups[category(r)].append(r)

    out = [
        "# Review: кандидаты на решение оператора",
        "",
        f"Источник: `inventory.tsv`, decision=review, {len(rows)} строк. "
        "Ничего не ingest-ено. Пришлите номера `n` для ingest (и тему); остальное — skip.",
        "",
        "| Категория | Шт. |",
        "|---|---|",
    ]
    known = [k for k, _ in CATEGORIES]
    extra = sorted(k for k in groups if k not in known)
    cats = CATEGORIES + [(k, k) for k in extra]
    for key, name in cats:
        if groups.get(key):
            out.append(f"| {name} | {len(groups[key])} |")
    for key, name in cats:
        items = sorted(groups.get(key, []), key=lambda r: (r["date"], int(r["n"])))
        if not items:
            continue
        out += ["", f"## {name} ({len(items)})", "",
                "| n | Дата | Размер | Msgs | Тема | Заголовок | Причина |",
                "|---|---|---|---|---|---|---|"]
        for r in items:
            size = int(r["size"] or 0)
            size_s = f"{size / 1024:.0f}K" if size < 1 << 20 else f"{size / (1 << 20):.1f}M"
            out.append(f"| {r['n']} | {r['date']} | {size_s} | {r['msgs']} | {r['topic']} "
                       f"| {cell(r['title'])} | {cell(r['reason'])} |")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"{a.out}: {len(rows)} rows, " +
          ", ".join(f"{k}={len(v)}" for k, v in sorted(groups.items())))


if __name__ == "__main__":
    main()
