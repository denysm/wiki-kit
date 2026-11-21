---
title: "Desk check: FluidInference/FluidAudio v0.18.4"
source: https://github.com/FluidInference/FluidAudio/tree/v0.18.4
type: repos
authors: ["FluidInference"]
source_date: 2026-11-19
ingested: 2026-11-21
repo: FluidInference/FluidAudio
kind: library
version: "0.18.4"
licence: Apache-2.0
tags: [catalog, desk-check, kind-library, swift, coreml, neural-engine, speech-to-text, streaming, diarization, vad, text-to-speech, echo-cancellation]
summary: "FluidAudio v0.18.4 read from a read-only clone: a Swift package with no package dependencies (macOS 14, iOS 17) that runs CoreML conversions of open speech models on the Neural Engine: Parakeet v3 and Ultra, streaming Nemotron and Parakeet EOU, Sortformer, LS-EEND and pyannote diarization, Silero VAD, LocalVQE echo cancellation, Supertonic-3 and other TTS. Models download from Hugging Face. Open-source apps built on it include a dual-track meeting transcriber and a live-caption overlay. Nothing built or run."
---

# Desk check: FluidInference/FluidAudio v0.18.4

Read from a shallow clone of tag `v0.18.4` (commit `e0c6103`, committed 2026-11-19) at `$EXTERNAL/FluidAudio`. Not modified; nothing built, installed or run. Checked 2026-11-21.

## Repository facts

- `LICENSE`: Apache License 2.0. `Package.swift`: `swift-tools-version: 6.0`, platforms `.macOS(.v14)` and `.iOS(.v17)`, package `dependencies: []`.
- README: "Models are optimized for background processing, ambient computing and always on workloads by running inference on the ANE, minimizing CPU usage and avoiding GPU/MPS entirely." "All models are publicly available on HuggingFace — converted and optimized by our team; permissive licenses."
- A search of `Sources/` for telemetry, analytics, posthog, sentry and mixpanel found only the `analytics` folder name inside CoreML model bundles and a domain list; no telemetry code. Read, not observed.

## Freshness (checked 2026-11-21 through `gh api`)

- `pushed_at` 2026-11-19T21:44:36Z; licence `Apache-2.0`; default branch `main`; not archived. Latest release `v0.18.4`, published 2026-11-19T21:44:37Z. An earlier session read `v0.15.6` (2026-08-19).

## Parts read in `Documentation/Models.md`

### Speech recognition

- **Parakeet TDT v3**: "Batch speech-to-text, 25 European languages (0.6B params). Default ASR model."
- **Parakeet Ultra**: "moondream's post-training of v3: same architecture, languages and API"; "More accurate than v3 on every benchmark (LibriSpeech test-clean 2.13 vs 2.27 %, test-other 3.81 vs 4.12 %, FLEURS 24-language mean 11.67 vs 14.81 %) at the same speed. int8 encoder (595 MB), ANE, iOS 17+." Marked "**Recommended** for new integrations."
- **Parakeet EOU**: "Streaming speech-to-text with end-of-utterance detection (120M params). Three chunk-size variants — 160ms / 320ms / 1280ms"; English only (README).
- **Nemotron Speech Streaming 0.6B**: "English-only (0.6B params)", chunks 560ms / 1120ms / 2240ms.
- **Nemotron Speech Streaming Multilingual 0.6B**: "RNNT streaming ASR, multilingual (en/es/fr/it/pt/de/zh/ja) with an `auto` language-detection mode. 0.6B params, 4 chunk-size tiers — 560ms / 1120ms / 2240ms / 4480ms (2240ms recommended)"; Hugging Face `FluidInference/Nemotron-3.5-ASR-Streaming-Multilingual-0.6b-CoreML`. Russian and Ukrainian are not in its list.
- **Nemotron Unified ASR 0.6B**: "25 European languages with punctuation and capitalization, offline (15 s) and streaming (2.08 s / 1.12 s / 0.56 s latency bundles)"; "int8 lost accuracy on French in the conversion check, so fp16 is the CLI default." Which 25 languages was not read.
- Others: Nemotron 3.5 Transcribe Lite (English, with speakers), Cohere Transcribe (14 languages), SenseVoiceSmall, Paraformer, LFM3-Audio-2B, Parakeet Unified 0.6B (English).
- `Documentation/ASR/CustomVocabulary.md` exists (custom vocabulary for names and jargon); not read.

### Diarization

- **Sortformer**: "Supports both streaming and complete-buffer inference for up to 4 speakers", "requiring 1040ms of warmup audio and 480ms per update for the low latency versions".
- **LS-EEND**: "Research prototype ... for up to 10 speakers", "900ms of warmup audio and 100ms per update".
- **Pyannote CoreML Pipeline**: online pipeline based on pyannote/speaker-diarization-3.1, offline batch pipeline based on pyannote/speaker-diarization-community-1.

### Voice detection, enhancement, speech output

- VAD: "Voice activity detection with Silero models".
- **LocalVQE**: "Neural acoustic echo cancellation + noise suppression + dereverberation for 16 kHz speech (DeepVQE derivative, Apache-2.0). Takes mic + far-end reference, returns clean near-end speech with 16 ms algorithmic latency."
- **Supertonic-3**: "Multilingual TTS, 31 languages", the list includes `ru`, `uk`, `nl`, `fr`, `de`, `es`, `en`; "~398 MB"; "44.1 kHz mono fp32 output". Kazakh is not in the list. Kokoro, PocketTTS, Phonon and LFM3-Audio also listed.

## Open-source apps built on it (README Showcase, open-source mark)

- **Meeting Transcriber** (`pasrom/meeting-transcriber`): "macOS menu bar app that auto-detects, records, and transcribes meetings (Teams, Zoom, Webex) with dual-track speaker diarization. Uses Parakeet ASR and speaker diarization."
- **Subtitles** (`daformat/subtitles`): "Live captions for anything your Mac plays: meetings and calls, videos, podcasts and lectures, drawn as an always-on-top overlay that stays put while you switch apps. Captures system audio with a Core Audio process tap and transcribes entirely on-device, with selectable latency and optional speaker breaks. Uses Parakeet EOU and Nemotron streaming ASR, Silero VAD, and Sortformer speaker diarization on the Apple Neural Engine."
- **Muesli** (`pHequals7/muesli`): "Captures microphone and system audio with automatic speaker diarization."

## How to run here

- **Clone**: `git clone --depth 1 --branch v0.18.4 https://github.com/FluidInference/FluidAudio $EXTERNAL/FluidAudio`; read only. Read first: `README.md`, `Documentation/Models.md`, `Documentation/API.md`, `Documentation/CLI.md`.
- **Outbound calls**: the models are downloaded from Hugging Face (`Sources/FluidAudio/Shared/Download/`).
- **Install steps to avoid**: adding it to a project before a trial; a trial builds it with `swift build` in a throwaway copy, after the user's yes. Whether it builds with the Command Line Tools alone was not checked.
