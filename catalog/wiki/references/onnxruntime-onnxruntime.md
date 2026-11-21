---
title: "ONNX Runtime"
category: reference
kind: runtime
areas: [search-and-embeddings]
url: https://onnxruntime.ai
version: "1.32.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/onnxruntime-onnxruntime-desk-check-2026-11-21.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, kind-runtime, onnx, embeddings, inference]
confidence: medium
volatility: hot
verified: 2026-11-21
summary: "Microsoft's cross-platform inference engine for ONNX models, with a framework of execution providers for CPU, NVIDIA, Intel, Apple, Qualcomm and others. Checked at 1.32.0 from PyPI and the project site, not from a clone: its GitHub repository answered 404. The CPU provider through Python is rejected for local embeddings: same recall, but 1,246 s to index against 439 s on Ollama, and a peak of 6.3 GB."
---

# ONNX Runtime

> An inference engine (kind `runtime`, licence MIT as PyPI reports it, version `1.32.0` read from PyPI and the project site, no clone): "a performance-focused scoring engine for Open Neural Network Exchange (ONNX) models", with execution providers per hardware. Here the CPU provider through Python was measured for embeddings and rejected.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Not this: embed a knowledge base with an int8 ONNX model in the Python process on the CPU. Rejected: 1,246 s against 439 s on Ollama, 6.3 GB peak, and `search.py` would depend on a venv's Python | `CPU` | search-and-embeddings |
| Run an ONNX model on an NVIDIA GPU | `NVIDIA CUDA` | search-and-embeddings |
| Run an ONNX model on Apple hardware | `Apple CoreML` | search-and-embeddings |
| Run an ONNX model in a browser | `WebGPU` | search-and-embeddings |

## Run it here

- **Not cloned.** The GitHub repository gave 404 to `gh api repos/microsoft/onnxruntime` on 2026-11-21, as it did on 2026-11-19, and to a plain page request; its last push, release date and archived state are not known. The version and licence come from PyPI (version `1.32.0`, uploaded 2026-11-13, licence "MIT License"), the page https://onnxruntime.ai and its execution-providers page.
- **Read first**: https://onnxruntime.ai/docs/execution-providers/.
- **Switch off**: not checked; outbound calls and telemetry were not looked for because no source was read.
- **Do not install**: `pip install onnxruntime` or `onnxruntime-genai`. The benchmark's venv held `onnxruntime`, `tokenizers` and `numpy` (136 MB) and is not kept; real installation waits for the user's yes.
- **Before relying on this card**: re-check PyPI (`curl -s https://pypi.org/pypi/onnxruntime/json`) and whether the GitHub repository answers.

## What's inside

Parts of a runtime are its backends; for ONNX Runtime, its execution providers. Only the overview page was read; every provider except `CPU` is known from the page's list.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `CPU` | The default provider; used through Python as `onnxruntime`. Rejected for local embeddings: the int8 model gave the same recall (cosine 0.9998) but took 1,246 s to index, peaked at 6.3 GB, answered in 42 ms, and would make `search.py` depend on the venv's Python. | rejected | A venv with `onnxruntime`, `tokenizers` and `numpy` (136 MB) | Revisit when an embedding model exists only as ONNX, or when the Ollama route stops working. |
| `NVIDIA CUDA` | Provider for NVIDIA GPUs. | listed | An NVIDIA GPU and CUDA | Read when the machine has an NVIDIA GPU. |
| `NVIDIA TensorRT` | Provider for NVIDIA GPUs through TensorRT; `NVIDIA TensorRT RTX` is a sibling. | listed | An NVIDIA GPU | Read when CUDA speed is not enough. |
| `Intel OpenVINO` | Provider for Intel hardware; `Intel oneDNN` is a sibling. | listed | Intel hardware | Read when the machine is Intel-based. |
| `Windows DirectML` | Provider for Windows GPUs. | listed | Windows | Read on Windows without CUDA. |
| `Qualcomm QNN` | Provider for Qualcomm devices. | listed | A Qualcomm device | Read for Snapdragon devices. |
| `Android NNAPI` | Provider for Android. | listed | Android | Read for Android apps. |
| `Apple CoreML` | Provider for Apple hardware; not measured here. | listed | A Mac or iPhone | Read when an ONNX model must use the Mac's accelerators and Ollama does not carry it. |
| `XNNPACK` | CPU provider for edge devices. | listed | A build with it | Read for edge CPUs. |
| `AMD ROCm`, `AMD MIGraphX`, `AMD Vitis AI` | Providers for AMD hardware; ROCm is marked "deprecated". | listed | AMD hardware | Read when the machine has AMD hardware. |
| `Cloud Azure` | Provider that calls a cloud service; marked "preview". | listed | An account; data leaves the machine | Read only if data may leave the machine. |
| `WebGPU` | Provider for browsers and WebGPU runtimes. | listed | A WebGPU runtime | Read when inference must run in a browser. |
| Community-maintained: `Arm ACL`, `Arm NN`, `Apache TVM`, `Rockchip RKNPU`, `Huawei CANN` | Providers kept by their communities; several marked "preview". | listed | The matching hardware | Read when the hardware matches. |

## Tried

None yet; the CPU measurement is in the benchmark note and the rejection is recorded in the desk check.

## Verdict

ONNX Runtime stays out of the kit's search: its CPU provider matched the recall of the Ollama route (cosine 0.9998) but needed 1,246 s to index where Ollama needed 439 s, peaked at 6.3 GB, and tied the search script to a venv. The card rests on PyPI and the project site only, because the GitHub repository answered 404, so licence and freshness are as PyPI reports them. Revisit when an embedding model ships only as ONNX, when a provider for the Mac's accelerators is measured, or when the GitHub repository answers again and a clone can be read.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; local embedding models and the runtimes that serve them
- [[ollama-ollama|ollama/ollama]] (../references/ollama-ollama.md): the runtime in use
- [[ggml-org-llama-cpp|ggml-org/llama.cpp]] (../references/ggml-org-llama-cpp.md): the baseline runtime
- [[google-embeddinggemma-2|google/embeddinggemma-2]] (../references/google-embeddinggemma-2.md): the model measured on it
- [[numpy-numpy|numpy/numpy]] (../references/numpy-numpy.md): a dependency of its Python package

## Sources

- [Desk check: ONNX Runtime 1.32.0 (not cloned)](../../raw/repos/onnxruntime-onnxruntime-desk-check-2026-11-21.md): PyPI and project-site facts, the 404 from GitHub, the provider list, the reason for the rejection.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): the CPU run against Ollama and `llama-server`, retold.
