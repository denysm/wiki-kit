---
title: "Desk check: ollama/ollama v0.40.17"
source: https://github.com/ollama/ollama/tree/v0.40.17
type: repos
authors: ["Ollama contributors"]
source_date: 2026-11-10
ingested: 2026-11-21
repo: ollama/ollama
kind: app
version: "0.40.17"
licence: MIT
tags: [catalog, desk-check, kind-app, ollama, embeddings, runtime, local-models]
summary: "Ollama v0.40.17 read from a read-only clone: its commands from cmd/ and the docs, the embeddings API, what the server listens on (localhost port 11434), what the app sends outward (hourly update check, model pulls, optional cloud) and how to switch off what can be; the kit runs the app 0.40.16 from ollama.com as its embedding server."
---

# Desk check: ollama/ollama v0.40.17

## Repository facts

- Repository https://github.com/ollama/ollama read at tag `v0.40.17` in a read-only clone at `$EXTERNAL/ollama` (`git describe --tags` gives `v0.40.17`, working tree clean). Go module `github.com/ollama/ollama`, `go 1.26.10`. Entry point `main.go`; command definitions in `cmd/cmd.go`; the desktop app for macOS and Windows in `app/`; docs in `docs/`.
- Licence file `LICENSE`: "MIT License", "Copyright (c) Ollama". GitHub reports MIT; they agree.
- The README's own description: "Start building with open models. Access the latest releases locally or in the cloud with complete privacy." Under "Supported backends" it names one: llama.cpp (`LLAMA_CPP_VERSION` file holds `b12257`).
- The README installs with `curl -fsSL https://ollama.com/install.sh | sh` on macOS and Linux and `irm https://ollama.com/install.ps1 | iex` on Windows, or by downloading `Ollama.dmg` or `OllamaSetup.exe`. A Docker image `ollama/ollama` exists.
- Docs: `docs/cli.mdx`, `docs/api.md`, `docs/faq.mdx`, `docs/macos.mdx`, `docs/capabilities/embeddings.mdx`, `docs/api/openai-compatibility.mdx`, `docs/cloud/faq.mdx`.

## Freshness (checked 2026-11-21 through `gh api`)

- `pushed_at`: 2026-11-21T04:05:50Z. Archived: false. Default branch `main`.
- Latest release: `v0.40.17`, published 2026-11-10T22:25:00Z, not a prerelease. The kit runs the app 0.40.16 (the use record), one release behind the tag read; the in-use app was not re-measured at 0.40.17.
- Licence as GitHub reports it: MIT; as read from the file: MIT.

## How to run here

- **Clone, read-only, only to read docs**: `git clone --depth 1 --branch v0.40.17 https://github.com/ollama/ollama $EXTERNAL/ollama`. Never build or edit it; the app is not run from the clone.
- **What runs**: the Ollama app 0.40.16 downloaded from ollama.com, not Homebrew. The measurement note: `brew install ollama` 0.40.16 also installed MLX, python@3.15 and seven more formulas (454 MB with Ollama itself) and made Python 3.15 the default `python3`; removing the formula later removed that Python too. The kit's QUICKSTART says the same: on a Mac take the app from the site.
- **Listens on**: by default the server binds the loopback address on port 11434 (the FAQ section "How can I expose Ollama on my network?"; reached as localhost, port 11434). `OLLAMA_HOST` changes the bind address; exposing it on a network is the docs' own FAQ topic and is not done here. Cross-origin requests are allowed from loopback and unspecified addresses by default; `OLLAMA_ORIGINS` adds more.
- **Sends outward** (read in the docs and in `app/updater/updater.go`, not observed on the wire):
  - Model pulls: `ollama pull` fetches from a registry over HTTPS ("Ollama does not use HTTP for model pulls, only HTTPS"); `HTTPS_PROXY` redirects it. `OLLAMA_REMOTES` is the allowed hosts for remote models, default `ollama.com`. After the pull the model is local.
  - Update check (macOS and Windows app): `UpdateCheckURLBase` is `https://ollama.com/api/update`, checked every `60 * 60 * time.Second` after an initial delay of 3 seconds. The request carries `os`, `arch`, `version`, a timestamp and a nonce; on macOS also a device id; it is signed with the server key when one exists. The code comment says "Always check for updates". The setting `AutoUpdateEnabled` (default on in the settings table) only decides whether the update is downloaded.
  - Cloud: signing in (`ollama signin`) lets the local install run models hosted in Ollama's cloud and web search; without it nothing is sent there. The local FAQ says: "Ollama runs locally. We don't see your prompts or data when you run locally."
  - Telemetry: a search of the Go sources and docs for "telemetry", "analytics", "posthog" and "segment" found none in the server or app; the hits were in launch integrations and unrelated code. This is a grep, not a proof.
