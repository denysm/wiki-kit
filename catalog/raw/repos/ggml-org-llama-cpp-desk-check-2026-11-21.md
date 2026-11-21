---
title: "Desk check: ggml-org/llama.cpp v1.0.0"
source: https://github.com/ggml-org/llama.cpp/tree/v1.0.0
type: repos
authors: ["The ggml authors"]
source_date: 2026-11-13
ingested: 2026-11-21
repo: ggml-org/llama.cpp
kind: runtime
version: "1.0.0"
licence: MIT
tags: [catalog, desk-check, kind-runtime, llama-cpp, ggml, embeddings, inference]
summary: "ggml-org/llama.cpp v1.0.0 read from a read-only clone: the backends (CPU, BLAS, Metal, CUDA and the rest), the llama umbrella command and the tools (llama-server with its embeddings routes, llama-embedding, llama-bench, llama-quantize and others); freshness from the GitHub API; outbound calls and how to switch them off; why llama-server is only a reference here."
---

# Desk check: ggml-org/llama.cpp v1.0.0

Read from a shallow clone of tag `v1.0.0` (commit `b1b770d90d94cad9e9ea5b993bdbc383a522fb28`, committed 2026-11-13) at `$EXTERNAL/llama.cpp`. The clone was not modified; nothing was built, installed or run. Checked 2026-11-21. Version read by this desk check: 1.0.0.

## Repository facts

- README title "llama.cpp", tagline "LLM inference in C/C++". Goal: "to enable LLM (and VLM) inference with minimal setup and state-of-the-art performance on a wide range of hardware - locally and in the cloud." The project "is build on top of the ggml library" (`ggml/` is inside the clone).
- `LICENSE`: "MIT License", "Copyright (c) 2023-2026 The ggml authors". The README badge also says MIT.
- Version is set in the root `CMakeLists.txt` (`LLAMA_VERSION_MAJOR 1`, `MINOR 0`, `PATCH 0`). `docs/release.md`: "llama.cpp uses semantic versioning (`MAJOR.MINOR.PATCH`)"; a breaking change to the public C API is a MAJOR bump.
- Tags in the clone: `b12359`, `v1.0.0`, `v1.0.0-b12359-b1b770d`. The README names two release streams: `v*` releases and `b*` nightly builds.
- Folders that hold parts: `ggml/src/` (one folder per backend), `tools/` (one folder per tool), `examples/`, `app/` (the `llama` umbrella command). Other folders: `src/` and `include/` (the `llama` library and its C API), `common/`, `docs/`, `grammars/`, `gguf-py/`, `tests/`, `vendor/`, `models/`, `skills/`, `conversion/`, plus `convert_hf_to_gguf.py` and other conversion scripts at the root.
- The repository root holds `CLAUDE.md` and `AGENTS.md` (instructions for coding agents working on the project itself); they are not part of the tool.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/ggml-org/llama.cpp`: `pushed_at` 2026-11-21T11:11:47Z; licence `MIT`; not archived.
- `gh api repos/ggml-org/llama.cpp/releases/latest`: tag `v1.0.0`, published 2026-11-13T10:20:19Z.
- So the clone is at the latest release. The repository moves daily (the push was on the day of this check); the `b*` nightly tags are newer than `v1.0.0`.
- Version mismatch to keep in mind: the benchmark note (`../notes/2026-11-21-measurements-local-embeddings.md`) writes the runtime as `llama-server` 0.7.0. The tag read here is 1.0.0. The note gives no build id, so the two numbers are not reconciled; the figures in the note are for what the note calls 0.7.0.

## How to run here

- Clone, read-only: `git clone --depth 1 --branch v1.0.0 https://github.com/ggml-org/llama.cpp $EXTERNAL/llama.cpp`. Never build or edit it. Read first: `README.md`, then `tools/server/README.md`, `docs/build.md` and `examples/embedding/README.md`.
- The README offers `curl -LsSf https://llama.app/install.sh | sh` and `irm https://llama.app/install.ps1 | iex`, Docker images (`ghcr.io/ggml-org/llama.cpp:server` and CUDA variants), pre-built release binaries and a build from source. None was used here.
- Outbound calls found: `-hf, --hf-repo <user>/<model>[:quant]` downloads a model from Hugging Face (`common/common.cpp` names `https://huggingface.co/`), with `-hft, --hf-token` or `HF_TOKEN` for private repositories; `--embd-gemma-default` "can download weights from the internet". The `llama update` command, visible only for builds made with `llama-install.sh`, runs the installer script from `llama.app`; otherwise it prints "Updates are available only when installed from https://llama.app". A search for "telemetry" and "analytics" in `common/`, `app/`, `src/` and the `tools/server` sources found no telemetry code (the one hit was a test file).
- Switch off: `--offline` ("Offline mode: forces use of cache, prevents network access", env `LLAMA_ARG_OFFLINE`); use `-m <file>` with a local GGUF instead of `-hf`; do not run `llama update`.
- `llama-server` defaults, from `tools/server/README.md`: listens on localhost; `--port` default 9931; `--api-key` default none; the Web UI is on by default (`--no-webui` switches it off); `--metrics` off by default; `--embedding` "restrict to only support embedding use case; use only with dedicated embedding models"; `--pooling {none,mean,cls,last,rank}`; `--embd-normalize N` default 2 (euclidean). The README's Docker example binds `--host 0.0.0.0`; do not copy that.
- What breaks without a build: nothing in the clone runs by itself; every tool is C++ and needs a CMake build or a release binary (`docs/build.md`). The clone is therefore read for docs and for the HTTP routes only.

