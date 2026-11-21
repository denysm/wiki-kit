---
title: "Desk check: ggml-org/whisper.cpp v1.9.5"
source: https://github.com/ggml-org/whisper.cpp/tree/v1.9.5
type: repos
authors: ["The ggml authors"]
source_date: 2026-10-06
ingested: 2026-11-21
repo: ggml-org/whisper.cpp
kind: cli
version: "1.9.5"
licence: MIT
tags: [catalog, desk-check, kind-cli, whisper-cpp, speech-to-text, transcription, local]
summary: "The command-line tools, model sizes and outbound calls of whisper.cpp v1.9.5 read from a read-only clone: whisper-cli, whisper-server, whisper-stream, whisper-quantize, whisper-bench, VAD tools and the example programs; models are downloaded from a model hub by a script; the tools themselves make no network call. Freshness from the GitHub API; how the kit's meeting-recording script calls it."
---

# Desk check: ggml-org/whisper.cpp v1.9.5

Read from a shallow clone of tag `v1.9.5` (commit `d1be6fde11ac6e0407606b4e42fe72d34add8037`, committed 2026-10-06) at `$EXTERNAL/whisper.cpp`. The clone was not modified; nothing was built, installed or run. Checked 2026-11-21. Version read by this desk check: 1.9.5.

## Repository facts

- A C/C++ port of OpenAI's Whisper speech-to-text model on the `ggml` tensor library. `README.md` is 1018 lines; each example folder under `examples/` has its own short README.
- `LICENSE`: "MIT License", "Copyright (c) 2023-2026 The ggml authors".
- Top-level folders: `src/` and `include/` (the library, `whisper.h`), `ggml/` (the tensor library), `examples/` (the programs below), `models/` (download and conversion scripts), `bindings/` (`go`, `java`, `javascript`, `ruby`), `tests/`, `samples/`, `grammars/`, `scripts/`, `ci/`, `cmake/`.
- The command-line programs are built with CMake (`examples/*/CMakeLists.txt` name the targets). The clone holds no prebuilt binary. How to get a binary is not part of this check: nothing was installed.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/ggml-org/whisper.cpp`: `pushed_at` 2026-11-20T15:48:52Z; licence `MIT`; default branch `master`; not archived.
- `gh api repos/ggml-org/whisper.cpp/releases/latest`: tag `v1.9.5`, published 2026-10-06T17:39:17Z.
- So the clone is at the latest release; commits were pushed to `master` after it.

## How to run here

- **Clone**: `git clone --depth 1 --branch v1.9.5 https://github.com/ggml-org/whisper.cpp $EXTERNAL/whisper.cpp`. Read only; never build or edit it. Read first: `README.md` ("Quick start", "Memory usage", "Quantization", "Voice Activity Detection (VAD)"), then `examples/cli/README.md` and `models/README.md`.
- **Outbound calls**: `models/download-ggml-model.sh` fetches models from the Hugging Face repository `ggerganov/whisper.cpp` (the tinydiarize model from `akashmjn/tinydiarize-whisper.cpp`); `models/download-vad-model.sh` fetches the VAD model from `ggml-org/whisper-vad`; the `parakeet-cli` README downloads its model with `hf download`. A search of `src/`, `include/` and `examples/cli/cli.cpp` for `http` found only reference links in comments, so the library and `whisper-cli` make no network call. Read in the source, not observed on the wire. No telemetry code was looked for beyond that search.
- **Switch off**: nothing to switch off in the tools. To keep data local, download a model file once by hand and pass it with `-m`.
- **Install steps to avoid**: the Docker images, Conan, the `WHISPER_COMMON_FFMPEG`, `WHISPER_SDL2`, Core ML, OpenVINO, CUDA, Vulkan and other build options in the README; a build or an install waits for the user's yes. The kit's guide uses a Homebrew package instead of this clone (see the use record).
- **What `whisper-cli` reads**: its help text says "supported audio formats: flac, mp3, ogg, wav". A video file has to be converted to audio first.

## Parts

Parts are the command-line programs (targets of `examples/*/CMakeLists.txt`) and the model sizes.

### `whisper-cli` (`examples/cli/cli.cpp`)

