---
title: "Desk check: facebookresearch/esm v1.0.3"
source: https://github.com/facebookresearch/esm/tree/v1.0.3
type: repos
authors: ["Facebook AI Research"]
source_date: 2022-10-18
ingested: 2026-11-21
repo: facebookresearch/esm
kind: model
version: "1.0.3"
licence: MIT
tags: [catalog, desk-check, kind-model, protein-language-models, embeddings, inverse-folding, variant-effects, archived]
summary: "Evolutionary Scale Modeling read from a read-only clone of tag v1.0.3: the pretrained protein language models it loads (ESM-2 in six sizes, ESM-1b, the five ESM-1v models, ESM-MSA-1b, ESM-IF1 and the legacy ESM-1 family), the five entry scripts, the download host and the measured size of each checkpoint, and the freshness check that shows the repository archived and moved to another owner. Nothing was installed, no weights were downloaded."
---

# Desk check: facebookresearch/esm v1.0.3

Read from a clone of tag `v1.0.3` (commit `ca8a710ef2014674ceb2960d12479ae9d2cb5418`, committed 2022-10-18) at `$EXTERNAL/esm`. The clone was not modified; nothing was installed, nothing was run, no weights were downloaded. Checked 2026-11-21. Version read by this desk check: 1.0.3.

## Repository facts

- `esm/version.py`: `version = "1.0.3"`. `setup.py`: package name `fair-esm`, `license="MIT"`, author "Facebook AI Research", packages `esm`, `esm/model`, `esm/inverse_folding`.
- `LICENSE`: "MIT License", "Copyright (c) Facebook, Inc. and its affiliates." The README's License section: "This source code is licensed under the MIT license found in the `LICENSE` file in the root directory of this source tree."
- What it is, in the README's words at this tag: "This repository contains code and pre-trained weights for **Transformer protein language models** from Facebook AI Research, including our state-of-the-art **ESM-2** and **MSA Transformer**, as well as **ESM-1v** for predicting variant effects and **ESM-IF1** for inverse folding."
- Folders: `esm/` (the library: `pretrained.py`, `data.py`, `modules.py`, `model/esm1.py`, `model/esm2.py`, `model/msa_transformer.py`, `inverse_folding/`), `scripts/` (one script), `examples/` (scripts, notebooks and example data), `tests/`. `hubconf.py` exposes every loader to `torch.hub`.
- ESMFold is **not** in this tag. The README of v1.0.3 does not mention it; upstream released it with tag `v2.0.0` (commit `0b59d87ebef95948c735b1f7aad463dc6dfa991b`, committed 2022-11-01, merge message "Release ESMFold - esm.pretrained.esmfold_v1"), which has no GitHub release entry.
- Weights are not in the repository. `esm/pretrained.py` downloads them at load time from `https://dl.fbaipublicfiles.com/fair-esm/models/<model name>.pt` through `torch.hub.load_state_dict_from_url`, into the torch hub cache (the README: "automatically downloaded to `~/.cache/torch/hub/checkpoints`"). Contact-regression weights come from `https://dl.fbaipublicfiles.com/fair-esm/regression/<model name>-contact-regression.pt`; `_has_regression_weights` returns "whether we expect / require regression weights; Right now that is all models except ESM-1v and ESM-IF".
- The only other outbound URLs in `esm/` and `scripts/` are the dataset archives of the ESM Structural Split Dataset in `esm/data.py` (`https://dl.fbaipublicfiles.com/fair-esm/structural-data/splits.tar.gz`, `.../pkl.tar.gz`) and documentation links in comments. There is no telemetry, no analytics and no usage reporting in the clone.
- `load_model_and_alphabet_local` loads a checkpoint from a local path instead, and expects the matching `-contact-regression.pt` file "co-located" beside it, so a machine without network access can run a model whose files were fetched elsewhere.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/facebookresearch/esm` resolves to `full_name` `Biohub/esm-archive`: the repository was transferred and renamed, and the old path redirects. `archived: true`, `pushed_at` 2024-02-07T03:31:38Z, licence reported by GitHub `MIT`, default branch `main`, homepage `https://biohub.github.io/esm-archive/`, 4175 stars.
- `gh api repos/facebookresearch/esm/releases/latest`: tag `v1.0.3`, release name "ESM-2 Public Release v1.0.3 (Fixes & Updates)", published 2022-10-18T13:38:47Z. Only three releases exist: `v1.0.3`, `v1.0.2` (2022-08-23) and `v1.0.0` (2022-08-22). The tag list also holds `v2.0.0` and older `v0.x` tags with no release entry, so `v1.0.3` is the latest release while `v2.0.0` is the newest tag.
- Last commit on the default branch: `2b369911bb5b4b0dda914521b9475cad1656b2ac`, 2023-06-27T15:29:55Z, "Make programming language reporting less confusing." The 2024-02-07 push did not add a commit to `main`.
- Licence as GitHub reports it (`MIT`) matches the `LICENSE` file in the clone.
- **Where the models live on**: the repository does not say. The README on the default branch was searched on 2026-11-21 for "archive", "moved", "no longer", "deprecated", "maintained", "biohub" and "evolutionaryscale"; there is no such notice, and the README still points at the ESM Metagenomic Atlas (`https://esmatlas.com`) and at the download host. The archive homepage GitHub lists (`https://biohub.github.io/esm-archive/`) was fetched on 2026-11-21 and its whole text is "Hello world, ESM!". So the only checked facts are: archived, owner now `Biohub`, repository renamed `esm-archive`, no successor named by the repository itself.
- The download host still serves the checkpoints: every size below was read on 2026-11-21 from the `content-length` header of a `HEAD` request to `https://dl.fbaipublicfiles.com/fair-esm/models/<model name>.pt`. No file was downloaded.

