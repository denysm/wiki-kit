---
title: "facebookresearch/esm"
category: reference
kind: model
areas: [science]
science_sections: [protein-engineering-and-design, machine-learning-and-ai]
repo: facebookresearch/esm
version: "1.0.3"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/facebookresearch-esm-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, science-protein-engineering-and-design, science-machine-learning-and-ai, kind-model, protein-language-models, embeddings, inverse-folding, variant-effects, archived]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Protein language models from Facebook AI Research with the Python library that loads them: ESM-2 in six sizes for sequence embeddings and contacts, the five ESM-1v models for variant effects, the MSA Transformer for alignments, and ESM-IF1 for fixed-backbone sequence design. The repository is archived and now sits under another owner; the weights are still served from the publisher's download host. Nineteen parts read or listed, nothing tried yet."
---

# facebookresearch/esm

> A collection of pretrained protein language models with the Python library that loads them (kind `model`, licence MIT, version `1.0.3` read): ESM-2 in six sizes, ESM-1b, the five-model ESM-1v ensemble for variant effects, the MSA Transformer, ESM-IF1 for inverse folding, and five entry scripts. The repository is **archived** upstream (last push 2024-02-07) and GitHub now resolves it to another owner under the name `esm-archive`; its README names no successor. Weights live outside the repository and are downloaded on first load.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn protein sequences into vectors for clustering, search or a downstream classifier | `esm2_t33_650M_UR50D` | science-machine-learning-and-ai |
| Try a protein-embedding pipeline end to end before paying for a large model | `esm2_t6_8M_UR50D` | science-machine-learning-and-ai |
| Embed a whole FASTA file in bulk, one tensor file per sequence | `scripts/extract.py` | science-machine-learning-and-ai |
| Get the strongest single-sequence embeddings in this collection when a GPU is available | `esm2_t36_3B_UR50D` | science-machine-learning-and-ai |
| Run the largest model on one GPU by offloading parameters to host memory | `examples/esm2_infer_fairscale_fsdp_cpu_offloading.py` | science-machine-learning-and-ai |
| Measure how well embeddings generalise across structural holdouts | `esm.data.ESMStructuralSplitDataset` | science-machine-learning-and-ai |
| Predict which residues touch each other, from one sequence and no alignment | `esm.pretrained` and `hubconf.py` | science-protein-engineering-and-design |
| Score how single mutations change a protein's function without labelled data | `esm1v_t33_650M_UR90S_1` … `esm1v_t33_650M_UR90S_5` | science-protein-engineering-and-design |
| Label a whole deep mutational scan with model scores | `examples/variant-prediction/predict.py` | science-protein-engineering-and-design |
| Use an alignment instead of a single sequence for a stronger structure signal | `esm_msa1b_t12_100M_UR50S` | science-protein-engineering-and-design |
| Design sequences for a given protein backbone | `examples/inverse_folding/sample_sequences.py` | science-protein-engineering-and-design |
| Rank candidate sequences against a backbone before making them | `examples/inverse_folding/score_log_likelihoods.py` | science-protein-engineering-and-design |

## Run it here