- The main program: transcribes or translates audio files. Options read in `examples/cli/README.md`: `-m` model path, `-f` input file, `-l` language ("[en     ]" default, `auto` to detect), `-t` threads (default 4), `--prompt` initial prompt, `-oj` JSON output, `-ojf` fuller JSON, `-of` output file path without extension, `-otxt`, `-osrt`, `-ovtt`, `-ocsv`, `-olrc`, `-ml` maximum segment length, `-tdrz` tinydiarize speaker turns (needs a `tdrz` model), `-di` stereo diarization, `-ng` no GPU, `-fa` flash attention, `--vad` with `-vm` a VAD model.
- Needs: a built binary and a model file. Anything notable: the output JSON has the segments with timestamps; the speaker labels come from `-tdrz` or `-di` only.

### `whisper-server` (`examples/server/server.cpp`)

- A simple HTTP server: "WAV Files are passed to the inference model via http requests." Options as `whisper-cli`, plus `--host`, `--port` (help text default 8080), `--inference-path` (default `/inference`), `--convert` ("requires ffmpeg on the server").
- Needs: a built binary and a model. It binds the loopback address by default (the help text lists it as the default host); not tried.

### `whisper-stream` (`examples/stream/stream.cpp`)

- "A naive example of performing real-time inference on audio from your microphone": samples audio every half a second and transcribes continuously. Needs SDL2 (`-DWHISPER_SDL2=ON`, README "Real-time audio input example") and a microphone.

### `whisper-quantize` (`examples/quantize/quantize.cpp`)

- "Tool for integer quantization of Whisper `ggml` model files"; README example `quantize models/ggml-base.en.bin models/ggml-base.en-q5_0.bin q5_0`. Needs a built binary and a model file.

### `whisper-bench` (`examples/bench/bench.cpp`)

- "A very basic tool for benchmarking the inference performance on your device": runs the encoder on random audio and records the time. Needs a built binary and a model file.

### `whisper-vad-speech-segments` (`examples/vad-speech-segments/speech.cpp`) and VAD in `whisper-cli`

- Splits an audio file into speech segments with a VAD (voice activity detection) model; the README ("Voice Activity Detection (VAD)") says `whisper-cli --vad` passes only detected speech segments to Whisper, which "can significantly speed up the transcription process". Supported VAD model: Silero-VAD, downloaded with `models/download-vad-model.sh silero-v6.2.0`.

### `parakeet-cli` and `parakeet-quantize` (`examples/parakeet-cli/`, `examples/parakeet-quantize/`)

- A second speech model, Parakeet, in the same repository; the `parakeet-cli` README gives a converted-model download. Only the README header and the CMake target names were read.

### Other example programs (read by name and README header only)

- `whisper-command` (voice commands from a microphone), `whisper-talk-llama` (talk with a LLaMA model in the terminal), `whisper-lsp` (a language server), `examples/addon.node`, the `*.wasm` browser examples, `whisper.android`, `whisper.objc`, `whisper.swiftui`, `whisper.nvim`, `wchess`, `ffmpeg-transcode.cpp`, and the scripts `generate-karaoke.sh`, `livestream.sh`, `twitch.sh`, `yt-wsp.sh`. Not read beyond the header.
- `bindings/` holds `go`, `java`, `javascript` and `ruby` folders; not read.

### Models (`models/README.md`, "Available models" and README "Memory usage")

- The model table lists disk sizes: tiny 75 MiB, base 142 MiB, small 466 MiB, medium 1.5 GiB, large-v3 2.9 GiB, large-v3-turbo 1.5 GiB, large-v3-turbo-q5_0 547 MiB. Models without `.en` are multilingual. "Memory usage" lists: tiny ~273 MB, base ~388 MB, small ~852 MB, medium ~2.1 GB, large ~3.9 GB (the large-v3-turbo row has no memory figure there).
- `models/download-ggml-model.sh` also lists `large-v3-turbo-q8_0`. Quantized files end in `-q5_0` or `-q8_0`.

## How the kit uses it

The kit's script `scripts/meeting2md.py` calls `whisper-cli` to transcribe meeting recordings; the use record is `raw/notes/trials/2026-11-21-whisper-cpp-local-meeting-transcription.md`. Status after it: `whisper-cli` and the `large-v3-turbo` model file are `in use`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 46 model calls on sonnet, $2.03 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
