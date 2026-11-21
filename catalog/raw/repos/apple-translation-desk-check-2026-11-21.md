---
title: "Desk check: Apple Translation framework (macOS 27.2.1)"
source: https://developer.apple.com/documentation/translation/translationsession
type: repos
authors: ["Apple"]
source_date: 2026-11-21
ingested: 2026-11-21
url: https://developer.apple.com/documentation/translation/translationsession
kind: library
version: "27.2.1"
licence: Apple system framework (macOS licence)
tags: [catalog, desk-check, kind-library, translation, apple, on-device, swift]
summary: "Apple's on-device Translation framework read from its developer documentation (JSON endpoints) on 2026-11-21: TranslationSession from macOS 15, the installedSource:target: initializer for languages already on the device from macOS 26, LanguageAvailability for supported pairs. Part of macOS; no install. Measurements are in the trial record."
---

# Desk check: Apple Translation framework (macOS 27.2.1)

Read from Apple's documentation through its JSON endpoints (`https://developer.apple.com/tutorials/data/documentation/translation/translationsession.json` and the initializer's page) on 2026-11-21. The framework ships with macOS; the machine that ran the checks has macOS 27.2.1.

## Facts from the documentation

- `TranslationSession`: "A class that performs translations between a pair of languages." Platforms: iOS 18.0, iPadOS 18.0, Mac Catalyst 26.0, macOS 15.0.
- Initializers listed: `init(installedSource:target:)` and `init(installedSource:target:preferredStrategy:)`.
- `init(installedSource:target:)`: "Creates a translation session to translate between a given source and target language already installed on device." Platforms: iOS 26.0, iPadOS 26.0, Mac Catalyst 26.0, macOS 26.0.
- Languages are downloaded by the system ("already installed on device"); a session created this way does not download them itself.

## How to run here

- Nothing to install: `import Translation` in a Swift program built with `swiftc` (Command Line Tools). Language packs are downloaded through the system's translation language settings.
- **Sends outward**: translation runs on the device once the language packs are installed; downloading packs is the outbound call. Read in the documentation, not observed.

## Parts

- `TranslationSession(installedSource:target:)`: translate strings between two installed languages, from a plain command-line program.
- `LanguageAvailability`: the supported languages and the status of a pair (`supported`, `installed`, `unsupported`).
- SwiftUI `.translationTask`: the documented path for apps that let the system download languages with a prompt; not read further.