## Parts

Parts of a runtime are its backends; the tools that run on them are listed as parts too, because the benchmark used one of them.

### Tool: `llama-server` (`tools/server/`, command `llama serve` in `app/llama.cpp`)

- `tools/server/README.md`: OpenAI-compatible "chat completions, responses, and embeddings routes". Embedding routes: `POST /v1/embeddings` ("requires that the model uses a pooling different than type `none`"; vectors "normalized using the Eucledian norm"), `POST /embedding` (not OpenAI-compatible; also multimodal) and `POST /embeddings` (non-OpenAI-compatible; supports all poolings including `--pooling none`). A reranker route needs a reranker model and `--embedding --pooling rank` or `--reranking`.
- Router mode: one server can load and unload several models (presets, `GET /models`).
- Needs: a build or a release binary, a GGUF model (a local file or `-hf`), RAM for the model (the benchmark note gives server peaks per model).
- Status here: `reference`; reason in the section "Why llama-server is a reference" below.

### Tool: `llama-embedding` (`examples/embedding/`)

- `examples/embedding/README.md`: "generate high-dimensional embedding vector of a given text with llama.cpp"; example `llama-embedding -m ./path/to/model --pooling mean --log-disable -p "Hello World!"` prints space-separated floats; `--embd-normalize` choices -1 none, 0 max absolute int16, 1 taxicab, 2 euclidean (default).
- Needs: a build, a GGUF embedding model.

### Tool: `llama-retrieval` (`examples/retrieval/`)

- README: "Demonstration of simple retrieval technique based on cosine similarity". A demo, not a search engine.

### Tool: `llama-bench` (`tools/llama-bench/`)

- README: "Performance testing tool for llama.cpp." Reports prompt-processing and token-generation speed for a model on a given backend.

### Tool: `llama-batched-bench` (`tools/batched-bench/`)

- README: "Benchmark the batched decoding performance of `llama.cpp`"; two modes, prompts not shared or shared.

### Tool: `llama-quantize` (`tools/quantize/`)

- README: takes a GGUF model "typically in a high-precision format like F32 or BF16, and converts it to a quantized format". Accuracy loss is usually measured in perplexity or Kullback-Leibler divergence and "can be minimized by using a suitable imatrix file".
- Needs: a build, enough disk and RAM for the source model.

### Tool: `llama-imatrix` (`tools/imatrix/`)

- README: "Compute an importance matrix for a model and given text dataset. Can be used during quantization to enhance the quality of the quantized models."

### Tool: `llama-perplexity` (`tools/perplexity/`)

- README: calculates perplexity "over a given text corpus"; "perplexity is **not** directly comparable between models, especially if they use different tokenizers".

### Tool: `llama-gguf-split` (`tools/gguf-split/`)

- README: "CLI to split / merge GGUF files" with `--split` and `--split-max-size`.

### Tool: `llama-fit-params` (`tools/fit-params/`)

- README: llama.cpp binaries "can automatically fit the projected memory use of a model to the free device memory available at runtime"; the tool prints the matching CLI arguments.

### Tool: `llama` umbrella command (`app/llama.cpp`)

- One executable with visible commands `serve` (alias `server`, "HTTP API server"), `cli` (alias `client`), `download` (alias `get`, "Download a model") and `update`, and hidden ones: `completion`, `bench`, `batched-bench`, `fit-params`, `quantize`, `perplexity`; also `version`, `licenses`, `help`.
- `download` fetches from the network; `update` runs the installer script (see How to run here).

