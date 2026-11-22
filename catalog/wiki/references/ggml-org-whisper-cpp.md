---
title: "ggml-org/whisper.cpp"
category: reference
kind: cli
areas: [converting-documents-and-recordings]
repo: ggml-org/whisper.cpp
version: "1.9.5"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/notes/trials/2026-11-22-whisper-cpp-chunked-stream-emulation-synthetic.md
  - raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md
  - raw/repos/ggml-org-whisper-cpp-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-whisper-cpp-local-meeting-transcription.md
created: 2026-11-21
updated: 2026-11-22
tags: [catalog, card, area-converting-documents-and-recordings, kind-cli, whisper-cpp, speech-to-text, transcription, local]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "C/C++ port of the Whisper speech-to-text model with command-line tools. whisper-cli with the large-v3-turbo model is in use in the kit's meeting-recording script for local transcription; the server, stream, quantize, bench and VAD tools are read, the example programs listed. The tools make no network call; models are downloaded from a model hub by a script."
---

# ggml-org/whisper.cpp

> A local speech-to-text program (kind `cli`, licence MIT, version `1.9.5` read in a clone): `whisper-cli` and a few other tools run OpenAI's Whisper models on one machine. Here `whisper-cli` with the `large-v3-turbo` model transcribes recorded calls for the kit's meeting script; the version in use is `1.9.5`.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a recorded call into a timestamped transcript on this machine, with no audio leaving it | `whisper-cli` | converting-documents-and-recordings |
| Get names and terms right in a transcript by giving the model a list of them | `whisper-cli` | converting-documents-and-recordings |
| Transcribe Russian speech with English technical terms | `large-v3-turbo` | converting-documents-and-recordings |
| Run the same model in less disk space, with a quantized file | `large-v3-turbo-q5_0` | converting-documents-and-recordings |
| Skip silence to speed up a long transcription | `whisper-vad-speech-segments` | converting-documents-and-recordings |
| Serve transcription to other programs over HTTP on this machine | `whisper-server` | converting-documents-and-recordings |
| Turn live speech from a microphone into text on this machine as it is spoken | `whisper-stream` | converting-documents-and-recordings |
| Recognise spoken commands from a microphone on this machine | `whisper-command` | converting-documents-and-recordings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone --depth 1 --branch v1.9.5 https://github.com/ggml-org/whisper.cpp $EXTERNAL/whisper.cpp`. Never build or edit it. Read first: `README.md` ("Quick start", "Memory usage", "Voice Activity Detection (VAD)"), then `examples/cli/README.md` and `models/README.md`.
- **In use**: `whisper-cli` with `ggml-large-v3-turbo.bin`, called by the kit's `scripts/meeting2md.py` as `whisper-cli -m <model> -f <wav> -l <lang> -t 10 -oj -of <path>` plus `--prompt` when names are given. The installed `whisper-cli` is `1.9.5` (checked 2026-11-21 with `--version`), the same as the tag read.
- **Sends outward**: nothing from the tools; a search of `src/`, `include/` and `examples/cli/cli.cpp` for `http` found only reference links. The model download scripts fetch from Hugging Face. Read in the source, not observed.
- **Switch off**: nothing to switch off; download a model once and pass it with `-m`.
- **Do not install**: the Docker images, Conan, or the Core ML, OpenVINO, CUDA and other build options; building the clone waits for the user's yes. Input must be flac, mp3, ogg or wav; a video file is converted first.

## What's inside

