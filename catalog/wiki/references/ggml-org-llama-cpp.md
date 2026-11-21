---
title: "ggml-org/llama.cpp"
category: reference
kind: runtime
areas: [search-and-embeddings]
repo: ggml-org/llama.cpp
version: "1.0.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/ggml-org-llama-cpp-desk-check-2026-11-21.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, kind-runtime, llama-cpp, ggml, embeddings, inference, local-models]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "C/C++ inference engine for open models in GGUF files, with backends for CPU, Apple Metal, CUDA, Vulkan and more, and tools including llama-server (an HTTP server with OpenAI-style embeddings routes). Read at v1.0.0. llama-server is the reference: the runtime on which three embedding models were benchmarked, while the kit's search runs on Ollama. Other backends and tools are read or listed."
---

# ggml-org/llama.cpp

> An inference engine (kind `runtime`, licence MIT, version `1.0.0` read in a clone): "LLM inference in C/C++" for models in GGUF files, on CPU, Apple Metal, CUDA, Vulkan and a dozen other backends, with tools such as `llama-server`. Here it is the baseline runtime of the embedding benchmark, read from a clone and not built.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Benchmark an embedding model on one machine: index speed, memory, time per query, recall | `llama-server` | search-and-embeddings |
| Serve a GGUF embedding model over HTTP on localhost, with an OpenAI-style embeddings call | `llama-server` | search-and-embeddings |
| Get one embedding vector for a text from a shell, with a chosen pooling and normalisation | `llama-embedding` | search-and-embeddings |
| Run models on an Apple Silicon GPU | `Metal` | search-and-embeddings |
| Measure speed of a model on a given backend | `llama-bench` | search-and-embeddings |
| Make a smaller (quantized) copy of a GGUF model | `llama-quantize` | search-and-embeddings |

## Run it here

- **Clone, read-only**: `git clone --depth 1 --branch v1.0.0 https://github.com/ggml-org/llama.cpp $EXTERNAL/llama.cpp`. Never build or edit it. Read first: `README.md`, then `tools/server/README.md`, `docs/build.md`, `examples/embedding/README.md`.
- **Version**: `1.0.0`, the latest release, published 2026-11-13. The benchmark note writes the runtime it used as `llama-server` `0.7.0` and gives no build id, so its figures are not tied to `1.0.0`. Before relying on this card, compare with upstream: `gh api repos/ggml-org/llama.cpp --jq .pushed_at` and `gh api repos/ggml-org/llama.cpp/releases/latest --jq .tag_name`; the repository is pushed to daily.
- **Reference use**: `llama-server` ran the benchmark of the three embedding models; it is not in daily use. The reason is in the Verdict.
- **Sends outward**: `-hf <user>/<model>` downloads a model from Hugging Face; `--embd-gemma-default` "can download weights from the internet"; `llama update` runs an installer script from `llama.app` and exists only in builds made with the installer. No telemetry code was found in `common/`, `app/`, `src/` and the server sources.
- **Switch off**: `--offline` ("forces use of cache, prevents network access"); load a local file with `-m` instead of `-hf`; do not run `llama update`. `llama-server` listens on localhost, port `9931` by default, with no API key (`--api-key` adds one) and its Web UI on (`--no-webui` removes it); never copy the README's Docker example that binds `--host 0.0.0.0`.
- **Do not install**: `curl -LsSf https://llama.app/install.sh | sh`, `irm https://llama.app/install.ps1 | iex`, Docker images or a build from source; real installation waits for the user's yes. Nothing in the clone runs without a build or a release binary.

## What's inside

