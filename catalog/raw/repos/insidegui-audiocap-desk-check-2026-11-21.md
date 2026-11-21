---
title: "Desk check: insidegui/AudioCap at 6f609e8"
source: https://github.com/insidegui/AudioCap/tree/6f609e8
type: repos
authors: ["Guilherme Rambo"]
source_date: 2025-08-07
ingested: 2026-11-21
repo: insidegui/AudioCap
kind: app
version: "6f609e8"
licence: BSD-2-Clause
tags: [catalog, desk-check, kind-app, core-audio, process-tap, system-audio, macos, swift]
summary: "AudioCap read from a read-only clone at commit 6f609e8: Apple-platform sample code that records audio from another app with the Core Audio process tap API of macOS 14.4, documented step by step in its README; BSD-2-Clause; the permission check uses private TCC functions behind a build flag. Read as the baseline for the kit's own capture helper. Nothing built or run."
---

# Desk check: insidegui/AudioCap at 6f609e8

Read from a shallow clone of the default branch (commit `6f609e8`, committed 2025-08-07) at `$EXTERNAL/AudioCap`. There are no releases. Not modified; nothing built or run. Checked 2026-11-21.

## Repository facts

- GitHub description: "Sample code for recording system audio on macOS 14.4+". `gh api`: licence `BSD-2-Clause`, `pushed_at` 2025-08-07T17:55:05Z, default branch `main`, not archived. `LICENSE`: "Copyright (c) 2024 Guilherme Rambo".
- README: "With macOS 14.4, Apple introduced new API in CoreAudio that allows any app to capture audio from other apps or the entire system, as long as the user has given the app permission to do so." "This project is provided as documentation for this new API to help developers of audio apps."
- An Xcode project (`AudioCap.xcodeproj`), sources in `AudioCap/ProcessTap/`: `ProcessTap.swift` (268 lines), `AudioProcessController.swift`, `CoreAudioUtils.swift`, `AudioRecordingPermission.swift`.

## What the README and code show

- **Permission**: the prompt text comes from `NSAudioCaptureUsageDescription` in the app's Info.plist; "There’s no public API to request audio recording permission or to check if the app has that permission." `AudioRecordingPermission.swift` uses "TCC SPI" (`TCCAccessPreflight`, `TCCAccessRequest` on `kTCCServiceAudioCapture`, loaded with `dlopen` from the private TCC framework) behind `ENABLE_TCC_SPI`; without the flag "the permission will be requested the first time audio recording is started in the app."
- **Setup steps** (README): translate the PID with `kAudioHardwarePropertyTranslatePIDToProcessObject`; create a `CATapDescription` and keep its `uuid`; `AudioHardwareCreateProcessTap`; create an aggregate device whose `kAudioAggregateDeviceTapListKey` holds `[kAudioSubTapUIDKey: <tap uuid>]`, with `kAudioAggregateDeviceIsPrivateKey` true; read `kAudioTapPropertyFormat`; `AudioDeviceCreateIOProcIDWithBlock`; `AudioDeviceStart`; stop and destroy everything at the end.
- **Code details** (`ProcessTap.swift`): `CATapDescription(stereoMixdownOfProcesses: [objectID])`; `muteBehavior` `.mutedWhenTapped` or `.unmuted`; aggregate keys `kAudioAggregateDeviceMainSubDeviceKey` (the output device), `kAudioAggregateDeviceTapAutoStartKey: true`, `kAudioAggregateDeviceSubDeviceListKey` with the output device, and in the tap list `kAudioSubTapDriftCompensationKey: true`.

## Why `reference`

The kit writes its own capture helper against Apple's API (it needs the microphone and the tap in one device, memory-only buffers and no private API). AudioCap is read as the baseline for that code; its BSD-2-Clause licence allows reuse with the copyright notice. Its private TCC calls are not taken.
