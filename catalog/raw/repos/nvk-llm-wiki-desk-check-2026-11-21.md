---
title: "Desk check: nvk/llm-wiki v1.0.0"
source: https://github.com/nvk/llm-wiki/tree/v1.0.0
type: repos
authors: ["nvk"]
source_date: 2026-10-24
ingested: 2026-11-21
repo: nvk/llm-wiki
kind: plugin
version: "1.0.0"
licence: MIT
tags: [catalog, desk-check, kind-plugin, llm-wiki, claude-code, knowledge-base, wiki]
summary: "Every part of nvk/llm-wiki v1.0.0 read from a read-only clone: 28 commands and the wiki-manager skill of the Claude Code plugin, six skill ports for Codex, OpenCode, DeepSeek Harness and small models, the Codex session hooks, and the bundled llm-wiki CLI; outbound calls, freshness from the GitHub API, which parts the kit uses and why this engine was chosen."
---

# Desk check: nvk/llm-wiki v1.0.0

Read from a shallow clone of tag `v1.0.0` (commit `35d37c5591c7585643196333edd83922e7bbc757`, committed 2026-10-24), at `$EXTERNAL/llm-wiki`. The clone was not modified; nothing was installed or run from it. Checked 2026-11-21. Version read by this desk check: 1.0.0.

## Repository facts

