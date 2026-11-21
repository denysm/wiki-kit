---
title: "Use record: whisper.cpp whisper-cli, local transcription of meeting recordings"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: ggml-org/whisper.cpp
part: whisper-cli
version: "1.9.5"
status: in use
tags: [catalog, trial, use-record, kind-cli, whisper-cpp, transcription]
summary: "whisper-cli with the large-v3-turbo model is in real use in the kit's script meeting2md.py to transcribe recorded calls locally: 58 minutes of audio took about 2.5 minutes on an Apple M4 Pro. Installed version 1.9.5, checked 2026-11-21 with `--version`."
---

# Use record: whisper.cpp whisper-cli, local transcription of meeting recordings

Source of this record: the kit's script `scripts/meeting2md.py` and its guide `docs/meeting-recordings-to-markdown.md`, read on 2026-11-21. Only what they state is written here.

- **Tool and parts**: ggml-org/whisper.cpp, part `whisper-cli`, with the model file `ggml-large-v3-turbo.bin` (part `large-v3-turbo`).
- **Task, by kind**: transcribe a recorded call locally, without sending audio anywhere, with names and numbers right when the speech is Russian with English technical terms.
- **How it is called**: the script runs `ffmpeg` to make 16 kHz mono audio in a temporary folder, then `whisper-cli -m <model> -f <wav> -l <lang> -t 10 -oj -of <temp path>`, adding `--prompt "<names, terms>"` when given, and reads the JSON segments. The language defaults to `ru`; the model path defaults to `~/.cache/whisper-cpp/ggml-large-v3-turbo.bin`. The script's docstring says whisper-cli runs "(Metal)".
- **Model**: `ggml-large-v3-turbo.bin`, "about 1.6 GB", downloaded once with `curl` from the Hugging Face repository `ggerganov/whisper.cpp`.
- **How it was obtained**: the guide says macOS: `brew install ffmpeg whisper-cpp`; elsewhere "a whisper.cpp build that provides `whisper-cli`". The clone was not built or used.
- **Version**: 1.9.5, the installed `whisper-cli` (version checked 2026-11-21 with `--version`); the Homebrew package of it. The desk check read `v1.9.5`, the same tag.
- **Result**: "58 minutes of audio took about 2.5 minutes on an Apple M4 Pro (Metal)". The guide says the Whisper text gets wording, names and numbers right "far more often" than the meeting platform's own transcript for such speech; speaker labels come from the platform transcript, not from Whisper, and can be off by one segment at a turn boundary.
- **Date of first use**: not stated.

## Cost

No money: the script runs on the local machine and "No model tokens are spent". The model file is about 1.6 GB on disk.
