---
title: "sokrypton/ColabFold"
category: reference
kind: cli
areas: [science]
science_sections: [protein-engineering-and-design]
repo: sokrypton/ColabFold
version: "1.6.3"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/sokrypton-colabfold-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, science-protein-engineering-and-design, kind-cli, colabfold, protein-structure, alphafold2, mmseqs2, msa]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Python CLI and Colab notebooks for protein structure prediction with AlphaFold2 and fast MMseqs2 MSAs. By default colabfold_batch sends the query sequences to the public MSA server at api.colabfold.com; the local route (940GB of databases, colabfold_search, then colabfold_batch on A3M input) keeps them on the machine. Desk-checked at v1.6.3, nothing tried: commands and main notebooks are candidates, the old search script is rejected, minor notebooks are listed."
---

# sokrypton/ColabFold

> A protein structure prediction toolkit (kind `cli`, licence MIT for the code, version `1.6.3` read): the Python commands `colabfold_batch`, `colabfold_search`, `colabfold_split_msas` and `colabfold_relax` that run AlphaFold2 with MMseqs2 MSAs, a database setup script, a self-hosted MSA server, a Dockerfile, and Google Colab notebooks for AlphaFold2, AlphaFold 3, ESMFold, RoseTTAFold2, Boltz and BioEmu. The model weights carry their own licences ("CC BY 4.0" for the AlphaFold2 parameters, as the notebooks state). Here it is read from a clone; nothing is installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Predict the structure of a protein or a complex from its sequence on a local GPU | `colabfold_batch` | science-protein-engineering-and-design |
| Build MSAs for many sequences without the sequences leaving the machine | `colabfold_search` | science-protein-engineering-and-design |
| Download and build the local sequence databases for MSA search | `setup_databases.sh` | science-protein-engineering-and-design |
| Turn sequences into AlphaFold 3 input JSON with MSAs | `colabfold_search` | science-protein-engineering-and-design |
| Split or merge MSA search results into one A3M file per query | `colabfold_split_msas` | science-protein-engineering-and-design |
| Relax existing structures with Amber | `colabfold_relax` | science-protein-engineering-and-design |
| Fetch the model weights ahead of time, so a run makes no download | `colabfold.download` | science-protein-engineering-and-design |
| Give a team its own MSA server, so no sequence goes to the public one | `MsaServer/` | science-protein-engineering-and-design |
| Run ColabFold in a container on a GPU host | `Dockerfile` | science-protein-engineering-and-design |
| Fold a public sequence in a browser when no local GPU is at hand | `AlphaFold2.ipynb` | science-protein-engineering-and-design |
| Predict protein, RNA, DNA and small-molecule complexes with the AlphaFold 3 code | `AlphaFold3_of3.ipynb` | science-protein-engineering-and-design |
| Fold a single sequence fast, without an MSA | `ESMFold.ipynb` | science-protein-engineering-and-design |
| Compare a prediction with a second model | `RoseTTAFold2.ipynb` | science-protein-engineering-and-design |
| Sample an ensemble of conformations instead of one structure | `BioEmu.ipynb` | science-protein-engineering-and-design |
| Not this: build MSAs with the old shell script. Rejected: disabled upstream, it exits at once | `colabfold_search.sh` | science-protein-engineering-and-design |

## Run it here

