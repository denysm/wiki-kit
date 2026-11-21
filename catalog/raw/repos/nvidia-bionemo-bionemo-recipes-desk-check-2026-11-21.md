---
title: "Desk check: NVIDIA-BioNeMo/bionemo-recipes v3.0.0"
source: https://github.com/NVIDIA-BioNeMo/bionemo-recipes/tree/v3.0.0
type: repos
authors: ["BioNeMo Team (NVIDIA)"]
source_date: 2026-06-24
ingested: 2026-11-21
repo: NVIDIA-BioNeMo/bionemo-recipes
kind: library
version: "3.0.0"
licence: Apache-2.0
tags: [catalog, desk-check, kind-library, bionemo, transformer-engine, protein-language-models, genomic-models, fsdp, fp8, sparse-autoencoders]
summary: "Every part of NVIDIA-BioNeMo/bionemo-recipes v3.0.0 read from a read-only clone: 13 recipe folders, 7 model packages, the sparse-autoencoder library and its 3 recipes; licences of code and weights; the redirect from NVIDIA/bionemo-framework; outbound calls (Weights & Biases, Hugging Face Hub, NGC, an LLM API in one optional step) and how to switch them off; the dev container that mounts host secrets."
---

# Desk check: NVIDIA-BioNeMo/bionemo-recipes v3.0.0

Read from a shallow clone of tag `v3.0.0` (commit `66c150f2920d6155697d4edfc87289f239b65022`, committed 2026-06-24), at `$EXTERNAL/bionemo-recipes`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 3.0.0.

## Repository facts

- Description on GitHub: "BioNeMo Recipes: For building and adapting AI models in drug discovery at scale".
- README: the repository provides "**model checkpoints** with TransformerEngine (TE) layers and **training recipes**" rather than "a batteries-included training framework". Three kinds of component: `models/` (Hugging Face `PreTrainedModel` classes with TransformerEngine layers inside), `recipes/` (self-contained training examples, each "a complete Docker container"), and `interpretability/` (sparse autoencoders). "Recipes are **not pip-installable packages** but serve as reference implementations"; `models/README.md`: models "are **not intended to be pip-installed directly**" and users "will typically interact with these models by loading pre-converted checkpoints directly from the Hugging Face Hub".
- Kind recorded here: `library`, because the parts are model classes and training entry points to read and adapt; there is no app, CLI or package for the repository as a whole.
- Parts counted at the tag: 13 recipe folders under `recipes/` (`vllm_inference/` holds one, `esm2`), 7 model packages under `models/` (`amplify`, `codonfm`, `esm2`, `geneformer`, `llama3`, `mixtral`, `qwen`), and under `interpretability/sparse_autoencoders/` the `sae` library plus 3 recipes (`esm2`, `codonfm`, `evo2`). Not parts: `docs/` (the documentation site), `ci/` (the CI scripts), `recipes/context_parallel.md` (a note on context parallelism).
- `VERSION` at the tag reads `2.7`, not 3.0.0; the release tag is the version recorded here.
- Release notes of `v3.0.0`: "This marks the first release from BioNeMo Recipes, a lighter-weight version of the BioNeMo model training framework"; it "drops support for the monolithic `bionemo-framework` container, and instead opts for per-folder Dockerfiles"; "all further releases of BioNeMo Recipes will occur on a rolling basis — the `v3.0.0` tag simply marks a reference point"; "The best way to use these recipes is as reference files to your coding agent"; "Legacy `bionemo-framework` code can be found in the `bionemo2` branch."
- Many recipe READMEs still link to `NVIDIA-BioNeMo/bionemo-framework` paths and say a recipe "does not depend on any other code in the top-level bionemo-framework repository".
- Root `CLAUDE.md` and `AGENTS.md`: the same 58 lines of contributor rules (scope of changes, tests, Ruff). A coding-agent session started inside the clone would load them.

### Licences

