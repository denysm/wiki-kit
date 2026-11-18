#!/usr/bin/env python3
"""Check the frontmatter of every SKILL.md in the kit (skills/ and specialists/).

Errors (exit 1):
  - no frontmatter between '---' lines at the top of the file;
  - `name` missing, not lowercase letters, digits and hyphens (at most 64), or
    not equal to the folder name;
  - `metadata.version` missing or not quoted (an unquoted 1.0 is read as a number);
  - `description` missing, longer than 1024 characters, or without triggers:
    it must say when to use the skill ("Use when ..." or "Triggers ...").
Warnings (exit 0): a SKILL.md longer than 500 lines; move detail to references/.

Usage:
  skill_check.py                 every skills/*/SKILL.md and specialists/*/SKILL.md of the kit
  skill_check.py PATH ...        given SKILL.md files, or folders searched for */SKILL.md

Stdlib only; reads the small YAML subset skills use (top-level keys, one nested
`metadata:` map, quoted or block-scalar strings), not general YAML.
"""
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
DESCRIPTION_MAX = 1024
LINES_WARN = 500
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TRIGGER_RE = re.compile(r"\b(use when|triggers?\b)", re.IGNORECASE)
KEY_RE = re.compile(r"^( *)([A-Za-z0-9_-]+):(?: (.*))?$")


def unquote(raw):
    """(value, quoted) for a scalar written on one line."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        body = raw[1:-1]
        body = re.sub(r'\\(["\\/])', r"\1", body).replace("\\n", "\n").replace("\\t", "\t")
        return body, True
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'"), True
    if " #" in raw:
        raw = raw.split(" #", 1)[0].rstrip()
    return raw, False


def parse_frontmatter(lines):
    """Return (fields, error). fields maps 'name' or 'metadata.version' to (value, quoted)."""
    if not lines or lines[0].strip() != "---":
        return None, "no frontmatter: the file must start with '---'"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, "frontmatter is not closed with '---'"
    body = lines[1:end]
    fields, parent, i = {}, None, 0
    while i < len(body):
        line = body[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = KEY_RE.match(line)
        if not m:
            continue  # list items and continuation lines of plain scalars
        indent, key, raw = len(m.group(1)), m.group(2), m.group(3) or ""
        if indent == 0:
            parent = key
            full = key
        elif parent:
            full = parent + "." + key
        else:
            continue
        if raw.strip()[:1] in ("|", ">"):  # block scalar: gather the indented lines
            block = []
            while i < len(body) and (not body[i].strip() or len(body[i]) - len(body[i].lstrip()) > indent):
                block.append(body[i].strip())
                i += 1
            sep = "\n" if raw.strip()[0] == "|" else " "
            fields[full] = (sep.join(block).strip(), True)
        elif raw.strip():
            raw = raw.strip()
            q = raw[0] if raw[0] in "\"'" else ""
            # a scalar may continue on more indented lines (a quoted one until its closing quote)
            while i < len(body) and len(body[i]) - len(body[i].lstrip()) > indent and (
                    (q and not (len(raw) > 1 and raw.endswith(q)))
                    or (not q and body[i].strip() and not KEY_RE.match(body[i]))):
                raw = raw + " " + body[i].strip()
                i += 1
            fields[full] = unquote(raw)
    return fields, None


def check(path):
    """Return (errors, warnings) for one SKILL.md."""
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    fields, err = parse_frontmatter(lines)
    if err:
        return [err], warnings
    folder = path.parent.name

    name = fields.get("name", ("", False))[0]
    if not name:
        errors.append("`name` is missing")
    else:
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"`name: {name}` must be lowercase letters, digits and hyphens, at most 64")
        if name != folder:
            errors.append(f"`name: {name}` differs from the folder name `{folder}`")

    if "metadata.version" not in fields:
        errors.append('`metadata.version` is missing (add `metadata:` with `  version: "X.Y.Z"`)')
    else:
        version, quoted = fields["metadata.version"]
        if not quoted:
            errors.append(f'`metadata.version: {version}` must be quoted: version: "{version}"')
        elif not version:
            errors.append("`metadata.version` is empty")

    desc = fields.get("description", ("", False))[0]
    if not desc:
        errors.append("`description` is missing")
    else:
        if len(desc) > DESCRIPTION_MAX:
            errors.append(f"`description` is {len(desc)} characters, over {DESCRIPTION_MAX}")
        if not TRIGGER_RE.search(desc):
            errors.append("`description` says what the skill does but not when to use it: add 'Use when ...' or 'Triggers ...'")

    if len(lines) > LINES_WARN:
        warnings.append(f"{len(lines)} lines, over {LINES_WARN}: move detail to references/")
    return errors, warnings


def targets(args):
    if not args:
        args = [str(KIT / "skills"), str(KIT / "specialists")]
    found = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            found.extend(sorted(p.glob("*/SKILL.md")))
        elif p.is_file():
            found.append(p)
        else:
            print(f"not found: {a}", file=sys.stderr)
            sys.exit(2)
    return found


def main(argv):
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    files = targets(argv)
    if not files:
        print("no SKILL.md found", file=sys.stderr)
        return 2
    n_err = n_warn = 0
    for f in files:
        try:
            shown = f.resolve().relative_to(KIT)
        except ValueError:
            shown = f
        errors, warnings = check(f)
        for e in errors:
            print(f"ERROR {shown}: {e}")
        for w in warnings:
            print(f"WARN  {shown}: {w}")
        n_err += len(errors)
        n_warn += len(warnings)
    print(f"{len(files)} SKILL.md checked: {n_err} errors, {n_warn} warnings")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
