"""Convert Claude Desktop Cowork sessions to Markdown raw notes.

Usage: cowork2md.py <sessions_dir> <plan.json>
plan.json: [{"id": "c6875113", "dest": "/abs/dir", "tags": ["project-a"]}, ...]
Reads local_<id>*.json metadata and the session's .claude/projects/**/*.jsonl
transcripts. Keeps user and assistant text and tool names; drops tool results,
system reminders and sidechains. Refuses to overwrite.
"""
import os
import datetime as dt
import json
import re
import sys
import unicodedata
from pathlib import Path

base = Path(sys.argv[1])
plan = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
TODAY = __import__("datetime").date.today().isoformat()


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:45].rstrip("-") or "session"


def yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def ts(ms) -> dt.datetime:
    ms = float(ms)
    return dt.datetime.fromtimestamp(ms / 1000 if ms > 1e11 else ms, dt.timezone.utc)


def clean(text: str) -> str:
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    return text.strip()


def render(content, role: str) -> str:
    if isinstance(content, str):
        return clean(content)
    parts = []
    for b in content or []:
        t = b.get("type")
        if t == "text":
            txt = clean(b.get("text") or "")
            if txt:
                parts.append(txt)
        elif t == "tool_use" and role == "assistant":
            inp = b.get("input") or {}
            target = inp.get("file_path") or inp.get("path") or inp.get("command") or inp.get("query") or inp.get("url") or inp.get("description") or ""
            parts.append(f"*[tool: {b.get('name')}{': ' + str(target)[:200] if target else ''}]*")
    return "\n\n".join(parts)


written = []
for item in plan:
    metas = list(base.glob(f"local_{item['id']}*.json"))
    assert len(metas) == 1, item
    meta = json.loads(metas[0].read_text(encoding="utf-8"))
    sdir = metas[0].with_suffix("")
    title = (meta.get("title") or "Cowork session").strip()
    created = ts(meta["createdAt"])
    last = ts(meta.get("lastActivityAt") or meta["createdAt"])
    events = []
    for j in (sdir / ".claude" / "projects").rglob("*.jsonl"):
        for line in j.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("type") not in ("user", "assistant") or e.get("isSidechain") or e.get("isMeta"):
                continue
            body = render((e.get("message") or {}).get("content"), e["type"])
            if body:
                events.append((e.get("timestamp") or "", e["type"], body))
    events.sort(key=lambda x: x[0])
    dest = Path(item["dest"])
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f"{created:%Y-%m-%d}-cowork-{slugify(title)}{item.get('suffix', '')}.md"
    if path.exists():
        raise SystemExit(f"refusing to overwrite {path}")
    first_user = next((b for _, r, b in events if r == "user"), "")
    summary = re.sub(r"\s+", " ", first_user)[:250]
    lines = [
        "---",
        f"title: {yaml_str(title)}",
        f"source: \"claude-desktop-cowork:{sdir.name}\"",
        "type: notes",
        f"ingested: {TODAY}",
        f"tags: [{', '.join(['cowork-session'] + item.get('tags', []))}]",
        f"summary: {yaml_str('Cowork session. Opening request: ' + summary)}",
        f"authors: [{os.environ.get('WIKI_KIT_AUTHOR', 'unknown')}, Claude]",
        f"source_date: {created:%Y-%m-%d}",
        f"source_updated: {last:%Y-%m-%d}",
        "---",
        "",
        f"# {title}",
        "",
        f"> Claude Desktop Cowork session `{sdir.name}`, {created:%Y-%m-%d} to {last:%Y-%m-%d}. "
        "Tool results and system reminders are omitted.",
    ]
    if item.get("files_note"):
        lines += ["", f"> Session files (uploads and outputs): {item['files_note']}"]
    lines += ["", "## Transcript", ""]
    for stamp, role, body in events:
        who = "User" if role == "user" else "Claude"
        lines += [f"### {who} — {stamp[:16].replace('T', ' ')}", "", body, ""]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    written.append(f"{len(events)}\t{path}")

print("\n".join(written))