## How to run here

- **Clone**: `git clone --depth 1 --branch v1.0.3 https://github.com/facebookresearch/esm $EXTERNAL/esm`, read-only. Never edit the clone. The old owner path still redirects; `Biohub/esm-archive` is the same repository.
- **Read first**: `$EXTERNAL/esm/README.md` (the model tables and the usage sections), then `$EXTERNAL/esm/esm/pretrained.py` for the loader of the variant in question, then the entry script for the task (`scripts/extract.py`, `examples/variant-prediction/predict.py`, `examples/inverse_folding/`).
- **Telemetry and outbound calls**: none, except the weight and dataset downloads named above. Nothing to switch off. To keep a machine offline, fetch the `.pt` file (and its `-contact-regression.pt` for every model except ESM-1v and ESM-IF1) elsewhere and load it with `esm.pretrained.load_model_and_alphabet("<path>.pt")`, which takes a filepath when the name ends in `.pt`.
- **Do not install**: `pip install fair-esm`, `pip install git+https://github.com/facebookresearch/esm.git` (both in the README), and the inverse-folding conda environment (`conda create -n inverse python=3.9`, `conda install pytorch cudatoolkit=11.3 -c pytorch`, `conda install pyg -c pyg -c conda-forge`, `pip install biotite`) from the inverse-folding README. Real installation waits for the user's yes; a trial belongs in a throwaway environment.
- **What a run takes**: PyTorch is a prerequisite ("As a prerequisite, you must have PyTorch installed to use this repository"). A GPU is optional and auto-detected: `scripts/extract.py` says "A cuda device is optional and will be auto-detected" and has `--nogpu` ("Do not use GPU even if available"). The repository gives no VRAM figures for any variant; the only memory statement is for the largest model, see `esm2_t48_15B_UR50D` below. Hardware figures in this desk check are therefore download sizes only.
- **What breaks without the plugin**: not applicable; this is not a plugin and nothing has to be loaded into an agent harness. The library is imported, or the scripts are run by path, from the clone.

## Parts

