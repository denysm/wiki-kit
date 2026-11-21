---
title: "tobi/qmd"
category: reference
kind: cli
areas: [search-and-embeddings, knowledge-bases]
repo: tobi/qmd
version: "2.9.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/tobi-qmd-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, area-knowledge-bases, kind-cli, qmd, search, bm25, embeddings, reranking, mcp, markdown]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Node CLI, SDK and MCP server for on-device hybrid search over Markdown: BM25, vectors and LLM re-ranking with three GGUF models downloaded from Hugging Face on first use, index in ~/.cache/qmd/index.sqlite. Deferred: considered once a wiki passes about 100 articles; the kit's own search.py does hybrid search meanwhile. Every part a candidate."
---

# tobi/qmd

> A command-line tool (kind `cli`, licence MIT, version `2.9.0` read), also usable as a Node library and an MCP server, that indexes Markdown folders and searches them on the machine: keyword search with BM25, vector search, and hybrid search with query expansion and LLM re-ranking through local GGUF models. The kit has not installed it; it is a deferred candidate for search over large wikis.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Search Markdown notes or a wiki by exact words, with no model | `search` | search-and-embeddings |
| Search a wiki by meaning when the question uses other words than the source | `query` | search-and-embeddings |
| Search by vector similarity only | `vsearch` | search-and-embeddings |
| Build or refresh the vectors of an indexed folder | `embed` | search-and-embeddings |
| Register the folders to index and describe them for better ranking | `collection`, `context` | knowledge-bases |
| Fetch the full text of search hits to answer from, with paths or docids | `get`, `multi-get` | knowledge-bases |
| Give an agent wiki search as native tools instead of shell calls | `mcp` | knowledge-bases |
| Teach an agent the search-then-retrieve loop over local Markdown | `qmd` skill | knowledge-bases |
| Measure search quality on a fixture of questions | `bench` | search-and-embeddings |
| Embed search over Markdown inside a Node program | SDK | search-and-embeddings |

## Run it here

- **Clone**: `git clone --depth 1 --branch v2.9.0 https://github.com/tobi/qmd $EXTERNAL/qmd`, read-only. Never edit the clone, and never run `npm install` or `bun install` in it: its `prepare` script copies a `pre-push` hook into the clone's `.git/hooks`.
- **Version**: `2.9.0`, the latest release, published 2026-11-18; two later commits on `main` touch embedding batching. Check: `gh api repos/tobi/qmd --jq .pushed_at` and `gh api repos/tobi/qmd/releases/latest --jq .tag_name`.
- **Read first**: `README.md` (Quick Start, MCP Server, Requirements, Data Storage), then `skills/qmd/SKILL.md`.
- **What running it takes**: a global npm or Bun install (`@tobilu/qmd`), Node.js >= 22 or Bun, on macOS Homebrew SQLite; on first use three GGUF models from Hugging Face into `~/.cache/qmd/models/` (about 300MB embeddings, 640MB re-ranker, 1.1GB query expansion). The index goes to `~/.cache/qmd/index.sqlite`, the config to `~/.config/qmd/index.yml`; `qmd init` keeps both inside a project.
- **Switch off**: no telemetry found. Outbound calls are the model downloads and, in `pull`, a check of each model against Hugging Face. Leave remote models off: `models.embed` set to an HTTP endpoint sends text to that server, and `models.rerank: "typesafe:<model>"` sends candidates to a hosted re-ranker. `qmd mcp --http` binds `localhost`, and its endpoints are unauthenticated: do not pass `--host 0.0.0.0`. Collection update commands are shell commands run by `qmd update`.
- **Do not install**: the package, the Claude Code plugin (`qmd@qmd`, which also registers the MCP server) or `qmd skill install`, until a wiki outgrows the kit's search and the user says yes. A sandbox trial would use `npx @tobilu/qmd` in a scratch folder with `XDG_CACHE_HOME` and `QMD_CONFIG_DIR` pointed into it, so models, index and config stay there.

## What's inside

