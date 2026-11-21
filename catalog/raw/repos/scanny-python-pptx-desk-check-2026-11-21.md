---
title: "Desk check: scanny/python-pptx 1.0.2"
source: https://github.com/scanny/python-pptx/tree/278b47b
type: repos
authors: ["Steve Canny"]
source_date: 2024-08-07
ingested: 2026-11-21
repo: scanny/python-pptx
kind: library
version: "1.0.2"
licence: MIT
tags: [catalog, desk-check, kind-library, python-pptx, pptx, powerpoint, converting]
summary: "python-pptx 1.0.2 read from a read-only clone at the default-branch commit 278b47b: the Presentation entry point, slides, notes, shapes, text and table modules the kit's doc2md.py uses to turn a .pptx into Markdown, and the modules it does not use (charts, fills, media). Pure Python, no network code found."
---

# Desk check: scanny/python-pptx 1.0.2

## Repository facts

- Repository https://github.com/scanny/python-pptx read in a read-only clone at `$EXTERNAL/python-pptx`, default branch `master`, commit `278b47b` ("fix(enum): replace read-only enum values", 2024-08-07). `git describe --tags` gives `v1.0.2`. The working tree was not edited.
- Package `python-pptx`, `__version__ = "1.0.2"` in `src/pptx/__init__.py`; `pyproject.toml` takes the version from it. PyPI (`https://pypi.org/pypi/python-pptx/json`, checked 2026-11-21) also gives 1.0.2, uploaded 2024-08-07. The two agree.
- README: "python-pptx is a Python library for creating, reading, and updating PowerPoint (.pptx) files." It "does not require the PowerPoint application to be installed or licensed". `pyproject.toml` describes it as "Create, read, and update PowerPoint 2007+ (.pptx) files."
- `requires-python = ">=3.8"`. Dependencies: Pillow, XlsxWriter (for charts), lxml, typing_extensions.
- Licence file `LICENSE`: "The MIT License (MIT)", "Copyright (c) 2013 Steve Canny". `pyproject.toml`: `license = { text = "MIT" }`.
- Layout: library in `src/pptx/`, docs in `docs/` (`docs/user/` guides, `docs/api/` reference), tests in `tests/` and `features/`.

## Freshness (checked 2026-11-21 through `gh api`)

- `pushed_at`: 2024-08-07T17:36:44Z. Archived: false. Default branch `master`. The clone's commit is the default-branch head (compare shows 0 commits ahead).
- Latest release: none (the releases endpoint answers 404); the version is the tag `v1.0.2` and PyPI. `HISTORY.rst` lists 1.0.2 (2024-08-07) first: "fix: #1003 restore read-only enum members".
- Licence as GitHub reports it: MIT; as read from the file: MIT.

## How to run here

- **Clone, read-only, only to read**: `git clone https://github.com/scanny/python-pptx $EXTERNAL/python-pptx`. Never build or edit it; it is not run from the clone.
- **Nothing to switch off**: a search of `src/` for `urllib`, `requests`, `socket`, `http.client`, `subprocess` and `telemetry` found no hits. The library reads and writes local files.
- **Do not install** it into a global Python. Use a throwaway environment, as the kit's own run line does: `uv run --no-project --with python-pptx python -I script.py`. That downloads the package from PyPI once; real installation waits for the user's yes.
- **Without it**: `doc2md.py` cannot extract a `.pptx`; its other formats still work.

## Parts

For a library a part is a module or main entry point, per `schema.md`.

### `pptx.Presentation` (`src/pptx/api.py`)

`Presentation(pptx=None)` returns a presentation loaded from a path or a file-like object; with no argument it loads the built-in default template. It raises `ValueError` when the file's main part is not a PowerPoint file ("is not a PowerPoint file"). It is the only name in `__all__`. Needs only a file. In use (use record).

### `pptx.slide` (`src/pptx/slide.py`)

Classes `Slide`, `Slides`, `SlideLayout`, `SlideMaster`, `NotesSlide`, `NotesMaster`. `prs.slides` iterates slides; `Slide.has_notes_slide` and `Slide.notes_slide` give the speaker-notes page; `NotesSlide.notes_text_frame` returns the text frame of the notes placeholder and `None` when there is none ("if the notes master does not have a body placeholder, or if the notes placeholder has been deleted"). Notable: a caller that does not check for `None` fails on such a deck. In use.

### `pptx.shapes` (`src/pptx/shapes/`)

`shapetree.py` holds the shape collections: `SlideShapes` is iterable; shapes carry `has_text_frame` and, for tables, `has_table`. The same module has the creation calls `add_chart`, `add_connector`, `add_group_shape`, `add_ole_object`, `add_picture`, `add_shape`, `add_textbox`, `build_freeform`, `add_movie` and `add_table`. Other files: `autoshape.py`, `connector.py`, `freeform.py`, `graphfrm.py`, `group.py`, `picture.py`, `placeholder.py`. Reading text from shapes: in use. Creating shapes: read, not used.

### `pptx.text` (`src/pptx/text/`)

`text.py` holds `TextFrame`, paragraphs and runs; `Paragraph.text` is the paragraph's text. `fonts.py` and `layout.py` handle fonts and fitting text. Paragraph text reading: in use.

### `pptx.table` (`src/pptx/table.py`)

`Table` with rows, columns and cells; each cell has `text` and a `text_frame`. Reading rows and cell text: in use.

### `pptx.chart` (`src/pptx/chart/`)

Chart objects (`chart.py`, `axis.py`, `plot.py`, `series.py`, `data.py`, `xlsx.py`); `add_chart` on the shape collection builds one. The charting features depend on XlsxWriter (`docs/user/install.rst`). Not used: `doc2md.py` ignores charts, so a chart's data is not in the extract.

### `pptx.dml`, `pptx.enum`, `pptx.media`, `pptx.action`, `pptx.opc`, `pptx.oxml`, `pptx.parts`, `pptx.package`

Named from the directory and the `docs/api/` page names (fills, lines and colours in `dml`; enumerations; media; click actions; package and XML layers). Not read beyond the names; listed.

## Reasons for any rejection or reference status

None.

## How the kit uses it

`scripts/doc2md.py` (`pptx_md`) imports `Presentation` and, for each slide, reads text from every shape that `has_text_frame`, the rows of every table shape, and the speaker notes. Use record: `raw/notes/trials/2026-11-21-python-pptx-slide-text-to-markdown.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 36 model calls on sonnet, $1.53 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
