#!/usr/bin/env bash
# Install wiki-kit on macOS or Linux: the llm-wiki plugin, an empty hub, the
# specialists, the front desk and the foreman, a self-check, then search by meaning:
# Ollama (asks first) and a small local model. Safe to run again: it only adds what is
# missing and never overwrites your files.
# Usage: bash bootstrap.sh [--hub DIR] [--lang en|ru|uk] [--no-plugin] [--yes] [--no-vectors]
#   --hub DIR     where your wiki lives and the specialists go (default: hub_path from
#                 ~/.config/llm-wiki/config.json, else ~/wiki; the specialists go to
#                 ~/.config/wiki-kit/specialists-hub instead when that file exists)
#   --lang        language of the hub rules and of the chat (default: from $LANG)
#   --no-plugin   skip the Claude Code plugin step (offline, or no Claude Code yet)
#   --yes         install Ollama without asking (without a terminal and without --yes it is skipped)
#   --no-vectors  skip search by meaning (no Ollama, no model download)
# Environment: WIKI_KIT_DIR (where to clone the kit, default ~/Projects/wiki-kit),
# WIKI_KIT_REPO (the kit's git address; needed only when this file runs outside a kit).
set -eu

PLUGIN_REPO="https://github.com/nvk/llm-wiki.git#v1.0.0"
PLUGIN_ID="wiki@llm-wiki"
HUB=""
HUB_GIVEN=0
LANG_CODE=""
NO_PLUGIN=0
YES=0
NO_VECTORS=0
while [ $# -gt 0 ]; do
  case "$1" in
    --hub) HUB="$2"; HUB_GIVEN=1; shift 2 ;;
    --lang) LANG_CODE="$2"; shift 2 ;;
    --no-plugin) NO_PLUGIN=1; shift ;;
    --yes|-y) YES=1; shift ;;
    --no-vectors) NO_VECTORS=1; shift ;;
    -h|--help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

ok=0; warn=0; fail=0
say()  { printf '%s\n' "$*"; }
good() { ok=$((ok + 1)); printf '  ok    %s\n' "$*"; }
note() { warn=$((warn + 1)); printf '  note  %s\n' "$*"; }
bad()  { fail=$((fail + 1)); printf '  FAIL  %s\n' "$*"; }

say "== 1/8 Tools on this computer"
command -v git >/dev/null || { bad "git is missing. macOS: run 'xcode-select --install'. Linux: install the 'git' package. Then run this again."; exit 1; }
good "git $(git --version | awk '{print $3}')"
command -v python3 >/dev/null || { bad "python3 is missing. macOS: run 'xcode-select --install'. Linux: install 'python3'. Then run this again."; exit 1; }
python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' || { bad "python3 is older than 3.9; install a newer one and run this again."; exit 1; }
good "python3 $(python3 -c 'import platform; print(platform.python_version())')"
HAS_CLAUDE=0
if command -v claude >/dev/null; then HAS_CLAUDE=1; good "Claude Code $(claude --version 2>/dev/null | awk '{print $1}')"
else note "Claude Code command line not found: install it with 'curl -fsSL https://claude.ai/install.sh | bash' (the VS Code extension alone has no 'claude' command), then run this again for the plugin step."; fi

say "== 2/8 The kit"
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

say "== 3/8 The llm-wiki plugin ($PLUGIN_ID, pinned to v1.0.0)"
if [ "$NO_PLUGIN" = 1 ] || [ "$HAS_CLAUDE" = 0 ]; then note "skipped"
elif claude plugin list --json 2>/dev/null | grep -q "\"$PLUGIN_ID\""; then good "already installed"
else
  claude plugin marketplace list 2>/dev/null | grep -q "llm-wiki" || claude plugin marketplace add "$PLUGIN_REPO" >/dev/null
  claude plugin install "$PLUGIN_ID" >/dev/null && good "installed" || bad "plugin install failed: run 'claude plugin install $PLUGIN_ID' and read the message"
