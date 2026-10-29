#!/usr/bin/env python3
"""Convert Claude / ChatGPT exports to one Markdown file per conversation.

Usage:
  chat2md.py EXPORT.json... --out TOPIC/inbox --ids ids.txt
  chat2md.py EXPORT.json... --out TOPIC/inbox --inventory inventory.tsv --topic career
  chat2md.py EXPORT.json... --out DIR --all

EXPORT is a Claude `conversations.json` or a ChatGPT `conversations-NNN.json`
(format is detected). Nothing is converted without a selection: pass --ids
(one conversation id per line), --inventory (rows with decision=ingest for
--topic, as written by inventory.py), or --all.

Output matches the earlier converted chats: YAML frontmatter, `## Transcript`,
`### User|Claude|ChatGPT — YYYY-MM-DD HH:MM`. Thinking, tool results, system and
hidden messages are omitted; tool calls become `*[tool: ...]*`. With --redact,
each file goes through raw_check.redact before it is written; the count is printed.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import raw_check  # noqa: E402

AUTHOR = os.environ.get("WIKI_KIT_AUTHOR", "unknown")  # your name, for authors:
TZ = None  # set from --tz; None = this machine's local time

TRANSLIT = dict(zip(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяіїєґў",
    ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t",
     "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya", "i", "yi", "ye", "g", "u"],
))


def slugify(title: str, limit: int = 40) -> str:
    s = "".join(TRANSLIT.get(ch, ch) for ch in title.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:limit].strip("-") or "untitled-chat"


def ts(value) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, timezone.utc).astimezone(TZ)
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(TZ)


def fmt(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d %H:%M") if dt else ""


def yq(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


# --- Claude -----------------------------------------------------------------

def claude_tool(block: dict) -> str:
    inp = block.get("input") or {}
    name = block.get("name") or "?"
    # Artifacts and written files are the conclusions of many chats: keep their full text.
    if name == "artifacts" and inp.get("content"):
        return f"**[Artifact: {inp.get('title') or inp.get('id') or 'artifact'}]**\n\n````\n{inp['content'].strip()}\n````"
    if name in ("create_file", "str_replace", "write") and (inp.get("file_text") or inp.get("content")):
        body = inp.get("file_text") or inp.get("content")
        return f"**[File: {inp.get('path') or inp.get('file_path') or ''}]**\n\n````\n{body.strip()}\n````"
    arg = next((str(inp[k]) for k in ("query", "url", "path", "command", "title") if inp.get(k)), "")
    arg = arg.replace("\n", " ")[:120]
    return f"*[tool: {block.get('name', '?')}{': ' + arg if arg else ''}]*"


def claude_message(m: dict) -> str:
    parts = []
    for b in m.get("content") or []:
        t = b.get("type")
        if t == "text" and b.get("text", "").strip():
            parts.append(b["text"].strip())
        elif t == "tool_use":
            parts.append(claude_tool(b))
        elif t == "image":
            parts.append("*[image]*")
        elif t == "voice_note":
            parts.append((b.get("text") or b.get("transcript") or "*[voice note]*").strip())
        elif t == "document":
            parts.append(f"*[document: {b.get('title') or b.get('name') or 'untitled'}]*")
        # thinking, tool_result, injected_prompt_block, token_budget: omitted
    if not parts and (m.get("text") or "").strip():
        parts.append(m["text"].strip())
    for a in m.get("attachments") or []:
        parts.append(f"*[attachment: {a.get('file_name', 'file')}]*")
        if (a.get("extracted_content") or "").strip():
            parts.append("```text\n" + a["extracted_content"].strip() + "\n```")
    for f in m.get("files") or []:
        parts.append(f"*[file: {f.get('file_name', 'file')}]*")
    return "\n\n".join(parts)


def claude_conversations(data: list) -> list[dict]:
    out = []
    for c in data:
        turns = []
        for m in c.get("chat_messages") or []:
            body = claude_message(m)
            if body:
                who = "User" if m.get("sender") == "human" else "Claude"
                turns.append((who, ts(m.get("created_at")), body))
        out.append({
            "id": c["uuid"], "title": (c.get("name") or "").strip() or "untitled chat",
            "created": ts(c.get("created_at")), "updated": ts(c.get("updated_at")),
            "source": f"https://claude.ai/chat/{c['uuid']}", "app": "claude",
            "intro": "Claude chat from the personal claude.ai account",
            "summary": (c.get("summary") or "").strip(), "turns": turns,
        })
    return out


# --- ChatGPT ----------------------------------------------------------------

def chatgpt_branch(conv: dict) -> list[dict]:
    """Messages on the path root -> current_node (the branch the user kept)."""
    mapping, node, path = conv["mapping"], conv.get("current_node"), []
    while node and node in mapping:
        if mapping[node].get("message"):
            path.append(mapping[node]["message"])
        node = mapping[node].get("parent")
    return path[::-1]


def chatgpt_message(m: dict) -> str:
    content = m.get("content") or {}
    ctype = content.get("content_type")
    if m.get("recipient") not in (None, "all"):
        return f"*[tool: {m['recipient']}]*"
    if ctype not in ("text", "multimodal_text"):
        return ""  # code to tools, thoughts, reasoning_recap, execution_output, system_error
    parts = []
    for p in content.get("parts") or []:
        if isinstance(p, str):
            if p.strip():
                parts.append(p.strip())
        elif isinstance(p, dict):
            pt = p.get("content_type", "")
            if pt == "audio_transcription" and p.get("text"):
                parts.append(p["text"].strip())
            elif "image" in pt:
                parts.append("*[image]*")
    return "\n\n".join(parts)


def chatgpt_conversations(data: list) -> list[dict]:
    out = []
    for c in data:
        if "mapping" not in c:
            continue
        turns = []
        for m in chatgpt_branch(c):
            role = (m.get("author") or {}).get("role")
            if role not in ("user", "assistant") or (m.get("metadata") or {}).get("is_visually_hidden_from_conversation"):
                continue
            body = chatgpt_message(m)
            if body:
                turns.append(("User" if role == "user" else "ChatGPT", ts(m.get("create_time")), body))
        cid = c.get("conversation_id") or c.get("id")
        out.append({
            "id": cid, "title": (c.get("title") or "").strip() or "untitled chat",
            "created": ts(c.get("create_time")), "updated": ts(c.get("update_time")),
            "source": f"https://chatgpt.com/c/{cid}", "app": "chatgpt",
            "intro": "ChatGPT chat from the personal chatgpt.com account",
            "summary": "", "turns": turns,
        })
    return out


def load_export(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a JSON list of conversations")
    sample = next((c for c in data if c), {})
    if "chat_messages" in sample:
        return claude_conversations(data)
    if "mapping" in sample:
        return chatgpt_conversations(data)
    raise SystemExit(f"{path}: unknown export format")


def export_date(path: Path) -> str:
    m = re.search(r"(\d{4})[-.](\d{2})[-.](\d{2})", str(path))
    return "-".join(m.groups()) if m else "unknown date"


# --- output -----------------------------------------------------------------

def render(c: dict, exported: str) -> str:
    created, updated = c["created"], c["updated"] or c["created"]
    d0 = created.date().isoformat() if created else ""
    d1 = updated.date().isoformat() if updated else d0
    label = "ChatGPT" if c["app"] == "chatgpt" else "Claude"
    lines = [
        "---",
        f"title: {yq(c['title'])}",
        f"source: {yq(c['source'])}",
        "type: notes",
        f"ingested: {date.today().isoformat()}",
        f"tags: [{c['app']}-chat]",
        f"summary: {yq(c['summary'][:300] or label + ' chat export.')}",
        f"authors: [{AUTHOR}, {label}]",
        f"source_date: {d0}",
        f"source_updated: {d1}",
        "---",
        "",
        f"# {c['title']}",
        "",
        f"> {c['intro']}, exported {exported}. Started {d0}, last updated {d1}. "
        "Thinking, tool results and hidden messages are omitted.",
        "",
        "## Transcript",
        "",
    ]
    for who, when, body in c["turns"]:
        lines += [f"### {who}" + (f" — {fmt(when)}" if when else ""), "", body, ""]
    return "\n".join(lines).rstrip() + "\n"


def selected_ids(args) -> set[str] | None:
    if args.all:
        return None
    ids: set[str] = set()
    if args.ids:
        text = sys.stdin.read() if str(args.ids) == "-" else args.ids.read_text(encoding="utf-8")
        ids |= {ln.split("#")[0].strip() for ln in text.splitlines() if ln.split("#")[0].strip()}
    if args.inventory:
        with args.inventory.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                if row.get("decision") == "ingest" and (not args.topic or row.get("topic") == args.topic) \
                        and "#" in row.get("path", ""):
                    ids.add(row["path"].rsplit("#", 1)[1])
    if not ids:
        raise SystemExit("no selection: pass --ids, --inventory (with --topic) or --all")
    return ids


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exports", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="target directory, usually topics/<name>/inbox")
    ap.add_argument("--ids", type=Path, help="file with conversation ids, or - for stdin")
    ap.add_argument("--inventory", type=Path, help="inventory.tsv; takes rows with decision=ingest")
    ap.add_argument("--topic", help="with --inventory: only rows for this topic")
    ap.add_argument("--all", action="store_true", help="convert every conversation")
    ap.add_argument("--redact", action="store_true", help="replace secrets/internal URLs via raw_check")
    ap.add_argument("--patterns", type=Path, help="extra internal patterns for raw_check")
    ap.add_argument("--tz", help="timezone for timestamps, e.g. Europe/Berlin (default: local)")
    ap.add_argument("--dry-run", action="store_true", help="print what would be written")
    args = ap.parse_args()
    global TZ
    TZ = ZoneInfo(args.tz) if args.tz else None

    want = selected_ids(args)
    extra = raw_check.load_patterns(args.patterns)
    args.out.mkdir(parents=True, exist_ok=True)
    total, written, found = Counter(), 0, set()

    for export in args.exports:
        exported = export_date(export)
        for c in load_export(export):
            if want is not None and c["id"] not in want:
                continue
            found.add(c["id"])
            if not c["turns"]:
                print(f"empty, skipped: {c['id']} {c['title']}")
                continue
            d0 = c["created"].date().isoformat() if c["created"] else "undated"
            stem = f"{d0}-{c['app']}-chat-{slugify(c['title'])}"
            target, n = args.out / f"{stem}.md", 2
            while target.exists() and c["source"] not in target.read_text(encoding="utf-8")[:600]:
                target, n = args.out / f"{stem}-{n}.md", n + 1
            text, counts = raw_check.redact(render(c, exported), extra) if args.redact else (render(c, exported), Counter())
            total += counts
            red = sum(counts.values())
            print(f"{'would write' if args.dry_run else 'wrote'} {target}" + (f"  (redacted {red})" if red else ""))
            if not args.dry_run:
                target.write_text(text, encoding="utf-8")
                written += 1

    if want is not None and want - found:
        print(f"not found in exports: {len(want - found)} id(s): " + ", ".join(sorted(want - found)[:5]), file=sys.stderr)
    n = sum(total.values())
    print(f"files: {written}  redacted: {n}" + (f"  ({', '.join(f'{k}={v}' for k, v in sorted(total.items()))})" if n else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