Parts of this collection are its model families and variants, plus the entry scripts. Every size is the `content-length` of a `HEAD` request on 2026-11-21, in bytes, with a rounded figure beside it.

### Model: `esm2_t6_8M_UR50D` (ESM-2, 8M)

- `esm/pretrained.py`: "6 layer ESM-2 model with 8M params, trained on UniRef50." README table: 6 layers, 8M parameters, dataset UR50/D 2021_04, embedding dimension 320.
- Needs: the checkpoint, 30099493 bytes (30 MB), plus its contact-regression file; PyTorch; no GPU required.
- Notable: the smallest ESM-2, the one to try a pipeline on. README comparison table: unsupervised contact prediction (top-L long-range precision) 15.9 on the large validation set against 54.5 for the 15B model.

### Model: `esm2_t12_35M_UR50D` (ESM-2, 35M)

- "12 layer ESM-2 model with 35M params, trained on UniRef50." README table: 12 layers, 35M parameters, embedding dimension 480.
- Needs: 134095705 bytes (134 MB) plus regression file; PyTorch; no GPU required.

### Model: `esm2_t30_150M_UR50D` (ESM-2, 150M)

- "30 layer ESM-2 model with 150M params, trained on UniRef50." README table: 30 layers, 150M parameters, embedding dimension 640.
- Needs: 592774773 bytes (593 MB) plus regression file; PyTorch.

### Model: `esm2_t33_650M_UR50D` (ESM-2, 650M)

- "33 layer ESM-2 model with 650M params, trained on UniRef50." README table: 33 layers, 650M parameters, embedding dimension 1280. This is the model of the README's quick start and of its `torch.hub` example.
- Needs: 2604537549 bytes (2.6 GB) plus regression file; PyTorch; a CUDA GPU optional.

### Model: `esm2_t36_3B_UR50D` (ESM-2, 3B)

- "36 layer ESM-2 model with 3B params, trained on UniRef50." README table: 36 layers, 3B parameters, embedding dimension 2560. Named in the README's "Main models you should use" table as the general-purpose choice together with the 15B model.
- Needs: 5678116398 bytes (5.7 GB) plus regression file; PyTorch; a GPU for anything but small batches (no figure given).

### Model: `esm2_t48_15B_UR50D` (ESM-2, 15B)

- "48 layer ESM-2 model with 15B params, trained on UniRef50. If you have OOM while loading this model, please refer to README on how to employ FSDP and ZeRO CPU offloading." README table: 48 layers, 15B parameters, embedding dimension 5120. README: "If you want to load very large models like 15B and/or do inference on long sequences on your machine, regular GPU inference may lead to OOM errors", and points at `examples/esm2_infer_fairscale_fsdp_cpu_offloading.py`.
- Needs: 30258341762 bytes (30 GB) plus regression file; PyTorch; a GPU plus host RAM for CPU offloading, or Fairscale FSDP. No VRAM figure is given in the repository.

### Model: `esm1b_t33_650M_UR50S` (ESM-1b)

- README "Main models you should use": "SOTA general-purpose protein language model ... Released with Rives et al. 2019 (Dec 2020 update)." Table: 33 layers, 650M parameters, dataset UR50/S 2018_03, embedding dimension 1280.
- Needs: 7828576466 bytes (7.8 GB) plus regression file; PyTorch. The file is three times the size of the ESM-2 model of the same parameter count.
- Notable: superseded by ESM-2 for structure tasks per the README comparison table (contact precision 41.1 against 52.7 for ESM-2 3B).

### Model: `esm1v_t33_650M_UR90S_1` … `_5` (ESM-1v ensemble)

