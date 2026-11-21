#!/usr/bin/env python3
"""Speech-recognition bench: compare local engines on your own recordings (voice/bench/README.md).

Usage:
  asr_bench.py run   [--audio ~/VoiceBench] [--refs voice/bench] [--engines LIST] [--lang ru]
                     [--glossary FILE] [--only read-1,free-2]
  asr_bench.py draft NAME [--engine whisper] [--audio ~/VoiceBench]   draft a reference to correct by hand
  asr_bench.py engines                                                list engines and whether they are ready

Recordings: <audio>/<name>.<m4a|wav|mp3|flac|ogg|caf> with names read-1..3 and free-1..2.
References: <refs>/<name>.txt (the read texts in the kit), else <audio>/<name>.ref.txt (corrected drafts,
kept next to the recordings). Hypotheses go to <audio>/hyp/<engine>/<name>.txt; results to
<audio>/results-<date>.json and a Markdown table on stdout. Nothing is written into the kit.

Engines (all local; paths through the environment):
  whisper          whisper-cli + $WHISPER_MODEL (default ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin)
  whisper-glossary the same with --prompt from --glossary (names and terms, one line)
  parakeet-cli     whisper.cpp parakeet-cli + $PARAKEET_GGML (ggml-parakeet-tdt-0.6b-v3-f16.bin); not in the
                   default list: the Homebrew 1.9.5 build aborted on this model on 2026-11-21
  nemo-parakeet    $NEMO_SPEECH transcribe --model $PARAKEET_GGUF (parakeet-tdt-0.6b-v3.q8_0.gguf)
  nemo-nemotron    $NEMO_SPEECH transcribe --model $NEMOTRON_GGUF, whole file at once
  nemo-nemotron-stream  the same with --stream (160 ms chunks through the streaming recogniser)
$VOICE_SANDBOX (default ~/.cache/wiki-kit/voice-sandbox) holds models/ and the unpacked nemo-speech.

Metrics after normalisation (lower case, ё -> е, punctuation and dashes dropped, digits kept):
WER and CER; latin = share of the reference's Latin-script words found in the hypothesis (English
terms); digits = share of number tokens found; rtf = processing seconds per audio second; mem = peak
resident memory of the engine process (from /usr/bin/time -l). Standard library only; needs ffmpeg.
"""
import argparse, glob, json, os, re, subprocess, sys, tempfile, time

HOME = os.path.expanduser("~")
SB = os.environ.get("VOICE_SANDBOX", os.path.join(HOME, ".cache/wiki-kit/voice-sandbox"))
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTS = ("m4a", "wav", "mp3", "flac", "ogg", "caf", "aiff", "aac")


def nemo_bin():
    if os.environ.get("NEMO_SPEECH"):
        return os.environ["NEMO_SPEECH"]
    hits = sorted(glob.glob(os.path.join(SB, "nemo", "**", "bin", "nemo-speech"), recursive=True))
    return hits[0] if hits else "nemo-speech"


def model(env, name):
    return os.environ.get(env, os.path.join(SB, "models", name))


def engines(lang, glossary):
    wm = os.environ.get("WHISPER_MODEL", os.path.join(HOME, ".cache/whisper-cpp/ggml-large-v3-turbo.bin"))
    loc = {"ru": "ru-RU", "uk": "uk-UA", "en": "en-US", "fr": "fr-FR", "de": "de-DE", "es": "es-ES",
           "nl": "nl-NL"}.get(lang, lang)
    nemo = nemo_bin()
    e = {
        "whisper": (["whisper-cli", "-m", wm, "-l", lang, "-t", "8", "-otxt", "-f"], wm),
        "parakeet-cli": (["parakeet-cli", "-m", model("PARAKEET_GGML", "ggml-parakeet-tdt-0.6b-v3-f16.bin"), "-f"],
                         model("PARAKEET_GGML", "ggml-parakeet-tdt-0.6b-v3-f16.bin")),
        "nemo-parakeet": ([nemo, "--quiet", "transcribe", "--model", model("PARAKEET_GGUF", "parakeet-tdt-0.6b-v3.q8_0.gguf"),
                           "--language", loc], model("PARAKEET_GGUF", "parakeet-tdt-0.6b-v3.q8_0.gguf")),
        "nemo-nemotron": ([nemo, "--quiet", "transcribe", "--model", model("NEMOTRON_GGUF", "nemotron-3.5-asr-streaming-0.6b.q8_0.gguf"),
                           "--language", loc], model("NEMOTRON_GGUF", "nemotron-3.5-asr-streaming-0.6b.q8_0.gguf")),
    }
    e["nemo-nemotron-stream"] = (e["nemo-nemotron"][0] + ["--stream"], e["nemo-nemotron"][1])
    if glossary:
        e["whisper-glossary"] = (e["whisper"][0][:-1] + ["--prompt", open(glossary, encoding="utf-8").read().strip(), "-f"], wm)
    return e


