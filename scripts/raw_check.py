#!/usr/bin/env python3
"""Scan text for secrets and internal URLs; optionally replace them with [REDACTED:secret].

Usage:
  raw_check.py PATH...                 # report only, exit 1 if anything found
  raw_check.py --fix PATH...           # rewrite files in place, print counts
  raw_check.py --patterns FILE PATH... # extra internal hosts/regexes
  raw_check.py --hosts PATH...         # list URL hosts by frequency, to build the patterns file
  raw_check.py --wiki [--names FILE] ROOT...  # also check wiki structure (see below)

PATH may be a file or a directory (recursed for text files). Matched values are
never printed, only kind and line number. Files under a `raw/` directory are
reported but never rewritten: raw/ is immutable, a hit there needs a human.

Extra patterns (one per line, `#` comments): a plain host such as `corp.example.com`
matches that host and its subdomains; a line starting with `re:` is a regex.
Default files: ~/.config/wiki-kit/internal-domains.txt, then the older
~/.config/llm-wiki/raw_check_patterns.txt (kept outside any repo, because
employer domains are themselves confidential).

--wiki adds the structural rules of a wiki root, printed as
`path:line: severity rule: excerpt`:
- raw/ files carry title, source, type, ingested, authors, source_date (warning);
- a copy of a corporate system (Jira, Confluence, SharePoint, mail, Teams,
  transcript) in raw/ is named *.local.md (error);
- internal URLs and hosts in raw/*.local.md are expected there and not counted
  (secrets still are);
- --names FILE (one customer/prospect name per line): a file that mentions one
  carries `sensitivity: confidential` (warning).
"""
from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from collections import Counter
from pathlib import Path

MARK = "[REDACTED:secret]"
DEFAULT_PATTERNS = [Path.home() / ".config/wiki-kit/internal-domains.txt",
                    Path.home() / ".config/llm-wiki/raw_check_patterns.txt"]
TEXT_EXT = {".md", ".txt", ".json", ".yaml", ".yml", ".html", ".htm", ".csv", ".tsv", ".xml"}

# (kind, regex, group to replace: 0 = whole match)
SECRET_PATTERNS: list[tuple[str, re.Pattern, int]] = [
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), 0),
    ("aws-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), 0),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b"), 0),
    ("api-key", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}"), 0),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), 0),
    ("google-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), 0),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), 0),
    ("bearer", re.compile(r"(?i)\bbearer\s+(?!\[REDACTED)([A-Za-z0-9._~+/-]{20,}=*)"), 1),
    ("assignment", re.compile(
        r"(?i)\b(?:password|passwd|pwd|passcode|secret|api[_-]?key|access[_-]?key|client[_-]?secret|auth[_-]?token|"
        r"пароль)\b[\"']?\s*[:=]\s*[\"']?(?!\[REDACTED)([^\s\"',;<>]{6,})"), 1),
    # Infrastructure identifiers: not secrets, but they map the employer's systems.
    ("s3-bucket", re.compile(r"\bs3://[\w.-]+"), 0),
    ("aws-arn", re.compile(r"\barn:aws[\w-]*:[\w-]+:[^\s\"'`)\]]*"), 0),
    ("aws-account-id", re.compile(r"(?i)\baccount(?:\s*id)?\s*[:=#]?\s*(\d{12})\b"), 1),
    ("ec2-instance", re.compile(r"\bi-[0-9a-f]{8,17}\b"), 0),
    ("meeting-id", re.compile(r"(?i)\bmeeting id\s*[:#]?\s*(\d[\d ]{6,}\d)"), 1),
]
INTERNAL_KINDS = {"internal-url", "internal-host", "private-ip", "s3-bucket", "aws-arn", "aws-account-id",
                  "ec2-instance", "meeting-id"}

URL_RE = re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s<>\"'`)\]}]+", re.I)
HOST_RE = re.compile(r"^[a-z][a-z0-9+.-]*://(?:([^/@\s]*)@)?([^/:?#\s]+)", re.I)
PRIVATE_IP_RE = re.compile(r"(?<![\d.])(?:10|127|192\.168|172\.(?:1[6-9]|2\d|3[01]))(?:\.\d{1,3}){1,3}(?![\d.])")