- **Switch off**:
  - Cloud features and web search: `OLLAMA_NO_CLOUD=1`, or `"disable_ollama_cloud": true` in `~/.ollama/server.json`; restart; the logs then show `Ollama cloud disabled: true` (docs/faq.mdx).
  - Automatic update download: the app's Settings switch labelled "Auto-download updates" (macOS and Windows). It stops the download, not the hourly check, per the updater code; when off, the app still shows a tray notification that an update is ready.
  - The hourly update check itself: no setting for it found in the docs or the updater code.
  - Model unloading: models stay in memory 5 minutes by default; `OLLAMA_KEEP_ALIVE`, the `keep_alive` request parameter, or `ollama stop <model>` change that.
  - On a Mac, environment variables for the app are set with `launchctl setenv` and the app is restarted (docs/faq.mdx).
- **Do not install**: via `curl ... | sh` or `irm ... | iex`, via Homebrew, or the Docker image; real installation of the app waits for the user's yes. Start-at-login behaviour of the app is not checked.
- **Files**: macOS keeps models in `~/.ollama/models`, logs in `~/.ollama/logs` (`app.log`, `server.log`), and the CLI at `Ollama.app/Contents/Resources/ollama`; on first start the app offers to link it into `/usr/local/bin` (docs/macos.mdx).
- **Without the app**: `ollama serve` starts the same server from the CLI; the embedding calls below need only that server.

## Parts

Parts are commands and the embeddings API, as `schema.md` says for an app. Defined in `cmd/cmd.go` (`rootCmd.AddCommand`) and `cmd/launch/launch.go`, described in `docs/cli.mdx`.

### `serve` (alias `start`)

"Start Ollama". Runs the HTTP server on port 11434; `ollama serve --help` lists the environment variables (docs/cli.mdx). The macOS app runs it from the menu bar. Needs nothing beyond the binary. In use, via the app.

### `pull`

"Pull a model from a registry". Downloads a model by name, for example the tag the kit uses. Outbound HTTPS once. In use.

### `run`

"Run a model": interactive chat or one prompt; for an embedding model prints a JSON array (docs/cli.mdx, `ollama run embeddinggemma "Hello world"`). Not used by the kit, which calls the server's HTTP endpoint.

### `list` (alias `ls`), `ps`, `rm`, `show`, `cp`

`list` "List models"; `ps` "List running models" (shows size, processor and when the model unloads); `rm MODEL [MODEL...]` "Remove a model"; `show MODEL` "Show information for a model"; `cp SOURCE DESTINATION` "Copy a model". Local only; read in `cmd/cmd.go` and the docs, not run by the kit.

### `stop`

"Stop a running model": unloads it from memory at once; the FAQ gives it as the way to unload immediately. Used in the measurement to time the first query after unloading.

### `create`

"Create a model" from a `Modelfile` (`FROM`, `SYSTEM`, ...). Not used.

### `push`, `signin` (hidden alias `login`), `signout` (hidden alias `logout`)

`push` "Push a model to a registry"; `signin` and `signout` sign in to and out of ollama.com, which the cloud FAQ ties to pushing models, pulling private models and running cloud models. They send data to ollama.com by design. Not used.

### `launch`

"Launch the Ollama menu or an integration" (`cmd/launch/launch.go`): sets up and starts external coding tools against Ollama models; the docs list OpenCode, Claude Code, Codex, VS Code and Droid, and the command's help lists more. It can also write the other tool's configuration. Not used; it is a coding-agent feature, not an embedding feature.

### `runner` and `gpu-discover` (hidden)

Defined with `Hidden: true`, so not shown in help; their purpose was not read beyond the names (a model runner and GPU discovery). Not for direct use.

### Embeddings API: `POST /api/embed`

Documented in `docs/api.md` and `docs/capabilities/embeddings.mdx`. Parameters: `model`, `input` (text or a list of texts; media objects with `text`, `image`, `audio` on models that take them), `truncate` (default true), `options`, `keep_alive` (default `5m`), `dimensions`. Returns `embeddings`. The docs' multimodal examples name the model `embeddinggemma2`; the tag the kit pulls is written in its `search.py` and listed on the Ollama library page.

### Embeddings API: `/v1/embeddings` (OpenAI-compatible)

Documented in `docs/api/openai-compatibility.mdx`: supported fields `model`, `input` (string or array of strings), `encoding format`, `dimensions`; token-array inputs and `user` are not supported. This is the endpoint the kit's `search.py` calls on port 11434. In use.

### Embeddings API: `/api/embeddings` (legacy)

"this endpoint has been superseded by `/api/embed`" (docs/api.md). Not used.

## Reasons for any rejection or reference status

None rejected. The Homebrew route is not a part; the reason it is avoided (extra formulas and a changed default `python3`) is under How to run here.

## How the kit uses it

The kit's installer offers the app from ollama.com; `search.py embed-setup` writes the config for the Ollama embedding model and `search.py index` calls the OpenAI-style endpoint. Use record: `raw/notes/trials/2026-11-21-ollama-embedding-server-for-search.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 42 model calls on sonnet, $1.95 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
