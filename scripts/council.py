#!/usr/bin/env python3
"""Ask several LLMs the same question over a wiki evidence packet, then let a blind judge compare.

PKIS patterns (2025-12): compare (independent experts) + Judge v1 (goal-aware rubric)
+ cost accounting. Claude runs through the local `claude -p` (subscription, no API key);
other vendors use their OpenAI-compatible endpoints with keys from the environment or
~/.config/llm-wiki/council.env (KEY=value lines, chmod 600).

Usage:
  council.py --list [VENDOR...]                       # models each configured vendor offers
  council.py -q "question" [--goal "..."] [--context FILE...]
             [--preset cheap|balanced|deep|private] [--models V:M,...] [--judge V:M|none]
             [--max-usd 0.50] [--dry-run] [--out report.md] [--web] [--mode compare|ensemble]
  council.py --verify ANSWER.md|- [--context SRC...] [-q "question"] [--verifier V:M,...]
  council.py --route -q "question" [--kind K]          # advice only: type, model, cost, command
  council.py --mark [RUN] decision|error|nothing [--note "..."] [--by claude]   # usefulness journal
  council.py --journal                                 # usefulness and cost per insight
  council.py --learn [--kind K]                        # learned scores per task kind and member

Members are VENDOR:MODEL[@EFFORT]. Vendors: claude, deepseek, openai, gemini, openrouter, ollama.
EFFORT is passed only when given, so by default every model runs at its own default level
(DeepSeek: thinking on, high). Values: none (DeepSeek: thinking off), minimal, low, medium, high,
xhigh, max; each vendor maps or rejects what it does not support (claude: low..max via --effort;
others: reasoning_effort). Examples: deepseek:deepseek-v4-pro@max, openai:gpt-6.1-sol@high,
deepseek:deepseek-flash@none, claude:opus@xhigh. `--list openrouter --grep gemini` filters the catalog.
Prices come from council_prices.json next to this script (per 1M tokens: cache miss, cache hit,
output; DeepSeek in CNY with off-peak hours; OpenAI long-context rates). Every priced call is
appended to ~/.config/llm-wiki/council_ledger.tsv. For claude the cost is what `claude -p`
reports (notional on a subscription). `council.py --prices` prints the table.

Every run (compare, ensemble, verify) gets a run id in ~/.config/llm-wiki/council_journal.tsv;
mark it afterwards: decision = changed the decision, error = found a mistake, nothing = nothing new.
`--journal` shows the useful share and paid USD per insight by mode. `--route` never spends:
it names the task type, a member and a measured price range to offer to the operator.

Learning: every run records a task kind (free text via --kind, e.g. the current project; otherwise a
regex guess) and the wiki topic (from --context paths). Judges and critics end with a SCORES line;
per-member scores go to ~/.config/llm-wiki/council_stats.tsv (model_bench.py --export-stats seeds it
from a bench). `--route` and `--learn` read these stats, so advice follows what is measured.

Power cuts: every answer is saved to ~/.cache/llm-wiki/council-answers/ the moment it arrives, so after
a crash the same command (also model_bench.py, verify_articles.py) replays what was already answered
and pays only for the rest. An identical call within COUNCIL_RESUME_HOURS (default 24) replays;
--fresh asks again. A replay that was already in the ledger costs 0 in the new run; one cut off
before the ledger is counted once, now. Journal, stats and reports are written atomically.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ENV_FILE = Path("~/.config/llm-wiki/council.env").expanduser()
PRICES_FILE = Path(__file__).with_name("council_prices.json")
LEDGER = Path("~/.config/llm-wiki/council_ledger.tsv").expanduser()
JOURNAL = Path("~/.config/llm-wiki/council_journal.tsv").expanduser()
JOURNAL_COLS = ["run", "time", "mode", "kind", "topic", "members", "paid_usd", "signal", "mark", "by", "note", "question"]
STATS = Path("~/.config/llm-wiki/council_stats.tsv").expanduser()
STATS_COLS = ["time", "run", "source", "kind", "topic", "member", "score", "best", "cost_usd", "web"]
ANSWERS = Path("~/.cache/llm-wiki/council-answers").expanduser()
RESUME_HOURS = float(os.environ.get("COUNCIL_RESUME_HOURS", "24"))  # identical call within this window replays
MIN_N = 2  # observations per kind and member before learned stats drive --route
# never sent to outside vendors (operator rule: employer/client data stays with Claude or a local model)
PRIVATE_TOPICS = {"work"}
LOCAL_VENDORS = {"claude", "ollama"}
MARKS = {"decision": "changed the decision", "error": "found a mistake", "nothing": "nothing new"}
VENDORS = {
    "deepseek": ("https://api.deepseek.com/v1", "DEEPSEEK_API_KEY"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "ollama": ("http://localhost:11434/v1", None),
}
NOT_CHAT = r"tts|transcribe|audio|realtime|image|embed|moderation|whisper|dall-e|babbage|davinci"
DATED = r"-\d{4}-\d{2}-\d{2}$|-\d{4}$"  # OpenAI snapshot ids; on OpenRouter such ids are distinct models
# presets from the model bench of 2026-10-26 (output/model-bench in the personal wiki);
# the judge is always from a family outside the members
PRESETS = {
    # bench v3 (2026-10-26): Claude by subscription carries the answers; cheap no-web models add diversity
    "cheap": ("deepseek:deepseek-flash,openai:gpt-6-luna,openrouter:z-ai/glm-5.3", "deepseek:deepseek-v4-pro"),
    "balanced": ("claude:sonnet,deepseek:deepseek-flash,openai:gpt-6-luna", "openai:gpt-6.1-sol"),
    "deep": ("claude:opus,claude:sonnet,deepseek:deepseek-flash,openai:gpt-6.1-sol", "deepseek:deepseek-v4-pro"),
    "private": ("claude:opus,claude:sonnet", "claude:opus"),  # subscription only; same-family judge
}
DEFAULT_PRESET = "balanced"
EXPERT = ("You are an independent expert. Do not assume other experts exist. "
          "Answer the question using the provided knowledge first; mark anything not supported "
          "by it as your own assumption. Be concrete and concise. Answer in the language of the question.")
JUDGE = """You are a senior reviewer. You receive several anonymous answers (A, B, ...) to the same question.
Judge which answer best serves the asker's goal under their constraints, not which sounds smartest.
Ignore answer length and order. Criteria (score each 1-5): fit to goal, depth of reasoning,
use of the provided knowledge, practical usefulness, blind spots / risks named, novelty.
Return Markdown:
## Scores
table: answer | each criterion | total
## Best
which answer and why (3-5 sentences)
## Disagreements
where the answers contradict each other and which side the evidence supports; keep real disagreements
## Synthesis
the best combined answer, discarding weak ideas
Answer in the language of the question.
Finish with one line exactly like: SCORES {"Answer 1": 24, "Answer 2": 19} (totals, max 30)."""
VERIFY = """You are a skeptical fact-checker from a different model family than the author.
You receive a question (optional), sources (optional) and an answer or wiki article written by someone else.
Do not rewrite the answer. Find what is wrong or missing. Return Markdown:
## Unsupported claims
table: claim (short quote) | verdict (supported by SOURCE / not in sources / contradicts SOURCE / doubtful) | why
List every factual claim that sources do not back; when no sources are given, list claims that need checking.
## Gaps
what the answer misses that matters for the question or goal (max 5)
## Contradictions
inside the answer or with the sources
## Verdict
one line: ok / minor fixes / major fixes
Answer in the language of the answer."""
HYPO = ("You are one of several independent experts. Propose 2-4 distinct hypotheses or options that answer the "
        "question, each with the key reasoning, the evidence for it and what would prove it wrong. Use the provided "
        "knowledge first; mark your own assumptions. Be concise. Answer in the language of the question.")
CRITIC = """You are a critic. You receive anonymous hypotheses (H1, H2, ...) from several experts.
For each: the strongest objection, missing evidence, hidden assumptions, and a 1-5 plausibility score.
Then name ideas that all experts missed. Be blunt and concise. Answer in the language of the question.
Finish with one line exactly like: SCORES {"H1": 4, "H2": 2} (plausibility 1-5)."""
SYNTH = """You are the final author. You receive a question, anonymous hypotheses from several experts and a critique.
Write the best answer for the asker's goal: keep what survives the critique, drop weak ideas, keep real
disagreements and say what would settle them. End with ## Next step (one concrete action).
Answer in the language of the question."""
# kind guesses for --route / journal when --kind is not given; kinds match bench v3 task types
# (output/model-bench/tasks-v3.json in the personal wiki). Scores and prices come from STATS.
ROUTES = [
    ("money_law", r"виз|внж|вид на жительств|гражданств|резидент|налог|декларац|апостил|нотари|банк|перевод.{0,20}(денег|деньг|средств)|"
                  r"swift|кредит|ипотек|закон|суд|штраф|договор|юрист|пенси|пособи|visa|residence|tax|bank|legal",
     "Claude слаб на процедурах с поиском (бенч v3: ВНЖ opus 4, sonnet 2)"),
    ("translate", r"переведи|перевод (на|с) |translat|грамматик|словар|домашк.{0,20}язык",
     "редкий язык или текст на фото: ни одна модель не выше 6.5/10 (бенч v3) — проверить у носителя языка, доплата не поможет"),
    ("choose", r"купить|выбрать|сравни|что лучше|какой .{0,30}(взять|выбрать)|цена|стоимост|тариф", ""),
    ("health", r"здоров|симптом|лекарств|врач|болит|болезн|анализ крови|температур", ""),
    ("tech", r"код|скрипт|python|bash|ошибк[аи] в|баг|docker|git\b|sql", ""),
    ("wiki", r"вики|wiki|compile|статья вики|источник", ""),
]
ROUTE_DEFAULT = ("Claude по подписке (8-10 баллов на остальных типах); второе мнение: --preset cheap (≈$0.01) "
                 "или проверка ответа: --verify (≈$0.004)")


def load_env() -> None:
    if ENV_FILE.exists():
        if ENV_FILE.stat().st_mode & 0o077:
            print(f"warn: {ENV_FILE} is readable by others; run chmod 600", file=sys.stderr)
        for line in ENV_FILE.read_text().splitlines():
            k, sep, v = line.partition("=")
            if sep and not line.lstrip().startswith("#") and v.strip():
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def tokens_estimate(text: str) -> int:
    return len(text) // 3


class NoCapability(RuntimeError):
    """The member cannot do what the task needs (vision, web): skip, do not score as 0."""


HTTP_TIMEOUT = int(os.environ.get("COUNCIL_HTTP_TIMEOUT", "600"))  # seconds per socket read; stalled calls fail fast
IMG_CACHE = Path("~/.cache/model-bench").expanduser()
# vision / web support outside the OpenRouter catalog (which states input_modalities itself)
VISION_NO = {"deepseek:deepseek-v4-pro"}
WEB_VENDORS = {"claude", "openai", "openrouter"}


def capable(member: str, need: str) -> bool:
    vendor, model, _ = split_member(member)
    if need == "web":
        return vendor in WEB_VENDORS
    if need == "image":
        if vendor == "openrouter":
            return "image" in OPENROUTER_MODALITIES.get(model, ["image"])
        return member.split("@")[0] not in VISION_NO and not re.search(r"gpt-3\.5|gpt-4(-|$)|o1-mini|o3-mini", model)
    return True


OPENROUTER_MODALITIES: dict[str, list[str]] = {}


def prep_image(path: str) -> tuple[str, str]:
    """Downscale a photo to <=1568 px JPEG (cached), return (media_type, base64)."""
    import base64
    import hashlib
    src = Path(path).expanduser()
    IMG_CACHE.mkdir(parents=True, exist_ok=True)
    out = IMG_CACHE / (hashlib.sha1(str(src).encode()).hexdigest()[:16] + ".jpg")
    if not out.exists():
        subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "1568", str(src), "--out", str(out)],
                       capture_output=True, check=True)
    return "image/jpeg", base64.b64encode(out.read_bytes()).decode()


def call_claude(model: str, system: str, turns: list[str], effort: str = "", images: tuple = (),
                web: bool = False) -> dict:
    """claude -p on the subscription; stream-json input carries images and several user turns."""
    # an API key in the env makes `claude -p` bill the API instead of the subscription
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    msgs = []
    for i, t in enumerate(turns):
        content = [{"type": "text", "text": t}]
        if i == 0:
            for img in images:
                mt, b64 = prep_image(img)
                content.append({"type": "image", "source": {"type": "base64", "media_type": mt, "data": b64}})
        msgs.append(json.dumps({"type": "user", "message": {"role": "user", "content": content}}))
    tools = ["--tools", "WebSearch,WebFetch", "--allowedTools", "WebSearch,WebFetch"] if web else ["--tools", ""]
    with tempfile.TemporaryDirectory() as cwd:  # empty cwd: no project CLAUDE.md
        r = subprocess.run(
            ["claude", "-p", "--model", model, *tools, "--system-prompt", system,
             "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
             "--no-session-persistence", "--strict-mcp-config", "--setting-sources", ""]
            + (["--effort", effort] if effort else []),
            input="\n".join(msgs) + "\n", capture_output=True, text=True, cwd=cwd, env=env, timeout=1800)
    results = [d for d in (json.loads(x) for x in r.stdout.splitlines() if x.startswith("{")) if d.get("type") == "result"]
    if not results:
        raise RuntimeError((r.stderr or r.stdout).strip()[:500])
    if any(d.get("is_error") for d in results):
        raise RuntimeError(next(d.get("result") for d in results if d.get("is_error")))
    ins = cached = outs = 0
    mu: dict = {}
    for d in results:
        u = d.get("usage", {})
        ins += u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        cached += u.get("cache_read_input_tokens", 0)
        outs += u.get("output_tokens", 0)
        for k, v in (d.get("modelUsage") or {}).items():
            mu[k] = mu.get(k, 0) + v.get("costUSD", 0)
    texts = [d["result"] for d in results]
    text = texts[0] if len(texts) == 1 else "\n\n".join(f"### Ход {i + 1}\n{t}" for i, t in enumerate(texts))
    return {"text": text, "model_id": max(mu, key=mu.get) if mu else model,  # side calls use a small model
            "in": ins, "cached": cached, "reasoning": 0, "out": outs,
            "cost": max(d.get("total_cost_usd") or 0 for d in results), "cost_note": "subscription"}


def http_json(url: str, key: str | None, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json",
                                          **({"Authorization": f"Bearer {key}"} if key else {})})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace")
            try:  # {"error": {"message"}} or [{"error": {...}}] (Gemini)
                j = json.loads(raw)
                j = j[0] if isinstance(j, list) else j
                detail = (j.get("error") or {}).get("message") or raw
            except (ValueError, AttributeError, IndexError):
                detail = raw
            detail = " ".join(detail.split())[:300]
            if e.code == 503 and attempt < 2:  # overloaded: retry after a pause
                time.sleep(10 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None


def call_openai_compat(vendor: str, model: str, system: str, turns: list[str], effort: str = "",
                       images: tuple = (), web: bool = False, member: str = "", prices: dict | None = None) -> dict:
    base, env = VENDORS[vendor]
    key = os.environ.get(env) if env else None
    if env and not key:
        raise RuntimeError(f"no {env} (set it in {ENV_FILE})")
    if web and vendor == "openai":
        return call_openai_responses(model, system, turns, effort, images, key, member, prices)
    if web and vendor != "openrouter":
        raise NoCapability(f"{vendor}: no web search")
    msgs: list[dict] = [{"role": "system", "content": system}]
    tot = {"in": 0, "cached": 0, "out": 0, "reasoning": 0, "cost": 0.0, "cost_note": ""}
    texts, model_id, priced = [], model, True
    for i, t in enumerate(turns):
        content: list | str = t
        if i == 0 and images:
            content = [{"type": "text", "text": t}] + [
                {"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % prep_image(img)}} for img in images]
        msgs.append({"role": "user", "content": content})
        body = {"model": model, "messages": msgs}
        if effort:
            body["reasoning_effort"] = effort
        if vendor == "openrouter":
            body["usage"] = {"include": True}  # exact USD cost in usage.cost
            if web:
                body["plugins"] = [{"id": "web"}]
        d = http_json(f"{base}/chat/completions", key, body)
        u = d.get("usage") or {}
        reply = d["choices"][0]["message"]["content"] or ""
        msgs.append({"role": "assistant", "content": reply})
        texts.append(reply)
        model_id = d.get("model", model)
        c_in, c_out = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        c_cached = u.get("prompt_cache_hit_tokens") or (u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
        cost = u.get("cost")
        if cost is None and prices is not None:
            cost, tot["cost_note"] = price_call(member, c_in, c_cached, c_out, prices)
        priced &= cost is not None
        tot["in"] += c_in; tot["cached"] += c_cached; tot["out"] += c_out; tot["cost"] += cost or 0
        tot["reasoning"] += (u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
    text = texts[0] if len(texts) == 1 else "\n\n".join(f"### Ход {i + 1}\n{t}" for i, t in enumerate(texts))
    return {"text": text, "model_id": model_id, **tot, "cost": tot["cost"] if priced else None}


def call_openai_responses(model, system, turns, effort, images, key, member, prices) -> dict:
    """OpenAI Responses API with the web_search tool ($10 per 1k calls + tokens)."""
    items: list[dict] = []
    tot = {"in": 0, "cached": 0, "out": 0, "reasoning": 0, "cost": 0.0, "cost_note": "web"}
    texts, model_id = [], model
    for i, t in enumerate(turns):
        content = [{"type": "input_text", "text": t}]
        if i == 0:
            content += [{"type": "input_image", "image_url": "data:%s;base64,%s" % prep_image(img)} for img in images]
        items.append({"role": "user", "content": content})
        body = {"model": model, "instructions": system, "input": items, "tools": [{"type": "web_search"}]}
        if effort:
            body["reasoning"] = {"effort": effort}
        d = http_json(f"{VENDORS['openai'][0]}/responses", key, body)
        reply = "".join(c.get("text", "") for o in d.get("output", []) if o.get("type") == "message"
                        for c in o.get("content", []) if c.get("type") == "output_text")
        searches = sum(o.get("type") == "web_search_call" for o in d.get("output", []))
        items.append({"role": "assistant", "content": reply})
        texts.append(reply)
        model_id = d.get("model", model)
        u = d.get("usage") or {}
        c_in, c_out = u.get("input_tokens", 0), u.get("output_tokens", 0)
        c_cached = (u.get("input_tokens_details") or {}).get("cached_tokens") or 0
        cost, _ = price_call(member, c_in, c_cached, c_out, prices) if prices is not None else (None, "")
        tot["in"] += c_in; tot["cached"] += c_cached; tot["out"] += c_out
        tot["reasoning"] += (u.get("output_tokens_details") or {}).get("reasoning_tokens") or 0
        tot["cost"] += (cost or 0) + 0.01 * searches
    text = texts[0] if len(texts) == 1 else "\n\n".join(f"### Ход {i + 1}\n{t}" for i, t in enumerate(texts))
    return {"text": text, "model_id": model_id, **tot}


def load_prices() -> dict:
    return json.loads(PRICES_FILE.read_text()) if PRICES_FILE.exists() else {"models": {}}


def split_member(member: str) -> tuple[str, str, str]:
    """'vendor:model@effort' -> (vendor, model, effort); model may itself contain ':'."""
    vendor, _, rest = member.partition(":")
    model, _, effort = rest.rpartition("@") if "@" in rest else (rest, "", "")
    return vendor, model, effort


def add_openrouter_prices(members: list[str], prices: dict) -> None:
    """Fill prices for openrouter members from the public catalog (USD per token -> per 1M)."""
    wanted = {split_member(m)[1] for m in members if m.startswith("openrouter:")}
    if not wanted:
        return
    for m in http_json(f"{VENDORS['openrouter'][0]}/models", None).get("data", []):
        if m["id"] in wanted:
            pr = m.get("pricing", {})
            f = lambda k: float(pr.get(k) or 0) * 1e6
            OPENROUTER_MODALITIES[m["id"]] = (m.get("architecture") or {}).get("input_modalities") or ["text"]
            prices["models"][f"openrouter:{m['id']}"] = {"in": f("prompt"), "cached": f("input_cache_read") or f("prompt"),
                                                         "out": f("completion")}


def deepseek_offpeak(now: datetime) -> bool:
    bj = now.astimezone(timezone(timedelta(hours=8)))
    return bj.weekday() >= 5 or not (9 <= bj.hour < 12 or 14 <= bj.hour < 18)


def next_offpeak(now: datetime) -> datetime:
    """First minute at or after `now` when DeepSeek off-peak rates apply."""
    t = now.replace(second=0, microsecond=0)
    while not deepseek_offpeak(t):
        t += timedelta(minutes=10 - t.minute % 10)
    return t


def wait_offpeak(members: list[str]) -> None:
    """Sleep until DeepSeek off-peak when any member is a DeepSeek model (bulk jobs: half price)."""
    if not any(m.startswith("deepseek:") for m in members):
        return
    now = datetime.now(timezone.utc)
    t = next_offpeak(now)
    if t > now:
        print(f"waiting for DeepSeek off-peak until {t.astimezone():%Y-%m-%d %H:%M}", file=sys.stderr)
        time.sleep((t - now).total_seconds())


def price_call(member: str, tin: int, cached: int, tout: int, prices: dict, now: datetime | None = None):
    """USD cost and a short note, or (None, '') when the model has no price."""
    p = prices["models"].get(member.split("@")[0])
    if not p:
        return None, ""
    rate, note = [p["in"], p["cached"], p["out"]], ""
    if "long" in p and tin > prices.get("long_context_threshold", 272000):
        rate, note = p["long"], "long ctx"
    if "offpeak" in p and deepseek_offpeak(now or datetime.now(timezone.utc)):
        rate, note = p["offpeak"], "off-peak"
    fx = prices.get("fx_to_usd", {}).get(p.get("currency", "USD"), 1.0)
    return ((tin - cached) * rate[0] + cached * rate[1] + tout * rate[2]) / 1e6 * fx, note


def save_text(path: Path, text: str) -> None:
    """Temp file + fsync + rename: a power cut leaves the old file or the new one, never a torn one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def cache_key(member: str, system: str, turns: list[str], images: tuple, web: bool) -> str:
    imgs = [(str(p), os.path.getmtime(p) if os.path.exists(p) else 0) for p in images]
    return hashlib.sha256(json.dumps([member, system, turns, imgs, web]).encode()).hexdigest()[:32]


