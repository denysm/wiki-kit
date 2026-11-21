# Speech recognition bench: Russian speech with English terms

A small, repeatable accuracy test for choosing a speech recognition engine on *your* voice, before a live engine is picked (see `docs/voice-design.md`, "Engines and how they are chosen"). Three read texts give an exact reference; two free talks show how the engines cope with real speech.

## Record (about 15 minutes)

1. iPhone Voice Memos, with Settings → Apps → Voice Memos → Audio Quality set to **Lossless** if your iPhone offers it. A quiet room, the phone 20–30 cm away, your normal pace. Do not restart after a slip: carry on, as in a call.
2. Read `read-1.txt`, `read-2.txt`, `read-3.txt`, one recording each, named `read-1`, `read-2`, `read-3`.
3. Two free talks of 2–3 minutes each, named `free-1` and `free-2`, with English terms as they come naturally. Nothing confidential: no employer, customer or colleague names.
   - `free-1`: how you organise your notes, wiki or AI tools — what works, what annoys you, what you want next.
   - `free-2`: explain a technology you know well to a colleague (for example how `git rebase` or Docker works), with your own examples.
4. Send the five files to the Mac (AirDrop lands them in Downloads) and move them to `~/VoiceBench/` — outside the kit and outside any wiki.

## References

- Read texts: the `.txt` file is the reference.
- Free talks: the most accurate engine writes a draft, you correct it into `~/VoiceBench/free-N.ref.txt`. The draft and the reference stay next to the recording, never in the kit.

## What is measured

Word and character error rate after normalisation (lower case, no punctuation, `ё` → `е`); the share of English terms written correctly in Latin script; numbers; speed (real-time factor) and peak memory. Results go into the catalog as trial records, told by kind, without the recordings or their text.