Parts of a runtime are its backends; the tools that run on them are rows too. Source: `ggml/src/<backend>/`, `tools/`, `examples/`, `app/`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `llama-server` | HTTP server (command `llama serve`): OpenAI-compatible chat, responses and embeddings routes; `/v1/embeddings` needs a pooling other than `none`, `--embedding` restricts it to embedding models, `--pooling` and `--embd-normalize` set the vector; router mode loads several models. | reference | A build or release binary, a GGUF model; model memory (server peak 656 MB for EmbeddingGemma 2, 765 MB for bge-m3, 5.0 GB for Qwen3-Embedding-4B in the benchmark) | Consult it again when a new embedding model is compared, or when a GGUF needs a runtime other than the one in use. |
| `Metal` | Backend for Apple Silicon: "enabled by default" on macOS, runs the computation on the GPU; off with `-DGGML_METAL=OFF` or `--n-gpu-layers 0`. The backend of the benchmark runs. | candidate | A Mac with Apple Silicon and a build with Metal | Try it when a model must run on the GPU of the same Mac without Ollama. |
| `CPU` | Default backend (`ggml/src/ggml-cpu/`): AVX, AVX2, AVX512 and AMX on x86, ARM NEON. | candidate | A build | Try it on a machine with no supported GPU. |
| `BLAS` | Optional backend; "may lead to some performance improvements in prompt processing using batch sizes higher than 32", not generation; Accelerate on Mac. | candidate | A build with a BLAS library | Try it when long-prompt processing, such as indexing, is the slow step on a CPU-only build. |
| `llama-embedding` | One vector for a text from the shell: `--pooling mean`, `--embd-normalize` (-1 none, 0 max absolute int16, 1 taxicab, 2 euclidean, default). | candidate | A build, a GGUF embedding model | Try it for a one-off embedding or to check a model's vectors against another runtime's. |
| `llama-bench` | "Performance testing tool for llama.cpp": prompt-processing and generation speed per backend. | candidate | A build, a model | Try it to compare backends or quantizations of one model before choosing. |
| `llama-batched-bench` | Benchmark of batched decoding; prompts shared or not. | candidate | A build, a model | Try it when a server will take many parallel requests. |
| `llama-quantize` | Converts a GGUF model from F32 or BF16 to a quantized format; loss measured with perplexity or Kullback-Leibler divergence, reduced with an imatrix. | candidate | A build, disk and RAM for the source model | Try it when a model exists only in full precision. |
| `llama-imatrix` | Computes an importance matrix on a text dataset to improve quantization. | candidate | A build, a model, a text file | Try it together with `llama-quantize`. |
| `llama-perplexity` | Perplexity of a model over a text corpus; not comparable across tokenizers. | candidate | A build, a model, a corpus | Try it after quantizing, to see what the quantization cost. |
| `llama-gguf-split` | Splits or merges GGUF files (`--split`, `--split-max-size`). | candidate | A build | Try it when a model file is too large to move in one piece. |
| `llama-fit-params` | Prints the CLI arguments that fit a model to the free device memory. | candidate | A build, a model | Try it when a model barely fits the GPU. |
| `llama-retrieval` | Demo of simple retrieval by cosine similarity. | candidate | A build, a model | Read it for a minimal example of embedding plus cosine ranking. |
| `llama` (umbrella command) | One executable: `serve`, `cli`, `download`, `update`, and hidden `completion`, `bench`, `batched-bench`, `fit-params`, `quantize`, `perplexity`. | listed | A release binary or a build; `download` and `update` use the network | Read when a release binary replaces separate tool binaries. |
| `llama-cli` | Interactive command-line chat. | listed | A build, a model | Read when a chat with a local model is wanted. |
| `llama-completion` | Text completion. | listed | A build, a model | Read when plain completion is wanted. |
| `llama-mtmd` | Multimodal (vision and audio) library and tool; the README warns of "very heavy development". | listed | A build, a multimodal model | Read when images must be embedded or described locally. |
| `llama-tts` | Audio generation through `libmtmd`. | listed | A build, a model | Read when speech output is wanted. |
| `llama-cvector-generator` | Generates a control vector from a GGUF model. | listed | A build, a model | Read when steering a model's style is wanted. |
| `llama-export-lora` | Applies LoRA adapters to a base model and exports the result. | listed | A build, a model, an adapter | Read when an adapter must be baked in. |
| `llama-results` | `--check` outputs of a model against a previous commit. | listed | A build, a model | Read when two builds must give the same output. |
| `ggml-metal-tuning` | Offline kernel tuner for the Metal backend. | listed | A Mac, a build | Read when tuning Metal kernels. |
| `llama-ui` | SvelteKit web interface of `llama-server`. | listed | Node to build | Read when a browser chat over the server is wanted. |
| `llama-tokenize`, `tools/connect` | No README in the folder; named in `tools/CMakeLists.txt`. | listed | A build | Read when a tokenizer check is needed. |
| `CUDA` | Backend for Nvidia GPUs (`docs/build.md`). | listed | An Nvidia GPU, CUDA | Read when the machine has an Nvidia GPU. |
| `HIP` | Backend for AMD GPUs. | listed | An AMD GPU | Read when the machine has an AMD GPU. |
| `MUSA` | Backend for Moore Threads GPUs. | listed | A Moore Threads GPU | Read when the machine has one. |
| `Vulkan` | Backend for GPUs through Vulkan; `docs/build.md` has a section for Mac users. | listed | A Vulkan GPU | Read when no CUDA or Metal backend fits. |
| `SYCL` | Backend for Intel GPUs. | listed | An Intel GPU | Read when the machine has an Intel GPU. |
| `CANN` | Backend for Huawei Ascend NPUs. | listed | An Ascend NPU | Read when the machine has one. |
| `OpenCL` | Backend for Adreno GPUs. | listed | An Adreno GPU | Read for Android on Snapdragon. |
| `OpenVINO` | Backend for Intel CPUs, GPUs and NPUs; marked "In Progress". | listed | An Intel device | Read when its status leaves "In Progress". |
| `Hexagon` | Backend for Snapdragon. | listed | A Snapdragon device | Read for Snapdragon NPUs. |
| `IBM zDNN` | Backend for IBM Z and LinuxONE. | listed | An IBM Z machine | Read when running on IBM Z. |
| `ZenDNN` | Backend for AMD CPUs. | listed | An AMD CPU | Read when running on AMD CPUs. |
| `WebGPU` | Backend for all devices through WebGPU; also browser builds. | listed | A WebGPU runtime | Read when inference must run in a browser. |
| `VirtGPU` | Backend for VirtGPU APIR. | listed | A virtualised GPU | Read when running in such a VM. |
| `BLIS` | BLAS-like backend (`docs/backend/BLIS.md`). | listed | A BLIS library | Read when a CPU build needs BLIS. |
| `RPC` | Exposes ggml devices on a remote host; the README calls it "fragile and insecure" and says "Never run the RPC server on an open network or in a sensitive environment!". | listed | A second machine; opens a network port | Read only when a model must be split across machines on a closed network. |

