---
title: "NVIDIA-BioNeMo/bionemo-recipes"
category: reference
kind: library
areas: [science]
science_sections: [protein-engineering-and-design, machine-learning-and-ai, infrastructure-and-platforms]
repo: NVIDIA-BioNeMo/bionemo-recipes
version: "3.0.0"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/nvidia-bionemo-bionemo-recipes-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, kind-library, bionemo, transformer-engine, esm2, evo2, codonfm, geneformer, fsdp, fp8, sparse-autoencoders]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "NVIDIA's reference training recipes and TransformerEngine model classes for biological foundation models (ESM-2, AMPLIFY, CodonFM, Geneformer, Evo2, Eden, Llama-style DNA models), plus sparse autoencoders for interpretability. The old NVIDIA/bionemo-framework repository now redirects here. Read at v3.0.0: every part needs an NVIDIA GPU and its container except the FP8 log analyser; all 24 parts are candidates."
---

# NVIDIA-BioNeMo/bionemo-recipes

> Reference training recipes and Hugging Face model classes with TransformerEngine layers for biological foundation models (kind `library`, version `3.0.0` read). Code licence Apache 2.0 (`LICENSE/license.txt`; GitHub detects none), with `models/amplify` under MIT; model weights carry their own terms, from MIT for the ESM-2 and AMPLIFY checkpoints to the NVIDIA Open Model License for CodonFM. The old `NVIDIA/bionemo-framework` repository redirects here. Parts are meant to be read and adapted, not pip-installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Pretrain or continue pretraining a protein language model (ESM-2 or AMPLIFY) on one or many NVIDIA GPUs, with low precision and sequence packing | `recipes/esm2_native_te` | science-protein-engineering-and-design |
| Train ESM-2 through the Hugging Face Trainer and Accelerate config files instead of a hand-written loop | `recipes/esm2_accelerate_te` | science-protein-engineering-and-design |
| Fine-tune ESM-2 with LoRA for a per-residue label such as secondary structure, then predict on a FASTA file | `recipes/esm2_peft_te` | science-protein-engineering-and-design |
| Embed many protein sequences with ESM-2 on a GPU server | `recipes/vllm_inference/esm2` | science-protein-engineering-and-design |
| Load a faster ESM-2 or AMPLIFY checkpoint through `transformers` for embeddings or masked-token logits | `models/esm2`, `models/amplify` | science-protein-engineering-and-design |
| Train or fine-tune a codon language model, or score codon variants zero-shot | `recipes/codonfm_ptl_te` | science-machine-learning-and-ai |
| Pretrain a single-cell gene-expression model (Geneformer) | `recipes/geneformer_native_te_mfsdp_fp8` | science-machine-learning-and-ai |
| Train, fine-tune, generate with or score DNA with Evo2, and convert its checkpoints | `recipes/evo2_megatron` | science-machine-learning-and-ai |
| Train a Llama-style DNA model on OpenGenome2 metagenomes | `recipes/opengenome2_llama_native_te` | science-machine-learning-and-ai |
| Find interpretable features inside a protein, codon or DNA language model with sparse autoencoders | `interpretability/sparse_autoencoders/sae` | science-machine-learning-and-ai |
| Train a vision transformer on images with Megatron-FSDP | `recipes/vit` | science-machine-learning-and-ai |
| Make transformer training faster on NVIDIA GPUs: TransformerEngine layers, FSDP2, FP8 or MXFP8, context parallelism | `recipes/llama3_native_te` | science-infrastructure-and-platforms |
| Find which layers underflow when training in FP8, from the training logs | `recipes/fp8_analysis` | science-infrastructure-and-platforms |
| Convert Llama 3, Qwen or Mixtral checkpoints to TransformerEngine layers and back | `models/llama3`, `models/qwen`, `models/mixtral` | science-infrastructure-and-platforms |

## Run it here

