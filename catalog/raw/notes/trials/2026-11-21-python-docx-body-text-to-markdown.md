---
title: "Use record: python-docx, document body to Markdown"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: python-openxml/python-docx
part: "docx.Document"
version: "1.2.0"
status: in use
tags: [catalog, trial, use-record, kind-library, python-docx, converting]
summary: "python-docx runs inside the kit's doc2md.py through uv run --with, with no install, to turn a .docx into Markdown: headings, list items, paragraphs and tables in body order. Version read 1.2.0; the version uv resolved on each run was not recorded. Cost not measured."
---

# Use record: python-docx, document body to Markdown

- **Task, by kind**: extract a Word document into a Markdown raw source, keeping headings, lists and tables.
- **How it is run**: `uv run --no-project --with python-pptx --with python-docx --with pypdf python -I doc2md.py plan.json` from a scratch folder; a throwaway environment, nothing installed globally.
- **Parts used** (read in `scripts/doc2md.py`, function `docx_md`): `docx.Document(path)` (part `docx.Document`); the body's child elements in order via `document.element.body.iterchildren()` (parts `docx.document`, `docx.oxml`); `Paragraph` with `text` and `style.name` (parts `docx.text`, `docx.styles`); `Table` with `rows`, `cells` and cell `text` (part `docx.table`).
- **Output**: a style named "Heading N" becomes a Markdown heading of level N+1 (at most 6); a style name containing "list" becomes `- text`; empty paragraphs are dropped; a table becomes a pipe table with a separator row after the first row.
- **Version**: 1.2.0 is what the desk check read in the clone and what PyPI lists as latest on 2026-11-21. The version `uv` resolved on each real run was not recorded.
- **Cost**: not measured; the package is downloaded once and cached by `uv`.

## Not checked

Comments, headers, footers, footnotes and text boxes are not extracted by the script and were not examined. Numbered lists whose style name lacks "list" come out as plain paragraphs (read from the script, not observed).