def cache_get(key: str) -> dict | None:
    f = ANSWERS / f"{key}.json"
    if RESUME_HOURS <= 0 or not f.exists() or time.time() - f.stat().st_mtime > RESUME_HOURS * 3600:
        return None
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except ValueError:
        return None
    print(f"{d['answer']['member']}: replay of an answer saved {datetime.fromtimestamp(f.stat().st_mtime):%H:%M} "
          "(--fresh asks again)", file=sys.stderr)
    if d.get("ledgered"):  # paid and counted before: free in this run
        return dict(d["answer"], cost=0.0, cost_note="replay", sec=0.0, replay=True)
    return dict(d["answer"], cache=key)  # paid before a crash, never reached the ledger: count it now


def cache_put(key: str, r: dict) -> None:
    save_text(ANSWERS / f"{key}.json", json.dumps({"answer": r, "ledgered": False}, ensure_ascii=False))


def cache_mark(key: str) -> None:
    f = ANSWERS / f"{key}.json"
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    save_text(f, json.dumps(dict(d, ledgered=True), ensure_ascii=False))


def ledger(rows: list[dict], question: str) -> None:
    new = not LEDGER.exists()
    with LEDGER.open("a", encoding="utf-8") as f:
        if new:
            f.write("time\tmember\tmodel_id\tin\tcached\tout\tcost_usd\tnote\tquestion\n")
        for r in rows:
            if "model_id" in r and not r.get("replay"):
                f.write(f"{datetime.now().isoformat(timespec='seconds')}\t{r['member']}\t{r['model_id']}\t{r['in']}\t"
                        f"{r['cached']}\t{r['out']}\t{'' if r['cost'] is None else round(r['cost'], 6)}\t"
                        f"{r['cost_note']}\t{question[:80]}\n")
        f.flush(); os.fsync(f.fileno())
    for r in rows:
        if r.get("cache"):
            cache_mark(r["cache"])