- **Clone**: `git clone --depth 1 --branch v1.0.3 https://github.com/facebookresearch/esm $EXTERNAL/esm`, read-only. Never edit the clone. The old owner path redirects: GitHub now reports the repository as `Biohub/esm-archive`.
- **Version**: `1.0.3`, the latest release, published 2022-10-18. The newest tag is `v2.0.0` (committed 2022-11-01), which added ESMFold and has no release entry; ESMFold is therefore not in this clone. Before relying on this card: `gh api repos/facebookresearch/esm --jq .archived` and `gh api repos/facebookresearch/esm/releases/latest --jq .tag_name`.
- **Read**: `$EXTERNAL/esm/README.md` for the model tables, then `$EXTERNAL/esm/esm/pretrained.py` for the loader of the variant in question, then the entry script for the task.
- **Switch off**: nothing. The clone has no telemetry and no analytics; the only outbound calls are the weight download (`dl.fbaipublicfiles.com`) on first load of a variant and the dataset archives of the structural split dataset. For an offline machine, fetch the `.pt` file (and its `-contact-regression.pt`, needed by every model except ESM-1v and ESM-IF1) elsewhere and pass the path to `esm.pretrained.load_model_and_alphabet`.
- **Do not install**: `pip install fair-esm`, the `pip install git+…` line from the README, or the inverse-folding conda environment (`conda create -n inverse python=3.9`, pytorch with `cudatoolkit=11.3`, `pyg`, `biotite`). A trial belongs in a throwaway environment; real installation waits for the user's yes.
- **No part is in use.** Nothing from this repository has been run here; every size below is a download size read from the publisher's host on 2026-11-21, not a measurement.

## What's inside

