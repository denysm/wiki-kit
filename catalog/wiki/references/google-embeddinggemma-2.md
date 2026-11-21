---
title: "google/embeddinggemma-2"
category: reference
kind: model
areas: [search-and-embeddings, knowledge-bases]
url: https://huggingface.co/google/embeddinggemma-2
version: "f9972ac"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/google-embeddinggemma-2-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-embeddinggemma-2-ollama-search-by-meaning.md
  - raw/notes/trials/2026-11-21-embeddinggemma-2-q8-0-llama-server-index.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, area-knowledge-bases, kind-model, embeddings, search, ollama, gguf]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Google's multimodal embedding model whose 270M text backbone, as the 8-bit Ollama tag embeddinggemma-2:270m-q8_0-text, is in use for search by meaning over Markdown knowledge bases on one machine. Chosen on measured recall over bge-m3 and Qwen3-Embedding-4B; the ONNX route is rejected, the other quantizations and tags are listed."
---

# google/embeddinggemma-2

> A Hugging Face model (kind `model`, licence Apache-2.0, revision `f9972ac` read): Google DeepMind's embedding model with a 270M-parameter text backbone and optional vision and audio encoders, 768 numbers per vector. The 8-bit text-only Ollama tag `embeddinggemma-2:270m-q8_0-text` is in use as the kit's search-by-meaning model; weights are not downloaded to read the card.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Find pages written in other words or in another language than the question, in a local Markdown knowledge base, with no data leaving the machine | `embeddinggemma-2:270m-q8_0-text` | search-and-embeddings |
| Add search by meaning to an agent-maintained knowledge base, with words as the fallback when the server is off | `embeddinggemma-2:270m-q8_0-text` | knowledge-bases |
| Embed text with a small model on a laptop through llama.cpp's server, outside Ollama | `embeddinggemma-2-Q8_0.gguf` | search-and-embeddings |
| Shrink the index of a very large body of chunks | `256 of 768 numbers` | search-and-embeddings |
| Not this: embed in the Python process through ONNX Runtime. Rejected: 1,246 s to index and 6.3 GB peak against 439 s and 275-282 MB through Ollama, and `search.py` would depend on a venv's Python | `ONNX int8 in ONNX Runtime` | search-and-embeddings |

## Run it here

- **No clone.** Read the card with `curl -s https://huggingface.co/google/embeddinggemma-2/raw/main/README.md` and the metadata with `https://huggingface.co/api/models/google/embeddinggemma-2`; the desk check read both at revision `f9972ac`.
- **In use**: the Ollama tag `embeddinggemma-2:270m-q8_0-text` (304 MB), served by the Ollama app `0.40.16` (see the Ollama card), called by `search.py` for search by meaning; the model revision read is `f9972ac`. `search.py embed-setup` writes the config; `search.py index ROOT` builds the vectors (minutes once, then seconds per new file). A pulled model never changes by itself; the index keeps the model name, prompts and dims and rebuilds the vectors when any changes.
- **Prompts**: query `task: search result | query: {text}`, document `title: {title} | text: {text}`, as the card's task prefixes and the kit's preset.
- **Switch off**: `search.py embed-setup --off`; search then runs on words alone. Pulling the model is the only outbound call; the model runs locally.
- **Do not install**: `sentence-transformers` or `transformers` to run the safetensors file, or the ONNX route; real installation of anything waits for the user's yes.

## What's inside

