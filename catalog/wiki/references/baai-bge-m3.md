---
title: "BAAI/bge-m3"
category: reference
kind: model
areas: [search-and-embeddings]
url: https://huggingface.co/BAAI/bge-m3
version: "5617a9f"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/baai-bge-m3-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-bge-m3-q8-0-llama-server-index.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, kind-model, embeddings, search, multilingual, gguf]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "BAAI's multilingual embedding model (1024 numbers, 8192 tokens). Its Q8_0 GGUF was measured on the kit's question set and is the runner-up behind EmbeddingGemma 2: within one question on recall, slower to index and larger. Kept as the first challenger to re-run on a larger body; other quantizations and the sparse heads are listed."
---

# BAAI/bge-m3

> A Hugging Face model (kind `model`, licence MIT, revision `5617a9f` read): a multilingual embedding model that does dense, sparse and multi-vector retrieval; the dense mode gives 1024 numbers per text. Its Q8_0 GGUF was measured and is the runner-up (`reference`) behind EmbeddingGemma 2; the model is not in use.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Embed text for search by meaning in a local knowledge base, as the challenger to the chosen model | `bge-m3-q8_0.gguf` | search-and-embeddings |
| Embed with a model that needs no query prompt and takes inputs up to 8192 tokens | `bge-m3-q8_0.gguf` | search-and-embeddings |
| Lexical-weight or multi-vector (ColBERT-style) retrieval from one multilingual model | `sparse_linear.pt` and `colbert_linear.pt` | search-and-embeddings |

## Run it here

- **No clone.** Read the card with `curl -s https://huggingface.co/BAAI/bge-m3/raw/main/README.md` and the metadata with `https://huggingface.co/api/models/BAAI/bge-m3`; the desk check read both at revision `5617a9f`.
- **To re-run the comparison** (only with the user's yes, on a larger body of questions): the kit's preset names it `bge-m3` with the Ollama model `bge-m3:567m`; `search.py embed-setup --preset bge-m3`, then `search.py index` and `search.py eval`. The model was run here as the Q8_0 GGUF on llama.cpp `llama-server`, not through that tag.
- **Switch off**: nothing runs unless the preset is set; `search.py embed-setup --off` removes it. No outbound call while running; a download contacts the publisher once.
- **Do not install**: FlagEmbedding or a `pip install -e .` from a clone, which the card's example uses; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `bge-m3-q8_0.gguf` | Q8_0 GGUF, 634553760 bytes (635 MB): recall 0.95/0.95 vectors only and 0.98/1.00 with words and translations; index 587 s (6.0k tokens/s), 765 MB, 15.5 ms per query on llama-server. | reference | A llama.cpp server and the 635 MB file; Apple M4 Pro (Metal) in the trial | Consult when the kit has a much larger body of questions (re-run `eval`; switch when it finds at least 3 more questions at recall@5). |
| `bge-m3-FP16.gguf`, `bge-m3-Q2_K.gguf`, `bge-m3-Q3_K.gguf`, `bge-m3-Q4_0.gguf`, `bge-m3-Q4_K_M.gguf`, `bge-m3-Q5_0.gguf`, `bge-m3-Q5_K_M.gguf`, `bge-m3-Q6_K.gguf` | Other quantizations in gpustack/bge-m3-GGUF, from 366114880 bytes (Q2_K) to 1157671200 (FP16), from metadata. | listed | A llama.cpp server | Read when the 8-bit file is too large or its recall is in doubt. |
| `pytorch_model.bin` and `onnx/` | Original weights (568M parameters per the measurements) and an ONNX export in this repository. | listed | A GPU or CPU pass with `transformers`, or ONNX Runtime | Read when a task cannot use a server. |
| `sparse_linear.pt` and `colbert_linear.pt` | The card's lexical-weight and multi-vector heads. | listed | FlagEmbedding; Ollama's endpoint returns only the dense vector | Read when a task needs sparse or ColBERT-style scores from one model. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-13 | Benchmark an embedding model for hybrid search over two Markdown knowledge-base roots | `bge-m3-q8_0.gguf` | Recall 0.95/0.95 vectors only, 0.98/1.00 with words and translations: within one question of EmbeddingGemma 2, slower to index, larger. | Index 587 s, 765 MB | [trial record](../../raw/notes/trials/2026-11-21-bge-m3-q8-0-llama-server-index.md) |

## Verdict

The runner-up, not the choice: it found one more question at recall@5 on vectors only (0.95 against 0.93) and ties with words and translations, but it indexed in 587 s against 357 s, takes 635 MB against 310 MB, makes 2 KB vectors against 1.5 KB and lacks Matryoshka truncation, which is the first lever for a very large root. Revisit when a larger body of questions is ready: re-run it against EmbeddingGemma 2 and switch only on a gain of at least 3 questions at recall@5.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; local embedding models and runtimes
- [[google-embeddinggemma-2|google/embeddinggemma-2]] (../references/google-embeddinggemma-2.md): the chosen model
- [[qwen-qwen3-embedding-4b|Qwen/Qwen3-Embedding-4B]] (../references/qwen-qwen3-embedding-4b.md): the larger model, rejected
- [[ollama-ollama|ollama/ollama]] (../references/ollama-ollama.md): the runtime behind the kit's preset

## Sources

- [Desk check: BAAI/bge-m3 revision 5617a9f](../../raw/repos/baai-bge-m3-desk-check-2026-11-21.md): the model card and API metadata read, GGUF files listed, the reason for `reference`.
- [Trial record: bge-m3 Q8_0 on llama-server](../../raw/notes/trials/2026-11-21-bge-m3-q8-0-llama-server-index.md): the run behind the Tried row.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): recall, speed, memory and the choice, retold.
