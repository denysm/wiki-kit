---
title: "ollama/ollama"
category: reference
kind: app
areas: [search-and-embeddings, knowledge-bases]
repo: ollama/ollama
version: "0.40.17"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/ollama-ollama-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, area-knowledge-bases, kind-app, ollama, embeddings, runtime, local-models]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "App and CLI that runs open models locally and serves them over HTTP on localhost port 11434. The app 0.40.16 from ollama.com is in use as the embedding server for the kit's search by meaning (serve, pull, the OpenAI-style /v1/embeddings endpoint); the other commands are read or listed. Read at v0.40.17: it checks for updates hourly, pulls models over HTTPS, and its cloud features can be switched off."
---

# ollama/ollama

> A local model runner (kind `app`, licence MIT, version `0.40.17` read in a clone; the app in use is `0.40.16`): a CLI plus a macOS and Windows app that run open models and serve them over HTTP on localhost port 11434. Here the app from ollama.com, not Homebrew, serves the embedding model for the kit's search by meaning.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Serve a small embedding model to local programs over HTTP, with no data leaving the machine | `serve` | search-and-embeddings |
| Add search by meaning to an agent-maintained knowledge base through a local embedding server | `/v1/embeddings` | knowledge-bases |
| Download an embedding model once and keep it local | `pull` | search-and-embeddings |
| Get embeddings through an OpenAI-style call, so any client that speaks it works | `/v1/embeddings` | search-and-embeddings |
| Get embeddings through the native call (batches, truncation, dimensions, keep-alive) | `POST /api/embed` | search-and-embeddings |
| Free the model's memory at once, or see what is loaded | `stop` | search-and-embeddings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone --depth 1 --branch v0.40.17 https://github.com/ollama/ollama $EXTERNAL/ollama`. Never build or edit it. Read first: `docs/faq.mdx`, then `docs/cli.mdx`, `docs/api.md` and `docs/macos.mdx`.
- **In use**: the app `0.40.16` downloaded from ollama.com, not Homebrew: the Homebrew formula also installed MLX, python@3.15 and seven more formulas (454 MB with Ollama itself) and made Python 3.15 the default `python3`. The app runs `ollama serve` from the menu bar and serves the Ollama tag `embeddinggemma-2:270m-q8_0-text` to `search.py` through `/v1/embeddings`. The tag read is `0.40.17`, one release newer than the app in use: re-check before relying on it.
- **Listens on**: localhost, port 11434, by default; `OLLAMA_HOST` changes it, and nothing here exposes it on a network.
- **Sends outward**: model pulls over HTTPS to a registry (default allowed host `ollama.com`; `HTTPS_PROXY` redirects them); an update check of the app every hour to `https://ollama.com/api/update`, carrying the operating system, architecture, version and, on macOS, a device id; Ollama's cloud models and web search only after `ollama signin`. A grep of the Go sources and docs found no telemetry or analytics code in the server or app. Read in the docs and the updater code, not observed on the wire.
- **Switch off**: cloud features with `OLLAMA_NO_CLOUD=1` or `"disable_ollama_cloud": true` in `~/.ollama/server.json`; the automatic update download with the app Settings switch "Auto-download updates", which does not stop the hourly check (no setting for the check was found); model memory with `OLLAMA_KEEP_ALIVE` or `ollama stop`.
- **Do not install**: with `curl ... | sh`, `irm ... | iex`, Homebrew or the Docker image; real installation of the app waits for the user's yes. Not checked: whether the app starts at login, a clean Mac, Windows, Linux.

## What's inside