- **Clone**: `git clone --depth 1 --branch v1.6.3 https://github.com/sokrypton/ColabFold $EXTERNAL/ColabFold`, read-only. Never edit the clone.
- **Version**: `1.6.3`, the latest release, published 2026-09-14. `main` was 8 commits ahead by 2026-11-19 (notebooks, a new `colabfold/rgi/`), none of them in the MSA server code. Before relying on this card: `gh api repos/sokrypton/ColabFold --jq .pushed_at` and `gh api repos/sokrypton/ColabFold/releases/latest --jq .tag_name`.
- **Read first**: `$EXTERNAL/ColabFold/README.md`, then `colabfold/batch.py` (`main`, the arguments), `colabfold/colabfold.py` (`run_mmseqs2`, the server client) and `setup_databases.sh`.
- **Switch off: the public MSA server.** `colabfold_batch` sends the unique query sequences (FASTA, numeric headers, no job names) to `https://api.colabfold.com` for every FASTA, CSV/TSV or PDB/CIF input, unless `--msa-mode single_sequence` is set; `--msa-only` and `--af3-json` do too, and so does `--templates` without local templates, even on A3M input. The server is "a limited shared resource only capable of processing a few thousand MSAs per day". To keep the sequences on the machine: build the databases with `MMSEQS_NO_INDEX=1 ./setup_databases.sh <db_folder>` (940GB of disk, "a couple of hours"), run `colabfold_search --mmseqs <mmseqs> input.fasta <db_folder> msas` (about 128GB RAM), then `colabfold_batch msas predictions` on the A3M output; for templates add `--templates` with `--custom-template-path`, or `--pdb-hit-file` plus `--local-pdb-path`. Or point `--host-url` at your own server (`MsaServer/`).
- **Switch off: other downloads.** The first prediction downloads AlphaFold2 weights from `storage.googleapis.com` into the user cache folder; fetch them once with `python -m colabfold.download` and point `--data` at that folder. `setup_databases.sh` downloads from `opendata.mmseqs.org` and rsyncs PDB files (a `SKIP_TEMPLATES` file in the database folder skips them). No telemetry was found.
- **Notebooks** run on Google Colab: the sequence goes to Google's runtime, and most of them also call the public MSA server. Use them only for sequences that may leave the machine.
- **Do not install**: the package (`pip install colabfold[...]`), the conda environment, the Docker image or the LocalColabFold installer. The commands do not run from the clone without one of them; a real install waits for the user's yes. The GPU path is CUDA (`jax[cuda12]`, `jax[cuda13]`), so it needs an NVIDIA GPU.

## What's inside