# Hosts that are internal by construction or are per-company tenants of enterprise SaaS.
INTERNAL_SUFFIXES = (
    ".local", ".lan", ".internal", ".corp", ".intranet", ".intra", ".localdomain", ".home.arpa",
    ".sharepoint.com", ".atlassian.net", ".slack.com", ".service-now.com", ".okta.com",
    ".my.salesforce.com", ".lightning.force.com", ".awsapps.com", ".myworkday.com",
)
INTERNAL_HOSTS = {"localhost", "teams.microsoft.com", "dev.azure.com", "app.slack.com"}
# Self-hosted tooling on a company domain: jira.acme.com, but not the public gitlab.com.
INTERNAL_LABELS = re.compile(r"^(?:[\w-]+\.)*(?:intranet|internal|jira|confluence|gitlab|jenkins|grafana|kibana|vpn)\.[\w-]+\.[\w.-]+$", re.I)
# Export-internal pointers (ChatGPT sediment://file_..., sandbox:/...) are not hosts.
IGNORE_SCHEMES = {"sediment", "sandbox", "file", "attachment", "about", "chrome", "data", "blob"}


def load_patterns(path: Path | None) -> list[re.Pattern]:
    paths = [Path(path)] if path else [p for p in DEFAULT_PATTERNS if p.exists()]
    lines = [line for p in paths for line in p.read_text(encoding="utf-8").splitlines()]
    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            out.append(re.compile(line[3:]))
        else:
            out.append(re.compile(r"(?<![\w-])(?:[\w-]+\.)*" + re.escape(line) + r"(?![\w-])", re.I))
    return out