Parts are commands and the embeddings API. Defined in `cmd/cmd.go` and `cmd/launch/launch.go`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `serve` | "Start Ollama": the HTTP server on port 11434; alias `start`; the macOS app runs it from the menu bar. | in use | The app `0.40.16` (130 MB; `ollama serve` 36 MB) | Re-check when a new app version ships (compare the latest release with `0.40.16` and the hourly update check's behaviour). |
| `pull` | "Pull a model from a registry"; used for the embedding model (24 s). | in use | Outbound HTTPS once; 304 MB for the in-use tag | Re-check when the model tag changes. |
| `/v1/embeddings` | OpenAI-compatible endpoint: `model`, `input` (string or array of strings), `encoding format`, `dimensions`; the call `search.py` makes. | in use | The server running; the model loaded (472 MB, unloaded after 5 idle minutes) | Re-check when the docs change the supported fields or `search.py` changes its call. |
| `stop` | "Stop a running model": unloads it from memory at once. | tried | The server running | The real task: freeing memory before another heavy job on the same machine. |
| `POST /api/embed` | Native embeddings call: `model`, `input` (text, list, or media objects), `truncate` (default true), `keep_alive` (default `5m`), `dimensions`; returns `embeddings`. | candidate | The server running | Try it when a client needs batching or multimodal input that `/v1/embeddings` lacks. |
| `run` | "Run a model": chat or one prompt; for an embedding model it prints a JSON array. | candidate | The server and a pulled model | Try it for a one-off embedding from a shell. |
| `list` (alias `ls`) | "List models". | candidate | Nothing beyond the CLI | Try it to check which tags are pulled. |
| `ps` | "List running models": size, processor and when each unloads. | candidate | The server running | Try it to see whether the embedding model is loaded. |
| `rm` | "Remove a model". | candidate | Nothing beyond the CLI | Try it when a replaced model tag must go. |
| `show` | "Show information for a model". | candidate | A pulled model | Try it to read a tag's details. |
| `cp` | "Copy a model" under a new name. | candidate | A pulled model | Try it before editing a model's Modelfile. |
| `create` | "Create a model" from a `Modelfile`. | candidate | A Modelfile and a base model | Try it when a custom model with fixed parameters is needed. |
| `push` | "Push a model to a registry"; needs an ollama.com account. | listed | An account; data leaves the machine | Read when a model must be shared. |
| `signin`, `signout` (hidden aliases `login`, `logout`) | Sign in to and out of ollama.com; ties the install to cloud models, private pulls and pushes. | listed | An account; data leaves the machine | Read when cloud models are wanted; not for local search. |
| `launch` | "Launch the Ollama menu or an integration": starts external coding tools against Ollama models and can write their configuration. | listed | The server; may change another tool's settings | Read when a coding tool must run on a local model. |
| `/api/embeddings` | Legacy embeddings endpoint, "superseded by `/api/embed`". | listed | The server running | Read only to port an old client. |
| `runner`, `gpu-discover` | Hidden commands (a model runner and GPU discovery); not for direct use. | listed | Nothing | Read when debugging model loading. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-14 | Serve an embedding model on one Mac, always on | `serve` | In use: the app `0.40.16` from ollama.com; first query after app start 0.80 s; with the server down search falls back to words in 0.134 s. | 130 MB app, 36 MB `ollama serve` | [use record](../../raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md) |
| 2026-11-14 | Download the embedding model | `pull` | In use; the tag pulled in 24 s. | Outbound HTTPS once | [use record](../../raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md) |
| 2026-11-14 | Call the server from a search script | `/v1/embeddings` | In use: index of both roots 442 s; `eval` with variants 43/44 at recall@5. | 472 MB while the model is loaded | [use record](../../raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md) |
| 2026-11-14 | Time the first query after unloading the model | `stop` | After `ollama stop` the whole query took 0.820 s against 0.183 s warm. | none beyond the timing | [use record](../../raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md) |

## Verdict

Ollama is the runtime of the kit's search by meaning: the app, not Homebrew, serving one 304 MB model on localhost. Three parts are in use and the rest of the CLI is read, not run. Known cost: the app checks for updates every hour and no switch for the check was found, only for the download and for cloud features. Revisit when the latest release passes `0.40.16` (re-check the in-use parts), when the updater changes, or when the tested route (one Mac with Homebrew before) is tried on a clean Mac, Windows or Linux.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; local embedding models and the runtimes that serve them
- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page; the server behind search over the articles
- [[google-embeddinggemma-2|google/embeddinggemma-2]] (../references/google-embeddinggemma-2.md): the model it serves
- [[baai-bge-m3|BAAI/bge-m3]] (../references/baai-bge-m3.md): the runner-up model

## Sources

- [Desk check: ollama/ollama v0.40.17](../../raw/repos/ollama-ollama-desk-check-2026-11-21.md): commands, docs and updater read from the clone, freshness through the GitHub API, what it listens on and sends.
- [Use record: Ollama app as the local embedding server](../../raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md): the real use behind `in use` and the Tried rows.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): runtime comparison, memory, timings and the Homebrew finding, retold.
