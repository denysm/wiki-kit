---
title: "Desk check: FFmpeg/FFmpeg n9.1"
source: https://github.com/FFmpeg/FFmpeg/tree/n9.1
type: repos
authors: ["FFmpeg developers"]
source_date: 2026-11-19
ingested: 2026-11-21
repo: FFmpeg/FFmpeg
url: https://ffmpeg.org
kind: cli
version: "9.1"
licence: "LGPL-2.1-or-later, optional parts GPL-2.0-or-later"
tags: [catalog, desk-check, kind-cli, ffmpeg, audio, video, conversion, frames]
summary: "The command-line tools, libraries, licence and filters of FFmpeg release n9.1 read from a read-only clone of the GitHub mirror: ffmpeg, ffprobe, ffplay, the select and showinfo filters the kit uses, the fps_mode option that replaces vsync, and the licence split between LGPL and GPL parts. Freshness from the GitHub API; how the kit's meeting-recording script calls it."
---

# Desk check: FFmpeg/FFmpeg n9.1

Read from a shallow clone of the GitHub mirror at tag `n9.1` (commit `74e4393595cf2b5857f0da925c4e0dd74ea306e5`, committed 2026-11-19, message "doc/APIchanges: add 9.1 cut line") at `$EXTERNAL/FFmpeg`. The file `RELEASE` reads `9.1`. The clone was not modified; nothing was built, installed or run. Checked 2026-11-21. Version read by this desk check: 9.1.

## Repository facts

- `README.md`: "FFmpeg is a collection of libraries and tools to process multimedia content such as audio, video, subtitles and related metadata." Libraries: `libavcodec`, `libavformat`, `libavutil`, `libavfilter`, `libavdevice`, `libswresample`, `libswscale`. Tools: `ffmpeg`, `ffplay`, `ffprobe`, "Additional small tools such as `aviocat`, `ismindex` and `qt-faststart`." Offline documentation is in `doc/`.
- `LICENSE.md`: "Most files in FFmpeg are under the GNU Lesser General Public License version 2.1 or later (LGPL v2.1+)". "Some optional parts of FFmpeg are licensed under the GNU General Public License version 2 or later (GPL v2+)"; "None of these parts are used by default, you have to explicitly pass `--enable-gpl` to configure to activate them. In this case, FFmpeg's license changes to GPL v2+." The GPL parts include a list of filters in libavfilter (for example `vf_blackframe.c`, `vf_boxblur.c`, `vf_cropdetect.c`, `vf_delogo.c`, `vf_eq.c`). `configure --help` also lists `--enable-nonfree`.
- Folders: `fftools/` (the programs), `libav*` and `libsw*` (the libraries), `doc/`, `tools/` (small utilities), `tests/`, `compat/`, `presets/`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/FFmpeg/FFmpeg`: description "Mirror of https://git.ffmpeg.org/ffmpeg.git"; `pushed_at` 2026-11-21T10:56:32Z; default branch `master`; not archived; licence reported as `NOASSERTION` (GitHub cannot detect the split licence; the licence above is read from `LICENSE.md`).
- `gh api repos/FFmpeg/FFmpeg/releases/latest` answers 404: the mirror publishes no GitHub releases. Tags were read instead: the highest release tag (names of the form `n<major>.<minor>[.<patch>]`, sorted by version) is `n9.1`; `n9.2-dev` is a development tag. Earlier releases seen: `n9.0`, `n9.0.1`, `n9.0.2`, `n8.1.3`.
- The first lines of the `gh api repos/FFmpeg/FFmpeg/tags` listing are old tags such as `v0.6.1`, so the unsorted listing does not show the latest release.
- The clone was at the default branch commit `ae9f4540cb6a549118aacef8361dc2f8da9d5f4a` (2026-11-21) and was moved to `n9.1`.

## How to run here

- **Clone**: `git clone --depth 1 https://github.com/FFmpeg/FFmpeg $EXTERNAL/FFmpeg`, then `git fetch --depth 1 origin tag n9.1` and `git checkout -q n9.1`. Read only; never build or edit it. Read first: `doc/ffmpeg.texi`, `doc/ffprobe.texi`, and the sections "select, aselect" and "showinfo" of `doc/filters.texi`. The website `https://ffmpeg.org` carries the same documentation.
- **Outbound calls**: `ffmpeg` opens network protocols only when given a URL; `configure` has `--disable-network` ("disable network support"). A search of `fftools`, `libavformat`, `libavcodec` and `libavutil` for `telemetry` and `analytics` found no match. Read in the source, not observed.
- **Switch off**: nothing to switch off for local files; give only local paths.
- **Install steps to avoid**: building from the clone, `--enable-gpl` and `--enable-nonfree` builds (they change the licence of the result), Docker images. Installation waits for the user's yes. The kit's guide uses a Homebrew package (see the use record).

