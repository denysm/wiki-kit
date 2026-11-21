---
title: "Desk check: nvidia/parakeet-tdt-0.6b-v3 revision 541d1f9"
source: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3/tree/541d1f99c6b0c3cd0b11a95167540bb8edefd82b
type: repos
authors: ["NVIDIA"]
source_date: 2026-08-05
ingested: 2026-11-21
url: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3
kind: model
version: "541d1f9"
licence: CC-BY-4.0
tags: [catalog, desk-check, kind-model, speech-to-text, multilingual, nvidia, gguf, timestamps]
summary: "Parakeet TDT 0.6B v3 read from its Hugging Face card and API metadata at revision 541d1f9: a batch multilingual recogniser for 25 European languages including Russian and Ukrainian, with word and segment timestamps, under CC-BY-4.0; a q8_0 GGUF for NeMo-Speech.cpp, a separate f16 conversion for whisper.cpp's parakeet-cli, a .nemo for NeMo. No weights downloaded."
---

# Desk check: nvidia/parakeet-tdt-0.6b-v3 revision 541d1f9

## Repository facts

- Model page https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3, revision `541d1f99c6b0c3cd0b11a95167540bb8edefd82b` (short `541d1f9`). API: created 2025-08-04T13:34:09.000Z, `lastModified` 2026-08-05T21:46:17.000Z, not gated, 540099 downloads.
- Licence: card header `license: cc-by-4.0`; "GOVERNING TERMS: Use of this model is governed by the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) license."
- Languages (card): Bulgarian (**bg**), Croatian (**hr**), Czech (**cs**), Danish (**da**), Dutch (**nl**), English (**en**), Estonian (**et**), Finnish (**fi**), French (**fr**), German (**de**), Greek (**el**), Hungarian (**hu**), Italian (**it**), Latvian (**lv**), Lithuanian (**lt**), Maltese (**mt**), Polish (**pl**), Portuguese (**pt**), Romanian (**ro**), Slovak (**sk**), Slovenian (**sl**), Spanish (**es**), Swedish (**sv**), Russian (**ru**), Ukrainian (**uk**). Kazakh is not among them.
- Features (card): "Accurate **word-level** and **segment-level** timestamps"; "**Long audio** transcription, supporting audio **up to 24 minutes** long with full attention (on A100 80GB) or up to 3 hours with local attention."
- Files (API, bytes): `model.safetensors` 2508311120, `parakeet-tdt-0.6b-v3.nemo` 2509332480, `parakeet-tdt-0.6b-v3.q8_0.gguf` 713975456, `tokenizer.json` 1159960, `.eval_results/open_asr_leaderboard.yaml`.

## How to run here

- **No clone.** Card: `curl -s https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3/raw/541d1f99c6b0c3cd0b11a95167540bb8edefd82b/README.md`; metadata: `https://huggingface.co/api/models/nvidia/parakeet-tdt-0.6b-v3?blobs=true`.
- **Runtimes**:
  - NeMo-Speech.cpp, named on the card: `nemo-speech transcribe audio.wav --model models/parakeet-tdt-0.6b-v3.q8_0.gguf`.
  - whisper.cpp `parakeet-cli` (`examples/parakeet-cli/README.md` at `v1.9.5`, read through `gh api`): its own conversion, `hf download ggml-org/parakeet-GGUF ggml-parakeet-tdt-0.6b-v3-f16.bin`; options `-m`, `-f`, `-t`, `-ng`, `-ps` ("print segment information"); "supported audio formats: flac, mp3, ogg, wav". The Homebrew `whisper.cpp` 1.9.5 bottle installs `parakeet-cli` (seen on this machine on 2026-11-21). On its first run on an Apple M4 here, `parakeet-cli --help` printed ggml compiling Metal libraries one by one ("compiled 'fa_aux' library in 3.619 sec" and similar lines), so the first start is slow.
  - NVIDIA NeMo (PyTorch).
- **Outbound calls**: the file download only.
- **Install steps to avoid**: NeMo and PyTorch in the kit's Python; a trial uses the GGUF files in a throwaway folder after the user's yes.

## Parts (variants)

- `q8_0.gguf`: 713975456 bytes, for NeMo-Speech.cpp.
- `ggml-parakeet-tdt-0.6b-v3-f16.bin` (ggml-org/parakeet-GGUF): for whisper.cpp `parakeet-cli`; size not read.
- `.nemo`: 2509332480 bytes, for NeMo.
- `model.safetensors`: 2508311120 bytes.
