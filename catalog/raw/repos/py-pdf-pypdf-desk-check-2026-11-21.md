---
title: "Desk check: py-pdf/pypdf 7.1.1"
source: https://github.com/py-pdf/pypdf/tree/7.1.1
type: repos
authors: ["Mathieu Fenniak", "pypdf contributors"]
source_date: 2026-11-18
ingested: 2026-11-21
repo: py-pdf/pypdf
kind: library
version: "7.1.1"
licence: BSD-3-Clause
tags: [catalog, desk-check, kind-library, pypdf, pdf, converting]
summary: "pypdf 7.1.1 read from a read-only clone at the tag 7.1.1: PdfReader and page text extraction that the kit's doc2md.py uses to turn a PDF into Markdown, plus the writer, merging, encryption, images, forms and optional dependencies it does not use. Licence BSD-3-Clause read from the file, which GitHub does not detect. Pure Python; one optional external binary."
---

# Desk check: py-pdf/pypdf 7.1.1

## Repository facts

- Repository https://github.com/py-pdf/pypdf read in a read-only clone at `$EXTERNAL/pypdf`, tag `7.1.1`, commit `f017482` ("REL: 7.1.1", 2026-11-18); default branch `main`. The working tree was not edited.
- Package `pypdf`, `__version__ = "7.1.1"` in `pypdf/_version.py`. PyPI (`https://pypi.org/pypi/pypdf/json`, checked 2026-11-21) also gives 7.1.1, uploaded 2026-11-18. The two agree.
- README: "pypdf is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files." It "can retrieve text and metadata from PDFs as well".
- `requires-python = ">=3.10"`. Required dependencies: none on Python 3.11 and later (`typing_extensions` below 3.11). Optional extras in `pyproject.toml`: `crypto` (cryptography), `cryptodome`, `image` (pillow), `fonts` (fonttools), `brotli`, `rtl_text`, `full`.
- Licence file `LICENSE`: begins "Copyright (c) 2006-2008, Mathieu Fenniak", then "Redistribution and use in source and binary forms, with or without modification", three conditions (source notice, binary notice, "The name of the author may not be used to endorse or promote products"). That is the BSD 3-Clause text; the file does not say "BSD". `pyproject.toml`: `license = "BSD-3-Clause"`, `license-files = ["LICENSE"]`.
- Layout: library in `pypdf/` (`_reader.py`, `_writer.py`, `_page.py`, `_text_extraction/`, `_encryption.py`, `filters.py`, `generic/`, `annotations/`, `actions/`), docs in `docs/user/`, changelog `CHANGELOG.md`.

## Freshness (checked 2026-11-21 through `gh api`)

- `pushed_at`: 2026-11-21T11:09:43Z (after the tag; commits after `7.1.1` were not read). Archived: false. Default branch `main`.
- Latest release: `7.1.1`, published 2026-11-18T11:50:52Z, not a prerelease. `CHANGELOG.md` for 7.1.1 lists security fixes (limits on inline image size, page label size, cross-reference stream work).
- Licence as GitHub reports it: `NOASSERTION` (not detected); as read from the file and `pyproject.toml`: BSD-3-Clause.

## How to run here

- **Clone, read-only, only to read**: `git clone --depth 1 --branch 7.1.1 https://github.com/py-pdf/pypdf $EXTERNAL/pypdf`. Never build or edit it; it is not run from the clone.
- **Outbound calls**: none found in `pypdf/` except `subprocess` in `pypdf/filters.py`, which runs the external `jbig2dec` binary to decode JBIG2 images when `JBIG2DEC_BINARY` or the configuration names one (`pypdf/_configuration.py`); without it the library raises `DependencyError("jbig2dec>=0.19 is required.")`. No network code found.
- **Do not install** it into a global Python. Use a throwaway environment, as the kit's own run line does: `uv run --no-project --with pypdf python -I script.py`; that downloads the package from PyPI once. Extras (`pypdf[crypto]` and the rest) are not needed for plain text extraction and are not installed. Real installation waits for the user's yes.
- **Without it**: `doc2md.py` cannot extract a `.pdf`; its other formats still work.

## Parts

For a library a part is a module or main entry point, per `schema.md`.

### `pypdf.PdfReader` (`pypdf/_reader.py`)

`PdfReader(path_or_stream)` opens a PDF; `pages` lists its pages; `is_encrypted` and `decrypt(password)` handle protected files; `metadata`, `outline` and `get_form_text_fields()` come from the shared base `PdfDocCommon` (`pypdf/_doc_common.py`). In use for `pages`.

### `pypdf.PageObject.extract_text` (`pypdf/_page.py`)

Returns the page's text as a string. Parameters include `orientations`, `space_width`, `extraction_mode` (`"plain"` or `"layout"`) and visitor callbacks. The docstring says: "This works well for some PDF files, but poorly for others, depending on the generator used" and "Do not rely on the order of text coming out of this function". `docs/user/extract-text.md` shows layout mode with options such as `layout_mode_space_vertically` and `layout_mode_strip_rotated`. Plain mode: in use.

### `pypdf.PdfWriter` (`pypdf/_writer.py`)

Writes PDFs: `add_page`, `add_blank_page`, `append`, `merge`, `append_pages_from_reader`, `encrypt`, `write`, `metadata`. Merging and splitting are the README's headline. Needs only the package; AES encryption needs the `crypto` extra (README). Not used.

### `pypdf.PageRange` and `pypdf.PaperSize` (`pypdf/pagerange.py`, `pypdf/papersizes.py`)

Page-range parsing and paper sizes. Not read beyond the names; listed.

### Images (`docs/user/extract-images.md`)

`page.images` gives a page's images, each with a `name` and an `image` that can be saved; reading pictures needs the `image` extra (pillow). Read in the docs; not used.

### `pypdf.generic`, `pypdf.annotations`, `pypdf.actions`, `pypdf.filters`, `pypdf.constants`, `pypdf.errors`, `pypdf.xmp`

Low-level PDF objects, annotations, actions, stream filters (with the `jbig2dec` call above), constants, exceptions and XMP metadata. Named from the directory; listed, except `filters`, whose subprocess use is read above.

## Reasons for any rejection or reference status

None.

## How the kit uses it

`scripts/doc2md.py` (`pdf_md`) opens the file with `PdfReader`, walks `pages`, calls `extract_text()` on each (an empty string when it returns nothing) and writes a `## Page N` section per page. Use record: `raw/notes/trials/2026-11-21-pypdf-page-text-to-markdown.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 36 model calls on sonnet, $1.53 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
