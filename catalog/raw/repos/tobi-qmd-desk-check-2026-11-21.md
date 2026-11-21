---
title: "Desk check: tobi/qmd v2.9.0"
source: https://github.com/tobi/qmd/tree/v2.9.0
type: repos
authors: ["Tobi Lutke (tobi)"]
source_date: 2026-11-18
ingested: 2026-11-21
repo: tobi/qmd
kind: cli
version: "2.9.0"
licence: MIT
tags: [catalog, desk-check, kind-cli, qmd, search, bm25, embeddings, mcp]
summary: "tobi/qmd v2.9.0 read from a read-only clone: a Node CLI (with an SDK and an MCP server) for on-device hybrid search over Markdown: BM25, vectors and LLM re-ranking with three GGUF models downloaded from Hugging Face on first use; index in ~/.cache/qmd/index.sqlite; every command, the MCP server, the Claude Code plugin manifest and its two skills; opt-in remote models; freshness; deferred by the kit."
---

# Desk check: tobi/qmd v2.9.0

Read from a shallow clone of tag `v2.9.0` (commit `aa247d0ee2e5dc3b83e1270714c0f06ca94e2514`, committed 2026-11-17), at `$EXTERNAL/qmd`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 2.9.0.

## Repository facts

- `package.json`: `"name": "@tobilu/qmd"`, `"version": "2.9.0"`, description "Query Markup Documents - On-device hybrid search for markdown files with BM25, vector search, and LLM reranking", `"bin": {"qmd": "bin/qmd"}`, `"license": "MIT"`, `"engines": {"node": ">=22.0.0"}`. Main dependencies: `node-llama-cpp` 3.22.3, `better-sqlite3` 13.2.0, `sqlite-vec` 0.1.9, `@modelcontextprotocol/server` 2.4.0, tree-sitter grammars for Go, Python, Rust, TypeScript.
- `LICENSE`: "MIT License", "Copyright (c) 2024-2026 Tobi Lutke".
- `CHANGELOG.md`: "## [2.9.0] - 2026-11-17": "QMD adds document processors, metadata filtering, and remote model support. This release also updates llama.cpp and hardens concurrent indexing and MCP shutdown."
- `.claude-plugin/marketplace.json`: marketplace `qmd`, one plugin `qmd` (`"version": "2.9.0"`, licence MIT) with `"skills": ["./qmd", "./release"]` and `"mcpServers": {"qmd": {"command": "qmd", "args": ["mcp"]}}`. `.pi/settings.json` points the Pi harness at the same `skills` folder.
- Other folders: `src/` (CLI in `src/cli/qmd.ts`, MCP server in `src/mcp/server.ts`, SDK entry `src/index.ts`), `finetune/` (training of the query-expansion model), `docs/` (`SYNTAX.md`, `PROCESSORS.md`), `test/`, `tools/`.
- Kind: `cli`. It is also a library (`createStore` from `@tobilu/qmd`) and ships an MCP server; the parts below are its commands, the SDK entry and the plugin's two skills.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/tobi/qmd`: `pushed_at` 2026-11-20T21:34:04Z; licence `MIT`; default branch `main`; not archived.
- `gh api repos/tobi/qmd/releases/latest`: tag `v2.9.0`, published 2026-11-18T03:48:03Z.
- `gh api repos/tobi/qmd/compare/v2.9.0...main`: `ahead_by` 2 ("Keep pooled embedding input in a single evaluation batch" and its merge). So the clone is at the latest release; two later commits touch embedding batching.

## How to run here

