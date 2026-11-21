---
title: "google-deepmind/alphafold"
category: reference
kind: app
areas: [science]
science_sections: [protein-engineering-and-design, scientific-databases]
repo: google-deepmind/alphafold
version: "2.3.2"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/google-deepmind-alphafold-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, science-protein-engineering-and-design, science-scientific-databases, kind-app, alphafold, protein-structure, docker, gpu, genetic-databases]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "The AlphaFold v2 inference pipeline (monomer and multimer): a Docker launcher and image, the pipeline script, database download scripts, a Colab notebook, and a guide to the AlphaFold Protein Structure Database. Code Apache 2.0, model parameters CC BY 4.0. Needs Linux, an NVIDIA GPU, Docker and 2.62 TB of genetic databases (600 GB reduced); no network call at prediction time. Desk-checked at v2.3.2, nothing tried."
---

# google-deepmind/alphafold

> The AlphaFold v2 inference pipeline (kind `app`, code licence Apache-2.0, version `2.3.2` read): `run_alphafold.py` with its Docker launcher and image, scripts that download the model parameters and the genetic databases, a simplified Colab notebook, and a guide to downloading precomputed predictions from the AlphaFold Protein Structure Database. The model parameters are under separate terms: "CC BY 4.0". Here it is read from a clone; nothing is installed or downloaded.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Predict a protein structure from its sequence with the full AlphaFold pipeline, sequences kept on the host | `docker/run_docker.py` | science-protein-engineering-and-design |
| Predict the structure of a complex, a homomer or a heteromer (`--model_preset=multimer`) | `docker/run_docker.py` | science-protein-engineering-and-design |
| Run the pipeline on smaller hardware with the reduced databases (`--db_preset=reduced_dbs`) | `docker/run_docker.py` | science-protein-engineering-and-design |
| Rerun a prediction with other settings without repeating the genetic search (`--use_precomputed_msas`) | `run_alphafold.py` | science-protein-engineering-and-design |
| Download the model parameters and the genetic databases | `scripts/download_all_data.sh` | science-protein-engineering-and-design |
| Build a bulk inference script on the model code | `alphafold` package | science-protein-engineering-and-design |
| Fold a public sequence in a browser, without the databases | `notebooks/AlphaFold.ipynb` | science-protein-engineering-and-design |
| Get the predicted structure of a UniProt protein without running a prediction | `afdb/README.md` | science-scientific-databases |
| Download predicted structures for whole proteomes or a custom list | `afdb/README.md` | science-scientific-databases |

## Run it here

- **Clone**: `git clone --depth 1 --branch v2.3.2 https://github.com/google-deepmind/alphafold $EXTERNAL/alphafold`, read-only. Never edit the clone.
- **Version**: `2.3.2`, the latest release, published 2023-04-05. `main` is 96 commits ahead with no newer release (not read). At this tag `setup.py` still says `2.3.1`. Before relying on this card: `gh api repos/google-deepmind/alphafold --jq .pushed_at` and `gh api repos/google-deepmind/alphafold/releases/latest --jq .tag_name`.
- **Read first**: `$EXTERNAL/alphafold/README.md` (installation, genetic databases, running, licences), then `docker/run_docker.py` and `run_alphafold.py`.
- **Where it runs**: "AlphaFold does not support other operating systems" than Linux; it needs a modern NVIDIA GPU, Docker with the NVIDIA Container Toolkit, and up to 3 TB of disk (SSD recommended). It does not run on macOS. Reference machine in the README: 12 vCPUs, 85 GB of RAM, an A100 GPU, databases on a 3 TB disk. The `reduced_dbs` preset needs 8 CPU cores, 8 GB of RAM and 600 GB of disk.
- **Licences**: code Apache 2.0; model parameters CC BY 4.0, with their own `LICENSE` file in the parameter tar; mirrored databases keep theirs (BFD and UniRef30 Creative Commons Attribution-ShareAlike 4.0, MGnify CC0 1.0); AlphaFold DB data CC-BY-4.0.
- **Switch off**: nothing at prediction time. No network call was found in `run_alphafold.py` or the library; the genetic search runs locally, so sequences stay on the host once the databases are there. The download scripts (556 GB) and the Docker build fetch from the network. The Colab notebook sends the sequence to Google's runtime.
- **Do not install**: the Docker image, the NVIDIA Container Toolkit, the databases (`scripts/download_all_data.sh`) or the launcher's requirements (`pip3 install -r docker/requirements.txt`). The clone is readable as it is; running needs all of them, and a real install or download waits for the user's yes.

