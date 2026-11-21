---
title: "nashsu/llm_wiki"
category: reference
kind: app
areas: [knowledge-bases, converting-documents-and-recordings, search-and-embeddings]
repo: nashsu/llm_wiki
version: "0.6.13"
licence: GPL-3.0
desk_checked: 2026-11-21
sources:
  - raw/repos/nashsu-llm-wiki-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-knowledge-bases, area-converting-documents-and-recordings, area-search-and-embeddings, kind-app, llm-wiki, knowledge-base, desktop-app, tauri, rejected]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Tauri desktop app that builds an LLM-maintained knowledge base from documents: two-step ingest, document parsing, chat with citations, optional vector search, a knowledge graph, deep research, review and lint, a web clipper, a local HTTP API and an MCP server. Rejected for work data: its own API keys send data past the organisation's model account. Its source already has Claude Code CLI and Ollama providers, so the revisit condition is due for the owner's review."
---

# nashsu/llm_wiki

> A desktop application (kind `app`, licence GPL-3.0 from the licence file, version `0.6.13` read) built on the LLM Wiki pattern: it turns documents into an interlinked Markdown wiki with an LLM, and adds a graph view, deep research, a review queue, a web clipper and a local API for agents. Rejected for work data; every part carries that reason.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Not this: build and maintain a knowledge base from documents in a desktop app. Rejected: for work data, its own API keys send data past the organisation's model account | two-step ingest | knowledge-bases |
| Not this: turn PDFs, Office files and e-books into wiki pages. Rejected: for work data, its own API keys send data past the organisation's model account | document parsing | converting-documents-and-recordings |
| Not this: chat with a knowledge base and get numbered citations. Rejected: for work data, its own API keys send data past the organisation's model account | chat and query | knowledge-bases |
| Not this: search a wiki by meaning. Rejected: for work data, its own API keys send data past the organisation's model account | vector search | search-and-embeddings |
| Not this: see a wiki as a graph and find its gaps. Rejected: for work data, its own API keys send data past the organisation's model account | knowledge graph, graph insights | knowledge-bases |
| Not this: research a gap on the web and ingest the results. Rejected: for work data, its own API keys send data past the organisation's model account | deep research | knowledge-bases |
| Not this: clip web pages into a knowledge base. Rejected: for work data, its own API keys send data past the organisation's model account | web clipper | knowledge-bases |
| Not this: let an agent query the app's wiki. Rejected: for work data, its own API keys send data past the organisation's model account | local HTTP API, MCP server | knowledge-bases |

## Run it here

- **Clone**: `git clone --depth 1 --branch v0.6.13 https://github.com/nashsu/llm_wiki $EXTERNAL/llm_wiki`, read-only.
- **Version**: `0.6.13`, the latest release, published 2026-10-22; `main` is identical to the tag. Check: `gh api repos/nashsu/llm_wiki/releases/latest --jq .tag_name`.
- **Read first**: `README.md`, then `src/lib/llm-providers.ts` and `src-tauri/src/commands/claude_cli.rs` for what leaves the machine.
- **Switch off** (if it is ever tried): web search providers, Firecrawl, MinerU Cloud and remote embeddings; "Launch at system startup"; unauthenticated local API access. Every ingest, chat, lint and research step goes to the chosen model provider; the update check asks GitHub for the latest release.
- **Do not install**: the app (binary or source build), its Chrome extension or its MCP server, for work data. A trial waits for the owner's re-decision and the user's yes.

## What's inside

