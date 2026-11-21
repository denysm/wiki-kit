---
title: "Use record: python-pptx, slide text and notes to Markdown"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: scanny/python-pptx
part: "pptx.Presentation"
version: "1.0.2"
status: in use
tags: [catalog, trial, use-record, kind-library, python-pptx, converting]
summary: "python-pptx runs inside the kit's doc2md.py through uv run --with, with no install, to turn a .pptx into Markdown: slide text, tables and speaker notes. Version read 1.0.2; the version uv resolved on each run was not recorded. Cost not measured."
---

# Use record: python-pptx, slide text and notes to Markdown

- **Task, by kind**: extract the text of a slide deck into a Markdown raw source with one section per slide.
- **How it is run**: `uv run --no-project --with python-pptx --with python-docx --with pypdf python -I doc2md.py plan.json` from a scratch folder. `uv` builds a throwaway environment; nothing is installed globally. `plan.json` lists the source file, the output path, title and frontmatter fields.
- **Parts used** (read in `scripts/doc2md.py`, function `pptx_md`): `Presentation(path)` and `prs.slides` (parts `pptx.Presentation`, `pptx.slide`); for each shape `has_text_frame`, `text_frame.paragraphs` and `text` (parts `pptx.shapes`, `pptx.text`); for table shapes `has_table`, `table.rows`, `cells` and cell `text` (part `pptx.table`); `has_notes_slide` and `notes_slide.notes_text_frame.text` for speaker notes.
- **Output**: one `## Slide N` section per slide with its text, tables as pipe rows, and a "Speaker notes" block when notes exist; a slide with no text gets `*(no text)*`.
- **Version**: 1.0.2 is what the desk check read in the clone and what PyPI lists as latest on 2026-11-21. The version `uv` resolved on each real run was not recorded.
- **Cost**: not measured; the package is downloaded from PyPI once and cached by `uv`.

## Not checked

Text in charts, grouped shapes and images is not extracted by the script and was not examined. `doc2md.py` calls `notes_text_frame.text` without a check for `None`, and the library returns `None` when a notes slide has no body placeholder (desk check, `pptx.slide`); whether that failure ever occurred was not recorded. Image-heavy decks are handled another way: see the LibreOffice use record.
