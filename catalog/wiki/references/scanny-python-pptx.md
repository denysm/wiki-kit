---
title: "scanny/python-pptx"
category: reference
kind: library
areas: [converting-documents-and-recordings]
repo: scanny/python-pptx
version: "1.0.2"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/scanny-python-pptx-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, kind-library, python-pptx, pptx, powerpoint]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Pure-Python library that reads, creates and updates .pptx files. Version 1.0.2 runs in the kit's doc2md.py through uv run --with, with no install, to extract slide text, tables and speaker notes into Markdown; charts and other modules are read or listed. No network code found."
---

# scanny/python-pptx

> A library for reading, creating and updating PowerPoint `.pptx` files (kind `library`, licence MIT, version `1.0.2`; PyPI gives the same). It needs no PowerPoint. Here it runs inside the kit's `doc2md.py`, in a throwaway `uv` environment, to turn a deck into Markdown.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a slide deck into Markdown with text, tables and speaker notes per slide | `pptx.Presentation` | converting-documents-and-recordings |
| Read the speaker notes of every slide | `pptx.slide` | converting-documents-and-recordings |
| Build or edit a deck from data in code (text boxes, pictures, tables, charts) | `pptx.shapes` | converting-documents-and-recordings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone https://github.com/scanny/python-pptx $EXTERNAL/python-pptx` at the default-branch commit `278b47b` (tag `v1.0.2`; no GitHub releases). Read first: `docs/user/quickstart.rst`, then `src/pptx/api.py`.
- **In use**: version `1.0.2` through `uv run --no-project --with python-pptx --with python-docx --with pypdf python -I doc2md.py plan.json` from a scratch folder; nothing installed globally. The version `uv` resolved on each real run was not recorded.
- **Switch off**: nothing; a search of `src/` for network and process calls found none.
- **Do not install** into a global Python; real installation waits for the user's yes. Not checked: decks with a notes slide that has no body placeholder, where the library returns `None` and `doc2md.py` does not check.

## What's inside

Parts are modules, as `schema.md` says for a library.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `pptx.Presentation` | `Presentation(path)` opens a `.pptx` or builds a default one; the only name in `__all__`. | in use | A venv with the package (`uv run --with`) | Re-check when a release after `1.0.2` appears or when a deck fails to open with "is not a PowerPoint file". |
| `pptx.slide` | Slides, layouts, masters and notes slides; `has_notes_slide` and `notes_text_frame` give the speaker notes, `None` without a notes placeholder. | in use | The same venv | Re-check on a deck without a notes placeholder, where `doc2md.py` would fail. |
| `pptx.shapes` | Shape collections: text frames and tables on read; `add_chart`, `add_picture`, `add_shape`, `add_textbox`, `add_table` and more on write. | in use | The same venv | Re-check text in grouped shapes, which a top-level loop does not reach. |
| `pptx.text` | Text frames, paragraphs, runs, fonts; paragraph `text`. | in use | The same venv | Re-check when extracted text loses line breaks or runs. |
| `pptx.table` | Table rows, columns and cells with `text`. | in use | The same venv | Re-check on a deck with merged cells. |
| `pptx.chart` | Chart objects and `add_chart`; uses XlsxWriter. | candidate | The package plus XlsxWriter | Try it when chart data must reach the Markdown extract, which `doc2md.py` skips. |
| `pptx.dml`, `pptx.enum`, `pptx.media`, `pptx.action`, `pptx.opc`, `pptx.oxml`, `pptx.parts`, `pptx.package` | Fills, lines and colours; enumerations; media; click actions; package and XML layers. | listed | The same venv | Read when a task needs formatting, media or the XML underneath. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Extract the text of slide decks into Markdown raw sources | `pptx.Presentation` | In use through `doc2md.py`; date is that of the record, first use not recorded. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md) |
| 2026-11-21 | Same task, slide text, notes, tables | `pptx.slide` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md) |
| 2026-11-21 | Same task, slide text, notes, tables | `pptx.shapes` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md) |
| 2026-11-21 | Same task, slide text, notes, tables | `pptx.text` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md) |
| 2026-11-21 | Same task, slide text, notes, tables | `pptx.table` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md) |

## Verdict

python-pptx is the deck reader of the kit's converter: small, pure Python, no network code found, run in a throwaway environment. Four modules it uses are `in use`; charts are read, the rest listed. Known gap: charts and grouped shapes do not reach the extract. Revisit when a release passes `1.0.2` (the last release is from 2024-08-07, the last push too) or when a deck loses content in conversion.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; documents, PDFs, slides, audio and video into text
- [[python-openxml-python-docx|python-openxml/python-docx]] (../references/python-openxml-python-docx.md): the same job for Word files
- [[py-pdf-pypdf|py-pdf/pypdf]] (../references/py-pdf-pypdf.md): the same job for PDFs
- [[libreoffice-libreoffice|LibreOffice/core]] (../references/libreoffice-libreoffice.md): converts image-heavy decks to PDF first

## Sources

- [Desk check: scanny/python-pptx 1.0.2](../../raw/repos/scanny-python-pptx-desk-check-2026-11-21.md): modules read from the clone, freshness through the GitHub API and PyPI, network-code search.
- [Use record: python-pptx, slide text and notes to Markdown](../../raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md): how `doc2md.py` uses it.
