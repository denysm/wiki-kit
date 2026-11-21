#!/usr/bin/env python3
"""Compare catalog cards with upstream: latest release, licence, last push, archived. Prints only.

Usage:
  catalog_fresh.py CARD ...        given cards (catalog/wiki/references/<owner>-<repo>.md)
  catalog_fresh.py --all [CATALOG] every card of the catalog (default: the kit's catalog/)

Per card it takes `repo`, `version`, `licence` and `desk_checked` from the
frontmatter. A GitHub `repo` is checked with the `gh` CLI (`gh api
repos/OWNER/NAME` and `.../releases/latest`, falling back to the newest tag); a
Hugging Face `url` with the public model API; any other `url` prints "check by
hand". One line per difference:

  version in card vs latest release or tag
  licence in card vs the one upstream reports (NOASSERTION: read the licence file)
  pushed (or modified) after desk_checked
  archived

It never edits a card: a new version of an `in use` part needs a new desk
check, which is agent work (docs/catalog-design.md, "Freshness check").
Exit 0 no differences, 1 differences, 2 error. Stdlib plus the `gh` CLI.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent


def front(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    out = {}
    if not lines or lines[0].strip() != "---":
        return out
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            if " #" in v and not v.startswith(('"', "'")):
                v = v.split(" #", 1)[0].rstrip()
            out[m.group(1)] = v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'" else v
    return out


def gh(path: str):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        if "404" in r.stderr or "Not Found" in r.stderr:
            return None
        raise RuntimeError(f"gh api {path}: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout)


def bare(v: str) -> str:
    return re.sub(r"^v(?=\d)", "", (v or "").strip())


def same_licence(card: str, up: str) -> bool:
    a, b = card.strip().lower(), up.strip().lower()
    return a == b or a.startswith(b + "-") or b.startswith(a + "-")


def check_github(fm: dict) -> list[str]:
    repo = fm["repo"]
    info = gh(f"repos/{repo}")
    if info is None:
        return [f"repository not found on GitHub: {repo}"]
    diffs = []
    if info.get("full_name", "").lower() != repo.lower():
        diffs.append(f"moved: {repo} is now {info.get('full_name')}")
    rel = gh(f"repos/{repo}/releases/latest")
    if rel:
        latest, when = rel.get("tag_name", ""), (rel.get("published_at") or "")[:10]
    else:
        tags = gh(f"repos/{repo}/tags?per_page=1") or []
        latest, when = (tags[0]["name"], "tag") if tags else ("", "")
    if latest and fm.get("version") and bare(latest) != bare(fm["version"]):
        diffs.append(f"version: card {fm['version']}, upstream {latest} ({when})")
    lic = ((info.get("license") or {}).get("spdx_id")) or "none"
    if lic == "NOASSERTION":
        diffs.append(f"licence: GitHub reports NOASSERTION; card says {fm.get('licence', '?')}: read the licence file")
    elif fm.get("licence") and not same_licence(fm["licence"], lic):
        diffs.append(f"licence: card {fm['licence']}, GitHub {lic}")
    pushed = (info.get("pushed_at") or "")[:10]
    if pushed and fm.get("desk_checked") and pushed > fm["desk_checked"]:
        diffs.append(f"pushed {pushed}, after the desk check of {fm['desk_checked']}")
    if info.get("archived"):
        diffs.append("archived upstream")
    return diffs


def check_hf(fm: dict, model: str) -> list[str]:
    try:
        with urllib.request.urlopen(f"https://huggingface.co/api/models/{model}", timeout=20) as r:
            info = json.load(r)
    except urllib.error.HTTPError as e:
        return [f"Hugging Face model not found: {model}"] if e.code == 404 else [f"Hugging Face API error {e.code}"]
    diffs = []
    lic = next((t.split(":", 1)[1] for t in info.get("tags", []) if t.startswith("license:")), "")
    if lic and fm.get("licence") and not same_licence(fm["licence"], lic):
        diffs.append(f"licence: card {fm['licence']}, Hugging Face {lic}")
    mod = (info.get("lastModified") or "")[:10]
    if mod and fm.get("desk_checked") and mod > fm["desk_checked"]:
        diffs.append(f"modified {mod}, after the desk check of {fm['desk_checked']}")
    if info.get("sha") and fm.get("version") and fm["version"] not in (info["sha"], info["sha"][:7]) \
            and re.fullmatch(r"[0-9a-f]{7,40}", fm["version"]):
        diffs.append(f"version: card {fm['version']}, Hugging Face revision {info['sha'][:7]}")
    return diffs


def check(card: Path) -> tuple[list[str], bool]:
    fm = front(card)
    if fm.get("repo"):
        return check_github(fm), True
    url = fm.get("url", "")
    m = re.match(r"https://huggingface\.co/([^/]+/[^/?#]+)", url)
    if m:
        return check_hf(fm, m.group(1)), True
    return [f"not on GitHub or Hugging Face ({url or 'no url'}): check by hand"], False


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cards", nargs="*", type=Path)
    ap.add_argument("--all", nargs="?", const=KIT / "catalog", type=Path, metavar="CATALOG")
    args = ap.parse_args(argv)
    cards = list(args.cards)
    if args.all:
        cards += sorted(p for p in (args.all / "wiki" / "references").glob("*.md") if p.name != "_index.md")
    if not cards:
        ap.error("give cards or --all")
    found = error = False
    for c in cards:
        try:
            diffs, _ = check(c)
        except (RuntimeError, OSError, ValueError) as e:
            print(f"{c.name}: error: {e}")
            error = True
            continue
        for d in diffs:
            print(f"{c.name}: {d}")
        found = found or bool(diffs)
        if not diffs:
            print(f"{c.name}: up to date")
    return 2 if error else 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
