"""Add short descriptions of attached images to an exported raw source, on demand.

Usage: describe_images.py <raw.local.md> [--model sonnet] [--limit N] [--batch 6] [--dry-run]

Reads the "Attachments" table of a file written by atlassian_export.py --files, finds image
rows whose local copy exists and that are not yet listed in the "## Images" section, asks
`claude -p` (default model: sonnet, Read tool only, run in a temp directory so this wiki's
context is not loaded) to describe them, and appends the answers to "## Images".
atlassian_export.py keeps that section when it re-exports the page.

Costs model tokens: run it only for pages whose images matter, and use --limit first.
Descriptions are brief (what the picture shows, visible labels); images are not embedded.
"""
import argparse, json, os, re, subprocess, sys, tempfile

IMG = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def section(text):
    m = re.search(r"\n## Images\n(.*?)(?=\n## |\Z)", text, re.S)
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--limit", type=int, default=0, help="describe at most N images")
    ap.add_argument("--batch", type=int, default=6, help="images per model call")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read()
    have = set(re.findall(r"^- `([^`]+)`:", section(text).group(1), re.M)) if section(text) else set()
    todo = []
    for row in re.findall(r"^\| \[([^\]]+)\]\([^)]*\) \|.*\| `([^`]+)` \|$", text, re.M):
        name, path = row[0], os.path.expanduser(row[1])
        if os.path.splitext(name)[1].lower() in IMG and os.path.exists(path) and name not in have:
            todo.append((name, path))
    if a.limit:
        todo = todo[:a.limit]
    print(f"{len(todo)} images to describe ({len(have)} already described)")
    if a.dry_run or not todo:
        return
    new = []
    for i in range(0, len(todo), a.batch):
        chunk = todo[i:i + a.batch]
        prompt = ("Read each image below with the Read tool and describe it for a project knowledge base. "
                  "For each: 1-3 sentences in English saying what it shows (diagram, UI screenshot, chart), "
                  "and quote the visible labels, titles and key numbers. Do not guess beyond what is visible. "
                  "If a credential, token or password is visible, write [REDACTED:secret] instead of it. "
                  "Answer with only a JSON object {\"<file name>\": \"<description>\"}.\n\n"
                  + "\n".join(f"{n}: {p}" for n, p in chunk))
        dirs = sorted({os.path.dirname(p) for _, p in chunk})
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(["claude", "-p", "--model", a.model, "--allowedTools=Read",
                                "--strict-mcp-config", "--output-format", "text",
                                *[f"--add-dir={d}" for d in dirs]],
                               input=prompt, capture_output=True, text=True, cwd=tmp)
        m = re.search(r"\{.*\}", r.stdout, re.S)
        try:
            got = json.loads(m.group(0)) if m else {}
        except ValueError:
            got = {}
        if not got:
            print(f"batch {i // a.batch + 1}: no usable answer: {(r.stderr or r.stdout)[:200]}", file=sys.stderr)
            continue
        for n, _ in chunk:
            if n in got:
                desc = re.sub(r"\s+", " ", str(got[n])).strip()
                new.append(f"- `{n}`: {desc}")
    if not new:
        sys.exit("nothing described")
    sec = section(text)
    if sec:
        text = text[:sec.end()].rstrip("\n") + "\n" + "\n".join(new) + "\n" + text[sec.end():]
    else:
        text = text.rstrip("\n") + "\n\n## Images\n\n" + "\n".join(new) + "\n"
    open(a.file, "w", encoding="utf-8").write(text)
    print(f"added {len(new)} descriptions to {a.file}")


if __name__ == "__main__":
    main()
