---
title: "Desk check: google/embeddinggemma-2 revision f9972ac"
source: https://huggingface.co/google/embeddinggemma-2/tree/f9972ac22e696a105c482202646979e33e4b5a1e
type: repos
authors: ["Google DeepMind"]
source_date: 2026-10-28
ingested: 2026-11-21
url: https://huggingface.co/google/embeddinggemma-2
kind: model
version: "f9972ac"
licence: Apache-2.0
tags: [catalog, desk-check, kind-model, embeddings, search, huggingface, ollama]
summary: "EmbeddingGemma 2 read from its Hugging Face model card and API metadata at revision f9972ac: a multimodal embedding model with a 270M-parameter text backbone, 768 numbers per vector; its GGUF quantizations, its Ollama library tags, the Ollama tag the kit uses for search by meaning and why it was chosen. No weights downloaded."
---

# Desk check: google/embeddinggemma-2 revision f9972ac

## Repository facts

- Model page: https://huggingface.co/google/embeddinggemma-2, revision read `f9972ac22e696a105c482202646979e33e4b5a1e` (short form `f9972ac`). Author: Google DeepMind. Not gated.
- Card header: `license: apache-2.0`, `pipeline_tag: feature-extraction`, `library_name: transformers`, languages `multilingual`. The card text says: "License: Apache 2.0". There is no separate licence file in the repository listing; the licence is read from the card and the API tag `license:apache-2.0`.
- What it is, in the card's words: "an open multimodal embedding model built by Google DeepMind which maps text (incl. code), images, video, and audio inputs ... into a single, unified 768-dimensional vector space". It has 740M total parameters: a 270M text model (130M transformer plus 140M embedder) with vision (170M) and audio (300M) encoders that can be loaded selectively. The API reports 744371512 parameters in BF16 for the safetensors file.
- Context window 8,192 tokens on the card; the GGUF metadata (below) reports a context length of 262144.
- Matryoshka truncation to 128, 256, 512 or 768 numbers; the card's table gives MTEB (multilingual, v2) 61.36 at 768 numbers and 60.41 at 256.
- Task prefixes: the card says each input is "trained with short task instruction prefixes"; documents with a title are formatted `title: {title} | text: {content}`. The kit's `search.py` preset uses `task: search result | query: {text}` for queries and `title: {title} | text: {text}` for documents.
- Files in the model repository: `model.safetensors`, tokenizer files, sentence-transformers configs (`1_Pooling`, `2_Normalize`), `README.md`. No GGUF in this repository.

## Freshness (checked 2026-11-21)

Read through the Hugging Face API, not `gh`: created 2026-09-14, last modified 2026-10-28, no tag other than `license:apache-2.0` and `arxiv:2610.37364` for licence or paper. Not gated, not marked deprecated. The measurements below were made on the model as Ollama and the GGUF publishers shipped it, not on this repository's safetensors file.

## How to run here

- No clone: the model page is read through `curl -s https://huggingface.co/google/embeddinggemma-2/raw/main/README.md` and `https://huggingface.co/api/models/google/embeddinggemma-2`. Do not download the weights to read the card.
- What is run here is the Ollama build `embeddinggemma-2:270m-q8_0-text` (text only, 8-bit), served by the Ollama app; see the use record named under Parts and the Ollama card. Nothing is installed by reading the card.
- Outbound calls: pulling the model contacts the Ollama registry once; after that the model runs on the machine. A pulled model never changes by itself (the measurement note).
- Do not install: `sentence-transformers` or `transformers` to run the safetensors file; the full 740M multimodal checkpoint is not needed for text search.

## Parts

Parts are variants, as `schema.md` says for a model.

### Ollama tag `embeddinggemma-2:270m-q8_0-text`

Taken from the Ollama library page `https://ollama.com/library/embeddinggemma-2/tags`: digest `c21dd30c1e38`, 304MB, 256K context window. This is the text-only 270M model at 8-bit. The measurement note gives 304 MB for it and calls it the choice. Status basis: use record `raw/notes/trials/2026-11-21-embeddinggemma-2-ollama-search-by-meaning.md`.

