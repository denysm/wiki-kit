---
title: "Use record: llm-wiki as the engine of agent-maintained knowledge bases"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: nvk/llm-wiki
part: "wiki, ingest, compile, query, ll, session, specialist, wiki-manager, llm-wiki CLI"
version: "1.0.0"
status: in use
tags: [catalog, trial, use-record, kind-plugin, llm-wiki, knowledge-base]
summary: "nvk/llm-wiki 1.0.0 runs as a Claude Code plugin, pinned and unforked, as the engine of agent-maintained Markdown knowledge bases since 2026-11-14; customised only through its extension points, with the kit's scripts and skills on top. Parts in use: init, ingest, compile, query, lessons, session promote, specialists, the wiki-manager skill and the CLI lint. Cost: not measured per part."
---

# Use record: llm-wiki as the engine of agent-maintained knowledge bases

- **Tool and parts**: nvk/llm-wiki, parts `wiki` (init), `ingest`, `compile`, `query`, `ll`, `session` (promote, on request), `specialist` (through its CLI subcommand), the `wiki-manager` skill, and the bundled CLI `llm-wiki` (`lint`, `specialist`).
- **Version**: 1.0.0, the tag `v1.0.0` of the desk check.
- **How it runs**: as the Claude Code plugin `wiki@llm-wiki`, installed from the marketplace at the `#v1.0.0` ref (the kit's `bootstrap.sh`), as is, without a fork. Not read from the clone: this is the one tool of its kind the kit installs.
- **Task, by kind**: the engine of agent-maintained Markdown knowledge bases (a hub of topic wikis: ingest sources into `raw/`, compile articles into `wiki/`, query with citations, lint, file lessons).
- **Since**: 2026-11-14, pinned at v1.0.0.
- **Kind of record**: real use, not a sandbox trial. Status after it: `in use`.

## How it is customised

Only through the extension points the plugin offers:

- a CLAUDE.md at the hub root (the hub's own rules for agents);
- each topic's `config.md` and `schema.md`;
- own specialists (personal `SKILL.md` methods in `HUB/.skills/`, validated and enabled per topic with `llm-wiki specialist`);
- adapters.

The kit is a layer of scripts and skills on top: it never edits the plugin. Lessons are written in the `/wiki:ll` note format (the kit's `wrap` skill files them with its own script); the deterministic lint is the plugin's CLI, `llm-wiki lint --wiki <name> --fix`, then again without `--fix`.

## Why this engine

It was chosen over nashsu/llm_wiki and over an own schema built from the Karpathy LLM Wiki gist.

- For it: complete feature set; an Obsidian vault per topic; an installable plugin for Claude Code and Codex; reference docs detailed enough to verify behaviour.
- Against it: heavy machinery to trust; pre-1.0 at the time; isolated topics.
- The own schema would take "about an hour to set up", but every command and check would have to be written and maintained.

## Result

In real use for the kit's knowledge bases, including this catalog, which is an llm-wiki topic linted by the plugin's CLI.

## Cost

Not measured per part: no token or dollar figure is attributed to the plugin.
