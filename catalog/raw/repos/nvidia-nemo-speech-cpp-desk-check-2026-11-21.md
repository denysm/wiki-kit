---
title: "Desk check: NVIDIA/NeMo-Speech.cpp v0.3.0"
source: https://github.com/NVIDIA/NeMo-Speech.cpp/tree/v0.3.0
type: repos
authors: ["NVIDIA"]
source_date: 2026-10-30
ingested: 2026-11-21
repo: NVIDIA/NeMo-Speech.cpp
kind: cli
version: "0.3.0"
licence: Apache-2.0
tags: [catalog, desk-check, kind-cli, nemo-speech-cpp, speech-to-text, streaming, diarization, translation, text-to-speech, ggml, metal, local]
summary: "NVIDIA's native C++ runtime for its speech models, read from a read-only clone of v0.3.0: a CLI (transcribe, live microphone, diarize, translate, synthesize, serve, bench), a local HTTP and WebSocket server, and a stable C SDK with streaming recognition. Runs GGUF files on ggml with Metal on Apple Silicon; models are pulled from Hugging Face. Licences of the models it runs read from Hugging Face. Nothing installed or run."
---

# Desk check: NVIDIA/NeMo-Speech.cpp v0.3.0

Read from a shallow clone of tag `v0.3.0` (commit `20999cc921d2b14aa58708f61756a8b2e787ba20`, committed 2026-10-30) at `$EXTERNAL/nemo-speech.cpp`. `VERSION`: "NEMO_SPEECH_VERSION: 0.3.0". The clone was not modified; nothing was built, installed or run. Checked 2026-11-21.

## Repository facts

- What it is, in the README's words: "A lightweight native C++ runtime for the NVIDIA Nemotron Speech model family, with broad hardware support", "NVIDIA's official solution for local speech inference", "with native inference powered by ggml". The clone carries `llama.cpp` (ggml) as a submodule folder.
- `LICENSE`: Apache License 2.0, "Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved." The README: "NVIDIA-authored code is released under the Apache License 2.0"; "Third-party components retain their respective terms" (`THIRD_PARTY_NOTICES.md`).
- Models and applications (README table): speech recognition with Nemotron 3.5 ASR Streaming 0.6B, Nemotron Speech Streaming 0.6B, Parakeet TDT 0.6B v3 and Parakeet CTC 1.1B; speech-LLM transcription with Nemotron 3.5 Transcribe 30B-A4B; speaker diarization with Streaming Sortformer 4-speaker v2 and Nemotron 3 Diarization, "standalone or combined with ASR"; text and speech translation with Riva Translate 4B Instruct v2; speech synthesis with MagpieTTS Multilingual 357M; full-duplex VoiceChat; speech processing with Silero VAD, "punctuation and capitalization, endpointing, text normalization, and subtitles".
- Performance claims in the README are for a GeForce RTX 4090 and a CPU only (for example "2.3 ms" and "27 ms" latency per 160 ms chunk); `BENCHMARK.md` has no Apple Silicon row (a search for apple, mac, metal and M1–M4 found none).

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/NVIDIA/NeMo-Speech.cpp`: created 2026-07-15T10:46:56Z, `pushed_at` 2026-11-20T12:22:59Z, licence `Apache-2.0`, default branch `main`, not archived.
- Releases: `nightly` 2026-11-13T09:29:06Z, `v0.3.0` 2026-10-30T11:24:18Z, `v0.2.0` 2026-10-02T15:42:06Z. The clone is at the latest tagged release.
- `v0.3.0` assets include `nemo-speech-0.3.0-macos-aarch64-metal.tar.gz` and `nemo-speech-0.3.0-macos-aarch64-metal.tar.gz.sha256`, `nemo-speech-0.3.0-macos-aarch64-cpu.tar.gz`, Linux CPU, CUDA and Vulkan archives, and `itn_configs.tar.bz2`.

## How to run here

- **Clone**: `git clone --depth 1 --branch v0.3.0 https://github.com/NVIDIA/NeMo-Speech.cpp $EXTERNAL/nemo-speech.cpp`; read only. Read first: `README.md`, `docs/install.md`, `docs/cli.md`, `docs/sdk.md`, `include/nemo_speech/asr.h`.
- **Install paths in the docs**: a `curl -fsSL .../scripts/install.sh | sh` installer (PowerShell `irm ... | iex` on Windows) that "downloads the prebuilt archive for the latest release, checks it against the SHA-256 checksum published with the release, and builds from source when no archive is available". `docs/install.md`: archives are named `nemo-speech-<version>-<linux|macos>-<x86_64|aarch64>-<backend>.tar.gz`; "On Apple Silicon, automatic selection installs `macos-aarch64-metal`"; checksums are verified on macOS with `shasum -a 256`.
- **Build from source** (`docs/build.md`): macOS with Homebrew `brew install cmake ninja sentencepiece abseil`; "Metal builds require macOS on Apple Silicon and the Xcode Command Line Tools; no separate Metal SDK is needed." Presets follow `<backend>-<component>` for `cpu`, `cuda`, `metal` and `vulkan`.
- **Outbound calls**: the CLI pulls models from Hugging Face: "On first use, the CLI downloads the pinned default Nemotron 3.5 GGUF from Hugging Face and verifies its size and SHA-256"; `app/model_store.cpp` builds `https://huggingface.co` URLs. "Local GGUF paths continue to work without downloading anything." A search of `app/`, `src/`, `server/` and `scripts/` for telemetry, analytics, posthog, sentry and mixpanel found nothing. Read in the source, not observed on the wire.
- **Server**: `nemo-speech serve` binds to the loopback address, port 8080, by default (README, which gives the full local URL); routes are "documented OpenAI-compatible subsets, alongside realtime WebSocket transcription".
- **Install steps to avoid**: piping the installer into a shell, Docker, CUDA builds; a trial uses the release archive, checked with `shasum -a 256`, unpacked into a throwaway folder that is not on `PATH`, after the user's yes.

