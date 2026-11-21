---
title: "Apple Translation"
category: reference
kind: library
areas: [live-speech-and-calls]
url: https://developer.apple.com/documentation/translation/translationsession
version: "27.2.1"
licence: Apple system framework (macOS licence)
desk_checked: 2026-11-21
sources:
  - raw/repos/apple-translation-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-apple-translation-languages-and-speed.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-live-speech-and-calls, kind-library, translation, apple, on-device, swift]
confidence: medium
volatility: warm
verified: 2026-11-21
summary: "macOS's on-device translation framework: TranslationSession(installedSource:target:) works from a plain swiftc program, 0.3–0.5 s per sentence; ru, uk, en, fr, de, es, nl and Flemish (nl-BE) are supported, Kazakh is not. Tried in a sandbox, not yet in real use."
---

# Apple Translation

> A system framework (kind `library`, part of macOS, read on macOS `27.2.1`): translates text between two installed languages on the device. A command-line Swift program can use it with `init(installedSource:target:)`, available from macOS 26. Tried for call subtitles in a sandbox.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Translate a call's committed sentences into the listener's language within half a second, on the device | `TranslationSession(installedSource:target:)` | live-speech-and-calls |
| Translate the listener's own sentence into the call language to read or hear it back | `TranslationSession(installedSource:target:)` | live-speech-and-calls |
| Check which language pairs a Mac can translate before a call | `LanguageAvailability` | live-speech-and-calls |
| Not this: Kazakh. The pair status is `unsupported` | `LanguageAvailability` | live-speech-and-calls |

## Run it here

- **Nothing to install**: `import Translation` in a program built with `swiftc`; language packs come from the system's translation language settings, once per language.
- **Sends outward**: the language-pack download; translation itself runs on the device (documentation, not observed).
- **Do not install**: nothing.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `TranslationSession(installedSource:target:)` | Translates between two installed languages; 0.3–0.5 s per sentence, 1.5 s first call, one wrong term in the trial. | tried | macOS 26 or later, the two language packs | The real task that would move it to `in use`: live subtitles in a real call. |
| `LanguageAvailability` | Lists supported languages and pair status; Kazakh `unsupported`. | tried | macOS 15 or later | The real task: the session-start check of a call app. |
| `.translationTask` (SwiftUI) | The app path that lets the system prompt for language downloads. | candidate | A SwiftUI app | Try it when the app should offer the download itself. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Translate call sentences between ru/uk/en/de/fr | `TranslationSession(installedSource:target:)` | Works from a `swiftc` program with no app bundle; 0.3–0.5 s per sentence, 1.5 s first call; one wrong term. | No cost | [trial record](../../raw/notes/trials/2026-11-21-apple-translation-languages-and-speed.md) |
| 2026-11-21 | Check languages for a call | `LanguageAvailability` | ru, uk, en, fr, de, es, nl, nl-BE supported; Kazakh unsupported; packs not yet installed on that machine. | No cost | [trial record](../../raw/notes/trials/2026-11-21-apple-translation-languages-and-speed.md) |

## Verdict

The default live translator for the owner's languages except Kazakh: fast, on the device, free, no app bundle needed. Kazakh needs another engine (a local language model). Revisit after its first real call, or when a macOS release adds Kazakh.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[nvidia-nemo-speech-cpp|NVIDIA/NeMo-Speech.cpp]] (../references/nvidia-nemo-speech-cpp.md): `translate`, a local alternative

## Sources

- [Desk check: Apple Translation framework](../../raw/repos/apple-translation-desk-check-2026-11-21.md): classes, initializers, platforms.
- [Trial: Apple Translation languages and speed](../../raw/notes/trials/2026-11-21-apple-translation-languages-and-speed.md): speed, quality and the language list.
