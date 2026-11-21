---
title: "Desk check: google-deepmind/alphafold v2.3.2"
source: https://github.com/google-deepmind/alphafold/tree/v2.3.2
type: repos
authors: ["DeepMind"]
source_date: 2023-04-05
ingested: 2026-11-21
repo: google-deepmind/alphafold
kind: app
version: "2.3.2"
licence: Apache-2.0
tags: [catalog, desk-check, kind-app, alphafold, protein-structure, docker, gpu, genetic-databases, science]
summary: "AlphaFold v2.3.2 read from a read-only clone: the Docker launcher and image, the pipeline script, eleven database download scripts, the Colab notebook, the AlphaFold DB access guide, the library and docs. Code Apache 2.0, model parameters CC BY 4.0; Linux with an NVIDIA GPU and Docker; full genetic databases 556 GB to download and 2.62 TB unzipped; no network call at prediction time."
---

# Desk check: google-deepmind/alphafold v2.3.2

Read from a shallow clone of tag `v2.3.2` (commit `3f31725591b0c6b0b6d63214235d3abe6b81742c`, committed 2023-03-27), at `$EXTERNAL/alphafold`. The clone was not modified; nothing was installed, built, downloaded or run. Checked 2026-11-21. Version read by this desk check: 2.3.2.

## Repository facts

- `README.md`: "This package provides an implementation of the inference pipeline of AlphaFold v2", plus AlphaFold-Multimer, which "represents a work in progress", a technical note for v2.3.0 and a CASP15 baseline set of predictions. 111 files tracked; the README has 819 lines.
- `LICENSE`: Apache License, Version 2.0. GitHub reports `Apache-2.0`.
- Model parameters have separate terms. README, "Model parameters": "While the AlphaFold code is licensed under the Apache 2.0 License, the AlphaFold parameters and CASP15 prediction data are made available under the terms of the CC BY 4.0 license." "Model Parameters License": "The AlphaFold parameters are made available under the terms of the Creative Commons Attribution 4.0 International (CC BY 4.0) license." The parameter tar holds its own `LICENSE` file (16 files in `params/`).
- Mirrored databases (README, "Mirrored Databases"): BFD (unmodified and modified) and UniRef30 v2021_03 under Creative Commons Attribution-ShareAlike 4.0; MGnify v2022_05 under CC0 1.0. Other third-party software "may be governed by separate terms".
- `setup.py` at this tag says `version='2.3.1'`, `author='DeepMind'`; the Colab notebook also says "AlphaFold v2.3.1". The tag and release are v2.3.2.
- Release notes of v2.3.2 (GitHub release body): more robust download in Colab, an option to relax only the best model, documentation of ranked outputs, results pickle without a jax dependency, TensorFlow 2.11.0, Python 3.9 in Colab, other fixes.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/google-deepmind/alphafold`: `pushed_at` 2026-04-22T17:58:21Z; licence `Apache-2.0`; default branch `main`; not archived.
- `gh api repos/google-deepmind/alphafold/releases/latest`: tag `v2.3.2`, name "Alphafold v2.3.2", published 2023-04-05T09:45:53Z. The clone is at the latest release.
- `gh api repos/google-deepmind/alphafold/compare/v2.3.2...main`: `main` is 96 commits ahead of the tag, touching `run_alphafold.py`, `docker/`, the download scripts, the README and the library, and adding a `server/` folder. No release has been cut from them. Not read.

## How to run here

- Clone: `git clone --depth 1 --branch v2.3.2 https://github.com/google-deepmind/alphafold $EXTERNAL/alphafold`, read-only.
- Platform: "You will need a machine running Linux, AlphaFold does not support other operating systems. Full installation requires up to 3 TB of disk space to keep genetic databases (SSD storage is recommended) and a modern NVIDIA GPU (GPUs with more memory can predict larger protein structures)."
- Route given by the README: install Docker and the NVIDIA Container Toolkit; download databases and parameters with `scripts/download_all_data.sh <DOWNLOAD_DIR>` (needs `aria2c`); build the image with `docker build -f docker/Dockerfile -t alphafold .`; `pip3 install -r docker/requirements.txt` (`absl-py==1.0.0`, `docker==5.0.0`) for the launcher; run `python3 docker/run_docker.py --fasta_paths=... --max_template_date=... --data_dir=$DOWNLOAD_DIR --output_dir=...`. Each of these steps is an install or a large download, which waits for the user's yes.
- Reference machine: "This was tested on Google Cloud with a machine using the `nvidia-gpu-cloud-image` with 12 vCPUs, 85 GB of RAM, a 100 GB boot disk, the databases on an additional 3 TB disk, and an A100 GPU."
- Database presets: `full_dbs` (default) "runs with all genetic databases used at CASP14"; `reduced_dbs` "is optimized for speed and lower hardware requirements. It runs with a reduced version of the BFD database. It requires 8 CPU cores (vCPUs), 8 GB of RAM, and 600 GB of disk space."
- Sizes: "The total download size for the full databases is around 556 GB and the total size when unzipped is 2.62 TB." Per folder (README directory tree, unzipped and download): `bfd/` ~ 1.8 TB (271.6 GB), `mgnify/` ~ 120 GB (67 GB), `params/` ~ 5.3 GB (5.3 GB), `pdb70/` ~ 56 GB (19.5 GB), `pdb_mmcif/` ~ 238 GB (43 GB, "About 199,000 .cif files"), `pdb_seqres/` ~ 0.2 GB (0.2 GB), `small_bfd/` ~ 17 GB (9.6 GB), `uniref30/` ~ 206 GB (52.5 GB), `uniprot/` ~ 105 GB (53 GB), `uniref90/` ~ 67 GB (34 GB). `bfd/` comes only with the full databases, `small_bfd/` only with the reduced ones; `pdb_seqres/` and `uniprot/` are "only for AlphaFold-Multimer".
- Prediction speed (README table, one A100, unrelaxed, three recycles, MSA and template search excluded): 100 residues 4.9 s; 400 residues 18 s; 1,000 residues 96 s; 2,000 residues 450 s; 5,000 residues 18,824 s.
- GPU memory: `run_docker.py` sets `TF_FORCE_UNIFIED_MEMORY` to `1` and `XLA_PYTHON_CLIENT_MEM_FRACTION` to `4.0`, which "allow us to make predictions on proteins that would typically be too long to fit into GPU memory".

