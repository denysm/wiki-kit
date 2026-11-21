---
title: "Desk check: LibreOffice 26.8.3 (LibreOffice/core)"
source: https://github.com/LibreOffice/core/tree/libreoffice-26.8.3.1
type: repos
authors: ["The Document Foundation", "LibreOffice contributors"]
source_date: 2026-11-09
ingested: 2026-11-21
url: https://www.libreoffice.org
repo: LibreOffice/core
kind: app
version: "26.8.3"
licence: MPL-2.0
tags: [catalog, desk-check, kind-app, libreoffice, soffice, headless, converting]
summary: "LibreOffice 26.8.3 desk-checked from the project's download page, its command-line help and the GitHub mirror (no clone): the soffice headless conversion commands the kit uses to turn office files into PDF, the other headless commands, and the licence question (project says MPL-2.0, the mirror shows GPL-3.0). Nothing was installed or run."
---

# Desk check: LibreOffice 26.8.3 (LibreOffice/core)

## Repository facts

- Project site https://www.libreoffice.org. Source mirror https://github.com/LibreOffice/core, default branch `master`, described as "Read-only LibreOffice core repo - no pull request (use gerrit instead https://gerrit.libreoffice.org/) - don't download zip, use https://dev-www.libreoffice.org/bundles/ instead". It is not cloned: the core repository is huge. Read through `gh api` and the project's public pages only.
- README (read through `gh api`): "LibreOffice is an integrated office suite based on copyleft licenses and compatible with most document formats and standards." It is backed by The Document Foundation.
- Version: the download page https://www.libreoffice.org/download/download-libreoffice/ (read 2026-11-21) offers 26.8.3 for Windows, macOS (Apple Silicon and Intel) and Linux (rpm, deb) and calls it "our latest stable release"; the page's version list is "LibreOffice 26.8.3 LibreOffice 26.2.7 LibreOffice 27.2.0.0 alpha1". The mirror's newest release tag is `libreoffice-26.8.3.1` (commit date 2026-11-09), next to `libreoffice-27.2.0.0.alpha1`. The card's version is 26.8.3. `https://download.documentfoundation.org/libreoffice/stable/` lists 25.8.7, 26.2.7, 26.8.2 and 26.8.3.
- Installed version, as told by the calling session: LibreOffice 26.8.3.1, the app, with `soffice` on PATH being the Homebrew cask wrapper of 26.8.3 (version checked 2026-11-21 from the app's Info.plist). It matches the card's version 26.8.3.
- Layout of the mirror's root: `COPYING`, `COPYING.LGPL`, `COPYING.MPL`, `README.md`, `readlicense_oo` and the source trees.

## Freshness (checked 2026-11-21 through `gh api`)

- `pushed_at`: 2026-11-21T10:05:34Z. Archived: false. Default branch `master`.
- Latest release: none as a GitHub release (the releases endpoint answers 404); releases are tags on the mirror and builds on the project's download pages.
- The mirror's tag list from `gh api repos/LibreOffice/core/tags` starts with old tags; the matching-refs query for `libreoffice-26` and `libreoffice-27` gives the current ones above.

## Licence: what each source says

- GitHub shows `GPL-3.0` for the mirror (`license.spdx_id`).
- `COPYING` (35147 bytes) starts "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007". `COPYING.LGPL` starts "GNU LESSER GENERAL PUBLIC LICENSE Version 3, 29 June 2007". `COPYING.MPL` starts "Mozilla Public License Version 2.0".
- The project's licence page https://www.libreoffice.org/about-us/licenses/ says: "LibreOffice is made available subject to the terms of the Mozilla Public License v2.0 which is reproduced below." It adds that the suite "includes software which differs from version to version under a large variety of other Open Source licenses", and that contributors are asked to license code "jointly under both the Mozilla Public License v2 and the GNU Lesser GPL v3+ licenses".
- So GitHub's `GPL-3.0` reflects the `COPYING` file that the mirror's detector picked; the project's own statement is MPL-2.0. The card records MPL-2.0 as the project's statement and shows the GitHub value beside it. This was read, not legally interpreted.

## How to run here

- **No clone.** Nothing was installed or run for this check. The office suite is installed from the project's download page, not from the source mirror; real installation waits for the user's yes.
- **Command line** (help page https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html): `soffice` is the launcher. `--headless` "Starts in 'headless mode' which allows using the application without user interface." `--convert-to OutputFileExtension[:OutputFilterName[:OutputFilterParams[,param]]] [--outdir output_dir]` converts files; "In absence of --outdir, current working directory is used for the result"; the help's examples include `--convert-to pdf *.doc`, `--convert-to pdf:writer_pdf_Export --outdir /home/user *.doc`, `--convert-to "html:XHTML Writer File:UTF8" *.doc` and `--convert-to "txt:Text (encoded):UTF8" *.doc`.
- **Outbound calls and telemetry**: not checked. The command-line help lists no switch for them.
- **Without it**: the kit's route for image-heavy decks (convert to PDF, then read the PDF) is unavailable; text extraction from decks, Word files and PDFs still works through the three Python libraries.

## Parts

For an app a part is a command or main function, per `schema.md`. Read from the help page above; the application itself was not run.

### `soffice --headless --convert-to pdf --outdir <dir> <file>`

Converts an office file (the kit's use: a slide deck) to PDF in `<dir>` without opening a window. Needs the installed suite and a writable output folder. In use (use record).

### `soffice --headless --convert-to <other targets>`

The same switch with other output extensions and filters: `html` with the filter `XHTML Writer File`, `txt` with `Text (encoded)`. The help links the lists of document filters and of filter options for CSV files and PDF files. Not used.

### `soffice --cat <file>`

"Applies filter 'txt:Text' to the following text documents and dump text content to console (implies --headless). Cannot be used with --convert-to." Not used.

### `soffice --print-to-file`

"Batch-print files to file", with `--printer-name` and `--outdir`. Not used.

### `soffice --norestore`, `--terminate_after_init`

`--norestore` "Disables restart and file recovery after a system crash"; `--terminate_after_init` "Exit after initialization complete (no documents loaded)". Read; not used.

### Other switches and starters

`--infilter`, `--accept`, `--invisible`, `--nologo`, `--nolockcheck`, `--safe-mode`, `--version`, `--writer`, `--calc`, `--draw`, `--impress`, `--math`, `--base`-style starters and the `--help*` pages: named in the help page's list, not read; listed.

## Reasons for any rejection or reference status

None.

## How the kit uses it

The kit's agent instructions (`agents/COMMON.md`, Step 1, documents) say: for image-heavy key decks run `soffice --headless --convert-to pdf --outdir SCRATCH <file>`, read the PDF, and add a short description of image-only slides. The text extractors (`scripts/doc2md.py` with python-pptx, python-docx, pypdf) do not call LibreOffice. Use record: `raw/notes/trials/2026-11-21-libreoffice-deck-to-pdf-headless.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 36 model calls on sonnet, $1.53 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