- Claude Code marketplace `.claude-plugin/marketplace.json`: `"name": "llm-wiki"`, `"version": "1.0.0"`, one plugin `"name": "wiki"` with `"source": "./claude-plugin"`. So the plugin id is `wiki@llm-wiki` and its commands are `/wiki` and `/wiki:<name>`.
- Plugin manifest `claude-plugin/.claude-plugin/plugin.json`: `"name": "wiki"`, `"version": "1.0.0"`, `"license": "MIT"`; it declares no hooks and no MCP servers.
- `claude-plugin/` holds `commands/` (28 command files), `skills/wiki-manager/` (one skill with 23 reference files in `references/`) and `bin/llm-wiki` (the CLI). There is no `hooks/` and no `agents/` folder in the Claude Code plugin.
- Other plugin folders: `plugins/llm-wiki/` (the Codex plugin: skills `wiki` and `wiki-query`, `hooks/hooks.json`, the same `bin/llm-wiki`), `plugins/llm-wiki-opencode/` (skills `wiki-manager` and `wiki-query`), `plugins/llm-wiki-dsh/` (DeepSeek Harness skill `wiki`), `profiles/query-lite/` (a read-only `wiki-query` skill for small models). The `references/` folder of every port is identical to the Claude Code one (`diff -q` finds no difference), and the Codex `bin/llm-wiki` is byte-identical to the Claude Code one.
- Counted by the catalog's parts rule (every `SKILL.md`, every `commands/*.md`, every `hooks/hooks.json`): 36 parts, that is 28 commands, 7 skills and 1 hook file. The bundled CLI `bin/llm-wiki` is not a part by that rule; it is described below as an extra row because the kit runs it.
- `LICENSE`: "MIT License", "Copyright (c) 2026 nvk".
- README changelog: "**v1.0.0** — **Stable identity, honest provenance, and five-runtime packaging.**" It adds stable `wiki_id` registry checks, raw coverage ownership, footnote and wiki-link integrity, nested raw namespaces, immutable refresh revisions with human-only verification, pinned Git manifest-only ingestion, DeepSeek Harness skills and Windows Codex hooks. The release name on GitHub is "v1.0.0 — Stable Provenance and Multi-Runtime Support".
- Repository root also has `scripts/` (installers and sync scripts for Codex, DeepSeek Harness, OpenCode; `llm-wiki-session`, the session helper), `benchmarks/`, `tests/`, and the project's own `CLAUDE.md` and `AGENTS.md` (instructions for developing the plugin, not parts).

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/nvk/llm-wiki`: `pushed_at` 2026-10-25T19:56:34Z; licence `MIT`; default branch `master`; not archived.
- `gh api repos/nvk/llm-wiki/releases/latest`: tag `v1.0.0`, published 2026-10-24T15:37:01Z.
- `gh api repos/nvk/llm-wiki/compare/v1.0.0...master`: `ahead_by` 1, the one commit "Update README.md". So the clone is at the latest release; the only later push changed the README.

## How to run here

- Clone: `git clone --depth 1 --branch v1.0.0 https://github.com/nvk/llm-wiki $EXTERNAL/llm-wiki`, read-only.
- Install as the kit does it: `claude plugin marketplace add https://github.com/nvk/llm-wiki.git#v1.0.0` and `claude plugin install wiki@llm-wiki` (the kit's `bootstrap.sh`, step "The llm-wiki plugin ... pinned to v1.0.0"). Installing from the upstream README (`claude plugin marketplace add nvk/llm-wiki`) follows the default branch, not the tag.
- Hooks: the Claude Code plugin at v1.0.0 ships no hooks, so nothing runs per session or per tool call when it is installed. The session hooks exist only in the Codex plugin (`plugins/llm-wiki/hooks/hooks.json`); `references/sessions.md` describes Claude Code hooks (`SessionStart`, `UserPromptSubmit`, `PostToolUse`, `PostToolBatch`, `PreCompact`, `PostCompact`, `Stop`, `SessionEnd`) as something an adapter would configure, not something the plugin installs.
- Outbound calls: the commands whose `allowed-tools` include `WebSearch` or `WebFetch` are `assess`, `audit`, `collect`, `idea`, `ingest`, `librarian`, `lint` (`WebSearch` only, for `--deep`), `plan`, `refresh`, `research`, `specialist` and `thesis`; `research` "Launches parallel agents to search the web". `collect` and `ingest` may also call `curl`; `collect --media archive|thumbnail|reference` defaults to downloading bounded originals ("Download/cache bounded originals by default", README); `ingest` fetches tweets through a Grok MCP server when one is configured. `checkpoint` may call `gh`. The CLI `bin/llm-wiki` and the session helper `llm_wiki_session.py` contain no network code (no `urllib.request`, `http` or `socket` use; the CLI imports only `urllib.parse`); the helper's docstring says it is "intentionally deterministic and local-only".
- OpenCode route to avoid: the README's OpenCode setup points `instructions` at a raw GitHub URL on `master`, which "OpenCode fetches ... fresh on every session start", so it is unpinned and an outbound call per session.
- What breaks without the plugin: the commands are Markdown instructions and read from the clone; they refer to `skills/wiki-manager/references/*.md` and to `${CLAUDE_PLUGIN_ROOT}/bin/llm-wiki`, which must then be read as paths under `$EXTERNAL/llm-wiki/claude-plugin/` (`skills/wiki-manager/references/...`) and as `$EXTERNAL/llm-wiki/claude-plugin/bin/llm-wiki`. `session` and `feedback` prefer `scripts/llm-wiki-session`, which is in the repository's `scripts/` but not inside `claude-plugin/`; without it they fall back to the file operations of `references/sessions.md`. The `/wiki` command names exist only when the plugin is installed.

## Parts

All commands resolve the hub from `$HOME/.config/llm-wiki/config.json` (`hub_path`), else `$HOME/wiki`, and the topic from `--wiki <name>` in `HUB/wikis.json` or `--local` (`.wiki/` in the current folder). Most skip archived topics unless `--include-archived` is given.

### Command: wiki (`claude-plugin/commands/wiki.md`)

- Description: "LLM wiki knowledge base — understands natural language." Router for natural-language requests, plus `init <name>` (creates `HUB/topics/<name>/`, or `.wiki/` with `--local`), status, and `config hub-path`. "A topic name is always required."
- Reads `skills/wiki-manager/SKILL.md` and `references/wiki-structure.md`. Tools: file tools and a few shell commands; no web.

### Command: ingest (`claude-plugin/commands/ingest.md`)

- Description: "Ingest source material into an active wiki. Accepts URLs, file paths, PDFs, freeform text, or processes the inbox. Supports tweets via Grok MCP."
- Options include `--type articles|papers|repos|notes|data`, `--raw-subdir`, `--inbox`, `--new-topic`. Hands bounded corpora to `ingest-collection`. Uses `curl`, `pdftotext`, `WebFetch`, `WebSearch`; tweets through `mcp__grok__*` tools when present.

### Command: ingest-collection (`claude-plugin/commands/ingest-collection.md`)

- Description: "Bulk-ingest source collections such as Git doc repos, MediaWiki sources, CSV/JSON message archives, and Wayback CDX snapshots into raw sources."
- Adapters `git`, `mediawiki-dump`, `mediawiki-api`, `csv-messages`, `wayback-cdx`; `--manifest-only --revision <ref>` pins Git paths and blob SHAs without copying bodies; `--dry-run`, `--limit`. Uses `git`, `curl`, `python3`, `bunzip2`, `gunzip`.

### Command: compile (`claude-plugin/commands/compile.md`)

- Description: "Compile raw sources into wiki articles. Synthesizes, cross-references, and organizes active knowledge."
- Reads `references/compilation.md` and `references/indexing.md`; `--full` recompiles everything, `--source`, `--topic`. File tools only; no web.

### Command: query (`claude-plugin/commands/query.md`)

- Description: "Ask read-only questions against the wiki. Supports quick, standard, deep, list, archived, supplementary-wiki, and resume modes with exact file citations."
- `allowed-tools: Read, Glob, Grep`: it cannot write. "This command is always read-only: do not update indexes or append to `log.md`." Modes `--quick`, `--deep`, `--raw`, `--list`, `--resume`, `--with <wiki>`.

### Command: lint (`claude-plugin/commands/lint.md`)

- Description: "Run health checks on the wiki. Find broken links, missing indexes, stale content, archive registry drift, inconsistencies, and suggest improvements."
- The agentic lint: runs the numbered checks of `references/linting.md` (C1 structure first); `--fix` applies fixes, `--deep` uses `WebSearch` "to fact-check claims and find missing information".

### Command: ll (`claude-plugin/commands/ll.md`)

- Description: "Extract lessons learned from the current session. Scans conversation for error→fix patterns, user corrections, and discoveries, then saves structured lessons to the wiki."
- Writes `raw/notes/YYYY-MM-DD-ll-<slug>.md` in the target wiki and updates `raw/notes/_index.md`; `--dry-run` previews, `--rules` also suggests CLAUDE.md or AGENTS.md rules. File tools only.

### Command: session (`claude-plugin/commands/session.md`)

- Description: "Capture, list, rehydrate, and promote llm-wiki session context. Supports automated hook capture into HUB/.sessions plus explicit promotion into topic raw notes."
- Subcommands `enable`, `disable`, `status`, `capture`, `list`, `show`, `rehydrate`, `promote <session-id> --topic <slug>`. Policy: "Auto-promotion is forbidden"; "Raw transcript archiving is off by default." Prefers `scripts/llm-wiki-session`, else the file operations of `references/sessions.md`.

### Command: feedback (`claude-plugin/commands/feedback.md`)

- Description: "Review, capture, and promote curated user-feedback candidates detected from session hooks."
- Candidates live under `HUB/.sessions/feedback/` until promoted into a topic's `raw/notes/`. Useful only where hooks capture sessions (Codex).

### Command: specialist (`claude-plugin/commands/specialist.md`)

- Description: "Manage personal specialist SKILL.md methods, topic allowlists, candidate discovery, and bounded specialist reviews."
- Routes `init`, `create`, `refresh`, `list`, `show`, `validate`, `enable`, `disable` to `"${CLAUDE_PLUGIN_ROOT}/bin/llm-wiki" specialist <subcommand>`; `suggest` and `apply` are agentic. Methods live in `HUB/.skills/`, are instruction-only and enabled per topic (README, "Personal Specialist Skills").

### Command: research (`claude-plugin/commands/research.md`)

- Description: "Deep multi-agent research on a topic, question, or thesis. Launches parallel agents to search the web, ingests sources, and compiles them into active wiki articles."
- README: "5 parallel agents: academic, technical, applied, news, contrarian"; `--deep` "8 agents"; `--retardmax` "10 agents". `--sources <N>` per round (default: 5, max: 20); `--min-time`; `--mode thesis "<claim>"`; up to three `--specialist` methods. Sends search queries to the web.

### Command: thesis (`claude-plugin/commands/thesis.md`)

- Description: "Deprecated — use /wiki:research --mode thesis instead." A shim that runs `research.md` with `--mode thesis`; "This shim will be removed in a future release."

### Command: plan (`claude-plugin/commands/plan.md`)

- Description: "Generate an implementation plan grounded in active wiki research." A "6-stage pipeline": read the wiki, interview, gap research, phased plan; `--quick`, `--no-interview`, `--no-research`, `--format rfc|adr|roadmap|spec`, `--with <wiki>`. Uses agents and the web for gap research.

### Command: assess (`claude-plugin/commands/assess.md`)

- Description: "Assess a local repo against the active wiki's research body and the broader market. Gap analysis, opportunities, competitive landscape."
- Asks which topic to compare against when none is named; writes `output/assess-{repo-name}-{YYYY-MM-DD}.md`. Uses agents and the web.

### Command: output (`claude-plugin/commands/output.md`)

- Description: "Generate output artifacts from active wiki content — summaries, reports, study guides, slide outlines, timelines, glossaries, comparisons. Outputs are filed back into the wiki."
- Types `summary`, `report`, `study-guide`, `slides`, `timeline`, `glossary`, `comparison`; `--with <wiki>`. No web.

### Command: audit (`claude-plugin/commands/audit.md`)

- Description: "Truth-seeking umbrella audit for llm-wiki. Combines active wiki maintenance, output drift checks, provenance review, and fresh research when trust is in doubt."
- `scan` (default) and `report`; `--artifact`, `--project`, `--fresh`; report in `.audit/REPORT.md`. Uses agents and the web.

### Command: librarian (`claude-plugin/commands/librarian.md`)

- Description: "Keep the active wiki article layer in check: staleness, quality, accuracy, and coherence."
- `scan` scores articles, report in `.librarian/REPORT.md`; `scan --passes ...conventions` writes a topic-guide proposal to `output/`; `fix <id>` is "not yet implemented". Uses agents and the web.

### Command: refresh (`claude-plugin/commands/refresh.md`)

- Description: "Check active wiki articles against current sources without mutating raw evidence or claiming automatic verification."
- `<article-path>` or `--due`; follows `references/refresh.md` (immutable revisions, human-only verification). Uses agents and the web.

### Command: collect (`claude-plugin/commands/collect.md`)

- Description: "Find, catalog, deduplicate, and optionally inventory bounded sets of artifacts, examples, resources, memes, tools, entities, media, or other collectible things."
- `--scale tiny|small|medium|large|huge`, `--media archive|thumbnail|reference` (originals downloaded by default), `--inventory preview|none|corpus|records`, `--dry-run`. Uses `curl`, agents and the web.

### Command: inventory (`claude-plugin/commands/inventory.md`)

- Description: "Track wiki-adjacent things the user cares about: items, Ideas, ingest candidates, entities, corpora, open questions, tasks, and other durable inventory records."
- Records under `inventory/`, saved views under `inventory/views/`, `migrate-output` from legacy outputs. File tools only.

### Command: idea (`claude-plugin/commands/idea.md`)

- Description: "Capture, research, shape, catalog, and explicitly promote Ideas into Projects through natural language."
- Writes `inventory/ideas/<slug>.md`; `develop` and `shape` research with the web; `promote` creates a Project with `WHY.md` and freezes the approved snapshot as `BRIEF.md`.

### Command: portfolio (`claude-plugin/commands/portfolio.md`)

- Description: "Show a read-only hub-wide portfolio of canonical Ideas and active Projects without duplicating topic-owned records." "This operation is read-only."

### Command: project (`claude-plugin/commands/project.md`)

- Description: "Manage projects inside a topic wiki. Projects are folders under output/projects/ that group related outputs (playbooks, images, code, data) with a goal captured in WHY.md."

### Command: dataset (`claude-plugin/commands/dataset.md`)

- Description: "Manage dataset manifests for data that is too large or unsuitable to store directly in the wiki. The wiki becomes the index/interface; the data stays external."
- Manifests under `datasets/<slug>/`; `profile` and `sample` are dry-run unless `--apply`.

### Command: archive (`claude-plugin/commands/archive.md`)

- Description: "Archive or restore whole topic wikis so old interests stay preserved but out of default context." Moves a topic to `HUB/topics/.archive/<slug>`; `restore`, `peek`.

### Command: checkpoint (`claude-plugin/commands/checkpoint.md`)

- Description: "Export, refresh, verify, or import a comprehensive cross-topic Project Knowledge Checkpoint for a repository, with privacy checks."
- Writes a bundle to `docs/knowledge/<slug>/` of a repository; `create` and `refresh` are dry-run by default; "`--apply` authorizes only the previewed file write—not commit, push, publication, release, or import."

### Command: retract (`claude-plugin/commands/retract.md`)

- Description: "Remove user-selected data or a source from wiki-controlled local files, including archives and session context. Dry-run first, apply explicitly, then verify."
- Literal values go through `scripts/llm-wiki retract --everywhere`, which reads from a hidden prompt or standard input and never prints the value.

### Command: adapter (`claude-plugin/commands/adapter.md`)

- Description: "Route to, register, inspect, validate, and run explicitly trusted local private adapters without putting their code or bulk data in the wiki."
- Runs `${CLAUDE_PLUGIN_ROOT}/bin/llm-wiki adapter route|add|list|show|doctor|run|remove`; registrations are machine-local; remote writes need an exact approved plan hash (README command table).

### Skill: wiki-manager (`claude-plugin/skills/wiki-manager/SKILL.md`, `references/`)

- Description: "Manage LLM-compiled wikis: initialize, ingest/import, compile/query, research/audit, ..." It activates for `/wiki` commands, wiki or knowledge-base work, or "questions in a directory with .wiki/ or a configured hub". Tools include `WebFetch` and `WebSearch`.
- Its 23 `references/*.md` files are the protocols every command reads (compilation, indexing, ingestion, linting, wiki-structure, sessions, specialists, and so on).

### Skill: wiki, Codex port (`plugins/llm-wiki/skills/wiki/SKILL.md`)

- Description: "Manage LLM-compiled wikis in Codex: ..." The Codex entry point `@wiki`; same references as the Claude Code skill.

### Skill: wiki-query, Codex port (`plugins/llm-wiki/skills/wiki-query/SKILL.md`)

- Description: "Fast, explicit, read-only llm-wiki queries for Codex." Invoked as `$wiki-query`; "It never activates implicitly or changes wiki files" (README).

### Skill: wiki-manager, OpenCode port (`plugins/llm-wiki-opencode/skills/wiki-manager/SKILL.md`)

- Description: "Manage LLM-compiled wikis in OpenCode: ..." Loaded through OpenCode `instructions` (see the unpinned URL above).

### Skill: wiki-query, OpenCode port (`plugins/llm-wiki-opencode/skills/wiki-query/SKILL.md`)

- Description: "Fast, read-only, index-first llm-wiki queries for OpenCode and compatible instruction-file harnesses."

### Skill: wiki, DeepSeek Harness port (`plugins/llm-wiki-dsh/skills/wiki/SKILL.md`)

- Description: "Manage LLM-compiled wikis in DeepSeek Harness: ..." Installed by `scripts/install-deepseek-harness.sh` into `${DSH_HOME:-$HOME/.dsh}/skills/wiki`.

### Skill: wiki-query, query-lite profile (`profiles/query-lite/SKILL.md`)

- Description: "Fast, read-only, index-first queries over an llm-wiki with bounded file reads, exact citations, and honest evidence gaps." A small preset for read-only setups.

### Hook: Codex session hooks (`plugins/llm-wiki/hooks/hooks.json`, `hooks/llm_wiki_session.py`, `hooks/llm-wiki-hook.cmd`)

- `hooks.json` registers `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `PreCompact`, `PostCompact` and `Stop`, each running `llm_wiki_session.py hook --harness codex --event-name <event> --if-enabled` with `"timeout": 5`.
- The helper appends a redacted event to `HUB/.sessions/queue/`, updates per-session state, writes a digest at checkpoints (every 50 observed tool events by default, compaction, stop), may record feedback candidates, and on `SessionStart` in balanced mode injects a short rehydration block. "It never calls an LLM or copies raw transcripts by default." `/wiki:session disable` makes it a no-op. The file is identical to `scripts/llm-wiki-session`.
- Codex only: the Claude Code plugin does not ship it. In Codex the hooks still need the user to review and trust them in `/hooks`.

### Extra: the CLI `llm-wiki` (`claude-plugin/bin/llm-wiki`, also `scripts/llm-wiki`)

- Docstring: "Local deterministic helpers for llm-wiki. This is not a replacement for the agentic /wiki workflows." Python 3, standard library only, no network code.
- Subcommands: `lint` ("Run local structural checks on a wiki root"; `--fix` "Apply unambiguous structural fixes", `--wiki`, `--local`, `--json`, `--fail-on critical|warning|suggestion`, `--strict-engine`), `archive`, `schema`, `identity`, `retract`, `specialist`, `adapter`, `checkpoint`.

## How the kit uses it

From the kit's public files (paths relative to the kit root) and the owner's notes, retold.

- In use as the engine of the kit's agent-maintained Markdown knowledge bases, run as a Claude Code plugin pinned at v1.0.0 since 2026-11-14, as is, without a fork. It is customised only through the extension points the plugin offers: a CLAUDE.md at the hub root, each topic's `config.md` and `schema.md`, own specialists, adapters. The kit is a layer of scripts and skills on top of it.
- `bootstrap.sh`: `PLUGIN_REPO="https://github.com/nvk/llm-wiki.git#v1.0.0"`, `PLUGIN_ID="wiki@llm-wiki"`; it runs `claude plugin marketplace add` and `claude plugin install`, and calls `bin/llm-wiki specialist --hub ... init` and `validate` from the plugin cache. Its last line tells the user to type `/wiki init personal`.
- `docs/QUICKSTART.md`: `/wiki init personal`, `/wiki:ingest` (a URL and a PDF), `/wiki:compile`, `/wiki:query`.
- `README.md`: `llm-wiki specialist validate`, `llm-wiki specialist enable ... --wiki ...`, `llm-wiki specialist refresh`; the catalog is "an llm-wiki topic".
- `skills/foreman/SKILL.md`: lessons go through `/wiki:ll` into the topic named in the work order. `skills/wrap/SKILL.md`: writes the lessons note "in the /wiki:ll format" and says the whole transcript is saved only on request through `/wiki:session` promote.
- `agents/COMMON.md`: agents run `bin/llm-wiki lint --wiki <name> --fix` from the plugin cache, then again without `--fix`, and never lint the hub root with `--fix`. The catalog's own `_index.md` files say "Generated by local llm-wiki lint."
- So in use: `wiki` (init), `ingest`, `compile`, `query`, `ll`, `session` (promote, on request), `specialist` (through its CLI subcommand), the `wiki-manager` skill (every command in use reads its `references/`), and the CLI (`lint`, `specialist`). No public kit file shows any other command, a port or the Codex hooks in use; those stay `candidate`.
- Why this engine: it was chosen over nashsu/llm_wiki and over an own schema built from the Karpathy LLM Wiki gist. The comparison recorded for it: complete feature set, an Obsidian vault per topic, an installable plugin for Claude Code and Codex, reference docs detailed enough to verify behaviour; against it: heavy machinery to trust, pre-1.0 at the time, isolated topics. The own schema would take "about an hour to set up", but every command and check would have to be written and maintained.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 90 model calls on opus, $6.66 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
