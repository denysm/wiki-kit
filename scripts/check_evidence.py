"""Deterministic grounding and link check for llm-wiki roots.

Usage: check_evidence.py [--strict] [--json] [--no-coverage] <wiki_root> [...]

Runs the mechanical half of the CLAUDE.md "Sources" rule so a model reads only
the flagged lines. For every article in <root>/wiki/ (index files skipped):
- sources: every path in frontmatter exists (a missing *.local.md is only a
  warning: it is expected on a clone) and is listed in the `## Sources`
  section, and the other way round.
- links: every relative markdown link resolves to a file; every [[wikilink]]
  slug names an article or a raw file of the same root.
- grounding: every number (2+ digits or decimal) and ISO date, and every quoted
  phrase of 20+ characters, in the body (not in frontmatter, `## Sources`,
  `## See Also`, links or code spans) appears word for word in the raw files
  the article cites. A number the article derived itself (a sum, a ratio) is
  reported too: that is a judgement for the reader, so it is a warning.
- coverage: every raw file is cited by an article or named in
  wiki/references/uncompiled-source-coverage.md (skip with --no-coverage).
Findings print as path:line: severity rule: excerpt. Errors (missing source,
broken link) exit 1; --strict makes ungrounded values errors too.
"""
import argparse, json, os, re, sys

SKIP_SECTIONS = {"sources", "see also"}
NUM = re.compile(r"(?<![\w./:#-])(\d{1,3}(?:,\d{3})+|\d+(?:[.,]\d+)?)(?![\w-]*[/\\])")
ISO = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
QUOTE = re.compile(r"“([^“”\n]{20,}?)”|(?<![\w*])\"([^\"\n]{20,}?)\"(?![\w])")
MDLINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
CODE = re.compile(r"`[^`\n]*`")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text, 0
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text, 0
    fm_text = text[4:end]
    body = text[end + 4:].lstrip("\n")
    offset = text[: len(text) - len(body)].count("\n")
    return parse_fm(fm_text), body, offset


def parse_fm(fm_text):
    fm, key = {}, None
    for line in fm_text.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            elif val:
                fm[key] = val.strip("'\"")
            else:
                fm[key] = []
        elif key and line.strip().startswith("- ") and isinstance(fm.get(key), list):
            fm[key].append(line.strip()[2:].strip().strip("'\""))
    return fm


def norm_text(s):
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).lower()


def norm_numbers(s):
    return re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)


def num_in(raw_numbers_text, token):
    t = norm_numbers(token)
    variants = {t, t.replace(".", ","), t.replace(",", ".")}
    if t.isdigit() and len(t) > 3:
        variants |= {f"{int(t) // 1000}k" if int(t) % 1000 == 0 else t, f"{int(t):,}".replace(",", " ")}
    return any(re.search(r"(?<![\d.,])" + re.escape(v) + r"(?![\d]|[.,]\d)", raw_numbers_text) for v in variants)


def sections(body):
    """Yield (line_no, section_name_lower, line) for body lines."""
    name = ""
    for i, line in enumerate(body.splitlines(), 1):
        h = re.match(r"^#{1,6}\s+(.*?)\s*$", line)
        if h:
            name = h.group(1).lower()
        yield i, name, line


