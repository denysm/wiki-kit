# Voice subsystem — design

Status: **approved by the owner on 2026-11-21**; the plan of record. Test recordings for the accuracy test: 3 read texts + 2 free talks (owner, 2026-11-21). Written after a brainstorm with the owner, using the `brainstorming` method of obra/superpowers 7.0.2 read from a clone (catalog status `in use`). The findings, law and sources behind it are in [voice-design-research.md](voice-design-research.md); this file does not repeat them. Results from the work Mac come back into the "Work Mac check" sections at the end, de-identified.

## Intent

The owner wants every call they take to turn into live text they can follow, in their own language, with the call language on demand, and later into an accurate transcript in their wiki. They also want to talk to the assistant by voice. It is for the owner personally, on their own machines; it is not deployed for an organisation. In the owner's words, it must be "perfectly fast, smooth and of high quality".

## Goals

1. **Live text for both sides.** While a Teams, Zoom or Webex call runs on a Mac, show what "me" (the owner's microphone) and "them" (the call app's sound) say, within about a second of the speech, without words changing after they are shown.
2. **Translation both ways.** Their speech in the owner's language on screen, and spoken into the owner's earpiece on a switch. The owner's own phrase in the call language on screen and, on a key press, spoken into the owner's earpiece so they can repeat it (for example, answering in French).
3. **An accurate record.** After the call, a precise transcript with speakers, then a Markdown source for the wiki.
4. **Answers during the call.** On a key press, an answer from the wiki and a local model; Claude only on its own key.
5. **Voice with the assistant.** Dictate prompts and hear answers in Claude Code.
6. **All the owner's devices**, in the order of the device matrix below.

## Non-goals (phases 0–6)

- A machine voice speaking into the call (virtual microphone).
- A native iPhone or Android app.
- Recognising people by voiceprint.
- Cloud speech recognition.

## Anti-goals (a failure even if everything else works)

- Call audio on disk without recording consent.
- Anything running that the other participants were not told about.
- Subtitles that flicker or rewrite themselves so they cannot be read; an earpiece voice more than about 4 s behind.
- The helper's own voice (translation, answers) appearing in the "them" track.
- The subtitle window visible to others when the owner shares their screen.
- Spending the work Mac's subscription quota without the owner pressing a key for it.
- Work data in the kit, on the home Mac, or in the home wiki.

## Constraints

- Both Macs now have **Xcode 27.2** (installed 2026-11-21) next to Swift 6.4. The kit still aims to build with `swift build` from the Command Line Tools for friends who have no Xcode; a part that only builds with Xcode stays optional, and whisper.cpp stays the default engine for them.
- Development and tests on the home Mac (M4, 16 GB); the work Mac (M4 Pro, 24 GB) only pulls, grants permissions, checks on real calls and connects the work wiki. Work Mac sessions are short and mechanical: everything they run is committed first, with exact commands.
- Local processing by default. Claude runs on subscriptions only (`claude -p`, no API key); the work Mac's quota is nearly used up.
- The kit is public: no names of the employer, customers or people; `leak_check.py` before every push.
- Tools are chosen through `catalog/wiki/topics/task-index.md`; a `candidate` or `listed` part is tried only in a sandbox and after the owner's yes, and the trial is recorded in the catalog.
- Kit scripts: standard-library Python plus numpy, calling binaries. The live path is native Swift (below).

## Decided by the owner (2026-11-21)

1. **Work use is approved by the employer** for recording and AI notes. The work Mac checks run on real calls with colleagues, through the consent gate. The work Mac's local config holds the approval date, no names.
2. **Audio lives in memory only.** Both tracks are kept in RAM for the whole call, never written to disk; after the call the precise pass, speaker separation and analysis run from memory, then the buffer is wiped. When everyone has agreed to recording (for example, the meeting is recorded anyway), the gate allows saving the audio to a file in the owner's recordings folder, never in the wiki or the kit.
3. **Back-translation goes to the owner only**: as text on screen, and on a key press as speech in the owner's earpiece. Nothing machine-voiced goes into the call.
4. **Tone and emotion analysis** is wanted for the owner's personal use; the owner works outside the EU, uses the output there, and takes international calls.
5. **The fastest, most optimal variant**: the owner handed over the how ("пусть будет самый шустрый и оптимальный вариант").
6. **Languages** (2026-11-21): first Russian with English terms, English and French; then Russian, Ukrainian, Kazakh, Flemish (Belgian Dutch), Dutch, Spanish and German; others may follow.
7. **Home test calls** run in Zoom and Teams (free versions installed at home), with Bluetooth headphones on the home Mac as the "me" microphone and the owner's iPhone with a wired headset as the second participant.

