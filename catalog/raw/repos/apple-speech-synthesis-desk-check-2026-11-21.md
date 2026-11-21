---
title: "Desk check: Apple speech synthesis — say and AVSpeechSynthesizer (macOS 27.2.1)"
source: https://developer.apple.com/documentation/avfaudio/avspeechsynthesizer
type: repos
authors: ["Apple"]
source_date: 2026-11-21
ingested: 2026-11-21
url: https://developer.apple.com/documentation/avfaudio/avspeechsynthesizer
kind: library
version: "27.2.1"
licence: Apple system software (macOS licence)
tags: [catalog, desk-check, kind-library, text-to-speech, apple, on-device, say]
summary: "macOS speech output read on 2026-11-21: the say command (man page: voice, rate, output file, audio device) and AVSpeechSynthesizer with speechVoices and Personal Voice authorization (developer documentation JSON). Part of macOS; no install. The voices installed on one machine are in the trial record."
---

# Desk check: Apple speech synthesis (macOS 27.2.1)

Read on 2026-11-21 from `man say` on macOS 27.2.1 and from Apple's documentation JSON endpoints for `AVSpeechSynthesizer`, `AVSpeechSynthesisVoice.speechVoices()` and `requestPersonalVoiceAuthorization(completionHandler:)`.

## `say` (man page)

- Options: `-v voice, --voice=voice`; `-r rate, --rate=rate`; `-o out.aiff, --output-file=file`; `-a ID, --audio-device=ID` and `-a name, --audio-device=name`; `-f file, --input-file=file`; `-i, --interactive`; `--progress`; `--file-format=format`; `--data-format=format`. `say -v '?'` lists the voices.
- `--audio-device` lets a program send speech to one output device (for example a headset) instead of the system default.

## `AVSpeechSynthesizer` (documentation)

- `AVSpeechSynthesizer`: "An object that produces synthesized speech from text utterances and enables monitoring or controlling of ongoing speech." Platforms: iOS 7.0, macOS 10.14.
- `AVSpeechSynthesisVoice.speechVoices()`: "Retrieves all available voices on the device." macOS 10.14.
- `requestPersonalVoiceAuthorization(completionHandler:)`: "Prompts the user to authorize your app to use personal voices." macOS 14.0.

## How to run here

- Nothing to install; `say` is on every Mac, `AVSpeechSynthesizer` is in AVFAudio. Enhanced and Premium voices are optional downloads in the system's spoken content settings.
- **Sends outward**: nothing for synthesis; voice downloads only.
- Speaking from inside a capture app keeps the speech in that app's process, so a tap that excludes the app does not record it; `say` runs as a separate process.
