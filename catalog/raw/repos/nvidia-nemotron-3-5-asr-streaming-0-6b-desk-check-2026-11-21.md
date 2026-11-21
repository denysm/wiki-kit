---
title: "Desk check: nvidia/nemotron-3.5-asr-streaming-0.6b revision ea30d66"
source: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b/tree/ea30d66debe3740a08b573244286791d423d6b3e
type: repos
authors: ["NVIDIA"]
source_date: 2026-09-10
ingested: 2026-11-21
url: https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b
kind: model
version: "ea30d66"
licence: OpenMDW-1.1
tags: [catalog, desk-check, kind-model, speech-to-text, streaming, multilingual, nvidia, gguf]
summary: "Nemotron 3.5 ASR Streaming 0.6B read from its Hugging Face card and API metadata at revision ea30d66: a multilingual cache-aware streaming recogniser with punctuation, chunk sizes from 80 ms to 1.12 s, Russian and Ukrainian among 19 transcription-ready locales, FLEURS word error rates per chunk size; a q8_0 GGUF for NeMo-Speech.cpp, a .nemo for NeMo and Transformers support. No weights downloaded."
---

# Desk check: nvidia/nemotron-3.5-asr-streaming-0.6b revision ea30d66

## Repository facts

- Model page https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b, revision `ea30d66debe3740a08b573244286791d423d6b3e` (short `ea30d66`). API: created 2026-05-15T21:52:25.000Z, `lastModified` 2026-09-10T16:49:07.000Z, not gated, 431243 downloads.
- Licence: card header `license: other`, `license_name: openmdw-1.1`, link https://openmdw.ai/license/1-1/. Card text: "Use of the model is governed by the [OpenMDW-1.1](https://openmdw.ai/license/1-1/) license."
- What it is: "a multilingual, streaming Automatic Speech Recognition (ASR) model", "this 600M parameter model transcribes speech into text with native support for punctuation and capitalization, and offers runtime flexibility with configurable chunk sizes, including 80ms, 160ms, 320ms, 560ms, and 1120ms." Architecture: "Cache-Aware FastConformer-RNNT", "24 encoder layers".
- Languages: "Transcription-ready (19 locales)": English (en-US, en-GB), Spanish (es-US, es-ES), French (fr-FR, fr-CA), Italian (it-IT), Portuguese (pt-BR, pt-PT), Dutch (nl-NL), German (de-DE), Turkish (tr-TR), Russian (ru-RU), Arabic (ar-AR), Hindi (hi-IN), Japanese (ja-JP), Korean (ko-KR), Vietnamese (vi-VN), Ukrainian (uk-UA). "Broad-coverage (13 locales)" and "Adaptation-ready (8 locales)" follow; Kazakh is in none of the three tiers. "Transcription-ready and broad-coverage locales (**32 total**) produce ASR transcription out of the box".
- Language detection: with `target_lang=auto` "the model detects the spoken language and emits the corresponding **language code/tag** in the output following the terminal punctuation".
- Latency: `att_context_size` in 80 ms frames: "[56, 0]: Chunk size = 1 (1 × 80ms = 0.08s)" up to "[56, 13]: Chunk size = 14 (14 × 80ms = 1.12s)".
- FLEURS word error rate (%), language given (LangID), chunk 80ms / 160ms / 320ms / 560ms / 1.12s:

| Language | 80ms | 160ms | 320ms | 560ms | 1.12s |
|---|---|---|---|---|---|
| English (en-US, en-GB) | 9.43 | 8.88 | 8.27 | 7.99 | 7.91 |
| German (de-DE) | 9.81 | 9.21 | 8.83 | 8.42 | 8.31 |
| French (fr-FR, fr-CA) | 10.97 | 10.60 | 9.79 | 9.45 | 9.03 |
| Russian (ru-RU) | 10.84 | 10.73 | 9.87 | 9.60 | 9.17 |
| Ukrainian (uk-UA) | 15.70 | 15.21 | 14.55 | 13.67 | 13.07 |

  With auto-detect, Russian is 12.47 / 12.09 / 11.01 / 10.57 / 10.03 and Ukrainian 18.81 / 17.96 / 16.79 / 15.60 / 14.59. The card warns: "Normalization is not perfect across all 40 language-locales, and residual mismatches between normalized text can inflate the reported error rates".
- Files (API, bytes): `model.safetensors` 2552062944, `nemotron-3.5-asr-streaming-0.6b.nemo` 2368284501, `nemotron-3.5-asr-streaming-0.6b.q8_0.gguf` 742090464, `tokenizer.json` 752051.

## How to run here

- **No clone.** Read the card with `curl -s https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b/raw/ea30d66debe3740a08b573244286791d423d6b3e/README.md`, the metadata with `https://huggingface.co/api/models/nvidia/nemotron-3.5-asr-streaming-0.6b?blobs=true`.
- **Runtimes named on the card**: NeMo-Speech.cpp (`nemo-speech transcribe audio.wav --model models/nemotron-3.5-asr-streaming-0.6b.q8_0.gguf --language en-US`, "or `--language auto`"); NVIDIA NeMo ("Python 3.11 or later, Cython, and a recent PyTorch version", `pip install git+https://github.com/NVIDIA/NeMo.git@main#egg=nemo_toolkit[asr]`); Transformers: "Nemotron3_5Asr is available in 🤗 Transformers starting from v5.13.0", with a streaming example and `processor.set_num_lookahead_tokens(6)`.
- **Outbound calls**: downloading the file is the only one; the runtimes run it locally.
- **Install steps to avoid**: NeMo from git `main` and PyTorch in the kit's Python; a trial uses the q8_0 GGUF with NeMo-Speech.cpp in a throwaway folder after the user's yes.

## Parts (variants)

- `q8_0.gguf`: 742090464 bytes, for NeMo-Speech.cpp.
- `.nemo`: 2368284501 bytes, for NeMo (PyTorch).
- `model.safetensors`: 2552062944 bytes, for Transformers (v5.13.0 or later).
