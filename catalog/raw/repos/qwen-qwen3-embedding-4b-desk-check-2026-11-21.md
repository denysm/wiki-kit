---
title: "Desk check: Qwen/Qwen3-Embedding-4B revision 5cf2132"
source: https://huggingface.co/Qwen/Qwen3-Embedding-4B/tree/5cf2132abc99cad020ac570b19d031efec650f2b
type: repos
authors: ["Qwen team"]
source_date: 2025-06-20
ingested: 2026-11-21
url: https://huggingface.co/Qwen/Qwen3-Embedding-4B
kind: model
version: "5cf2132"
licence: Apache-2.0
tags: [catalog, desk-check, kind-model, embeddings, search, huggingface]
summary: "Qwen3-Embedding-4B read from its Hugging Face model card and API metadata at revision 5cf2132: a 4B text embedding model, up to 2560 numbers, 32k context, in a 0.6B, 4B, 8B series; its official GGUF files; why the Q8_0 build is rejected for this kit (nothing measurable gained, far slower). No weights downloaded."
---

# Desk check: Qwen/Qwen3-Embedding-4B revision 5cf2132

## Repository facts

- Model page: https://huggingface.co/Qwen/Qwen3-Embedding-4B, revision read `5cf2132abc99cad020ac570b19d031efec650f2b` (short form `5cf2132`). Author: Qwen. Base model `Qwen/Qwen3-4B-Base`. Not gated.
- Licence: the card header says `license: apache-2.0` and the API tag is `license:apache-2.0`; no separate licence file in the repository listing, so the licence is read from the card and the tag.
- The card's overview: model type text embedding, 100+ languages, 4B parameters, context length 32k, "Embedding Dimension: Up to 2560, supports user-defined output dimensions ranging from 32 to 2560". It is instruction aware: queries come with a one-sentence task instruction (`Instruct: {task}` then `Query:{query}`), documents without one; the card says instructions typically give "an improvement of 1% to 5%".
- The series table lists text embedding sizes 0.6B (28 layers, 1024 numbers), 4B (36 layers, 2560) and 8B (36 layers, 4096), all with 32K sequence length, plus rerankers in 0.6B, 4B and 8B. The card says the 8B embedding model ranks No.1 on the MTEB multilingual leaderboard as of June 5, 2025, score 70.58.
- Files in the model repository: two safetensors shards (4021774336 parameters in BF16 per the API), tokenizer files, sentence-transformers configs. No GGUF in this repository.
- The card's usage examples use `transformers` (4.51.0 or later) with `last_token_pool` and left padding.

## Freshness (checked 2026-11-21)

Through the Hugging Face API: created 2025-06-03, last modified 2025-06-20. Not gated. Older than the measurements; the series' official GGUF repositories exist (below).

## How to run here

- No clone: `curl -s https://huggingface.co/Qwen/Qwen3-Embedding-4B/raw/main/README.md` and `https://huggingface.co/api/models/Qwen/Qwen3-Embedding-4B`. Do not download the weights to read the card.
- What was run here is the Q8_0 GGUF on llama.cpp `llama-server` 0.7.0 (Metal) for one measurement; see the trial record. It needs 5.0 GB of server memory, so run it only on a machine with room and only on request.
- Outbound calls: none while running locally; a download contacts the publisher once.
- Do not install: `transformers`, `sentence-transformers` or a GPU stack to read the card or to run it; real installation waits for the user's yes.

## Parts

### Q8_0 GGUF `Qwen3-Embedding-4B-Q8_0.gguf` (Qwen/Qwen3-Embedding-4B-GGUF, revision `f460253`, Apache-2.0)

Size 4279660224 bytes, consistent with the 4.3 GB the measurement note gives. The note's figures for the Q8_0 run (Apache-2.0, 2560 dims, 4.3 GB): recall 0.95/0.98 vectors only and 0.95/1.00 with words, translations and vectors (words plus vectors 0.91/0.98); index 5,969 s (about 0.6k tokens/s; for 44 minutes the GPU was shared with another run, so an upper bound), 5.0 GB, 100 ms per query on llama-server. Trial record: `raw/notes/trials/2026-11-21-qwen3-embedding-4b-q8-0-llama-server-index.md`.

Reason for `rejected` (retold without names): on the measured question set the larger model bought nothing measurable. It found as many questions as bge-m3 on vectors only (0.95) and fewer with words, translations and vectors (0.95/1.00 against 0.98/1.00 for the 270M model), while indexing 13,090 chunks took 5,969 s against 357 s, memory was 5.0 GB against 656 MB and a query took 100 ms against 13 ms. Growth check from the same note: a full embedding pass up to 456 ms per chunk, so at 100,000 chunks up to 13 h and at 1,000,000 chunks up to 5 days; vectors of 5 KB per chunk; pure scoring cost grows with 2560 numbers. "On a machine that can run it, the larger model bought nothing measurable on this set."

### Other GGUF files in Qwen/Qwen3-Embedding-4B-GGUF

From the file listing, not tried, in bytes: `Qwen3-Embedding-4B-Q4_K_M.gguf` 2496703776, `Qwen3-Embedding-4B-Q5_0.gguf` 2823134496, `Qwen3-Embedding-4B-Q5_K_M.gguf` 2888936736, `Qwen3-Embedding-4B-Q6_K.gguf` 3305684256, `Qwen3-Embedding-4B-f16.gguf` 8049889824.

### Safetensors shards (this repository)

BF16, 4021774336 parameters in two shards. Not tried.

### Other sizes: Qwen3-Embedding-0.6B and Qwen3-Embedding-8B

Taken from the card's series table and the API, not read beyond that, not tried. `Qwen/Qwen3-Embedding-0.6B`: revision `97b0c61`, Apache-2.0, 1024 numbers; an official GGUF repository `Qwen/Qwen3-Embedding-0.6B-GGUF` has `Qwen3-Embedding-0.6B-Q8_0.gguf` and `Qwen3-Embedding-0.6B-f16.gguf`. `Qwen/Qwen3-Embedding-8B`: revision `1d8ad4c`, Apache-2.0, 4096 numbers; official GGUF repository `Qwen/Qwen3-Embedding-8B-GGUF` with `Qwen3-Embedding-8B-Q8_0.gguf` at 8047105824 bytes. The measurement note did not run either.

## Reasons for any rejection or reference status

Rejected: the Q8_0 4B build, for the reasons above (no measurable gain on this set, far slower and larger, cost per chunk grows with the corpus). Revisit condition: a body of text on which `search.py eval` shows it finding at least 3 more questions at recall@5 than the chosen model, or a much faster runtime for it.

## How the kit uses it

Not used. The kit has no preset for it.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 42 model calls on sonnet, $1.95 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
