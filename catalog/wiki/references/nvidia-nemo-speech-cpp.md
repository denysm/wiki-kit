---
title: "NVIDIA/NeMo-Speech.cpp"
category: reference
kind: cli
areas: [live-speech-and-calls, converting-documents-and-recordings]
repo: NVIDIA/NeMo-Speech.cpp
version: "0.3.0"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/nvidia-nemo-speech-cpp-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, area-converting-documents-and-recordings, kind-cli, nemo-speech-cpp, speech-to-text, streaming, diarization, translation, text-to-speech, ggml, metal, local]
confidence: medium
volatility: hot
verified: 2026-11-21
summary: "NVIDIA's native C++ runtime for its speech models on ggml (Metal on Apple Silicon): streaming recognition with Nemotron 3.5 and Parakeet v3, diarization, translation and synthesis, as a CLI, a local server and a stable C SDK that a native app can link. Read, not run; models come from Hugging Face under their own licences."
---

# NVIDIA/NeMo-Speech.cpp

> A local speech runtime (kind `cli`, licence Apache-2.0, version `0.3.0` read in a clone): NVIDIA's "official solution for local speech inference", running its speech models as GGUF files on ggml, with Metal on Apple Silicon. One binary covers recognition (including streaming and the live microphone), diarization, translation and synthesis; a C SDK exposes the same in-process. Nothing here is tried yet.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Recognise speech as it is spoken inside a native app, pushing audio from your own capture and reading partial and final text | `NeMoSpeech::ASR` streaming API | live-speech-and-calls |
| Transcribe the microphone live from a terminal on this machine | `transcribe --live` | live-speech-and-calls |
| Compare speech models on your own recordings without PyTorch | `transcribe` | converting-documents-and-recordings |
| Tell up to eight speakers apart in a call, as it runs or afterwards | `diarize` | live-speech-and-calls |
| Translate text locally between English and Russian, Ukrainian, French, German or Dutch | `translate` | live-speech-and-calls |
| Speak text aloud locally in English, French, German or Spanish | `synthesize` | live-speech-and-calls |
| Serve live transcription to other local programs over a WebSocket | `serve` | live-speech-and-calls |

## Run it here

- **Clone, read-only**: `git clone --depth 1 --branch v0.3.0 https://github.com/NVIDIA/NeMo-Speech.cpp $EXTERNAL/nemo-speech.cpp`. Read first: `README.md`, `docs/install.md`, `docs/cli.md`, `docs/sdk.md`, `include/nemo_speech/asr.h`.
- **To try it**: take the release archive `nemo-speech-0.3.0-macos-aarch64-metal.tar.gz`, check it with its `.sha256` file and `shasum -a 256`, unpack it into a throwaway folder that is not on `PATH`, and pass local GGUF paths with `--model`. A source build needs `cmake ninja sentencepiece abseil` from Homebrew and only the Command Line Tools for Metal.
- **Sends outward**: model pulls from Hugging Face, verified by size and SHA-256; local GGUF paths download nothing. No telemetry code was found in the source. Read, not observed.
- **Switch off**: pass local model paths so nothing is pulled; `serve` binds the loopback address, port 8080, by default; keep it there.
- **Do not install**: the `install.sh | sh` and `irm | iex` installers, Docker, CUDA builds. Real installation waits for the user's yes.

## What's inside

Parts are the commands of `app/main.cpp` and the SDK component that matters here.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `NeMoSpeech::ASR` streaming API | `nemo_speech_asr_stream_push_f32` / `nemo_speech_asr_stream_next`, results flagged final or not, per-stream VAD, endpointing, language code or `auto`, speech contexts, word time offsets. | candidate | The release archive's headers and shared libraries, a GGUF model | Try it as the recogniser inside a native capture app, one stream per track. |
| `transcribe` | Transcribe WAV files with any supported model and language. | candidate | The archive and a GGUF model (sizes on the Parakeet v3 and Nemotron 3.5 cards) | Try it on the speech-recognition bench recordings against whisper.cpp. |
| `transcribe --live` | Live transcription of the default microphone (miniaudio capture). | candidate | The archive, a model, a microphone | Try it to measure time to first text before building the native path. |
| `diarize` | Streaming Sortformer 4-speaker v2 (`cc-by-4.0`) or Nemotron 3 Diarization (`openmdw-1.1`, up to eight speakers), alone or with ASR. | candidate | The archive and a diarization GGUF | Try it on a call recording with three or more speakers. |
| `translate` | Riva Translate 4B Instruct v2 (`nvidia-open-model-license`): English and 36 other languages, including Russian, Ukrainian, French, German and Dutch; not Kazakh. | candidate | The archive, a 4B-parameter model (several GB of memory) | Try it against Apple Translation and a local LLM on call sentences. |
| `synthesize` | MagpieTTS Multilingual 357M (`nvidia-open-model-license`); no Russian, Ukrainian or Kazakh. | candidate | The archive and the TTS model with its codec | Try it for French or German speech in an earpiece against the system voices. |
| `serve` | Local HTTP server with OpenAI-compatible routes and realtime WebSocket transcription. | candidate | The archive; loopback only | Try it when a second program needs live text without linking the SDK. |
| `pull`, `model` | Download a model ahead of time; list defaults and short names. | candidate | Network access to Hugging Face | Try it when models are fetched for a trial. |
| `bench`, `doctor`, `health` | Benchmarking and diagnostics. | listed | The archive | Read `BENCHMARK.md` and `docs/troubleshooting.md` when a trial needs numbers or fails. |

## Tried

none yet

## Verdict

A strong candidate for the live recogniser of a native call app: one runtime, a stable C streaming API and Metal, covering Russian and Ukrainian through Nemotron 3.5 and Parakeet v3. Nothing is run yet; its claimed speeds are for NVIDIA GPUs and a CPU, not Apple Silicon. Revisit after the speech-recognition bench trial, or when a release after `0.3.0` ships.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page
- [[nvidia-nemotron-3-5-asr-streaming-0-6b|nvidia/nemotron-3.5-asr-streaming-0.6b]] (../references/nvidia-nemotron-3-5-asr-streaming-0-6b.md): the streaming model it runs
- [[nvidia-parakeet-tdt-0-6b-v3|nvidia/parakeet-tdt-0.6b-v3]] (../references/nvidia-parakeet-tdt-0-6b-v3.md): the batch model it runs
- [[apple-translation|Apple Translation]] (../references/apple-translation.md): the on-device translator `translate` competes with

## Sources

- [Desk check: NVIDIA/NeMo-Speech.cpp v0.3.0](../../raw/repos/nvidia-nemo-speech-cpp-desk-check-2026-11-21.md): commands, SDK streaming API, install and build paths, outbound calls, model licences and languages.
