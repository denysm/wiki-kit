# Voice subsystem — brainstorm inputs and research (2026-11-21)

Status: **research done, design not written yet.** This file carries the findings of one planning session so the design can continue on another machine without re-doing the research. The next step is `docs/voice-design.md` (brainstorm → design → phased plan). Nothing here is installed or adopted yet; tools named below that are not `in use` in `catalog/` need a catalog card and a sandbox trial first.

## Goal (owner's words, condensed)

1. Talk to the assistant by voice: live transcription and answers.
2. Record the owner's conversations with other people across channels, transcribe them, tell who spoke.
3. Keep logs, help answer questions, translate into the owner's language and back.
4. Work on all the owner's devices, as a kit-wide feature.

## Decided by the owner

- Devices: work Mac, home Mac, iPhone + Apple Watch, Windows (a locked-down corporate VDI and a PC).
- Channels: first Teams / Zoom / Webex calls on the Mac; in-person meetings later.
- Output: text on screen (subtitles, translation, hints) **and** voice in an earpiece, with a mode switch.
- Development runs on the home Mac (personal subscription); the work Mac only pulls, grants permissions and verifies on real calls. Results flow back as de-identified commits to this file or the design doc. Work data never goes to the home Mac or into the kit.

## Constraints

- Kit scripts: standard-library Python 3.9+ plus numpy, calling external binaries; Swift helpers built with `swiftc` (Command Line Tools, no Xcode) are allowed, as `scripts/pdf2txt.swift` already is. Heavy torch stacks only in an optional venv if clearly worth it.
- Reference machine (work Mac): Apple M4 Pro 24 GB, macOS 27.2, whisper.cpp 1.9.5 (`whisper-cli`, `whisper-stream`, `whisper-server`, `parakeet-cli`) with `ggml-large-v3-turbo`, ffmpeg 9, llama.cpp, Ollama with `gemma4:12b` and `embeddinggemma-2`, Swift 6.4. No Tailscale, no virtual audio device. A wireless DECT headset is used for calls.
- Windows VDI: 16-core CPU, no GPU, huggingface.co blocked, GitHub and PyPI reachable, installs restricted.
- Monthly paid-model budget is small: local processing by default, paid calls only on demand.

## Catalog check (2026-11-21)

`in use`: whisper.cpp `whisper-cli` + `large-v3-turbo`, ffmpeg audio extraction, Ollama, llama.cpp, superpowers `brainstorming`. `candidate`: whisper.cpp `whisper-server`, `whisper-vad-speech-segments` (files only), OpenSpec, elephant-goldfish `egm-brainstorm`, A2UI (too heavy for subtitles). **Empty** in the catalog: live `whisper-stream`, system-audio capture, live VAD, diarization, translation, TTS, wake word, browser microphone/streaming. These need cards (desk checks) before use. Side note: `catalog_fresh.py` reports ffmpeg upstream as "v0.6.1", which looks like a tag-sorting false positive (card 9.1, machine 9.0.2).

## Findings

### Capture (per device)

| Device | Approach | Notes |
|---|---|---|
| Mac | `swiftc` helper: Core Audio process tap on the call apps (or all output) + microphone in one aggregate device → 2-channel 16 kHz WAV, ch1 = me, ch2 = others | "Me vs others" needs no model. Without `NSAudioCaptureUsageDescription` the tap returns silent buffers with no error; ship the helper as a minimal ad-hoc-signed `.app` launched with `open` so it has its own permission; reset with `tccutil reset AudioCapture`. Base code: AudioTee (MIT, "API unstable"), AudioCap sample. Headset avoids bleed; on speakers the mic re-records the others. |
| Windows VDI | Capture on the **Mac endpoint**, not inside the VM | With Teams media optimization the call audio runs on the endpoint; inside the VM loopback hears nothing. Use the platform's own captions/transcripts where allowed. |
| Windows PC | WASAPI (process) loopback | Not designed yet. |
| iPhone | Take calls on the Mac; in person — Voice Memos (iPhone/Watch) saved to a synced folder the Mac watches | Built-in call recording is not available in the EU; apps cannot capture other apps' calls; a Safari web app loses the mic in background. A native iOS app needs Xcode. |
| Android | Pixel Recorder export only | Low priority. |

Reusable products: MacWhisper (proprietary; system audio, real-time, watch folder, Markdown) as a stopgap; anarlog (ex-Hyprnote, MIT) as the best open-source base; Meetily (MIT core). None puts me/others on separate channels.

### Speech recognition and diarization

