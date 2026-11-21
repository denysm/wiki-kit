---
title: "Desk check: sokrypton/ColabFold v1.6.3"
source: https://github.com/sokrypton/ColabFold/tree/v1.6.3
type: repos
authors: ["Milot Mirdita", "Sergey Ovchinnikov", "Martin Steinegger", "Kostantin Schütze", "Yoshitaka Moriwaki", "Lim Heo"]
source_date: 2026-09-14
ingested: 2026-11-21
repo: sokrypton/ColabFold
kind: cli
version: "1.6.3"
licence: MIT
tags: [catalog, desk-check, kind-cli, colabfold, protein-structure, alphafold2, mmseqs2, msa, science]
summary: "ColabFold v1.6.3 read from a read-only clone: four commands (colabfold_batch, colabfold_search, colabfold_split_msas, colabfold_relax), the weight downloader, the database setup script, the self-hosted MSA server, the Dockerfile and the Colab notebooks. Re-reads the decided case: FASTA or CSV input to colabfold_batch sends the sequences to the public MSA server at api.colabfold.com; local databases (940GB) and colabfold_search keep them on the machine."
---

# Desk check: sokrypton/ColabFold v1.6.3

Read from a shallow clone of tag `v1.6.3` (commit `84c27d9cc500489fd9b97545d2325b9d00f251d5`, committed 2026-09-14), at `$EXTERNAL/ColabFold`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 1.6.3.

## Repository facts

- `pyproject.toml`: `name = "colabfold"`, `version = "1.6.3"`, `license = "MIT, but separate licenses for the trained weights"`, Python ">=3.10". Four console commands: `colabfold_batch = 'colabfold.batch:main'`, `colabfold_search = 'colabfold.mmseqs.search:main'`, `colabfold_split_msas = 'colabfold.mmseqs.split_msas:main'`, `colabfold_relax = 'colabfold.relax:main'`. Extras: `alphafold` (AlphaFold2 code as `alphafold-colabfold` 2.3.20, JAX, Haiku, prebuilt binaries), `alphafold-minus-jax`, `openmm`.
- `LICENSE`: "MIT License", copyright 2021 by the upstream author. GitHub reports `MIT`.
- Weights are not covered by the MIT licence. The licence cell of the notebooks `AlphaFold2.ipynb` and `batch/AlphaFold2_batch.ipynb`: ColabFold source is MIT, and the notebook "uses the AlphaFold2 source code and its parameters licensed under [Apache 2.0] and [CC BY 4.0] respectively".
- `README.md` heading: "ColabFold - v1.6.3", "Making Protein folding accessible to all via Google Colab!". 121 files tracked; the README has 293 lines.
- Release notes of v1.6.3 (GitHub release body): "ColabFold can now be fully installed from pip"; Turing and Volta GPUs "are now much faster with `--use-fast-kernels`"; ipSAE and pDockQ2 interface scores for complexes; kalign, hhsearch and openmm from pip, "No conda needed for the local install"; a fix for `--msa-mode single_sequence` that used "one additional randomly picked homolog per seed" with A3M or cached input.
- Parts live in: `colabfold/` (the package and its four commands), `setup_databases.sh`, `colabfold_search.sh`, `MsaServer/`, `Dockerfile`, `utils/`, and notebooks at the top level and in `batch/`, `beta/`, `verbose/`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/sokrypton/ColabFold`: `pushed_at` 2026-11-19T16:08:26Z; licence `MIT`; default branch `main`; not archived.
- `gh api repos/sokrypton/ColabFold/releases/latest`: tag `v1.6.3`, name "ColabFold 1.6.3", published 2026-09-14T07:02:37Z. The clone is at the latest release.
- `gh api repos/sokrypton/ColabFold/compare/v1.6.3...main`: `main` is 8 commits ahead (2026-09-19 to 2026-11-09): a `ColabFold2_preview` notebook, an "RGI" toolkit (`colabfold/rgi/`), notebook updates, `colabfold/alphafold/models.py`, `colabfold/citations.py`, `pyproject.toml`. None of them touches `colabfold/colabfold.py`, `colabfold/batch.py`, `colabfold/mmseqs/` or `setup_databases.sh`, so the MSA server findings below still hold on `main`. Not read.

## How to run here

- Clone: `git clone --depth 1 --branch v1.6.3 https://github.com/sokrypton/ColabFold $EXTERNAL/ColabFold`, read-only.
- Nothing runs from the clone without installing: the commands need the Python package with JAX (README: `pip install colabfold[alphafold,openmm] jax[cuda12] openmm[cuda12]`; "CUDA 13 is recommended if you have a Blackwell GPU or newer"; a "CPU only" install `pip install colabfold[alphafold,openmm]`; and `pip install colabfold` "For colabfold_search only (no structure prediction)"). The README's conda line adds `mmseqs2=18.8cc5c`. Alternatives: the Docker image `ghcr.io/sokrypton/colabfold:1.6.3-cuda12`, or the third-party LocalColabFold installer. Every one of these is an install, which waits for the user's yes.
- GPU: the README's GPU installs are CUDA builds (`jax[cuda12]`, `jax[cuda13]`). FAQ: "For GPUs with ~16G the max length is ~2000". `colabfold/utils.py` has an error text `NO_GPU_FOUND` that says to "pass `--cpu`", but `colabfold_batch` has no `--cpu` argument at v1.6.3 and the text is imported but not used.
- Speed (README): `--use-fast-kernels` is "about 2.5x faster and with slightly lower memory"; the first run per sequence length or MSA depth compiles the model, which "can take minutes"; `JAX_COMPILATION_CACHE_DIR` keeps compiled models between runs on the same machine.

