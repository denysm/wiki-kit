#!/usr/bin/env bash
# Install wiki-kit on macOS or Linux: the llm-wiki plugin, an empty hub, the
# specialists and the front desk, then a self-check. Safe to run again: it only
# adds what is missing and never overwrites your files.
#
# Usage: bash bootstrap.sh [--hub DIR] [--lang en|ru|uk] [--no-plugin]
#   --hub DIR    where your wiki lives (default: hub_path from
#                ~/.config/llm-wiki/config.json, else ~/wiki)
#   --lang       language of the hub rules and of the chat (default: from $LANG)
#   --no-plugin  skip the Claude Code plugin step (offline, or no Claude Code yet)
# Environment: WIKI_KIT_DIR (where to clone the kit, default ~/Projects/wiki-kit),
# WIKI_KIT_REPO (the kit's git address; needed only when this file runs outside a kit).
set -eu

PLUGIN_REPO="https://github.com/nvk/llm-wiki.git#v0.25.1"
PLUGIN_ID="wiki@llm-wiki"
HUB=""
LANG_CODE=""
NO_PLUGIN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --hub) HUB="$2"; shift 2 ;;
    --lang) LANG_CODE="$2"; shift 2 ;;
    --no-plugin) NO_PLUGIN=1; shift ;;
    -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

ok=0; warn=0; fail=0
say()  { printf '%s\n' "$*"; }
good() { ok=$((ok + 1)); printf '  ok    %s\n' "$*"; }
note() { warn=$((warn + 1)); printf '  note  %s\n' "$*"; }
bad()  { fail=$((fail + 1)); printf '  FAIL  %s\n' "$*"; }

say "== 1/7 Tools on this computer"
command -v git >/dev/null || { bad "git is missing. macOS: run 'xcode-select --install'. Linux: install the 'git' package. Then run this again."; exit 1; }
good "git $(git --version | awk '{print $3}')"
command -v python3 >/dev/null || { bad "python3 is missing. macOS: run 'xcode-select --install'. Linux: install 'python3'. Then run this again."; exit 1; }
python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' || { bad "python3 is older than 3.9; install a newer one and run this again."; exit 1; }
good "python3 $(python3 -c 'import platform; print(platform.python_version())')"
HAS_CLAUDE=0
if command -v claude >/dev/null; then HAS_CLAUDE=1; good "Claude Code $(claude --version 2>/dev/null | awk '{print $1}')"
else note "Claude Code command line not found: install it with 'curl -fsSL https://claude.ai/install.sh | bash' (the VS Code extension alone has no 'claude' command), then run this again for the plugin step."; fi

say "== 2/7 The kit"
here=$(cd "$(dirname "$0")" 2>/dev/null && pwd || true)
if [ -n "$here" ] && [ -f "$here/scripts/leak_check.py" ]; then
  KIT="$here"; good "using the kit at $KIT"
else
  KIT="${WIKI_KIT_DIR:-$HOME/Projects/wiki-kit}"
  if [ -d "$KIT/.git" ]; then git -C "$KIT" pull -q --ff-only && good "updated $KIT"
  else
    [ -n "${WIKI_KIT_REPO:-}" ] || { bad "no kit here: clone it first (git clone <address you were sent> ~/Projects/wiki-kit) or set WIKI_KIT_REPO"; exit 1; }
    mkdir -p "$(dirname "$KIT")"; git clone -q "$WIKI_KIT_REPO" "$KIT" && good "cloned into $KIT"
  fi
fi
git -C "$KIT" config core.hooksPath hooks && good "kit hooks on (leak check before push, specialists re-sync)"

say "== 3/7 The llm-wiki plugin ($PLUGIN_ID, pinned to v0.25.1)"
if [ "$NO_PLUGIN" = 1 ] || [ "$HAS_CLAUDE" = 0 ]; then note "skipped"
elif claude plugin list --json 2>/dev/null | grep -q "\"$PLUGIN_ID\""; then good "already installed"
else
  claude plugin marketplace list 2>/dev/null | grep -q "llm-wiki" || claude plugin marketplace add "$PLUGIN_REPO" >/dev/null
  claude plugin install "$PLUGIN_ID" >/dev/null && good "installed" || bad "plugin install failed: run 'claude plugin install $PLUGIN_ID' and read the message"
fi

say "== 4/7 Your hub (the folder with your wikis)"
CONFIG="$HOME/.config/llm-wiki/config.json"
if [ -z "$HUB" ] && [ -f "$CONFIG" ]; then
  HUB=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1])).get("hub_path",""))' "$CONFIG")
fi
HUB="${HUB:-$HOME/wiki}"
HUB="${HUB/#\~/$HOME}"
if [ ! -f "$CONFIG" ]; then
  mkdir -p "$(dirname "$CONFIG")"
  python3 -I -c 'import json,sys; json.dump({"hub_path": sys.argv[1]}, open(sys.argv[2], "w"))' "$HUB" "$CONFIG"
  good "hub path saved in $CONFIG"
fi
if [ -z "$LANG_CODE" ]; then case "${LANG:-}" in ru*) LANG_CODE=ru ;; uk*) LANG_CODE=uk ;; *) LANG_CODE=en ;; esac; fi
case "$LANG_CODE" in ru) LANGUAGE=Russian ;; uk) LANGUAGE=Ukrainian ;; *) LANGUAGE=English ;; esac
if [ -f "$HUB/_index.md" ]; then
  good "hub exists at $HUB (left as it is)"