## Approaches considered

| Approach | What it trades | Verdict |
|---|---|---|
| A. Swift helper for capture and window + Python orchestrator on the live path | Reuses kit Python live; every chunk of audio crosses a process boundary, adding latency and a second place where audio lives | Superseded by C once Xcode was in place and speed became the first goal |
| B. Fork an open-source meeting app (anarlog, Meetily) | Ready UI and summaries; large Rust/TypeScript code bases, no "me / them" split, a fork to maintain, outside the kit's constraints | Rejected |
| **C. Native live path**: one Swift app holds capture, buffer, voice detection, recognition, translation, speech output and the window; kit Python works after the call and for wiki answers | Fastest (no process hops, Neural Engine and Metal in-process); audio stays in one process, which makes "memory only" natural; more Swift code | **Picked** (owner: fastest, Xcode installed) |

## Design

### The app and the scripts

- **Kit Voice** (`voice/` in the kit): a SwiftPM package that builds a small macOS app bundle, `KitVoice.app`, with a menu-bar icon and no Dock icon. Bundle id `local.wiki-kit.voice` (no personal handle). It holds every live layer below.
- **Kit scripts** (`scripts/`, Python): turn a finished session into a wiki source, answer from the wiki, speak Claude Code's answers (phase 0).
- **The engines** (speech recognition, voice detection, speaker separation) sit behind one Swift protocol each, so a model can be swapped by configuration after a measurement, without rewriting the app.

### Layers

```text
call app sound ── process tap ──┐
                                 ├─► two-track buffer in RAM ─┬─► voice detection ─► recogniser "me"  ─┐
microphone (headset) ───────────┘   (16 kHz, mlock)           └─► voice detection ─► recogniser "them" ─┤
                                                                                                        ▼
                    window: subtitles, translation, hints ◄── translator ◄── committed sentences ──► session log (text)
                    earpiece: speech (switch, key)       ◄──┘
after the call (same app, from RAM): precise pass ─► speaker separation ─► analysis ─► Markdown ─► kit scripts ─► wiki raw/
```

**1. Capture.** A Core Audio process tap on the call apps (Teams, Zoom, Webex, by bundle id), or on all output except Kit Voice itself, plus the microphone, in one private aggregate device, so both tracks share a clock and arrive in one callback. Each track is converted in-process to 16 kHz mono and appended to a ring buffer in RAM (about 230 MB per hour for two 16-bit tracks), locked against paging where the memory-lock limit allows. Kit Voice speaks through its own process, so a tap that excludes it never hears its own voice. It asks for two permissions: microphone and system audio recording (`NSAudioCaptureUsageDescription`; without it the tap returns silence and no error). It is signed with one stable identity so the permissions survive rebuilds.

**2. Recognition, live.** Per track: voice detection cuts speech from silence; a streaming recogniser produces a dim tail that may still change and committed words that never change. Committing follows the engine's own streaming output, or agreement between consecutive hypotheses for engines that have none. Languages are set per track per session (default: "me" Russian, "them" English, `auto` allowed). A per-session glossary of names and terms is fed to engines that accept one.

**3. Speaker separation.** "Me" and "them" come from the tracks, with no model. Inside "them", speakers are separated after the call, from RAM. Names come from the platform transcript or participant list by time, the way `meeting2md.py` already maps Teams turns, or are typed by the owner. No voiceprints are enrolled or stored.

**4. Translation and answers.**
- Committed sentences go to Apple Translation in-process. A glossary-aware second pass by the local `gemma4:12b` (Ollama) improves the log, not the live line.
- The owner's sentence is translated into the call language; a key speaks it into the earpiece.
- On the answer key, the question and the last minutes of transcript go to the kit's `search.py` over the wiki and to the local model. On the Claude key, they go to `claude -p` with a minimal excerpt, and the cost line goes into the log.

**5. Output.**
- **Window:** a borderless, always-on-top panel over the call that does not take focus. It shows "me" and "them" lines in two colours, the uncommitted tail dimmed and the translation under each line. Size, opacity and position are adjustable, and clicks can pass through it. It is excluded from screen capture, which is checked on real screen shares.
- **Earpiece:** speech from Kit Voice's own synthesiser to a chosen output device (default: the system output, normally the headset). Voices are taken per language from the installed system voices.
- **Mode switch** (hotkey and menu): text, text and voice, voice, off.

