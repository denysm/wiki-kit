# Meeting recordings to Markdown

How to turn a recorded call into a raw source for the wiki without spending model tokens: transcribe it locally with Whisper, take speaker changes from the meeting platform's own transcript, and save a frame each time the shared screen changes. Script: [`scripts/meeting2md.py`](../scripts/meeting2md.py).

## Why not just use the platform transcript

The transcript that Teams makes during the call is fine for knowing who spoke when, and weak at everything else when people speak Russian with English technical terms in it. Product and tool names come out as phonetic nonsense, and numbers get lost. A compile from that text leaves the key points unclear, and a second pass to check them against the recording costs more than the first.

Local Whisper `large-v3-turbo` gets the wording, the names and the numbers right far more often, so the two transcripts split the work:

| Question | Source |
|---|---|
| What was said: wording, terms, numbers | Whisper transcript |
| Who said it | Teams turn lines (`Name   m:ss`) |
| What was on the screen | Scene-change frames |

In one measured case, compiling from the Teams text and then verifying it cost about $4.5 in a single answer. The script itself costs nothing: it runs on your machine, and the model reads only the finished Markdown.

## Rule

Transcribe before any compile. Run `meeting2md.py` once, compile once from the Whisper text, and keep the Teams transcript beside it for speaker questions.

## Setup

1. Install the two programs. macOS: `brew install ffmpeg whisper-cpp`. Linux: ffmpeg from your package manager and a [whisper.cpp](https://github.com/ggerganov/whisper.cpp) build that provides `whisper-cli`.
2. Download the model (about 1.6 GB) once:

   ```bash
   mkdir -p ~/.cache/whisper-cpp
   curl -L -o ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
   ```

3. Download the Teams transcript of the meeting and convert it to text (for example `doc2md.py` for the `.docx`). The script reads only its turn lines: a speaker name, two or more spaces, a time (`Name   13:57`).

## Run

```bash
python3 -I scripts/meeting2md.py "recording.mp4" out.md \
  --teams teams-transcript.md \
  --prompt "names of the people, products and terms you expect" \
  --frames "recording-frames"
```

- `--lang` defaults to `ru`; pass `--lang en` (or another Whisper language code) for other calls.
- `--prompt` is the cheapest accuracy gain: list the participants' names and the product and tool names that will come up.
- `--frames DIR` saves a JPEG each time the picture changes (`f_NNN_MMmSSs.jpg`) and `timestamps.tsv`. Keep the folder next to the recording, named `<recording stem>-frames`. `--scene` sets the threshold (default `0.25`; lower gives more frames).
- Without `--teams` every block is labelled `Speaker`.

The output is the body only: one block per speaker turn, `**Name** [m:ss]` and the text. Add the raw source frontmatter yourself (`source`, `authors`, `source_date`, `ingested`), and say in `source` that the text is a local Whisper transcript with speakers taken from the platform transcript.

## What to expect

- Speed: 58 minutes of audio took about 2.5 minutes on an Apple M4 Pro (Metal). The frame pass reads the whole video once more.
- Frames: 53 frames for a 58-minute call with screen sharing, enough for an agent to describe what was shown. Describe them in the raw file; do not put the images into the wiki.
- Speaker labels can be off by one segment at a turn boundary, because Whisper segments and Teams turns are cut at different moments.

## Pitfalls

- ffmpeg 8 removed `-vsync`; the script uses `-fps_mode vfr` and reads frame times from `pts_time` in the `showinfo` log.
- The recording, the frames and the Teams transcript are originals: keep them where your recordings are archived, not in the wiki. Only the Markdown transcript enters `raw/`, under the same confidentiality rules as any other source.
