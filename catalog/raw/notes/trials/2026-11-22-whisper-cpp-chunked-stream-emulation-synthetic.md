---
title: "Trial: whisper.cpp whisper-cli on pause-cut pieces, emulating whisper-stream, synthetic Russian speech"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-22
ingested: 2026-11-22
repo: ggml-org/whisper.cpp
part: whisper-cli
version: "1.9.5"
status: tried
tags: [catalog, trial, kind-cli, speech-to-text, whisper-cpp, streaming, vad, smoke-test]
summary: "Sandbox smoke test, 2026-11-22, Apple M4 Mac mini 16 GB: the kit bench's whisper-chunks engine (whisper-cli 1.9.5, large-v3-turbo, greedy, no text context, pieces of 1 to 10 s cut in the middle of pauses, emulating whisper-stream's VAD mode) on 51.4 s of synthetic Russian speech: 6 pieces covering the whole file, WER 26.5 % against 20.7 % for the whole file at once. Pipeline check only; the owner's real recordings decide."
---

# Trial: whisper-cli on pause-cut pieces (whisper-stream emulation)

- **Task, by kind**: estimating what live recognition with whisper would cost in accuracy, before investing in a streaming recogniser (Nemotron 3.5 through NeMo-Speech.cpp) for live captions of Russian speech with English terms.
- **Kind of record**: sandbox trial with `scripts/asr_bench.py` of the owner's private voice repository (in the kit until 2026-11-23), engine `whisper-chunks`. Nothing installed beyond the Homebrew `whisper.cpp` package already in use.
- **Machine**: Apple M4 Mac mini, 16 GB.
- **Input**: a bench text of the owner's private voice repository (in the kit until 2026-11-23, as `voice/bench/read-1.txt`) spoken by the macOS voice Milena, 51.4 s, 16 kHz mono, as in the [earlier smoke test](2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md). The file was deleted after the run.

## Setup

- `whisper-cli` 1.9.5, model `large-v3-turbo`. For each piece: `-mc 0` (no text context) and `-bs 1 -bo 1` (greedy decoding), because `whisper-stream` decodes greedily by default; plain `whisper-cli` searches five beams.
- Cutting: an energy VAD over 30 ms frames. Cuts go in the middle of every pause of at least 1 s; pieces under 1 s are merged and pieces over 10 s (`whisper-stream`'s default `--length`) are split at their quietest frame. The pieces cover the whole file.

## Result

| Engine | Pieces | WER % | CER % | Latin-script terms % | Numbers % | Real-time factor | Peak memory MB |
|---|---|---|---|---|---|---|---|
| whisper-cli, whole file (beam 5) | 1 | 20.7 | 12.4 | 51.4 | 100.0 | 0.085 | 1910 |
| whisper-cli, pause-cut pieces (greedy) | 6 | 26.5 | 21.9 | 31.4 | 100.0 | 0.191 | 1856 |

- Cutting into pieces cost about 6 points of WER and 20 points of English terms kept in Latin script on this input.
- The real-time factor includes loading the model once per piece, so it is not the live latency.
- The emulation is an optimistic bound for `whisper-stream`. The real tool also loses the start of turns longer than its window and caps each piece at 32 tokens (`-mt`).
- Synthetic speech has no real pauses, so most cuts were forced at 10 s. The owner's recordings decide.
