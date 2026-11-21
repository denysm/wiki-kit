---
title: "FFmpeg/FFmpeg"
category: reference
kind: cli
areas: [converting-documents-and-recordings]
repo: FFmpeg/FFmpeg
url: https://ffmpeg.org
version: "9.1"
licence: "LGPL-2.1-or-later, optional parts GPL-2.0-or-later"
desk_checked: 2026-11-21
sources:
  - raw/repos/ffmpeg-ffmpeg-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-ffmpeg-audio-and-scene-frames-for-transcripts.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, kind-cli, ffmpeg, audio, video, frames]
confidence: high
volatility: hot
summary: "Command-line toolbox and libraries for audio and video. ffmpeg with the select and showinfo filters is in use in the kit's meeting script to extract 16 kHz audio and scene-change frames; ffprobe and ffplay are read or listed. Read at n9.1 from the GitHub mirror: the old -vsync option is gone and -fps_mode replaces it; LGPL by default, GPL only with --enable-gpl."
verified: 2026-11-21
---

# FFmpeg/FFmpeg

> A multimedia toolbox (kind `cli`, licence LGPL-2.1-or-later with optional GPL parts, release `9.1` read as tag `n9.1` in the GitHub mirror): `ffmpeg`, `ffprobe` and `ffplay` plus libraries. Here `ffmpeg` makes audio for a local transcriber and saves a frame each time a shared screen changes; the version in use is not stated.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a video recording into 16 kHz mono audio for a speech-to-text program | `ffmpeg` | converting-documents-and-recordings |
| Save a picture each time the screen in a recording changes, with the time of each | `select` | converting-documents-and-recordings |
| Read the times of the frames a filter passed | `showinfo` | converting-documents-and-recordings |
| Check the format, streams and length of a recording before converting it | `ffprobe` | converting-documents-and-recordings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone --depth 1 https://github.com/FFmpeg/FFmpeg $EXTERNAL/FFmpeg`, then `git fetch --depth 1 origin tag n9.1` and `git checkout -q n9.1`. Never build or edit it. Read first: `doc/ffmpeg.texi`, `doc/ffprobe.texi`, then "select, aselect" and "showinfo" in `doc/filters.texi`. The mirror has no GitHub releases, so the release is the highest `n<major>.<minor>` tag; the repo's first tag listing shows old `v0.x` tags.
- **In use**: `ffmpeg` called by the kit's `scripts/meeting2md.py` twice: `-vn -ac 1 -ar 16000 -c:a pcm_s16le` for audio, and a `-vf` chain of `select` on `scene` above `0.25`, `showinfo` and `scale=1280:-1`, with `-fps_mode vfr`, for frames, with times read from `pts_time`. The guide says "ffmpeg 8 removed `-vsync`". Read at `n9.1`: `fftools/ffmpeg_opt.c` defines `fps_mode` and no `vsync` option. The installed `ffmpeg` is `9.0.2` (checked 2026-11-21 with `--version`), one patch release behind the `9.1` read: re-check before relying on a filter or option changed since.
- **Sends outward**: nothing for local files; network protocols open only for a URL, and `--disable-network` exists at build time. No `telemetry` or `analytics` text found in the main source folders. Read, not observed.
- **Switch off**: nothing; pass local paths only.
- **Do not install**: a build from the clone, `--enable-gpl` or `--enable-nonfree` builds (they change the licence of the result), Docker images; installation waits for the user's yes.

## What's inside

Parts are the programs and the filters in use. Defined in `fftools/` and `doc/filters.texi`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `ffmpeg` | "a command line toolbox to manipulate, convert and stream multimedia content"; used with `-vn`, `-ac`, `-ar`, `-vf` and `-fps_mode vfr`. | in use | A binary; local files | Re-check when the in-use `9.0.2` moves to `9.1` or later, and when a release changes `-fps_mode` or the `-v info` log. |
| `select` | Filter that passes frames for which an expression is true; the variable `scene` is "value between 0 and 1 to indicate a new scene". | in use | Inside an `ffmpeg` call | Re-check when the frame count for a recording changes with a new release. |
| `showinfo` | Filter that prints a line per frame, with `pts_time:`; the video is not modified. | in use | Inside an `ffmpeg` call; the log on standard error | Re-check when the log line format changes. |
| `ffprobe` | Prints format and stream information, human- and machine-readable; `-show_format`, `-show_streams`. | candidate | A binary | Try it to read a recording's streams and length before converting. |
| `ffplay` | "a minimalistic multimedia player". | listed | A binary and a display | Read when a recording must be played to check a frame. |
| `tools/` programs (`aviocat`, `ismindex`, `qt-faststart`, `ffhash` and others) | Small utilities. | listed | A build | Read when a task needs one of them by name. |
| Libraries `libavcodec`, `libavformat`, `libavfilter`, `libavutil`, `libavdevice`, `libswresample`, `libswscale` | The code behind the programs. | listed | A C toolchain | Read when a program must call FFmpeg directly. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| not stated | Extract audio from a video for a transcriber | `ffmpeg` | In use: 16 kHz mono PCM audio for the transcriber. | None beyond local time | [use record](../../raw/notes/trials/2026-11-21-ffmpeg-audio-and-scene-frames-for-transcripts.md) |
| not stated | Save a frame at each screen change | `select` | In use: 53 frames for a 58-minute call with screen sharing; threshold `0.25`. | The frame pass reads the whole video once more | [use record](../../raw/notes/trials/2026-11-21-ffmpeg-audio-and-scene-frames-for-transcripts.md) |
| not stated | Read frame times from the filter log | `showinfo` | In use: times taken from `pts_time`. | None | [use record](../../raw/notes/trials/2026-11-21-ffmpeg-audio-and-scene-frames-for-transcripts.md) |

## Verdict

FFmpeg is the kit's media tool: one program, two calls, no network. Three parts are in use; `ffprobe` is read and the rest listed. The licence is LGPL unless a build adds `--enable-gpl`, which the kit does not need. Version in use is `9.0.2`, behind the `9.1` read. Revisit when the in-use version moves to `9.1`, when a release changes `-fps_mode` or `showinfo` output, or when a recording needs more than the two calls.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; recordings to transcripts and frames
- [[ggml-org-whisper-cpp|ggml-org/whisper.cpp]] (../references/ggml-org-whisper-cpp.md): reads the audio it makes

## Sources

- [Desk check: FFmpeg/FFmpeg n9.1](../../raw/repos/ffmpeg-ffmpeg-desk-check-2026-11-21.md): programs, filters, licence and the `-fps_mode` check read from the clone; freshness through the GitHub API.
- [Use record: audio extraction and scene-change frames](../../raw/notes/trials/2026-11-21-ffmpeg-audio-and-scene-frames-for-transcripts.md): how the kit's script calls it.