## What's inside

Parts: the launcher, the image, the pipeline script, eleven download scripts (one row each), the Colab notebook, the AlphaFold DB guide, the library and two documents.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `docker/run_docker.py` | Starts the `alphafold` image: mounts the FASTA files, the databases and the output folder, requests NVIDIA GPUs, passes the presets (`monomer`, `monomer_casp14`, `monomer_ptm`, `multimer`; `full_dbs`, `reduced_dbs`), relaxes the best model by default; multimer runs 5 seeds per model, "25 total predictions". | candidate | Linux, Docker, the NVIDIA Container Toolkit, the built image, the databases; `absl-py` and `docker` in a venv. On one A100: 400 residues 18 s, 1,000 residues 96 s, 2,000 residues 450 s (MSA search excluded). No network. | Try it on a published monomer with a known structure, with `--db_preset=reduced_dbs`, on a Linux GPU host. |
| `docker/Dockerfile` | Image on `nvidia/cuda` `11.1.1` with Ubuntu 18.04: HMMER, kalign, hh-suite `v3.3.0`, Python `3.8`, OpenMM `7.5.1`, `jax==0.3.25`; entry point `run_alphafold.py`. | candidate | Docker and network for the build (base image, GitHub, Miniconda, jax wheels). | Build it on the GPU host before the first run; check the NVIDIA apt GPG note in the README. |
| `run_alphafold.py` | The pipeline: genetic and template search, inference, ranking by pLDDT, Amber relaxation; writes `ranked_*.pdb`, `result_model_*.pkl`, `timings.json` and `msas/`. "optimized for predicting the structure of a single protein". | candidate | Inside the image, or jackhmmer, hhblits, hhsearch, hmmsearch, hmmbuild, kalign, JAX and OpenMM installed by hand; an NVIDIA GPU; every database path. No network. | Try `--use_precomputed_msas` when rerunning a target with another model preset. |
| `scripts/download_all_data.sh` | Downloads the parameters and every database; `reduced_dbs` takes small BFD instead of BFD. | candidate | `aria2c`, `rsync`; 556 GB of downloads, 2.62 TB of disk (full); a folder outside the repository. | Run it on the GPU host chosen for AlphaFold, in the background. |
| `scripts/download_alphafold_params.sh` | Downloads the parameters: 5 CASP14, 5 pTM and 5 AlphaFold-Multimer models, under CC BY 4.0. | candidate | `aria2c`; 5.3 GB from `storage.googleapis.com`. | Run it alone when only the weights change, as the README's update steps do. |
| `scripts/download_bfd.sh` | Full BFD. | candidate | `aria2c`; 1.8 TB on disk (271.6 GB download). | Run it only for `full_dbs`. |
| `scripts/download_small_bfd.sh` | Reduced BFD for `reduced_dbs`. | candidate | `aria2c`; 17 GB (9.6 GB download). | Run it for a first, smaller setup. |
| `scripts/download_mgnify.sh` | MGnify clusters `2022_05`. | candidate | `aria2c`; 120 GB (67 GB download). | Run it with any setup. |
| `scripts/download_pdb70.sh` | PDB70 for monomer template search. | candidate | `aria2c`; 56 GB (19.5 GB download). | Run it for monomer presets. |
| `scripts/download_pdb_mmcif.sh` | Every PDB mmCIF file by rsync, for templates. | candidate | `aria2c`, `rsync` (port 33444); 238 GB (43 GB download). | Run it with any setup; rerun with PDB seqres for multimer. |
| `scripts/download_pdb_seqres.sh` | PDB seqres, proteins only, for multimer templates. | candidate | `aria2c`; 0.2 GB; same date as the mmCIF files. | Run it for `multimer`. |
| `scripts/download_uniref30.sh` | UniRef30 `2021_03`. | candidate | `aria2c`; 206 GB (52.5 GB download). | Run it for `full_dbs`. |
| `scripts/download_uniprot.sh` | TrEMBL plus Swiss-Prot, merged, for multimer MSA pairing. | candidate | `aria2c`; 105 GB (53 GB download). | Run it for `multimer`. |
| `scripts/download_uniref90.sh` | UniRef90. | candidate | `aria2c`; 67 GB (34 GB download). | Run it with any setup. |
| `notebooks/AlphaFold.ipynb` | "a slightly simplified version of AlphaFold v2.3.1" on Colab: no templates, part of BFD; "a small fraction have a large drop in accuracy due to the smaller MSA and lack of templates". | candidate | A Google account and Colab; the sequence goes to Google's runtime; no MSA server. | Try it on a public sequence when no Linux GPU host is at hand. |
| `afdb/README.md` | How to get precomputed AlphaFold predictions: "The AlphaFold UniProt release (214M predictions)", per entry `model_v4.cif`, pLDDT and PAE JSON; single proteins on `alphafold.ebi.ac.uk`, subsets by manifest or BigQuery, bulk from a public Cloud Storage bucket. | candidate | Network; for bulk or custom subsets a Google Cloud account and `gsutil`. Full set 23 TiB, about 644M files after unpacking, "roughly 2.5 days" at 1 Gbps; BigQuery and transfers can cost money past the free tier. Data CC-BY-4.0. | Try it before predicting any protein that has a UniProt accession. |
| `alphafold` package | Library with `common`, `data`, `model`, `relax`, `notebooks`; the README points to `RunModel.predict` and `make_fixed_size` for bulk inference ("We do not provide a bulk inference script"). | listed | A venv with JAX and the pinned requirements; not checked. | Read when many proteins must be predicted and one run per protein is too slow. |
| `docs/technical_note_v2.3.0.md` | Notes on v2.3.0: new multimer weights with a training cutoff of 2021-09-30. | listed | Nothing; a document. | Read when choosing between multimer weight versions. |
| `docs/casp15_predictions.zip` | The CASP15 baseline set of predictions. | listed | Nothing; data under CC BY 4.0. | Read when a baseline for CASP15 targets is needed. |