### Outbound calls, and how to keep sequences on the machine (the decided case, re-read at v1.6.3)

1. **The public MSA server.** README, "Generating MSAs for small scale local structure/complex predictions using the MSA server": "When you pass a FASTA or CSV file containing your sequences to `colabfold_batch` it will automatically query the public MSA server to generate MSAs." This holds in the code at v1.6.3.
   - Which server: `DEFAULT_API_SERVER = "https://api.colabfold.com"` in `colabfold/utils.py`, the default of `colabfold_batch --host-url`, whose help says: "By default, the free public MSA server hosted by the ColabFold team is queried."
   - What is sent (`run_mmseqs2` in `colabfold/colabfold.py`): an HTTP POST to `{host_url}/ticket/msa` (or `ticket/pair` for the paired MSA of a complex) with two form fields, `q` = the unique query sequences as FASTA with numeric headers starting at 101 (job names are not sent), and `mode` (`env`, `all`, `env-nofilter`, `nofilter`, or `pairgreedy` / `paircomplete` with `-env`). Then GET `{host_url}/ticket/{ID}` to poll and GET `{host_url}/result/download/{ID}` for a `.tar.gz` of A3M files. With templates, GET `{host_url}/template/{ids}` with up to 20 PDB ids. Every request carries the header `User-Agent: colabfold/<version>` (plus the git commit when installed from git).
   - When: `get_queries` in `colabfold/input.py` reads FASTA (`.fasta`, `.faa`, `.fa`), CSV/TSV, A3M, PDB/CIF or a folder of them. Only A3M input (an `.a3m` file, A3M files in a folder, or a CSV with an `a3mpath` column) carries its own MSA. For every other query `colabfold_batch` calls the server unless `--msa-mode single_sequence` is set ("Databases to use to create the MSA: UniRef30+Environmental (default), UniRef30 only or None. Using an A3M file as input overwrites this option."). `--msa-only` and `--af3-json` from FASTA query the server too.
   - Templates: `--templates` "Query PDB templates from the MSA server" and warns: "This can result in the MSA server being queried with A3M input." In the code, A3M input with `--templates` and no local templates calls the server with the sequences for templates. Local templates avoid it: `--custom-template-path <folder of PDB files>` ("No templates will be queried from the MSA server"), or `--pdb-hit-file <hits.m8>` from `colabfold_search` together with `--local-pdb-path <local PDB mmCIF mirror>`, which copies the hit structures into `<results>/templates` and uses them as custom templates.
   - Terms printed when the default server is used (`ACCEPT_DEFAULT_TERMS`): it is "a limited shared resource only capable of processing a few thousand MSAs per day. Please submit jobs only from a single IP address." README FAQ: "Please do not use multiple computers to query the server."
   - The way around, as the README gives it ("Generating MSAs for large scale structure/complex predictions"): create the databases on "a disk with sufficient storage (940GB (!))", which "will take a couple of hours": `MMSEQS_NO_INDEX=1 ./setup_databases.sh /path/to/db_folder`; then `colabfold_search --mmseqs /path/to/bin/mmseqs input_sequences.fasta /path/to/db_folder msas` ("This needs a lot of CPU") and `colabfold_batch msas predictions` ("This needs a GPU"). "In any case the batch searches will require a machine with about 128GB RAM or, if the databases are to be kept permamently in RAM, with over 1TB RAM." For MSAs identical to the server's, use MMseqs2 Release 18. `colabfold_search` makes no network call (it runs the local `mmseqs` binary); `colabfold_batch` on its A3M output does not call the server as long as templates are off or local.
   - A second way around: run your own server (`MsaServer/`, below) and pass `--host-url`; the sequences then go only to that server.
