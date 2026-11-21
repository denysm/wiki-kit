---
title: "karpathy LLM Wiki gist"
category: reference
kind: pattern
areas: [knowledge-bases]
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
version: "ac46de1"
licence: "none stated: read only"
desk_checked: 2026-11-21
sources:
  - raw/repos/karpathy-llm-wiki-gist-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-knowledge-bases, kind-pattern, llm-wiki, knowledge-base, pattern, obsidian]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Idea file describing an agent-maintained Markdown wiki: compile knowledge once and keep it current, three layers (raw, wiki, schema), ingest, query and lint, an index and a log, optional search, Obsidian as the viewer. The pattern behind the kit's knowledge bases; read for ideas, run through nvk/llm-wiki."
---

# karpathy LLM Wiki gist

> A pattern (kind `pattern`, no licence stated, so read only; revision `ac46de1` read): one Markdown idea file to paste into a coding agent, which then builds a personal wiki with you. It describes ideas, not an implementation. Every part is `reference`: the kit runs the pattern through nvk/llm-wiki.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Understand why an agent-maintained wiki beats retrieval on every question | compounding wiki | knowledge-bases |
| Decide what the agent may change and what stays immutable | three layers | knowledge-bases |
| Shape the ingest, query and lint workflows of a knowledge base | ingest, query, lint | knowledge-bases |
| Decide when an index file stops being enough and search is needed | index and log, search tools | knowledge-bases |
| Browse a knowledge base as a graph next to the agent | Obsidian as viewer | knowledge-bases |

## Run it here

- **Clone**: `git clone https://gist.github.com/442a6bf555914893e9891c11519de94f.git $EXTERNAL/karpathy-llm-wiki-gist`, read-only.
- **Version**: revision `ac46de1`, the gist's only revision (committed 2026-04-04). Check: `gh api gists/442a6bf555914893e9891c11519de94f/commits --jq '.[0].version'`.
- **Read**: `llm-wiki.md`, the only file.
- **Switch off**: nothing; it is text, with no calls.
- **Do not install**: nothing is needed to read it; the tools it mentions (Obsidian plugins, qmd) wait for a task and the user's yes.

## What's inside

Parts: the main ideas of `llm-wiki.md`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| compounding wiki | The agent builds and keeps current a persistent wiki instead of rediscovering knowledge per question; the human curates, the agent does the bookkeeping. | reference | Nothing to read; an agent that writes files to apply. | When the kit's hub rules are redesigned. |
| three layers | Immutable raw sources, an agent-owned wiki, a schema file (CLAUDE.md, AGENTS.md) that sets conventions and workflows. | reference | Nothing. | When a new layer (inventory, datasets) is proposed. |
| ingest | Read a source, discuss it, write a summary, update index, entity pages and log; one source may touch 10-15 pages. | reference | Nothing. | When the ingest rules of a topic change. |
| query | Answer with citations in any fitting form; file good answers back as pages. | reference | Nothing. | When outputs pile up outside the wiki. |
| lint | Periodic check for contradictions, stale claims, orphans, missing pages and cross-references, gaps to research. | reference | Nothing. | When adding a lint check. |
| index and log | A content index read first, enough at about 100 sources; an append-only log with a greppable entry prefix. | reference | Nothing. | When a wiki passes about 100 sources. |
| search tools | Proper search once the wiki grows: qmd, or a simple script the agent writes. | reference | The chosen search tool. | When search over a wiki falls short. |
| Obsidian as viewer | Obsidian as the IDE, the agent as programmer, the wiki as codebase; clipper, local images, graph view, slides, frontmatter queries, git. | reference | Obsidian, optional. | When a wiki is browsed by people, not only agents. |

## Tried

None yet: the gist is read for ideas, not run.

## Verdict

The pattern behind the kit's knowledge bases, kept as a reference. An own schema built from it would take "about an hour to set up", but every command and check would then have to be written and maintained, so the kit runs the pattern through nvk/llm-wiki. Consult it again when the hub rules are redesigned, when a wiki outgrows its index, or if the gist gets a new revision.

## See Also

- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page
- [[nvk-llm-wiki|nvk/llm-wiki]] ([nvk/llm-wiki](../references/nvk-llm-wiki.md)): the engine that implements the pattern here
- [[nashsu-llm-wiki|nashsu/llm_wiki]] ([nashsu/llm_wiki](../references/nashsu-llm-wiki.md)): a desktop app built on the same pattern
- [[tobi-qmd|tobi/qmd]] ([tobi/qmd](../references/tobi-qmd.md)): the search tool the gist names

## Sources

- [Desk check: karpathy LLM Wiki gist (revision ac46de1)](../../raw/repos/karpathy-llm-wiki-gist-desk-check-2026-11-21.md): every idea read from the clone, freshness through the GitHub API, the reason for `reference`.