def _is_private_ip(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local


def url_kind(url: str, extra: list[re.Pattern]) -> str | None:
    """Return why a URL must be redacted, or None if it is fine."""
    m = HOST_RE.match(url)
    if not m or url.split(":", 1)[0].lower() in IGNORE_SCHEMES:
        return None
    userinfo, host = m.group(1), m.group(2).lower()
    if userinfo and ":" in userinfo:
        return "url-credentials"
    if any(p.search(host) or p.search(url) for p in extra):
        return "internal-url"
    if host in INTERNAL_HOSTS or host.endswith(INTERNAL_SUFFIXES) or _is_private_ip(host):
        return "internal-url"
    if "." not in host or INTERNAL_LABELS.match(host):
        return "internal-url"
    return None


def redact(text: str, extra: list[re.Pattern] | None = None) -> tuple[str, Counter]:
    """Return (redacted text, Counter of kinds). Idempotent."""
    extra = extra or []
    counts: Counter = Counter()

    def sub_url(m: re.Match) -> str:
        kind = url_kind(m.group(0), extra)
        if not kind:
            return m.group(0)
        counts[kind] += 1
        return MARK

    text = URL_RE.sub(sub_url, text)
    for kind, rx, grp in SECRET_PATTERNS:
        def sub(m: re.Match, kind=kind, grp=grp) -> str:
            counts[kind] += 1
            if grp == 0:
                return MARK
            s, e = m.span(grp)
            return m.group(0)[: s - m.start()] + MARK + m.group(0)[e - m.start():]
        text = rx.sub(sub, text)
    for p in extra:  # bare internal hosts outside URLs
        def sub_host(m: re.Match) -> str:
            counts["internal-host"] += 1
            return MARK
        text = p.sub(sub_host, text)

    def sub_ip(m: re.Match) -> str:
        if not _is_private_ip(m.group(0)) or m.group(0).count(".") != 3:
            return m.group(0)
        counts["private-ip"] += 1
        return MARK

    text = PRIVATE_IP_RE.sub(sub_ip, text)
    return text, counts


def scan(text: str, extra: list[re.Pattern] | None = None) -> list[tuple[int, str]]:
    """Return (line number, kind) for every hit, without changing anything."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        _, c = redact(line, extra)
        hits += [(n, k) for k, v in c.items() for _ in range(v)]
    return hits


REQUIRED = ("title", "source", "type", "ingested", "authors", "source_date")
CORPORATE_SOURCE = re.compile(r"(?i)(jira|confluence|sharepoint|knowledge base|teams|outlook|\.eml\b|transcript)")


def frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip("\"'")
    return {}


def wiki_findings(f: Path, text: str, names: list[str]) -> list[tuple[int, str, str, str]]:
    """Structural rules of a wiki root: (line, severity, rule, excerpt)."""
    if f.suffix != ".md" or f.name in {"_index.md", "log.md", "config.md", "schema.md"}:
        return []
    out = []
    fm = frontmatter(text)
    if "raw" in f.parts:
        out += [(1, "warning", f"frontmatter-missing-{k}", "") for k in REQUIRED if k not in fm]
        if not f.name.endswith(".local.md") and CORPORATE_SOURCE.search(fm.get("source", "") + " " + f.name):
            out.append((1, "error", "corporate-copy-not-local", fm.get("source", "")[:60]))
    if names and fm.get("sensitivity") != "confidential":
        low = text.lower()
        hit = sorted({n for n in names if re.search(r"\b" + re.escape(n.lower()) + r"\b", low)})
        if hit:
            out.append((1, "warning", "customer-name-without-confidential", ", ".join(hit)))
    return out


def iter_files(paths: list[str]):
    for p in map(Path, paths):
        if p.is_dir():
            yield from sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in TEXT_EXT)
        elif p.is_file():
            yield p
        else:
            print(f"missing: {p}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--fix", action="store_true", help="rewrite files in place (never under raw/)")
    ap.add_argument("--patterns", type=Path, help=f"extra internal patterns (default {DEFAULT_PATTERNS})")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print the total")
    ap.add_argument("--hosts", action="store_true", help="list URL hosts with counts (already-flagged ones marked)")
    ap.add_argument("--wiki", action="store_true", help="also check wiki structure (raw frontmatter, *.local.md)")
    ap.add_argument("--names", type=Path, help="with --wiki: customer/prospect names, one per line")
    args = ap.parse_args()
    extra = load_patterns(args.patterns)
    names = [n.strip() for n in args.names.read_text(encoding="utf-8").splitlines()
             if n.strip() and not n.startswith("#")] if args.names else []

    if args.hosts:
        hosts: Counter = Counter()
        flagged = set()
        for f in iter_files(args.paths):
            for url in URL_RE.findall(f.read_text(encoding="utf-8", errors="replace")):
                m = HOST_RE.match(url)
                if m:
                    hosts[m.group(2).lower()] += 1
                    if url_kind(url, extra):
                        flagged.add(m.group(2).lower())
        for host, n in hosts.most_common():
            print(f"{n:6d}  {'R' if host in flagged else ' '}  {host}")
        return 0

    total: Counter = Counter()
    blocked = errors = 0
    for f in iter_files(args.paths):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"skip {f}: {e}", file=sys.stderr)
            continue
        if args.wiki:
            for n, sev, rule, excerpt in wiki_findings(f, text, names):
                print(f"{f}:{n}: {sev} {rule}" + (f": {excerpt}" if excerpt else ""))
                errors += sev == "error"
        new, counts = redact(text, extra)
        if args.wiki and "raw" in f.parts and f.name.endswith(".local.md"):
            counts = Counter({k: v for k, v in counts.items() if k not in INTERNAL_KINDS})
        if not counts:
            continue
        total += counts
        in_raw = "raw" in f.parts
        if not args.quiet:
            lines = sorted({n for n, _ in scan(text, extra)})
            kinds = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
            where = ",".join(map(str, lines[:10])) + ("…" if len(lines) > 10 else "")
            note = " (raw/: not rewritten, needs review)" if in_raw and args.fix else ""
            print(f"{sum(counts.values()):4d}  {f}  [{kinds}] lines {where}{note}")
        if args.fix and not in_raw:
            f.write_text(new, encoding="utf-8")
        elif in_raw:
            blocked += 1

    n = sum(total.values())
    verb = "redacted" if args.fix else "found"
    print(f"{verb}: {n}" + (f"  ({', '.join(f'{k}={v}' for k, v in sorted(total.items()))})" if n else ""))
    if args.fix:
        return 1 if blocked or errors else 0
    return 1 if n or errors else 0


if __name__ == "__main__":
    sys.exit(main())
