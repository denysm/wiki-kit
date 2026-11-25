#!/bin/sh
# Tests for the retired-history rule of leak_check.py (.leak-retired), on a throwaway repository.
# Usage: scripts/test_leak_retired.sh   (PY=python3.9 to pick the interpreter; CI passes PY=python)
set -eu
here=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-python3}
t=$(mktemp -d)
trap 'rm -rf "$t"' EXIT
r="$t/r"
fail=0
g() { git -C "$r" -c user.name=t -c user.email=t@example.invalid -c init.defaultBranch=main "$@"; }
at() { GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1"; export GIT_AUTHOR_DATE GIT_COMMITTER_DATE; }
lc() { "$PY" -I "$here/leak_check.py" --repo "$r" --names /dev/null "$@" > "$t/out" 2>&1; }
refused() {  # a refusal is exit 1 with the checker's verdict line, never a crash
  name=$1; shift
  if lc "$@"; then echo "FAIL (should be refused): $name"; fail=1
  elif ! grep -q '^leak check: .* problem(s)$' "$t/out"; then echo "FAIL (no verdict, crashed?): $name"; cat "$t/out"; fail=1; fi
}
passes() { name=$1; shift; if ! lc "$@"; then echo "FAIL (should pass): $name"; cat "$t/out"; fail=1; fi; }
says() { name=$1; shift; if ! grep -q "$1" "$t/out"; then echo "FAIL (no '$1' in output): $name"; cat "$t/out"; fail=1; fi; }
fp() { printf '%s' "$1" | "$PY" -I -c 'import hashlib, sys; print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest()[:24])'; }

mkdir "$r"; g init -q
# the old history: a file and a line that the rewrite drops
mkdir "$r/d"; echo "old plan" > "$r/d/gone.md"; printf 'keep\n  a dropped line here\n' > "$r/card.md"
g add -A; at 2026-01-01T00:00:00Z; g commit -q -m old; g branch old
# the rewritten history, then .leak-retired in a commit of its own
g checkout -q --orphan main2; g rm -rq --cached .; rm -rf "$r/d"; printf 'keep\n' > "$r/card.md"
g add card.md; g commit -q -m rewritten
{ echo "# throwaway test"; echo "before 2026-01-02T00:00:00+00:00"
  echo "path $(fp d/gone.md)"; echo "line $(fp 'a dropped line here')"; } > "$r/.leak-retired"
g add -A; at 2026-01-03T00:00:00Z; g commit -q -m retired; base=$(g rev-parse HEAD)

passes "the rewritten history, whole" --history
passes "the rewritten history over its base" --history --base "$base"

# a merge of the old history: old commits by date, their files and lines by fingerprint
g checkout -q -b merged "$base"; at 2026-01-04T00:00:00Z; g merge -q -s ours --allow-unrelated-histories -m merge old
refused "merge of the old history" --history --base "$base"
says "the merge is refused by date" "authored before 2026-01-02"

# the old branch pushed as a new branch: REV has no .leak-retired, the base has it
g checkout -q old
refused "old branch, rule read from the base" --history --base "$base"
says "the old branch's dropped file is found in its tree" "path dropped from this history"

# re-authored content after the cutoff (a soft reset and a new commit), and a re-indented line
g checkout -q -b soft "$base"; mkdir -p "$r/d"; echo "old plan" > "$r/d/gone.md"; printf 'keep\n\t a dropped line here  \n' > "$r/card.md"
g add -A; at 2026-01-05T00:00:00Z; g commit -q -m "new work"
refused "re-authored dropped file and line" --history --base "$base"
says "a dropped line is found though re-indented" "line dropped from this history"
refused "the same in the tree alone" --rev soft
says "the tree check finds the dropped file" "^d/gone.md: path dropped from this history"

# new work authored after the cutoff passes; an old date is compared only against a base
g checkout -q -b new "$base"; echo fine > "$r/new.md"; g add -A; at 2026-01-06T00:00:00Z; g commit -q -m new
passes "new work" --history --base "$base"
g checkout -q -b olddate "$base"; echo fine > "$r/x.md"; g add -A; at 2026-01-01T12:00:00Z; g commit -q -m x
passes "no base: dates not compared" --history
refused "an old author date over a base" --history --base "$base"
says "the old date is the reason" "authored before 2026-01-02"

# .leak-retired that does not parse is a problem, never a rule turned off
g checkout -q new
for bad in "before: 2026-01-02T00:00:00+00:00" "Before 2026-01-02T00:00:00+00:00" "before 2026-01-02T00:00:00" \
           "path 1234" "line $(fp x)
path $(fp y)"; do
  printf '%s\n' "$bad" > "$r/.leak-retired"
  refused "bad .leak-retired: $bad" --rev new
  says "the bad line is named: $bad" "^.leak-retired: "
done
printf '\357\273\277before 2026-01-02 00:00:00+00:00\n' > "$r/.leak-retired"
passes "a BOM and the space form are read" --rev new
for good in "before 2026-01-02T00:00:00Z" "before 2026-01-02T05:00:00+0500"; do
  printf '%s\n' "$good" > "$r/.leak-retired"
  passes "read on every Python: $good" --rev new
done
g checkout -q -- .leak-retired
# the history is read whatever the pusher's diff settings
g checkout -q soft; g config diff.noprefix true; g config diff.mnemonicPrefix true
refused "dropped line found with diff.noprefix" --history --base "$base"
says "the line hash still matches under diff.noprefix" "commit .* line dropped from this history"
g config --unset diff.noprefix; g config --unset diff.mnemonicPrefix; g checkout -q new

# dropped paths with a space, a quote or non-ASCII letters, re-added and deleted again within one push
g checkout -q -b paths "$base"
{ cat "$r/.leak-retired"; for f in 'sp ace/a b.md' 'q"uote.md' 'я.md' d/gone.png d/empty.md; do echo "path $(fp "$f")"; done; } > "$t/lr"
cp "$t/lr" "$r/.leak-retired"; g add -A; at 2026-01-03T01:00:00Z; g commit -q -m "more paths"; pbase=$(g rev-parse HEAD)
for f in "sp ace/a b.md" 'q"uote.md' "я.md"; do
  mkdir -p "$r/$(dirname "$f")"; echo x > "$r/$f"; g add -A; at 2026-01-07T00:00:00Z; g commit -q -m add
  g rm -q "$f"; g commit -q -m del
  refused "a dropped path re-added and deleted: $f" --history --base "$pbase"
  says "found in history: $f" "^commit .* path dropped from this history"
  g reset -q --hard "$pbase"
done
# a binary file and an empty file have no `+++` line in the diff
mkdir -p "$r/d"; printf 'PNG\000\001' > "$r/d/gone.png"; : > "$r/d/empty.md"; g add -A; at 2026-01-07T00:00:00Z; g commit -q -m bin
g rm -q d/gone.png d/empty.md; g commit -q -m del
refused "a binary and an empty file at dropped paths, re-added and deleted" --history --base "$pbase"
says "the binary file is found" "^commit .* d/gone.png: path dropped from this history"
says "the empty file is found" "^commit .* d/empty.md: path dropped from this history"
g reset -q --hard "$pbase"
# a rename into a dropped path and back (rename detection must not hide it)
g checkout -q -b ren "$base"; mkdir -p "$r/d"; at 2026-01-08T00:00:00Z
g mv card.md d/gone.md; g commit -q -m ren; g mv d/gone.md card.md; g commit -q -m back
refused "a rename into a dropped path and back" --history --base "$base"
says "the renamed path is found" "^commit .* path dropped from this history"
# an added line that reads like a file header must not end the file's lines
g checkout -q -b hdr "$base"; printf '++ /dev/null\na dropped line here\n' > "$r/x.md"; g add -A; at 2026-01-09T00:00:00Z; g commit -q -m hdr
g rm -q x.md; g commit -q -m gone
refused "a dropped line after a header-like line" --history --base "$base"
says "the line after it is found" "^commit .* line dropped from this history"
# the root commit's diff is read whatever log.showRoot says (whole-history mode, no base)
g checkout -q old; g config log.showRoot false; cp "$t/lr" "$r/.leak-retired"   # the rule from the working copy
refused "the old root commit, whole history" --history
says "the root commit's dropped path is found" "^commit .* path dropped from this history"
rm "$r/.leak-retired"; g config --unset log.showRoot; g checkout -q new

if [ "$fail" -ne 0 ]; then exit 1; fi
echo "retired-history tests passed"
