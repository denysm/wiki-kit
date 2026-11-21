---
title: "Desk check: makeusabrew/audiotee at 56ac954"
source: https://github.com/makeusabrew/audiotee/tree/56ac954
type: repos
authors: ["makeusabrew"]
source_date: 2026-03-31
ingested: 2026-11-21
repo: makeusabrew/audiotee
kind: cli
version: "56ac954"
licence: none stated
tags: [catalog, desk-check, kind-cli, core-audio, process-tap, system-audio, macos, swift]
summary: "AudioTee read from a read-only clone at commit 56ac954: a Swift command-line tool that streams system or per-process output audio as raw PCM to stdout through Core Audio taps (macOS 14.2+), with include/exclude process lists, mute, mono or stereo, resampling to 16 kHz. No licence file and no licence in the README, so it is reading only. Nothing built or run."
---

# Desk check: makeusabrew/audiotee at 56ac954

Read from a shallow clone of the default branch (commit `56ac954`, committed 2026-03-31) at `$EXTERNAL/audiotee`. No releases. Not modified; nothing built or run. Checked 2026-11-21.

## Repository facts

- GitHub description: "Capture system audio output on macOS using Apple's Core Audio taps API." `gh api`: licence `null`, `pushed_at` 2026-03-31T13:12:49Z, default branch `main`, not archived.
- **No licence**: the clone has no `LICENSE` file and the README names none. An earlier session noted it as MIT; that is not supported by the repository. Without a licence its code cannot be copied; it is read for ideas only.
- A Swift package (`Package.swift`, `Sources/AudioTeeCore`, `Sources/AudioTeeCLI`, `Tests`).

## What it does (README and code)

- "System audio is captured using the Core Audio taps API introduced in macOS 14.2"; requirements "macOS 14.2 or later" and system audio recording permission.
- "By default, AudioTee captures audio output from **all** running processes." "Tap output defaults to `mono`"; "Only the default output device is currently supported."
- Options: `--include-processes`, `--exclude-processes` (process IDs), `--mute` ("Mute processes being tapped"), `--stereo`, `--sample-rate` (8000, 16000, 22050, 24000, 32000, 44100, 48000), `--chunk-duration` ("[default: 0.2, max: 5.0]"). "Any sample rate (even one matching your device default) converts to 16-bit signed integers". Output is raw PCM on stdout (`swift run audiotee --sample-rate 16000 > output.pcm`).
- Permissions: "There is no provision in the code to pre-emptively check for the required `NSAudioCaptureUsageDescription` permission, so you'll be prompted the first time AudioTee tries to record anything"; "some terminal emulators like iTerm don't always prompt for these permissions (though the macOS builtin terminal definitely does)".
- `AudioTapManager.swift`: a `CATapDescription` with `processes`, `isPrivate = true`, `isMixdown = true`, `isMono`, `isExclusive` (the exclude mode: the listed processes are left out), `deviceUID = nil` (system default); a private aggregate device with an empty sub-device list, then the tap added through `kAudioAggregateDevicePropertyTapList`.

## Why `reference`

The idea of "all output except listed processes" (`isExclusive`) is the one the kit's helper needs to leave its own speech out of the "them" track; the code itself is not reused because it has no licence.