| Use | Recommendation | Why / caveat |
|---|---|---|
| Mac live, now | `whisper-stream` + turbo, `--step 700-1000`, `--vad`, `-kc`, one stream per channel | Already installed; first text ~1–2 s (estimate), flickering tail. |
| Mac live, target | NVIDIA Nemotron 3.5 ASR Streaming 0.6B | Only streaming model found covering ru/uk/en/de/fr with punctuation; FLEURS WER en 7.91, de 8.31, fr 9.03, ru 9.17, uk 13.07 at 1.12 s chunks. Non-torch ports (ONNX, CoreML, OpenVINO) of unknown maturity; licence conflict between ports. |
| Rejected | Apple SpeechTranscriber (no ru/uk), Voxtral Realtime (no uk, GPU), Kyutai STT (en/fr) | |
| Mac after the call | `whisper-cli` turbo; second opinion `parakeet-cli` (Parakeet TDT v3, 25 EU languages) | Accurate pass replaces the live draft. |
| Diarization (others channel) | pyannote community-1 via FluidAudio / Argmax SpeakerKit (Swift) or sherpa-onnx | sherpa-onnx models are on GitHub releases (works where HF is blocked) and run on Windows CPU. Live options (Sortformer v2, LS-EEND) lack meeting DER evidence. |
| Naming speakers | Map clusters to platform transcript turns / participant list by time | Voiceprints only with explicit consent (biometric data). |
| Windows CPU | sherpa-onnx: Parakeet v3 int8 (~18–30× real time) + diarization | whisper.cpp ggml models would have to be carried in. |
| iPhone | Record and process on the Mac | WhisperKit / FluidAudio need an Xcode build. |

Streaming policy: SimulStreaming (AlignAtt) beats LocalAgreement per its authors; WhisperLiveKit wraps both. Main open test: **turbo vs Parakeet v3 vs Nemotron on 3–5 of the owner's own recordings of Russian speech with English terms** — no published WER covers that.

### Translation, voice output, interpretation

- Apple Translation works from a `swiftc` CLI via `TranslationSession(installedSource:target:)`, no app bundle: all 20 pairs among ru/uk/en/de/fr installed, 0.3–0.5 s per sentence (1.5 s first call). One error seen ("ordre du jour" → schedule).
- `gemma4:12b` via Ollama: 0.44–0.70 s warm per sentence; good as a context-aware second pass with a glossary.
- Cloud fallback: Claude Haiku 5.5 ≈ $0.03–0.05 per hour of speech (thinking off); DeepL ≈ $1.4/hour.
- Non-commercial licences to avoid: NLLB-200, SeamlessStreaming, Hibiki-Zero. Apple Live Translation and Teams Interpreter do not support ru/uk.
- TTS: macOS `say` — Milena (ru), Lesya (uk), 0.6–1.0 s per sentence; Enhanced/Premium voices not installed. Personal Voice is denied to an unsigned CLI. Kokoro has no ru/uk; Qwen3-TTS has ru, not uk; Piper engine is now GPL-3.0.
- Speaking into a call: virtual mic (BlackHole, GPL-3.0) only after the owner approves the text; disclose machine voice (EU AI Act Art. 50 transparency applies from 2026-08-02).
- UX evidence: earpiece translation users preferred 3–4 s lag; subtitle readers who do not know the source language accept lag but hate flicker.

### Claude-side

- Claude Code `/voice`: built-in dictation (hold or tap), ru and uk among 20 languages, no tokens consumed, **audio goes to Anthropic's cloud**, needs claude.ai sign-in (not an API key); works in the VS Code extension except remote sessions.
- Stop / SubagentStop hooks receive `last_assistant_message` → can be piped to `say` (voice answers today, no code beyond a hook).
- `claude -p` with `--output-format stream-json`, `--resume`; Agent SDK sessions. Messages API has no audio input/output and no realtime voice API.
- Prices per 1M tokens: Haiku 5.5 $0.10 in / $0.50 out (cache read $0.01); Sonnet 5.5 $2 / $10. A rolling-transcript assistant: ~$0.04/hour on Haiku, ~$0.70/hour on Sonnet (estimate).
- Claude apps voice mode is beta; custom remote MCP connectors in voice mode are not documented.

### Law and policy (not legal advice)

| Where | Recording a conversation you take part in |
|---|---|
| Germany §201 StGB | Offence without every speaker's consent; up to 3 years |
| Switzerland Art. 179ter StGB | Offence without the others' consent |
| France Art. 226-1 CP | Consent needed; presumed if done openly and nobody objected |
| Poland, Spain, Ukraine, UK, US federal | Participant may record; disclosure/use limited; US all-party states: CA, DE, FL, IL, MD, MA, MT, NV, NH, PA, WA |

