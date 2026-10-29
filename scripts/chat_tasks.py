#!/usr/bin/env python3
"""Classify the operator's chats by task type (what the AI was asked to do), for benchmark design.

Usage:
  chat_tasks.py TOPIC_DIR... --out TSV [--model claude:sonnet] [--batch 40] [--limit N] [--wait-offpeak]

Reads raw/notes/*.md chat transcripts (ChatGPT / Claude exports), dedupes by `source`, and sends
title + date + first user message (+ counts) in batches to one model via council.py (default:
Claude on the subscription, since chats contain private data). Writes one TSV row per chat:
path, date, title, msgs, chars, primary, secondary, needs, stakes, lang. Re-runs skip rows already
in TSV. Prints a summary of task types at the end.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import council  # noqa: E402

TYPES = {
    "lookup": "справка и факты: как устроено, где взять, правила, процедуры",
    "choose": "сравнение и выбор: покупка, вариант, город, школа, тариф",
    "documents": "анализ документа, файла, скриншота, таблицы; извлечение данных",
    "writing": "написать или отредактировать текст: письмо, сообщение, пост, резюме, презентация",
    "translate": "перевод, язык, домашка по языку",
    "tech": "код, скрипты, Mac, сеть, настройка программ и устройств",
    "science": "наука и исследования: биология, омиксы, статьи, методы",
    "career": "карьера, стратегия, коучинг, поиск работы, переговоры",
    "health": "здоровье, симптомы, лекарства, врачи",
    "money_law": "финансы, банки, налоги, визы, ВНЖ, документы, право",
    "image_id": "распознать по фото: минерал, насекомое, растение, предмет",
    "plan": "планирование: поездка, маршрут, расписание, проект",
    "work": "работа на работодателя и клиентов: питчи, архитектура, данные",
    "learn": "объяснить концепцию, обучение, разобраться в теме",
    "other": "прочее",
}
SYSTEM = ("You classify chat sessions by the TASK the user gave the AI (not by topic). "
          "Allowed task types: " + "; ".join(f"{k} = {v}" for k, v in TYPES.items()) + ". "
          "For each item return primary (one type), secondary (zero or one type), needs (comma list from: "
          "web (fresh facts or prices), image (photo/screenshot input), long_doc (long text or file), "
          "calc (numbers), code, multi_turn (iterative refinement), none), stakes (low|medium|high: "
          "money, health, legal or career consequences), lang (ISO 639-1 code such as ru, en, uk, or mixed). "
          "Return ONLY a JSON list of objects with keys id, primary, secondary, needs, stakes, lang.")
COLS = ["path", "date", "title", "msgs", "chars", "primary", "secondary", "needs", "stakes", "lang"]


def chats(topics: list[Path]) -> list[dict]:
    seen, out = set(), []
    for t in topics:
        for p in sorted((t / "raw" / "notes").glob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            if "### User" not in text:
                continue
            src = re.search(r'^source:\s*"?([^"\n]+)', text, re.M)
            key = src.group(1) if src else p.name
            if key in seen:
                continue
            seen.add(key)
            title = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.M)
            date = re.search(r"^source_date:\s*(\S+)", text, re.M)
            first = re.search(r"### User[^\n]*\n+(.*?)(?=\n### |\Z)", text, re.S)
            out.append({"path": str(p), "date": date.group(1) if date else p.name[:10],
                        "title": title.group(1) if title else p.stem,
                        "msgs": len(re.findall(r"^### User", text, re.M)), "chars": len(text),
                        "first": " ".join((first.group(1) if first else "").split())[:500]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topics", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", default="claude:sonnet")
    ap.add_argument("--batch", type=int, default=40)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--wait-offpeak", action="store_true", help="sleep until DeepSeek off-peak (half price) first")
    a = ap.parse_args()
    council.load_env()
    done = {}
    if a.out.exists():
        done = {r["path"]: r for r in csv.DictReader(a.out.open(encoding="utf-8"), delimiter="\t")}
    items = [c for c in chats(a.topics) if c["path"] not in done][: a.limit]
    print(f"{len(items)} chats to classify ({len(done)} done)", file=sys.stderr)
    prices = council.load_prices()
    if a.wait_offpeak:
        council.wait_offpeak([a.model])
    for i in range(0, len(items), a.batch):
        chunk = items[i:i + a.batch]
        body = "\n".join(json.dumps({"id": n, "title": c["title"], "date": c["date"], "user_messages": c["msgs"],
                                     "first_user_message": c["first"]}, ensure_ascii=False)
                         for n, c in enumerate(chunk))
        r = council.ask(a.model, SYSTEM, body, prices)
        if "error" in r:
            print(f"batch {i}: {r['error'][:200]}", file=sys.stderr); continue
        m = re.search(r"\[.*\]", r["text"], re.S)
        try:
            res = {int(x["id"]): x for x in json.loads(m.group(0))} if m else {}
        except (ValueError, KeyError, TypeError):
            res = {}
        for n, c in enumerate(chunk):
            x = res.get(n)
            if x:
                done[c["path"]] = {**{k: c[k] for k in COLS[:5]}, "primary": x.get("primary", ""),
                                   "secondary": x.get("secondary") or "", "stakes": x.get("stakes", ""),
                                   "needs": ",".join(x["needs"]) if isinstance(x.get("needs"), list) else x.get("needs", ""),
                                   "lang": x.get("lang", "")}
        with a.out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, COLS, delimiter="\t")
            w.writeheader(); w.writerows(done.values())
        print(f"batch {i // a.batch + 1}: {len(res)}/{len(chunk)} classified, {r['sec']}s", file=sys.stderr)
    rows = list(done.values())
    print(f"\n{len(rows)} chats")
    for field in ("primary", "stakes", "lang"):
        print(field + ": " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r[field] for r in rows).most_common()))
    needs = collections.Counter(n for r in rows for n in r["needs"].split(",") if n)
    print("needs: " + ", ".join(f"{k} {v}" for k, v in needs.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
