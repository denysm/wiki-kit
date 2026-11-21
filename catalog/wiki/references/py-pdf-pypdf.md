---
title: "py-pdf/pypdf"
category: reference
kind: library
areas: [converting-documents-and-recordings]
repo: py-pdf/pypdf
version: "7.1.1"
licence: BSD-3-Clause
desk_checked: 2026-11-21
sources:
  - raw/repos/py-pdf-pypdf-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-pypdf-page-text-to-markdown.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, kind-library, pypdf, pdf]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Pure-Python PDF library: text and metadata extraction, splitting, merging, cropping, encryption. Version 7.1.1 runs in the kit's doc2md.py through uv run --with, with no install, to extract page text into Markdown; the writer, images and forms are read or listed. Licence BSD-3-Clause read from the file; one optional external binary."
---

# py-pdf/pypdf

> A pure-Python PDF library (kind `library`, licence BSD-3-Clause read from the `LICENSE` file because GitHub does not detect it, version `7.1.1`; PyPI gives the same). Here it runs inside the kit's `doc2md.py`, in a throwaway `uv` environment, to pull the text of each PDF page into Markdown.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a PDF with a text layer into Markdown, one section per page | `pypdf.PdfReader` | converting-documents-and-recordings |
| Get a page's text as a string, plain or laid out like the page | `pypdf.PageObject.extract_text` | converting-documents-and-recordings |
| Split, merge, crop or encrypt PDFs in code | `pypdf.PdfWriter` | converting-documents-and-recordings |
| Save the pictures of a PDF page | `page.images` | converting-documents-and-recordings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone --depth 1 --branch 7.1.1 https://github.com/py-pdf/pypdf $EXTERNAL/pypdf`. Read first: `README.md`, then `docs/user/extract-text.md`.
- **In use**: version `7.1.1` through `uv run --no-project --with python-pptx --with python-docx --with pypdf python -I doc2md.py plan.json` from a scratch folder; nothing installed globally, no extras. The version `uv` resolved on each real run was not recorded.
- **Switch off**: nothing; no network code found. The only external call is `jbig2dec` through `subprocess` for JBIG2 images, and only when a binary is configured.
- **Do not install** into a global Python, and do not add extras (`pypdf[crypto]`, `pypdf[image]`) unless a task needs them; real installation waits for the user's yes. Not checked: scanned PDFs, tables, multi-column pages.

## What's inside

Parts are the main entry points, as `schema.md` says for a library.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `pypdf.PdfReader` | Opens a PDF; `pages`, `is_encrypted`, `decrypt`, `metadata`, `outline`, form fields. | in use | A venv with the package (`uv run --with`) | Re-check when a release after `7.1.1` appears or a PDF fails to open. |
| `pypdf.PageObject.extract_text` | A page's text; `"plain"` mode is used; the docstring warns it "works well for some PDF files, but poorly for others". | in use | The same venv | Re-check on a PDF whose text comes out in the wrong order or empty. |
| `pypdf.PdfWriter` | `add_page`, `append`, `merge`, `encrypt`, `write`, `metadata`. | candidate | The package; AES encryption needs the `crypto` extra | Try it when pages of PDFs must be merged, split or protected. |
| `extract_text(extraction_mode="layout")` | Fixed-width text that follows the page layout. | candidate | The same venv | Try it on a PDF with columns or tables where plain mode scrambles order. |
| `page.images` | A page's images, saved through `image`. | candidate | The package plus the `image` extra (pillow) | Try it when pictures must be pulled from a PDF. |
| `pypdf.PageRange`, `pypdf.PaperSize`, `pypdf.generic`, `pypdf.annotations`, `pypdf.actions`, `pypdf.constants`, `pypdf.errors`, `pypdf.xmp` | Page ranges, paper sizes, low-level objects, annotations, actions, constants, exceptions, XMP metadata. | listed | The same venv | Read when a task edits annotations or reads XMP. |
| `pypdf.filters` | Stream decoders; runs the external `jbig2dec` binary for JBIG2 images when one is configured. | candidate | The package; `jbig2dec` for JBIG2 images | Try it when a scanned PDF's JBIG2 images fail to decode. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Extract the text layer of PDFs into Markdown raw sources | `pypdf.PdfReader` | In use through `doc2md.py`; date is that of the record, first use not recorded. | Not measured | [use record](../../raw/notes/trials/2026-11-21-pypdf-page-text-to-markdown.md) |
| 2026-11-21 | Same task, page text | `pypdf.PageObject.extract_text` | In use in plain mode. | Not measured | [use record](../../raw/notes/trials/2026-11-21-pypdf-page-text-to-markdown.md) |

## Verdict

pypdf is the PDF reader of the kit's converter: pure Python, no required dependencies on Python 3.11 and later, run in a throwaway environment. Two parts are `in use`, the writer, layout mode, images and decoders are read, the rest listed. The use is the text layer only; scanned pages were not checked. Revisit when a release passes `7.1.1` (the last release is from 2026-11-18, the last push 2026-11-21) or when a PDF extracts badly.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; documents, PDFs, slides, audio and video into text
- [[scanny-python-pptx|scanny/python-pptx]] (../references/scanny-python-pptx.md): the same job for slide decks
- [[python-openxml-python-docx|python-openxml/python-docx]] (../references/python-openxml-python-docx.md): the same job for Word files
- [[libreoffice-libreoffice|LibreOffice/core]] (../references/libreoffice-libreoffice.md): makes the PDFs that pypdf then reads

## Sources

- [Desk check: py-pdf/pypdf 7.1.1](../../raw/repos/py-pdf-pypdf-desk-check-2026-11-21.md): modules read from the clone, licence file against GitHub, freshness through the GitHub API and PyPI.
- [Use record: pypdf, page text to Markdown](../../raw/notes/trials/2026-11-21-pypdf-page-text-to-markdown.md): how `doc2md.py` uses it.
