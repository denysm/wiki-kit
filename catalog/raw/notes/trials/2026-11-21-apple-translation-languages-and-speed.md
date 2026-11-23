---
title: "Trial: Apple Translation from a command-line Swift program — languages and speed"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
url: https://developer.apple.com/documentation/translation/translationsession
part: "TranslationSession(installedSource:target:), LanguageAvailability"
version: "27.2.1"
status: tried
tags: [catalog, trial, kind-library, translation, apple, on-device]
summary: "Two sandbox checks of Apple Translation for live call subtitles, 2026-11-21: in the planning session, TranslationSession(installedSource:target:) from a swiftc program translated a sentence in 0.3–0.5 s (1.5 s first call) across all 20 pairs of ru/uk/en/de/fr, with one wrong term; on an Apple M4 Mac mini with macOS 27.2.1, LanguageAvailability listed ru, uk, en, fr, de, es, nl and nl-BE as supported and Kazakh as unsupported. No cost."
---

# Trial: Apple Translation from a command-line Swift program

- **Tool and part**: Apple Translation framework; `TranslationSession(installedSource:target:)` and `LanguageAvailability`.
- **Task, by kind**: translating committed sentences of a call into the listener's language, live, on the device.
- **Kind of record**: sandbox trials, not real use. Status after it: `tried`.

## Speed and quality (planning session, 2026-11-21)

As recorded in `docs/design-research.md` of the owner's private voice repository (the kit's `docs/voice-design-research.md` until 2026-11-23) (the machine is not stated there): `TranslationSession(installedSource:target:)` works from a `swiftc` command-line program with no app bundle; all 20 pairs among ru/uk/en/de/fr were installed; 0.3–0.5 s per sentence, 1.5 s for the first call; one error seen: "ordre du jour" translated as "schedule".

## Languages on this machine (2026-11-21)

A throwaway `swiftc` program called `LanguageAvailability().supportedLanguages` and `status(from:to:)` on an Apple M4 Mac mini, macOS 27.2.1:

- Supported: `ar-AE ar-SA da de de-AT de-CH en en-AU en-CA en-GB en-IE en-IN en-NZ en-SG en-ZA es es-CL es-MX es-US fi fr fr-BE fr-CH fr-CA he hi id it it-CH ja ko ms nb nl nl-BE pl pt pt-PT ru sv th tr uk vi zh zh-HK zh-TW`.
- From ru, en and fr to each of the others among ru, en, fr, uk, nl, es, de: `supported`; to `kk` (Kazakh): `unsupported`.
- On this machine the pairs are `supported`, not `installed`: the language packs still have to be downloaded before `init(installedSource:target:)` can use them.

## Cost

No tokens, no money: the framework is part of macOS.