Parts: the app's main functions, from the README and the source.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| two-step ingest | The LLM analyses a source, then writes summary, entity and concept pages, index, log and overview; hash cache, persistent queue, folder import, watch of `raw/sources/`. Rejected: for work data, its own API keys send data past the organisation's model account. | rejected | The app and a model provider; every source goes to it. | Revisit when it can work through the organisation's Claude account or a local model. |
| document parsing | PDF, DOCX, PPTX, XLSX, ODS, EPUB, MOBI to Markdown; MinerU Cloud or local for complex PDFs. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The app; MinerU Cloud sends PDFs out. | Revisit when it works through the organisation's Claude account or a local model. |
| image ingestion | Captions PDF images with a vision model for image-aware search. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | A vision-capable provider. | Revisit when it works through the organisation's Claude account or a local model. |
| chat and query | Word search over wiki and sources, graph expansion, a context budget from 4K to 1M tokens, numbered citations, answers saved back to the wiki. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | A model provider. | Revisit when it works through the organisation's Claude account or a local model. |
| vector search | Optional embeddings through an OpenAI-compatible endpoint, stored in LanceDB; off by default. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | An embeddings endpoint, local or remote. | Revisit when it works through the organisation's Claude account or a local model. |
| knowledge graph | Relevance from links, shared sources, common neighbours and page type; Louvain communities with cohesion scores. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The app. | Revisit when it works through the organisation's Claude account or a local model. |
| graph insights | Surprising connections and knowledge gaps (isolated pages, sparse communities, bridge pages), each with a research button. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The app. | Revisit when it works through the organisation's Claude account or a local model. |
| deep research | LLM-written queries to Tavily, SerpApi or SearXNG, synthesis into a page, auto-ingest. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | A search provider and a model provider; queries leave the machine. | Revisit when it works through the organisation's Claude account or a local model. |
| chat agent and skills | Rust agent with wiki, source, graph and web tools, approved shell commands and local `SKILL.md` folders. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | A model provider. | Revisit when it works through the organisation's Claude account or a local model. |
| review queue | Items flagged for human judgment during ingest, with fixed actions and pre-written search queries. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The app. | Revisit when it works through the organisation's Claude account or a local model. |
| lint | Orphans, broken links, pages without outlinks; semantic findings from the model. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | A model provider for the semantic part. | Revisit when it works through the organisation's Claude account or a local model. |
| cascade deletion | Deleting a source removes its summary and cleans shared pages, index and dead links. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The app. | Revisit when it works through the organisation's Claude account or a local model. |
| web clipper | Chrome extension that sends cleaned Markdown to the app's clipper port for auto-ingest. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | Chrome and the running app. | Revisit when it works through the organisation's Claude account or a local model. |
| local HTTP API | Token-protected API on `localhost` port 19828: projects, files, reviews, hybrid search, agent chat, graph, rescan. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The running app. | Revisit when it works through the organisation's Claude account or a local model. |
| MCP server | Ten tools over the same API (status, projects, files, read, reviews, search, chat, graph, rescan). Rejected: for work data, own API keys send data past the organisation's model account. | rejected | Node.js and the running app. | Revisit when it works through the organisation's Claude account or a local model. |
| projects and templates | Scenario templates fill `purpose.md` and `schema.md`; ZIP export and import; index rebuild; an Obsidian vault folder. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | The app. | Revisit when it works through the organisation's Claude account or a local model. |
| model providers | OpenAI, Anthropic, Google, Azure, MiniMax, custom endpoints, Ollama, and subprocess providers for the Claude Code and Codex CLIs. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | An API key, a local Ollama, or a signed-in `claude` CLI. | Revisit when it works through the organisation's Claude account or a local model. On paper this looks met: the `claude-code` provider runs the local `claude` CLI on its signed-in account, and `ollama` is a local model. Owner to re-decide. |
| update check | Asks the GitHub releases API for a newer version and shows a hint; never downloads. Rejected: for work data, own API keys send data past the organisation's model account. | rejected | Network to GitHub. | Revisit when it works through the organisation's Claude account or a local model. |

## Tried

None yet: rejected without a trial.

## Verdict

Rejected for work data only: a third-party desktop app with its own API keys sends work data to the model provider past the organisation's own model account. The GPL-3.0 licence is a fact, not the reason: it allows use and forbids only copying its code into the MIT kit. With one's own keys at home it may be used, but there is no need, since the kit's engine is nvk/llm-wiki. The revisit condition is that it can work through the organisation's Claude account or a local model, and this desk check found both a Claude Code CLI provider and an Ollama provider in `0.6.13`: the decision is due for the owner's review, with web search, cloud parsing and remote embeddings left off in any trial.

## See Also

- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page
- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; document parsing
- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; vector search
- [[nvk-llm-wiki|nvk/llm-wiki]] ([nvk/llm-wiki](../references/nvk-llm-wiki.md)): the engine chosen instead
- [[karpathy-llm-wiki-gist|karpathy LLM Wiki gist]] ([karpathy LLM Wiki gist](../references/karpathy-llm-wiki-gist.md)): the pattern the app is built on

## Sources

- [Desk check: nashsu/llm_wiki v0.6.13](../../raw/repos/nashsu-llm-wiki-desk-check-2026-11-21.md): every main function read from the README and the source, outbound calls, freshness, the reason for rejection and what was found against its revisit condition.
