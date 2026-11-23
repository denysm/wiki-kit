---
title: "Trial: macOS say — voices for nine languages and speed"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
url: https://developer.apple.com/documentation/avfaudio/avspeechsynthesizer
part: "say; Personal Voice"
version: "27.2.1"
status: tried
tags: [catalog, trial, kind-library, text-to-speech, apple, say]
summary: "Sandbox checks of macOS speech output for an earpiece voice, 2026-11-21: in the planning session say spoke a sentence in 0.6–1.0 s with Milena (ru) and Lesya (uk), Enhanced/Premium voices were not installed, and Personal Voice was denied to an unsigned command-line program; on an Apple M4 Mac mini with macOS 27.2.1 say -v '?' listed a voice for each of ru, uk, kk, en, fr, de, es, nl and nl-BE. No cost."
---

# Trial: macOS `say` — voices and speed

- **Tool and part**: macOS speech synthesis; `say`, and Personal Voice through `AVSpeechSynthesizer`.
- **Task, by kind**: speaking translations and answers into a listener's earpiece during a call.
- **Kind of record**: sandbox trials, not real use. Status after it: `tried`.

## Speed (planning session, 2026-11-21)

As recorded in `docs/design-research.md` of the owner's private voice repository (the kit's `docs/voice-design-research.md` until 2026-11-23) (the machine is not stated there): "macOS `say` — Milena (ru), Lesya (uk), 0.6–1.0 s per sentence; Enhanced/Premium voices not installed. Personal Voice is denied to an unsigned CLI."

## Voices on this machine (2026-11-21)

`say -v '?'` on an Apple M4 Mac mini, macOS 27.2.1, filtered to the listener's languages (novelty voices left out):

- ru_RU Milena; uk_UA Lesya; kk_KZ Aru; nl_BE Ellen; nl_NL Xander; es_ES Mónica; fr_FR Thomas, Jacques; de_DE Anna; en_US Samantha; en_GB Daniel.
- Eddy and Flo in en_US, en_GB, fr_FR, fr_CA, de_DE and es_ES.

## Cost

No tokens, no money: part of macOS.