class Blocked(RuntimeError):
    """The packet must not leave Claude / local models."""


def guard(members: list[str], text: str, topic: str, kind: str, allow: bool = False) -> None:
    """Refuse outside vendors for private topics (work), secrets and employer hosts (raw_check patterns)."""
    outside = [m for m in members if split_member(m)[0] not in LOCAL_VENDORS]
    if not outside or allow:
        return
    why = []
    if topic in PRIVATE_TOPICS or kind.split("-")[0] in PRIVATE_TOPICS:
        why.append(f"topic/kind '{topic or kind}' is work data")
    try:
        import raw_check
        hits = raw_check.scan(text, raw_check.load_patterns(None))
    except Exception as e:  # a broken scanner must not silently let data out
        hits = [(0, f"scanner error {e}")]
    if hits:
        kinds = sorted({k for _, k in hits})
        why.append(f"{len(hits)} secret/internal hits ({', '.join(kinds)})")
    if why:
        raise Blocked(f"blocked for {', '.join(outside)}: {'; '.join(why)}. Use claude:/ollama: members, "
                      "redact the packet, or --allow-external if the operator agreed")


def journal_read() -> list[dict]:
    if not JOURNAL.exists():
        return []
    lines = JOURNAL.read_text(encoding="utf-8").splitlines()[1:]
    return [dict(zip(JOURNAL_COLS, ln.split("\t"))) for ln in lines if ln.strip()]