## Parts

Parts are the command-line programs of `fftools/` and the filters the kit uses.

### `ffmpeg` (`fftools/ffmpeg.c`, `doc/ffmpeg.texi`)

- "a command line toolbox to manipulate, convert and stream multimedia content" (README). Options read in `doc/ffmpeg.texi`: `-vn` (drops video), `-ac` channels, `-ar` sample rate, `-vf` and `-af` filter graphs, `-q` quality, `-fps_mode`.
- `-fps_mode` (documented at "Set video sync method / framerate mode"): values `passthrough`, `cfr`, `vfr` ("Frames are passed through with their timestamp or dropped so as to prevent 2 frames from having the same timestamp."), `auto` (default). The option table in `fftools/ffmpeg_opt.c` defines `fps_mode`; a search of `fftools/*.c` for the option names `"vsync"` and `"-vsync"` finds none, and `doc/ffmpeg.texi` does not mention `vsync`. So in n9.1 the old `-vsync` option is gone and `-fps_mode` is the one to use.
- Needs: a binary. Anything notable: `-v info` prints the filter log to standard error, which is where `showinfo` writes.

### `ffprobe` (`fftools/ffprobe.c`, `doc/ffprobe.texi`)

- "gathers information from multimedia streams and prints it in human- and machine-readable fashion"; options include `-show_format` and `-show_streams`. Needs: a binary.

### `ffplay` (`fftools/ffplay.c`, `doc/ffplay.texi`)

- "a minimalistic multimedia player". Needs: a binary and a display. Not read beyond the README line and the doc title.

### Filter `select` (`doc/filters.texi`, section "select, aselect")

- Passes frames for which an expression is non-zero. The variable `scene` ("value between 0 and 1 to indicate a new scene") and the example `ffmpeg -i video.avi -vf select='gt(scene\,0.4)',scale=160:120,tile -frames:v 1 preview.png`; the docs say "Comparing scene against a value between 0.3 and 0.5 is generally a sane choice."

### Filter `showinfo` (`doc/filters.texi`, section "showinfo"; `libavfilter/vf_showinfo.c`)

- "Show a line containing various information for each input video frame. The input video is not modified." Each line carries `pts_time:` (read in `vf_showinfo.c`), so the times of the frames a `select` passed can be read from the log.

### Small tools in `tools/` (read by name only)

- `aviocat`, `ismindex`, `qt-faststart`, `ffescape`, `ffeval`, `ffhash`, `graph2dot` and others are in `tools/`; `doc/examples/` holds 27 files of C examples for the libraries. Not read.

### Libraries (`libavcodec`, `libavformat`, `libavfilter`, `libavutil`, `libavdevice`, `libswresample`, `libswscale`)

- Named in the README; not read for this check.

## How the kit uses it

The kit's script `scripts/meeting2md.py` calls `ffmpeg` twice; the use record is `raw/notes/trials/2026-11-21-ffmpeg-audio-and-scene-frames-for-transcripts.md`. Status after it: `ffmpeg` is `in use`, and the filters `select` and `showinfo` are `in use` inside its second call.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 46 model calls on sonnet, $2.03 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
