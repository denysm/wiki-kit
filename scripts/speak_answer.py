#!/usr/bin/env python3
"""Speak Claude Code's answers aloud on macOS: a Stop hook (phase 0 of docs/voice-design.md).

Usage:
  speak_answer.py                      hook mode: read the Stop hook JSON on stdin, speak the answer if on
  speak_answer.py on | off | status    switch spoken answers on or off (off by default)
  speak_answer.py stop                 stop the answer being spoken now
  speak_answer.py test [TEXT] [--file OUT.aiff]
                                       show the voice and text that would be spoken; with --file,
                                       synthesise into a file (no sound) and print the time it took
  speak_answer.py install | uninstall  add or remove the async Stop hook in ~/.claude/settings.json
                                       (a dated backup of the file is written first)

What is spoken: the start of the answer, up to max_chars, cut at a sentence end. Code blocks,
tables, links' addresses and Markdown marks are left out. The voice follows the language of the
text: Cyrillic with Kazakh letters -> kk, with Ukrainian letters -> uk, other Cyrillic -> ru; Latin
text -> en, fr, de, es or nl by common words. A new answer stops the one still being spoken.

Config (created on first use, never committed): ~/.config/wiki-kit/voice/speak.json
  {"on": false, "max_chars": 600, "rate": null, "device": null, "voices": {"ru": "Milena", ...}}
  rate: words per minute for `say -r`; device: an output device name or ID for `say -a`.
Needs macOS `say`. Standard library only.
"""
import json, os, re, signal, subprocess, sys, time

CONF_DIR = os.path.expanduser("~/.config/wiki-kit/voice")
CONF = os.path.join(CONF_DIR, "speak.json")
PIDF = os.path.join(CONF_DIR, "say.pid")
SETTINGS = os.path.expanduser("~/.claude/settings.json")
VOICES = {"ru": "Milena", "uk": "Lesya", "kk": "Aru", "en": "Samantha", "fr": "Thomas",
          "de": "Anna", "es": "Mónica", "nl": "Xander"}
DEFAULT = {"on": False, "max_chars": 600, "rate": None, "device": None, "voices": VOICES}
STOP = {
    "en": "the and is are you to of in that it for with this be not was on what have can will".split(),
    "fr": "le la les est et des une un du que pour dans pas vous avec sur qui sont ce cette".split(),
    "de": "der die das und ist nicht ein eine ich sie es zu mit den auf für sich auch".split(),
    "es": "el la los las es y que de en un una por con para no se del al como más".split(),
    "nl": "de het een en is van dat niet je ik op te zijn met voor maar ook dit".split(),
}


def load_conf():
    c = dict(DEFAULT)
    try:
        c.update(json.load(open(CONF, encoding="utf-8")))
    except (OSError, ValueError):
        pass
    c["voices"] = {**VOICES, **(c.get("voices") or {})}
    return c


