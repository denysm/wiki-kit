---
title: "Use record: FFmpeg audio extraction and scene-change frames for transcripts"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: FFmpeg/FFmpeg
part: ffmpeg
version: "9.0.2"
status: in use
tags: [catalog, trial, use-record, kind-cli, ffmpeg, audio, frames]
summary: "ffmpeg is in real use in the kit's script meeting2md.py: it extracts 16 kHz mono audio for a local transcriber and, on request, saves a frame each time the picture changes, with the select and showinfo filters and -fps_mode vfr; 53 frames for a 58-minute call with screen sharing. Installed version 9.0.2, checked 2026-11-21 with `--version`."
---

# Use record: FFmpeg audio extraction and scene-change frames for transcripts

Source of this record: the kit's script `scripts/meeting2md.py` and its guide `docs/meeting-recordings-to-markdown.md`, read on 2026-11-21. Only what they state is written here.

- **Tool and parts**: FFmpeg, part `ffmpeg`, with the filters `select` and `showinfo`.
- **Task, by kind**: (1) turn a video recording into audio a speech-to-text program reads; (2) save a picture each time a shared screen changes, with the time of each.
- **Audio call**: `ffmpeg -v error -y -i <recording> -vn -ac 1 -ar 16000 -c:a pcm_s16le <wav>`: no video, one channel, 16 kHz, 16-bit PCM, into a temporary folder.
- **Frame call**: `ffmpeg -v info -i <recording> -vf "select='gt(scene,<threshold>)',showinfo,scale=1280:-1" -fps_mode vfr -q:v 4 <folder>/f_%03d.jpg`; the threshold defaults to `0.25` (`--scene`; "lower gives more frames"). The script reads the frame times from `pts_time` in the `showinfo` lines on standard error and names each file `f_NNN_MMmSSs.jpg`, plus `timestamps.tsv`.
- **Version**: 9.0.2, the installed `ffmpeg` (version checked 2026-11-21 with `--version`); the guide says "ffmpeg 8 removed `-vsync`; the script uses `-fps_mode vfr`". How it was installed: the guide says `brew install ffmpeg whisper-cpp` on macOS. The desk check read `n9.1` and found `-fps_mode` documented and no `vsync` option in `fftools/ffmpeg_opt.c`.
- **Result**: "53 frames for a 58-minute call with screen sharing, enough for an agent to describe what was shown"; "The frame pass reads the whole video once more."
- **Date of first use**: not stated.

## Cost

No money and no tokens: it runs on the local machine.