def journal_write(rows: list[dict]) -> None:
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    clean = lambda v: str(v).replace("\t", " ").replace("\n", " ")
    save_text(JOURNAL, "\t".join(JOURNAL_COLS) + "\n" + "".join(
        "\t".join(clean(r.get(c, "")) for c in JOURNAL_COLS) + "\n" for r in rows))


def journal_add(mode: str, members: list[str], paid: float, question: str, kind: str = "", topic: str = "",
                signal: str = "", run: str = "") -> str:
    rows = journal_read()
    run = run or new_run()
    rows.append({"run": run, "time": datetime.now().isoformat(timespec="seconds"), "mode": mode, "kind": kind,
                 "topic": topic, "members": ",".join(members), "paid_usd": f"{paid:.6f}", "signal": signal,
                 "question": question[:120]})
    journal_write(rows)
    return run


def new_run() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def guess_kind(question: str) -> str:
    q = question.lower()
    return next((k for k, rx, _ in ROUTES if re.search(rx, q)), "general")


def guess_topic(files: list[Path]) -> str:
    for f in files:
        m = re.search(r"topics/([^/]+)/", str(f.resolve()))
        if m:
            return m.group(1)
    m = re.search(r"topics/([^/]+)", os.getcwd())
    return m.group(1) if m else ""


