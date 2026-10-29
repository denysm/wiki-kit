"""Move files into a destination tree, logging every action.

Usage: move_tree.py <log.tsv> <dest_dir> <src> [<src> ...]
A src directory moves its contents (relative layout kept); a src file moves
into dest_dir. Same name + same content: source removed (dup). Same name +
different content: moved as <stem>-<tag><ext>. Skips .DS_Store.
Log columns: action, source, destination.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

log_path, dest_root, srcs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
TAG = os.environ.get("MOVE_TAG", "moved")


def digest(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


pairs = []
for s in map(Path, srcs):
    if s.is_dir():
        pairs += [(f, dest_root / f.relative_to(s)) for f in sorted(s.rglob("*")) if f.is_file()]
    elif s.is_file():
        pairs.append((s, dest_root / s.name))

counts = {"moved": 0, "dup-removed": 0, "renamed": 0, "skipped": 0}
with log_path.open("a", encoding="utf-8") as log:
    for src, dst in pairs:
        if src.name == ".DS_Store":
            src.unlink()
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            if digest(src) == digest(dst):
                src.unlink()
                log.write(f"dup-removed\t{src}\t{dst}\n")
                counts["dup-removed"] += 1
                continue
            alt = dst.with_name(f"{dst.stem}-{TAG}{dst.suffix}")
            if alt.exists():
                log.write(f"skipped\t{src}\t{alt}\n")
                counts["skipped"] += 1
                continue
            dst, action = alt, "renamed"
        else:
            action = "moved"
        shutil.move(str(src), str(dst))
        log.write(f"{action}\t{src}\t{dst}\n")
        counts[action] += 1
    # remove now-empty source directories
    for s in map(Path, srcs):
        if s.is_dir():
            for d in sorted((p for p in s.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                if not any(d.iterdir()):
                    d.rmdir()
            if not any(s.iterdir()):
                s.rmdir()

print(counts)
