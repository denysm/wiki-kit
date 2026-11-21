---
title: "Apple speech synthesis (say, AVSpeechSynthesizer)"
category: reference
kind: library
areas: [live-speech-and-calls]
url: https://developer.apple.com/documentation/avfaudio/avspeechsynthesizer
version: "27.2.1"
licence: Apple system software (macOS licence)
desk_checked: 2026-11-21
sources:
  - raw/repos/apple-speech-synthesis-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-apple-speech-synthesis-voices-and-speed.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, kind-library, text-to-speech, apple, on-device, say]
confidence: medium
volatility: warm
verified: 2026-11-21
summary: "macOS speech output: the say command and AVSpeechSynthesizer. say speaks a sentence in 0.6–1.0 s; installed voices cover ru, uk, kk, en, fr, de, es, nl and Flemish; say can target one audio device. Personal Voice was denied to an unsigned command-line program. Tried in a sandbox."
---

# Apple speech synthesis (`say`, `AVSpeechSynthesizer`)

> System speech output (kind `library`, part of macOS, read on macOS `27.2.1`): the `say` command and the `AVSpeechSynthesizer` class speak text with the installed voices, on the device. The voices on the trial machine cover every language the owner needs, Kazakh included. Tried in a sandbox.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Speak a translated sentence into a headset during a call, in the listener's language | `AVSpeechSynthesizer` | live-speech-and-calls |
| Read an assistant's answer aloud from a script or a hook | `say` | live-speech-and-calls |
| Send speech to the headset only, not the speakers (`--audio-device`) | `say` | live-speech-and-calls |
| Speak Kazakh, Flemish or Ukrainian when other engines have no voice for them | installed voices | live-speech-and-calls |

## Run it here

- **Nothing to install**: `say` and AVFAudio ship with macOS. Better voices are optional downloads (Enhanced, Premium) in the system's spoken content settings.
- **Sends outward**: nothing for synthesis.
- **Keep in mind**: speech made inside a capture app stays in that app's process and can be left out of the capture; `say` is a separate process.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `say` | Speaks text with a chosen voice, rate and output device; 0.6–1.0 s per sentence in the trial. | tried | Nothing | The real task that would move it to `in use`: spoken answers from a Claude Code hook. |
| installed voices | ru Milena, uk Lesya, kk Aru, nl-BE Ellen, nl Xander, es Mónica, fr Thomas, de Anna, en Samantha on the trial machine. | tried | The voices; Enhanced/Premium are extra downloads | The real task: the earpiece voice in a real call. |
| `AVSpeechSynthesizer` | In-process synthesis with `speechVoices()`. | candidate | AVFAudio, macOS 10.14 or later | Try it inside the capture app, checking that its speech stays out of the tapped track. |
| Personal Voice | The user's own synthetic voice; authorization from macOS 14.0. | tried | A signed app and the user's consent | The real task: a signed capture app asks for it; denied to an unsigned command-line program in the trial. |
| Enhanced and Premium voices | Higher-quality voices. | candidate | A download per voice | Try one for ru and fr against the compact voices. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Speak sentences in Russian and Ukrainian | `say` | 0.6–1.0 s per sentence with Milena and Lesya. | No cost | [trial record](../../raw/notes/trials/2026-11-21-apple-speech-synthesis-voices-and-speed.md) |
| 2026-11-21 | List voices for nine languages | installed voices | A voice for each of ru, uk, kk, en, fr, de, es, nl, nl-BE. | No cost | [trial record](../../raw/notes/trials/2026-11-21-apple-speech-synthesis-voices-and-speed.md) |
| 2026-11-21 | Use the owner's own voice | Personal Voice | Denied to an unsigned command-line program. | No cost | [trial record](../../raw/notes/trials/2026-11-21-apple-speech-synthesis-voices-and-speed.md) |

## Verdict

The default earpiece voice: free, on the device, every needed language including Kazakh, about a second per sentence. Compact voices sound plain; Enhanced voices and neural engines (FluidAudio's Supertonic-3, NeMo-Speech.cpp's Magpie) are the quality challengers. Revisit after the first real call with the earpiece.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[fluidinference-fluidaudio|FluidInference/FluidAudio]] (../references/fluidinference-fluidaudio.md): Supertonic-3

## Sources

- [Desk check: Apple speech synthesis](../../raw/repos/apple-speech-synthesis-desk-check-2026-11-21.md): `say` options, class documentation.
- [Trial: macOS say voices and speed](../../raw/notes/trials/2026-11-21-apple-speech-synthesis-voices-and-speed.md): timings, voices, Personal Voice.