def parse_scores(text: str) -> dict[str, float]:
    m = re.search(r"SCORES\s*(\{.*?\})", text or "", re.S)
    try:
        return {k: float(v) for k, v in json.loads(m.group(1)).items()} if m else {}
    except (ValueError, TypeError):
        return {}


def stats_read() -> list[dict]:
    if not STATS.exists():
        return []
    return [dict(zip(STATS_COLS, ln.split("\t"))) for ln in STATS.read_text(encoding="utf-8").splitlines()[1:] if ln.strip()]


def stats_write(rows: list[dict]) -> None:
    STATS.parent.mkdir(parents=True, exist_ok=True)
    save_text(STATS, "\t".join(STATS_COLS) + "\n" + "".join(
        "\t".join(str(r.get(c, "")).replace("\t", " ") for c in STATS_COLS) + "\n" for r in rows))


def stats_add(run: str, source: str, kind: str, topic: str, scored: dict[str, float], costs: dict, web: bool) -> None:
    """scored: member -> score 0-10 for one task; the top score is marked best."""
    if not scored:
        return
    top = max(scored.values())
    now = datetime.now().isoformat(timespec="seconds")
    stats_write(stats_read() + [{"time": now, "run": run, "source": source, "kind": kind, "topic": topic, "member": m,
                                 "score": f"{v:.2f}", "best": int(v == top), "web": int(web),
                                 "cost_usd": "" if costs.get(m) is None else f"{costs[m]:.6f}"}
                                for m, v in scored.items()])


def learned(kind: str = "", topic: str = "") -> dict[str, dict]:
    """member -> n, mean score, wins, mean paid cost over stats rows of this kind (or topic)."""
    agg: dict[str, dict] = {}
    for r in stats_read():
        if (kind and r["kind"] != kind) or (topic and r["topic"] != topic):
            continue
        a = agg.setdefault(r["member"], {"n": 0, "sum": 0.0, "wins": 0, "cost": [], "web": 0})
        a["n"] += 1; a["sum"] += float(r["score"]); a["wins"] += int(r["best"] or 0); a["web"] += int(r["web"] or 0)
        if r["cost_usd"] and not r["member"].startswith("claude:"):
            a["cost"].append(float(r["cost_usd"]))
    for a in agg.values():
        a["mean"] = a["sum"] / a["n"]
        a["avg_cost"] = sum(a["cost"]) / len(a["cost"]) if a["cost"] else 0.0
        a["max_cost"] = max(a["cost"], default=0.0)
    return agg


def print_learned(kind: str = "") -> None:
    rows, jr = stats_read(), journal_read()
    kinds = [kind] if kind else sorted({r["kind"] for r in rows} | {r.get("kind", "") for r in jr} - {""})
    if not kinds:
        print(f"no stats yet ({STATS})"); return
    for k in kinds:
        js = [r for r in jr if r.get("kind") == k and r.get("mark")]
        useful = sum(r["mark"] in ("decision", "error") for r in js)
        print(f"## {k}: journal {useful}/{len(js)} useful" if js else f"## {k}: no journal marks yet")
        for m, a in sorted(learned(k).items(), key=lambda kv: -kv[1]["mean"]):
            cost = "subscription" if m.startswith("claude:") else f"${a['avg_cost']:.4f}/task"
            print(f"  {m:40} n={a['n']:<3} score {a['mean']:4.1f}  wins {a['wins']:<2} {cost}")


def journal_mark(run: str, mark: str, note: str, by: str = "operator") -> int:
    rows = journal_read()
    hit = [r for r in rows if r["run"] == run] if run != "last" else rows[-1:]
    if not hit:
        print(f"no run {run} in {JOURNAL}", file=sys.stderr); return 1
    hit[0]["mark"], hit[0]["note"], hit[0]["by"] = mark, note, by
    journal_write(rows)
    print(f"{hit[0]['run']} ({hit[0]['mode']}): {mark} — {hit[0]['question'][:70]}")
    return 0


