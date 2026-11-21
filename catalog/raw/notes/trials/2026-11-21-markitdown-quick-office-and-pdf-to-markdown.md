---
title: "Use record: markitdown command for quick Office and PDF to Markdown"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: microsoft/markitdown
part: markitdown command
version: "0.1.5"
status: in use
tags: [catalog, trial, use-record, kind-cli, markitdown, office, pdf]
summary: "The markitdown command, installed as a uv tool, is in real use by the kit's maintainer for quick one-off conversion of Office files and PDFs to Markdown. The kit's own conversion script does not call it. Installed version 0.1.5, checked 2026-11-21 with `--version`; dates and speed are not stated."
---

# Use record: markitdown command for quick Office and PDF to Markdown

Told by the kit owner, retold here without detail; not re-measured.

- **Tool and part**: microsoft/markitdown, part `markitdown` command.
- **Task, by kind**: convert an Office document or a PDF to Markdown quickly, by hand, when the kit's script is not the right fit.
- **How it is run**: installed as a `uv tool`, so it lives in its own environment and is called as the `markitdown` command.
- **Version**: 0.1.5, the installed `markitdown` (version checked 2026-11-21 with `--version`). The desk check read `v0.1.9`, the latest release on 2026-11-21, so the tool in use is behind it.
- **Not part of the kit's scripts**: `scripts/doc2md.py` does not call it (a search of the kit's `scripts/` for `markitdown` finds no match).
- **Not stated**: which extras were installed, the date of first use, speed, the quality of the output.

## Cost

Not measured: no money and no tokens are spent by the command itself, and no figure was recorded.
