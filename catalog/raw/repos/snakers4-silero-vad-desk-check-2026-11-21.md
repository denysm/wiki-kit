---
title: "Desk check: snakers4/silero-vad v6.2.3"
source: https://github.com/snakers4/silero-vad/tree/v6.2.3
type: repos
authors: ["Silero Team"]
source_date: 2026-09-23
ingested: 2026-11-21
repo: snakers4/silero-vad
kind: model
version: "6.2.3"
licence: MIT
tags: [catalog, desk-check, kind-model, vad, voice-activity-detection, onnx, local]
summary: "Silero VAD v6.2.3 read through the GitHub API (README, release notes, file tree): a small voice activity detector, MIT, no telemetry, under 1 ms per 30 ms chunk on one CPU thread, 8 and 16 kHz; ONNX and JIT files of about 1.2 to 2.8 MB. The same model is built into whisper.cpp, NeMo-Speech.cpp and FluidAudio. Nothing run."
---

# Desk check: snakers4/silero-vad v6.2.3

Read through `gh api` (README, latest release notes, the file tree at `v6.2.3`); no clone. Checked 2026-11-21.

## Repository facts

- Licence: `gh api` reports `MIT`; README: "Published under permissive license (MIT) Silero VAD has zero strings attached - no telemetry, no keys, no registration, no built-in expiration, no keys or vendor lock." (The README's licence badge carries the alt text "CC BY-NC 4.0" over an MIT label; the API and the text say MIT.)
- Speed: "One audio chunk (30+ ms) takes less than **1ms** to be processed on a single CPU thread." Size: "JIT model is around two megabytes in size." Languages: "trained on huge corpora that include over **6000** languages". Rates: "**8000 Hz** and **16000 Hz**".
- Python package extras: `silero-vad[onnx-cpu]` needs `onnxruntime>=1.16.1` and `numpy`; release `v6.2.3` notes: "torchaudio is now an optional dependency instead of required. Only torch is required".
- Model files at `v6.2.3` (`src/silero_vad/data/`, bytes): `silero_vad.onnx` 2327524, `silero_vad.jit` 2272526, `silero_vad_16k_op15.onnx` 1289603, `silero_vad_half.onnx` 1280395, `silero_vad_16k_sequence.onnx` 1246165, `silero_vad_op18_ifless.onnx` 2845718, `silero_vad_openvino_16k.onnx` 1288203.
- Examples include C++ with ONNX Runtime (`examples/cpp`).

## Freshness (2026-11-21, `gh api`)

- `pushed_at` 2026-11-20T13:27:41Z; default branch `master`; not archived. Latest release `v6.2.3`, published 2026-09-23T11:36:47Z.

## Where it already runs without its Python package

- whisper.cpp: `whisper-cli --vad` with a Silero model fetched by `models/download-vad-model.sh silero-v6.2.0` (whisper.cpp desk check).
- NeMo-Speech.cpp: the ASR VAD config takes a model path (NeMo-Speech.cpp desk check).
- FluidAudio: "Voice activity detection with Silero models" (FluidAudio desk check).

## How to run here

- No install needed for the kit's path: use the copy built into the recogniser in use. The Python package (torch or onnxruntime) is not installed; a trial of it goes into a throwaway venv after the user's yes.