**6. Session log.**
- **Text log:** JSONL per session, with time, track, speaker, language, text, committed flag, translation, engine and latency. It lives outside the wiki and the kit, in the app's support folder, and is deleted after 30 days by default.
- **Audit log:** a separate append-only file records gate answers, start, stop, saves and deletions, with no names.

**7. Into the wiki.** A kit script turns the session's precise transcript into the format `meeting2md.py` writes (`**Name** [m:ss]` blocks), with raw-source frontmatter, and drops it into the chosen topic's inbox or `raw/`. On the work Mac that is the work wiki; at home, a personal topic. Compiling stays a separate, explicit step.

### Consent gate (mandatory)

Nothing is captured until the gate passes, every session; no answer is remembered from an earlier call.

| Gate line | Effect |
|---|---|
| Call category: work, personal, other | `work` is offered only when the local config holds the employer-approval date. Blocked outright: HR, health, legal, pricing and others' private calls. |
| Notice given (in the invitation or aloud) | Required. Suggested words: "I use a local tool for notes and analysis of our conversation; tell me if you object." |
| Nobody objected; recording not disabled by the organiser | Required. |
| Someone may be in Germany, Switzerland, France or a US all-party state | Then an explicit "yes" from everyone is required. |
| Everyone agreed to recording | Optional; only then may the audio be saved to a file. |
| Tone analysis | Optional; offered only when the owner enabled it in the local config. |

While capturing, the menu-bar icon shows a red dot. **Pause** stops capture. **Stop and purge** wipes this session's buffer and log at once, for when someone objects mid-call. The audit log gets the gate answers.

### Tone and emotion analysis (decision 4)

- **Speech metrics** for every call, computed after the call from timestamps and levels: pace, pauses, interruptions, talk-time share. These are not emotion recognition.
- **Tone and emotion inference** runs after the call, from RAM. It is a local opt-in setting of the owner and off in the kit by default. The kit's README carries the warning that the EU AI Act forbids it at work (Art. 5(1)(f)).
- **Gate and log:** the gate shows the analysis line, and the log marks that the analysis ran.
- **Model:** chosen by a desk check (catalog area to open: emotion from speech).

### Engines and how they are chosen

The live default and the precise default are both picked by measurement, not by preference:

