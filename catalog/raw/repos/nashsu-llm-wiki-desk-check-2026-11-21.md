---
title: "Desk check: nashsu/llm_wiki v0.6.13"
source: https://github.com/nashsu/llm_wiki/tree/v0.6.13
type: repos
authors: ["Yong Su (nashsu)"]
source_date: 2026-10-22
ingested: 2026-11-21
repo: nashsu/llm_wiki
kind: app
version: "0.6.13"
licence: GPL-3.0
tags: [catalog, desk-check, kind-app, llm-wiki, knowledge-base, desktop-app, tauri, rejected]
summary: "nashsu/llm_wiki v0.6.13 read from a read-only clone: a Tauri desktop app that builds a knowledge base from documents with an LLM (ingest, parsing, chat, vector search, graph, deep research, review, lint, web clipper, local HTTP API and MCP server). GPL-3.0 from the licence file (GitHub reports NOASSERTION). Rejected for work data: its own API keys send data to the model provider past the organisation's own model account. The source already has a Claude Code CLI provider and an Ollama provider, which bears on the revisit condition."
---

# Desk check: nashsu/llm_wiki v0.6.13

Read from a shallow clone of tag `v0.6.13` (commit `e08cfce65aad8b76b13546a081c1a8d4422b70c3`, committed 2026-10-21), at `$EXTERNAL/llm_wiki`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 0.6.13.

## Repository facts

- `package.json`: `"name": "llm-wiki"`, `"private": true`, `"version": "0.6.13"`; `src-tauri/tauri.conf.json`: `"version": "0.6.13"`.
- README: "LLM Wiki is a cross-platform desktop application that turns your documents into an organized, interlinked knowledge base — automatically." It says it "is based on Karpathy's LLM Wiki pattern" and lists what it kept (three layers, ingest, query, lint, `index.md`, `log.md`, wikilinks, frontmatter, Obsidian compatibility) and what it added.
- The repository ships the pattern gist verbatim as `llm-wiki.md` (`cmp` with the gist clone finds them identical).
- Tech stack (README): Tauri v2 with a Rust backend, React 19 and TypeScript, Milkdown editor, sigma.js graph, LanceDB for optional vectors, Zustand state.
- `LICENSE`: "LLM Wiki — Copyright (C) 2024-2026 Yong Su", then "GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007". So GPL-3.0; GitHub's API reports `NOASSERTION` because of the added first line. README: "licensed under the **GNU General Public License v3.0**".
- Folders: `src/` (React front end; `src/lib/` holds ingest, search, graph, lint, providers), `src-tauri/` (Rust backend: `api_server.rs`, `clip_server.rs`, `commands/`, `agent/`), `mcp-server/` (Node MCP server), `extension/` (Chrome extension), `plans/`, `scripts/`.
- Also from the in-app changelog (`src/lib/changelog.ts`): the "Claude Code CLI provider (the \"no API key\" option)" was made to work "across ingest, sweep, lint, chat, sources, and the clip watcher" in version 0.4.4; a fix for Ollama on a LAN address is in 0.4.3.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/nashsu/llm_wiki`: `pushed_at` 2026-10-21T11:17:29Z; licence `NOASSERTION`; default branch `main`; not archived.
- `gh api repos/nashsu/llm_wiki/releases/latest`: tag `v0.6.13` ("LLM Wiki v0.6.13"), published 2026-10-22T01:21:07Z.
- `gh api repos/nashsu/llm_wiki/compare/v0.6.13...main`: `identical`. So the clone is at the latest release and nothing was pushed after it.

## How to run here

- Clone: `git clone --depth 1 --branch v0.6.13 https://github.com/nashsu/llm_wiki $EXTERNAL/llm_wiki`, read-only.
- Running it means installing a desktop app: pre-built binaries from the releases (macOS `.dmg` for Apple Silicon, Windows `.msi`, Linux `.deb` and `.AppImage`), or a build from source with Node.js 20+, Rust 1.88+ and `protoc` (`npm install`, `npm run tauri build`). Not done here.
- Outbound calls, all configured in Settings: the chosen LLM provider for every ingest, chat, lint and research step (providers in `src/stores/wiki-store.ts`: `openai`, `anthropic`, `google`, `azure`, `ollama`, `custom`, `minimax`, `claude-code`, `codex-cli`); an OpenAI-compatible embeddings endpoint when vector search is on ("disabled by default"); web search through Tavily, SerpApi or SearXNG for Deep Research; Firecrawl (`https://api.firecrawl.dev` by default) when configured; MinerU Cloud (`https://mineru.net/api/v4`) for complex PDFs when chosen; an update check against the GitHub releases API (`https://api.github.com/repos/<repo>/releases/latest`) that only shows a hint and does not download.
- Local servers: an HTTP API on `localhost` port 19828 ("token-protected"; Settings can allow local unauthenticated access) and the clipper API on port 19827; the MCP server calls the same API.
- Other behaviour: an optional "Launch at system startup" setting; on macOS the close button hides the window and the app keeps running.
- `claude-code` provider: the Rust command spawns the local `claude` CLI as `claude -p --output-format stream-json --input-format stream-json --verbose --model <model>`, with an isolation mode that adds `--setting-sources project`, `--disable-slash-commands`, empty `--tools` and `--no-session-persistence`. So it runs on whatever account that CLI is signed in to. `ollama` talks to a local Ollama server.

## Parts (main functions)

### Function: two-step ingest (`src/lib/ingest.ts`, `src/lib/ingest-queue.ts`)

- Step 1, the LLM analyses a source (entities, concepts, connections, contradictions); step 2, it writes source summaries, entity and concept pages, `index.md`, `log.md`, `overview.md` and review items. SHA256 cache skips unchanged files; a persistent serial queue with retries "up to 3 times"; folder import; auto-watch of `raw/sources/`.
- Needs: the app and an LLM provider; every source goes to that provider.

