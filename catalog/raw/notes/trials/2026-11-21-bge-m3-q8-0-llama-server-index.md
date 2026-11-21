---
title: "Trial record: bge-m3 Q8_0 GGUF on llama-server, index speed and recall"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-13
ingested: 2026-11-21
url: https://huggingface.co/BAAI/bge-m3
part: "bge-m3-q8_0.gguf"
version: "5617a9f"
status: tried
tags: [catalog, trial, kind-model, embeddings, search, llama-cpp]
summary: "bge-m3 Q8_0 on llama.cpp llama-server 0.7.0 (Metal, Apple M4 Pro 24 GB), indexing 13,090 chunks: recall 0.95/0.95 vectors only, index 587 s, 765 MB, 15.5 ms per query. Retold from the measurement note."
---

# Trial record: bge-m3 Q8_0 on llama-server

Task, by kind: benchmark an embedding model for hybrid search over two Markdown knowledge-base roots (13,090 chunks, 3.47 million tokens), as the challenger to the chosen model. Retold from `../2026-11-21-measurements-local-embeddings.md`.

## Setup

bge-m3 Q8_0 (MIT, 568M, 1024 dims, 635 MB) on llama.cpp `llama-server` 0.7.0 (Metal) on an Apple M4 Pro with 24 GB.

## Result

- Recall@5/@10, vectors only 0.95/0.95; words, translations and vectors 0.98/1.00.
- Index 587 s (6.0k tokens/s), 765 MB, 15.5 ms per query.
- Full embedding pass: 44.8 ms per chunk, about 75 min at 100,000 chunks; vectors take 2 KB per chunk.

## Cost

Index 587 s; no tokens spent on any model API.
