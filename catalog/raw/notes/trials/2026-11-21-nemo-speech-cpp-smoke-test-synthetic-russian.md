---
title: "Trial: NeMo-Speech.cpp, Nemotron 3.5, Parakeet v3, whisper.cpp — smoke test on synthetic Russian speech"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: NVIDIA/NeMo-Speech.cpp
part: "transcribe (nemotron q8_0, parakeet q8_0), whisper-cli, parakeet-cli"
version: "0.3.0"
status: tried
tags: [catalog, trial, kind-cli, speech-to-text, nemo-speech-cpp, whisper-cpp, parakeet, nemotron, smoke-test]
summary: "Sandbox smoke test, 2026-11-21, Apple M4 Mac mini 16 GB, macOS 27.2.1: the NeMo-Speech.cpp 0.3.0 macOS Metal archive (checksum matched) ran Nemotron 3.5 q8_0 (offline and --stream) and Parakeet v3 q8_0 on 51.4 s of synthetic Russian speech with English terms, faster than real time; whisper-cli 1.9.5 large-v3-turbo ran too; whisper.cpp parakeet-cli 1.9.5 from Homebrew aborted. Pipeline check only: synthetic speech says nothing about accuracy on a real voice."
---

# Trial: speech engines, smoke test on synthetic Russian speech

- **Task, by kind**: checking that local speech engines run end to end before an accuracy test on real recordings of the owner's voice (Russian with English terms).
- **Kind of record**: sandbox trial. Nothing installed on `PATH` except the Homebrew `whisper.cpp` package, which carries the `in use` `whisper-cli`.
- **Machine**: Apple M4 Mac mini, 16 GB, macOS 27.2.1.

## Setup

- NeMo-Speech.cpp: the release archive `nemo-speech-0.3.0-macos-aarch64-metal.tar.gz`, SHA-256 `2b972ed8b5dba07492212acf8cb75cbf34ecb141198ffa1997febe84b7c4d9ed`, equal to the published `.sha256`; unpacked into a throwaway folder, not on `PATH`; `nemo-speech --version` printed "nemo-speech 0.3.0".
- Models downloaded once from Hugging Face at the revisions of their desk checks: `nemotron-3.5-asr-streaming-0.6b.q8_0.gguf` (742090464 bytes) and `parakeet-tdt-0.6b-v3.q8_0.gguf` (713975456 bytes), sizes equal to the API listing; `ggml-parakeet-tdt-0.6b-v3-f16.bin` from `ggml-org/parakeet-GGUF` (1255897319 bytes).
- Input: the kit's bench text `voice/bench/read-1.txt` (121 words after normalisation) spoken by the macOS voice Milena into a file, 51.4 s, converted to 16 kHz mono WAV. Runner: the kit's `scripts/asr_bench.py`.

## Result

| Engine | WER % | Latin-script terms found % | Numbers found % | Real-time factor | Peak memory MB |
|---|---|---|---|---|---|
| whisper-cli 1.9.5, `large-v3-turbo` | 20.7 | 51.4 | 100.0 | 0.098 | 1899 |
| nemo-speech, Parakeet v3 q8_0 | 35.5 | 20.0 | 100.0 | 0.345 | 268 |
| nemo-speech, Nemotron 3.5 q8_0, whole file | 45.5 | 0.0 | 25.0 | 0.071 | 498 |
| nemo-speech, Nemotron 3.5 q8_0, `--stream` | 45.5 | 0.0 | 25.0 | 0.119 | 410 |

- All three NeMo-Speech.cpp runs and whisper-cli finished faster than real time on the M4.
- Nemotron and Parakeet wrote the English terms in Cyrillic transliteration ("стейджинг", "роллбэк") and Nemotron wrote some numbers as words; whisper kept many terms in Latin script ("Payment Service", "rollback", "Argo CD", "PostgreSQL", "pull request").
- whisper.cpp `parakeet-cli` 1.9.5 (Homebrew, with Homebrew `ggml` 1.0.0) aborted (exit 134) in `ggml_view_3d` while building the encoder graph, on the 51.4 s file and on a 10 s cut, with the `ggml-org/parakeet-GGUF` f16 model.
- The first runner pass read whisper-cli's stdout with `-np -nt` and kept only two segments; reading its `-otxt` file fixed that (the numbers above are from the fixed run).

## What this does not show

Synthetic speech from one system voice: it says nothing about accuracy on the owner's real voice. The accuracy test on the owner's recordings follows.

## Cost

No tokens, no money; about 2.6 GB of downloads.