def journal_summary() -> None:
    rows = journal_read()
    if not rows:
        print(f"journal is empty ({JOURNAL})"); return
    print("mode       runs marked decision error nothing useful%  paid$   $/insight")
    for mode in sorted({r["mode"] for r in rows}) + ["ALL"]:
        rs = [r for r in rows if mode in ("ALL", r["mode"])]
        n = {k: sum(r.get("mark") == k for r in rs) for k in MARKS}
        marked, useful = sum(n.values()), n["decision"] + n["error"]
        paid = sum(float(r["paid_usd"] or 0) for r in rs)
        pct = f"{100 * useful / marked:.0f}%" if marked else "—"
        per = f"${paid / useful:.4f}" if useful else "—"
        print(f"{mode:10} {len(rs):4} {marked:6} {n['decision']:8} {n['error']:5} {n['nothing']:7} {pct:>7} "
              f"{paid:7.4f}   {per}")
    todo = [r for r in rows if not r.get("mark")]
    if todo:
        print(f"\nunmarked ({len(todo)}): council.py --mark RUN decision|error|nothing")
        for r in todo[-10:]:
            print(f"  {r['run']} {r['mode']:8} ${float(r['paid_usd'] or 0):.4f} {r['question'][:70]}")


def route(question: str, kind: str = "", topic: str = "") -> None:
    """Advice only, from learned stats: is a paid member measurably better than Claude for this kind?"""
    kind = kind or guess_kind(question)
    note = next((n for k, _, n in ROUTES if k == kind and n), "")
    stats = learned(kind) or (learned(topic=topic) if topic else {})
    print(f"type: {kind}" + (f" · topic: {topic}" if topic else "") + (f"\nnote: {note}" if note else ""))
    if topic in PRIVATE_TOPICS or kind.split("-")[0] in PRIVATE_TOPICS:
        print("private: work data — only claude: or ollama: members; outside vendors are blocked"); return
    solid = {m: a for m, a in stats.items() if a["n"] >= MIN_N}
    if not solid:
        print(f"learned: too few observations (need {MIN_N} per member); default: {ROUTE_DEFAULT}"); return
    top = sorted(solid.items(), key=lambda kv: -kv[1]["mean"])[:5]
    print("learned: " + "; ".join(f"{m} {a['mean']:.1f} (n={a['n']})" for m, a in top))
    claude = max((a["mean"] for m, a in solid.items() if m.startswith("claude:")), default=0.0)
    paid = [(m, a) for m, a in solid.items() if not m.startswith("claude:") and a["mean"] >= claude + 1.0]
    if not paid:
        print(f"advice: Claude ({claude:.1f}) is not beaten by >=1 point; {ROUTE_DEFAULT}"); return
    m, a = max(paid, key=lambda kv: (kv[1]["mean"] - claude) / max(kv[1]["avg_cost"], 0.001))
    web = a["web"] * 2 >= a["n"]
    hi = max(a["max_cost"], 0.01)
    print(f"offer: {m}{' + web' if web else ''}: {a['mean']:.1f} vs Claude {claude:.1f}, ≈${a['avg_cost']:.2f} per question "
          f"(max seen ${hi:.2f}); ask the operator before spending")
    print(f"command: council.py -q {json.dumps(question, ensure_ascii=False)} --kind {kind} --models {m} "
          f"--judge none {'--web ' if web else ''}--max-usd {hi:.2f}")
    cheaper = [(x, b) for x, b in solid.items() if not x.startswith("claude:") and x != m
               and b["avg_cost"] < a["avg_cost"] and b["mean"] > claude]
    if cheaper:
        x, b = max(cheaper, key=lambda kv: kv[1]["mean"])
        print(f"cheaper: {x}: {b['mean']:.1f} for ≈${b['avg_cost']:.2f}")


def print_prices(prices: dict) -> None:
    fx = prices.get("fx_to_usd", {})
    print(f"as of {prices.get('as_of')}, USD per 1M tokens (miss / hit / out); CNY->USD {fx.get('CNY')} ({fx.get('as_of')})")
    for m, p in sorted(prices["models"].items(), key=lambda kv: kv[1]["out"] * fx.get(kv[1].get("currency", "USD"), 1)):
        k = fx.get(p.get("currency", "USD"), 1.0)
        line = f"{m:32} {p['in'] * k:8.3f} {p['cached'] * k:8.4f} {p['out'] * k:8.3f}"
        if "offpeak" in p:
            line += "   off-peak " + " / ".join(f"{x * k:.4g}" for x in p["offpeak"])
        if "long" in p:
            line += "   >272K " + " / ".join(f"{x:g}" for x in p["long"])
        print(line)


def ask(member: str, system: str, prompt: str, prices: dict, images: tuple = (), web: bool = False,
        turns: list[str] | None = None) -> dict:
    """One member answers: prompt (+ images) and optional follow-up user turns; web = search allowed."""
    vendor, model, effort = split_member(member)
    t0 = time.time()
    all_turns = [prompt] + list(turns or [])
    key = cache_key(member, system, all_turns, images, web)
    hit = cache_get(key)
    if hit:
        return hit
    try:
        if images and not capable(member, "image"):
            raise NoCapability(f"{member}: no image input")
        if web and not capable(member, "web"):
            raise NoCapability(f"{member}: no web search")
        r = (call_claude(model, system, all_turns, effort, images, web) if vendor == "claude"
             else call_openai_compat(vendor, model, system, all_turns, effort, images, web, member, prices))
    except NoCapability as e:
        return {"member": member, "skip": str(e), "sec": 0.0}
    except Exception as e:  # one failed member must not sink the council
        return {"member": member, "error": str(e)[:500], "sec": round(time.time() - t0, 1)}
    if r["cost"] is None and vendor == "gemini":
        r["cost_note"] = "free tier?"  # direct key: free quota, no price table
    out = {"member": member, "sec": round(time.time() - t0, 1), **r}
    cache_put(key, out)
    return dict(out, cache=key)


def list_models(vendors: list[str], grep: str = "") -> None:
    print("claude: haiku, sonnet, opus (aliases of `claude -p --model`; subscription)")
    for v in vendors or list(VENDORS):
        base, env = VENDORS[v]
        key = os.environ.get(env) if env else None
        if env and not key:
            print(f"{v}: no {env}"); continue
        try:
            ids = sorted(m["id"].removeprefix("models/") for m in http_json(f"{base}/models", key).get("data", []))
            chat = [i for i in ids if not re.search(NOT_CHAT, i) and re.search(grep, i, re.I)
                    and not (v == "openai" and re.search(DATED, i))]
            print(f"{v}: {len(ids)} models, {len(chat)} chat: " + ", ".join(chat))
        except Exception as e:
            print(f"{v}: error {str(e)[:200]}")