Parts are variants. Sizes are as the sources give them; "from metadata" means taken from a file listing or the Ollama tags page, not read or run.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `embeddinggemma-2:270m-q8_0-text` | Ollama tag, text only, 8-bit, 304 MB, 768 numbers; recall 0.93/0.95 vectors only and 0.98/1.00 with words and translations on 44 questions; index of both roots 442 s. | in use | The Ollama app and a one-time pull (304 MB); about 472 MB while the model is loaded; no GPU server | Re-check when `search.py eval` on a larger body of text shows a challenger finding at least 3 more questions at recall@5, or on a new revision of the model. |
| `embeddinggemma-2-Q8_0.gguf` | Q8_0 GGUF (unsloth/embeddinggemma-2-GGUF), 309855520 bytes; on llama.cpp `llama-server` `0.7.0`: index 357 s, server peak 656 MB, 13 ms per query. | tried | A clone of llama.cpp and the 310 MB file; Apple M4 Pro (Metal) in the trial | The real task that would move it to `in use`: a machine where Ollama cannot be installed. |
| `256 of 768 numbers` | Matryoshka truncation: vectors only 0.89/0.93 without translations, no loss with them on this set; float16 index smaller. | reference | A `dims: 256` config; no extra download | Consult when one knowledge-base root passes about 100,000 chunks. |
| `ONNX int8 in ONNX Runtime` | int8 model in the Python process, ONNX Runtime 1.32 on the CPU: same recall (cosine 0.9998), 1,246 s to index, 6.3 GB peak, 42 ms per answer. | rejected | A venv with onnxruntime, tokenizers and numpy (136 MB) | Revisit only if `search.py` must run with no server at all and indexing time stops mattering. Rejected: slower, far more memory, a Python dependency. |
| `model.safetensors` | The repository's BF16 checkpoint, 744371512 parameters with the vision and audio encoders. | listed | `sentence-transformers`, a GPU or a slow CPU pass | Read when a task needs images, video or audio embedded with the full model. |
| `embeddinggemma-2-BF16.gguf`, `embeddinggemma-2-F16.gguf` | Unquantized GGUF files, 557950240 bytes each (from metadata). | listed | A llama.cpp server | Read when 8-bit recall is in doubt. |
| `embeddinggemma-2-UD-Q4_K_XL.gguf`, `embeddinggemma-2-UD-Q5_K_XL.gguf`, `embeddinggemma-2-UD-Q6_K_XL.gguf` | Smaller quantizations, 175673856, 210055680 and 248812032 bytes (from metadata). | listed | A llama.cpp server | Read when the 304 MB download is too large. |
| `mmproj-BF16.gguf`, `mmproj-F16.gguf`, `mmproj-Q8_0.gguf` | Projector files for the vision and audio encoders, 982074880, 980895232 and 554821120 bytes (from metadata). | listed | A multimodal-capable llama.cpp build | Read when a task embeds images or audio. |
| `270m-bf16-text`, `270m-mxfp8-text`, `270m-nvfp4-text` | Other text-only Ollama tags: 574MB, 442MB and 378MB (from the tags page). | listed | The Ollama app | Read when the 8-bit tag is replaced. |
| `440m-bf16-text-vision`, `440m-mxfp8-text-vision`, `440m-nvfp4-text-vision`, `440m-q8_0-text-vision` | Text and vision Ollama tags: 910MB, 778MB, 714MB, 671MB. | listed | The Ollama app | Read when images must be embedded with the text. |
| `570m-bf16-text-audio`, `570m-mxfp8-text-audio`, `570m-nvfp4-text-audio`, `570m-q8_0-text-audio` | Text and audio Ollama tags; `570m-bf16-text-audio` is 1.2GB and `570m-mxfp8-text-audio` is 1.1GB (the other two sizes not read). | listed | The Ollama app | Read when audio must be embedded with the text. |
| `740m-bf16`, `740m-mxfp8`, `740m-nvfp4`, `740m-q8_0` | All encoders in one Ollama tag; the `latest` tag is 1.3GB (the four sizes not read). | listed | The Ollama app | Read when all modalities share one tag. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-13 | Benchmark an embedding model for hybrid search over two Markdown knowledge-base roots | `embeddinggemma-2-Q8_0.gguf` | Recall 0.93/0.95 vectors only; Ollama's vectors equal llama-server's (mean cosine 1.0000). | Index 357 s | [trial record](../../raw/notes/trials/2026-11-21-embeddinggemma-2-q8-0-llama-server-index.md) |
| 2026-11-14 | Search by meaning over Markdown knowledge bases, kept always on | `embeddinggemma-2:270m-q8_0-text` | In use: 43/44 at recall@5 and 44/44 at recall@10 with variants; whole query 0.183 s with vectors. | Index of both roots 442 s | [use record](../../raw/notes/trials/2026-11-21-embeddinggemma-2-ollama-search-by-meaning.md) |

## Verdict

The text-only 8-bit Ollama tag is the kit's embedding model: it matches bge-m3 within one question, indexes 1.6 times faster and is half the download. The llama-server build is a working alternative, the ONNX route is rejected, and the other quantizations and modality tags wait for a task. Revisit when `search.py eval` on a much larger body shows a challenger ahead by at least 3 questions at recall@5 (compare bge-m3 first), or when the model gets a new revision. Not measured: clean Mac, Windows, Linux; MLX; 4-bit weights.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; the model, its runtimes and variants
- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page; the in-use tag serves search over the articles
- [[baai-bge-m3|BAAI/bge-m3]] (../references/baai-bge-m3.md): the runner-up on the same measurements
- [[qwen-qwen3-embedding-4b|Qwen/Qwen3-Embedding-4B]] (../references/qwen-qwen3-embedding-4b.md): the larger model that bought nothing measurable
- [[ollama-ollama|ollama/ollama]] (../references/ollama-ollama.md): the runtime that serves the in-use tag

## Sources

- [Desk check: google/embeddinggemma-2 revision f9972ac](../../raw/repos/google-embeddinggemma-2-desk-check-2026-11-21.md): the model card and API metadata read, variants and tags listed.
- [Use record: EmbeddingGemma 2 through Ollama](../../raw/notes/trials/2026-11-21-embeddinggemma-2-ollama-search-by-meaning.md): the real use behind `in use`.
- [Trial record: Q8_0 GGUF on llama-server](../../raw/notes/trials/2026-11-21-embeddinggemma-2-q8-0-llama-server-index.md): the run behind `tried`.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): recall, speed, memory and the choice, retold.