## Tried

None yet. The benchmark runs of `llama-server` are recorded on the model cards and in the measurements note; they back the `reference` status through the desk check.

## Verdict

llama.cpp is the baseline runtime of the embedding benchmark, not the runtime in use: `llama-server` indexed EmbeddingGemma 2 in 357 s against 439 s for Ollama with identical vectors, yet the decided choice is EmbeddingGemma 2 through Ollama. Nothing here was built or run from the clone. Known cost: the benchmark's `llama-server` was written as `0.7.0` while the latest release read is `1.0.0`, so the figures are not tied to this version. Revisit when a new embedding model is compared, when a build id for the benchmark is needed, or when a GGUF needs a runtime Ollama lacks.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; local embedding models and the runtimes that serve them
- [[ollama-ollama|ollama/ollama]] (../references/ollama-ollama.md): the runtime in use
- [[google-embeddinggemma-2|google/embeddinggemma-2]] (../references/google-embeddinggemma-2.md): the model benchmarked and chosen
- [[baai-bge-m3|BAAI/bge-m3]] (../references/baai-bge-m3.md): the runner-up model
- [[qwen-qwen3-embedding-4b|Qwen/Qwen3-Embedding-4B]] (../references/qwen-qwen3-embedding-4b.md): the largest model benchmarked
- [[onnxruntime-onnxruntime|onnxruntime]] (../references/onnxruntime-onnxruntime.md): the runtime rejected for embeddings

## Sources

- [Desk check: ggml-org/llama.cpp v1.0.0](../../raw/repos/ggml-org-llama-cpp-desk-check-2026-11-21.md): backends and tools read from the clone, freshness through the GitHub API, outbound calls, the reason for `reference`.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): the benchmark on `llama-server`, the Ollama comparison, retold.