def norm(t):
    t = t.lower().replace("ё", "е")
    t = re.sub(r"(?<=\d)[.,:](?=\d)", "\u0001", t)          # keep 4.2 and 15:30 together
    t = re.sub(r"[^\w\u0001]+", " ", t).replace("\u0001", ".").replace("_", " ")
    return t.split()


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def share(ref_tokens, hyp_tokens):
    if not ref_tokens:
        return None
    pool = list(hyp_tokens); hit = 0
    for t in ref_tokens:
        if t in pool:
            pool.remove(t); hit += 1
    return hit / len(ref_tokens)


def score(ref, hyp):
    r, h = norm(ref), norm(hyp)
    rc, hc = " ".join(r), " ".join(h)
    lat = lambda ws: [w for w in ws if re.search(r"[a-z]", w)]
    dig = lambda ws: [w for w in ws if re.search(r"\d", w)]
    return {"wer": lev(r, h) / max(1, len(r)), "cer": lev(rc, hc) / max(1, len(rc)),
            "latin": share(lat(r), lat(h)), "digits": share(dig(r), dig(h)), "ref_words": len(r)}


def to_wav(src, d):
    out = os.path.join(d, os.path.splitext(os.path.basename(src))[0] + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", out], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                               capture_output=True, text=True).stdout.strip())
    return out, dur


def transcribe(cmd, wav, name, d):
    if cmd[0] == "whisper-cli":  # its stdout carries timestamps; read the plain text file instead
        txt = os.path.join(d, "w-" + name)
        cmd = cmd[:-1] + ["-of", txt, "-f"]
    full = ["/usr/bin/time", "-l"] + cmd + [wav]
    t0 = time.time(); p = subprocess.run(full, capture_output=True, text=True); dt = time.time() - t0
    mem = re.search(r"(\d+)\s+maximum resident set size", p.stderr)
    if p.returncode != 0:
        raise RuntimeError(f"exit {p.returncode}: {p.stderr.strip().splitlines()[-3:]}")
    out = open(txt + ".txt", encoding="utf-8").read() if cmd[0] == "whisper-cli" else p.stdout
    lines = [l for l in out.splitlines() if l.strip()]
    if cmd[0] == "parakeet-cli":  # keep the transcript, drop its progress lines
        lines = [l for l in lines if not re.match(r"^(Processing|parakeet_|load_|ggml_|Segments|Segment \d|Tokens|\s*\[)", l)]
    return " ".join(l.strip() for l in lines), dt, (int(mem.group(1)) / 2**20 if mem else None)


def recordings(audio, only):
    out = {}
    for f in sorted(os.listdir(audio)):
        stem, ext = os.path.splitext(f)
        if ext.lstrip(".").lower() in EXTS and re.match(r"^(read|free)-\d+$", stem) and (not only or stem in only):
            out[stem] = os.path.join(audio, f)
    return out


def reference(name, refs, audio):
    for p in (os.path.join(refs, name + ".txt"), os.path.join(audio, name + ".ref.txt")):
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    return None


def run(a):
    eng = engines(a.lang, a.glossary)
    names = [x.strip() for x in a.engines.split(",")]
    recs = recordings(a.audio, set(a.only.split(",")) if a.only else None)
    if not recs:
        sys.exit(f"no recordings named read-N or free-N in {a.audio}")
    results = []
    with tempfile.TemporaryDirectory() as d:
        for name, src in recs.items():
            wav, dur = to_wav(src, d)
            ref = reference(name, a.refs, a.audio)
            for e in names:
                cmd, need = eng[e]
                if not os.path.exists(need):
                    print(f"skip {e}: missing {need}", file=sys.stderr); continue
                try:
                    hyp, dt, mem = transcribe(cmd, wav, name, d)
                except RuntimeError as err:
                    print(f"{e} {name}: {err}", file=sys.stderr); continue
                hp = os.path.join(a.audio, "hyp", e); os.makedirs(hp, exist_ok=True)
                open(os.path.join(hp, name + ".txt"), "w", encoding="utf-8").write(hyp + "\n")
                row = {"engine": e, "file": name, "seconds": round(dur, 1), "rtf": round(dt / dur, 3),
                       "mem_mb": round(mem) if mem else None}
                if ref:
                    row.update({k: (round(v, 4) if isinstance(v, float) else v) for k, v in score(ref, hyp).items()})
                results.append(row); print(json.dumps(row, ensure_ascii=False), file=sys.stderr)
    out = os.path.join(a.audio, time.strftime("results-%Y%m%d-%H%M.json"))
    json.dump(results, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    table(results); print(f"\nresults: {out}")


def table(rows):
    pct = lambda v: "" if v is None else f"{100 * v:.1f}"
    print("| engine | file | WER % | CER % | latin % | digits % | rtf | mem MB |\n|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['engine']} | {r['file']} | {pct(r.get('wer'))} | {pct(r.get('cer'))} | {pct(r.get('latin'))} | "
              f"{pct(r.get('digits'))} | {r['rtf']} | {r['mem_mb'] or ''} |")
    by = {}
    for r in rows:
        if r.get("wer") is not None:
            by.setdefault(r["engine"], []).append(r)
    if by:
        print("\n| engine | files | mean WER % (by words) | mean latin % | mean rtf |\n|---|---|---|---|---|")
        for e, rs in by.items():
            w = sum(r["wer"] * r["ref_words"] for r in rs) / sum(r["ref_words"] for r in rs)
            lat = [r["latin"] for r in rs if r.get("latin") is not None]
            print(f"| {e} | {len(rs)} | {100 * w:.1f} | {pct(sum(lat) / len(lat)) if lat else ''} | "
                  f"{sum(r['rtf'] for r in rs) / len(rs):.3f} |")


def draft(a):
    eng = engines(a.lang, None)
    src = recordings(a.audio, {a.name}).get(a.name) or sys.exit(f"no recording {a.name} in {a.audio}")
    with tempfile.TemporaryDirectory() as d:
        wav, _ = to_wav(src, d)
        hyp, dt, _ = transcribe(eng[a.engine][0], wav, a.name, d)
    p = os.path.join(a.audio, a.name + ".draft.txt")
    open(p, "w", encoding="utf-8").write(re.sub(r"(?<=[.!?…])\s+", "\n", hyp) + "\n")
    print(f"draft ({a.engine}, {dt:.1f} s) -> {p}\ncorrect it and save as {a.name}.ref.txt in the same folder")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("run", "draft", "engines"):
        s = sub.add_parser(n)
        s.add_argument("--audio", default=os.path.join(HOME, "VoiceBench"))
        s.add_argument("--lang", default="ru")
        if n == "run":
            s.add_argument("--refs", default=os.path.join(KIT, "voice", "bench"))
            s.add_argument("--engines", default="whisper,nemo-parakeet,nemo-nemotron,nemo-nemotron-stream")
            s.add_argument("--glossary"); s.add_argument("--only")
        if n == "draft":
            s.add_argument("name"); s.add_argument("--engine", default="whisper")
    a = ap.parse_args()
    if a.cmd == "engines":
        for k, (cmd, need) in engines(a.lang, None).items():
            print(f"{k:22} {'ready' if os.path.exists(need) else 'missing ' + need}  {cmd[0]}")
        return
    (run if a.cmd == "run" else draft)(a)


if __name__ == "__main__":
    main()