- GDPR applies to work use (no household exemption); a notice gives transparency, not consent; voiceprints are special-category biometric data (explicit consent). EU AI Act bans emotion inference from voice at work (Art. 5(1)(f)).
- Live transcription without keeping audio does not help in France, the US or under GDPR; German commentators disagree.
- Cases: the Otter.ai class action survived dismissal (2026-08); a proposed class action targets a bot-free device-audio notetaker — the same design as this tool. Teams can auto-block external notetaker bots (2026-08).

**Safeguards, ranked (design requirements):** 1) employer approval before any work use; 2) per-session consent gate — notice in invitation and aloud, no objection; explicit yes where German, Swiss, French or US all-party law may apply; logged; 3) stay off when the organizer disabled recording or anyone objects; 4) no voiceprints without explicit, revocable consent; 5) no emotion or stress inference; 6) local processing, no stored audio by default, cloud only per explicit question with a minimal excerpt; 7) off for HR, health, legal, pricing and private calls; 8) short retention; 9) per-person access and deletion; 10) append-only audit log.

## Proposed phases (estimate: 12–16 sessions)

0. `/voice` dictation + Stop-hook `say` for spoken answers (config only).
1. Two-channel capture helper (`.app`) + `meeting2md.py` per channel.
2. Live subtitles and session log (JSONL: time, channel, speaker, text, translation).
3. Translation (Apple Translation, Gemma second pass) + text/earpiece mode switch.
4. Answers from the wiki on a hotkey (`search.py` + Haiku 5.5).
5. Post-call diarization, speaker naming, ingest into the wiki.
6. iPhone/Watch file path, VDI-from-endpoint, in-person meetings.

Each phase ends with a short check list for the work Mac (pull, permissions, a real call), whose de-identified results are committed back here.

## Open questions

- Recognition accuracy on the owner's speech (test above).
- Which app macOS credits for the tap permission when the tool starts from VS Code; whether an `open`-launched `.app` prompts cleanly on 27.2.
- Maturity and licence of Nemotron ports; whether FluidAudio / Argmax builds need Xcode.
- Employer policy on recording and AI tools.
- Home Mac hardware (Apple Silicon assumed).

## Sources (selection, dates as read 2026-11-21)

- whisper.cpp releases 1.9.0–1.9.5: https://github.com/ggml-org/whisper.cpp/releases
- Nemotron 3.5 ASR Streaming: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b (2026-06-04)
- FluidAudio: https://github.com/FluidInference/FluidAudio (v0.15.6, 2026-08-19)
- Argmax OSS: https://github.com/argmaxinc/argmax-oss-swift (v1.1.0, 2026-08-06)
- pyannote community-1: https://huggingface.co/pyannote/speaker-diarization-community-1 (2025-09)
- sherpa-onnx diarization models: https://csukuangfj.github.io/sherpa/onnx/speaker-diarization/models.html
- Core Audio taps: https://developer.apple.com/documentation/coreaudio/capturing-system-audio-with-core-audio-taps ; AudioTee: https://github.com/makeusabrew/audiotee
- Teams VDI media optimization: https://learn.microsoft.com/en-us/microsoftteams/vdi-2 (updated 2026-11-12)
- iPhone call recording: https://support.apple.com/en-ae/guide/iphone/iph57c6590e9/26/ios ; feature availability: https://www.apple.com/ios/feature-availability/
- Apple TranslationSession: https://developer.apple.com/documentation/translation/translationsession
- Open-source TTS overview: https://www.assemblyai.com/blog/free-open-source-text-to-speech (2026-11-18)
- Claude Code voice dictation: https://code.claude.com/docs/en/voice-dictation ; hooks: https://code.claude.com/docs/en/hooks.md ; pricing: https://platform.claude.com/docs/en/about-claude/pricing.md
- §201 StGB: https://www.gesetze-im-internet.de/stgb/__201.html ; GDPR: https://eur-lex.europa.eu/eli/reg/2016/679/oj ; AI Act: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- AI transcription in German businesses: https://www.heuking.de/en/news-events/newsletter-articles/detail/legally-compliant-use-of-ai-transcription-tools-in-businesses.html (2026-04-30)
- Otter.ai ruling: https://www.bairdholm.com/blog/core-privacy-claims-against-ai-note-taking-platform-survive-dismissal/ (2026-08-24)
- Digital Omnibus on AI: https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo (2026-07-27)