- README: "Language model specialized for prediction of variant effects. Enables SOTA zero-shot prediction of the functional effects of sequence variations. Same architecture as ESM-1b, but trained on UniRef90." Each loader's docstring: "33 layer transformer model with 650M params, trained on Uniref90. This is model 1 of a 5 model ensemble." `esm1v_t33_650M_UR90S()` without a number loads model 1.
- The variant-prediction README runs all five at once: `--model-location esm1v_t33_650M_UR90S_1 esm1v_t33_650M_UR90S_2 esm1v_t33_650M_UR90S_3 esm1v_t33_650M_UR90S_4 esm1v_t33_650M_UR90S_5`.
- Needs: 7828635339 bytes (7.8 GB) each for models 1 to 4 and 7828635531 bytes (7.8 GB) for model 5, so about 39 GB for the full ensemble; PyTorch. No contact-regression files (`_has_regression_weights` excludes `esm1v`).
- Notable: the README adds that "ESM-2 could be used for variant prediction as well, and is expected to have similar performance to ESM-1v."

### Model: `esm_msa1b_t12_100M_UR50S` (MSA Transformer)

- README: "MSA Transformer language model. Can be used to extract embeddings from an MSA. Enables SOTA inference of structure. Released with Rao et al. 2021 (ICML'21 version, June 2021)." Table: 12 layers, 100M parameters, dataset UR50/S + MSA 2018_03, embedding dimension 768.
- Needs: 1387625262 bytes (1.4 GB) plus regression file; PyTorch; and an input alignment (`.a3m`), not a bare sequence. Example alignments ship in `examples/data/`.
- Notable: the best unsupervised contact precision in the README's own table (57.4 on the large validation set), above every single-sequence model including ESM-2 15B (54.5), because it reads an alignment.

### Model: `esm_if1_gvp4_t16_142M_UR50` (ESM-IF1, inverse folding)

- Loader docstring: "Inverse folding model with 142M params, with 4 GVP-GNN layers, 8 Transformer encoder layers, and 8 Transformer decoder layers, trained on CATH structures and 12 million alphafold2 predicted structures from UniRef50 sequences." README: "built for predicting protein sequences from their backbone atom coordinates ... achieves 51% native sequence recovery on structurally held-out backbones with 72% recovery for buried residues", and "is also trained with span masking to tolerate missing backbone coordinates".
- Needs: 1700450121 bytes (1.7 GB); PyTorch, PyTorch Geometric and biotite. No contact-regression file. The inverse-folding README: "It is highly recommended to start a new conda environment from scratch due to potential CUDA compatability issues between pytorch and the pytorch-geometric package required for the inverse folding model."
- Notable: the model code is `esm/inverse_folding/` (`gvp_transformer.py`, `util.py`, `multichain_util.py`); the README calls the architecture `GVPTransformer`. Sampling temperature defaults to 1, and "To optimize for native sequence recovery, we recommend sampling with low temperature such as 1e-6."

### Models: legacy ESM-1 family (`esm1_t34_670M_UR50S`, `esm1_t34_670M_UR50D`, `esm1_t34_670M_UR100`, `esm1_t12_85M_UR50S`, `esm1_t6_43M_UR50S`, `esm_msa1_t12_100M_UR50S`)

- Known from the README's "Pre-trained Models" table and the loader list in `esm/pretrained.py` and `hubconf.py` only; their docstrings, sizes and behaviour were not read. The table gives 34 layers and 670M parameters for the three `t34` models (embedding dimension 1280), 12 layers and 85M for `esm1_t12_85M_UR50S`, 6 layers and 43M for `esm1_t6_43M_UR50S` (both 768), and 12 layers and 100M for `esm_msa1_t12_100M_UR50S` (768).
- The README's chronological list marks them as earlier releases: ESM-1 "Released with Rives et al. 2019 (Aug 2020 update)", ESM-MSA-1 "Released with Rao et al. 2021 (Preprint v1)", both superseded by ESM-1b, ESM-2 and ESM-MSA-1b.
- Needs: not measured; the same loader path and download host as the others.

### Entry point: `esm.pretrained` and `hubconf.py`

