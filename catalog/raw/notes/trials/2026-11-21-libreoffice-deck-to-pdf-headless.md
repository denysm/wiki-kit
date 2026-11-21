---
title: "Use record: LibreOffice headless, image-heavy deck to PDF"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: LibreOffice/core
part: "soffice --headless --convert-to pdf"
version: "26.8.3"
status: in use
tags: [catalog, trial, use-record, kind-app, libreoffice, soffice, converting]
summary: "The kit's ingest instructions use soffice --headless --convert-to pdf --outdir to turn image-heavy slide decks into PDF before reading them. The installed version is 26.8.3.1 (checked 2026-11-21); run dates were not recorded. Cost not measured."
---

# Use record: LibreOffice headless, image-heavy deck to PDF

- **Task, by kind**: a slide deck whose slides are mostly pictures gives little text through the text extractor; convert it to PDF and read the PDF instead, then add a short description of the image-only slides.
- **Command**: `soffice --headless --convert-to pdf --outdir SCRATCH <file>`, from the kit's agent instructions (`agents/COMMON.md`, Step 1, documents). The output goes to a scratch folder; the original file is not touched.
- **Part used**: `soffice --headless --convert-to pdf`. Other conversion targets, `--cat` and `--print-to-file` are not used.
- **Version**: 26.8.3 is the version the desk check read on the project's download page. Installed version: LibreOffice 26.8.3.1, the app; `soffice` on PATH is the Homebrew cask wrapper of 26.8.3 (version checked 2026-11-21 from the app's Info.plist). It matches the version the desk check read. No date of a first run was recorded; 2026-11-21 is the date of this record.
- **Cost**: not measured. The PDF is then read through the agent's own PDF reading, not through pypdf.

## Not checked

Output quality for particular decks, run time, and whether LibreOffice sends anything outward during conversion.
