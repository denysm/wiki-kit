---
title: "Desk check: ONNX Runtime 1.32.0 (not cloned)"
source: https://pypi.org/project/onnxruntime/1.32.0/
type: repos
authors: ["Microsoft Corporation"]
source_date: 2026-11-13
ingested: 2026-11-21
url: https://onnxruntime.ai
kind: runtime
version: "1.32.0"
licence: MIT
tags: [catalog, desk-check, kind-runtime, onnxruntime, embeddings, inference, not-cloned]
summary: "ONNX Runtime 1.32.0 checked from PyPI and the project's web site, not from a clone: the GitHub repository answered 404 to the API and to a plain page request on 2026-11-21. The execution-provider framework and its list; the CPU provider through Python is rejected for embeddings here, with the measured reason retold from the benchmark note."
---

# Desk check: ONNX Runtime 1.32.0 (not cloned)

No clone exists, so no source file was read. Read on 2026-11-21: the PyPI record of `onnxruntime`, the home page https://onnxruntime.ai, and its page https://onnxruntime.ai/docs/execution-providers/. Nothing was installed or run. Version read by this desk check: 1.32.0.

## Repository facts

- Description on PyPI: "ONNX Runtime is a runtime accelerator for Machine Learning models". The PyPI long description: "ONNX Runtime is a performance-focused scoring engine for Open Neural Network Exchange (ONNX) models."
- Home page tagline: "Cross-platform accelerated machine learning." and "Production-grade AI engine to speed up training and inferencing in your existing technology stack." It names `pip install onnxruntime` and `pip install onnxruntime-genai` (a separate package for generative models, not read).
- PyPI: version `1.32.0`, author "Microsoft Corporation", licence field "MIT License" and classifier "License :: OSI Approved :: MIT License"; Python `>=3.11`; wheels for macOS arm64, Linux x86_64 and aarch64, Windows amd64 and arm64, first uploaded 2026-11-13. Dependencies: `flatbuffers`, `numpy>=1.21.6`, `packaging`, `protobuf>=4.25.8`; extras `symbolic` (sympy) and `quantization` (ml_dtypes). Project URLs: Homepage https://onnxruntime.ai, Download https://github.com/microsoft/onnxruntime/tags.
- No licence file was read (no clone); the licence is as PyPI reports it.

## Freshness (checked 2026-11-21)

- `gh api repos/microsoft/onnxruntime`: HTTP 404 "Not Found". `gh api repos/microsoft/onnxruntime/releases/latest`: 404. `gh api repos/Microsoft/onnxruntime` and a plain request to https://github.com/microsoft/onnxruntime also gave 404. It gave 404 on 2026-11-19 too. The repository that PyPI and the home page point to is therefore not readable from here; why is not known.
- PyPI lists release notes for 1.32.0 down to 1.17.0 at `github.com/Microsoft/onnxruntime/releases/tag/v1.32.0`; that page also gave 404.
- Latest version on PyPI: 1.32.0, uploaded 2026-11-13. This is the version the benchmark note names ("ONNX Runtime 1.32").
- Not known: last push, archived or not.

## How to run here

- Not cloned and not installable from a clone. Do not `pip install onnxruntime` for the kit: the CPU provider through Python is rejected (below), and `search.py` would depend on that venv's Python.
- Outbound calls and telemetry: not checked (no source read). The measurement note's venv had `onnxruntime`, `tokenizers` and `numpy` only.

## Parts

Parts of a runtime are its backends; for ONNX Runtime they are execution providers (EPs). Read: the overview page of EPs only, not the page of each provider. The page says: "ONNX Runtime works with different hardware acceleration libraries through its extensible Execution Providers (EP) framework", nodes or sub-graphs go to a provider through `GetCapability()`, and providers are tried in priority order (for example `['CUDAExecutionProvider', 'CPUExecutionProvider']`). "The ONNX Runtime package can be built with any combination of the EPs along with the default CPU execution provider."

Providers named in the page's navigation:

- **CPU** (the default provider; used through Python as `onnxruntime` with `InferenceSession`): the one measured here. See "Why the CPU provider is rejected".
- **NVIDIA CUDA**, **NVIDIA TensorRT**, **NVIDIA TensorRT RTX**: NVIDIA GPUs.
- **Intel OpenVINO**, **Intel oneDNN**: Intel hardware.
- **Windows DirectML**.
- **Qualcomm QNN**.
- **Android NNAPI**.
- **Apple CoreML**: the provider that would target Apple hardware; its page was not read.
- **XNNPACK**.
- **AMD ROCm** (marked "deprecated" in the summary table), **AMD MIGraphX**, **AMD Vitis AI**.
- **Cloud Azure** (marked "preview").
- **WebGPU**.
- Community-maintained: **Arm ACL**, **Arm NN**, **Apache TVM**, **Rockchip RKNPU**, **Huawei CANN** (several marked "preview").

## Why the CPU provider is rejected

From the benchmark note, for EmbeddingGemma 2: "ONNX Runtime 1.32 on the CPU (int8 model in the Python process; a venv with onnxruntime, tokenizers and numpy, 136 MB) gave the same recall (cosine 0.9998) but took 1,246 s, peaked at 6.3 GB, answered in 42 ms and would make `search.py` depend on the venv's Python: rejected." For comparison, in the same note Ollama 0.40.16 took 439 s, its runner peaked at 275-282 MB and it answered in 15.5 ms per query, and `llama-server` took 357 s with a peak of 656 MB. So the CPU provider through Python matched the quality and lost on indexing time, memory, query time and on a dependency on a particular Python. Revisit when an embedding model is available only as ONNX, or when a provider that uses the Mac's GPU (CoreML) is measured; the note did not measure any other provider.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 41 model calls on sonnet, $2.05 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