- **Clone**: `git clone --depth 1 --branch v3.0.0 https://github.com/NVIDIA-BioNeMo/bionemo-recipes $EXTERNAL/bionemo-recipes`, read-only. Never edit the clone.
- **Version**: `3.0.0`, the latest release, published 2026-06-24. Releases are rolling: the tag "simply marks a reference point", and `main` was 48 commits ahead at the check. Compare before relying on this card: `gh api repos/NVIDIA-BioNeMo/bionemo-recipes --jq .pushed_at` and `gh api repos/NVIDIA-BioNeMo/bionemo-recipes/compare/v3.0.0...main --jq .ahead_by`. `VERSION` in the tag reads `2.7`.
- **Read**: `README.md`, then the part's own `README.md` and, for native PyTorch recipes, `hydra_config/L0_sanity.yaml` (local data, W&B `offline`).
- **Hardware**: every part except `recipes/fp8_analysis` runs in its own Docker image built from an NGC PyTorch container with `--gpus all`; FP8 needs compute capability 9.0 (Hopper) or newer, MXFP8 and NVFP4 need Blackwell. No part states a GPU memory minimum. Not checked: any part on a machine without an NVIDIA GPU.
- **Sends outward**: Weights & Biases from the training loops; the Hugging Face Hub for checkpoints, tokenizers and default datasets; NGC for Evo2 and Eden checkpoints (`download_bionemo_data`, guest sign-in without a key); UniProt, GitHub and dataset hosts for some recipes; an LLM API (Anthropic by default, OpenAI or NVIDIA NIM) only when the CodonFM SAE analysis gets `--auto-interp`. Exported ESM-2 checkpoints load model code shipped with the weights (`trust_remote_code=True`). No telemetry outside NVIDIA's own CI scripts.
- **Switch off**: `WANDB_MODE=disabled`; download datasets once and run with `HF_DATASETS_OFFLINE=1` and a local path; leave `--auto-interp` off; point `BIONEMO_CACHE_DIR` at a scratch folder.
- **Do not install**: no `docker build`, `uv sync`, `pip install`, `.ci_build.sh`, `install_vllm.sh` or `install_hybridep.sh` here, and no `pre-commit install`. Never open the clone in its dev container: it bind-mounts the host's `~/.ssh`, `~/.gnupg`, `~/.netrc` and `~/.claude` into the container. Start coding-agent sessions outside the clone (its root `CLAUDE.md` holds contributor rules). A real run waits for the user's yes and an NVIDIA GPU host.

## What's inside