Parts: four registered commands, two modules run with `python -m`, two shell scripts, the server folder, the Dockerfile, a weight converter, and the notebooks (one row each for the README's notebooks, one row per folder for the rest).

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `colabfold_batch` | Predicts structures with AlphaFold2 (monomer, multimer, DeepFold), ranks the models, optionally relaxes them with Amber, writes PDB, scores and plots; `--af3-json` writes AlphaFold 3 input instead. Input: FASTA, CSV/TSV, A3M, or a folder of them. | candidate | The installed package with JAX; an NVIDIA GPU ("For GPUs with ~16G the max length is ~2000"); the weight download on first run; the query sequences go to the public MSA server unless the input is A3M or `--msa-mode single_sequence`. | Try it on a published sequence with a known structure, on A3M input from `colabfold_search`, on a Linux host with an NVIDIA GPU. |
| `colabfold_search` | Local MSA search: runs `mmseqs` on a query FASTA against the local databases and writes one A3M per query; `--af3-json` writes AlphaFold 3 input JSON. GPU search with `--gpu 1`. | candidate | `pip install colabfold` is enough; `mmseqs` (Release 18 for the server's MSAs); the 940GB databases; about 128GB RAM and many CPU cores (`--threads 64` by default). No network. | Try it when sequences must not leave the machine and a host with the databases exists. |
| `setup_databases.sh` | Downloads and builds UniRef30, ColabFoldDB and PDB100 for `mmseqs`, and rsyncs PDB mmCIF files for templates. Reruns skip finished steps. | candidate | `mmseqs`, `aria2c`, `curl` or `wget`, `rsync`; 940GB of disk; network for the downloads (no query data leaves). `GPU=1` for GPU databases. | Run it with `DEBUG_MINI_DB=1` first (a small test database), then for real on the host chosen for local search. |
| `colabfold_split_msas` | Splits the combined `final.a3m` of a search folder into one A3M file per MSA. | candidate | The package; reads files only. | Try it when a `colabfold_search` folder holds one combined `final.a3m`. |
| `merge_and_split_msas` | Module (`python -m colabfold.mmseqs.merge_and_split_msas`): merges the UniRef and environmental search results with `mmseqs mergedbs`, then splits them per MSA. | candidate | The package and `mmseqs`. | Try it when a search left `uniref.a3m` and `bfd.mgnify30.metaeuk30.smag30.a3m` separate. |
| `colabfold_relax` | Amber relaxation of a PDB file or a folder of them; `--use-gpu` runs it on GPU. | candidate | The package with the `openmm` extra; CPU or GPU. | Try it on a predicted structure saved unrelaxed. |
| `colabfold.download` | Module (`python -m colabfold.download`): downloads AlphaFold2 weights ahead of time (multimer v3 and pTM by default). | candidate | The package; network once to `storage.googleapis.com`; no sequence is sent. | Run it once on the GPU host before the first prediction. |
| `MsaServer/` | Self-hosted MSA server: `setup-and-start-local.sh` fetches pinned `mmseqs` and `mmseqs-server` binaries, runs `setup_databases.sh` and starts the server on localhost port 8080; a systemd example. | candidate | A Linux server; the databases; "768GB-1024GB RAM" for answers within seconds in CPU mode; `curl`, `aria2c`, `rsync`, `aws`. Sequences go only to this server. | Try it when several people need MSAs for sequences that must not reach the public server. |
| `Dockerfile` | Image with MMseqs2 GPU binaries and ColabFold with `jax[cuda12]`; published as `ghcr.io/sokrypton/colabfold:1.6.3-cuda12`. | candidate | Docker and an NVIDIA GPU; the container still downloads weights and calls the public MSA server unless told otherwise. | Try it on a GPU host where nothing should be installed into the system Python. |
| `colabfold_search.sh` | The old shell version of the search. | rejected | Nothing: it exits at its second line. | Rejected: upstream disabled it ("Do not use this script. Use the python colabfold_search instead"). Revisit if upstream enables it again. |
| `utils/convert_deepfold_weights.py` | Converts a DeepFold weights `.npz` into AlphaFold parameter names. | candidate | numpy; loads pickled data, so trusted files only. | Try it only when DeepFold weights arrive in their original `.npz` form. |
| `utils/plot_scores.ipynb` | Plots from a run's `scores.json` (title only). | listed | Jupyter, not checked. | Read when scores of a `colabfold_batch` run need plots. |
| `AlphaFold2.ipynb` | AlphaFold2 with MMseqs2 MSAs on Colab, monomers and complexes, templates; `custom` mode takes an uploaded A3M. | candidate | A Google account and Colab; the sequence goes to Google and, in MMseqs2 modes, to the public MSA server. | Try it on a public sequence when no local GPU is at hand. |
| `batch/AlphaFold2_batch.ipynb` | The same for a folder of inputs, with Google Drive mounted. | candidate | Colab and Google Drive; the sequences go to Google and to the public MSA server. | Try it for a batch of public sequences. |
| `AlphaFold3_of3.ipynb` | AlphaFold 3 code on Colab for protein, RNA, DNA and small-molecule complexes, with OpenFold3 weights (Apache 2.0) or the official AlphaFold 3 weights. As shipped, `use_af3_weights = True`, although its text says OpenFold3 is the default. | candidate | Colab; the sequence goes to Google and, in `mmseqs2_server` mode, to the public MSA server; the official weights are "subject to the [AF3 weights terms of use]". | Try it on a public complex; untick `use_af3_weights` unless those terms are accepted. |
| `ESMFold.ipynb` | ESMFold on Colab, single sequence, no MSA. | candidate | Colab; the sequence goes to Google only. | Try it for a quick fold of a public sequence. |
| `RoseTTAFold2.ipynb` | RoseTTAFold2 on Colab with ColabFold's MSA client. | candidate | Colab; the sequence goes to Google and to the public MSA server. | Try it to compare a prediction with AlphaFold2 on a public sequence. |
| `Boltz1.ipynb` | Boltz on Colab; the MSA comes from `colabfold_batch --msa-only`. | candidate | Colab; the sequence goes to Google and to the public MSA server. | Try it as a second model on a public complex. |
| `BioEmu.ipynb` | Samples structure ensembles with BioEmu (`bioemu-v1.0` or `bioemu-v1.1`), then runs `foldseek`. | candidate | Colab; how the `bioemu` package builds its MSA was not checked. | Try it when a task needs conformations rather than one structure; check the MSA route first. |
| `RoseTTAFold.ipynb` | Older RoseTTAFold on Colab (not in the README table), MSA from the public server. | candidate | Colab; the sequence goes to Google and to the public MSA server; weights from `files.ipd.uw.edu`. | Try it only to reproduce older RoseTTAFold results. |
| `beta/relax_amber.ipynb` | Amber relaxation of an uploaded structure on Colab. | candidate | Colab; the structure goes to Google. | Try it on a public structure when no local OpenMM exists. |
| `beta/omegafold.ipynb` | OmegaFold on Colab, single sequence, no MSA. | candidate | Colab; the sequence goes to Google only. | Try it next to `ESMFold.ipynb` on a public sequence. |
| `beta/` other notebooks: `AlphaFold2_advanced.ipynb`, `AlphaFold2_advanced_beta.ipynb`, `AlphaFold2_advanced_old.ipynb`, `AlphaFold2_complexes.ipynb`, `AlphaFold_wJackhmmer.ipynb`, `Alphafold_single.ipynb`, `ESMFold.ipynb`, `ESMFold_advanced.ipynb`, `ESMFold_api.ipynb`, `RoseTTAFold.ipynb`, `alphafold_output_at_each_recycle.ipynb`, `convert_256_to_384_rep.ipynb`, `omegafold_hacks.ipynb` | "BETA (in development) notebooks" and older variants (titles only). | listed | Colab; not checked. | Read one when a task needs its option, for example jackhmmer MSAs (`AlphaFold_wJackhmmer.ipynb`). |
| `verbose/` notebooks: `alphafold_noTemplates_noMD.ipynb`, `alphafold_noTemplates_yesMD.ipynb` | AlphaFold notebooks without templates (titles only). | listed | Colab; not checked. | Read when the notebooks above do not fit. |

## Tried

None yet: no part has been run here.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

Nothing was run; the rows rest on the desk check of `1.6.3`. On a Linux host with an NVIDIA GPU, `colabfold_batch` is the route to structure prediction, but its default sends the sequences to the public MSA server, and every notebook sends them to Google Colab. For sequences that must stay on the machine only the local route counts: the 940GB databases, `colabfold_search`, then `colabfold_batch` on A3M input with templates off or local. Revisit when the freshness check shows a release after `1.6.3` (re-read `colabfold/colabfold.py` and `colabfold/batch.py` for the server path first), or when a protein structure task arrives.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; the science sections
- [[area-science-protein-engineering-and-design|Protein engineering and design]] ([Protein engineering and design](../topics/area-science-protein-engineering-and-design.md)): section page; every part of this card
- [[google-deepmind-alphafold|google-deepmind/alphafold]] (../references/google-deepmind-alphafold.md): the AlphaFold2 code and weights ColabFold runs, with full genetic databases instead of MMseqs2
- [[facebookresearch-esm|facebookresearch/esm]] (../references/facebookresearch-esm.md): the ESMFold model behind `ESMFold.ipynb`

## Sources

- [Desk check: sokrypton/ColabFold v1.6.3](../../raw/repos/sokrypton-colabfold-desk-check-2026-11-21.md): every part read from the clone, the MSA server path re-read in the code, freshness checked through the GitHub API.