- Clone: `git clone --depth 1 --branch v2.9.0 https://github.com/tobi/qmd $EXTERNAL/qmd`, read-only.
- Running it would need an install the kit has not made: `npm install -g @tobilu/qmd` or `bun install -g @tobilu/qmd` (or `npx @tobilu/qmd`), Node.js >= 22 or Bun >= 1.0.0, and on macOS Homebrew SQLite ("brew install sqlite") for extension support. A sandbox trial would use `npx` in a scratch folder with `XDG_CACHE_HOME` and `QMD_CONFIG_DIR` pointed into it.
- Do not run `npm install` or `bun install` inside the clone: the `prepare` script runs `scripts/install-hooks.mjs`, which copies a `pre-push` hook into the clone's `.git/hooks`.
- Models: "QMD uses three local GGUF models (auto-downloaded on first use)", "downloaded from HuggingFace and cached in `~/.cache/qmd/models/`" (or `$XDG_CACHE_HOME/qmd/models`). Defaults in `src/llm.ts`:
  - embeddings `hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf` (README: "~300MB");
  - re-ranking `hf:ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF/qwen3-reranker-0.6b-q8_0.gguf` ("~640MB");
  - query expansion `hf:tobil/qmd-query-expansion-1.7B-gguf/qmd-query-expansion-1.7B-q4_k_m.gguf` ("~1.1GB"), a fine-tuned model.
  - Together about 2 GB of downloads (the sum of the three README sizes). `query` needs all three unless `--no-rerank` and typed `lex:`/`vec:` lines are used; `search` needs none.
  - `QMD_EMBED_MODEL`, `QMD_RERANK_MODEL`, `QMD_GENERATE_MODEL` or `models:` in `index.yml` override them; the README suggests `Qwen3-Embedding-0.6B` "for better multilingual (CJK) support". Switching the embedding model needs `qmd embed -f`.
- Index and config: "Index stored in: `~/.cache/qmd/index.sqlite`" (SQLite with FTS5 and `sqlite-vec`); config in `~/.config/qmd/index.yml` (honours `XDG_CONFIG_HOME` and `QMD_CONFIG_DIR`); `qmd init` makes a project-local `.qmd/index.yml` beside a project-local `index.sqlite`. Approvals of checked-in configs go to `~/.config/qmd/trusted.json`; the MCP daemon PID to `~/.cache/qmd/mcp.pid`.
- Outbound calls found: model downloads and, in `pull`, a `HEAD` request per model to `https://huggingface.co/<repo>/resolve/main/<file>` to compare ETags (`HF_ENDPOINT` selects a mirror). Opt-in only: remote embeddings through an OpenAI-compatible endpoint (`models.embed: "http://...#model-id"`, keyless unless `apiKeyEnv` names a variable), and remote re-ranking through TypeSafe's fixed `https://api.typesafe.ai/v1/systemone` endpoint (`models.rerank: "typesafe:<model>"`, needs a key). No telemetry or analytics code was found (search for `telemetry`, `analytics`, `posthog`, `sentry`, and for `fetch(` and `https://` in `src/`).
- Shell commands it can run: `qmd collection update-cmd <name> '<command>'` sets a command (for example `git pull`) that `qmd update` runs before re-indexing. A checked-in `.qmd/index.yml` "is not trusted by default": its update commands, collection paths outside the project and custom models are skipped unless approved with `qmd trust` (or `QMD_TRUST_LOCAL_CONFIG=1`).

## Parts

### Command: collection (`src/cli/qmd.ts`, `case "collection"`)

- `add` (path, `--name`, `--mask` globs), `list`, `remove`, `rename`, `show`, `metadata` (keys, types and value counts to filter on), `include` / `exclude` from unscoped queries, `update-cmd` (a shell command before `qmd update`). Collections are a global registry searchable from any folder.
- Needs: an installed `qmd`; writes `index.yml`.

### Command: context (`case "context"`)

- `add`, `list`, `rm`: human-written descriptions attached to `qmd://` paths, returned with matching documents; the README calls it "the key feature of QMD".

### Command: ls (`case "ls"`)

- Lists indexed files of a collection or sub-path.

### Command: get (`case "get"`)

- Shows one document by path or docid (`#abc123`), optionally `:from:count`; line numbers on by default; fuzzy suggestions for wrong paths.

### Command: multi-get (`case "multi-get"`)

- Fetches several documents by glob, comma-separated list or docids; skips files over 64 KB by default (`--max-bytes`).

### Command: search (`case "search"`)

- "Full-text BM25 keywords (no LLM)": SQLite FTS5, no model needed. Output formats `cli`, `json`, `csv`, `md`, `xml`, `files`; `-c` collections, `--filter` metadata, `--min-score`, `--all`.

### Command: vsearch (`case "vsearch"`, alias `vector-search`)

- "Vector similarity only"; needs the embeddings from `qmd embed` and the embedding model; free-text queries also use local query expansion.

### Command: query (`case "query"`, alias `deep-search`)

