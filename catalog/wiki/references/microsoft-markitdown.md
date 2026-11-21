---
title: "microsoft/markitdown"
category: reference
kind: cli
areas: [converting-documents-and-recordings]
repo: microsoft/markitdown
version: "0.1.9"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/microsoft-markitdown-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-markitdown-quick-office-and-pdf-to-markdown.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-converting-documents-and-recordings, kind-cli, markitdown, markdown, office, pdf]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Python command and library that converts Office files, PDF, images, audio, HTML and more to Markdown. The markitdown command, as a uv tool, is in use for quick one-off Office and PDF conversion; the kit's own script does not call it. Read at v0.1.9: speech transcription, YouTube transcripts, two Azure services and LLM image description call outside services, off unless their extra, flag or client is given."
---

# microsoft/markitdown

> A file-to-Markdown converter (kind `cli`, also a Python library; licence MIT, version `0.1.9` read in a clone): one `markitdown` command and a `MarkItDown` class with a converter per format. Here the command is used by hand for quick Office and PDF conversion; the kit's script `doc2md.py` does its own conversion and does not call it.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Convert a Word, PowerPoint or PDF file to Markdown in one command | `markitdown` command | converting-documents-and-recordings |
| Convert a PDF with tables or forms to Markdown | `PdfConverter` | converting-documents-and-recordings |
| Convert documents with no data leaving the machine | `markitdown` command | converting-documents-and-recordings |
| Call the converter from Python code | `MarkItDown` API | converting-documents-and-recordings |
| Let a local agent convert a file or web address through a tool call | `markitdown-mcp` | converting-documents-and-recordings |
| Read text out of images inside PDF or Office files with a vision model (data leaves the machine) | `markitdown-ocr` | converting-documents-and-recordings |
| Add a converter for a format it lacks | plugin mechanism | converting-documents-and-recordings |

## Run it here

- **Clone, read-only, to read docs only**: `git clone --depth 1 --branch v0.1.9 https://github.com/microsoft/markitdown $EXTERNAL/markitdown`. Never build or edit it. Read first: `README.md`, then `packages/markitdown/src/markitdown/_markitdown.py` and `__main__.py`.
- **In use**: the `markitdown` command installed as a `uv tool`, by hand, for quick Office and PDF to Markdown. The installed `markitdown` is `0.1.5` (checked 2026-11-21 with `--version`), behind the `0.1.9` read: re-check before relying on a converter changed since. The extras installed are not stated. The kit's `scripts/doc2md.py` does not call it: a search of the kit's `scripts/` for `markitdown` found no match.
- **Sends outward, off unless used**: speech transcription sends audio to a Google web service (extra `audio-transcription`); YouTube links fetch transcripts (extra `youtube-transcription`); Azure Document Intelligence and Content Understanding send the document to an Azure endpoint (`-d` with `-e`, `--use-cu`); an LLM describes images only when `llm_client` and `llm_model` are given in code, and `markitdown-ocr` sends images to such a model. `convert()` also fetches `http:` and `https:` addresses. No `telemetry` or `analytics` text found in the core package. Read in the source, not observed.
- **Keep off**: pass local file paths only (`convert_local()` in code); install only the extras needed, for example `markitdown[pdf, docx, pptx]`, never `[all]`; do not pass `-d`, `-e`, `--use-cu` or `-p`; set no `llm_client`; plugins are "disabled by default".
- **Do not install**: `pip install 'markitdown[all]'`, `markitdown-ocr`, the MCP server or the Docker image into the clone or the global environment; installation waits for the user's yes.

## What's inside

