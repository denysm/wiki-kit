---
title: "FluidInference/FluidAudio"
category: reference
kind: library
areas: [live-speech-and-calls, converting-documents-and-recordings]
repo: FluidInference/FluidAudio
version: "0.18.4"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/fluidinference-fluidaudio-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, area-converting-documents-and-recordings, kind-library, swift, coreml, neural-engine, speech-to-text, streaming, diarization, vad, text-to-speech, echo-cancellation]
confidence: medium
volatility: hot
verified: 2026-11-21
summary: "Swift package (no package dependencies) that runs CoreML conversions of open speech models on the Apple Neural Engine: Parakeet v3 and Ultra, streaming Nemotron and Parakeet EOU, Sortformer, LS-EEND and pyannote diarization, Silero VAD, LocalVQE echo cancellation, Supertonic-3 speech in 31 languages. Read, not built; models from Hugging Face."
---

# FluidInference/FluidAudio

> A Swift library (kind `library`, licence Apache-2.0, version `0.18.4` read in a clone) for macOS 14 and iOS 17 that runs speech recognition, diarization, voice detection, echo cancellation and speech synthesis as CoreML models on the Neural Engine, leaving the CPU and GPU free. Open-source meeting and live-caption apps are built on it. Not tried yet.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Transcribe a finished call inside a Swift app, on the Neural Engine, in 25 European languages | Parakeet Ultra | converting-documents-and-recordings |
| Show live text for an English, French, German or Spanish speaker in a Swift app | Nemotron Speech Streaming Multilingual 0.6B | live-speech-and-calls |
| Tell up to 4 speakers apart while a call runs | Sortformer | live-speech-and-calls |
| Separate speakers after a call | Pyannote CoreML Pipeline | converting-documents-and-recordings |
| Cut speech from silence before recognition | Silero VAD | live-speech-and-calls |
| Remove loudspeaker echo from the microphone when no headset is used | LocalVQE | live-speech-and-calls |
| Speak text in Russian, Ukrainian, Dutch, French, German or Spanish from a Swift app | Supertonic-3 | live-speech-and-calls |
| Read the code of open-source apps that already capture both sides of a Mac call | Showcase apps | live-speech-and-calls |

## Run it here

- **Clone, read-only**: `git clone --depth 1 --branch v0.18.4 https://github.com/FluidInference/FluidAudio $EXTERNAL/FluidAudio`. Read first: `README.md`, `Documentation/Models.md`, `Documentation/API.md`.
- **To try it**: `swift build` in a throwaway copy; whether the Command Line Tools alone are enough is not checked yet. Each model downloads from Hugging Face on first use.
- **Sends outward**: model downloads only; no telemetry code found in `Sources/`.
- **Do not install**: adding the package to a project before a trial; real use waits for the user's yes.

## What's inside

Parts are the model managers listed in `Documentation/Models.md` that matter for calls.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| Parakeet TDT v3 | Batch recognition, 25 European languages, default model. | candidate | The package and the CoreML model | Try it on the speech-recognition bench. |
| Parakeet Ultra | Post-trained v3: FLEURS 24-language mean 11.67 vs 14.81 %, int8 encoder (595 MB), recommended. | candidate | The package and the model | Try it on the bench next to v3. |
| Nemotron Speech Streaming Multilingual 0.6B | Streaming, en/es/fr/it/pt/de/zh/ja with `auto`, chunks 560ms to 4480ms; no Russian. | candidate | The package and the model | Try it for an English "them" track against NeMo-Speech.cpp. |
| Nemotron Unified ASR 0.6B | Streaming and offline, 25 European languages, latency bundles 2.08 s / 1.12 s / 0.56 s; fp16 default. | candidate | The package and the model | Try it for Russian live text, after checking its language list. |
| Parakeet EOU | English streaming, 120M, 160ms / 320ms / 1280ms. | candidate | The package and the model | Try it when an English-only call needs the lowest latency. |
| Sortformer | Streaming diarization, up to 4 speakers, 480ms per update. | candidate | The package and the model | Try it on a call recording with 3–4 speakers. |
| LS-EEND | Research prototype, up to 10 speakers. | listed | The package and the model | Read when calls have more than 4 speakers. |
| Pyannote CoreML Pipeline | Online (3.1-based) and offline (community-1-based) diarization. | candidate | The package and the models | Try it for the after-call pass against Sortformer. |
| Silero VAD | Voice activity detection. | candidate | The package | Try it if the recogniser has no VAD of its own. |
| LocalVQE | Echo cancellation and noise suppression for 16 kHz mic audio given the far-end signal, 16 ms latency, beta. | candidate | The package; the call's own sound as reference | Try it on a call taken on speakers. |
| Supertonic-3 | TTS in 31 languages incl. ru, uk, nl, fr, de, es; ~398 MB; 44.1 kHz. | candidate | The package and the model | Try it against the system voices for the earpiece. |
| Showcase apps | Open-source Meeting Transcriber (dual-track, Teams/Zoom/Webex), Subtitles (process tap, overlay), Muesli. | reference | Their own repositories | Consult when building the capture app or the overlay. |
| Kokoro, PocketTTS, Phonon, LFM3-Audio, Cohere Transcribe, SenseVoice, Paraformer, Transcribe Lite | Other TTS and recognition models. | listed | The package and the model | Read when the candidates above fall short. |

## Tried

none yet

## Verdict

The fastest-looking path for a native Mac call app: everything on the Neural Engine, permissive licences, real apps already shaped like the planned one. Its streaming Russian rests on Nemotron Unified, whose language list is still unread; NeMo-Speech.cpp covers that gap on Metal. Revisit after the bench and a build check with and without Xcode, or on a release after `0.18.4`.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page
- [[nvidia-parakeet-tdt-0-6b-v3|nvidia/parakeet-tdt-0.6b-v3]] (../references/nvidia-parakeet-tdt-0-6b-v3.md)
- [[snakers4-silero-vad|snakers4/silero-vad]] (../references/snakers4-silero-vad.md)
- [[apple-speech-synthesis|Apple speech synthesis (say, AVSpeechSynthesizer)]] (../references/apple-speech-synthesis.md): the system voices Supertonic-3 competes with
- [[nvidia-nemotron-3-5-asr-streaming-0-6b|nvidia/nemotron-3.5-asr-streaming-0.6b]] (../references/nvidia-nemotron-3-5-asr-streaming-0-6b.md): the model behind its multilingual streaming conversion

## Sources

- [Desk check: FluidInference/FluidAudio v0.18.4](../../raw/repos/fluidinference-fluidaudio-desk-check-2026-11-21.md): package facts, model list, showcase apps, outbound calls.