- `esm/pretrained.py` is the single entry point for loading: `load_model_and_alphabet(name_or_path)` takes a hub name or a `.pt` path, `load_model_and_alphabet_hub` downloads, `load_model_and_alphabet_local` reads a local file, and one named function per variant returns `(model, alphabet)`.
- `hubconf.py` declares `dependencies = ["torch"]` and re-exports all 21 loader functions, which is what makes the README's `torch.hub.load("facebookresearch/esm:main", "esm2_t33_650M_UR50D")` work without a clone. That hub call fetches the code from the default branch, not from this tag.
- Usage after loading, from the README: `batch_converter = alphabet.get_batch_converter()`, `model.eval()`, then `model(batch_tokens, repr_layers=[33], return_contacts=True)`; per-sequence vectors are the mean over residue positions, and "token 0 is always a beginning-of-sequence token, so the first residue is token 1."
- Needs: the clone (or the installed package) and PyTorch; network on first load of each variant.

### Entry script: `scripts/extract.py`

- README: "We provide a script that efficiently extracts embeddings in bulk from a FASTA file." Documented command: `python scripts/extract.py esm2_t33_650M_UR50D examples/data/some_proteins.fasta examples/data/some_proteins_emb_esm2 --repr_layers 0 32 33 --include mean per_tok`. One `.pt` file per input sequence.
- Arguments read from the file: `--toks_per_batch` (default 4096, "maximum batch size"), `--repr_layers`, `--include` with `per_tok`, `mean` and `bos` ("Don't use with the pre-trained models - we trained without bos-token supervision"), `--truncation_seq_length` (default 1022, "truncate sequences longer than the given value"), `--nogpu`.
- Needs: the clone, PyTorch, the checkpoint of the chosen variant, a FASTA file; a CUDA GPU is used when present unless `--nogpu` is given.

### Entry script: `examples/variant-prediction/predict.py`

- Labels a deep mutational scan with model scores. Documented commands in `examples/variant-prediction/README.md` for the five ESM-1v models and for the MSA Transformer (the latter with `--msa-path`).
- Arguments read from the file: `--model-location` (one or more), `--sequence`, `--dms-input`, `--mutation-col`, `--dms-output`, `--offset-idx`, `--scoring-strategy` with `choices=["wt-marginals", "pseudo-ppl", "masked-marginals"]`, `--msa-path`, `--nogpu`.
- Notable, read in the code: `--nogpu` is honoured only when moving the model (`if torch.cuda.is_available() and not args.nogpu: model = model.cuda()`), while the scoring paths call `batch_tokens_masked.cuda()` unconditionally (the `pseudo-ppl` helper, the MSA Transformer loop, and both the `wt-marginals` and `masked-marginals` branches). So this script in practice needs a CUDA device; on a machine without one it fails in the scoring step rather than falling back to CPU.
- Needs: the clone, PyTorch, a CUDA GPU as just described, the ESM-1v or MSA Transformer checkpoints (about 39 GB for the full ensemble), `pandas`, `biopython`, `tqdm`, `numpy`, and a CSV of mutations. The folder also ships result files of "the 41 Deep Mutational Scanning datasets reported in the paper".

### Entry scripts: `examples/inverse_folding/sample_sequences.py` and `score_log_likelihoods.py`

- Documented in `examples/inverse_folding/README.md`, which was read; **the two scripts' own code was not read** (a model safety classifier stopped that step; see "Not checked" below), so their flags are recorded here only as the README documents them.
- `sample_sequences.py` designs sequences for a backbone: `python sample_sequences.py data/5YH2.pdb --chain C --temperature 1 --num-samples 3 --outpath output/sampled_sequences.fasta`. Input "can have either `.pdb` or `.cif` as suffix"; "By default, the script only loads the backbone of the specified target chain as model input", and `--multichain-backbone` conditions on the whole complex. The README warns that "one failure mode in sampled sequences is a high number of repeated amino acids" and advises filtering those out.
- `score_log_likelihoods.py` scores given sequences against a structure: `python score_log_likelihoods.py data/5YH2.pdb data/5YH2_mutated_seqs.fasta --chain C --outpath output/5YH2_mutated_seqs_scores.csv`, with the same `--multichain-backbone` option. "The output values are the average log-likelihoods averaged over all amino acids in a sequence."
- The library functions behind them, named in the same README: `esm.inverse_folding.util.load_structure`, `extract_coords_from_structure`, `score_sequence`, and `multichain_util.extract_coords_from_complex`, `sample_sequence_in_complex`, `score_sequence_in_complex`. Input format: "a list of backbone atom coordinates for the N, CA, C atoms in each amino acid ... of shape L x 3 x 3".
- Needs: the clone, the ESM-IF1 checkpoint (1.7 GB), PyTorch, PyTorch Geometric and biotite in an environment of their own, and a PDB or mmCIF structure.

