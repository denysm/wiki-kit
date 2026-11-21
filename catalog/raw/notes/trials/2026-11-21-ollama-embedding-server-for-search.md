---
title: "Use record: Ollama app as the local embedding server for search by meaning"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-14
ingested: 2026-11-21
repo: ollama/ollama
part: "serve"
version: "0.40.16"
status: in use
tags: [catalog, trial, use-record, kind-app, ollama, embeddings, search]
summary: "The Ollama app 0.40.16 from ollama.com, not Homebrew, serves the embedding model embeddinggemma-2:270m-q8_0-text for the kit's search.py and was kept always on: pull 24 s, index of both roots 442 s, whole query 0.183 s with vectors. Retold from the measurement note."
---

# Use record: Ollama app as the local embedding server

Task, by kind: serve a small embedding model on one Mac for search by meaning over Markdown knowledge bases, always on, with nothing leaving the machine. Retold from `../2026-11-21-measurements-local-embeddings.md`.

## What is used

The Ollama app 0.40.16 from ollama.com (notarized Developer ID), copied to `/Applications`. On first start it created `/usr/local/bin/ollama` as a link to `Ollama.app/Contents/Resources/ollama` and runs `ollama serve` from the menu bar. The commands used: `serve` (through the app), `pull` for the embedding model, `stop` to unload it for one timing; `search.py` calls the OpenAI-style `/v1/embeddings` endpoint on port 11434.

The first route was Homebrew (`brew install ollama` 0.40.16): it also installed MLX, python@3.15 and seven more formulas (454 MB with Ollama itself) and made Python 3.15 the default `python3`. It was removed (`brew uninstall ollama mlx-c mlx`); Homebrew 7 then autoremoved `python@3.15`, which was reinstalled on request.

## Result

- `pull` 24 s; `embed-setup` ok (768 numbers); `index` of both roots 442 s; `eval` with variants 43/44 at recall@5 and 44/44 at recall@10.
- Whole `search.py query` process, median of 10 runs: words only 0.112 s, with vectors 0.183 s, after `ollama stop` unloaded the model 0.820 s, the first query after the app starts 0.80 s, with the server down 0.134 s and the note "words only".
- Memory: the app 130 MB, `ollama serve` 36 MB, and while the model is loaded its llama-server 472 MB; the model is unloaded after 5 idle minutes by default.
- Earlier runtime comparison on the same model: Ollama 0.40.16 took 439 s, one slot by default, 15.5 ms per query, 1.5 s cold start; its vectors equal llama-server's (mean cosine 1.0000).

## Cost

442 s for the first index of both roots, then seconds per new file; the memory above; no tokens spent on any model API.

## Not checked

Whether the app starts at login; a clean Mac (this Mac had Homebrew); Windows; Linux. The app was not re-measured at 0.40.17.
