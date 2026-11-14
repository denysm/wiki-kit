"""Copy the kit's specialists into a hub's .skills/, keeping the hub's own tuning.

Usage: sync_specialists.py [HUB] [--only NAME ...] [--index] [--dry-run | --check]

HUB defaults to the path in ~/.config/wiki-kit/specialists-hub, else hub_path
in ~/.config/llm-wiki/config.json. Set the first when the llm-wiki hub of this
machine must not get your specialists (for example a work hub next to a
personal one). The llm-wiki
validator refuses symlinks in .skills/, so the hub holds a copy; treat it as a
cache of the kit: this script keeps it identical, the department skill runs it
before every specialist call, and the kit's hooks/ run it after commit, merge
and checkout (`git config core.hooksPath hooks`). --check changes nothing and
exits 1 if the copy differs. For each specialists/<name>/
of the kit: new or changed core files are copied, core files no longer in the
kit are removed, and the hub's references/*.local.md files are never touched.
Hub specialists that are not in the kit (your personal ones) are left alone.
Enabling a specialist for a topic stays a separate step (`llm-wiki specialist enable`).
After copying or removing anything it rebuilds the hub's .skills/_index.md (it
lists versions) with the llm-wiki plugin; --index rebuilds it even when nothing
was copied (the installers use it). When only the index date would change, the
index and log.md are put back as they were, so a run that changes nothing leaves
the hub's git tree clean.
"""
import argparse
import filecmp
import json
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "specialists"
CONFIG = Path("~/.config/llm-wiki/config.json").expanduser()
SPEC_HUB = Path("~/.config/wiki-kit/specialists-hub").expanduser()


def core_files(root: Path) -> set:
    return {p.relative_to(root) for p in root.rglob("*")
            if p.is_file() and p.name != ".DS_Store" and not p.name.endswith(".local.md")}


def plugin_cli():
    """The llm-wiki command of the newest plugin version in the Claude Code cache, or None."""
    def version(p):
        return tuple(int(x) if x.isdigit() else -1 for x in p.parent.parent.name.split("."))
    found = sorted(Path.home().glob(".claude/plugins/cache/llm-wiki/wiki/*/bin/llm-wiki"), key=version)
    return found[-1] if found else None


def refresh_index(hub: Path) -> str:
    """Rebuild .skills/_index.md; put it and log.md back when only the date would change."""
    cli = plugin_cli()
    if cli is None:
        return "not rebuilt (no llm-wiki plugin)"
    index, log = hub / ".skills" / "_index.md", hub / "log.md"
    old_index = index.read_bytes() if index.is_file() else None
    old_log = log.read_bytes() if log.is_file() else None
    run = subprocess.run([sys.executable, "-I", str(cli), "specialist", "--hub", str(hub), "refresh"],
                         capture_output=True, encoding="utf-8", errors="replace")
    if run.returncode:
        why = (run.stderr or run.stdout).strip().splitlines() or ["failed"]
        return f"not rebuilt (llm-wiki: {why[-1]})"

    def body(data: bytes) -> list:
        return [line for line in data.splitlines() if not line.startswith(b"Last updated:")]

    if old_index is not None and index.is_file() and body(old_index) == body(index.read_bytes()):
        index.write_bytes(old_index)
        if old_log is None:
            log.unlink(missing_ok=True)
        else:
            log.write_bytes(old_log)
        return "up to date"
    return "rebuilt"


ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("hub", type=Path, nargs="?", help="hub root (default: specialists-hub, else hub_path)")
ap.add_argument("--only", nargs="+", metavar="NAME", help="sync just these specialists")
ap.add_argument("--index", action="store_true",
                help="rebuild .skills/_index.md even when nothing was copied (it is rebuilt after any change)")
mode = ap.add_mutually_exclusive_group()
mode.add_argument("--dry-run", action="store_true", help="print what would change")
mode.add_argument("--check", action="store_true", help="like --dry-run, exit 1 if anything differs")
args = ap.parse_args()
args.dry_run = args.dry_run or args.check

if args.hub is None and SPEC_HUB.is_file():
    args.hub = Path(SPEC_HUB.read_text(encoding="utf-8").strip())
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
changed = counts["added"] + counts["updated"] + counts["removed"]
summary = ("dry run: " if args.dry_run else "") + ", ".join(f"{k} {v}" for k, v in counts.items())
if not args.dry_run and (changed or args.index):
    summary += "; index " + refresh_index(args.hub.expanduser())
print(summary)
if args.check and changed:
    raise SystemExit(1)