### Entry script: `examples/esm2_infer_fairscale_fsdp_cpu_offloading.py`

- Loads `esm2_t48_15B_UR50D` wrapped layer by layer in Fairscale's `FullyShardedDataParallel` with `mixed_precision=True`, `cpu_offload=True` and `state_dict_device=torch.device("cpu")` ("reduce GPU mem usage"), then runs one forward pass with `repr_layers=[48], return_contacts=True`.
- Needs: the clone, PyTorch with NCCL, `fairscale`, a CUDA GPU (`batch_tokens.cuda()`), host RAM for the offloaded parameters, the 30 GB checkpoint, and a one-process distributed group that the example starts with `torch.distributed.init_process_group`, backend `nccl`, `world_size=1`, `rank=0`, over a TCP address on `localhost`.

### Dataset: `esm.data.ESMStructuralSplitDataset`

- Known from the README only: "a five-fold cross validation dataset of protein domain structures that can be used to measure generalization of representations across different levels of structural dissimilarity", with holdouts at family, superfamily and fold level, providing "3d coordinates, distance maps, and secondary structure labels". On first use it "will download `splits` and `pkl`"; the archives (`splits.tar.gz`, `pkl.tar.gz`, `msas.tar.gz`) are the dataset URLs in `esm/data.py` listed above. Their sizes were not checked.

### Example notebooks (`examples/`)

- `contact_prediction.ipynb` (contacts from attention maps with ESM-2 and the MSA Transformer), `sup_variant_prediction.ipynb` (train a supervised variant predictor on embeddings), `esm_structural_dataset.ipynb` (load and index the structural split dataset), `inverse_folding/notebook.ipynb` and `inverse_folding/notebook_multichain.ipynb` (sampling, scoring and encoder output for single chains and complexes). Known from the README's descriptions; the notebooks themselves were not opened.
- Each has a Colab badge, so a run there sends the data to a third party; locally they need the same environment as the matching script.

## Status reasons

- No part is rejected. Nothing in this repository has been used in real work, so no part is `tried` or `in use`.
- `listed` rather than `candidate`: the legacy ESM-1 family and `esm_msa1_t12_100M_UR50S` (the README's own tables and the loader list only), `ESMStructuralSplitDataset`, the example notebooks, and the two inverse-folding scripts (their documented commands were read, their code was not).
- The repository being archived is a fact about its future, not a reason to reject it: the code at this tag is complete, the licence is MIT, and the checkpoints are still served. It is the reason the Check when of every row names a condition, and the reason a newer protein language model should be compared before this one goes into real work.

## Not checked

- A model safety classifier stopped one step of this desk check: reading how `examples/inverse_folding/sample_sequences.py` and `examples/inverse_folding/score_log_likelihoods.py` handle the GPU. The step was not retried and nothing was reworded to get past it; both scripts are therefore described from `examples/inverse_folding/README.md` only and are marked `listed`.
- No weights were downloaded and no model was run, so there is no measurement of speed, memory or quality in this desk check.
- Sizes of the legacy ESM-1 checkpoints, of the contact-regression files and of the structural-dataset archives were not checked.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 50 model calls on opus, $5.96 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
