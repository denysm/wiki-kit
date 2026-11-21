---
title: "Desk check: BAAI/bge-m3 revision 5617a9f"
source: https://huggingface.co/BAAI/bge-m3/tree/5617a9f61b028005a4858fdac845db406aefb181
type: repos
authors: ["BAAI"]
source_date: 2024-07-03
ingested: 2026-11-21
url: https://huggingface.co/BAAI/bge-m3
kind: model
version: "5617a9f"
licence: MIT
tags: [catalog, desk-check, kind-model, embeddings, search, huggingface]
summary: "bge-m3 read from its Hugging Face model card and API metadata at revision 5617a9f: a multilingual dense, sparse and multi-vector embedding model, 1024 numbers, 8192 tokens; its GGUF Q8_0 file and other quantizations; why the Q8_0 build is kept as the measured runner-up behind EmbeddingGemma 2. No weights downloaded."
---

# Desk check: BAAI/bge-m3 revision 5617a9f

## Repository facts

- Model page: https://huggingface.co/BAAI/bge-m3, revision read `5617a9f61b028005a4858fdac845db406aefb181` (short form `5617a9f`). Author: BAAI. Not gated.
- Licence: the card header says `license: mit` and the API tag is `license:mit`; there is no separate licence file in the repository listing, so the licence is read from the card and the tag.
- The card's words: "It can simultaneously perform the three common retrieval functionalities of embedding model: dense retrieval, multi-vector retrieval, and sparse retrieval", "support more than 100 working languages", inputs "up to 8192 tokens".
- Its table gives dimension 1024 and sequence length 8192 for `BAAI/bge-m3`. The model "no longer requires adding instructions to the queries".
- Files in the model repository: `pytorch_model.bin`, `sparse_linear.pt`, `colbert_linear.pt`, tokenizer files, an `onnx/` folder (`model.onnx`, `model.onnx_data`, tokenizer files), sentence-transformers configs. No GGUF in this repository.
- The card's usage example installs FlagEmbedding from a git clone and `pip install -e .`; that route is not used here.

## Freshness (checked 2026-11-21)

Through the Hugging Face API: created 2024-01-27, last modified 2024-07-03. Not gated. The model is older than the measurements and has had no change since mid-2024; the card's own news line says the MIRACL results were updated on 2024/7/1.

## How to run here

- No clone: `curl -s https://huggingface.co/BAAI/bge-m3/raw/main/README.md` and `https://huggingface.co/api/models/BAAI/bge-m3`. Do not download the weights to read the card.
- What was run here is the Q8_0 GGUF on llama.cpp `llama-server` 0.7.0 (Metal) for a measurement; see the trial record. Ollama carries the model as `bge-m3:567m`, the tag the kit's `search.py` preset names for it; that tag was not run, only the GGUF.
- Outbound calls: none while running locally; a pull or download contacts the publisher once.
- Do not install: FlagEmbedding, or `pip install -e .` from a clone, to read the card or to run the dense vectors; the sparse and multi-vector outputs need that library and the kit uses neither.

## Parts

### Q8_0 GGUF `bge-m3-q8_0.gguf` (ggml-org/bge-m3-Q8_0-GGUF, revision `9eba04c`, MIT; also in gpustack/bge-m3-GGUF as `bge-m3-Q8_0.gguf`)

Size 634553760 bytes in both listings, consistent with the 635 MB the measurement note gives. The note's figures for the Q8_0 run (MIT, 568M, 1024 dims, 635 MB): recall 0.95/0.95 vectors only and 0.98/1.00 with words and translations; index 587 s (6.0k tokens/s), 765 MB, 15.5 ms per query on llama-server. Trial record: `raw/notes/trials/2026-11-21-bge-m3-q8-0-llama-server-index.md`.

Status basis for `reference` (retold without names): this is the measured runner-up. It found one more question than EmbeddingGemma 2 at recall@5 on vectors only (0.95 against 0.93) and is equal with words and translations (0.98/1.00 both), but it indexes slower (587 s against 357 s for the same hardware and server), takes more memory (765 MB against 656 MB) and is twice the download (635 MB against 310 MB; the note: "half the download"), and its 1024-number vectors take 2 KB per chunk against 1.5 KB. It also lacks Matryoshka truncation, which the first scaling lever for a very large root needs. The note's rule for switching: when a larger body of questions shows the challenger finding at least 3 more questions at recall@5, the bar vectors themselves had to clear (`ollama pull bge-m3:567m`, `embed-setup --preset bge-m3`, `index`, `eval`).

### Other GGUF quantizations (gpustack/bge-m3-GGUF, revision `2d48f17`, MIT)

From the file listing, not read or tried, in bytes: `bge-m3-FP16.gguf` 1157671200, `bge-m3-Q2_K.gguf` 366114880, `bge-m3-Q3_K.gguf` 402290752, `bge-m3-Q4_0.gguf` 421558336, `bge-m3-Q4_K_M.gguf` 437778496, `bge-m3-Q5_0.gguf` 459307072, `bge-m3-Q5_K_M.gguf` 467662912, `bge-m3-Q6_K.gguf` 499415104.

### Original weights `pytorch_model.bin` and the `onnx/` folder (this repository)

`pytorch_model.bin` and an ONNX export in `onnx/`; the note gives 568M parameters. Not tried. The ONNX Runtime route was rejected for EmbeddingGemma 2 on the same grounds (see its desk check).

### Sparse and multi-vector heads `sparse_linear.pt` and `colbert_linear.pt`

The card's second and third retrieval modes (lexical weights, ColBERT-style vectors). They need FlagEmbedding, and Ollama's embedding endpoint returns only the dense vector, so the kit does not use them. Not tried.

## Reasons for any rejection or reference status

Reference: measured runner-up, within one question of the chosen model, slower to index, larger, no Matryoshka; kept as the first challenger to re-run.

## How the kit uses it

`search.py` ships a preset for it (`bge-m3`, model name `bge-m3:567m`, no prompts); the chosen model is EmbeddingGemma 2. Numbers: `raw/notes/2026-11-21-measurements-local-embeddings.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 42 model calls on sonnet, $1.95 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