## Parts

Commands are the names in `app/main.cpp`: `transcribe`, `diarize`, `translate`, `synthesize`, `bench`, `pull`, `model`, `doctor`, `health`, `serve`.

### `transcribe` and `transcribe --live`

- Transcribes a WAV file; "The CLI selects an available backend and handles common mono or stereo PCM WAV sample rates automatically." `--live` transcribes "the default microphone on builds that include live capture"; `app/microphone_capture.cpp` uses miniaudio: "one implementation across CoreAudio, WASAPI". `--model` takes a short name (`nemotron-en`) or a local GGUF path; `--language` takes a locale or `auto` (model card examples).

### Native SDK, component `ASR` (`include/nemo_speech/asr.h`)

- `docs/sdk.md`: "Release archives include stable C headers, shared libraries, and an exported CMake package"; components `ASR` (`nemo_speech/asr.h`, "offline and streaming recognition"), plus diarization, NMT and TTS headers (`include/nemo_speech/` has `asr.h`, `diar.h`, `nmt.h`, `tts.h`).
- Streaming: "create a stream with `nemo_speech_asr_streaming_recognize`, alternate `nemo_speech_asr_stream_push_f32` with calls to `nemo_speech_asr_stream_next`, call `nemo_speech_asr_stream_finish`, drain the remaining results with `next`, and release the stream with `nemo_speech_asr_stream_close`." "One ASR recognizer can serve independent calls from multiple threads. Drive an individual stream from one thread."
- `asr.h` configs: a streaming config ("Streaming execution policy (latency/throughput), not model identity"), a VAD config with `model_path` ("empty/NULL = no VAD"), endpointing with `vad_based`, post-processing with `itn_model_dir`, speech contexts, recognition options with `language_code` ("NULL/"" = auto/default"), `enable_word_time_offsets`, `enable_automatic_punctuation`; results expose `nemo_speech_asr_result_is_final` and `nemo_speech_asr_result_language_code`; `nemo_speech_asr_stream_force_endpoint` cuts an utterance.
- Example programs: `examples/transcribe_live.cpp` ("microphone capture and streaming ASR"), `examples/diarize_file.cpp`, `examples/synthesize_text.cpp`.

### `diarize`

- Speaker diarization with Streaming Sortformer 4-speaker v2 or Nemotron 3 Diarization, standalone or combined with ASR (`nemo_speech_diar_stream`, `nemo_speech_diar_segments` in `docs/sdk.md`).

### `translate`

- Text and speech translation with Riva Translate 4B Instruct v2, "with composed ASR-to-NMT-to-TTS speech translation". Build preset `metal-nmt` is a "Metal-enabled NMT build".

### `synthesize`

- Speech synthesis with MagpieTTS Multilingual 357M; `docs/tts/configuration.md`: "Both v2602 and v2607 support `en`, `es`, `de`, `fr`, `it`, `vi`," (the list continues in the file).

### `serve`, `pull`, `model`, `bench`, `doctor`, `health`

- `serve`: the local HTTP server and playground. `pull`: "`nemo-speech pull nemotron-en` downloads the English-only model ahead of time". `model list`: "to see defaults, short names, and which command uses each model". `bench`, `doctor`, `health`: names only (`docs/troubleshooting.md` covers `doctor`; not read).

## Licences and languages of the models it runs (Hugging Face API, 2026-11-21)

| Model | Licence | Languages that matter here |
|---|---|---|
| `nvidia/nemotron-3.5-asr-streaming-0.6b` | `openmdw-1.1` | see its own desk check |
| `nvidia/parakeet-tdt-0.6b-v3` | `cc-by-4.0` | see its own desk check |
| `nvidia/diar_streaming_sortformer_4spk-v2` | `cc-by-4.0` | language independent |
| `nvidia/Nemotron-3-Diarization` | `openmdw-1.1` | its card: "handles up to eight speakers"; "input buffer latency as low as 80 ms ... although the lowest recommended configuration is 0.32 s" |
| `nvidia/Riva-Translate-4B-Instruct-v2` | `nvidia-open-model-license` | card: "translates text in English and 36 non-English languages", including "Russian(ru)", "Ukrainian(uk)", "French(fr)", "German(de)", "Dutch(nl)"; Kazakh is not in the list |
| `nvidia/magpie_tts_multilingual_357m` | `nvidia-open-model-license` | API language tags `ar`, `de`, `en`, `es`, `fr`, `hi`, `it`, `ja`, `ko`, `pt`, `vi`, `zh`; no Russian, Ukrainian or Kazakh |