fi

say "== 4/8 Your hub (the folder with your wikis)"
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

say "== 5/8 Private lists (outside every repository)"
CFG="$HOME/.config/wiki-kit"
mkdir -p "$CFG"; chmod 700 "$CFG"
[ -f "$CFG/private-names.txt" ] || { printf '# Names that must never reach the kit: your family, employer, clients.\n# One case-insensitive regex per line, for example: Acme Corp\n' > "$CFG/private-names.txt"; chmod 600 "$CFG/private-names.txt"; }
[ -f "$CFG/internal-domains.txt" ] || { printf '# Internal host suffixes of your employer or clients, one per line, for example: corp.example.com\n' > "$CFG/internal-domains.txt"; chmod 600 "$CFG/internal-domains.txt"; }
good "$CFG (fill private-names.txt before your first push to the kit)"

say "== 6/8 Specialists and the front desk"
# The specialists go where the kit's hooks and the front desk send them: --hub when
# given, else the hub named in specialists-hub, else the hub above.
SPEC_FILE="$CFG/specialists-hub"
SPEC_HUB="$HUB"
if [ -f "$SPEC_FILE" ]; then
  spec=$(python3 -I -c 'import os, sys
p = open(sys.argv[1], encoding="utf-8").read().strip()
print(os.path.realpath(os.path.expanduser(p)) if p else "")' "$SPEC_FILE")
  here_hub=$(python3 -I -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$HUB")
  if [ -n "$spec" ] && [ "$spec" != "$here_hub" ]; then
    if [ "$HUB_GIVEN" = 1 ]; then
      note "specialists go to $HUB (--hub), but the kit's hooks and the front desk send them to $spec (from $SPEC_FILE): change or remove that file"
    else SPEC_HUB="$spec"; good "specialists hub: $spec (from $SPEC_FILE; $HUB gets none)"; fi
  fi
fi
LLM_WIKI=$(ls -d "$HOME"/.claude/plugins/cache/llm-wiki/wiki/*/bin/llm-wiki 2>/dev/null | tail -1 || true)
lw() { python3 -I "$LLM_WIKI" specialist --hub "$SPEC_HUB" "$@" >/dev/null 2>&1; }
if [ -z "$LLM_WIKI" ]; then note "specialists wait for the plugin: run this again after step 3 succeeds"
elif [ ! -d "$SPEC_HUB" ]; then note "no folder $SPEC_HUB for the specialists: fix $SPEC_FILE or pass --hub, then run this again"
else
  [ -d "$SPEC_HUB/.skills" ] || lw init
  # --index: rebuild .skills/_index.md when it is stale; a no-op leaves the hub untouched
  if out=$(python3 -I "$KIT/scripts/sync_specialists.py" "$SPEC_HUB" --index 2>&1); then good "specialists: $(printf '%s\n' "$out" | tail -1)"
  else bad "specialists: $(printf '%s\n' "$out" | tail -1)"; fi
fi
mkdir -p "$HOME/.claude/skills"
if [ -e "$HOME/.claude/skills/department" ]; then good "front desk skill already present"
else ln -s "$KIT/skills/department" "$HOME/.claude/skills/department" && good "front desk skill linked (say 'coach' or 'help me decide' in any folder)"; fi
if [ -e "$HOME/.claude/skills/foreman" ]; then good "foreman skill already present"
else ln -s "$KIT/skills/foreman" "$HOME/.claude/skills/foreman" && good "foreman skill linked (say 'assemble a team' or 'work order' in any folder)"; fi

say "== 7/8 Self-check"
broken=$(python3 -I -c 'import sys
for f in sys.argv[1:]:
    try: compile(open(f, encoding="utf-8").read(), f, "exec")
    except SyntaxError: print(f.rsplit("/", 1)[-1], end=" ")' "$KIT"/scripts/*.py)
[ -z "$broken" ] && good "all scripts compile on this python3" || bad "scripts that need a newer python3: $broken"
DEPS_OK=0
deps=$(python3 -I "$KIT/scripts/search.py" install-deps 2>&1) && { DEPS_OK=1; good "python packages: $(printf '%s' "$deps" | tr '\n' ' ')"; } || bad "numpy could not be installed: run 'python3 -I $KIT/scripts/search.py install-deps' and read its message"
if [ -d "$SPEC_HUB/.skills" ]; then
  python3 -I "$KIT/scripts/sync_specialists.py" "$SPEC_HUB" --check >/dev/null && good "hub specialists match the kit" || bad "hub specialists differ from the kit"
  lw validate && good "specialists pass the plugin validator" || bad "plugin validator: run 'python3 -I $LLM_WIKI specialist --hub $SPEC_HUB validate'"
fi
python3 -I "$KIT/scripts/leak_check.py" --repo "$KIT" >/dev/null 2>&1 && good "kit passes the leak check" || bad "kit fails the leak check: run python3 -I $KIT/scripts/leak_check.py --repo $KIT"

say "== 8/8 Search by meaning (Ollama and a small local model; optional)"
# Every failure here is one note line, never a stop: search works on words without the model.
EMBED_MODEL="embeddinggemma-2:270m-q8_0-text"
OLLAMA_API="http://127.0.0.1:11434"
SEARCH_CFG="${WIKI_KIT_SEARCH_CONFIG:-$CFG/search.json}"
ollama_up() { python3 -I -c 'import sys, urllib.request; urllib.request.urlopen(sys.argv[1], timeout=2)' "$OLLAMA_API/api/version" >/dev/null 2>&1; }
ollama_wait() { local i; for i in $(seq "$1"); do ollama_up && return 0; sleep 1; done; ollama_up; }
find_ollama() {
  local i
  OLLAMA_APP=""; OLLAMA_BIN=""
  for i in /Applications/Ollama.app "$HOME/Applications/Ollama.app"; do [ -d "$i" ] && { OLLAMA_APP="$i"; break; }; done
  OLLAMA_BIN=$(command -v ollama 2>/dev/null || true)
  if [ -z "$OLLAMA_BIN" ] && [ -n "$OLLAMA_APP" ] && [ -x "$OLLAMA_APP/Contents/Resources/ollama" ]; then OLLAMA_BIN="$OLLAMA_APP/Contents/Resources/ollama"; fi
  [ -n "$OLLAMA_BIN" ]
}
install_ollama() {
  # the official installer from ollama.com: on macOS the app into /Applications and the
  # ollama command (the Mac may ask for your password); on Linux a service (asks for sudo)
  local how tmp a
  if [ "$(uname -s)" = Darwin ]; then how="the Ollama app into /Applications"; else how="Ollama into /usr/local (needs sudo)"; fi
  if [ "$YES" != 1 ]; then
    [ -t 0 ] || { note "search by meaning is off: Ollama is missing. Run bootstrap again in a terminal (it asks) or with --yes, or install it from https://ollama.com/download"; return 1; }
    printf '        Ollama is missing. Install %s with the official installer from ollama.com? [Y/n] ' "$how"
    read -r a || a=n
    case "$a" in ""|[Yy]*) ;; *) note "search by meaning is off: Ollama not installed (install it from https://ollama.com/download, or run bootstrap again)"; return 1 ;; esac
  fi
  tmp=$(mktemp -d) || return 1
  if ! curl -fsSL https://ollama.com/install.sh -o "$tmp/install.sh"; then
    rm -rf "$tmp"; note "could not download the Ollama installer: install it from https://ollama.com/download, then run bootstrap again"; return 1
  fi
  sh "$tmp/install.sh" || { rm -rf "$tmp"; note "the Ollama installer failed (see above): install it from https://ollama.com/download, then run bootstrap again"; return 1; }
  rm -rf "$tmp"
  find_ollama || { note "Ollama was installed but its command is not found: open a new terminal and run bootstrap again"; return 1; }
  good "Ollama installed ($("$OLLAMA_BIN" --version 2>/dev/null | awk '{print $NF}'))"
}
vectors() {
  local log pid check pull_log
  [ "$NO_VECTORS" = 1 ] && { note "search by meaning skipped (--no-vectors)"; return 0; }
  [ "$DEPS_OK" = 1 ] || { note "search by meaning skipped: numpy is missing (see step 7)"; return 0; }
  find_ollama || install_ollama || return 0
  if ! ollama_up; then
    if [ -n "$OLLAMA_APP" ]; then open -a "$OLLAMA_APP" >/dev/null 2>&1 || true; ollama_wait 30 || true; fi
    if ! ollama_up; then  # no app (Linux without a running service, or the command alone)
      mkdir -p "$HOME/.cache/wiki-kit"
      nohup "$OLLAMA_BIN" serve >"$HOME/.cache/wiki-kit/ollama-serve.log" 2>&1 </dev/null &
      ollama_wait 30 || { note "Ollama does not answer at $OLLAMA_API: start it (the Ollama app, or 'ollama serve'), then run bootstrap again"; return 0; }
    fi
  fi
  if ! "$OLLAMA_BIN" list 2>/dev/null | awk 'NR > 1 {print $1}' | grep -qxF "$EMBED_MODEL"; then
    say "        downloading $EMBED_MODEL (about 300 MB, once)"
    if [ -t 2 ]; then  # a terminal: the progress bar redraws in place
      "$OLLAMA_BIN" pull "$EMBED_MODEL" >/dev/null || { note "could not download $EMBED_MODEL: run '$OLLAMA_BIN pull $EMBED_MODEL' and read the message, then run bootstrap again"; return 0; }
    else  # captured output: the progress bar would be thousands of lines, so it goes to a log kept only on failure
      pull_log="$HOME/.cache/wiki-kit/ollama-pull.log"
      mkdir -p "$(dirname "$pull_log")"
      "$OLLAMA_BIN" pull "$EMBED_MODEL" >"$pull_log" 2>&1 || { note "could not download $EMBED_MODEL (log: $pull_log): run '$OLLAMA_BIN pull $EMBED_MODEL' and read the message, then run bootstrap again"; return 0; }
      rm -f "$pull_log"
    fi
  fi
  if [ ! -f "$SEARCH_CFG" ]; then
    python3 -I "$KIT/scripts/search.py" embed-setup >/dev/null 2>&1 || true
  fi
  if ! grep -q '"embeddings"' "$SEARCH_CFG" 2>/dev/null; then
    note "search by meaning is switched off in $SEARCH_CFG; to switch it on: python3 -I $KIT/scripts/search.py embed-setup"; return 0
  fi
  check=$(python3 -I "$KIT/scripts/search.py" embed-check 2>&1) || { note "the model does not answer: $(printf '%s' "$check" | tail -1)"; return 0; }
  log="$HOME/.cache/wiki-kit/bootstrap-index.log"
  mkdir -p "$(dirname "$log")"
  pid=$(cat "$log.pid" 2>/dev/null || true)
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    good "search by meaning on; the hub index is still being built (log: $log)"; return 0
  fi
  nohup python3 -I "$KIT/scripts/search.py" index "$HUB" >"$log" 2>&1 </dev/null &
  echo $! > "$log.pid"
  good "search by meaning on (the model answers); building the hub index in the background (log: $log)"
}
vectors || note "search by meaning step stopped early; search works on words"

say ""
say "Done: $ok ok, $warn note(s), $fail failure(s). Hub: $HUB"
say "Next: open the hub folder in VS Code, start Claude Code, sign in, and type:  /wiki init personal"
say "Guide: $KIT/docs/QUICKSTART.md (English), $KIT/docs/QUICKSTART.ru.md (Russian), $KIT/docs/QUICKSTART.uk.md (Ukrainian)"
[ "$fail" -eq 0 ]