def packet(question: str, goal: str, files: list[Path]) -> str:
    parts = [f"# Question\n{question}"]
    if goal:
        parts.append(f"# Asker's goal and constraints\n{goal}")
    for f in files:
        parts.append(f"# Knowledge: {f}\n{f.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def money(x) -> str:
    return "n/a" if x is None else f"${x:.4f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", nargs="*", metavar="VENDOR")
    ap.add_argument("--prices", action="store_true", help="print the price table and exit")
    ap.add_argument("--grep", default="", help="regex filter for --list")
    ap.add_argument("-q", "--question")
    ap.add_argument("--goal", default="")
    ap.add_argument("--context", nargs="*", type=Path, default=[])
    ap.add_argument("--preset", choices=PRESETS, default=DEFAULT_PRESET,
                    help="members+judge: cheap, balanced (default), deep, private; --models/--judge override")
    ap.add_argument("--models")
    ap.add_argument("--judge", help="VENDOR:MODEL, or none")
    ap.add_argument("--max-usd", type=float, default=0.50, help="abort if the priced estimate exceeds this")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="ask again instead of replaying saved answers")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--web", action="store_true", help="let members search the web (claude, openai, openrouter)")
    ap.add_argument("--mode", choices=["compare", "ensemble"], default="compare",
                    help="compare: answers + blind judge; ensemble: hypotheses -> critique (judge) -> synthesis")
    ap.add_argument("--synth", default="claude:opus", help="ensemble synthesizer (default: Claude on the subscription)")
    ap.add_argument("--verify", metavar="ANSWER", help="second-pass check of a file ('-' = stdin) against --context")
    ap.add_argument("--verifier", default="deepseek:deepseek-flash,openai:gpt-6-luna",
                    help="verify: first member that answers wins (cross-family to Claude)")
    ap.add_argument("--route", action="store_true", help="advice only: task type, paid option with price, command")
    ap.add_argument("--mark", nargs="+", metavar="ARG", help="[RUN] decision|error|nothing (RUN default: last)")
    ap.add_argument("--note", default="", help="note for --mark")
    ap.add_argument("--journal", action="store_true", help="usefulness summary and cost per insight")
    ap.add_argument("--learn", action="store_true", help="learned scores per task kind and member")
    ap.add_argument("--kind", default="", help="task kind for stats (free text, e.g. the project); default: guessed")
    ap.add_argument("--topic", default="", help="wiki topic for stats; default: from --context paths")
    ap.add_argument("--by", default="operator", help="who set --mark: operator or claude")
    ap.add_argument("--allow-external", action="store_true",
                    help="send work data / packets with secret hits to outside vendors (operator's explicit OK only)")
    a = ap.parse_args()
    if a.fresh:
        global RESUME_HOURS
        RESUME_HOURS = 0
    load_env()
    if a.list is not None:
        list_models(a.list, a.grep); return 0
    if a.journal:
        journal_summary(); return 0
    if a.learn:
        print_learned(a.kind); return 0
    if a.mark:
        run, mark = (["last"] + a.mark)[-2:]
        if mark not in MARKS:
            ap.error(f"mark must be one of {', '.join(MARKS)}")
        return journal_mark(run, mark, a.note, a.by)
    prices = load_prices()
    if a.prices:
        print_prices(prices); return 0
    if a.route:
        if not a.question:
            ap.error("--route needs -q")
        route(a.question, a.kind, a.topic or guess_topic(a.context)); return 0
    a.topic = a.topic or guess_topic(a.context)
    if a.verify:
        a.kind = a.kind or (guess_kind(a.question) if a.question else "verify")
        return verify(a, prices)
    if not a.question:
        ap.error("-q is required")
    a.kind = a.kind or guess_kind(a.question)
    # ensemble defaults to cheap hypothesis makers and a cheap critic; the synthesizer is Claude
    preset = "cheap" if a.mode == "ensemble" and a.preset == DEFAULT_PRESET else a.preset
    a.models = a.models or PRESETS[preset][0]
    a.judge = a.judge or PRESETS[preset][1]
    members = [m.strip() for m in a.models.split(",") if m.strip()]
    extra = [a.judge] + ([a.synth] if a.mode == "ensemble" else [])
    add_openrouter_prices(members + extra, prices)
    prompt = packet(a.question, a.goal, a.context)
    est_in = tokens_estimate(prompt)
    # web search pulls in pages: bench v3 web tasks averaged ~40-110K input tokens per member
    est = sum(price_call(m, max(est_in, 80000) if a.web else est_in, 0, 2000, prices)[0] or 0 for m in members)
    if a.mode == "ensemble" or a.judge != "none":
        # judge / critic output is mostly reasoning: ~5-6K tokens in the ensemble test of 2026-10-26
        est += sum(price_call(m, est_in + 2000 * len(members), 0, 6000, prices)[0] or 0
                   for m in extra if m != "none")
    print(f"packet ≈{est_in} tokens, {len(members)} members, mode {a.mode}, priced estimate ≈${est:.4f} "
          f"(claude: subscription)", file=sys.stderr)
    try:
        guard(members + extra, prompt, a.topic, a.kind, a.allow_external)
    except Blocked as e:
        print(f"abort: {e}", file=sys.stderr); return 3
    if a.dry_run:
        return 0
    if est > a.max_usd:
        print(f"abort: estimate ${est:.4f} > --max-usd {a.max_usd}", file=sys.stderr); return 2
    with cf.ThreadPoolExecutor(len(members)) as ex:
        answers = list(ex.map(lambda m: ask(m, HYPO if a.mode == "ensemble" else EXPERT, prompt, prices, web=a.web),
                              members))
    ok = [r for r in answers if "error" not in r and "skip" not in r]
    labels, extra_rows, sections = {}, [], []
    order = ok[:]
    random.Random(a.seed).shuffle(order)
    tag = "H" if a.mode == "ensemble" else "Answer "
    labels = {f"{tag}{i + 1}": r["member"] for i, r in enumerate(order)}
    blind = "\n\n".join(f"## {k}\n{r['text']}" for k, r in zip(labels, order))
    if a.mode == "ensemble" and ok:
        critique = ask(a.judge, CRITIC, f"{prompt}\n\n# Hypotheses\n{blind}", prices) if a.judge != "none" else None
        crit_text = critique["text"] if critique and "text" in critique else "(no critique)"
        synth = ask(a.synth, SYNTH, f"{prompt}\n\n# Hypotheses\n{blind}\n\n# Critique\n{crit_text}", prices)
        extra_rows = ([dict(critique, member=f"critic {critique['member']}")] if critique else []) + \
            [dict(synth, member=f"synth {synth['member']}")]
        sections = [("Synthesis", synth), ("Critique (critic saw anonymous hypotheses)", critique)]
    elif a.judge != "none" and len(ok) >= 2:
        verdict = ask(a.judge, JUDGE, f"{prompt}\n\n# Answers\n{blind}", prices)
        extra_rows = [dict(verdict, member=f"judge {verdict['member']}")]
        sections = [("Verdict (judge saw anonymous answers)", verdict)]
    rows = answers + extra_rows
    total = sum(r.get("cost") or 0 for r in rows)
    run = new_run()
    graded = extra_rows[0] if extra_rows and (a.mode == "compare" or len(extra_rows) == 2) else None
    raw = parse_scores(graded.get("text", "")) if graded else {}
    scale = 2.0 if a.mode == "ensemble" else 1 / 3  # plausibility 1-5 or total of 30 -> 0-10
    stats_add(run, f"council:{a.mode}", a.kind, a.topic, {labels[k]: v * scale for k, v in raw.items() if k in labels},
              {r["member"]: r.get("cost") for r in ok}, a.web)
    roles = f"critic: {a.judge} · synth: {a.synth}" if a.mode == "ensemble" else f"judge: {a.judge}"
    out = [f"# Council: {a.question[:80]}", "",
           f"Date: {date.today().isoformat()} · script: council.py · mode: {a.mode} · kind: {a.kind} · {roles} · web: {a.web} · "
           "blind order: " + (", ".join(f"{k}={v}" for k, v in labels.items()) or "—"), "",
           *usage_table(rows)]
    paid = sum(r.get("cost") or 0 for r in rows if r.get("cost_note") != "subscription")
    journal_add(a.mode, members, paid, a.question, a.kind, a.topic, f"scored {len(raw)}/{len(labels)}", run)
    out += ["", f"API cost (paid): {money(paid)} · total incl. notional Claude: {money(total)} · run: {run}", ""]
    ledger(rows, a.question)
    print(f"API cost (paid): {money(paid)} · total incl. notional Claude: {money(total)} · ledger: {LEDGER}", file=sys.stderr)
    for title, r in sections:
        if r and "error" not in r:
            out += [f"# {title}", "", r["text"], ""]
    for r in ok:
        out += [f"# {'Hypotheses' if a.mode == 'ensemble' else 'Answer'}: {r['member']}", "", r["text"], ""]
    emit(a.out, "\n".join(out), run)
    return 0 if ok else 1


