---
title: "makeusabrew/audiotee"
category: reference
kind: cli
areas: [live-speech-and-calls]
repo: makeusabrew/audiotee
version: "56ac954"
licence: none stated
desk_checked: 2026-11-21
sources:
  - raw/repos/makeusabrew-audiotee-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, kind-cli, core-audio, process-tap, system-audio, macos, swift]
confidence: high
volatility: warm
verified: 2026-11-21
summary: "Swift command-line tool that streams system or per-process audio as raw PCM through Core Audio taps (macOS 14.2+), with exclude lists and 16 kHz output. No licence, so it is reading only; its exclude-mode tap is the idea the kit's helper uses to keep its own voice out of the capture."
---

# makeusabrew/audiotee

> A command-line tool (kind `cli`, no licence stated, commit `56ac954` read in a clone) that writes the Mac's output audio, from all processes or a chosen set, to stdout as raw PCM using Core Audio taps. It has no licence file, so it is read for ideas, not reused.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Capture all output audio except some processes (for example your own app's voice) | `--exclude-processes` | live-speech-and-calls |
| Pipe system audio at 16 kHz into another program | `--sample-rate` | live-speech-and-calls |
| Not this: reuse its code in the kit. No licence | `AudioTapManager` | live-speech-and-calls |

## Run it here

- **Clone, read-only**: `git clone --depth 1 https://github.com/makeusabrew/audiotee $EXTERNAL/audiotee`. Read first: `README.md`, then `Sources/AudioTeeCore/Core/AudioTapManager.swift`.
- **Sends outward**: nothing; it writes PCM to stdout.
- **Do not install**: nothing; do not copy its code (no licence).

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `--exclude-processes` | Taps all output except the listed process IDs (`isExclusive`). | reference | Reading only | Consult when the helper's own-voice exclusion misbehaves. |
| `--sample-rate` | Resamples and converts to 16-bit integers. | reference | Reading only | Consult when choosing where the helper resamples. |
| `AudioTapManager` | Private tap and private aggregate device with an empty sub-device list. | reference | Reading only | Consult when the helper's tap setup fails. |
| `--include-processes`, `--mute`, `--stereo`, `--chunk-duration` | Per-process tap, muting, stereo, chunk size (default 0.2 s). | listed | A build of the tool | Read when a stdout capture tool is wanted for a test. |

## Tried

none yet

## Verdict

A compact reference for exclude-mode taps; not usable as code without a licence. Revisit if the repository adds one.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[insidegui-audiocap|insidegui/AudioCap]] (../references/insidegui-audiocap.md): the BSD-licensed sample of the same API

## Sources

- [Desk check: makeusabrew/audiotee at 56ac954](../../raw/repos/makeusabrew-audiotee-desk-check-2026-11-21.md): options, tap setup, the missing licence.