Parts are the command-line programs and the model sizes. Defined by `examples/*/CMakeLists.txt` and `models/README.md`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `whisper-cli` | The main program: transcribe or translate audio; `-oj` JSON with segments, `-l` language, `--prompt`, `-t` threads, `-tdrz` speaker turns, `--vad`. | in use | A binary and a model file | Re-check when a release newer than `1.9.5` ships or the JSON output changes. |
| `large-v3-turbo` | Multilingual model, 1.5 GiB on disk; the file `ggml-large-v3-turbo.bin` used by the meeting script. | in use | The model file; the memory figure for it is not in the README | Re-check when a newer large model is listed in `models/README.md`. |
| `large-v3-turbo-q5_0` | The same model quantized to 547 MiB. | candidate | The model file | Try it when memory or disk is short, and compare the wording on a recording with names and numbers. |
| `large-v3` | Multilingual large model, 2.9 GiB. | candidate | The model file; about 3.9 GB of memory (the README row is `large`) | Try it when the turbo model misses words. |
| `medium` | Multilingual model, 1.5 GiB. | candidate | The model file; about 2.1 GB of memory | Try it when memory is short, and compare the wording. |
| `small` | Multilingual model, 466 MiB. | candidate | The model file; about 852 MB of memory | Try it when memory is short, and compare the wording. |
| `base` | Multilingual model, 142 MiB. | candidate | The model file; about 388 MB of memory | Try it when disk is very short, and compare the wording. |
| `tiny` | Multilingual model, 75 MiB. | candidate | The model file; about 273 MB of memory | Try it to check a pipeline end to end. |
| `whisper-server` | A simple HTTP server: WAV files are passed to the model in requests; `--convert` needs ffmpeg. | candidate | A binary and a model; binds the loopback address by default | Try it when several programs need transcription without reloading the model each time. |
| `whisper-stream` | Real-time transcription from a microphone, every half a second. | candidate | A binary, a model, SDL2 and a microphone | Try it when live text from a microphone is wanted. |
| `whisper-quantize` | Integer quantization of `ggml` model files. | candidate | A binary and a model file | Try it when a model has no ready quantized file. |
| `whisper-bench` | Times the encoder on random audio for one device. | candidate | A binary and a model file | Try it to compare two machines or two models. |
| `whisper-vad-speech-segments` | Splits audio into speech segments with a VAD model (Silero-VAD). | candidate | A binary, the VAD model download | Try it on a long recording with long silences. |
| `parakeet-cli` | Runs the Parakeet model in the same repository. | rejected | A binary and a converted model | Revisit on a release after `1.9.5`. Rejected: the Homebrew `1.9.5` build aborted on the converted Parakeet v3 model in a trial; NeMo-Speech.cpp runs Parakeet instead. |
| `parakeet-quantize` | Quantizer for Parakeet model files. | listed | A binary and a model file | Read when a Parakeet file must be quantized. |
| `whisper-command` | Voice commands. | listed | A binary, SDL2 | Read when a voice interface is wanted. |
| `whisper-talk-llama`, `whisper-lsp` | A talk-with-a-language-model demo, a language server. | listed | A binary, SDL2 for the first | Read when a voice interface is wanted. |
| `bindings` | `go`, `java`, `javascript` and `ruby` folders. | listed | Their own toolchains | Read when a program in those languages must call it. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| not stated | Transcribe recorded calls locally | `whisper-cli` | In use at `1.9.5`: 58 minutes of audio took about 2.5 minutes on an Apple M4 Pro (Metal), model `large-v3-turbo`. | No tokens; model file about 1.6 GB | [use record](../../raw/notes/trials/2026-11-21-whisper-cpp-local-meeting-transcription.md) |
| not stated | Transcribe Russian speech with English terms | `large-v3-turbo` | In use; wording, names and numbers right "far more often" than the platform transcript. | Same run | [use record](../../raw/notes/trials/2026-11-21-whisper-cpp-local-meeting-transcription.md) |
| 2026-11-21 | Smoke test on synthetic Russian speech, 51.4 s | `whisper-cli` | `large-v3-turbo` on an Apple M4 16 GB: real-time factor 0.098, peak memory 1899 MB; kept English terms in Latin script more often than the NVIDIA models. | No cost | [trial record](../../raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md) |
| 2026-11-22 | Emulate whisper-stream (pause-cut pieces, greedy, no context) on synthetic Russian speech | `whisper-cli` | 6 pieces covering 51.4 s: WER 26.5 % against 20.7 % for the whole file, Latin-script terms 31.4 % against 51.4 %; an optimistic bound for live whisper. | No cost | [trial record](../../raw/notes/trials/2026-11-22-whisper-cpp-chunked-stream-emulation-synthetic.md) |
| 2026-11-21 | Same test | `parakeet-cli` | Aborted (exit 134) in `ggml_view_3d`. | No cost | [trial record](../../raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md) |

## Verdict

whisper.cpp is the kit's speech-to-text: `whisper-cli` with one multilingual model, run locally, so a recording never leaves the machine. Two parts are in use; `parakeet-cli` was run once and rejected (it aborted); the rest are read from the docs, not run. Version in use and version read are both `1.9.5`. Revisit when a newer release ships, when a release changes the JSON output, or when a quantized model is tried on a real recording.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; documents, audio and video to Markdown or transcripts
- [[ffmpeg-ffmpeg|FFmpeg/FFmpeg]] (../references/ffmpeg-ffmpeg.md): makes the 16 kHz audio it reads
- [[nvidia-parakeet-tdt-0-6b-v3|nvidia/parakeet-tdt-0.6b-v3]] (../references/nvidia-parakeet-tdt-0-6b-v3.md): the model `parakeet-cli` runs
- [[snakers4-silero-vad|snakers4/silero-vad]] (../references/snakers4-silero-vad.md): the VAD model behind `--vad`

## Sources

- [Desk check: ggml-org/whisper.cpp v1.9.5](../../raw/repos/ggml-org-whisper-cpp-desk-check-2026-11-21.md): programs, models, options and outbound calls read from the clone; freshness through the GitHub API.
- [Use record: whisper-cli for local meeting transcription](../../raw/notes/trials/2026-11-21-whisper-cpp-local-meeting-transcription.md): how the kit's script calls it and the measured speed.
- [Trial: speech engines, smoke test on synthetic Russian speech](../../raw/notes/trials/2026-11-21-nemo-speech-cpp-smoke-test-synthetic-russian.md): runs on an Apple M4, speeds, a pipeline check only.
- [Trial: whisper-cli on pause-cut pieces, emulating whisper-stream](../../raw/notes/trials/2026-11-22-whisper-cpp-chunked-stream-emulation-synthetic.md): 6 pieces of synthetic Russian speech, WER 26.5 % against 20.7 % whole-file.