2. **Model weights.** On the first prediction `colabfold_batch` calls `download_alphafold_params` (`colabfold/download.py`), which fetches AlphaFold2 parameters from `storage.googleapis.com` (`alphafold_params_2021-07-14.tar` for monomers, `alphafold_params_colab_2022-12-06.tar` for `alphafold2_multimer_v3`, older multimer tars, or five DeepFold files from `colabfold.steineggerlab.workers.dev`) into the user cache folder (`appdirs.user_cache_dir`). It sends no sequence. It is skipped when the success marker file is already in `<data>/params`; `--data` points at that folder.
3. **Database setup downloads** (`setup_databases.sh`): from `https://opendata.mmseqs.org/colabfold/`, and PDB mmCIF files by rsync from `rsync.wwpdb.org::ftp` on port 33444, unless a file `SKIP_TEMPLATES` is in the database folder. Downloads only; no query data leaves.
4. **Notebooks** run on Google Colab: the sequence goes to Google's runtime, and most notebooks call the public MSA server (below). The structure viewer loads `3Dmol.js` from `3dmol.org` (`colabfold/pdb.py`, notebooks only).
5. No other network call or telemetry was found: a search for URLs and `requests` across `colabfold/` found only the server client, the weight downloader and the viewer script.

## Parts

### Command: colabfold_batch (`colabfold/batch.py`, `main`)

- Predicts structures with AlphaFold2 (monomer `alphafold2_ptm`, multimer v1 to v3, `deepfold_v1`), ranks models, optionally relaxes them with Amber (`--amber`, `--num-relax`, `--use-gpu-relax`), and writes PDB, JSON scores and plots. Input "One of: 1) directory with FASTA/A3M files, 2) CSV/TSV file, 3) FASTA file or 4) A3M file." (PDB/CIF files are also accepted, for `--initial-guess`). 57 `add_argument` calls, grouped as MSA, prediction, relaxation, output, advanced and AlphaFold3 arguments.
- MSA: `--msa-mode` default `mmseqs2_uniref_env`; choices `mmseqs2_uniref_env`, `mmseqs2_uniref_env_envpair`, `mmseqs2_uniref`, `single_sequence`. `--pair-mode` and `--pair-strategy` for complexes. `--host-url` picks the server.
- Speed: `--use-fast-kernels` (alias `--use-pallas`), `--kernel-backend` (`auto`, `pallas`, `cuda_legacy`), `--compile-mode` (`fast`, `tuned`, `full`), `--recompile-padding`, `--sort-queries-by`.
- `--af3-json` writes AlphaFold3 input JSON instead of predicting.
- Needs: the installed package with JAX; an NVIDIA GPU for the CUDA path; the weight download on first run; the public MSA server unless the input is A3M or `--msa-mode single_sequence` (see above).

### Command: colabfold_search (`colabfold/mmseqs/search.py`, `main`)

- Builds MSAs locally: runs the `mmseqs` binary (subprocess) on a query FASTA against the databases from `setup_databases.sh` and writes one A3M per query. Arguments: `query`, `dbbase` ("The path to the database and indices you downloaded and created with setup_databases.sh"), `base` (output).
- Defaults: `--db1 uniref30_2302_db`, `--db3 colabfold_envdb_202108_db`, `--use-env 1`, `--use-templates 0` with `--db2` empty, `--use-env-pairing 0` with `--db4 spire_ctg10_2401_db` (`setup_databases.sh` does not download that database; `MsaServer/config.json` marks it "not used in public MSA server"), `--threads 64`, `--db-load-mode 0`, `--prefilter-mode 0` ("0: k-mer (high-mem), 1: ungapped (high-cpu), 2: exhaustive (no prefilter, very slow)"), `--gpu 0`, `--gpu-server 0`, `--af3-json`, `--af3-msa-as-path`. Template search needs `--use-templates 1` and a `--db2`; the README does not document that route (not checked further).
- GPU search: databases built with `GPU=1 ./setup_databases.sh`, then `--gpu 1`; optionally `mmseqs gpuserver` keeps databases in GPU memory and `--gpu-server 1 --db-load-mode 2`. Needs an MMseqs2 build with GPU support (the setup script: "update to at least release 16").
- Needs: `mmseqs` in `PATH` or `--mmseqs`; the 940GB databases; "about 128GB RAM" for batch searches; many CPU cores. No network.

### Script: setup_databases.sh

