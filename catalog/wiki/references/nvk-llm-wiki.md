---
title: "nvk/llm-wiki"
category: reference
kind: plugin
areas: [knowledge-bases, designing-something-new, writing-documents-and-articles, building-skills-and-plugins]
repo: nvk/llm-wiki
version: "1.0.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/nvk-llm-wiki-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-llm-wiki-engine-knowledge-bases.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-knowledge-bases, area-designing-something-new, area-writing-documents-and-articles, area-building-skills-and-plugins, kind-plugin, claude-code, llm-wiki, knowledge-base, wiki, obsidian]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Claude Code plugin that runs agent-maintained Markdown knowledge bases: 28 commands (ingest, compile, query, lint, research, lessons, sessions, specialists and more), the wiki-manager skill, ports for Codex, OpenCode and DeepSeek Harness, Codex-only session hooks, and a local deterministic CLI. The kit's engine, installed pinned at 1.0.0 and unforked; nine parts and the CLI in use, the rest candidates."
---

# nvk/llm-wiki

> A Claude Code plugin (kind `plugin`, licence MIT, version `1.0.0` read) for knowledge bases that an agent maintains: sources go into `raw/`, the agent compiles cited articles into `wiki/`, and commands query, lint, research and file lessons. It ships 28 commands and one skill for Claude Code, skill ports for other harnesses, session hooks for Codex only, and a standard-library CLI for the checks that need no model. Unlike other plugins in this catalog, this one is installed: it is the kit's engine.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Start a knowledge base for a topic, or one local to a project | `wiki` | knowledge-bases |
| Add a web page, a PDF, a file or pasted text to a knowledge base | `ingest` | knowledge-bases |
| Import a whole corpus: a docs repo, a MediaWiki, a message archive, web archive snapshots | `ingest-collection` | knowledge-bases |
| Turn new raw sources into cited, cross-linked articles | `compile` | knowledge-bases |
| Answer a question from a knowledge base with file citations, without changing it | `query` | knowledge-bases |
| Check a knowledge base's structure, links and indexes and fix the mechanical issues, without a model | CLI `llm-wiki` | knowledge-bases |
| Have an agent health-check a knowledge base and fact-check it on the web | `lint` | knowledge-bases |
| Save the lessons of a working session into a knowledge base | `ll` | knowledge-bases |
| Keep a distilled digest of a session and promote it into a topic | `session` | knowledge-bases |
| Review user corrections and preferences captured from sessions | `feedback` | knowledge-bases |
| Research a topic on the web and compile the findings into articles | `research` | knowledge-bases |
| Test a claim with evidence for and against, ending in a verdict | `research` (`--mode thesis`) | knowledge-bases |
| Audit whether a knowledge base and its outputs can still be trusted | `audit` | knowledge-bases |
| Find stale, weak or inconsistent articles | `librarian` | knowledge-bases |
| Re-check articles against their current sources, with a human verifying | `refresh` | knowledge-bases |
| Find and catalog a bounded set of things (tools, examples, media) | `collect` | knowledge-bases |
| Track items, source candidates and open questions with a status and a next action | `inventory` | knowledge-bases |
| Point a knowledge base at a dataset too large to copy into it | `dataset` | knowledge-bases |
| Hide an old topic from default context without deleting it | `archive` | knowledge-bases |
| Hand a project's knowledge to a code repository as a checked bundle | `checkpoint` | knowledge-bases |
| Remove a source or a sensitive value from every file the wiki controls | `retract` | knowledge-bases |
| Act on an external resource through a trusted local adapter | `adapter` | knowledge-bases |
| Plan an implementation grounded in what a knowledge base knows | `plan` | designing-something-new |
| Capture a rough idea, research and shape it, then promote it to a project | `idea` | designing-something-new |
| See every idea and project across topics | `portfolio` | designing-something-new |
| Group related outputs under one goal | `project` | designing-something-new |
| Compare a code repository with a knowledge base and the market | `assess` | designing-something-new |
| Write a summary, report, study guide, slide outline, timeline, glossary or comparison from a knowledge base | `output` | writing-documents-and-articles |
| Write, validate and enable personal review methods (specialist skills) per topic | `specialist` | building-skills-and-plugins |
| Query a knowledge base read-only from Codex, OpenCode or a small model | Codex skill `wiki-query`, OpenCode skill `wiki-query`, query-lite skill `wiki-query` | knowledge-bases |
| Run the wiki workflows from Codex, OpenCode or DeepSeek Harness | Codex skill `wiki`, OpenCode skill `wiki-manager`, DeepSeek Harness skill `wiki` | knowledge-bases |
| Capture session context automatically across compaction and restarts, in Codex | Codex hooks | knowledge-bases |