def usage_table(rows: list[dict]) -> list[str]:
    out = ["| member | model id | in | cached | out | of it reasoning | cost | sec |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if "error" in r or "skip" in r:
            out.append(f"| {r['member']} | {'ERROR: ' + r['error'][:120] if 'error' in r else 'skip: ' + r['skip']} | | | | | | {r['sec']} |")
        else:
            out.append(f"| {r['member']} | {r['model_id']} | {r['in']} | {r['cached']} | {r['out']} | {r['reasoning'] or ''} "
                       f"| {money(r['cost'])} {r['cost_note']} | {r['sec']} |")
    return out


def emit(path: Path | None, report: str, run: str) -> None:
    if path:
        save_text(path, report); print(f"wrote {path}", file=sys.stderr)
    else:
        print(report)
    print(f"run {run}: after reading, mark it: council.py --mark {run} decision|error|nothing", file=sys.stderr)


def verify(a, prices: dict) -> int:
    """Second pass: a cross-family model looks for unsupported claims, gaps and contradictions."""
    text = sys.stdin.read() if a.verify == "-" else Path(a.verify).read_text(encoding="utf-8")
    parts = ([f"# Question\n{a.question}"] if a.question else []) + ([f"# Asker's goal\n{a.goal}"] if a.goal else [])
    parts += [f"# Source: {f}\n{f.read_text(encoding='utf-8')}" for f in a.context]
    body = "\n\n".join(parts + [f"# Answer to check\n{text}"])
    verifiers = [m.strip() for m in a.verifier.split(",") if m.strip()]
    add_openrouter_prices(verifiers, prices)
    est = price_call(verifiers[0], tokens_estimate(body), 0, 12000, prices)[0] or 0  # mostly reasoning
    print(f"verify packet ≈{tokens_estimate(body)} tokens, {verifiers[0]} ≈${est:.4f}", file=sys.stderr)
    try:
        guard(verifiers, body, a.topic, a.kind, a.allow_external)
    except Blocked as e:
        print(f"abort: {e}", file=sys.stderr); return 3
    if a.dry_run:
        return 0
    if est > a.max_usd:
        print(f"abort: estimate ${est:.4f} > --max-usd {a.max_usd}", file=sys.stderr); return 2
    rows = []
    for m in verifiers:
        rows.append(ask(m, VERIFY, body, prices))
        if "text" in rows[-1]:
            break
    ledger(rows, "verify: " + (a.question or a.verify))
    paid = sum(r.get("cost") or 0 for r in rows if r.get("cost_note") != "subscription")
    vd = re.search(r"##\s*Verdict\s*\n+\W*(ok|minor|major)", rows[-1].get("text", ""), re.I)
    run = journal_add("verify", [rows[-1]["member"]], paid, a.question or f"verify {a.verify}", a.kind, a.topic,
                      vd.group(1).lower() if vd else "")
    out = [f"# Verify: {a.question[:80] if a.question else a.verify}", "",
           f"Date: {date.today().isoformat()} · script: council.py --verify · sources: {len(a.context)}", "",
           *usage_table(rows), "", f"API cost (paid): {money(paid)} · run: {run}", ""]
    if "text" in rows[-1]:
        out += [rows[-1]["text"], ""]
    emit(a.out, "\n".join(out), run)
    return 0 if "text" in rows[-1] else 1

if __name__ == "__main__":
    sys.exit(main())