### Outbound calls

- At prediction time: none. A search for URLs, `requests` and `urllib` across `alphafold/` and `run_alphafold.py` (tests excluded) found only licence and paper links in comments. The genetic search runs locally (jackhmmer, hhblits, hhsearch, hmmsearch, hmmbuild, kalign) against the downloaded databases, so the query sequences stay on the machine.
- At setup: the download scripts fetch from `storage.googleapis.com` (`alphafold` and `alphafold-databases` buckets), `wwwuser.gwdg.de` (PDB70), the EBI and UniProt FTP servers, `ftp.wwpdb.org` (PDB seqres) and `rsync.rcsb.org` on port 33444 (PDB mmCIF). The Docker build pulls `nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu18.04`, clones hh-suite v3.3.0 from GitHub, downloads Miniconda, one file from `git.scicore.unibas.ch` and the jax wheels. Downloads only; no query data leaves.
- The Colab notebook runs on Google Colab: the sequence goes to Google's runtime, which streams database chunks from `storage.googleapis.com` and runs jackhmmer there. No MSA server is involved.
- No telemetry was found.

## Parts

### Launcher: docker/run_docker.py

- Starts the `alphafold` image with the Docker Python client: mounts each FASTA file, the database paths under `--data_dir` and the output folder into the container, requests NVIDIA GPUs (`--use_gpu`, default true; `--gpu_devices`, default `all`), runs as the current user (`--docker_user`), and streams the logs; Ctrl+C kills the container.
- Flags passed through: `--fasta_paths`, `--max_template_date`, `--db_preset` (`full_dbs`, `reduced_dbs`), `--model_preset` (`monomer`, `monomer_casp14`, `monomer_ptm`, `multimer`), `--num_multimer_predictions_per_model` (default 5, so "25 total predictions" for multimer), `--models_to_relax` (`best`, `all`, `none`), `--enable_gpu_relax`, `--use_precomputed_msas`, `--benchmark`. Output default `/tmp/alphafold`.
- Needs: Docker, the NVIDIA Container Toolkit, the built image, the databases, `absl-py` and `docker` in a Python environment.

### Image: docker/Dockerfile

- `FROM nvidia/cuda:${CUDA}-cudnn8-runtime-ubuntu18.04` with `CUDA=11.1.1`; installs HMMER and kalign from apt, builds hh-suite v3.3.0, installs Miniconda with Python 3.8, OpenMM 7.5.1 and pdbfixer, the Python requirements and `jax==0.3.25` with a CUDA 11 `jaxlib`, applies `docker/openmm.patch`, and sets `run_alphafold.py` as the entry point.
- Needs: Docker and network for the build. The README notes a GPG error on the NVIDIA apt repository and links a workaround.

### Pipeline: run_alphafold.py

- The pipeline itself (run inside the image, or directly when the tools are installed): genetic search, template search, model inference, ranking by pLDDT, Amber relaxation. Required flags: `fasta_paths`, `output_dir`, `data_dir`, `uniref90_database_path`, `mgnify_database_path`, `template_mmcif_dir`, `max_template_date`, `obsolete_pdbs_path`, `use_gpu_relax`; the BFD, small BFD, UniRef30, PDB70, PDB seqres and UniProt paths are checked against the chosen presets: small BFD for `reduced_dbs`, BFD and UniRef30 for `full_dbs`, PDB70 for the monomer presets, PDB seqres and UniProt for `multimer`. Binary paths default to `shutil.which` of jackhmmer, hhblits, hhsearch, hmmsearch, hmmbuild and kalign.
- Output per target: `features.pkl`, `ranked_{0,1,2,3,4}.pdb`, `ranking_debug.json`, `relax_metrics.json`, `relaxed_model_*.pdb`, `result_model_*.pkl`, `timings.json`, `unrelaxed_model_*.pdb`, and `msas/`. pLDDT is stored in the B-factor column.
- "The provided inference script is optimized for predicting the structure of a single protein"; "We do not provide a bulk inference script".
- Needs: Linux, an NVIDIA GPU, the databases and parameters, the search binaries, JAX, OpenMM.