## Run it here

- **Clone** (for reading the parts): `git clone --depth 1 --branch v1.0.0 https://github.com/nvk/llm-wiki $EXTERNAL/llm-wiki`, read-only. Never edit the clone.
- **Version**: `1.0.0`, the latest release, published 2026-10-24; the only later upstream commit (pushed 2026-10-25) changed the README. Before relying on this card: `gh api repos/nvk/llm-wiki --jq .pushed_at` and `gh api repos/nvk/llm-wiki/releases/latest --jq .tag_name`. A new release needs a new desk check before the pin moves.
- **In use**: the plugin `wiki@llm-wiki` at `1.0.0`, installed in Claude Code from the marketplace pinned to the tag (`claude plugin marketplace add https://github.com/nvk/llm-wiki.git#v1.0.0`, then `claude plugin install wiki@llm-wiki`, as the kit's `bootstrap.sh` does), used as is since 2026-11-14, without a fork. It is customised only through its extension points: a CLAUDE.md at the hub root, each topic's `config.md` and `schema.md`, own specialists, adapters; the kit's scripts and skills sit on top. Parts used: `/wiki init`, `/wiki:ingest`, `/wiki:compile`, `/wiki:query`, `/wiki:ll` (and its note format), `/wiki:session` promote on request, specialists through `llm-wiki specialist`, and the CLI lint `llm-wiki lint --wiki <name> --fix`, then again without `--fix`; never `--fix` on a hub root.
- **Read first**: `$EXTERNAL/llm-wiki/claude-plugin/commands/<command>.md`, then the `skills/wiki-manager/references/*.md` files it names.
- **Switch off**: the Claude Code plugin ships no hooks, so nothing runs per session. Outbound calls happen only in commands that use web search or fetch (`research`, `thesis`, `assess`, `audit`, `librarian`, `refresh`, `plan`, `idea`, `specialist`, `collect`, `ingest` for URLs, `lint --deep`); `collect` downloads originals unless given `--media reference`; `ingest` uses a Grok MCP server for tweets when one is configured. The CLI and the session helper have no network code. In Codex, `/wiki:session disable` turns the session hooks into no-ops.
- **Do not install**: from the default branch (the upstream README's `claude plugin marketplace add nvk/llm-wiki` follows `master`, not the tag); the Codex plugin, the DeepSeek Harness installer or the OpenCode `instructions` URL, which fetches the skill from `master` on every session start. Moving the pin to a new version waits for a new desk check and the user's yes.

## What's inside

Parts: 28 commands in `claude-plugin/commands/`, the `wiki-manager` skill, six skill ports (Codex, OpenCode, DeepSeek Harness, query-lite), one Codex hook file: 36 by the catalog's parts rule. The bundled CLI is listed as an extra row because the kit runs it. Without the plugin, every command is still readable: read its `skills/wiki-manager/references/...` as paths under `$EXTERNAL/llm-wiki/claude-plugin/`, and `${CLAUDE_PLUGIN_ROOT}/bin/llm-wiki` as `$EXTERNAL/llm-wiki/claude-plugin/bin/llm-wiki`; only the `/wiki` command names need the plugin.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `wiki` | Router for natural-language wiki requests; `init <name>` creates a topic under the hub (or `.wiki/` with `--local`); status and hub-path config. | in use | Readable; creating a hub by hand means following `references/wiki-structure.md`. | On a new release, re-check the topic layout `init` writes against the kit's hub rules. |
| `ingest` | Adds a URL, file, PDF, text or the inbox to `raw/`, typed `articles`, `papers`, `repos`, `notes` or `data`; hands corpora to `ingest-collection`. | in use | Readable; needs `pdftotext` for PDFs and web fetch for URLs. | On a new release, re-check raw frontmatter and type rules against the kit's raw checks. |
| `ingest-collection` | Bulk import through adapters `git`, `mediawiki-dump`, `mediawiki-api`, `csv-messages`, `wayback-cdx`; `--manifest-only` pins Git paths and blob SHAs without copying bodies. | candidate | Readable; needs `git`, `curl`, `python3`. | Try it on a public docs repository whose pages should become one raw file each. |
| `compile` | Turns new raw sources into cited articles and updates indexes; `--full` recompiles all. | in use | Readable; file tools only. | On a new release, re-check article frontmatter and `## Sources` rules against `check_evidence.py`. |
| `query` | Read-only answer with file citations: quick, standard, deep, list, resume; `--with` adds a second wiki. Allowed tools are only Read, Glob, Grep. | in use | Readable; works with file tools only. | On a new release, re-check that it stays read-only. |
| `lint` | Agentic health check over the numbered checks of `references/linting.md`; `--fix` repairs, `--deep` fact-checks with web search. | candidate | Readable; `--deep` needs web search. The kit runs the CLI lint instead. | Try `--deep` on a small topic whose claims can be checked on the web. |
| `ll` | Extracts lessons (error and fix, corrections, discoveries) into `raw/notes/YYYY-MM-DD-ll-<slug>.md`; `--rules` suggests agent rules. | in use | Readable; file tools only. | On a new release, re-check the note format the kit's `wrap` skill copies. |
| `session` | Lists, shows, rehydrates and promotes session digests under `HUB/.sessions/`; enable or disable capture. Never auto-promotes; no transcripts by default. | in use | Readable; prefers `scripts/llm-wiki-session` (in the repository's `scripts/`, not in `claude-plugin/`), else plain file operations. In Claude Code no hook captures sessions. | On a new release, re-check the promote output and whether Claude Code hooks are added. |
| `feedback` | Lists and promotes feedback candidates (corrections, preferences, approvals) captured by session hooks into `raw/notes/`. | candidate | Readable; has nothing to read unless hooks capture sessions (Codex only). | Try it if session hooks are ever run in a sandbox session. |
| `specialist` | Manages personal `SKILL.md` review methods in `HUB/.skills/`: `init`, `create`, `validate`, `enable` per topic, `refresh` through the CLI; `suggest` and `apply` are agentic. | in use | The deterministic subcommands work from the clone's CLI; `apply` needs the commands. | On a new release, re-check the validator rules the kit's specialists must pass. |
| `research` | Parallel web-research agents (5 by default, 8 with `--deep`, 10 with `--retardmax`), then ingest and compile; `--sources` per round, `--min-time`, `--mode thesis`, up to three specialists. | candidate | Readable; needs subagents and web search; queries leave the machine. | Try it on a public technology question for a scratch topic, and record the cost. |
| `thesis` | Deprecated shim that runs `research --mode thesis`; to be removed. | candidate | Readable; same needs as `research`. | Use `research --mode thesis` instead when a claim needs testing. |
| `plan` | Six-stage plan grounded in the wiki: read, interview, gap research, phased plan; `--format rfc\|adr\|roadmap\|spec`. | candidate | Readable; gap research needs subagents and the web. | Try it when a build plan should cite a topic's articles. |
| `assess` | Compares a local repository with a topic and the market; writes `output/assess-{repo-name}-{YYYY-MM-DD}.md`. | candidate | Readable; needs subagents and the web. | Try it on one of the kit's own script folders against a related topic. |
| `output` | Generates a summary, report, study guide, slide outline, timeline, glossary or comparison from articles and files it back. | candidate | Readable; file tools only. | Try it for a glossary or timeline of a mature topic. |
| `audit` | Umbrella trust audit: wiki maintenance, output drift, provenance, fresh research when trust is in doubt; report in `.audit/REPORT.md`. | candidate | Readable; needs subagents and the web. | Try it on a topic whose outputs are older than its sources. |
| `librarian` | Scores articles for staleness and quality; report in `.librarian/REPORT.md`; can propose topic-guide conventions; `fix` is not implemented. | candidate | Readable; needs subagents and the web. | Try a scan on the largest topic before a clean-up. |
| `refresh` | Re-checks articles against current sources, with immutable revisions and verification left to a human. | candidate | Readable; needs subagents and the web. | Try `--due` on articles marked hot. |
| `collect` | Finds, dedupes and catalogs bounded sets of things; scales from tiny to huge; downloads originals by default. | candidate | Readable; needs subagents, web search and `curl`. | Try it with `--media reference` to catalog candidate tools for a task. |
| `inventory` | Durable tracking records (items, candidates, open questions, tasks) under `inventory/`, with saved views. | candidate | Readable; file tools only. | Try it for a source queue that should outlive a session. |
| `idea` | Captures an idea in `inventory/ideas/`, researches and shapes it, promotes it to a project with `WHY.md` and a frozen `BRIEF.md`. | candidate | Readable; `develop` and `shape` need the web. | Try it on the next rough proposal that is not yet a project. |
| `portfolio` | Read-only view of ideas and projects across all active topics. | candidate | Readable; read-only. | Try it once two or more topics hold ideas. |
| `project` | Groups related outputs under `output/projects/<slug>/` with a `WHY.md`. | candidate | Readable; file tools only. | Try it when one goal collects several outputs in a topic. |
| `dataset` | Manifests under `datasets/<slug>/` for data that stays outside the wiki; profile and sample only with `--apply`. | candidate | Readable; file tools only. | Try it for a data folder too large for `raw/`. |
| `archive` | Moves a topic to `HUB/topics/.archive/` and back; peeks into archived indexes. | candidate | Readable; the CLI's `archive` does the move. | Try it on the first topic that goes quiet. |
| `checkpoint` | Exports a cross-topic knowledge bundle into a repository's `docs/knowledge/<slug>/`, dry-run first, with privacy checks; `--apply` writes only the previewed files. | candidate | Readable; the CLI seals and verifies; may call `gh`. | Try it for a code repository that needs a knowledge handoff, with audience `private`. |
| `retract` | Removes a source or a value from every wiki file, archives and sessions included; dry-run, apply, verify; literal values only through a hidden prompt. | candidate | Readable; the CLI's `retract --everywhere` does the value scan. | Try a dry run the next time a source must go. |
| `adapter` | Routes, registers, checks and runs trusted local private adapters; registrations stay machine-local; remote writes need an approved plan hash. | candidate | Works through the clone's CLI. | Try it when a hosted document must be edited from a wiki workflow. |
| `wiki-manager` skill | The protocols every command reads: 23 reference files (structure, ingestion, compilation, indexing, linting, sessions, specialists and more); activates on wiki work. | in use | The reference files read as plain Markdown from the clone. | On a new release, diff `references/` before moving the pin. |
| Codex skill `wiki` | The same workflows for Codex as `@wiki`; identical references. | candidate | Codex only. | Read it if a knowledge base is ever run from Codex. |
| Codex skill `wiki-query` | Read-only lookups in Codex, invoked explicitly; never writes. | candidate | Codex only. | Read it with the Codex skill `wiki`. |
| OpenCode skill `wiki-manager` | The workflows for OpenCode, loaded as an instruction file. | candidate | OpenCode only; the upstream setup fetches it from `master` on every session. | Read it if a knowledge base is run from OpenCode; pin a local copy. |
| OpenCode skill `wiki-query` | Read-only, index-first queries for OpenCode and other instruction-file harnesses. | candidate | OpenCode only. | Read it with the OpenCode skill `wiki-manager`. |
| DeepSeek Harness skill `wiki` | The workflows for DeepSeek Harness, copied into its user skill folder by an installer script. | candidate | DeepSeek Harness only. | Read it if a knowledge base is run from DeepSeek Harness. |
| query-lite skill `wiki-query` | Small read-only query preset with bounded reads and exact citations. | candidate | Works as plain instructions in any harness. | Try it with a small local model answering from one topic. |
| Codex hooks (`hooks/hooks.json`) | Six Codex events run the local session helper: redacted events, per-session state and digests under `HUB/.sessions/`, digest every 50 tool events, soft rehydration at session start; 5-second timeout; no model calls, no network. | candidate | Codex only; the Claude Code plugin does not ship it. Codex asks the user to trust it. | Read again if a Claude Code release adds hooks; they would run every session. |
| CLI `llm-wiki` (`bin/llm-wiki`) | Standard-library Python helpers for the checks that need no model: `lint` (`--fix`, `--fail-on`, `--json`), `archive`, `schema`, `identity`, `retract`, `specialist`, `adapter`, `checkpoint`. | in use | Runs from the clone with `python3 -I`; no network code. | On a new release, re-run the kit's lint on every topic before moving the pin. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-14 to 2026-11-21 | Engine of agent-maintained Markdown knowledge bases | `wiki`, `ingest`, `compile`, `query`, `ll`, `session`, `specialist`, `wiki-manager` skill, CLI `llm-wiki` | Real use as the installed plugin at `1.0.0`, pinned and unforked; customised only through its extension points, the kit's scripts and skills on top. This catalog is one of its topics. | not measured per part | [use record](../../raw/notes/trials/2026-11-21-llm-wiki-engine-knowledge-bases.md) |

## Verdict

The kit's engine: nine parts and the CLI are in real use at `1.0.0`, installed as the plugin, pinned and unforked. It was chosen over a desktop app and over writing an own schema from the pattern gist, because the own schema would take "about an hour to set up" but every command and check would then be the kit's to maintain; the price is heavy machinery to trust and topics that stay isolated. The other commands, the ports and the Codex hooks are candidates waiting for a task. Revisit when the freshness check shows a release after `1.0.0` (diff `references/` and re-run the lint on every topic before moving the pin), or when a Claude Code release of the plugin adds hooks.

## See Also

- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page; ingest, compile, query, lint, research
- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; `plan`, `idea`, `assess`
- [[area-writing-documents-and-articles|Writing documents and articles]] ([Writing documents and articles](../topics/area-writing-documents-and-articles.md)): area page; `output`
- [[area-building-skills-and-plugins|Building skills and plugins]] ([Building skills and plugins](../topics/area-building-skills-and-plugins.md)): area page; `specialist`
- [[nashsu-llm-wiki|nashsu/llm_wiki]] ([nashsu/llm_wiki](../references/nashsu-llm-wiki.md)): the desktop app it was chosen over
- [[karpathy-llm-wiki-gist|karpathy LLM Wiki gist]] ([karpathy LLM Wiki gist](../references/karpathy-llm-wiki-gist.md)): the pattern it implements
- [[tobi-qmd|tobi/qmd]] ([tobi/qmd](../references/tobi-qmd.md)): Markdown search deferred for larger wikis

## Sources

- [Desk check: nvk/llm-wiki v1.0.0](../../raw/repos/nvk-llm-wiki-desk-check-2026-11-21.md): every part read from the clone, outbound calls, freshness through the GitHub API, the kit's use and the reason for the choice.
- [Use record: llm-wiki as the engine of agent-maintained knowledge bases](../../raw/notes/trials/2026-11-21-llm-wiki-engine-knowledge-bases.md): the real use behind the `in use` statuses and the Tried row.