def save_conf(c):
    os.makedirs(CONF_DIR, exist_ok=True)
    json.dump(c, open(CONF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def clean(md):
    t = re.sub(r"```.*?(```|$)", " ", md, flags=re.S)            # fenced code
    t = re.sub(r"^\s*\|.*\|\s*$", " ", t, flags=re.M)            # tables
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)              # links, images -> their text
    t = re.sub(r"https?://\S+", " ", t)                           # bare addresses
    t = re.sub(r"`([^`]*)`", r"\1", t)                            # inline code marks
    t = re.sub(r"^\s*(written for|написано для)\b.*$", " ", t, flags=re.M | re.I)  # audience lines
    t = re.sub(r"(токены|tokens)\s*:[^\n]*", " ", t, flags=re.I)  # token reports, to the end of the line
    t = re.sub(r"^\s{0,3}#{1,6}\s+(.*?)[.:!?]?\s*$", r"\1.", t, flags=re.M)  # headings end with a pause
    t = re.sub(r"^\s{0,3}(>|[-*+]|\d+[.)])\s+", "", t, flags=re.M)  # quotes, lists
    t = re.sub(r"(\*\*|__|\*|_|~~)(?=\S)(.+?)(?<=\S)\1", r"\2", t)  # bold, italics, strike
    return t


def excerpt(md, limit):
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", clean(md))]
    out = ""
    for p in (p for p in paras if p):
        if len(out) + len(p) + 1 <= limit:
            out = (out + " " + p).strip()
            continue
        if not out:  # first paragraph alone is too long: cut it at a sentence end
            parts = re.split(r"(?<=[.!?…])\s+", p)
            for s in parts:
                if len(out) + len(s) + 1 > limit:
                    break
                out = (out + " " + s).strip()
            out = out or p[:limit]
        break
    return out


def lang_of(text):
    cyr = len(re.findall(r"[А-Яа-яЁёІіЇїЄєҐґӘәҒғҚқҢңӨөҰұҮүҺһ]", text))
    lat = len(re.findall(r"[A-Za-zÀ-ÿ]", text))
    if cyr >= lat and cyr:
        if re.search(r"[ӘәҒғҚқҢңӨөҰұҮүҺһ]", text):
            return "kk"
        if re.search(r"[ІіЇїЄєҐґ]", text) and not re.search(r"[ЫыЭэЪъЁё]", text):
            return "uk"
        return "ru"
    words = re.findall(r"[a-zà-ÿ]+", text.lower())
    score = {k: sum(w in set(v) for w in words) for k, v in STOP.items()}
    best = max(score, key=score.get)
    return best if score[best] else "en"


def stop_speaking():
    try:
        pid = int(open(PIDF).read().strip())
        if "say" in subprocess.run(["ps", "-o", "comm=", "-p", str(pid)],
                                   capture_output=True, text=True).stdout:
            os.kill(pid, signal.SIGTERM)
    except (OSError, ValueError):
        pass


def say_cmd(c, text, lang, out=None):
    cmd = ["say", "-v", c["voices"].get(lang, VOICES["en"])]
    if c.get("rate"):
        cmd += ["-r", str(c["rate"])]
    if c.get("device") and not out:
        cmd += ["-a", str(c["device"])]
    if out:
        cmd += ["-o", out]
    return cmd + ["--", text]


def speak(c, text):
    lang = lang_of(text)
    stop_speaking()
    os.makedirs(CONF_DIR, exist_ok=True)
    p = subprocess.Popen(say_cmd(c, text, lang), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
    open(PIDF, "w").write(str(p.pid))


def hook():
    c = load_conf()
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    if not c.get("on"):
        return
    text = excerpt(data.get("last_assistant_message") or "", int(c.get("max_chars") or 600))
    if text:
        speak(c, text)


def hook_command():
    return f"python3 -I {os.path.abspath(__file__)}"


def install(remove=False):
    try:
        s = json.load(open(SETTINGS, encoding="utf-8"))
    except FileNotFoundError:
        s = {}
    if os.path.exists(SETTINGS):
        bak = SETTINGS + time.strftime(".bak-%Y%m%d-%H%M%S")
        open(bak, "w", encoding="utf-8").write(open(SETTINGS, encoding="utf-8").read())
        print(f"backup: {bak}")
    groups = s.setdefault("hooks", {}).setdefault("Stop", [])
    mine = lambda g: any("speak_answer.py" in (h.get("command") or "") for h in g.get("hooks", []))
    groups[:] = [g for g in groups if not mine(g)]
    if not remove:
        groups.append({"hooks": [{"type": "command", "command": hook_command(), "async": True, "timeout": 30}]})
    if not groups:
        del s["hooks"]["Stop"]
    if not s["hooks"]:
        del s["hooks"]
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    json.dump(s, open(SETTINGS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(("removed" if remove else "installed") + f" Stop hook in {SETTINGS}" +
          ("" if remove else f": {hook_command()} (async). Spoken answers are {'on' if load_conf()['on'] else 'off'}; "
                              "turn on with: speak_answer.py on"))


def main():
    a = sys.argv[1:]
    if not a:
        return hook()
    c = load_conf()
    if a[0] in ("on", "off"):
        c["on"] = a[0] == "on"; save_conf(c); print(f"spoken answers: {a[0]}")
    elif a[0] == "status":
        print(json.dumps({**c, "config": CONF}, ensure_ascii=False, indent=2))
    elif a[0] == "stop":
        stop_speaking()
    elif a[0] == "test":
        out = a[a.index("--file") + 1] if "--file" in a else None
        words = [x for i, x in enumerate(a[1:], 1) if x != "--file" and (i == 1 or a[i - 1] != "--file")]
        text = excerpt(" ".join(words) or "Проверка голоса: это начало ответа.", int(c["max_chars"]))
        lang = lang_of(text)
        print(f"lang={lang} voice={c['voices'].get(lang)} chars={len(text)}\n{text}")
        if out:
            t0 = time.time(); subprocess.run(say_cmd(c, text, lang, out), check=True)
            print(f"synthesised in {time.time() - t0:.2f} s -> {out}")
    elif a[0] in ("install", "uninstall"):
        install(remove=a[0] == "uninstall")
    else:
        print(__doc__); sys.exit(2)


if __name__ == "__main__":
    main()