Parts are the model families and their sizes, plus the entry scripts that drive them. The repository gives no VRAM figures, so Needs names the download and what the code requires.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `esm2_t6_8M_UR50D` | ESM-2, 6 layers, 8M parameters, 320 numbers per residue. The smallest model, for wiring a pipeline up. | candidate | 30099493 bytes (30 MB) plus its contact-regression file; PyTorch; no GPU | Try it first on any new embedding pipeline, before a larger size is downloaded. |
| `esm2_t12_35M_UR50D` | ESM-2, 12 layers, 35M parameters, 480 numbers per residue. | candidate | 134095705 bytes (134 MB) plus regression file; PyTorch; no GPU | Try it when the 8M model's vectors are too weak but a CPU-only run is still wanted. |
| `esm2_t30_150M_UR50D` | ESM-2, 30 layers, 150M parameters, 640 numbers per residue. | candidate | 592774773 bytes (593 MB) plus regression file; PyTorch | Try it on a few thousand sequences when the small models underperform on a labelled task. |
| `esm2_t33_650M_UR50D` | ESM-2, 33 layers, 650M parameters, 1280 numbers per residue. The default of the README's quick start and of its `torch.hub` example. | candidate | 2604537549 bytes (2.6 GB) plus regression file; PyTorch; a CUDA GPU optional | Try it on the first real embedding task: a set of sequences to cluster, search or classify. |
| `esm2_t36_3B_UR50D` | ESM-2, 36 layers, 3B parameters, 2560 numbers per residue. Named with the 15B model as the general-purpose choice. | candidate | 5678116398 bytes (5.7 GB) plus regression file; PyTorch; a GPU for anything but small batches | Try it when the 650M model's vectors decide a real comparison and a GPU is free. |
| `esm2_t48_15B_UR50D` | ESM-2, 48 layers, 15B parameters, 5120 numbers per residue. Best contact precision of the single-sequence models in the repository's own table (54.5 against 52.7 for 3B). | candidate | 30258341762 bytes (30 GB) plus regression file; a GPU with host RAM for offloading, or Fairscale FSDP; the loader warns about out-of-memory errors | Try it only when a smaller ESM-2 has been measured first and the gain is worth 30 GB. |
| `esm1v_t33_650M_UR90S_1` … `esm1v_t33_650M_UR90S_5` | Five models of one ensemble, ESM-1b architecture trained on UniRef90, specialised for zero-shot variant effects. | candidate | 7828635339 bytes (7.8 GB) each for models 1 to 4 and 7828635531 bytes (7.8 GB) for model 5, about 39 GB for the ensemble; PyTorch; no regression files | Try it on a mutation set with measured effects, scoring one model first and the ensemble only if the single model is close. |
| `esm_msa1b_t12_100M_UR50S` | MSA Transformer: reads a multiple sequence alignment instead of one sequence. Highest unsupervised contact precision in the repository's table (57.4). | candidate | 1387625262 bytes (1.4 GB) plus regression file; PyTorch; an `.a3m` alignment as input | Try it when alignments already exist for the proteins in question and single-sequence contacts are too weak. |
| `esm_if1_gvp4_t16_142M_UR50` | ESM-IF1 inverse folding: predicts sequences from backbone coordinates; 51% native sequence recovery, 72% on buried residues, tolerant of missing coordinates. | candidate | 1700450121 bytes (1.7 GB); PyTorch, PyTorch Geometric and biotite in an environment of their own | Try it on a backbone that already has a known sequence, and compare recovery before using it to design anything. |
| `esm1b_t33_650M_UR50S` | ESM-1b, 33 layers, 650M parameters, 1280 numbers per residue; the 2020 general-purpose model, below ESM-2 on structure tasks (41.1 against 52.7). | candidate | 7828576466 bytes (7.8 GB) plus regression file; PyTorch | Try it only to reproduce a published ESM-1b result; otherwise use ESM-2 650M. |
| `esm1_t34_670M_UR50S`, `esm1_t34_670M_UR50D`, `esm1_t34_670M_UR100`, `esm1_t12_85M_UR50S`, `esm1_t6_43M_UR50S`, `esm_msa1_t12_100M_UR50S` | The 2020 ESM-1 family and the first MSA Transformer, from the README's model table and the loader list; superseded by ESM-1b, ESM-2 and ESM-MSA-1b. | listed | The same loader path and download host; sizes not checked | Read when a paper to be reproduced used one of these exact names. |
| `esm.pretrained` and `hubconf.py` | The loading entry point: one function per variant returning model and alphabet, a local-file path loader, and the `torch.hub` entry that works without a clone. Contacts come from `model(tokens, return_contacts=True)`. | candidate | The clone and PyTorch; network on the first load of each variant | Try it the first time a model is loaded here, from a local `.pt` path rather than the hub. |
| `scripts/extract.py` | Bulk embedding from a FASTA file: one `.pt` per sequence, chosen layers, `mean` or `per_tok` vectors; batches by `--toks_per_batch` (default 4096) and truncates at `--truncation_seq_length` (default 1022). | candidate | The clone, PyTorch, the chosen checkpoint, a FASTA file; a CUDA device is auto-detected, `--nogpu` forces CPU | Try it on the first batch of sequences that has to become vectors on disk. |
| `examples/variant-prediction/predict.py` | Labels a deep mutational scan with ESM-1v or MSA Transformer scores; strategies `wt-marginals`, `pseudo-ppl`, `masked-marginals`. | candidate | The clone, PyTorch, pandas, biopython, the ESM-1v or MSA checkpoints, a CSV of mutations — and a CUDA GPU in practice: its scoring paths call `.cuda()` even when `--nogpu` is given | Try it on a published mutational scan where the answer is known; on a machine without a CUDA device, expect to patch the scoring call or use the library directly. |
| `examples/inverse_folding/sample_sequences.py` | Samples sequence designs for a backbone in PDB or mmCIF (code read 2026-11-21). Positional `pdbfile`; flags `--chain` (default none), `--temperature` (default one, higher for more diversity), `--num-samples` (default 1), `--outpath` (default `output/sampled_seqs.fasta`, parent folder created), `--multichain-backbone` / `--singlechain-backbone` (default single chain). Multinomial sampling, no beam search. Writes one FASTA record per sample and prints the sequence recovery against the native sequence. | listed | The clone, the ESM-IF1 checkpoint, PyTorch Geometric and biotite, a structure file | On every run it calls `esm.pretrained.esm_if1_gvp4_t16_142M_UR50()`, which fetches the ESM-IF1 checkpoint if it is not cached; nothing else is downloaded. The script only reads the structure and writes the FASTA file. Not run here. |
| `examples/inverse_folding/score_log_likelihoods.py` | Scores variant sequences against a backbone (code read 2026-11-21). Positional `pdbfile` and `seqfile` (FASTA); flags `--chain` (default `A`), `--outpath` (default `output/sequence_scores.csv`, parent folder created), `--multichain-backbone` / `--singlechain-backbone` (default single chain). Prints log-likelihood and perplexity of the native sequence, then writes a `seqid,log_likelihood` CSV, one row per FASTA record. | listed | The clone, the ESM-IF1 checkpoint, PyTorch Geometric, biotite (FASTA reader) and tqdm, a structure and a FASTA | Same checkpoint fetch on every run via `esm.pretrained.esm_if1_gvp4_t16_142M_UR50()`; no other download. How `score_sequence` computes the value (per-residue average or not) lives in `esm.inverse_folding.util` and was not read. Not run here. |
| `examples/esm2_infer_fairscale_fsdp_cpu_offloading.py` | Loads the 15B model layer by layer in Fairscale FSDP with mixed precision and CPU offloading, then runs one forward pass. | candidate | The clone, PyTorch with NCCL, `fairscale`, a CUDA GPU, host RAM, the 30 GB checkpoint | Try it when the 15B model is the only option left and one GPU has to carry it. |
| `esm.data.ESMStructuralSplitDataset` | Five-fold cross-validation set of domain structures with family, superfamily and fold holdouts; 3D coordinates, distance maps and secondary-structure labels, downloaded on first use. | listed | Network for the dataset archives (sizes not checked) and the library | Read when embeddings have to be judged for generalisation rather than on one in-house set. |
| `examples/contact_prediction.ipynb`, `examples/sup_variant_prediction.ipynb`, `examples/esm_structural_dataset.ipynb`, `examples/inverse_folding/notebook.ipynb`, `examples/inverse_folding/notebook_multichain.ipynb` | The repository's five example notebooks: contacts from attention, a supervised variant predictor on embeddings, the structural dataset, and inverse folding for single chains and complexes. | listed | The same environment as the matching script; each carries a Colab badge, so running them there sends the data to a third party | Read one when its script needs a worked example; run locally, not in the hosted notebook. |

