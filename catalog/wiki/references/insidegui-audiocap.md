---
title: "insidegui/AudioCap"
category: reference
kind: app
areas: [live-speech-and-calls]
repo: insidegui/AudioCap
version: "6f609e8"
licence: BSD-2-Clause
desk_checked: 2026-11-21
sources:
  - raw/repos/insidegui-audiocap-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, kind-app, core-audio, process-tap, system-audio, macos, swift]
confidence: high
volatility: cold
verified: 2026-11-21
summary: "Sample app that documents the Core Audio process tap API of macOS 14.4: tap another app's sound through a private aggregate device and an IO proc. Read as the baseline for the kit's capture helper; BSD-2-Clause; its private permission calls are not taken."
---

# insidegui/AudioCap

> Sample code (kind `app`, licence BSD-2-Clause, commit `6f609e8` read in a clone) that records the sound of another app with the Core Audio process tap API introduced in macOS 14.4, with a step-by-step README. Used here as reading, not as a dependency.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Capture a call app's sound on a Mac without a virtual audio driver | `ProcessTap` | live-speech-and-calls |
| Know which Info.plist key and which steps a capture app needs | README "API Description" | live-speech-and-calls |
| Not this: check the system-audio permission through public API. There is none; AudioCap uses private TCC calls behind a flag | `AudioRecordingPermission` | live-speech-and-calls |

## Run it here

- **Clone, read-only**: `git clone --depth 1 https://github.com/insidegui/AudioCap $EXTERNAL/AudioCap`. Read first: `README.md`, then `AudioCap/ProcessTap/ProcessTap.swift`.
- **Building it** needs Xcode (an `.xcodeproj`); not needed to use it as reading.
- **Sends outward**: nothing found; it records locally.
- **Do not install**: nothing; copying code into the kit keeps the BSD-2-Clause notice.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `ProcessTap` | `CATapDescription` for one process, process tap, private aggregate device with tap list and drift compensation, IO proc block. | reference | Reading only | Consult when the kit's capture helper changes how it builds its aggregate device. |
| README "API Description" | The setup steps and the `NSAudioCaptureUsageDescription` key. | reference | Reading only | Consult when a macOS release changes the tap API. |
| `AudioRecordingPermission` | Permission check and request through private TCC functions, behind `ENABLE_TCC_SPI`. | rejected | Private API | Revisit if Apple publishes a public permission check. Rejected: private API, not needed when the first capture triggers the prompt. |
| `AudioProcessController`, `ProcessSelectionView`, `RecordingIndicator` | Lists audio-producing processes, picks one, shows a recording indicator. | listed | Reading only | Read when the helper needs a process picker. |

## Tried

none yet

## Verdict

The clearest public guide to Mac process taps; the kit's helper follows its steps with the microphone added to the same aggregate device and without private API. Revisit when macOS changes the tap API.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[makeusabrew-audiotee|makeusabrew/audiotee]] (../references/makeusabrew-audiotee.md): a command-line take on the same API

## Sources

- [Desk check: insidegui/AudioCap at 6f609e8](../../raw/repos/insidegui-audiocap-desk-check-2026-11-21.md): README steps, code details, licence, why it is a reference.
