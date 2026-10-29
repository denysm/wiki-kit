"""Copy the kit's specialists into a hub's .skills/, keeping the hub's own tuning.

Usage: sync_specialists.py [HUB] [--only NAME ...] [--dry-run | --check]

HUB defaults to hub_path in ~/.config/llm-wiki/config.json. The llm-wiki
validator refuses symlinks in .skills/, so the hub holds a copy; treat it as a
cache of the kit: this script keeps it identical, the department skill runs it
before every specialist call, and the kit's hooks/ run it after commit, merge
and checkout (`git config core.hooksPath hooks`). --check changes nothing and
exits 1 if the copy differs. For each specialists/<name>/
of the kit: new or changed core files are copied, core files no longer in the
kit are removed, and the hub's references/*.local.md files are never touched.
Hub specialists that are not in the kit (your personal ones) are left alone.
Enabling a specialist for a topic stays a separate step (`llm-wiki specialist enable`).
"""
import argparse
import filecmp
import json
import shutil
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "specialists"
CONFIG = Path("~/.config/llm-wiki/config.json").expanduser()


def core_files(root: Path) -> set:
    return {p.relative_to(root) for p in root.rglob("*")
            if p.is_file() and p.name != ".DS_Store" and not p.name.endswith(".local.md")}


ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("hub", type=Path, nargs="?", help="hub root (default: hub_path from llm-wiki config)")
ap.add_argument("--only", nargs="+", metavar="NAME", help="sync just these specialists")
mode = ap.add_mutually_exclusive_group()
mode.add_argument("--dry-run", action="store_true", help="print what would change")
mode.add_argument("--check", action="store_true", help="like --dry-run, exit 1 if anything differs")
args = ap.parse_args()
args.dry_run = args.dry_run or args.check

if args.hub is None:
    if not CONFIG.is_file():
        raise SystemExit(f"no HUB given and no {CONFIG}")
    args.hub = Path(json.loads(CONFIG.read_text(encoding="utf-8"))["hub_path"])
skills = args.hub.expanduser() / ".skills"
if not skills.is_dir():
    raise SystemExit(f"no .skills/ in {args.hub} (run `llm-wiki specialist init` first)")
names = args.only or sorted(d.name for d in KIT.iterdir() if d.is_dir())
counts = {"added": 0, "updated": 0, "removed": 0, "same": 0}
for name in names:
    src, dst = KIT / name, skills / name
    if not src.is_dir():
        raise SystemExit(f"not a kit specialist: {name}")
    if dst.is_symlink():
        raise SystemExit(f"{dst} is a symlink; the validator refuses it, remove it first")
    have = core_files(dst) if dst.is_dir() else set()
    for rel in sorted(core_files(src)):
        action = "updated" if rel in have else "added"
        if rel in have and filecmp.cmp(src / rel, dst / rel, shallow=False):
            counts["same"] += 1
            continue
        counts[action] += 1
        print(f"{action}\t{name}/{rel}")
        if not args.dry_run:
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src / rel, dst / rel)
    for rel in sorted(have - core_files(src)):
        counts["removed"] += 1
        print(f"removed\t{name}/{rel}")
        if not args.dry_run:
            (dst / rel).unlink()
print(("dry run: " if args.dry_run else "") + ", ".join(f"{k} {v}" for k, v in counts.items()))
if args.check and counts["added"] + counts["updated"] + counts["removed"]:
    raise SystemExit(1)