### Function: document parsing (`src-tauri`, `src/lib/mineru.ts`)

- PDF (built-in extractor, optional MinerU Cloud, Local API or Pipeline), DOCX, PPTX, XLSX, ODS, EPUB and MOBI to Markdown; images and media previewed.
- Needs: the app; MinerU Cloud sends PDFs out when chosen.

### Function: multimodal image ingestion

- Extracts images from PDFs, captions them with a vision LLM, and shows them in image-aware search results.
- Needs: a vision-capable provider; images go to it.

### Function: chat and query pipeline (`src/lib/search.ts`, `src/lib/context-budget.ts`)

- Tokenized search (English words, Chinese bigrams) over `wiki/` and `raw/sources/`, optional vector hits, graph expansion two hops deep, a context budget from 4K to 1M tokens split 60/20/5/15, numbered citations; multi-conversation chat saved in `.llm-wiki/chats/`; "Save to Wiki" files answers into `wiki/queries/`.
- Needs: an LLM provider.

### Function: vector semantic search (LanceDB)

- Optional embedding retrieval through "any OpenAI-compatible /v1/embeddings endpoint", stored in LanceDB; README benchmark: "overall recall improved from 58.2% to 71.4% with vector search enabled".
- Needs: an embeddings endpoint (local or remote).

### Function: knowledge graph and communities (`src/lib/graph-relevance.ts`)

- A 4-signal relevance model (direct link ×3.0, source overlap ×4.0, Adamic-Adar ×1.5, type affinity ×1.0), sigma.js view, Louvain communities with cohesion scores (warning below 0.15).

### Function: graph insights (`src/lib/graph-insights.ts`)

- Surprising connections (cross-community, cross-type, periphery to hub) and knowledge gaps (isolated pages, sparse communities, bridge nodes), each with a Deep Research button.

### Function: deep research (`src/lib/deep-research.ts`)

- Web search through Tavily, SerpApi or SearXNG with LLM-written queries, a confirmation dialog, synthesis into a research page and auto-ingest; 3 concurrent tasks.
- Needs: a search provider key or instance and an LLM provider.

### Function: backend chat agent and skills (`src-tauri/src/agent/`)

- A Rust agent with wiki, source, graph and web search tools, AnyTXT, workspace file tools, "approved shell commands" and skill file reads; scans local `SKILL.md` folders, chosen per conversation with `/skill`; generated files under `agent-workspace/`.

### Function: review queue

- The LLM flags items for human judgment during ingest with fixed actions (Create Page, Deep Research, Skip) and pre-written search queries.

### Function: lint (`src/lib/lint.ts`)

- Findings of type orphan, broken link, no outlinks and semantic; structural checks run in a worker, semantic checks through the LLM.

### Function: cascade deletion (`src/lib/source-lifecycle.ts`)

- Deleting a source removes its summary page, drops it from shared pages' `sources[]`, cleans `index.md` and dead wikilinks.

### Function: Chrome web clipper (`extension/`)

- Manifest V3 extension using Readability and Turndown; sends clips to the app's clipper API on port 19827, where a watcher ingests them.

### Function: local HTTP API (`src-tauri/src/api_server.rs`)

- On `localhost` port 19828: health, projects, files, reviews, hybrid search, agent chat (streaming optional), graph, source rescan, page embedding. Token-protected unless local unauthenticated access is allowed in Settings.

### Function: MCP server (`mcp-server/`)

- Node MCP server over the same API. Tools: `llm_wiki_status`, `llm_wiki_projects`, `llm_wiki_set_project`, `llm_wiki_files`, `llm_wiki_read_file`, `llm_wiki_reviews`, `llm_wiki_search`, `llm_wiki_chat`, `llm_wiki_graph`, `llm_wiki_rescan_sources`. A separate agent-skill repository (not read) talks to the same app.

### Function: projects and templates

- Scenario templates (Research, Reading, Personal Growth, Business, General) pre-fill `purpose.md` (goals, key questions, scope, thesis) and `schema.md`; ZIP export and import; deterministic rebuild of `wiki/index.md`; an auto-generated `.obsidian/` folder.

### Function: LLM providers (`src/lib/llm-providers.ts`, `src/lib/claude-cli-transport.ts`)

- Per-project models, Chat and Ingest routed separately; providers listed above, including the `claude-code` and `codex-cli` subprocess transports and `ollama`. Keys are saved through the Tauri store.

### Function: update check (`src/lib/update-check.ts`)

- Asks the GitHub releases API for the latest version and shows a hint with a link; "We intentionally don't download or install".

## Why rejected

Rejected for work data only, as the kit owner decided: it is a third-party desktop app with its own API keys, so work data goes to the model provider past the organisation's own model account. Its GPL-3.0 licence (read from the licence file; GitHub reports `NOASSERTION`) is a fact, not a reason: it allows use and forbids only copying its code into the kit, which is MIT. With one's own keys at home it may be used; there is no need, since the kit's engine is nvk/llm-wiki, which was chosen over it (the comparison is in the nvk/llm-wiki desk check). Revisit condition: the app can work through the organisation's Claude account or a local model.

What this desk check found against that condition: at v0.6.13 the provider list already includes `claude-code`, which runs the local `claude` CLI and so uses whatever account that CLI is signed in to, and `ollama`, a local model server; the in-app changelog dates the working Claude Code CLI provider to 0.4.4. On paper the condition looks met for the model calls; not tried. Web search, Firecrawl, MinerU Cloud, a remote embeddings endpoint and the update check would still send data or requests out unless left off. The decision stays as recorded until the owner reviews it.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 90 model calls on opus, $6.66 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
