---
title: "python-openxml/python-docx"
category: reference
kind: library
areas: [converting-documents-and-recordings]
repo: python-openxml/python-docx
version: "1.2.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/python-openxml-python-docx-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, kind-library, python-docx, docx, word]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Pure-Python library that reads, creates and updates .docx files. Version 1.2.0 runs in the kit's doc2md.py through uv run --with, with no install, to turn a Word document into Markdown with headings, lists and tables; comments and other modules are read or listed. No network code found."
---

# python-openxml/python-docx

> A library for reading, creating and updating Word `.docx` files (kind `library`, licence MIT, version `1.2.0`; PyPI gives the same). Here it runs inside the kit's `doc2md.py`, in a throwaway `uv` environment, to turn a document into Markdown.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a Word document into Markdown with headings, list items and tables in order | `docx.Document` | converting-documents-and-recordings |
| Read the paragraph styles of a document to rebuild its outline | `docx.styles` | converting-documents-and-recordings |
| Read the review comments of a document | `docx.comments` | converting-documents-and-recordings |
| Generate or edit a Word document from data in code | `docx.document` | converting-documents-and-recordings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone https://github.com/python-openxml/python-docx $EXTERNAL/python-docx` at the default-branch commit `e454546` (tag `v1.2.0`; no GitHub releases). Read first: `docs/user/quickstart.rst`, then `src/docx/api.py` and `src/docx/document.py`.
- **In use**: version `1.2.0` through `uv run --no-project --with python-pptx --with python-docx --with pypdf python -I doc2md.py plan.json` from a scratch folder; nothing installed globally. The version `uv` resolved on each real run was not recorded.
- **Switch off**: nothing; a search of `src/` for network and process calls found none.
- **Do not install** into a global Python; real installation waits for the user's yes.

## What's inside

Parts are modules, as `schema.md` says for a library.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `docx.Document` | `Document(path)` opens a `.docx` or builds a default one; the only name in `__all__`. | in use | A venv with the package (`uv run --with`) | Re-check when a release after `1.2.0` appears or a file fails to open. |
| `docx.document` | The document: `paragraphs`, `tables`, `iter_inner_content()`, `comments`, and writers such as `add_paragraph`, `add_table`, `save`. | in use | The same venv | Re-check when body order breaks on a document with nested tables. |
| `docx.text` | `Paragraph.text`, `style`, `runs`, `hyperlinks`. | in use | The same venv | Re-check when hyperlink text goes missing from an extract. |
| `docx.table` | `Table` rows, columns and cells with `text`. | in use | The same venv | Re-check on a table with merged cells. |
| `docx.styles` | Style objects; the style name drives the Markdown heading and list rules. | in use | The same venv | Re-check on a document whose headings use custom style names. |
| `docx.oxml` | The XML element layer; used only to walk the body in order. | in use | The same venv | Re-check when the body walk is replaced by `iter_inner_content()`. |
| `docx.comments` | Review comments, the feature added at the version read ("Add support for comments") | candidate | The same venv | Try it when a reviewed document's comments must reach the extract. |
| `docx.section`, `docx.shape`, `docx.image`, `docx.drawing`, `docx.settings`, `docx.opc`, `docx.parts`, `docx.enum`, `docx.dml` | Sections with headers and footers, shapes, images, package plumbing, enumerations. | listed | The same venv | Read when headers, footers or pictures matter. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Extract Word documents into Markdown raw sources | `docx.Document` | In use through `doc2md.py`; date is that of the record, first use not recorded. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md) |
| 2026-11-21 | Same task, body in order | `docx.document` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md) |
| 2026-11-21 | Same task, body in order | `docx.text` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md) |
| 2026-11-21 | Same task, body in order | `docx.table` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md) |
| 2026-11-21 | Same task, body in order | `docx.styles` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md) |
| 2026-11-21 | Same task, body in order | `docx.oxml` | In use through `doc2md.py`. | Not measured | [use record](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md) |

## Verdict

python-docx is the Word reader of the kit's converter: small, pure Python, no network code found, run in a throwaway environment. Six modules are `in use`; comments are read, the rest listed. Known gaps: comments, headers, footers and footnotes do not reach the extract. Revisit when a release passes `1.2.0` or when a reviewed document loses its comments in conversion.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; documents, PDFs, slides, audio and video into text
- [[scanny-python-pptx|scanny/python-pptx]] (../references/scanny-python-pptx.md): the same job for slide decks
- [[py-pdf-pypdf|py-pdf/pypdf]] (../references/py-pdf-pypdf.md): the same job for PDFs
- [[libreoffice-libreoffice|LibreOffice/core]] (../references/libreoffice-libreoffice.md): converts other office formats to PDF

## Sources

- [Desk check: python-openxml/python-docx 1.2.0](../../raw/repos/python-openxml-python-docx-desk-check-2026-11-21.md): modules read from the clone, freshness through the GitHub API and PyPI, network-code search.
- [Use record: python-docx, document body to Markdown](../../raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md): how `doc2md.py` uses it.