### Script: scripts/download_all_data.sh

- Downloads parameters and every database into `<DOWNLOAD_DIR>`; a second argument `reduced_dbs` takes small BFD instead of BFD. "The download directory `<DOWNLOAD_DIR>` should *not* be a subdirectory in the AlphaFold repository directory." Needs `aria2c`, `rsync`; 556 GB of downloads and 2.62 TB of disk for the full set.

### Script: scripts/download_alphafold_params.sh

- Downloads `https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar` (5 CASP14 models, 5 pTM models, 5 AlphaFold-Multimer models, `LICENSE`), ~ 5.3 GB. The README explains how to switch back to the deprecated v2.2.0 or v2.1.0 multimer weights.

### Scripts: one per database

- `scripts/download_bfd.sh`: BFD from the `alphafold-databases` bucket (`casp14_versions`), ~ 1.8 TB (271.6 GB); full databases only.
- `scripts/download_small_bfd.sh`: reduced BFD (`reduced_dbs`), ~ 17 GB (9.6 GB).
- `scripts/download_mgnify.sh`: `mgy_clusters_2022_05.fa`, ~ 120 GB (67 GB).
- `scripts/download_pdb70.sh`: PDB70 from `wwwuser.gwdg.de` (`pdb70_from_mmcif_200401`), ~ 56 GB (19.5 GB).
- `scripts/download_pdb_mmcif.sh`: every PDB mmCIF file by rsync from `rsync.rcsb.org` port 33444 (it names EBI and PDBj mirrors if slow), ~ 238 GB (43 GB).
- `scripts/download_pdb_seqres.sh`: `pdb_seqres.txt` from `ftp.wwpdb.org`, filtered to proteins, ~ 0.2 GB; multimer only. PDB seqres and PDB mmCIF must come from the same date.
- `scripts/download_uniref30.sh`: `UniRef30_2021_03`, ~ 206 GB (52.5 GB).
- `scripts/download_uniprot.sh`: TrEMBL and Swiss-Prot from the EBI FTP server, merged into `uniprot.fasta`, ~ 105 GB (53 GB); multimer only.
- `scripts/download_uniref90.sh`: `uniref90.fasta` from the UniProt FTP server, ~ 67 GB (34 GB).
- Each needs `aria2c` (the mmCIF script also `rsync`) and the disk named.

### Notebook: notebooks/AlphaFold.ipynb (Colab)

- "a slightly simplified version of AlphaFold v2.3.1": "no templates (homologous structures) and a selected portion of the BFD database"; "a small fraction have a large drop in accuracy due to the smaller MSA and lack of templates", and multimers lose some accuracy against a local run. Downloads `alphafold_params_colab_2022-12-06.tar`; streams database chunks from `storage.googleapis.com/alphafold-colab...` and runs jackhmmer in the runtime; results are downloaded as a zip.
- Needs: a Google account and Colab; the sequence goes to Google's runtime.

### Guide: afdb/README.md (AlphaFold Protein Structure Database)

- How to get precomputed predictions instead of running AlphaFold: "The AlphaFold UniProt release (214M predictions)" in a public Google Cloud Storage bucket named `public-datasets-deepmind-alphafold-v4`, metadata on BigQuery. "A Google Cloud account is required for the download". Licence: "Data is available for academic and commercial use, under a CC-BY-4.0 licence".
- Size: "the size of the dataset is 23 TiB, 3 * 214M files"; a bulk download is 1,015,797 sharded proteome tar files, "roughly 2.5 days" on a 1 Gbps connection, about 644M files after unpacking. Subsets: the search bar on `alphafold.ebi.ac.uk` for single proteins, premade species and Swiss-Prot sets on its download page, 3D-Beacons, file manifests with `gsutil -m cp -I`, BigQuery (free tier with "1 TB of free processed query data each month").
- Per entry: `model_v4.cif`, `confidence_v4.json` (pLDDT) and `predicted_aligned_error_v4.json`.
- Needs: network; for bulk or custom subsets a Google Cloud account and `gsutil`; BigQuery and the Storage Transfer Service can incur costs beyond the free tier.

### Library: the alphafold package (`alphafold/`)

- Subpackages `common`, `data` (pipelines and tool wrappers), `model`, `relax`, `notebooks`. The README points to `RunModel.predict` and `make_fixed_size` for anyone building bulk inference. Read by layout only.

### Docs: docs/technical_note_v2.3.0.md and docs/casp15_predictions.zip

- The note describes v2.3.0: new AlphaFold-Multimer weights fine-tuned "using identical model architecture but a new training cutoff of 2021-09-30". The zip is the CASP15 baseline set of predictions. Read by title and first paragraph only.

## Reasons for any rejection or reference status

- No part is rejected, in use or tried; there is no record of use.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 69 model calls on opus, $5.03 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