Parts are the command, the API, the converters it registers and the other packages. Defined in `packages/`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `markitdown` command | `markitdown file -o out.md`, or standard input; `-x`, `-m`, `-c`, `-d`, `-e`, `--use-cu`, `-p`, `--list-plugins`, `--keep-data-uris`. | in use | Python; the extras for the formats used | Re-check before relying on a converter changed between `0.1.5` in use and the `0.1.9` read, and when a release changes the output for Word, PowerPoint or PDF. |
| `MarkItDown` API | `MarkItDown(enable_plugins=False).convert("file")`; `.markdown`; `convert_local`, `convert_stream`, `convert_response`. | candidate | Python | Try it when a script, not a shell command, must convert. |
| `PdfConverter` | PDF text with table and form handling (`pdfminer.six`, `pdfplumber`). | candidate | Extra `pdf` | Try it on a PDF with tables and compare with the kit's own PDF text. |
| `PptxConverter` | Slide text; images described only with an LLM client. | candidate | Extra `pptx` | Try it on a deck and compare with the kit's own slide text. |
| `AudioConverter` | `.wav`, `.mp3`, `.m4a`, `.mp4`: metadata through `exiftool`, and speech transcription. | candidate | Extra `audio-transcription` sends audio to a Google service | Read when an outside transcription is acceptable; not for recordings that must stay local. |
| `ImageConverter` | `.jpg`, `.jpeg`, `.png`: `exiftool` metadata, and an LLM description only with a client. | candidate | Optional `exiftool`; an LLM client sends images out | Try it for image metadata only. |
| `YouTubeConverter` | Fetches a video's transcript from its URL. | candidate | Extra `youtube-transcription`; network | Read when a public video transcript is wanted. |
| `DocumentIntelligenceConverter` | Sends the file to Azure Document Intelligence. | candidate | An Azure endpoint; data leaves the machine | Read only when a cloud service is allowed for the document. |
| `ContentUnderstandingConverter` | Sends the file to Azure Content Understanding. | candidate | An Azure endpoint; data leaves the machine | Read only when a cloud service is allowed for the document. |
| plugin mechanism | Entry point group `markitdown.plugin`, `register_converters`; off unless `-p` or `enable_plugins=True`. | candidate | A plugin package | Try it when a format is missing and a plugin exists. |
| `markitdown-ocr` | Plugin, version `0.1.2`: LLM vision reads text from images in PDF, DOCX, PPTX and XLSX. | candidate | An OpenAI-compatible client; images leave the machine | Read when scanned pages must be read and a model may see them. |
| `markitdown-mcp` | MCP server, version `0.0.1a8`, tool `convert_to_markdown(uri)` for `http:`, `https:`, `file:`, `data:`; STDIO by default. | candidate | Python or Docker; the tool can fetch web addresses | Try it when an agent needs conversion as a tool, over STDIO. |
| `markitdown-sample-plugin` | Skeleton of an RTF converter plugin. | candidate | Nothing to run | Read when writing a plugin. |
| `PlainTextConverter` | Plain text formats. | listed | Core | Read when a text format is rejected. |
| `ZipConverter` | Converts each file inside a ZIP. | listed | Core | Read when an archive must be converted whole. |
| `HtmlConverter` | HTML to Markdown. | listed | Core | Read when HTML pages are converted. |
| `RssConverter` | Feeds. | listed | Core | Read when a feed is converted. |
| `WikipediaConverter` | Wikipedia pages. | listed | Core; network for a web address | Read when a Wikipedia page is converted. |
| `BingSerpConverter` | Bing search result pages. | listed | Core | Read when such a page must be converted. |
| `DocxConverter` | Word files (`mammoth`). | listed | Extra `docx` | Read when the command's Word output is checked. |
| `XlsxConverter` | Excel `.xlsx` (`pandas`, `openpyxl`). | listed | Extra `xlsx` | Read when a spreadsheet is converted. |
| `XlsConverter` | Old Excel `.xls` (`xlrd`). | listed | Extra `xls` | Read when an old spreadsheet is converted. |
| `OutlookMsgConverter` | Outlook `.msg` messages (`olefile`). | listed | Extra `outlook` | Read when mail files are converted. |
| `EpubConverter` | `.epub` books. | listed | Core | Read when a book is converted. |
| `CsvConverter` | `.csv` tables. | listed | Core | Read when a CSV is converted. |
| `IpynbConverter` | Jupyter notebooks. | listed | Core | Read when a notebook is converted. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| not stated | Quick one-off Office or PDF to Markdown by hand | `markitdown` command | In use at `0.1.5` as a `uv tool`; extras and output quality not recorded. | Not measured | [use record](../../raw/notes/trials/2026-11-21-markitdown-quick-office-and-pdf-to-markdown.md) |

## Verdict

markitdown is the kit maintainer's quick converter for one-off Office and PDF files, run as a `uv tool`; the kit's own script does the batch work. One part is in use, twelve are read and thirteen listed. Known cost: `[all]` installs clients for outside services, and several features send data out when switched on; the safe route is local files and only the extras needed. Revisit when the in-use `0.1.5` is upgraded to `0.1.9` or later and the extras are recorded, when its output is compared with `doc2md.py` on the same files, or when the MCP package's version `0.0.1a8` is replaced by a stable one.

## See Also

- [[area-converting-documents-and-recordings|Converting documents and recordings]] ([Converting documents and recordings](../topics/area-converting-documents-and-recordings.md)): area page; documents and recordings to Markdown
- [[scanny-python-pptx|scanny/python-pptx]] (../references/scanny-python-pptx.md): the slide reader the kit's script uses instead
- [[python-openxml-python-docx|python-openxml/python-docx]] (../references/python-openxml-python-docx.md): the Word reader the kit's script uses instead
- [[py-pdf-pypdf|py-pdf/pypdf]] (../references/py-pdf-pypdf.md): the PDF reader the kit's script uses instead

## Sources

- [Desk check: microsoft/markitdown v0.1.9](../../raw/repos/microsoft-markitdown-desk-check-2026-11-21.md): command, converters, packages and outbound calls read from the clone; freshness through the GitHub API.
- [Use record: markitdown command for quick conversion](../../raw/notes/trials/2026-11-21-markitdown-quick-office-and-pdf-to-markdown.md): the real use and the finding that the kit's script does not call it.
