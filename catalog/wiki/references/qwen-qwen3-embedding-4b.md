---
title: "Qwen/Qwen3-Embedding-4B"
category: reference
kind: model
areas: [search-and-embeddings]
url: https://huggingface.co/Qwen/Qwen3-Embedding-4B
version: "5cf2132"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/qwen-qwen3-embedding-4b-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-qwen3-embedding-4b-q8-0-llama-server-index.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, kind-model, embeddings, search, multilingual, gguf]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Qwen's 4B text embedding model (up to 2560 numbers, 32k context) in a 0.6B, 4B and 8B series. Its Q8_0 GGUF was measured on the kit's question set: nothing measurable gained over the 270M model, far slower and larger, so it is rejected; the other sizes and quantizations are listed."
---

# Qwen/Qwen3-Embedding-4B

> A Hugging Face model (kind `model`, licence Apache-2.0, revision `5cf2132` read): a 4B text embedding model with up to 2560 numbers per text, from a series of 0.6B, 4B and 8B sizes. The Q8_0 GGUF was measured here and is rejected: on the kit's set the larger model bought nothing measurable and indexed far slower.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Not this: embed a local knowledge base with a larger model hoping for better recall. Rejected: on this set the larger model bought nothing measurable and indexed in 5,969 s against 357 s for the 270M model | `Qwen3-Embedding-4B-Q8_0.gguf` | search-and-embeddings |
| Embed text with a very long context (32k) or task instructions on a machine that has the memory | `Qwen3-Embedding-0.6B` | search-and-embeddings |
| Embed with the series' largest model where speed and memory do not matter | `Qwen3-Embedding-8B` | search-and-embeddings |

## Run it here

- **No clone.** Read the card with `curl -s https://huggingface.co/Qwen/Qwen3-Embedding-4B/raw/main/README.md` and the metadata with `https://huggingface.co/api/models/Qwen/Qwen3-Embedding-4B`; the desk check read both at revision `5cf2132`.
- **Not in use**: the kit has no preset for it. It was run once as the Q8_0 GGUF on llama.cpp `llama-server`; the server took 5.0 GB, so do not run it again without a reason and the user's yes.
- **Switch off**: nothing runs unless set up; no outbound call while running; a download contacts the publisher once.
- **Do not install**: `transformers`, `sentence-transformers` or a GPU stack to read the card; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `Qwen3-Embedding-4B-Q8_0.gguf` | Q8_0 GGUF, 4279660224 bytes (4.3 GB): recall 0.95/0.98 vectors only and 0.95/1.00 with words, translations and vectors; index 5,969 s (an upper bound), 5.0 GB, 100 ms per query on llama-server. | rejected | A llama.cpp server and 5.0 GB of memory; Apple M4 Pro (Metal) in the trial | Revisit when `search.py eval` on a larger body shows it finding at least 3 more questions at recall@5 than the chosen model, or a much faster runtime for it exists. Rejected: no measurable gain on this set, far slower, 5 KB per chunk. |
| `Qwen3-Embedding-4B-Q4_K_M.gguf`, `Qwen3-Embedding-4B-Q5_0.gguf`, `Qwen3-Embedding-4B-Q5_K_M.gguf`, `Qwen3-Embedding-4B-Q6_K.gguf`, `Qwen3-Embedding-4B-f16.gguf` | Other quantizations in Qwen/Qwen3-Embedding-4B-GGUF, from 2496703776 bytes (Q4_K_M) to 8049889824 (f16), from metadata. | listed | A llama.cpp server | Read when the 4B size is wanted at lower memory. |
| `Qwen3-Embedding-4B` safetensors | The repository's two BF16 shards, 4021774336 parameters. | listed | `transformers` `4.51.0` or later and a GPU | Read when a task needs the unquantized model. |
| `Qwen3-Embedding-0.6B` | The 0.6B size, 1024 numbers, 32K sequence length; official GGUF repository with `Qwen3-Embedding-0.6B-Q8_0.gguf` and `Qwen3-Embedding-0.6B-f16.gguf` (revision `97b0c61`). | listed | A llama.cpp server for the GGUF | Read when a model between 270M and 4B is wanted. |
| `Qwen3-Embedding-8B` | The 8B size, 4096 numbers; the card says it ranks No.1 on the MTEB multilingual leaderboard (as of June 5, 2025, score 70.58); official GGUF repository with `Qwen3-Embedding-8B-Q8_0.gguf` at 8047105824 bytes (revision `1d8ad4c`). | listed | A llama.cpp server and the memory for the 8047105824-byte file | Read only after the 4B size shows a gain on a larger body of text. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-13 | Benchmark a larger embedding model for hybrid search over two Markdown knowledge-base roots | `Qwen3-Embedding-4B-Q8_0.gguf` | Recall 0.95/0.98 vectors only, 0.95/1.00 with words, translations and vectors; nothing measurable gained over the chosen 270M model. | Index 5,969 s at most, 5.0 GB | [trial record](../../raw/notes/trials/2026-11-21-qwen3-embedding-4b-q8-0-llama-server-index.md) |

## Verdict

Rejected for this kit on this set: the 4B build did not beat the 270M model with words and translations, indexed 13,090 chunks in up to 5,969 s against 357 s, and its cost per chunk grows with every added page (up to 13 h for a full pass at 100,000 chunks). Its other sizes were not run. Revisit when a larger body of questions shows at least 3 more questions at recall@5 than the chosen model, or when a much faster runtime for it appears.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; local embedding models and runtimes
- [[google-embeddinggemma-2|google/embeddinggemma-2]] (../references/google-embeddinggemma-2.md): the chosen model
- [[baai-bge-m3|BAAI/bge-m3]] (../references/baai-bge-m3.md): the runner-up

## Sources

- [Desk check: Qwen/Qwen3-Embedding-4B revision 5cf2132](../../raw/repos/qwen-qwen3-embedding-4b-desk-check-2026-11-21.md): the model card and API metadata read, GGUF files and other sizes listed, the reason for `rejected`.
- [Trial record: Qwen3-Embedding-4B Q8_0 on llama-server](../../raw/notes/trials/2026-11-21-qwen3-embedding-4b-q8-0-llama-server-index.md): the run behind the Tried row.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): recall, speed, memory and growth check, retold.