def check_article(root, path, findings, slugs, strict):
    rel = os.path.relpath(path, root)

    def add(line, sev, rule, msg):
        findings.append({"file": rel, "line": line, "severity": sev, "rule": rule, "msg": msg})

    text = open(path, encoding="utf-8", errors="replace").read()
    fm, body, off = split_frontmatter(text)
    srcs = fm.get("sources") or []
    if isinstance(srcs, str):
        srcs = [srcs]

    raw_texts, unverifiable = [], 0
    for s in srcs:
        p = os.path.join(root, s)
        if os.path.isfile(p):
            raw_texts.append(open(p, encoding="utf-8", errors="replace").read())
        elif s.endswith(".local.md"):
            unverifiable += 1
            add(1, "warn", "source-missing-local", s)
        else:
            add(1, "error", "source-missing", s)
    if not srcs:
        add(1, "error", "no-sources", "frontmatter has no sources")

    # ## Sources section vs frontmatter
    sec_links = set()
    for _, name, line in sections(body):
        if name == "sources":
            for m in MDLINK.finditer(line):
                sec_links.add(os.path.normpath(os.path.join(os.path.dirname(path), m.group(1).split("#")[0])))
    fm_abs = {os.path.normpath(os.path.join(root, s)) for s in srcs}
    for s in sorted(set() if os.path.basename(path) == "uncompiled-source-coverage.md" else fm_abs - sec_links):
        add(1, "warn", "source-not-in-section", os.path.relpath(s, root))
    for s in sorted(sec_links - fm_abs):
        if os.sep + "raw" + os.sep in s:
            add(1, "warn", "section-source-not-in-frontmatter", os.path.relpath(s, root))

    raw_all = norm_text("\n".join(raw_texts))
    raw_nums = norm_numbers(raw_all)
    can_ground = bool(raw_texts) and unverifiable == 0

    for ln, name, line in sections(body):
        fl = ln + off
        for m in MDLINK.finditer(line):
            tgt = m.group(1)
            if re.match(r"^(https?:|mailto:|#)", tgt):
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(path), tgt.split("#")[0]))
            if not os.path.exists(p):
                if p.endswith(".local.md"):
                    add(fl, "warn", "link-missing-local", tgt)
                else:
                    add(fl, "error", "broken-link", tgt)
        for m in WIKILINK.finditer(CODE.sub(" ", line)):
            if m.group(1).strip().rstrip("\\") not in slugs:
                add(fl, "error", "broken-wikilink", m.group(1))

        if name in SKIP_SECTIONS or not can_ground:
            continue
        plain = MDLINK.sub(" ", WIKILINK.sub(" ", line))
        plain = re.sub(r"^\s*(\d+[.)]|[-*]|>)\s+", "", plain)
        quotes = [a or b for a, b in QUOTE.findall(plain.replace("**", ""))]
        for q in quotes:
            if norm_text(q) not in raw_all:
                add(fl, "warn" if not strict else "error", "quote-not-in-sources", q[:80])
        plain = QUOTE.sub(" ", plain)
        for d in ISO.findall(CODE.sub(" ", plain)):
            if d not in raw_all:
                add(fl, "warn" if not strict else "error", "date-not-in-sources", d)
        plain = ISO.sub(" ", CODE.sub(" ", plain))
        seen = set()
        for m in NUM.finditer(plain):
            tok = m.group(1)
            digits = re.sub(r"\D", "", tok)
            if tok in seen or (len(digits) < 2 and "." not in tok and "," not in tok):
                continue
            if re.fullmatch(r"(19|20)\d\d", tok):
                continue
            seen.add(tok)
            if not num_in(raw_nums, tok):
                add(fl, "warn" if not strict else "error", "number-not-in-sources", tok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-coverage", action="store_true")
    a = ap.parse_args()

    findings, n_articles = [], 0
    for root in a.roots:
        root = os.path.abspath(root)
        wiki = os.path.join(root, "wiki")
        if not os.path.isdir(wiki):
            print(f"{root}: no wiki/ directory", file=sys.stderr)
            return 2
        arts = []
        for dp, _, fns in os.walk(wiki):
            for fn in fns:
                if fn.endswith(".md") and not fn.startswith("_"):
                    arts.append(os.path.join(dp, fn))
        slugs = {os.path.splitext(os.path.basename(p))[0] for p in arts}
        raw_dir = os.path.join(root, "raw")
        raws = []
        for dp, _, fns in os.walk(raw_dir):
            for fn in fns:
                if fn.endswith(".md") and not fn.startswith("_"):
                    raws.append(os.path.join(dp, fn))
                    slugs.add(os.path.splitext(fn)[0])
        cited = set()
        for p in sorted(arts):
            n_articles += 1
            check_article(root, p, findings, slugs, a.strict)
            fm, _, _ = split_frontmatter(open(p, encoding="utf-8", errors="replace").read())
            for s in fm.get("sources") or []:
                cited.add(os.path.normpath(os.path.join(root, s)))
        if not a.no_coverage:
            cov = os.path.join(wiki, "references", "uncompiled-source-coverage.md")
            cov_text = open(cov, encoding="utf-8", errors="replace").read() if os.path.isfile(cov) else ""
            for r in sorted(raws):
                if os.path.normpath(r) not in cited and os.path.basename(r) not in cov_text:
                    findings.append({"file": os.path.relpath(r, root), "line": 1, "severity": "warn",
                                     "rule": "raw-not-cited", "msg": "cited by no article and not in uncompiled-source-coverage.md"})

    findings.sort(key=lambda f: (f["severity"] != "error", f["file"], f["line"]))
    errors = sum(f["severity"] == "error" for f in findings)
    warns = len(findings) - errors
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=1))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line']}: {f['severity']} {f['rule']}: {f['msg']}")
        print(f"check_evidence: {n_articles} articles, {errors} errors, {warns} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