## Tried

None yet.

## Verdict

A complete, MIT-licensed collection with one model for each of the protein tasks this catalog cares about: embeddings in six sizes, variant effects, alignment-based contacts and fixed-backbone design. The risk is not the code but its future: the repository is archived, the last push was 2024-02-07, it now sits under a different owner as `esm-archive`, and it names no successor, so nothing here will be fixed upstream. The checkpoints were still served on 2026-11-21. Start with the 8M or 650M ESM-2 model and `scripts/extract.py`, which need no GPU figures to be useful; treat the variant-prediction and inverse-folding scripts as GPU-and-environment work. Revisit when a part is actually needed for a task, when a freshness check shows the archive moved or the download host stopped answering, or when a maintained protein language model has to be compared against ESM-2 before either goes into real work.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; scientific computation and data access
- [[area-science-protein-engineering-and-design|Protein engineering and design]] ([Protein engineering and design](../topics/area-science-protein-engineering-and-design.md)): section page; variant effects, contacts, inverse folding
- [[area-science-machine-learning-and-ai|Machine learning and AI]] ([Machine learning and AI](../topics/area-science-machine-learning-and-ai.md)): section page; sequence embeddings and the models that produce them
- [[agemagician-prottrans|agemagician/ProtTrans]] (../references/agemagician-prottrans.md): the other collection of protein language models in this catalog
- [[dauparas-proteinmpnn|dauparas/ProteinMPNN]] (../references/dauparas-proteinmpnn.md): the other fixed-backbone sequence designer
- [[nvidia-bionemo-bionemo-recipes|NVIDIA-BioNeMo/bionemo-recipes]] (../references/nvidia-bionemo-bionemo-recipes.md): maintained recipes for training and serving protein models

## Sources

- [Desk check: facebookresearch/esm v1.0.3](../../raw/repos/facebookresearch-esm-desk-check-2026-11-21.md): every part read from the clone, the download sizes, the archive and transfer checked through the GitHub API, and what was not checked.