### Tools read by their README first lines only

- `llama-cli` (`tools/cli/`): interactive command-line chat; README is an auto-generated option list.
- `llama-completion` (`tools/completion/`): text completion.
- `llama-mtmd` and the multimodal library (`tools/mtmd/`): README warns "very heavy development, and breaking changes are expected".
- `llama-tts` (`tools/tts/`): "demonstrate audio generation capability in llama.cpp via `libmtmd`".
- `llama-cvector-generator` (`tools/cvector-generator/`): "generate a control vector using gguf models".
- `llama-export-lora` (`tools/export-lora/`): "Apply LORA adapters to base model and export the resulting model."
- `llama-results` (`tools/results/`): `--check` model outputs against a previous commit.
- `ggml-metal-tuning` (`tools/tuning/`): "Offline kernel tuner for the Metal backend."
- `llama-ui` (`tools/ui/`): "A modern, feature-rich web interface for llama-server built with SvelteKit"; needs Node to build.
- `llama-tokenize` (`tools/tokenize/`), `tools/connect/`: no README in the folder; known from `tools/CMakeLists.txt` only.

### Backends (`ggml/src/<backend>/`, README table "Supported backends")

The README lists 17 backends with target devices: BLAS (all), BLIS (all), CANN (Huawei Ascend NPU), CUDA (Nvidia GPU), HIP (AMD GPU), Hexagon (Snapdragon), IBM zDNN (IBM Z & LinuxONE), MUSA (Moore Threads GPU), Metal (Apple Silicon), OpenCL (Adreno GPU), OpenVINO [In Progress] (Intel CPUs, GPUs, and NPUs), RPC (all), SYCL (Intel GPU), VirtGPU (VirtGPU APIR), Vulkan (GPU), WebGPU (all), ZenDNN (AMD CPU). The CPU backend (`ggml/src/ggml-cpu/`, with AVX, AVX2, AVX512 and AMX on x86, ARM NEON, KleidiAI) is the default and is not a row of that table. `docs/ops.md` lists which operations each backend supports.

- **CPU** (`docs/build.md` "CPU Build"): the default build; read.
- **Metal** (`docs/build.md` "Metal Build"): "On MacOS, Metal is enabled by default. Using Metal makes the computation run on the GPU." Switch off at build time with `-DGGML_METAL=OFF`, or at run time with `--n-gpu-layers 0`. Read. This is the backend of the benchmark runs.
- **BLAS** (`docs/build.md` "BLAS Build"): "may lead to some performance improvements in prompt processing using batch sizes higher than 32"; does not affect generation; Accelerate Framework is "enabled by default" on Mac. Read.
- **CUDA**, **HIP**, **MUSA**, **Vulkan**, **SYCL**, **CANN**, **OpenCL**, **OpenVINO**, **Hexagon**, **IBM zDNN**, **ZenDNN**, **WebGPU**, **VirtGPU**, **BLIS**, **RPC**: known from the README table and the headings of `docs/build.md`; not read in depth. `tools/rpc/README.md` carries the warning "The functionality is fragile and insecure. **Never run the RPC server on an open network or in a sensitive environment!**" and the RPC backend is marked proof-of-concept there.

## Why llama-server is a reference

`llama-server` is the runtime on which the three embedding models were benchmarked, so it is the baseline for any later model comparison. From the benchmark note: `llama-server` 0.7.0 (Metal) on an Apple M4 Pro with 24 GB, a corpus of two roots, 13,090 chunks, 3.47 million tokens; EmbeddingGemma 2 Q8_0 indexed in 357 s (9.7k tokens/s) with a server peak of 656 MB with 4 slots and 13 ms per query; bge-m3 Q8_0 in 587 s (6.0k tokens/s), 765 MB, 15.5 ms; Qwen3-Embedding-4B Q8_0 in 5,969 s (about 0.6k tokens/s, an upper bound), 5.0 GB, 100 ms. For EmbeddingGemma 2 the Ollama runtime took 439 s, 15.5 ms per query, and its vectors equal llama-server's (mean cosine 1.0000, same recall). The kit's search does not run on llama-server: the decided choice is EmbeddingGemma 2 through Ollama. So llama-server stays a baseline, read for the benchmark and for its routes, and is not the runtime in use. Consult it again when a new embedding model is compared, or when a GGUF needs a runtime other than Ollama's.

## How the kit uses it

The kit used `llama-server` only in the benchmark of embedding models (see the note above, written 2026-11-12 to 2026-11-14). No part is in daily use.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 41 model calls on sonnet, $2.05 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