Parts: the commands of `qmd`, the SDK entry, and the two skills of its Claude Code plugin.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `collection` | Adds, lists, renames, removes, includes or excludes indexed folders with glob masks; shows metadata keys; sets an update command run before re-indexing. | candidate | An installed `qmd`. | Try it on a copy of one wiki root when a wiki passes about 100 articles. |
| `context` | Attaches human-written descriptions to `qmd://` paths, returned with matching documents. | candidate | An installed `qmd`. | Try it with the wiki's `raw/` and `wiki/` described separately. |
| `ls` | Lists indexed files of a collection. | candidate | An installed `qmd`. | Try it with `collection`. |
| `get` | Shows one document by path or docid, from a line, line-numbered. | candidate | An installed `qmd`. | Try it with the search trial. |
| `multi-get` | Fetches several documents by glob, list or docids; skips large files. | candidate | An installed `qmd`. | Try it with the search trial. |
| `search` | BM25 keyword search over SQLite FTS5; JSON, CSV, Markdown, XML or file-list output; metadata filters. | candidate | An installed `qmd`; no model. | Compare it with the kit's `search.py` on the same question set. |
| `vsearch` | Vector similarity search over the embeddings. | candidate | The embedding model and `embed` run. | Try it with `query` in the same trial. |
| `query` | Hybrid search: the query plus an LLM expansion, BM25 and vectors fused by reciprocal rank, top 30 re-ranked by a local model, blended by position; typed `lex:`, `vec:`, `hyde:` lines skip the expansion. | candidate | All three models (about 2 GB), or `--no-rerank` and typed lines; faster with a GPU. | Try it on cross-language questions where the kit's word search misses. |
| `embed` | Chunks documents (900 tokens, 15% overlap, code by syntax tree on request) and stores vectors. | candidate | The embedding model; minutes per large wiki. | Try it with `query`; record the time on one wiki. |
| `pull` | Downloads the three models; `--refresh` re-checks them against Hugging Face. | candidate | Network to Hugging Face. | Run it once in the sandbox, with the cache in the scratch folder. |
| `update` | Re-indexes collections, running their update commands first. | candidate | An installed `qmd`. | Try it after editing wiki files in the sandbox. |
| `init` | Creates a project-local index and config. | candidate | An installed `qmd`. | Use it in the sandbox so nothing lands in the home cache. |
| `status` | Index and collection health; MCP daemon state. | candidate | An installed `qmd`. | Run it in the sandbox. |
| `doctor` | Diagnoses runtime, `sqlite-vec`, embedding fingerprints and GPU. | candidate | An installed `qmd`. | Run it first in the sandbox. |
| `trust` | Approves or revokes the gated fields (commands, outside paths, custom models) of a checked-in project config. | candidate | An installed `qmd`. | Only if a project config is ever committed. |
| `cleanup` | Drops orphans, compacts the full-text index, vacuums; dry run available. | candidate | An installed `qmd`. | After a sandbox trial with deletions. |
| `bench` | Scores search quality from a fixture of questions and expected files; reports zeros silently when the collection is not indexed. | candidate | An installed `qmd` and a fixture. | Try it with the kit's search question set turned into a fixture. |
| `mcp` | MCP server with tools `query`, `get`, `multi_get`, `status`, `metadata`; stdio by default, `--http` on `localhost:8181` with a daemon mode; origin check, no authentication. | candidate | An installed `qmd`; models stay loaded while it runs. | Try stdio for one sandbox session if shell calls prove clumsy. |
| `skills` and `skill` | Prints the bundled skills; `skill install` writes the qmd skill into `.agents/skills/qmd`. | candidate | An installed `qmd`. | Read the skill from the clone instead of installing it. |
| SDK | `createStore` with update, embed and search; document processors turn exports into several index documents. | candidate | Node.js and the package in a project. | Only if a kit script ever moves to Node. |
| `qmd` skill | Agent loop: search, then retrieve full text, then answer citing paths or docids; write typed queries instead of relying on the built-in expansion. | candidate | `qmd` on the path, or its MCP server. | Read it with the search trial; its loop already matches the kit's search rule. |
| `release` skill | Cuts qmd's own releases and installs its git hooks; not invoked by the model. | candidate | A qmd checkout. | No task here: read it only if contributing upstream. |

## Tried

None yet.

## Verdict

A deferred candidate: no part has been tried. It is considered for Markdown search once a wiki passes about 100 articles; until then the kit's own `scripts/search.py` does hybrid search without an install or model downloads. Revisit when a wiki passes that size or word search keeps missing questions phrased in other words, and try it in a sandbox with its caches inside a scratch folder; check the release after `2.9.0` first.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; `search`, `query`, `embed`
- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page; collections, retrieval, MCP
- [[karpathy-llm-wiki-gist|karpathy LLM Wiki gist]] ([karpathy LLM Wiki gist](../references/karpathy-llm-wiki-gist.md)): names qmd as the search option for a growing wiki
- [[google-embeddinggemma-2|google/embeddinggemma-2]] ([google/embeddinggemma-2](../references/google-embeddinggemma-2.md)): the embedding model in use for the kit's own search; qmd's default is `embeddinggemma-300M`
- [[ggml-org-llama-cpp|ggml-org/llama.cpp]] ([ggml-org/llama.cpp](../references/ggml-org-llama-cpp.md)): the runtime under qmd's models

## Sources

- [Desk check: tobi/qmd v2.9.0](../../raw/repos/tobi-qmd-desk-check-2026-11-21.md): every part read from the clone, models, index location, MCP server, outbound calls, freshness, and the kit's deferral.