## Tried

None yet: no part has been run here.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

Nothing was run; the rows rest on the desk check of `2.3.2`. AlphaFold is the full pipeline for a Linux host with an NVIDIA GPU, Docker and 2.62 TB of databases (600 GB with `reduced_dbs`); once the databases are local it makes no network call, so sequences stay on the host. For a protein that already has a UniProt accession, the AlphaFold DB guide gives a precomputed structure without any of that. Revisit when a release after `2.3.2` appears (96 unreleased commits are on `main`), or when a structure task needs the full pipeline rather than ColabFold.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; the science sections
- [[area-science-protein-engineering-and-design|Protein engineering and design]] ([Protein engineering and design](../topics/area-science-protein-engineering-and-design.md)): section page; the pipeline, scripts and notebook
- [[area-science-scientific-databases|Scientific databases and data access]] ([Scientific databases and data access](../topics/area-science-scientific-databases.md)): section page; the AlphaFold DB guide
- [[sokrypton-colabfold|sokrypton/ColabFold]] (../references/sokrypton-colabfold.md): runs the same AlphaFold2 model with MMseqs2 MSAs instead of the full databases

## Sources

- [Desk check: google-deepmind/alphafold v2.3.2](../../raw/repos/google-deepmind-alphafold-desk-check-2026-11-21.md): every part read from the clone, licences of code, parameters and databases, sizes, freshness checked through the GitHub API.