- "Hybrid search with auto expansion + reranking (recommended)": the original query (weighted ×2) plus an LLM expansion, each searched in BM25 and vectors, fused with Reciprocal Rank Fusion (k=60) and a top-rank bonus, top 30 re-ranked by the Qwen3 re-ranker, then a position-aware blend. Typed query documents with `lex:`, `vec:`, `hyde:` and `intent:` lines skip the built-in expansion; `--no-rerank` skips re-ranking ("much faster on CPU"); `--explain` traces scores.
- Needs: all three models unless `--no-rerank` and typed lines are used.

### Command: embed (`case "embed"`)

- Chunks indexed documents ("900 tokens/chunk, 15% overlap") and stores vectors; `-f` re-embeds all; `--chunk-strategy auto` chunks code at function and class boundaries with tree-sitter; `--max-docs-per-batch`, `--max-batch-mb`, `--timeout` (default 30 minutes).

### Command: pull (`case "pull"`)

- Downloads the embedding, generation and re-rank models; `--refresh` re-checks them against Hugging Face.

### Command: update (`case "update"`)

- Re-indexes all collections; runs each collection's update command first; `--pull` runs `git pull` before.

### Command: init (`case "init"`)

- "Create a project-local .qmd index": config and index inside the project instead of `~/.config` and `~/.cache`.

### Command: status (`case "status"`)

- Index and collection health, contexts, metadata keys, whether the MCP daemon runs.

### Command: doctor (`case "doctor"`)

- "Diagnose the install (runtime, sqlite-vec, embedding fingerprints, GPU probe)". Not in the help text, documented in the README.

### Command: trust (`case "trust"`)

- `trust`, `trust list`, `trust revoke`: approve the gated fields of a checked-in `.qmd` config.

### Command: cleanup (`case "cleanup"`)

- "Drop inactive docs/orphans, compact FTS, vacuum"; `--dry-run`.

### Command: bench (`case "bench"`)

- Runs search-quality benchmarks from a fixture file across the backends; table or `--json`. "if the fixture's collection isn't indexed, bench currently runs to completion and reports all zeros with no warning."

### Command: mcp (`case "mcp"`, `src/mcp/server.ts`)

- "Start the MCP server (stdio transport for AI agents)". Tools: `query`, `get`, `multi_get`, `status`, `metadata`. `qmd mcp --http` serves on `localhost:8181` (`POST /mcp`, `POST /query` alias `/search`, `POST /metadata`, `GET /health`); `--daemon` backgrounds it; `qmd mcp stop`.
- Binds to `localhost` by default; rejects requests whose `Origin` is not a loopback address (DNS-rebinding guard); "the endpoints are unauthenticated". Models stay loaded across requests; contexts are disposed "after 5 min idle".

### Command: skills and skill (`case "skills"`, `case "skill"`)

- `qmd skills list|get|path` prints the bundled skills; `qmd skill install` writes the qmd skill into `./.agents/skills/qmd` (`--global`: `~/.agents/skills/qmd`).

### Library: SDK (`src/index.ts`, `createStore`)

- `createStore({ dbPath, config })` with `update`, `embed`, `searchVector` and more; document processors (new in 2.9.0, `docs/PROCESSORS.md`) turn JSON exports or logs into several index documents through explicit callbacks or trusted argv commands.

### Skill: qmd (`skills/qmd/SKILL.md`)

- Description: "Search local markdown knowledge bases, notes, docs, and wikis with QMD." `allowed-tools: Bash(qmd:*), mcp__qmd__*`; metadata version "2.3.0" (older than the package). Workflow: search, then retrieve with `get` or `multi-get`, then answer from retrieved text citing paths or docids; "Do not answer from snippets alone"; prefer typed `qmd query` documents the agent writes itself over the built-in expansion.
- Without the plugin: readable; needs an installed `qmd`.

### Skill: release (`skills/release/SKILL.md`)

- Description: "Manage releases for this project. Validates changelog, installs git hooks, and cuts releases." `disable-model-invocation: true`. A maintainer tool for qmd itself.

## How the kit uses it

- Not used. Status `candidate`, deferred: considered for Markdown search once a wiki passes about 100 articles. Meanwhile the kit's own `scripts/search.py` does hybrid search: `docs/PROJECT-CONTEXT.md` (kit root), line 100: "`search.py` default mode is hybrid (reciprocal rank fusion of exact words and stem-prefix matching) on a plain unicode61 index"; line 104: "local embeddings are adopted as an optional part of `search.py`". The pattern gist also names qmd as the search option once an index file is not enough (its desk check in this catalog).

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 90 model calls on opus, $6.66 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
