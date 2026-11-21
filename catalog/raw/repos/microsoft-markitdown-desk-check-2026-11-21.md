---
title: "Desk check: microsoft/markitdown v0.1.9"
source: https://github.com/microsoft/markitdown/tree/v0.1.9
type: repos
authors: ["Microsoft Corporation", "Adam Fourney"]
source_date: 2026-10-21
ingested: 2026-11-21
repo: microsoft/markitdown
kind: cli
version: "0.1.9"
licence: MIT
tags: [catalog, desk-check, kind-cli, markitdown, markdown, office, pdf, conversion]
summary: "The command, converters, extras, plugin mechanism, MCP server package and outbound calls of markitdown v0.1.9 read from a read-only clone: one markitdown command and Python API converting Office files, PDF, images, audio, HTML, YouTube links and more to Markdown; speech transcription, YouTube transcripts, two Azure document services and LLM image description call outside services and are off unless used. Freshness from the GitHub API; the kit's script does not call it."
---

# Desk check: microsoft/markitdown v0.1.9

Read from a shallow clone of tag `v0.1.9` (commit `21d9c1d01ecc12538dab19811fd247ef2f96ef60`, committed 2026-10-21) at `$EXTERNAL/markitdown`. The clone was not modified; nothing was installed or run. Checked 2026-11-21. Version read by this desk check: 0.1.9 (`packages/markitdown/src/markitdown/__about__.py`).

## Repository facts

- `README.md`: "MarkItDown is a lightweight Python utility for converting various files to Markdown for use with LLMs and related text analysis pipelines." It says the output "is meant to be consumed by text analysis tools -- and may not be the best option for high-fidelity document conversions for human consumption." Supported inputs listed: PDF, PowerPoint, Word, Excel, images (EXIF metadata and OCR), audio (EXIF metadata and speech transcription), HTML, text-based formats (CSV, JSON, XML), ZIP files, YouTube URLs, EPubs.
- `LICENSE`: "MIT License", "Copyright (c) Microsoft Corporation." Python `>=3.10,<3.15` (`packages/markitdown/pyproject.toml`).
- Four packages under `packages/`: `markitdown` (the tool, version 0.1.9), `markitdown-mcp` (version `0.0.1a8`), `markitdown-ocr` (version `0.1.2`), `markitdown-sample-plugin`.
- Core dependencies: `beautifulsoup4`, `requests`, `certifi`, `markdownify`, `magika` (file-type detection), `charset-normalizer`, `defusedxml`. Optional extras: `all`, `pptx`, `docx`, `xlsx`, `xls`, `pdf`, `outlook`, `audio-transcription`, `youtube-transcription`, `az-doc-intel`, `az-content-understanding`.
- Security note (README, "Security Considerations"): "MarkItDown performs I/O with the privileges of the current process"; `convert()` "is intentionally permissive and can handle local files, remote URIs, and byte streams"; prefer `convert_local()`, `convert_response()` or `convert_stream()`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/microsoft/markitdown`: `pushed_at` 2026-11-07T00:14:01Z; licence `MIT`; default branch `main`; not archived.
- `gh api repos/microsoft/markitdown/releases/latest`: tag `v0.1.9`, published 2026-10-21T19:40:32Z.
- So the clone is at the latest release; commits were pushed to `main` after it.

## How to run here

- **Clone**: `git clone --depth 1 --branch v0.1.9 https://github.com/microsoft/markitdown $EXTERNAL/markitdown`. Read only; never build or edit it. Read first: `README.md`, then `packages/markitdown/src/markitdown/_markitdown.py` and `__main__.py`.
- **Outbound calls** (all read in the source, none observed):
  - `converters/_transcribe_audio.py` calls `recognizer.recognize_google(...)` of the `SpeechRecognition` package: audio is sent to a Google web speech service. Only with the `audio-transcription` extra installed; audio files (`.wav`, `.mp3`, `.m4a`, `.mp4`) otherwise give metadata only, or an error that names the missing extra.
  - `converters/_youtube_converter.py` fetches a video's transcript through `youtube-transcript-api`; only for a YouTube URL and with the `youtube-transcription` extra.
  - `converters/_doc_intel_converter.py` (Azure Document Intelligence) and `converters/_cu_converter.py` (Azure Content Understanding) send the document to an Azure endpoint; registered only when `docintel_endpoint` or `cu_endpoint` is given (CLI `-d`/`--use-docintel` with `-e`, `--use-cu` with `--cu-endpoint`, or the environment variable `MARKITDOWN_DOCINTEL_ENDPOINT`). The Content Understanding client sets the user agent `markitdown-cu/<version>`.
  - `converters/_image_converter.py` and `converters/_pptx_converter.py` send images to an LLM only when `llm_client` and `llm_model` are given; the CLI has no flag for that. The `markitdown-ocr` plugin does the same for images in PDF, DOCX, PPTX and XLSX files, and "If no `llm_client` is provided the plugin still loads, but OCR is silently skipped".
  - `_markitdown.py`: `convert()` accepts `http:`, `https:`, `file:` and `data:` URIs and fetches web addresses with `requests`; the session asks servers for Markdown over HTML.
  - A search of `packages/markitdown/src` for `telemetry` and `analytics` found no match.
