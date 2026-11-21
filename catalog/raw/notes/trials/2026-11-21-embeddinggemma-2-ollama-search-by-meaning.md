---
title: "Use record: EmbeddingGemma 2 through Ollama, search by meaning over Markdown knowledge bases"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-14
ingested: 2026-11-21
url: https://huggingface.co/google/embeddinggemma-2
part: "Ollama tag embeddinggemma-2:270m-q8_0-text"
version: "f9972ac"
status: in use
tags: [catalog, trial, use-record, kind-model, embeddings, search, ollama]
summary: "EmbeddingGemma 2 as the Ollama tag embeddinggemma-2:270m-q8_0-text is in real use as the embedding model of the kit's search.py: chosen on recall measured on 44 questions, indexed two knowledge-base roots in 442 s, and kept always on. Facts retold from raw/notes/2026-11-21-measurements-local-embeddings.md."
---

# Use record: EmbeddingGemma 2 through Ollama, search by meaning

Task, by kind: find pages of a Markdown knowledge base that are written in other words or in another language than the question, on one machine with no data leaving it. All facts below are retold from `../2026-11-21-measurements-local-embeddings.md`.

## What is used

The Ollama tag `embeddinggemma-2:270m-q8_0-text` (304 MB), served by the Ollama app 0.40.16 (see the Ollama use record), called by `search.py` through the OpenAI-style embeddings endpoint. Model revision on Hugging Face read by the desk check: `f9972ac`. Query prompt `task: search result | query: {text}`, document prompt `title: {title} | text: {text}`. `search.py embed-setup` writes the config.

## Result

- Recall@5/@10 on 44 questions (21 of them cross-language): words 0.73/0.77, vectors only 0.93/0.95, words plus vectors 0.93/0.98, words, translations and vectors 0.98/1.00. The threshold was fixed before the runs: vectors had to add at least 3 questions at recall@5; they added more (43 questions against 40).
- Runs on the Ollama app 0.40.16: `pull` 24 s, index of both roots 442 s, `eval` with variants 43/44 at recall@5 and 44/44 at recall@10.
- Whole `search.py query` process, median of 10 runs: words only 0.112 s, with vectors 0.183 s; after the model was unloaded 0.820 s.
- Memory while loaded: the model's llama-server 472 MB; Ollama unloads it after 5 idle minutes by default.
- Choice against bge-m3: within one question, 1.6 times faster to index, half the download.

## Cost

Index of both roots 442 s once; day to day only new chunks are embedded. Memory as above. No tokens spent on any model API.

## Not checked

A clean Mac, Windows, Linux; MLX as the runtime; 4-bit weights. A newer model is worth switching to only when `search.py eval` shows a gain.