1. **Accuracy test (owner's step 5).** Compare `large-v3-turbo` (whisper.cpp), Parakeet TDT v3 and Nemotron 3.5 ASR Streaming on 3–5 recordings of the owner's Russian speech with English terms. Measure word and character error, the accuracy of the English terms, and speed. Apple's on-device recogniser joins for the English "them" track only, since it has no Russian.
2. **Latency test (phase 2).** The live candidates run inside Kit Voice: time to first text, and time to committed text.
3. **Defaults.** The result table goes into the catalog as trial records, and the defaults are set per track, language and live or precise.

Until then the default is whisper.cpp `large-v3-turbo`, the one engine `in use`.

Coverage of the owner's languages by the candidate engines, from the catalog's desk checks and trials (2026-11-21). "Whisper" is the language list of the Whisper models, not tested here.

| Language | Whisper turbo | Nemotron 3.5 streaming | Parakeet v3 | Apple Translation | System voice |
|---|---|---|---|---|---|
| Russian | yes | yes | yes | yes | Milena |
| English | yes | yes | yes | yes | Samantha, Daniel |
| French | yes | yes | yes | yes | Thomas, Jacques |
| Ukrainian | yes | yes | yes | yes | Lesya |
| Kazakh | yes | **no** | **no** | **no** | Aru |
| Flemish / Dutch | yes | nl-NL | nl | nl, nl-BE | Ellen (nl-BE), Xander |
| Spanish | yes | yes | yes | yes | Mónica |
| German | yes | yes | yes | yes | Anna |

So a Kazakh session uses Whisper for recognition and the local `gemma4:12b` for translation; every other language can use the faster engines. The primary candidate for the live recogniser is NeMo-Speech.cpp's C streaming SDK with Nemotron 3.5, linked into Kit Voice; FluidAudio (Neural Engine) is the challenger, and its VAD, diarization and echo cancellation are candidates for the same app.

## Device matrix

| Device | Capture | Live | After the call | Phase |
|---|---|---|---|---|
| Work Mac (M4 Pro, 24 GB, Xcode) | Tap on Teams, Zoom, Webex + DECT headset | Kit Voice | Kit Voice + work wiki | checks for phases 0–5 |
| Home Mac (M4, 16 GB, Xcode) | Tap on Zoom, Teams (free) + Bluetooth headphones | Kit Voice | Kit Voice + home wiki | development, 0–5 |
| iPhone + Apple Watch | Voice Memos saved to a synced folder | none | Kit Voice on a Mac reads the folder | 6 |
| Windows VDI | Captured on the Mac endpoint (Teams media optimisation); platform captions where allowed | on the Mac | on the Mac | 6 |
| Windows PC | Process loopback (WASAPI) + sherpa-onnx on CPU | later | later | after 6 |
| Android | Pixel Recorder export | none | on a Mac | low priority |

## Phases and done criteria

Each phase ends with a "Work Mac check" section added below, committed and pushed before the owner runs it.

| Phase | Builds | Done when |
|---|---|---|
| 0 | Claude Code `/voice` dictation + a Stop hook that speaks the answer (kit script, toggle off by default) | On both Macs: a prompt dictated in Russian is understood; the answer's first paragraph is spoken in the right language's voice within about 1 s of the answer ending; code blocks are not read; the toggle works; no tokens added. |
| 1 | Kit Voice: gate, two-track capture to RAM, stop, precise pass from RAM, Markdown with Me/Them; save only with recording consent | A 10-minute test call gives Me/Them right on at least 95 % of segments with a headset; no audio file appears on disk (checked); permissions are asked once and survive a rebuild; the gate blocks capture until it passes; stop-and-purge leaves nothing. |
| 2 | Live recognition per track, the window, the session log | On the work Mac: median time to first text at most 1.5 s; committed words never change; a 60-minute session runs without drift or memory growth beyond the buffer; the call stays smooth; the window does not show in a screen share. |
| 3 | Live translation, earpiece speech with the mode switch, back-translation on a key | Translation shows at most 1 s after a committed sentence; earpiece lag at most 4 s; Kit Voice's own speech absent from the "them" track (checked on a recording); the switch works mid-call. |
| 4 | Answers on a key (wiki + local model), Claude on its own key | Local answer on screen within 5 s; Claude used only on its key, with its cost line in the log; the excerpt sent stays within the set limit. |
| 5 | After the call: speaker separation, naming, speech metrics, opt-in tone analysis, Markdown into the wiki | Speaker turns right on a test call (error measured and recorded); names right on at least 90 % of turns when a platform transcript exists; the source passes the wiki's raw checks. |
| 6 | iPhone/Watch voice memos through a watched folder; the VDI from the endpoint; in-person meetings (one microphone, separation after the event) | One real case of each, recorded de-identified. |

The engine measurements (owner's step 5) run alongside phase 1, so that phase 2 starts with a chosen live engine.

## Calls made by the designer (not by the owner; check while reading)

- One local config, `~/.config/wiki-kit/voice.json`, next to the kit's other private lists: the employer-approval date, tone analysis on or off, default languages, the glossary, the earpiece device, log retention, the recordings folder. Never committed.
- Defaults: "me" Russian, "them" English, the owner's language Russian; text log kept 30 days; precise pass with whisper.cpp `large-v3-turbo` until the measurements pick another engine.
- Phase 0's Stop hook goes into the user-level Claude Code settings on each Mac, off until toggled on. It speaks with the system `say` voices, chosen by the script of the text (Cyrillic with Ukrainian letters: the Ukrainian voice, other Cyrillic: Russian, Latin: English) and skips code blocks.
- The app's identity stays stable through a self-signed code-signing certificate or the Xcode personal team, so that macOS keeps its permissions across rebuilds.
- If a platform shows the window in a screen share despite the exclusion, a hide hotkey is the fallback, and the case is recorded in a work Mac check.
- The accuracy test runs on the home Mac with recordings the owner makes for it (below); no work recording leaves the work Mac.

## Left to the builder

- Package layout inside `voice/`, the build script and the signing method. The constraints: a stable identity, and a Command Line Tools build where possible.
- How the app and the scripts talk: subprocess calls, a local socket, or files.
- The overlay's exact look, fonts and colours, inside the window rules above.
- Voice detection thresholds, the commit rule details, ring-buffer sizing and the length cap.
- Hotkeys: global, needing no Accessibility permission where possible.
- How the earpiece device is picked when the call app uses a different output from the system default.
- Echo handling when the owner uses speakers instead of a headset. With a headset, nothing is needed.

## Work Mac checks

None yet. The first one is added when phase 0 and the capture prototype are committed.