### Q8_0 GGUF `embeddinggemma-2-Q8_0.gguf` (unsloth/embeddinggemma-2-GGUF, revision `031f0d4`, Apache-2.0)

Size 309855520 bytes, which is consistent with the 310 MB the measurement note gives for the Q8_0 file it ran; which publisher's file that run used is not recorded. Metadata: architecture `gemma-embedding2`, context_length 262144, pooling type 1, 271002648 parameters in the GGUF header. Measured on llama.cpp `llama-server` 0.7.0 (Metal): see trial record `raw/notes/trials/2026-11-21-embeddinggemma-2-q8-0-llama-server-index.md`. Status basis: that record.

### Other GGUF files in unsloth/embeddinggemma-2-GGUF

From the file listing (sizes in bytes), not read or tried: `embeddinggemma-2-BF16.gguf` 557950240, `embeddinggemma-2-F16.gguf` 557950240, `embeddinggemma-2-UD-Q4_K_XL.gguf` 175673856, `embeddinggemma-2-UD-Q5_K_XL.gguf` 210055680, `embeddinggemma-2-UD-Q6_K_XL.gguf` 248812032, and three projector files for the vision and audio encoders: `mmproj-BF16.gguf` 982074880, `mmproj-F16.gguf` 980895232, `mmproj-Q8_0.gguf` 554821120. A text-only search does not need the projector files.

### Other Ollama library tags

From the Ollama tags page, not tried. Text only, 270m: `270m-bf16-text` 574MB, `270m-mxfp8-text` 442MB, `270m-nvfp4-text` 378MB. Text and vision, 440m: `440m-bf16-text-vision` 910MB, `440m-mxfp8-text-vision` 778MB, `440m-nvfp4-text-vision` 714MB, `440m-q8_0-text-vision` 671MB. Text and audio, 570m: `570m-bf16-text-audio` 1.2GB, `570m-mxfp8-text-audio` 1.1GB, `570m-nvfp4-text-audio`, `570m-q8_0-text-audio` (sizes of these two not read). All encoders, 740m: `740m-bf16`, `740m-mxfp8`, `740m-nvfp4`, `740m-q8_0` (sizes not read; the `latest` tag is 1.3GB).

### Safetensors `model.safetensors` (this repository)

BF16, 744371512 parameters including the vision and audio encoders. Not tried: running it needs `sentence-transformers` and a GPU or a slow CPU pass, and the runtime comparison below shows the Ollama route gives the same vectors from the 8-bit build.

### ONNX int8 model in ONNX Runtime

Not from this repository (a separate `onnx-community/embeddinggemma-2-ONNX` listing exists; not read). The measurement note ran an int8 ONNX model in the Python process through ONNX Runtime 1.32 on the CPU. Rejected, reason as the note gives it: same recall (cosine 0.9998) but 1,246 s to index, 6.3 GB peak, 42 ms per answer, and it would make `search.py` depend on a venv's Python.

### Shorter vectors (Matryoshka, 256 of 768 numbers)

A setting of the model, not a file. Measured: cost 2 questions without translations (vectors only 0.89/0.93) and none with them; float16 index smaller; full vectors stay the default. Status basis: this section and the measurement note; reference.

## Reasons for any rejection or reference status

- ONNX int8 on CPU: rejected for the dependency on a venv's Python, 1,246 s against 439 s through Ollama, and 6.3 GB peak against 275-282 MB.
- 256 numbers: reference. It is the first lever when one knowledge-base root passes about 100,000 chunks (the note says so), measured before it would ship.

## How the kit uses it

`search.py embed-setup` writes the config for `embeddinggemma-2:270m-q8_0-text` through Ollama; vectors are scored with numpy. Chosen on measurements of recall on a fixed set of 44 questions: it matches bge-m3 within one question, indexes 1.6 times faster and is half the download. Details and numbers: `raw/notes/2026-11-21-measurements-local-embeddings.md`. The Ollama docs in the app's repository name this model `embeddinggemma2` in API examples; the tag the kit pulls is the one in `search.py`, and the library page lists it as written above.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 42 model calls on sonnet, $1.95 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