Parts: 13 recipe folders, 7 model packages, and the sparse-autoencoder library with 3 recipes. Every part was read; none was run.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `recipes/esm2_native_te` | ESM-2 (and AMPLIFY in BF16) training with a plain PyTorch loop: DDP, FSDP2, Megatron-FSDP, sequence packing, FP8, MXFP8, NVFP4, context parallelism; configs from `L0_sanity` to `L1_15B_perf_test`. | candidate | An NVIDIA GPU and the recipe's container (or Python 3.12, `torch==2.9.0`, `transformer-engine[pytorch]==2.9.0`); the default dataset streams from the Hub; W&B on unless disabled | Try it when a protein language model must be pretrained or continued on GPUs; start with `L0_sanity`. |
| `recipes/esm2_accelerate_te` | ESM-2 or AMPLIFY training through the Hugging Face Trainer, with FSDP, DeepSpeed and FP8 chosen by Accelerate config files. | candidate | An NVIDIA GPU and the container; dataset `chandar-lab/UR100P` from the Hub | Try it when a team already trains with the Hugging Face Trainer and wants TE speed-ups. |
| `recipes/esm2_peft_te` | LoRA fine-tuning of ESM-2 for per-residue secondary structure, and inference from FASTA to CSV; ships a sanity dataset and builds the Porter6 sets. | candidate | An NVIDIA GPU and the container; the Porter6 download from GitHub | Try it on a per-residue labelling task for proteins with a few thousand labelled sequences. |
| `recipes/vllm_inference/esm2` | Serves exported ESM-2 checkpoints in vLLM as a pooling model and returns embeddings; golden-value tests against Hugging Face. | candidate | An NVIDIA GPU; vLLM `v0.15.1` compiled for the GPU's CUDA architecture; `trust_remote_code=True` | Try it when embeddings are needed for a large set of protein sequences. |
| `recipes/codonfm_native_te` | CodonFM training with a plain PyTorch loop: FSDP2, sequence packing, FP8 and NVFP4, using TE's standard transformer layer. | candidate | An NVIDIA GPU and the container; no checkpoint from this recipe is published yet | Try it when a codon model must be trained from scratch with FSDP2. |
| `recipes/codonfm_ptl_te` | TE-accelerated reproduction of CodonFM on PyTorch Lightning: pretraining, fine-tuning, LoRA, data curation, checkpoint conversion, notebooks for zero-shot variant scoring and mRNA tasks; EnCodon 80M to 1B. | candidate | An NVIDIA GPU and its own container; weights under the NVIDIA Open Model License; notebooks download their data; W&B only with `--enable_wandb` | Try it when codon-level variant effects or mRNA expression or stability must be predicted. |
| `recipes/geneformer_native_te_mfsdp_fp8` | Geneformer pretraining on single-cell transcriptomes with Megatron-FSDP and FP8; configs `10m`, `106m`, `4b`; ships 500 tokenized samples. | candidate | An NVIDIA GPU and the container; FP8 needs compute capability 8.9 or newer; W&B needs an API key | Try it when a single-cell foundation model must be pretrained or scaled. |
| `recipes/llama3_native_te` | Llama 3 training with a plain PyTorch loop, set up for genomic sequences: FP8, MXFP8, NVFP4, packing, context parallelism, profiling, KV-cache inference, export to Hugging Face. | candidate | An NVIDIA GPU and the container; local test data by default; W&B on unless disabled | Try it when a decoder model must be trained on long sequences across several GPUs. |
| `recipes/opengenome2_llama_native_te` | Llama 3 next-token training on the OpenGenome2 metagenome subset with FSDP2, THD packing and FP32 master weights; a 7B model with grouped-query attention. | candidate | NVIDIA GPUs (the README's runs used 48 H100) and the container; `arcinstitute/opengenome2` from the Hub, resharded with DuckDB | Try it when a DNA language model must be trained on metagenomes. |
| `recipes/evo2_megatron` | Evo2 (Striped Hyena) on Megatron Bridge: train, LoRA fine-tune, generate (`infer_evo2`), score FASTA (`predict_evo2`), preprocess, splice transcripts, convert NeMo2, Savanna and Vortex checkpoints; 1B to 40B models. | candidate | NVIDIA GPUs (Hopper for FP8 checkpoints); the container or the venv from `.ci_build.sh`; checkpoints from NGC or the Hub | Try it when DNA sequences must be scored or generated with Evo2, or Evo2 fine-tuned. |
| `recipes/eden_megatron` | Eden genomic models (Llama 3.1 architecture, 100M to 35B) on Megatron Bridge: train, generate, score FASTA, convert to and from Hugging Face. | candidate | NVIDIA GPUs; the container or the built venv; a SQLite-backed sharded dataset | Try it when an Eden checkpoint must be fine-tuned or used for scoring. |
| `recipes/vit` | Vision transformer training and inference with Megatron-FSDP and TransformerEngine on the beans image dataset. | candidate | An NVIDIA GPU and the container with `--shm-size=16G`; dataset download from the Hub | Try it when an image model must be trained with sharded data parallelism. |
| `recipes/fp8_analysis` | Parses FP8 statistics logs from ESM-2 or Llama 3 runs, draws heatmaps of gradient underflow per layer over time, exports CSV. | candidate | No GPU: a venv with `matplotlib`, `numpy`, `pandas`, `seaborn`, or the `python:3.12-slim` container; FP8 logs from a training run (sample logs ship with it) | Try it after an FP8 training run whose loss diverges from the BF16 run. |
| `models/esm2` | ESM-2 classes with TE layers, Hugging Face to TE conversion and back, Hub export; six checkpoints from 8M to 15B parameters converted from the original weights. | candidate | An NVIDIA GPU and TransformerEngine; the checkpoint from the Hub (weights MIT); model code from the checkpoint | Try it when ESM-2 inference or fine-tuning is too slow with the original classes. |
| `models/amplify` | AMPLIFY protein BERT with TE layers; checkpoints 120M and 350M; FP8 and export under development. | candidate | An NVIDIA GPU and TransformerEngine (container `nvcr.io/nvidia/pytorch:25.01-py3`); folder licence MIT | Try it when an AMPLIFY model is compared with ESM-2 on a protein task. |
| `models/geneformer` | Converts Geneformer V1 and V2 checkpoints (10M to 316M) to TE format. | candidate | An NVIDIA GPU and TransformerEngine; source checkpoints from the Hub | Try it when Geneformer inference must run faster or in FP8. |
| `models/codonfm` | CodonFM masked language model with TE layers, its tokenizer and dataset code; no README. | candidate | An NVIDIA GPU, `torch`, `transformer_engine[pytorch]`, `transformers` | Read it with `recipes/codonfm_native_te` when that recipe is tried. |
| `models/llama3` | Llama 3 classes with TE layers, conversion from Hugging Face checkpoints, KV-cache inference with beam search; no pre-converted checkpoints published. | candidate | An NVIDIA GPU and TransformerEngine; access to the gated Llama weights on the Hub | Try it when a Llama 3 checkpoint must be trained or served with TE. |
| `models/mixtral` | Mixture-of-experts classes with TE grouped linear layers and expert parallelism; optional fused DeepEP router. | candidate | Several NVIDIA GPUs; TransformerEngine; DeepEP and NVLink peer access only for the fused router | Try it when a mixture-of-experts model must be trained across GPUs. |
| `models/qwen` | Qwen2.5 and Qwen3 classes with TE layers, conversion scripts, KV-cache inference. | candidate | An NVIDIA GPU and TransformerEngine | Try it when a small Qwen model must be fine-tuned with TE speed-ups. |
| `interpretability/sparse_autoencoders/sae` | Domain-agnostic sparse autoencoder library: ReLU-L1, Top-K and MoE architectures, trainer, evaluation, LLM feature labelling, React dashboard; an early release. | candidate | A uv venv (`torch>=2.0`); a GPU for real runs; an LLM API key only for feature labelling; Node for the dashboard | Try it when the features a biological language model learned must be inspected. |
| `interpretability/sparse_autoencoders/recipes/esm2` | Extracts ESM-2 activations, trains a TopK SAE, scores features against Swiss-Prot annotations, builds a dashboard; configs for 650M, 3B, 15B. | candidate | NVIDIA GPUs; UniProt downloads or a local FASTA; ESM-2 checkpoints from the Hub | Try it when protein language model features must be mapped to known protein annotations. |
| `interpretability/sparse_autoencoders/recipes/codonfm` | Extracts Encodon activations, trains and evaluates an SAE, annotates features (codon usage, amino acid, wobble position, CpG), optional LLM labels and dashboard. | candidate | NVIDIA GPUs; the Encodon 1B checkpoint; a CSV of coding sequences; an LLM API key only with `--auto-interp` | Try it after a codon model is in use and its features need explaining. |
| `interpretability/sparse_autoencoders/recipes/evo2` | Chunks a FASTA, streams Evo2 activations of one layer, trains an SAE; scripts only, no README. | candidate | NVIDIA GPUs; the venv of `recipes/evo2_megatron`; an Evo2 7B checkpoint | Try it after `recipes/evo2_megatron` runs and its features need explaining. |

## Tried

None yet: no part has been run, in a sandbox or in real work.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

A reference set to read and adapt, not a package to install: every part was read, all 24 are candidates, and none runs without an NVIDIA GPU host and its container except the FP8 log analyser. The protein recipes and model classes are the likeliest first use; the genomic recipes and the sparse autoencoders follow the models they wrap. Revisit when a task needs ESM-2, Evo2, CodonFM or Geneformer trained, fine-tuned or scored on GPUs, and on every check where `main` has moved far past `3.0.0`, since releases are rolling.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; sections protein engineering and design, machine learning and AI, infrastructure and platforms
- [[facebookresearch-esm|facebookresearch/esm]] ([facebookresearch/esm](../references/facebookresearch-esm.md)): the original ESM-2 code and weights that `models/esm2` converts
- [[deepchem-deepchem|deepchem/deepchem]] ([deepchem/deepchem](../references/deepchem-deepchem.md)): another machine-learning library for drug discovery in the catalog

## Sources

- [Desk check: NVIDIA-BioNeMo/bionemo-recipes v3.0.0](../../raw/repos/nvidia-bionemo-bionemo-recipes-desk-check-2026-11-21.md): every part read from the clone, licences of code and weights, the redirect from the old repository, freshness through the GitHub API, outbound calls and what to avoid.