- GitHub reports no licence (`license: null`), because the licence file sits in a folder: `LICENSE/license.txt` is the Apache License, Version 2.0; `LICENSE/third_party.txt` lists third-party attributions (among them PyFastx under MIT, the Meta ESM codebase under MIT, Hugging Face transformers, 3Dmol.js under BSD-3-Clause, DiffDock under MIT, OpenFold). README, "License": "This project is licensed under the terms described in [LICENSE/license.txt]".
- Per-folder licence files: `models/amplify/LICENSE` is MIT ("Copyright (c) 2024 chandar-lab"); `recipes/vit/LICENSE` is Apache 2.0 plus MIT notices for code adapted from pytorch-image-models, vit-pytorch, minGPT and the ibean dataset code; `models/esm2/LICENSE` is Apache 2.0 with "Copyright 2022 Meta and The HuggingFace Inc. team"; `models/geneformer`, `recipes/codonfm_ptl_te`, `recipes/evo2_megatron`, `recipes/eden_megatron`, `recipes/vllm_inference/esm2` and the two `example_8m_checkpoint` folders carry Apache 2.0 texts.
- Model weights have their own terms. Model card templates in the repository: `models/esm2/model_readme.template` and `models/amplify/model_readme.template` say `license: mit`; `models/geneformer/model_readme.md` says `license: apache-2.0`. `docs/docs/models/evo2.md`: "Use of this model is governed by the NVIDIA Open Model License Agreement" (for the NIM container of Evo2).
- Hugging Face API, checked 2026-11-21 (`https://huggingface.co/api/models/<id>`, field `cardData.license`): `nvidia/esm2_t6_8M_UR50D` and `nvidia/esm2_t48_15B_UR50D` `mit`; `nvidia/AMPLIFY_120M` `mit`; `nvidia/NV-CodonFM-Encodon-TE-80M-v1` and `nvidia/NV-CodonFM-Encodon-1B-v1` `other` with `license_name` `nvidia-open-model-license`; `arcinstitute/savanna_evo2_1b_base` `apache-2.0`; `ctheodoris/Geneformer` `apache-2.0`; none of these is gated. Source checkpoints named in the model READMEs: `meta-llama/Llama-3.2-1B-Instruct` `llama3.2`, gated `manual` (access must be requested); `mistralai/Mixtral-8x7B-v0.1` `apache-2.0`; `Qwen/Qwen3-0.6B` `apache-2.0`.

### Hardware stated by the repository

- README footnotes: FP8 "Requires compute capability 9.0 and above (Hopper+)"; MXFP8 "Requires compute capability 10.0 and 10.3 (Blackwell), 12.0 support pending"; NVFP4 "Requires compute capability 10.0 and above (Blackwell+)".
- Testing tiers in the README: L0 "<10 minutes, single GPU"; L1 "Up to 4 hours, up to 16 GPUs"; L2 "Multiple days, hundreds of GPUs". The recipes' unit-test CI job runs on the runner `linux-amd64-gpu-l4-latest-1`; `recipes/esm2_accelerate_te/README.md`: "Hardware requirements beyond those used in CI, like a single L4, should be annotated with pytest.mark.requires".
- The CI contract for every component: `docker build -t {component_tag} .` then `docker run --rm -it --gpus all {component_tag} pytest -v .`. No recipe states a GPU memory minimum.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/NVIDIA-BioNeMo/bionemo-recipes`: `pushed_at` 2026-11-13T11:36:43Z; licence `null` (not detected; see Licences); default branch `main`; not archived; created 2023-10-16T01:31:06Z.
- `gh api repos/NVIDIA/bionemo-framework` returns the same repository (`full_name` `NVIDIA-BioNeMo/bionemo-recipes`, same `created_at`). Without following redirects the API answers HTTP 301 to `https://api.github.com/repositories/705428944`, and the web page `https://github.com/NVIDIA/bionemo-framework` answers HTTP 301 to `https://github.com/NVIDIA-BioNeMo/bionemo-recipes`. So the old framework repository was renamed and moved; its old code is the `bionemo2` branch.
- `gh api repos/NVIDIA-BioNeMo/bionemo-recipes/releases/latest`: tag `v3.0.0`, name "v3.0.0 - BioNeMo Recipes", published 2026-06-24T18:26:26Z. The release before it: `v2.7`, published 2025-10-01T23:46:29Z.
- `gh api repos/NVIDIA-BioNeMo/bionemo-recipes/compare/v3.0.0...main`: `main` is 48 commits ahead of the tag. Releases are rolling, so a freshness check compares `main` as well as the latest tag.

