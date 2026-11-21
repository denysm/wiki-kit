---
title: "Trial record: EmbeddingGemma 2 Q8_0 GGUF on llama-server, index speed and recall"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-13
ingested: 2026-11-21
url: https://huggingface.co/google/embeddinggemma-2
part: "embeddinggemma-2-Q8_0.gguf"
version: "f9972ac"
status: tried
tags: [catalog, trial, kind-model, embeddings, search, llama-cpp]
summary: "EmbeddingGemma 2 Q8_0 on llama.cpp llama-server 0.7.0 (Metal, Apple M4 Pro 24 GB), indexing 13,090 chunks: recall 0.93/0.95 vectors only, index 357 s, server peak 656 MB, 13 ms per query. Retold from the measurement note."
---

# Trial record: EmbeddingGemma 2 Q8_0 on llama-server

Task, by kind: benchmark an embedding model for hybrid search over two Markdown knowledge-base roots (13,090 chunks, 3.47 million tokens). Retold from `../2026-11-21-measurements-local-embeddings.md`.

## Setup

EmbeddingGemma 2 Q8_0 (Google, 2026-09, Apache-2.0, 270M text parameters, 768 dims, 310 MB) on llama.cpp `llama-server` 0.7.0 (Metal) on an Apple M4 Pro with 24 GB. Nothing was installed for this record beyond that server; the Ollama runs reuse the same model.

## Result

- Recall@5/@10, vectors only 0.93/0.95; words, translations and vectors 0.98/1.00.
- Index 357 s (9.7k tokens/s), server peak 656 MB with 4 slots, 13 ms per query.
- Ollama 0.40.16 on the same model: 439 s, runner peak 275-282 MB, 15.5 ms per query, 1.5 s cold start, vectors equal llama-server's (mean cosine 1.0000, same recall).

## Cost

Index 357 s; no tokens spent on any model API.