- **Keep off**: use local file paths only (or `convert_local()` in code); do not install the `audio-transcription`, `youtube-transcription`, `az-doc-intel` or `az-content-understanding` extras, nor `markitdown-ocr`; do not pass `-d`, `-e`, `--use-cu`, or `-p`/`--use-plugins`; set no `llm_client`. Plugins are "disabled by default" (README).
- **Install steps to avoid**: `pip install 'markitdown[all]'` (README) pulls every extra, including the audio and Azure clients; install only the extras needed (`markitdown[pdf, docx, pptx]` is the README's own example). The Docker image and the MCP server are not needed. Installation waits for the user's yes.

## Parts

Parts are the command and the converters it registers (`_markitdown.py`, `enable_builtins`), then the other packages. Later registrations take priority over earlier ones.

### `markitdown` command (`packages/markitdown/src/markitdown/__main__.py`)

- Script entry `markitdown = "markitdown.__main__:main"`. `markitdown path-to-file.pdf > document.md`, `-o` output file, input from standard input, `-x` extension hint, `-m` MIME type, `-c` charset, `-d`/`--use-docintel` with `-e`/`--endpoint`, `--use-cu`/`--use-content-understanding` with `--cu-endpoint`, `--cu-analyzer`, `--cu-file-types`, `-p`/`--use-plugins`, `--list-plugins`, `--keep-data-uris`, `-v` version. Needs: Python and the extras for the formats used.

### Python API `MarkItDown` (`_markitdown.py`)

- `MarkItDown(enable_plugins=False).convert("file")` returns an object with `.markdown`; also `convert_local`, `convert_stream`, `convert_response`. `enable_builtins` registers the converters below; keyword arguments `llm_client`, `llm_model`, `llm_prompt`, `docintel_endpoint`, `cu_endpoint`, `exiftool_path`, `style_map`.

### Converters (`packages/markitdown/src/markitdown/converters/`)

- `PlainTextConverter`, `ZipConverter` (iterates over the archive), `HtmlConverter`: generic formats.
- `RssConverter`, `WikipediaConverter`, `YouTubeConverter`, `BingSerpConverter`: web pages and feeds; the YouTube one fetches transcripts (see outbound calls).
- `DocxConverter` (extra `docx`, `mammoth`), `XlsxConverter` and `XlsConverter` (`pandas`, `openpyxl`, `xlrd`), `PptxConverter` (`python-pptx`; images described only with an LLM client), `PdfConverter` (`pdfminer.six`, `pdfplumber`; has table and form handling code), `OutlookMsgConverter` (`olefile`), `EpubConverter`, `CsvConverter`, `IpynbConverter`.
- `AudioConverter` (`.wav`, `.mp3`, `.m4a`, `.mp4`): metadata through `exiftool` if installed, and speech transcription (outbound call, above). `ImageConverter` (`.jpg`, `.jpeg`, `.png`): `exiftool` metadata, and an LLM description only with a client.
- `DocumentIntelligenceConverter`, `ContentUnderstandingConverter`: cloud converters (above).
- Needs: Python and the matching extra; `exiftool` optional.

### Plugin mechanism (`_markitdown.py`, `_load_plugins`; `packages/markitdown-sample-plugin`)

- A plugin is a Python package that declares an entry point in the group `markitdown.plugin` and implements `register_converters`; plugins are off unless `--use-plugins` or `enable_plugins=True`. `markitdown --list-plugins` lists installed ones. `markitdown-sample-plugin` shows an RTF converter skeleton (its `accepts` and `convert` raise `NotImplementedError`).

### `markitdown-ocr` (`packages/markitdown-ocr`, version 0.1.2)

- A plugin: "LLM Vision plugin for MarkItDown that extracts text from images embedded in PDF, DOCX, PPTX, and XLSX files"; needs an OpenAI-compatible client and sends images to that model. Entry point `ocr = "markitdown_ocr"`. README only read, plus the `pyproject.toml`.

### `markitdown-mcp` (`packages/markitdown-mcp`, version 0.0.1a8)

- An MCP server over STDIO (default), Streamable HTTP and SSE with one tool, `convert_to_markdown(uri)`, where "uri can be any `http:`, `https:`, `file:`, or `data:` URI". The README says it is "meant for local use, with local trusted agents" and binds to `localhost` by default. Needs: Python; Docker is optional. An MCP tool that takes a web address can fetch it.

## How the kit uses it

The maintainer uses it as a `uv tool` for quick Office and PDF to Markdown; the use record is `raw/notes/trials/2026-11-21-markitdown-quick-office-and-pdf-to-markdown.md`. The kit's own script `scripts/doc2md.py` does not call it: a search of the kit's `scripts/` for `markitdown` found no match, and `doc2md.py` imports `python-pptx`, `python-docx` and `pypdf` directly.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 46 model calls on sonnet, $2.03 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