## How to run here

- Clone: `git clone --depth 1 --branch v3.0.0 https://github.com/NVIDIA-BioNeMo/bionemo-recipes $EXTERNAL/bionemo-recipes`, read-only. Read `README.md`, then the part's own `README.md` and, for the native PyTorch recipes, `hydra_config/L0_sanity.yaml`.
- Running any part except `recipes/fp8_analysis` needs an NVIDIA GPU with CUDA: each recipe and model folder builds its own Docker image, run with `--gpus all`. Base images at the tag: `nvcr.io/nvidia/pytorch:26.04-py3` for most folders; `nvcr.io/nvidia/pytorch:25.01-py3` for `models/amplify`; `nvcr.io/nvidia/pytorch:25.08-py3` as the default for `recipes/codonfm_ptl_te`; `nvcr.io/nvidia/cuda:13.0.2-cudnn-devel-ubuntu24.04` for the alternative `Dockerfile.cuda` of `recipes/esm2_native_te`; `python:3.12-slim` for `recipes/fp8_analysis`. The model code imports `transformer_engine`. Not checked: any part on a machine without an NVIDIA GPU.
- Outbound calls found:
  - Weights & Biases. The native PyTorch recipes call `wandb.init(**args.wandb_init_args, config=self._run_config)` on the main process (`perf_logger.py`); `hydra_config/defaults.yaml` sets only a run `name`, the `L0_sanity` configs set `mode: "offline"`, and the tests set `WANDB_MODE` to `disabled`. `recipes/codonfm_ptl_te` logs to W&B only with `--enable_wandb` ("If these are omitted, WandB logging will be skipped"); `recipes/evo2_megatron` takes `--wandb-project` and `--wandb-entity`; `recipes/geneformer_native_te_mfsdp_fp8` asks for `WANDB_API_KEY`; the SAE trainer calls `wandb.init` when W&B is configured. Switch off: `WANDB_MODE=disabled` (or `offline`).
  - Hugging Face Hub. Configs, tokenizers and checkpoints (`nvidia/...`, `facebook/esm2_...`, `arcinstitute/...`) and datasets: `recipes/esm2_native_te` streams `nvidia/esm2_uniref_pretraining_data` by default; `recipes/esm2_accelerate_te` loads `chandar-lab/UR100P` by default; `recipes/opengenome2_llama_native_te` uses `arcinstitute/opengenome2`; `recipes/vit` downloads `AI-Lab-Makerere/beans`; `recipes/llama3_native_te` points to `mlfoundations/dclm-baseline-1.0` for its Lingua configs. The `L0_sanity` configs read local files (`train.parquet`, `test_genomic_sequences.parquet`, `genecorpus_500_samples.parquet`) and local tokenizers. Offline use, from `recipes/esm2_native_te/README.md`, "Downloading Pre-Training Data For Offline Training": download with `hf download`, then run with `HF_DATASETS_OFFLINE=1` and the local path; `HF_TOKEN` is set for the download.
  - NGC. `download_bionemo_data` (in `recipes/evo2_megatron` and `recipes/eden_megatron`) pulls checkpoints from NGC through `ngcsdk`; the key comes "from ~/.ngc/config, or from environment variables"; with a missing or invalid key it logs an error and continues "signing in as guest". Files are cached in `BIONEMO_CACHE_DIR`, default the user cache folder `bionemo`. Its other source, `pbss`, is described as "NVIDIA-internal download".
  - Other downloads: `recipes/esm2_peft_te/data/prepare_porter6_dataset.py` fetches a zip from the Porter6 GitHub repository; the SAE `esm2` recipe downloads UniRef50 or Swiss-Prot FASTA from `ftp.uniprot.org` and annotations from `rest.uniprot.org`; the CodonFM notebooks download their evaluation data; `models/mixtral/install_hybridep.sh` clones DeepEP from GitHub and pip-installs it; `recipes/vllm_inference/esm2/install_vllm.sh` clones vLLM `v0.15.1` and builds it from source.
  - An LLM API. The SAE library's `autointerp` sends feature summaries to Anthropic, OpenAI or NVIDIA NIM, with keys from `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` or `NIM_API_KEY`; in the recipes it runs only when `scripts/analyze.py` of the CodonFM SAE recipe gets `--auto-interp` (default provider `anthropic`, default model `claude-sonnet-4-20250514`). Leave the flag off to keep data local.
  - Remote code. `models/esm2/export.py` writes an `auto_map` into each exported checkpoint's `config.json`, pointing at model code shipped with the checkpoint, and its smoke test loads the result with `trust_remote_code=True`; the vLLM example also passes `trust_remote_code=True`.
  - Telemetry: none in the recipes or models; the only telemetry code is in `ci/lepton/` (a "kratos telemetry wrapper" for NVIDIA's own CI jobs). Search: `telemetry`, `posthog`, `sentry_sdk`, `mixpanel` across the clone.
- Do not use:
  - The dev container. `.devcontainer/initializeCommand.sh` runs on the host and creates `~/.claude`, `~/.codex`, `~/.cursor`, `~/.ssh` and empty `~/.netrc` and `~/.claude.json` when missing; `.devcontainer/devcontainer.json` bind-mounts the host's `~/.ssh` (read-only), `~/.gnupg`, `~/.netrc`, `~/.claude`, `~/.claude.json`, `~/.codex`, `~/.cursor`, `~/.config` and `~/.cache` into the container.
  - `pre-commit install` (a contributor step), `.ci_build.sh` (builds the Evo2 and Eden virtual environments), `docker build`, `install_vllm.sh`, `install_hybridep.sh`, `uv sync`.
  - `recipes/geneformer_native_te_mfsdp_fp8/internal/gitingest.sh`: it writes `gitingest.txt` (every tracked file concatenated) into the clone. The README of that recipe opens with "DO NOT proceed without reading [AGENT_DOCUMENTATION.md](AGENT_DOCUMENTATION.md) first", a note addressed to AI agents; the file it names is plain documentation of the recipe.
- Nothing needs switching off just to read the clone.

## Parts

### Recipe: esm2_native_te (`recipes/esm2_native_te/`)

- "TransformerEngine-accelerated ESM-2 training with native PyTorch training loop": sequence packing (THD), FP8, MXFP8 and NVFP4 with layer-wise control, DDP, FSDP2 and Megatron-FSDP, context parallelism. Entry points: `train_ddp.py`, `train_fsdp2.py`, `train_mfsdp.py`, `train_ddp_cp.py`, `train_fsdp2_cp.py`; `slurm.sh` for multi-node. Models: ESM-2 (all features) and AMPLIFY (BF16 only).
- Configs: `L0_sanity` (local `esm2_t6_8M_UR50D` config, 250 steps, local `train.parquet`, W&B `offline`), `L0_sanity_cp`, `L1_650M`, `L1_3B`, `L1_15B_perf_test`.
- Needs: an NVIDIA GPU and the recipe's container (`nvcr.io/nvidia/pytorch:26.04-py3`), or the manual route of `Dockerfile.cuda`: Python 3.12, `torch==2.9.0` for CUDA 13.0, `flash-attn`, `transformer-engine[pytorch]==2.9.0`. FP8 needs Hopper or newer. The default dataset streams from the Hugging Face Hub; W&B as above.

### Recipe: esm2_accelerate_te (`recipes/esm2_accelerate_te/`)

- "TE-accelerated ESM-2 using the Hugging Face Transformers Trainer class and Hugging Face Accelerate", with FP8 and FSDP or DeepSpeed through Accelerate config files (`default`, `dynamo`, `fp8`, `fsdp1_hf`, `fsdp1_te`, `fsdp2_hf`, `fsdp2_te`). Entry point `train.py`; configs `L0_sanity`, `L0_sanity_amplify`, `L1_amplify_350M_partial_conv`, `L1_esm2_15B_perf_test`.
- Needs: an NVIDIA GPU and its container; the default dataset `chandar-lab/UR100P` from the Hugging Face Hub; W&B as above.

### Recipe: esm2_peft_te (`recipes/esm2_peft_te/`)

- "PEFT Fine-tuning with TransformerEngine-accelerated ESM-2": LoRA fine-tuning (`train_lora_ddp.py`) for per-residue secondary structure and inference on a FASTA file to CSV (`infer.py`). Ships `data/peft_sanity_dataset.parquet`, "a **5,000-sample subset**" of `lamm-mit/protein_secondary_structure_from_PDB`, and `data/input_infer.fasta`; the Porter6 train and validation sets are built by `data/prepare_porter6_dataset.py` from the Porter6 GitHub repository.
- Needs: an NVIDIA GPU and its container; network only for the Porter6 download and Hub checkpoints.

### Recipe: vllm_inference/esm2 (`recipes/vllm_inference/esm2/`)

- "ESM-2 vLLM Inference": runs the exported ESM-2 TE checkpoints in vLLM (">= 0.14") as a pooling model, `runner="pooling"`, `trust_remote_code=True`, and `model.embed(...)` returns embeddings. "No conversion scripts or weight renaming are needed". Golden-value tests compare vLLM, native Hugging Face and the Hub reference model.
- Needs: an NVIDIA GPU; vLLM built into the image (`--build-arg INSTALL_VLLM=true` with `TORCH_CUDA_ARCH_LIST`) or by `install_vllm.sh`, which clones vLLM `v0.15.1` and compiles it for the GPU's CUDA architecture.

### Recipe: codonfm_native_te (`recipes/codonfm_native_te/`)

- "TransformerEngine-accelerated CodonFM training with native PyTorch training loop": FSDP2 (`train_fsdp2.py`), sequence packing, FP8 and NVFP4 with layer-wise control; uses TE's standard `TransformerLayer` (the "non-exact" variant), which "converges on par with the original". Ships a sample `train.parquet`. "A native_te checkpoint trained with this recipe will be uploaded in the future."
- Needs: an NVIDIA GPU (FP8 Hopper or newer, NVFP4 Blackwell or newer) and the container; W&B as above.

### Recipe: codonfm_ptl_te (`recipes/codonfm_ptl_te/`)

- "Codon FM: Foundation Models for Codon Sequences": a TransformerEngine-accelerated reproduction of NVIDIA-Digital-Bio/CodonFM on PyTorch Lightning, with pretraining, fine-tuning (including LoRA) and evaluation scripts, data curation tools and a PyTorch-to-TE checkpoint converter. EnCodon models: 80M, 600M, 1B and 1B (CDSWT), original and TE checkpoints on the Hugging Face Hub.
- Notebooks: zero-shot variant effect scoring (Cancer Hotspots, DDD and ASD cohorts, ClinVar missense and synonymous variants) and downstream tasks (ribosome profiling with riboNN, mRFP expression, mRNA stability); the notebooks download their datasets.
- Benchmarks were "run on `8 x NVIDIA H100 80GB HBM3` GPUs in `bfloat16` precision". Data curation advice: "For machines with 32GB or less of RAM, try chunk sizes of `500000000`".
- Needs: an NVIDIA GPU and its own container (base `nvcr.io/nvidia/pytorch:25.08-py3`); weights are under the NVIDIA Open Model License (see Licences); W&B only with `--enable_wandb` and a `WANDB_API_KEY`.

### Recipe: geneformer_native_te_mfsdp_fp8 (`recipes/geneformer_native_te_mfsdp_fp8/`)

- "Geneformer Pretraining with mfsdp and a custom pytorch training loop": a BERT model pretrained on single-cell transcriptomes, forked from the original Geneformer code and sped up. Entry point `train.py` under `torchrun`; configs `10m`, `106m`, `4b`, `l0_sanity`. Ships "a parquet file with 500 samples of tokenized data" and the vocabulary.
- FP8 "requires GPU compute capability ≥ 8.9 (H100+ GPUs)". W&B needs `WANDB_API_KEY`.
- Needs: an NVIDIA GPU and the container.

### Recipe: llama3_native_te (`recipes/llama3_native_te/`)

- "TransformerEngine-accelerated Llama 3 training with native PyTorch training loop", "configured for genomic sequences using a custom nucleotide tokenizer"; FP8, MXFP8, NVFP4, sequence packing, context parallelism, Nsight Systems profiling, KV-cache inference and conversion to Hugging Face format. Entry points `train_ddp.py`, `train_fsdp2.py`, `train_fsdp2_cp.py`; model configs `Llama-3.1-8B`, `Llama-3.1-70B`, `Llama-3.2-1B`, `lingua-1B`.
- Default data: the local `test_genomic_sequences.parquet`; a Lingua reproduction trains on `mlfoundations/dclm-baseline-1.0`. Benchmarks in the README were run on 32 GB300 GPUs and on 64 B200 GPUs.
- Needs: an NVIDIA GPU and the container; W&B as above.

### Recipe: opengenome2_llama_native_te (`recipes/opengenome2_llama_native_te/`)

- "TE-accelerated Llama 3 with a native PyTorch training loop for autoregressive DNA token prediction on the metagenome subset of the OpenGenome2 genomic dataset": FSDP2 (`train_fsdp2.py`, `train_fsdp2_cp.py`), THD packing, FP32 master weights, a 7B model with grouped-query attention; validated against a Megatron baseline. `DATASET.md` recommends downloading the metagenome JSONL files from `arcinstitute/opengenome2` (about 80 shards) and resharding them into shuffled Parquet with DuckDB.
- The README's runs used "6× H100 nodes (48 GPUs)".
- Needs: NVIDIA GPUs and the container; the dataset from the Hugging Face Hub.

### Recipe: evo2_megatron (`recipes/evo2_megatron/`)

- "A self-contained training, inference, and checkpoint conversion recipe for **Evo2** genomic foundation models built on Megatron Bridge". Evo2 (Striped Hyena) models "scale from 1B to 40B parameters with context lengths up to 1M+ nucleotides".
- CLI tools from `pyproject.toml` `[project.scripts]`: `train_evo2`, `infer_evo2` (generation), `predict_evo2` (log-likelihood scoring of FASTA), `preprocess_evo2` (FASTA to Megatron binary), `splice_evo2` (transcripts from FASTA and GTF), `evo2_convert_nemo2_to_mbridge`, `evo2_convert_savanna_to_mbridge`, `evo2_export_mbridge_to_vortex`, `evo2_remove_optimizer`, `bionemo_fasta_to_jsonl`; plus `download_bionemo_data`. LoRA fine-tuning is supported. Checkpoints: NGC (NeMo2 format, converted first) and Savanna checkpoints on the Hugging Face Hub.
- Install: `./.ci_build.sh` builds a virtual environment. The README reports a "12 hour 48 H100 GPU training run" and "small training runs at 2M context on only 512 H100 GPUs for the 40b parameter model".
- Needs: NVIDIA GPUs (Hopper for FP8 checkpoints), the container or the built venv, NGC or Hugging Face downloads for checkpoints.

### Recipe: eden_megatron (`recipes/eden_megatron/`)

- "Eden is a family of genomic models that use the Llama 3.1 architecture, developed by Basecamp Research. Models range from 100M to 35B parameters." CLI tools: `train_eden`, `infer_eden`, `predict_eden`, `eden_convert_nemo2_to_mbridge`, `eden_export_mbridge_to_hf`, `eden_convert_hf_to_mbridge`, `eden_remove_optimizer`; plus `download_bionemo_data`. Model sizes from `eden_100m` to `eden_35b`, eleven keys. Data: the ShardedEdenDataset, "backed by SQLite".
- Needs: NVIDIA GPUs, the container or the built venv.

### Recipe: vit (`recipes/vit/`)

- "`BioNeMo-Vision`: Training a `VisionTransformer` (ViT) with `Megatron-FSDP` and `TransformerEngine`": `train.py`, `infer.py`, checkpoint conversion between DCP and `torch.save`. Trains on the `AI-Lab-Makerere/beans` dataset, downloaded from the Hugging Face Hub. Run the container with `--shm-size=16G`.
- Needs: an NVIDIA GPU and the container; the dataset download.

### Recipe: fp8_analysis (`recipes/fp8_analysis/`)

- "FP8 Training Analyzer": "A model-agnostic tool for analyzing FP8 quantization logs and visualizing gradient underflows during training"; `analyze_and_create_heatmap.py` parses FP8 statistics logs, detects layers, draws heatmaps ("600 DPI") and exports CSV. Supported log sources: ESM2 and LLAMA3 with DDP or FSDP2. Ships `dummy_logs_esm2` and `dummy_logs_llama3`.
- Needs: no GPU; a container from `python:3.12-slim` or a venv with `matplotlib==3.10.1`, `numpy==1.26.4`, `pandas==2.2.3`, `seaborn==0.13.2`; FP8 statistics logs from a training run.

### Model: esm2 (`models/esm2/`)

- "ESM-2 Optimized with NVIDIA TransformerEngine": `modeling_esm_te.py` (`NVEsm*` classes), `convert.py` (Hugging Face to TE and back), `export.py` (packages Hub checkpoints), a fast tokenizer. Checkpoints "converted from the original Facebook weights": `nvidia/esm2_t6_8M_UR50D` (8M parameters) up to `nvidia/esm2_t48_15B_UR50D` (15B parameters), six sizes. Load: `AutoModel.from_pretrained("nvidia/esm2_t6_8M_UR50D")`.
- Needs: an NVIDIA GPU, TransformerEngine (the NGC PyTorch container is recommended), the checkpoint from the Hub (weights `mit`), model code from the checkpoint (`auto_map`).

### Model: amplify (`models/amplify/`)

- "AMPLIFY Optimized with NVIDIA TransformerEngine": a protein BERT; checkpoints `nvidia/AMPLIFY_120M` and `nvidia/AMPLIFY_350M` (120M and 350M parameters). FP8, THD and export are "Under development". Licence of the folder: MIT.
- Needs: an NVIDIA GPU, TransformerEngine (container `nvcr.io/nvidia/pytorch:25.01-py3`), the checkpoint from the Hub.

### Model: geneformer (`models/geneformer/`)

- "Geneformer Implemented with Transformer Engine": `export.py` converts `Geneformer-V1-10M`, `Geneformer-V2-104M`, `Geneformer-V2-316M` and `Geneformer-V2-104M_CLcancer` to TE format, from the original Hugging Face checkpoints.
- Needs: an NVIDIA GPU, TransformerEngine, the source checkpoints from the Hub (`ctheodoris/Geneformer`, `apache-2.0`).

### Model: codonfm (`models/codonfm/`)

- No README. `modeling_codonfm_te.py` ("TransformerEngine-optimized CodonFM model for masked language modeling"), `tokenizer.py`, `dataset.py`; tests compare against stored golden values. Requirements: `torch`, `transformer_engine[pytorch]`, `transformers`. Used by `recipes/codonfm_native_te`.
- Needs: an NVIDIA GPU and TransformerEngine.

### Model: llama3 (`models/llama3/`)

- "Llama-3.1 Optimized with NVIDIA TransformerEngine": "we do not currently distribute pre-converted TE checkpoints on HuggingFace Hub"; users convert Hugging Face Llama 3 checkpoints with `convert.py`. FP8, MXFP8, THD, context parallelism, "KV-cache inference" with beam search; tensor parallelism under development. Examples use `meta-llama/Llama-3.2-1B-Instruct`.
- Needs: an NVIDIA GPU, TransformerEngine, a Hugging Face account with access to the gated Llama weights.

### Model: mixtral (`models/mixtral/`)

- "Mixtral Optimized with NVIDIA TransformerEngine": a mixture-of-experts model with TE `MultiheadAttention` and `GroupedLinear`, expert parallelism through `DTensor` composed with FSDP2, KV-cache inference. An optional `FusedTokenRouter` needs DeepEP "and NVLink peer access between GPUs", installed by `install_hybridep.sh`. Examples use `mistralai/Mixtral-8x7B-v0.1`.
- Needs: several NVIDIA GPUs for expert parallelism, TransformerEngine.

### Model: qwen (`models/qwen/`)

- "Qwen2.5 / Qwen3 Optimized with NVIDIA TransformerEngine": `convert_qwen2.py`, `convert_qwen3.py`, `modeling_qwen2_te.py`, `modeling_qwen3_te.py`; FP8, MXFP8, THD, KV-cache inference with beam search. Examples use `Qwen/Qwen3-0.6B` and `Qwen/Qwen2.5-0.5B-Instruct`.
- Needs: an NVIDIA GPU, TransformerEngine (container `nvcr.io/nvidia/pytorch:26.04-py3`).

### Interpretability: sae library (`interpretability/sparse_autoencoders/sae/`)

- "Sparse Autoencoders for Model Interpretability": "a domain-agnostic implementation of SAE designed for mechanistic model interpretability". Architectures ReLU-L1, Top-K and MoE; a trainer with checkpointing and logging; evaluation (reconstruction, sparsity, dead latents); `autointerp` (LLM-based feature labels); an activation collector; a React dashboard. "**Early Release** -- This project is under active development. APIs and interfaces may change between versions."
- Needs: a venv from the uv workspace (`uv sync`), `torch>=2.0`, Python `>=3.10`; a GPU for real runs; an LLM API key only for `autointerp`; Node for building the dashboard.

### Interpretability: SAE recipe esm2 (`interpretability/sparse_autoencoders/recipes/esm2/`)

- "ESM2 SAE Recipe": extract activations, then train a TopK SAE ("8x expansion, top-32 sparsity by default"), then evaluate (loss recovered, F1 against Swiss-Prot annotations, UMAP) and build a dashboard. Configs for the 650M, 3B and 15B models; examples run `torchrun --nproc_per_node=4`.
- Needs: NVIDIA GPUs; UniRef50 or Swiss-Prot downloads from UniProt, or a local FASTA; ESM-2 checkpoints from the Hub.

### Interpretability: SAE recipe codonfm (`interpretability/sparse_autoencoders/recipes/codonfm/`)

- "CodonFM SAE Recipe": extract, train, evaluate, then optional analysis (codon usage bias, amino acid identity, wobble position, CpG content, optional LLM labels) and dashboard. Needs an Encodon checkpoint downloaded from `nvidia/NV-CodonFM-Encodon-1B-v1` and a CSV of coding sequences. Launchers `1b.sh`, `1b_swissprot.sh`.
- Needs: NVIDIA GPUs; the checkpoint download; an LLM API key only with `--auto-interp`.

### Interpretability: SAE recipe evo2 (`interpretability/sparse_autoencoders/recipes/evo2/`)

- No README. Package `evo2-sae`, "Sparse Autoencoders for the Evo2 DNA language model". Scripts: `7b.sh` (chunk a FASTA, extract activations of one layer, default `LAYER` 26, train an SAE), `chunk_fasta.py`, `extract.py` ("Streaming Evo2 activation extractor"), `train.py`. It activates the virtual environment of `recipes/evo2_megatron` (`EVO2_MEGATRON_DIR`) and needs `CKPT_DIR`, an Evo2 7B MBridge checkpoint, and `FASTA`; `NPROC` defaults to 8 GPUs.
- Needs: NVIDIA GPUs, the Evo2 recipe's venv, an Evo2 checkpoint.

## Statuses after this desk check

All 24 parts above were read: each is `candidate`. None is `listed`. No part was tried or used, and none is rejected.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 111 model calls on opus, $6.77 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
