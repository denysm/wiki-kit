---
title: "LibreOffice/core"
category: reference
kind: app
areas: [converting-documents-and-recordings]
repo: LibreOffice/core
url: https://www.libreoffice.org
version: "26.8.3"
licence: MPL-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/libreoffice-libreoffice-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-libreoffice-deck-to-pdf-headless.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, kind-app, libreoffice, soffice, headless]
confidence: medium
volatility: hot
verified: 2026-11-21
summary: "Office suite whose soffice launcher converts office files without a window. The kit's instructions use soffice --headless --convert-to pdf to turn image-heavy slide decks into PDF before reading them (version 26.8.3 read, installed 26.8.3.1); other headless uses are read or listed. Licence: the project says MPL-2.0, the GitHub mirror shows GPL-3.0."
---

# LibreOffice/core

> An office suite (kind `app`, version `26.8.3` read on the project's download page, licence MPL-2.0 as the project states it; the GitHub mirror shows `GPL-3.0`). Here only its headless `soffice --convert-to` is used, to turn image-heavy decks into PDF. Not cloned, not installed or run for this card.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a slide deck whose slides are mostly pictures into a PDF that can be read page by page | `soffice --headless --convert-to pdf` | converting-documents-and-recordings |
| Convert an office file to HTML or plain text without opening a window | `soffice --headless --convert-to <other targets>` | converting-documents-and-recordings |
| Dump the text of a text document to the console | `soffice --cat` | converting-documents-and-recordings |

## Run it here

- **No clone**: the core repository is huge. Read the project's pages instead: https://www.libreoffice.org/download/download-libreoffice/ and the command-line help https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html.
- **In use**: the command `soffice --headless --convert-to pdf --outdir SCRATCH <file>` from the kit's agent instructions, for image-heavy decks. Installed version: `26.8.3.1`, the app, with `soffice` on PATH being the Homebrew cask wrapper of `26.8.3` (version checked 2026-11-21 from the app's Info.plist); it matches the version the desk check read; run dates were not recorded.
- **Licence**: GitHub shows `GPL-3.0` for the mirror, whose `COPYING` is the GPL version 3 text next to `COPYING.LGPL` and `COPYING.MPL`; the project's licence page says it is "made available subject to the terms of the Mozilla Public License v2.0". Both are recorded; this is not legal advice.
- **Switch off**: not checked; the command-line help lists no switch for outbound calls or telemetry.
- **Do not install** from the source mirror or a package manager on the strength of this card; real installation, from the project's download page, waits for the user's yes.

## What's inside

Parts are commands, as `schema.md` says for an app.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `soffice --headless --convert-to pdf` | Converts an office file to PDF in the `--outdir` folder, no window. | in use | The installed suite and a writable folder | Re-check output on a deck with many pictures and when a release after `26.8.3` appears. |
| `soffice --headless --convert-to <other targets>` | The same switch with other extensions and filters, such as `html` or `txt`. | candidate | The installed suite | Try it when a Word file needs HTML or text without Python. |
| `soffice --cat` | Applies the text filter and dumps text to the console; cannot be combined with `--convert-to`. | candidate | The installed suite | Try it for a quick look at a text document's content. |
| `soffice --print-to-file` | Batch-prints files to file, with `--printer-name` and `--outdir`. | candidate | The installed suite | Try it when a print-style PDF export is wanted. |
| `soffice --norestore`, `--terminate_after_init` | Disable crash recovery; exit after initialization. | candidate | The installed suite | Try them if a headless run hangs on recovery. |
| `--infilter`, `--accept`, `--invisible`, `--nologo`, `--nolockcheck`, `--safe-mode`, `--version`, `--writer`, `--calc`, `--draw`, `--impress`, `--math`, `--help*` | Input filters, remote control, display and start options, document starters, help pages. | listed | The installed suite | Read when a task needs them. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Convert image-heavy slide decks to PDF before reading | `soffice --headless --convert-to pdf` | In use per the kit's instructions; date is that of the record, first use not recorded. | Not measured | [use record](../../raw/notes/trials/2026-11-21-libreoffice-deck-to-pdf-headless.md) |

## Verdict

LibreOffice is the fallback of the kit's converter for decks the Python extractors cannot read well: one command, run headless, output to a scratch folder. One command is `in use`; the other headless commands are read from the help page, the rest listed. The confidence is medium because run dates and outbound behaviour were not recorded or checked. Revisit when a release passes `26.8.3`, when the licence question matters for a distribution, or when conversion quality on a deck is in doubt.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; documents, PDFs, slides, audio and video into text
- [[scanny-python-pptx|scanny/python-pptx]] (../references/scanny-python-pptx.md): reads decks directly, without LibreOffice
- [[python-openxml-python-docx|python-openxml/python-docx]] (../references/python-openxml-python-docx.md): reads Word files directly
- [[py-pdf-pypdf|py-pdf/pypdf]] (../references/py-pdf-pypdf.md): reads the PDFs that LibreOffice makes

## Sources

- [Desk check: LibreOffice 26.8.3](../../raw/repos/libreoffice-libreoffice-desk-check-2026-11-21.md): download page, command-line help, licence files and licence page, mirror freshness.
- [Use record: LibreOffice headless, image-heavy deck to PDF](../../raw/notes/trials/2026-11-21-libreoffice-deck-to-pdf-headless.md): the kit's use of `--convert-to pdf`.