- Downloads and builds the local search databases in the folder given as its first argument: `uniref30_2302` and `colabfold_envdb_202108` (prebuilt CPU and GPU databases by default, `FAST_PREBUILT_DATABASES=1`), `uniref30_2302_newtaxonomy`, `pdb100_230517.fasta.gz`, `pdb100_foldseek_230517.tar.gz`, all from `https://opendata.mmseqs.org/colabfold/`; then PDB mmCIF by rsync (arguments two and three choose the server and port; a fourth argument takes the first copy from an AWS S3 snapshot). Builds MMseqs2 indexes unless `MMSEQS_NO_INDEX=1`.
- Switches: `MMSEQS_NO_INDEX`, `GPU=1`, `DOWNLOADS_ONLY`, `DEBUG_MINI_DB=1` (a small Swiss-Prot test database), a `SKIP_TEMPLATES` file in the folder (no PDB templates). It can be rerun: marker files (`DOWNLOADS_READY`, `UNIREF30_READY` and others) skip finished steps.
- Needs: `mmseqs` in `PATH`; `aria2c`, `curl` or `wget`; `rsync`; 940GB of disk; network for the downloads.

### Command: colabfold_split_msas (`colabfold/mmseqs/split_msas.py`)

- "Take an a3m database from the colabdb search and turn it into a folder of a3m files": splits `final.a3m` in a `colabfold_search` folder into one A3M file per MSA. Reads files only. It accepts `--mmseqs` but does not use it.
- Needs: the package.

### Module: merge_and_split_msas (`colabfold/mmseqs/merge_and_split_msas.py`)

- Not a registered command; runs as a module. Merges the two search results (`uniref.a3m` and `bfd.mgnify30.metaeuk30.smag30.a3m`) with `mmseqs mergedbs`, then splits them into one A3M file per MSA.
- Needs: the package and `mmseqs`.

### Command: colabfold_relax (`colabfold/relax.py`)

- Amber relaxation of existing structures through AlphaFold's relax module. Input "Directory with PDB files or a single PDB file"; `--max-iterations`, `--tolerance`, `--stiffness`, `--max-outer-iterations`; `--use-gpu` to "run amber on GPU instead of CPU".
- Needs: the package with the `openmm` extra.

### Module: colabfold.download (`colabfold/download.py`)

- `python -m colabfold.download [model_type]` downloads AlphaFold2 weights ahead of time; without an argument it fetches `alphafold2_multimer_v3` and `AlphaFold2-ptm`. URLs and target folder as under "Model weights" above.
- Needs: the package and network once; after that runs make no weight download.

### Folder: MsaServer/ (self-hosted MSA server)

- `MsaServer/README.md`: "Setting up your local ColabFold API server" on "a Linux (or macOS for testing) machine".
- `setup-and-start-local.sh`: checks for `curl`, `aria2c`, `rsync` and `aws`; downloads pinned `mmseqs` and `mmseqs-server` binaries from `https://mmseqs.com/archive/<commit>/`; runs `../setup_databases.sh` into `MsaServer/databases`; starts `mmseqs-server -local -config config.json`. It exits until one PDB rsync mirror (RCSB, PDBe or PDBj) is uncommented. `GPU=1` is Linux only.
- `config.json`: binds localhost port 8080 under the prefix `/api/`; `dbmanagment` false ("No additional authentication provided"); optional HTTP Basic Auth and rate limiting, commented out; CORS on.
- `systemd-example-mmseqs-server.service` and `restart-systemd.sh` run it as a service.
- Memory: "the two default databases (UniRef30+ColabFoldDB) require currently 768GB-1024GB RAM to stay resident in RAM" for answers within seconds in CPU mode.
- Use: `colabfold_batch --host-url <server>`; in notebooks, `host_url=` in the `run()` call.
- Needs: a Linux server, the databases, the RAM above for fast answers; sequences go only to that server.

### Dockerfile

- Builds from `debian:trixie-slim`; adds MMseqs2 GPU binaries from `https://mmseqs.com/archive/8cc5ce367b5638c4306c2d7cfc652dd099a4643f/`; installs `.[alphafold,openmm]` with `jax[cuda12]<0.12` and `openmm[cuda12]` (build argument `CUDA=cuda12`). A volume `cache` holds the weights (`XDG_CACHE_HOME=/cache`). CI publishes `ghcr.io/sokrypton/colabfold:<version>-cuda12` for `linux/amd64` and `-cuda13` for `linux/amd64,linux/arm64`.
- Needs: Docker and an NVIDIA GPU with CUDA; the image still downloads weights and calls the MSA server unless told otherwise.

### Script: colabfold_search.sh

