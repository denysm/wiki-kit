"""Transcribe a meeting recording locally with whisper.cpp and attach speakers from a Teams transcript.

Usage: meeting2md.py <recording.mp4|.wav> <out.md> [--teams teams_transcript.md] [--lang ru]
                     [--model ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin] [--prompt "names, terms"]
                     [--frames DIR] [--scene 0.25]

--frames DIR also saves scene-change frames (screen share) as f_NNN_MMmSSs.jpg plus timestamps.tsv.
Keep DIR next to the recording, wherever the recording is archived, named "<recording stem>-frames".

Steps: ffmpeg extracts 16 kHz mono audio to a temp dir; whisper-cli (Metal) transcribes it to JSON;
segments are grouped into speaker blocks using the "Name   m:ss" turn lines of the Teams transcript
(a label can be off at a turn boundary); without --teams every block is "Speaker".
Writes the body only: "**Speaker** [m:ss]" + text.
Add frontmatter yourself (or with doc2md conventions). No model tokens are spent.
58 minutes of audio took about 2.5 minutes on an M4 Pro with large-v3-turbo.
Needs ffmpeg and whisper-cli (whisper.cpp) on PATH. Guide: docs/meeting-recordings-to-markdown.md.
Model download: https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
"""
import argparse, json, os, re, shutil, subprocess, tempfile


def turns_from_teams(path):
    turns = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(.+?)\s{2,}(?:(\d+):)?(\d+):(\d{2})\s*$", line.rstrip("\n"))
        if m:
            s = int(m.group(2) or 0) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            turns.append((s, m.group(1).strip()))
    return turns


def save_frames(rec, out, scene):
    os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", rec, "-vf",
                            f"select='gt(scene,{scene})',showinfo,scale=1280:-1", "-fps_mode", "vfr",
                            "-q:v", "4", os.path.join(d, "f_%03d.jpg")], capture_output=True, text=True, check=True)
        times = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
        rows = []
        for i, t in enumerate(times, 1):
            src = os.path.join(d, f"f_{i:03d}.jpg")
            if not os.path.exists(src):
                continue
            name = f"f_{i:03d}_{int(t // 60):02d}m{int(t % 60):02d}s.jpg"
            shutil.move(src, os.path.join(out, name))
            rows.append(f"{name}\t{int(t // 60)}:{int(t % 60):02d}")
    open(os.path.join(out, "timestamps.tsv"), "w").write("\n".join(rows) + "\n")
    print(f"{len(rows)} frames -> {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("recording"); ap.add_argument("out")
    ap.add_argument("--teams"); ap.add_argument("--lang", default="ru")
    ap.add_argument("--model", default=os.path.expanduser("~/.cache/whisper-cpp/ggml-large-v3-turbo.bin"))
    ap.add_argument("--prompt", default="")
    ap.add_argument("--frames", help="save scene-change frames into this folder")
    ap.add_argument("--scene", type=float, default=0.25)
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.recording, "-vn", "-ac", "1", "-ar", "16000",
                        "-c:a", "pcm_s16le", wav], check=True)
        cmd = ["whisper-cli", "-m", a.model, "-f", wav, "-l", a.lang, "-t", "10", "-oj", "-of", os.path.join(d, "w")]
        if a.prompt:
            cmd += ["--prompt", a.prompt]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segs = json.load(open(os.path.join(d, "w.json"), encoding="utf-8"))["transcription"]
    if a.frames:
        save_frames(a.recording, a.frames, a.scene)
    turns = turns_from_teams(a.teams) if a.teams else []

    def spk(t):
        who = turns[0][1] if turns else "Speaker"
        for s, n in turns:
            if s <= t + 1:
                who = n
            else:
                break
        return who

    blocks, cur = [], None
    for g in segs:
        x, y = g["offsets"]["from"] / 1000, g["offsets"]["to"] / 1000
        txt = g["text"].strip()
        if not txt:
            continue
        who = spk((x + y) / 2)
        if cur and cur[0] == who:
            cur[2].append(txt)
        else:
            cur = [who, x, [txt]]; blocks.append(cur)
    with open(a.out, "w", encoding="utf-8") as f:
        for who, x, parts in blocks:
            f.write(f"**{who}** [{int(x // 60)}:{int(x % 60):02d}]\n{' '.join(parts)}\n\n")
    print(f"{len(segs)} segments, {len(blocks)} blocks, {len(turns)} Teams turns -> {a.out}")


if __name__ == "__main__":
    main()