else
  mkdir -p "$HUB/topics"
  today=$(date +%Y-%m-%d)
  [ -f "$HUB/wikis.json" ] || cat > "$HUB/wikis.json" <<EOF
{
  "default": "<HUB>",
  "wikis": {
    "hub": {"path": "<HUB>", "description": "Personal knowledge hub"}
  },
  "local_wikis": []
}
EOF
  cat > "$HUB/_index.md" <<EOF
# Wiki Hub

> Personal knowledge base. Content lives in topic wikis.

Last updated: $today

## Topic Wikis

| Topic | Description | Sources | Articles |
|-------|-------------|---------|----------|

## Recent Changes

- $today: Hub initialized (wiki-kit bootstrap.sh)
EOF
  [ -f "$HUB/log.md" ] || printf '# Wiki Activity Log\n\n## [%s] init | Hub initialized by wiki-kit bootstrap.sh\n' "$today" > "$HUB/log.md"
  [ -f "$HUB/CLAUDE.md" ] || sed -e "s/{HUB_NAME}/My wiki/" -e "s/{WIKI_LANGUAGE}/$LANGUAGE/" -e "s/{CHAT_LANGUAGE}/$LANGUAGE/" \
    "$KIT/templates/hub-CLAUDE.md" > "$HUB/CLAUDE.md"
  [ -f "$HUB/README.md" ] || printf '# State and plan\n\nUpdated: %s. Empty hub created by wiki-kit bootstrap.sh. Next: create the first topic with `/wiki init <topic>`.\n' "$today" > "$HUB/README.md"
  [ -f "$HUB/.gitignore" ] || cat > "$HUB/.gitignore" <<'EOF'
.DS_Store
# files that must not leave this computer
*.local.md
.sessions/
inbox/.processed/
# kit specialists in .skills/ are a cache of wiki-kit (sync_specialists.py);
# only your own tuning (*.local.md) is history of this hub
.skills/*/SKILL.md
.skills/*/references/*
!.skills/*/references/*.local.md
EOF
  good "empty hub created at $HUB (rules in $LANGUAGE)"
fi
if [ ! -d "$HUB/.git" ]; then
  git -C "$HUB" init -q && good "hub is a git repository (local only, no remote; the first commit comes with your first topic)"
fi

say "== 5/7 Private lists (outside every repository)"
CFG="$HOME/.config/wiki-kit"
mkdir -p "$CFG"; chmod 700 "$CFG"
[ -f "$CFG/private-names.txt" ] || { printf '# Names that must never reach the kit: your family, employer, clients.\n# One case-insensitive regex per line, for example: Acme Corp\n' > "$CFG/private-names.txt"; chmod 600 "$CFG/private-names.txt"; }
[ -f "$CFG/internal-domains.txt" ] || { printf '# Internal host suffixes of your employer or clients, one per line, for example: corp.example.com\n' > "$CFG/internal-domains.txt"; chmod 600 "$CFG/internal-domains.txt"; }
good "$CFG (fill private-names.txt before your first push to the kit)"

say "== 6/7 Specialists and the front desk"
LLM_WIKI=$(ls -d "$HOME"/.claude/plugins/cache/llm-wiki/wiki/*/bin/llm-wiki 2>/dev/null | tail -1 || true)
lw() { python3 -I "$LLM_WIKI" specialist --hub "$HUB" "$@" >/dev/null 2>&1; }
if [ -n "$LLM_WIKI" ]; then
  [ -d "$HUB/.skills" ] || lw init
  python3 -I "$KIT/scripts/sync_specialists.py" "$HUB" | tail -1 | sed 's/^/  ok    specialists: /'
  lw refresh || true
else note "specialists wait for the plugin: run this again after step 3 succeeds"; fi
mkdir -p "$HOME/.claude/skills"
if [ -e "$HOME/.claude/skills/department" ]; then good "front desk skill already present"
else ln -s "$KIT/skills/department" "$HOME/.claude/skills/department" && good "front desk skill linked (say 'coach' or 'help me decide' in any folder)"; fi

say "== 7/7 Self-check"
broken=$(python3 -I -c 'import sys
for f in sys.argv[1:]:
    try: compile(open(f, encoding="utf-8").read(), f, "exec")
    except SyntaxError: print(f.rsplit("/", 1)[-1], end=" ")' "$KIT"/scripts/*.py)
[ -z "$broken" ] && good "all scripts compile on this python3" || bad "scripts that need a newer python3: $broken"
if [ -d "$HUB/.skills" ]; then
  python3 -I "$KIT/scripts/sync_specialists.py" "$HUB" --check >/dev/null && good "hub specialists match the kit" || bad "hub specialists differ from the kit"
  lw validate && good "specialists pass the plugin validator" || bad "plugin validator: run 'python3 -I $LLM_WIKI specialist --hub $HUB validate'"
fi
python3 -I "$KIT/scripts/leak_check.py" --repo "$KIT" >/dev/null 2>&1 && good "kit passes the leak check" || bad "kit fails the leak check: run python3 -I $KIT/scripts/leak_check.py --repo $KIT"
say ""
say "Done: $ok ok, $warn note(s), $fail failure(s). Hub: $HUB"
say "Next: open the hub folder in VS Code, start Claude Code, sign in, and type:  /wiki init personal"
say "Guide: $KIT/docs/QUICKSTART.md (English), $KIT/docs/QUICKSTART.ru.md (Russian), $KIT/docs/QUICKSTART.uk.md (Ukrainian)"
[ "$fail" -eq 0 ]
