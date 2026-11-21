---
title: "Desk check: python-openxml/python-docx 1.2.0"
source: https://github.com/python-openxml/python-docx/tree/e454546
type: repos
authors: ["Steve Canny"]
source_date: 2025-06-16
ingested: 2026-11-21
repo: python-openxml/python-docx
kind: library
version: "1.2.0"
licence: MIT
tags: [catalog, desk-check, kind-library, python-docx, docx, word, converting]
summary: "python-docx 1.2.0 read from a read-only clone at the default-branch commit e454546 (the v1.2.0 release commit): the Document entry point, paragraphs, tables, styles and comments that the kit's doc2md.py uses or could use to turn a .docx into Markdown. Pure Python, no network code found."
---

# Desk check: python-openxml/python-docx 1.2.0

## Repository facts

- Repository https://github.com/python-openxml/python-docx read in a read-only clone at `$EXTERNAL/python-docx`, default branch `master`, commit `e454546` ("release: prepare v1.2.0 release", 2025-06-16). `git describe --tags` gives `v1.2.0`. The working tree was not edited.
- Package `python-docx`, `__version__ = "1.2.0"` in `src/docx/__init__.py`; `pyproject.toml` takes the version from it. PyPI (`https://pypi.org/pypi/python-docx/json`, checked 2026-11-21) also gives 1.2.0, uploaded 2025-06-16. The two agree.
- README: "python-docx is a Python library for reading, creating, and updating Microsoft Word 2007+ (.docx) files."
- `requires-python = ">=3.9"`. Dependencies: lxml, typing_extensions.
- Licence file `LICENSE`: "The MIT License (MIT)", "Copyright (c) 2013 Steve Canny". `pyproject.toml`: `license = { text = "MIT" }`.
- Layout: library in `src/docx/`, docs in `docs/` (`docs/user/` guides, `docs/api/`), tests in `tests/` and `features/`. `HISTORY.rst` lists 1.2.0 (2025-06-16) first: "Add support for comments" and "Drop support for Python 3.8, add testing for Python 3.13".

## Freshness (checked 2026-11-21 through `gh api`)

- `pushed_at`: 2026-08-01T14:59:42Z. Archived: false. Default branch `master`. The clone's commit equals the default-branch head (compare shows status "identical"), so the later push did not add commits to the default branch.
- Latest release: none (the releases endpoint answers 404); the version is the tag `v1.2.0` and PyPI.
- Licence as GitHub reports it: MIT; as read from the file: MIT.

## How to run here

- **Clone, read-only, only to read**: `git clone https://github.com/python-openxml/python-docx $EXTERNAL/python-docx`. Never build or edit it; it is not run from the clone.
- **Nothing to switch off**: a search of `src/` for `urllib`, `requests`, `socket`, `http.client`, `subprocess` and `telemetry` found no hits.
- **Do not install** it into a global Python. Use a throwaway environment, as the kit's own run line does: `uv run --no-project --with python-docx python -I script.py`; that downloads the package from PyPI once. Real installation waits for the user's yes.
- **Without it**: `doc2md.py` cannot extract a `.docx`; its other formats still work.

## Parts

For a library a part is a module or main entry point, per `schema.md`.

### `docx.Document` (`src/docx/api.py`)

`Document(docx=None)` opens a path or a file-like object, or builds a default document. The only name in `__all__`. In use.

### `docx.document` (`src/docx/document.py`)

The document object: `paragraphs`, `tables`, `sections`, `styles`, `comments`, `core_properties`, `iter_inner_content()`, and writers `add_paragraph`, `add_heading`, `add_table`, `add_picture`, `add_page_break`, `add_section`, `add_comment`, `save`. In use for the document body: the kit's script walks `document.element.body` children in order, so paragraphs and tables stay interleaved.

### `docx.text` (`src/docx/text/`)

`paragraph.py`: `Paragraph.text`, `style`, `runs`, `hyperlinks`, `iter_inner_content`. In use: paragraph text and style.

### `docx.table` (`src/docx/table.py`)

`Table` with `rows`, `columns`, `cell(row, col)`, `add_row`, `add_column`; each cell has `text`. In use: row and cell text.

### `docx.styles` (`src/docx/styles/`)

Style objects; a paragraph's `style.name` is what the kit's script matches ("heading N", names containing "list"). In use.

### `docx.comments` (`src/docx/comments.py`, `docs/user/comments.rst`)

New in 1.2.0: "Add support for comments". `Document.comments`; `Document.add_comment`. The docs say a comment can only be added to the main document. Read, not used: the kit's script does not extract comments.

### `docx.oxml`

The XML element layer (`src/docx/oxml/`: `document.py`, `table.py`, `text/`, `styles.py`, `numbering.py`, `section.py` and others). In use only through `document.element.body.iterchildren()`.

### `docx.section`, `docx.shape`, `docx.image`, `docx.drawing`, `docx.settings`, `docx.opc`, `docx.parts`, `docx.enum`, `docx.dml`

Named from the directory and docs page names (sections, headers and footers in `docs/user/hdrftr.rst`, shapes, images, package plumbing). Not read beyond the names; listed.

## Reasons for any rejection or reference status

None.

## How the kit uses it

`scripts/doc2md.py` (`docx_md`) opens the file with `docx.Document`, walks the body in order, writes headings as Markdown headings one level deeper, paragraphs whose style name contains "list" as `- ` items, other paragraphs as text, and tables as pipe tables with a separator row. Use record: `raw/notes/trials/2026-11-21-python-docx-body-text-to-markdown.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 36 model calls on sonnet, $1.53 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
