---
title: "Trial record: Qwen3-Embedding-4B Q8_0 GGUF on llama-server, index speed and recall"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-13
ingested: 2026-11-21
url: https://huggingface.co/Qwen/Qwen3-Embedding-4B
part: "Qwen3-Embedding-4B-Q8_0.gguf"
version: "5cf2132"
status: tried
tags: [catalog, trial, kind-model, embeddings, search, llama-cpp]
summary: "Qwen3-Embedding-4B Q8_0 on llama.cpp llama-server 0.7.0 (Metal, Apple M4 Pro 24 GB), indexing 13,090 chunks: recall 0.95/0.98 vectors only, index 5,969 s (an upper bound), 5.0 GB, 100 ms per query. Retold from the measurement note."
---

# Trial record: Qwen3-Embedding-4B Q8_0 on llama-server

Task, by kind: benchmark a larger embedding model for hybrid search over two Markdown knowledge-base roots (13,090 chunks, 3.47 million tokens), to see whether size buys recall. Retold from `../2026-11-21-measurements-local-embeddings.md`.

## Setup

Qwen3-Embedding-4B Q8_0 (Apache-2.0, 2560 dims, 4.3 GB) on llama.cpp `llama-server` 0.7.0 (Metal) on an Apple M4 Pro with 24 GB.

## Result

- Recall@5/@10, vectors only 0.95/0.98; words, translations and vectors 0.95/1.00 (words plus vectors 0.91/0.98).
- Index 5,969 s (about 0.6k tokens/s; for 44 minutes the GPU was shared with another run, so treat it as an upper bound), 5.0 GB, 100 ms per query.
- On a machine that can run it, the larger model bought nothing measurable on this set.

## Cost

Index 5,969 s at most; 5.0 GB of server memory; no tokens spent on any model API.
