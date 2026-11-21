---
title: "nvidia/nemotron-3.5-asr-streaming-0.6b"
category: reference
kind: model
areas: [live-speech-and-calls]
url: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b
version: "ea30d66"
licence: OpenMDW-1.1
desk_checked: 2026-11-21
sources:
  - raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md
  - raw/repos/nvidia-nemotron-3-5-asr-streaming-0-6b-desk-check-2026-11-21.md
  - raw/repos/fluidinference-fluidaudio-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, kind-model, speech-to-text, streaming, multilingual, nvidia, gguf]
confidence: medium
volatility: hot
verified: 2026-11-21
summary: "NVIDIA's multilingual streaming speech recogniser (600M, cache-aware, punctuation, chunks from 80 ms to 1.12 s) with Russian and Ukrainian among 19 transcription-ready locales; no Kazakh. Its q8_0 GGUF runs in NeMo-Speech.cpp without PyTorch. Read from the card, not run."
---

# nvidia/nemotron-3.5-asr-streaming-0.6b

> A Hugging Face model (kind `model`, licence OpenMDW-1.1, revision `ea30d66` read): a 600M-parameter streaming recogniser that writes punctuated text while audio arrives, in chunks from 80 ms to 1.12 s, for 19 transcription-ready locales including Russian, Ukrainian, English, French, German, Spanish and Dutch. Not tried yet.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Show what a call participant says within about a second, in Russian, Ukrainian, English, French, German, Spanish or Dutch, on this machine | `q8_0.gguf` | live-speech-and-calls |
| Transcribe a call where the language changes, with a language tag per utterance | `q8_0.gguf` | live-speech-and-calls |
| Not this: Kazakh speech. It is in none of the card's language tiers | `q8_0.gguf` | live-speech-and-calls |

## Run it here

- **No clone.** Card and metadata through the URLs in the desk check, at revision `ea30d66`.
- **To try it**: the `q8_0.gguf` file (742090464 bytes) with NeMo-Speech.cpp in a throwaway folder; chunk size by `att_context_size` (`[56, 13]` is 1.12 s), language by locale or `auto`.
- **Sends outward**: only the one-time download.
- **Do not install**: NeMo from git `main` or PyTorch in the kit's Python; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `q8_0.gguf` | The model quantized for NeMo-Speech.cpp; FLEURS word error rate for Russian 10.84 at 80ms and 9.17 at 1.12s with the language given, Ukrainian 15.70 and 13.07, English 9.43 and 7.91, French 10.97 and 9.03. | tried | NeMo-Speech.cpp and 742090464 bytes; peak memory 498 MB in the trial | The real task that would move it to `in use`: live text in a real call, after the accuracy bench on the owner's recordings. |
| `.nemo` | The NeMo checkpoint. | listed | NeMo from git and PyTorch (Python 3.11 or later), 2368284501 bytes | Read when a fine-tune on the owner's terms is wanted. |
| `model.safetensors` | The Transformers checkpoint, Transformers v5.13.0 or later. | listed | A venv with Transformers and PyTorch, 2552062944 bytes | Read when a Python reference result is needed to check a port. |
| CoreML conversion (FluidAudio) | `FluidInference/Nemotron-3.5-ASR-Streaming-Multilingual-0.6b-CoreML`, for en/es/fr/it/pt/de/zh/ja only, chunk tiers 560ms / 1120ms / 2240ms / 4480ms. | candidate | FluidAudio in a Swift app; no Russian or Ukrainian | Try it for the English or French "them" track against the GGUF path on the Neural Engine. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Smoke test on synthetic Russian speech, 51.4 s | `q8_0.gguf` | Ran through NeMo-Speech.cpp on an Apple M4, whole file and `--stream`, real-time factor 0.071 and 0.119; English terms transliterated into Cyrillic, some numbers written as words. | No cost | [trial record](../../raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md) |

## Verdict

The only streaming model found that covers the owner's Russian and Ukrainian with punctuation, now runnable without PyTorch through NeMo-Speech.cpp. Its published error rates are for FLEURS read speech; Russian with English terms is untested. Revisit after the speech-recognition bench, or on a new revision.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[nvidia-nemo-speech-cpp|NVIDIA/NeMo-Speech.cpp]] (../references/nvidia-nemo-speech-cpp.md): the runtime for its GGUF file
- [[fluidinference-fluidaudio|FluidInference/FluidAudio]] (../references/fluidinference-fluidaudio.md): the CoreML conversion

## Sources

- [Desk check: nvidia/nemotron-3.5-asr-streaming-0.6b revision ea30d66](../../raw/repos/nvidia-nemotron-3-5-asr-streaming-0-6b-desk-check-2026-11-21.md): card, licence, languages, chunk sizes, error rates, files.
- [Desk check: FluidInference/FluidAudio v0.18.4](../../raw/repos/fluidinference-fluidaudio-desk-check-2026-11-21.md): the CoreML conversion and its languages.
- [Trial: speech engines, smoke test on synthetic Russian speech](../../raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md): runs on an Apple M4, speeds, a pipeline check only.