- Disabled upstream: its second line prints "Do not use this script. Use the python colabfold_search instead" and the script exits. The rest is the old shell version of the search.

### Utility: utils/convert_deepfold_weights.py

- Converts a DeepFold weights `.npz` into AlphaFold parameter names: `python utils/convert_deepfold_weights.py <in> <out>`. Loads the input with `allow_pickle=True`, so only for trusted files. Needs numpy.

### Notebook: utils/plot_scores.ipynb

- Title "Using scores.json for plotting". Not read beyond the title.

### Notebooks on Google Colab (README table)

Each runs on Google Colab, installs its packages into the Colab runtime, and ends with a download of the results. Needs for all: a Google account and Colab; the sequence goes to Google's runtime.

- `AlphaFold2.ipynb` (AlphaFold2_mmseqs2): monomers and complexes, MMseqs2 MSAs, templates. `msa_mode` `mmseqs2_uniref_env`, `mmseqs2_uniref`, `single_sequence` or `custom` (upload an A3M). The MMseqs2 modes call the public MSA server.
- `batch/AlphaFold2_batch.ipynb`: the same for a folder of inputs; mounts Google Drive (`drive.mount('/content/drive')`). MMseqs2 modes call the public MSA server.
- `AlphaFold3_of3.ipynb` ("AlphaFold 3 (OpenFold3)"): protein, RNA, DNA and small-molecule structures with the AlphaFold 3 code. `msa_mode` `mmseqs2_server` (passes `--use_msa_server`) or `single_sequence`. Weights: its text says "By default the notebook uses the open **OpenFold3** weights (Apache-2.0, no restrictions)" and that official AlphaFold 3 parameters "are subject to the [AF3 weights terms of use]". But at v1.6.3 the install cell sets `use_af3_weights = True`, so as shipped it downloads the official AlphaFold 3 weights from `storage.googleapis.com/alphafold3/`. Licence cell: "AlphaFold 3 source code and OpenFold3 weights are both licensed under [Apache 2.0]".
- `ESMFold.ipynb`: single-sequence prediction with ESMFold, no MSA; installs forks of `openfold` and `esm`. Suggests the ESMFold API at `esmatlas.com` "For short monomeric proteins under the length 400", which sends the sequence to that API.
- `RoseTTAFold2.ipynb`: clones RoseTTAFold2 and uses ColabFold's `run_mmseqs2`, so the public MSA server.
- `Boltz1.ipynb`: installs `boltz`; makes the MSA with `colabfold_batch ... --msa-only` (public MSA server), then predicts with Boltz.
- `BioEmu.ipynb`: installs `bioemu` and samples structures (`bioemu-v1.0` or `bioemu-v1.1`), then runs `foldseek`. How the `bioemu` package builds its MSA was not checked.
- `RoseTTAFold.ipynb` (top level, not in the README table): older RoseTTAFold with `cf.run_mmseqs2` (public MSA server); downloads weights from `files.ipd.uw.edu`.
- `beta/relax_amber.ipynb` ("relax input structure"): Amber relaxation of an uploaded structure; no MSA.
- `beta/omegafold.ipynb`: OmegaFold, single-sequence; clones a fork of OmegaFold; no MSA.

### Other notebooks: beta/ and verbose/ (titles only)

- `beta/`: `AlphaFold2_advanced.ipynb`, `AlphaFold2_advanced_beta.ipynb`, `AlphaFold2_advanced_old.ipynb`, `AlphaFold2_complexes.ipynb`, `AlphaFold_wJackhmmer.ipynb`, `Alphafold_single.ipynb`, `ESMFold.ipynb`, `ESMFold_advanced.ipynb`, `ESMFold_api.ipynb`, `RoseTTAFold.ipynb`, `alphafold_output_at_each_recycle.ipynb`, `convert_256_to_384_rep.ipynb`, `omegafold_hacks.ipynb`, with helper files (`colabfold.py`, `colabfold_alphafold.py`, `pairmsa.py`, patches, `RoseTTAFold_install.sh`, `RoseTTAFold_run.sh`). The README calls this group "BETA (in development) notebooks" and links only `relax_amber` and `omegafold` from it; retired notebooks are listed on the project wiki.
- `verbose/`: `alphafold_noTemplates_noMD.ipynb`, `alphafold_noTemplates_yesMD.ipynb`.
- Read by title only.

## Reasons for any rejection or reference status

- `colabfold_search.sh`: rejected because upstream disables it (it prints "Do not use this script. Use the python colabfold_search instead" and exits); `colabfold_search` does the same job.
- No other part is rejected. No part is in use or tried: there is no record of use.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 69 model calls on opus, $5.03 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
