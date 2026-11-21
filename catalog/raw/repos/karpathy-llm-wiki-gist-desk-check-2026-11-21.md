---
title: "Desk check: karpathy LLM Wiki gist (revision ac46de1)"
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f/ac46de1ad27f92b28ac95459c782c07f6b8c964a
type: repos
authors: ["Andrej Karpathy (karpathy)"]
source_date: 2026-04-04
ingested: 2026-11-21
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
kind: pattern
version: "ac46de1"
licence: "none stated: read only"
tags: [catalog, desk-check, kind-pattern, llm-wiki, knowledge-base, pattern]
summary: "The LLM Wiki gist read at its only revision ac46de1: one idea file, llm-wiki.md, describing an agent-maintained Markdown wiki with three layers, three operations, an index and a log, optional search, and Obsidian as the viewer. No licence stated. It is the pattern behind the kit's knowledge-base design, run through nvk/llm-wiki rather than an own schema."
---

# Desk check: karpathy LLM Wiki gist (revision ac46de1)

Read from a clone of gist `442a6bf555914893e9891c11519de94f` at revision `ac46de1ad27f92b28ac95459c782c07f6b8c964a` (committed 2026-04-04T16:25:13Z), at `$EXTERNAL/karpathy-llm-wiki-gist`. The clone was not modified. Checked 2026-11-21. Version read by this desk check: ac46de1.

## Repository facts

- One file: `llm-wiki.md`, 11985 bytes, heading "# LLM Wiki", subtitle "A pattern for building personal knowledge bases using LLMs."
- It calls itself "an idea file, it is designed to be copy pasted to your own LLM Agent", meant to "communicate the high level idea", while "your agent will build out the specifics in collaboration with you".
- Licence: the gist states none, and a gist has no licence field. Recorded as "none stated: read only": read and retold here, not copied.
- The same file ships verbatim inside nashsu/llm_wiki as `llm-wiki.md` (`cmp` finds the two identical).

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api gists/442a6bf555914893e9891c11519de94f` returned HTTP 502 twice; not checked through that endpoint.
- `gh api gists/442a6bf555914893e9891c11519de94f/commits`: one revision, `ac46de1ad27f92b28ac95459c782c07f6b8c964a`, committed 2026-04-04T16:25:13Z by `karpathy`.
- `git ls-remote` of the gist: `HEAD` and `refs/heads/master` both at `ac46de1ad27f92b28ac95459c782c07f6b8c964a`. So the clone is at the only revision.

## How to run here

- Clone: `git clone https://gist.github.com/442a6bf555914893e9891c11519de94f.git $EXTERNAL/karpathy-llm-wiki-gist`, read-only.
- Nothing runs: it is a Markdown text. No telemetry, no outbound calls, nothing to switch off.
- It mentions tools (Obsidian and its Web Clipper, Marp and Dataview plugins, qmd); none needs to be installed to read it.

## Parts (main ideas)

### Idea: a compounding wiki instead of retrieval

- Most document use of LLMs "looks like RAG": the model rediscovers knowledge on every question and "There's no accumulation."
- Instead the LLM "incrementally builds and maintains a persistent wiki": on each new source it updates entity pages, revises summaries and notes contradictions; knowledge "is compiled once and then *kept current*".
- Division of labour ("Why this works"): the human curates sources, directs analysis and asks questions; the LLM does the bookkeeping that makes people abandon wikis. "The LLM's job is everything else."
- Needs: an agent that can read and write files.

### Idea: three layers (raw sources, wiki, schema)

- Raw sources are immutable: "the LLM reads from them but never modifies them".
- The wiki is LLM-generated Markdown the LLM "owns ... entirely".
- The schema is a document such as CLAUDE.md or AGENTS.md that "tells the LLM how the wiki is structured" and which workflows to follow; human and LLM co-evolve it.

### Idea: ingest

- Drop a source in, the LLM reads it, discusses takeaways, writes a summary page, updates the index, entity and concept pages, and the log. "A single source might touch 10-15 wiki pages."
- The author prefers one source at a time with the human involved; batch ingest is possible.

### Idea: query, and file good answers back

- The LLM searches pages, reads them and answers with citations, in whatever form fits (a page, a table, a slide deck, a chart).
- "good answers can be filed back into the wiki as new pages", so explorations compound like sources do.

### Idea: lint

- A periodic health check for contradictions, stale claims, orphan pages, concepts lacking their own page, missing cross-references, and data gaps a web search could fill; the LLM also suggests new questions and sources.

### Idea: index.md and log.md

- `index.md` is a content catalog (link, one-line summary, optional metadata) updated on every ingest and read first when answering; it "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" without embedding-based retrieval.
- `log.md` is append-only and chronological; a consistent entry prefix such as `## [2026-04-02] ingest | Article Title` makes it parseable with `grep`.

### Idea: optional search tools

- As the wiki grows, "you want proper search". It names qmd ("a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device", with a CLI and an MCP server), or a simpler search script the LLM writes.
- Needs: the chosen search tool; nothing for the index-only route.

### Idea: Obsidian as the viewer, and tips

- "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."
- Tips: Obsidian Web Clipper for getting web articles into Markdown; downloading images locally; the graph view; Marp for slides; Dataview over frontmatter; "The wiki is just a git repo of markdown files."
- Needs: Obsidian and plugins, all optional.

## Why reference

The gist is the pattern behind the kit's knowledge-base design. The kit runs the pattern through nvk/llm-wiki rather than through an own schema built from this gist. The comparison recorded for that choice: nvk/llm-wiki offers a complete feature set, an Obsidian vault per topic, an installable plugin for Claude Code and Codex, and reference docs detailed enough to verify behaviour; against it, heavy machinery to trust, pre-1.0 at the time, isolated topics. An own schema from the gist would take "about an hour to set up", but every command and check would have to be written and maintained. So the gist is read for ideas, not run: every part is `reference`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 90 model calls on opus, $6.66 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
