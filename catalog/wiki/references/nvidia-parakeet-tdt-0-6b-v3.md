---
title: "nvidia/parakeet-tdt-0.6b-v3"
category: reference
kind: model
areas: [converting-documents-and-recordings, live-speech-and-calls]
url: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3
version: "541d1f9"
licence: CC-BY-4.0
desk_checked: 2026-11-21
sources:
  - raw/repos/nvidia-parakeet-tdt-0-6b-v3-desk-check-2026-11-21.md
  - raw/repos/fluidinference-fluidaudio-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, area-live-speech-and-calls, kind-model, speech-to-text, multilingual, nvidia, gguf, timestamps]
confidence: medium
volatility: hot
verified: 2026-11-21
summary: "NVIDIA's batch multilingual speech recogniser for 25 European languages including Russian and Ukrainian, with word timestamps, CC-BY-4.0. Runs without PyTorch three ways: NeMo-Speech.cpp (q8_0 GGUF), whisper.cpp parakeet-cli (f16 conversion) and FluidAudio (CoreML, plus the post-trained Parakeet Ultra). Read, not run."
---

# nvidia/parakeet-tdt-0.6b-v3

> A Hugging Face model (kind `model`, licence CC-BY-4.0, revision `541d1f9` read): a 0.6B batch recogniser for 25 European languages, Russian and Ukrainian among them, with word-level and segment-level timestamps. A candidate second opinion to Whisper for transcripts after a call. Not tried yet.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Transcribe a recorded call in Russian, Ukrainian, English, French, German, Spanish or Dutch on this machine, as a second opinion to Whisper | `q8_0.gguf` | converting-documents-and-recordings |
| Get word timestamps to line text up with speaker turns | `q8_0.gguf` | converting-documents-and-recordings |
| Transcribe with the model already installed with whisper.cpp | `ggml-parakeet-tdt-0.6b-v3-f16.bin` | converting-documents-and-recordings |
| Transcribe on the Neural Engine from a Swift app, with a more accurate post-trained variant | Parakeet Ultra (FluidAudio) | live-speech-and-calls |
| Not this: Kazakh speech. It is not among the 25 languages | `q8_0.gguf` | converting-documents-and-recordings |

## Run it here

- **No clone.** Card and metadata through the URLs in the desk check, at revision `541d1f9`.
- **To try it**: the `q8_0.gguf` (713975456 bytes) with NeMo-Speech.cpp, or `ggml-org/parakeet-GGUF` `ggml-parakeet-tdt-0.6b-v3-f16.bin` with whisper.cpp `parakeet-cli` (installed with the Homebrew `whisper.cpp` 1.9.5 bottle), both in a throwaway folder. The first `parakeet-cli` start compiles Metal libraries and is slow.
- **Sends outward**: only the one-time download.
- **Do not install**: NeMo or PyTorch in the kit's Python; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `q8_0.gguf` | The model quantized for NeMo-Speech.cpp. | candidate | NeMo-Speech.cpp and 713975456 bytes | Try it on the speech-recognition bench against `large-v3-turbo`. |
| `ggml-parakeet-tdt-0.6b-v3-f16.bin` | ggml-org's conversion for whisper.cpp `parakeet-cli` (`-ps` prints segments). | candidate | `parakeet-cli` from whisper.cpp 1.9.5; the file from `ggml-org/parakeet-GGUF` | Try it on the same bench to compare the two runtimes. |
| Parakeet TDT v3 (FluidAudio) | FluidAudio's default batch model, 25 European languages, on the Neural Engine. | candidate | FluidAudio in a Swift app | Try it for the precise pass inside a native app. |
| Parakeet Ultra (FluidAudio) | Post-training of v3 with the same languages: FLEURS 24-language mean 11.67 vs 14.81 % for v3; int8 encoder (595 MB). | candidate | FluidAudio in a Swift app | Try it on the bench next to v3. |
| `.nemo` | The NeMo checkpoint, 2509332480 bytes. | listed | NeMo and PyTorch | Read when a fine-tune is wanted. |
| `model.safetensors` | The checkpoint, 2508311120 bytes. | listed | Transformers and PyTorch | Read when a Python reference result is needed. |

## Tried

none yet

## Verdict

The strongest non-Whisper candidate for an accurate pass after a call in the owner's European languages, with three local runtimes to choose from. It does not stream by itself; live use goes through FluidAudio's windowing or the Nemotron streaming model instead. Revisit after the speech-recognition bench.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page
- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[ggml-org-whisper-cpp|ggml-org/whisper.cpp]] (../references/ggml-org-whisper-cpp.md): `parakeet-cli`
- [[nvidia-nemo-speech-cpp|NVIDIA/NeMo-Speech.cpp]] (../references/nvidia-nemo-speech-cpp.md): the GGUF runtime
- [[fluidinference-fluidaudio|FluidInference/FluidAudio]] (../references/fluidinference-fluidaudio.md): CoreML conversions and Parakeet Ultra

## Sources

- [Desk check: nvidia/parakeet-tdt-0.6b-v3 revision 541d1f9](../../raw/repos/nvidia-parakeet-tdt-0-6b-v3-desk-check-2026-11-21.md): card, licence, languages, files, runtimes.
- [Desk check: FluidInference/FluidAudio v0.18.4](../../raw/repos/fluidinference-fluidaudio-desk-check-2026-11-21.md): the CoreML conversions and Parakeet Ultra.
