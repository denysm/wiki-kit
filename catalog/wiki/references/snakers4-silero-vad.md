---
title: "snakers4/silero-vad"
category: reference
kind: model
areas: [live-speech-and-calls]
repo: snakers4/silero-vad
version: "6.2.3"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/snakers4-silero-vad-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, kind-model, vad, voice-activity-detection, onnx, local]
confidence: medium
volatility: warm
verified: 2026-11-21
summary: "Small voice activity detector (MIT, no telemetry, under 1 ms per 30 ms chunk on one CPU thread, 8 and 16 kHz). Already built into whisper.cpp, NeMo-Speech.cpp and FluidAudio, so the kit uses it through the recogniser rather than its Python package. Read, not run."
---

# snakers4/silero-vad

> A voice activity detector (kind `model`, licence MIT, version `6.2.3` read through the GitHub API): tells speech from silence in 30 ms chunks, in under 1 ms on one CPU thread, at 8 or 16 kHz. Its model files are about 1.2 to 2.8 MB. Not tried yet.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Cut live call audio into speech segments before recognition, so the recogniser skips silence | the copy inside the recogniser | live-speech-and-calls |
| Detect speech in a native app with ONNX Runtime and no Python | `silero_vad.onnx` | live-speech-and-calls |

## Run it here

- **No clone needed**: the recognisers carry it. whisper.cpp `--vad` with the `silero-v6.2.0` model, NeMo-Speech.cpp's VAD config (a model path), FluidAudio's VAD.
- **Sends outward**: nothing; "no telemetry, no keys, no registration".
- **Do not install**: the Python package (torch or onnxruntime) in the kit's Python; a trial of it goes into a throwaway venv after the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| the copy inside the recogniser | Silero VAD as shipped in whisper.cpp, NeMo-Speech.cpp and FluidAudio. | candidate | The recogniser's own VAD file | Try it with the live recogniser that wins the bench. |
| `silero_vad.onnx` | ONNX model, 2327524 bytes; C++ example with ONNX Runtime. | candidate | ONNX Runtime | Try it only if the chosen recogniser has no VAD. |
| `silero_vad_16k_op15.onnx`, `silero_vad_half.onnx`, `silero_vad_16k_sequence.onnx`, `silero_vad_op18_ifless.onnx`, `silero_vad_openvino_16k.onnx` | Variants for 16 kHz, half precision, sequence inference, older runtimes and OpenVINO. | listed | ONNX Runtime or OpenVINO | Read when the default file does not load in a runtime. |
| `silero_vad.jit` | PyTorch JIT model, 2272526 bytes. | listed | PyTorch | Read when a Python reference result is needed. |

## Tried

none yet

## Verdict

The standard small VAD, already inside every recogniser the kit considers, so it needs no separate install. Revisit when the chosen recogniser's VAD misses speech or cuts words.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[ggml-org-whisper-cpp|ggml-org/whisper.cpp]] (../references/ggml-org-whisper-cpp.md): `whisper-cli --vad`
- [[fluidinference-fluidaudio|FluidInference/FluidAudio]] (../references/fluidinference-fluidaudio.md): its CoreML VAD

## Sources

- [Desk check: snakers4/silero-vad v6.2.3](../../raw/repos/snakers4-silero-vad-desk-check-2026-11-21.md): licence, speed and size claims, files, where it is built in.
