---
title: "Use record: pypdf, page text to Markdown"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: py-pdf/pypdf
part: "pypdf.PdfReader"
version: "7.1.1"
status: in use
tags: [catalog, trial, use-record, kind-library, pypdf, converting]
summary: "pypdf runs inside the kit's doc2md.py through uv run --with, with no install, to turn a PDF into Markdown with one section per page. Version read 7.1.1; the version uv resolved on each run was not recorded. Cost not measured."
---

# Use record: pypdf, page text to Markdown

- **Task, by kind**: extract the text layer of a PDF into a Markdown raw source with one section per page.
- **How it is run**: `uv run --no-project --with python-pptx --with python-docx --with pypdf python -I doc2md.py plan.json` from a scratch folder; a throwaway environment, nothing installed globally and no extras.
- **Parts used** (read in `scripts/doc2md.py`, function `pdf_md`): `PdfReader(path)` and `pages` (part `pypdf.PdfReader`); `extract_text()` on each page, plain mode, an empty string when it returns nothing (part `pypdf.PageObject.extract_text`).
- **Output**: a `## Page N` heading with the page's text per page; a page without a text layer gives an empty section (read from the script, not observed).
- **Version**: 7.1.1 is what the desk check read in the clone and what PyPI lists as latest on 2026-11-21. The version `uv` resolved on each real run was not recorded.
- **Cost**: not measured; the package is downloaded once and cached by `uv`.

## Not checked

Scanned PDFs, tables, multi-column layout, encrypted files and layout mode were not examined. For decks whose slides are mostly pictures the kit's rules convert to PDF with LibreOffice and read that PDF; that route is in the LibreOffice use record.
