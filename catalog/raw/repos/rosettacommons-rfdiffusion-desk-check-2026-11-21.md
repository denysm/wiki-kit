---
title: "Desk check: RosettaCommons/RFdiffusion v1.1.0"
source: https://github.com/RosettaCommons/RFdiffusion/tree/v1.1.0
type: repos
authors: ["Rosetta Commons", "Joseph Watson", "David Juergens", "Nathaniel Bennett", "Brian Trippe", "Jason Yim"]
source_date: 2023-04-03
ingested: 2026-11-21
repo: RosettaCommons/RFdiffusion
kind: app
version: "1.1.0"
licence: BSD
tags: [catalog, desk-check, kind-app, rfdiffusion, protein-design, diffusion, science, protein-engineering-and-design]
summary: "Every part of RFdiffusion v1.1.0 read from a read-only clone: the one inference command, the two hydra configs, the thirteen example design modes (unconditional, motif scaffolding, inpaint_seq, enzyme active site, partial diffusion with and without sequence, binder design, fold-conditioned binder and TIM barrel, cyclic, dihedral and tetrahedral oligomers, symmetric motif scaffolding), the secondary-structure helper, the importable package with its twelve guiding potentials and symmetry generator, the bundled NVIDIA SE(3)-Transformer with its own licence, the seven checkpoints that are not in the repository, and the bundled example inputs. Licence read from the file (BSD) against what GitHub reports (NOASSERTION); freshness from the GitHub API; no telemetry or outbound call found in the inference code."
---

# Desk check: RosettaCommons/RFdiffusion v1.1.0

Read from a shallow clone of tag `v1.1.0` (commit `9273ef67335acaf91df0150473a274759229cdf6`, committed 2023-04-03), at `$EXTERNAL/RFdiffusion`. The clone was not modified; nothing was installed, downloaded or run. Checked 2026-11-21. Version read by this desk check: 1.1.0.

## Repository facts

- `LICENSE` (30 lines) begins "BSD License" and "Copyright (c) 2023 University of Washington. Developed at the Institute for Protein Design by Joseph Watson, David Juergens, Nathaniel Bennett, Brian Trippe and Jason Yim". It carries the three usual BSD conditions: source redistributions retain the notice, binary redistributions reproduce it "in the documentation and/or other materials provided with the distribution", and "Neither the name of the University of Washington nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission." The software is provided "AS IS" with the standard disclaimer of warranties and liability. It is the three-clause form of the BSD licence; the file itself carries no SPDX identifier, which is why GitHub reports it as NOASSERTION.
- README, last line of the body: "RFdiffusion is released under an open source BSD License (see LICENSE file). It is free for both non-profit and for-profit use."
- Model weights are **not** in the repository. The README's installation section lists seven checkpoint files to fetch by hand with `wget` from a public file server at the Institute for Protein Design, plus one optional file: `Base_ckpt.pt`, `Complex_base_ckpt.pt`, `Complex_Fold_base_ckpt.pt`, `InpaintSeq_ckpt.pt`, `InpaintSeq_Fold_ckpt.pt`, `ActiveSite_ckpt.pt`, `Base_epoch8_ckpt.pt`, and under "Optional:" `Complex_beta_ckpt.pt`. The clone states no separate licence, terms of use or citation condition for these checkpoint files: the only licence texts in the clone are `LICENSE` (BSD, above) and `env/SE3Transformer/LICENSE` with `env/SE3Transformer/NOTICE` (below). The README gives no file sizes and no GPU memory figure for them.
- `setup.py` declares `name='rfdiffusion'`, `version='1.0.0'` (the file was not bumped for the v1.1.0 tag), `description='RFdiffusion is an open source method for protein structure generation.'`, `author='Rosetta Commons'`, `scripts=["scripts/run_inference.py"]`, `packages=["rfdiffusion"]`, `install_requires=['torch', 'se3-transformer']`.
- Top-level folders that hold parts: `scripts/` (one command), `config/inference/` (two configs), `examples/` (13 design-mode scripts and their input data), `helper_scripts/` (one helper and a sample pdb), `rfdiffusion/` (the importable package), `env/` (the conda environment file and a bundled copy of NVIDIA's SE(3)-Transformer). `img/` holds the README figures.
- The README's "Things Diffusion can do" list: "Motif Scaffolding", "Unconditional protein generation", "Symmetric unconditional generation (cyclic, dihedral and tetrahedral symmetries currently implemented, more coming!)", "Symmetric motif scaffolding", "Binder design", "Design diversification ("partial diffusion", sampling around a design)".
- Bundled third party: `env/SE3Transformer/LICENSE` is "Copyright 2021 NVIDIA CORPORATION & AFFILIATES" with MIT-style permission text, and `env/SE3Transformer/NOTICE` says the repository "includes software from https://github.com/FabianFuchsML/se3-transformer-public licensed under the MIT License" and from "https://github.com/lucidrains/se3-transformer-pytorch licensed under the MIT License". Its Python files carry `SPDX-License-Identifier: MIT`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/RosettaCommons/RFdiffusion`: `pushed_at` 2026-10-28T16:51:54Z; default branch `main`; not archived; description "Code for running RFdiffusion"; 3144 stars.
- Licence as GitHub reports it: `"spdx_id":"NOASSERTION"`, name "Other" — GitHub does not detect the BSD text. The licence file itself says "BSD License" (above), so the card records BSD.
- `gh api repos/RosettaCommons/RFdiffusion/releases/latest`: tag `v1.1.0`, name "v1.1.0 RFdiffusion Python Module", published 2023-04-03T21:36:55Z. The repository has two releases in all: `v1.1.0` and `v1.0.0` (published 2023-03-31T22:53:23Z).
- So the clone is at the latest release, but `main` has been pushed since: the last push is 2026-10-28 and the last release 2023-04-03, so commits on `main` are not covered by this desk check.
- Release notes of `v1.1.0`: "RFdiffusion has been refactored into a python module. This makes it easier to run the inference script from any working directory, and makes it easier for a user to import RFdiffusion into their own python scripts and use it as a library." and "The `run_inference.py` script is now within the `scripts/` directory, so submission scripts will need to point to this new location."

## How to run here

- **Clone**: `git clone --depth 1 --branch v1.1.0 https://github.com/RosettaCommons/RFdiffusion $EXTERNAL/RFdiffusion`, read-only. Never edit the clone.
- **Read first**: `README.md` (480 lines), then `config/inference/base.yaml` for every default the command accepts.
- **Telemetry and outbound calls**: none found in the inference path. A search for `https://`, `requests.`, `urllib`, `wget`, `curl `, `telemetry`, `wandb` and `boto3` across `*.py`, `*.yaml`, `*.yml` and `*.sh` outside `env/` returned only documentation URLs in comments and the project URL in `setup.py`. The one `wandb` import in the clone is in the bundled NVIDIA training code (`env/SE3Transformer/se3_transformer/runtime/loggers.py`), which inference does not use. The only network step is the manual `wget` of the checkpoints described in the README. Nothing has to be switched off; no input structure leaves the machine.
- **Writes into the clone, to be redirected**: with default settings the command writes inside the repository. `rfdiffusion/inference/model_runners.py` resolves the weights folder to `f"{SCRIPT_DIR}/../../models"` and the diffusion-schedule cache to `f"{SCRIPT_DIR}/../../schedules"`, where `SCRIPT_DIR` is the folder of that file, and it creates the schedules folder on first run (`if not os.path.exists(schedule_directory): os.mkdir(schedule_directory)`). The README notes the first run is slow: "the first time you run RFdiffusion, it will take a while 'Calculating IGSO3'. Once it has done this, it'll be cached for future reference though!" To keep the clone untouched, pass `inference.model_directory_path`, `inference.schedule_directory_path` and `inference.output_prefix` pointing outside it.
- **Do not install**: the conda environment and the package. The README's recipe is `conda env create -f env/SE3nv.yml`, then in that environment `pip install --no-cache-dir -r requirements.txt` and `python setup.py install` inside `env/SE3Transformer`, then `pip install -e .` at the repository root. `env/SE3nv.yml` pins `python=3.9`, `pytorch=1.9`, `torchaudio`, `torchvision`, `cudatoolkit=11.1`, `dgl-cuda11.1`, `icecream`, and by pip `hydra-core` and `pyrsistent` — an NVIDIA CUDA machine with conda. A real installation, and any checkpoint download, waits for the user's yes.
- **What it needs to run at all**: that conda environment, one or more of the seven checkpoints downloaded by hand, and a machine the environment can be built on. `rfdiffusion/inference/model_runners.py` selects the device as `torch.device('cuda')` when `torch.cuda.is_available()` and `torch.device('cpu')` otherwise, so there is a CPU fallback, but the pinned environment is CUDA-only and the repository names no CPU-only environment and no GPU memory figure. The README states the scaling: "RFdiffusion scales in runtime as O(N^2) where N is the number of residues in your system."
- **Nothing was run** for this desk check: no environment was created, no checkpoint was downloaded, no design was generated.

## Parts

### Command: `scripts/run_inference.py`

- The only command in the repository (185 lines). Hydra entry point: `@hydra.main(version_base=None, config_path="../config/inference", config_name="base")`; "There are many ways to run it, governed by hydra configs." Any config key can be overridden on the command line, and the README warns that defaults are drawn from the checkpoint, so "the default values in `config/inference/base.yml` might not match the actual values used during inference, with a specific checkpoint".
- It builds a sampler through `rfdiffusion.inference.utils.sampler_selector`, which returns `ScaffoldedSampler` when `scaffoldguided.scaffoldguided` is set, and otherwise `Sampler` or `SelfConditioning` according to `inference.model_runner` (default `SelfConditioning`).
- It loops over `inference.num_designs` designs and, per design, over the reverse-diffusion timesteps down to `inference.final_step`; `inference.cautious` (default True) skips a design whose `.pdb` already exists.
- Output per design: `<output_prefix>_<i>.pdb` with every designed residue written as glycine and no sidechains; `<output_prefix>_<i>.trb`, a pickle with the full config, per-step pLDDT, the device name, the run time and the contig mapping (`con_ref_pdb_idx`/`con_hal_pdb_idx`, `con_ref_idx0`/`con_hal_idx0`, `inpaint_seq`); and, when `inference.write_trajectory` is on (the default), two multi-model trajectory pdbs per design in a `traj/` folder (`_Xt-1_traj.pdb` and `_pX0_traj.pdb`), which the README says are "ordered in reverse".
- Checkpoint selection, when `inference.ckpt_override_path` is not set (`model_runners.py`): `contigmap.inpaint_seq` or `contigmap.provide_seq` → `InpaintSeq_Fold_ckpt.pt` with scaffold guidance, else `InpaintSeq_ckpt.pt`; `ppi.hotspot_res` without scaffold guidance → `Complex_base_ckpt.pt`; `scaffoldguided.scaffoldguided` → `Complex_Fold_base_ckpt.pt`; otherwise `Base_ckpt.pt`. With an override it prints "WARNING: You're overriding the checkpoint path from the defaults."
- Needs: the conda environment, the matching checkpoint, and a CUDA GPU for any realistic run.

### Config: `config/inference/base.yaml`

- The default config, read by the command unless `--config-name` names another. Groups: `inference`, `contigmap`, `model`, `diffuser`, `denoiser`, `ppi`, `potentials`, `contig_settings`, `preprocess`, `logging`, `scaffoldguided`.
- Defaults that matter at inference: `num_designs: 10`, `write_trajectory: True`, `cautious: True`, `final_step: 1`, `model_runner: SelfConditioning`, `diffuser.T: 50`, `denoiser.noise_scale_ca: 1` and `noise_scale_frame: 1`, `potentials.guide_scale: 10`, `potentials.guide_decay: constant`, `scaffoldguided.mask_loops: True`.
- README on the step count: "RFdiffusion was originally trained with 200 discrete timesteps", "In many cases, running with as few as approximately 20 steps provides outputs of equivalent *in silico* quality to running with 200 steps (providing a 10X speedup). The default is now set to 50 steps."
- README on what is worth changing: `inference.final_step`, `denoiser.noise_scale_ca` and `denoiser.noise_scale_frame`; "Generally, don't change the `model`, `preprocess` or `diffuser` configs."
- Needs: nothing to read; it is a 130-line YAML file.

### Config: `config/inference/symmetry.yaml`

- Selected with `--config-name symmetry`; it inherits `base` through `defaults: - base` and "puts diffusion in `symmetry-mode`". Defaults `inference.symmetry: c2`, `inference.model_only_neighbors: False`, `contigmap.contigs: ['100']`.
- Its comments list the available symmetries: "Cyclic symmetry (C_n) # call as c5", "Dihedral symmetry (D_n) # call as d5", "Tetrahedral symmetry # call as tetrahedral", "Octahedral symmetry # call as octahedral", "Icosahedral symmetry # call as icosahedral". The README's own list names cyclic, dihedral and tetrahedral as "currently implemented".
- The contig length is the total length of the oligomer and "must be divisible by *n* chains".
- Needs: nothing to read.

### Design mode: `examples/design_unconditional.sh`

- Unconditional monomer generation: `'contigmap.contigs=[100-200]' inference.num_designs=10`, length sampled per design. The README's minimal form is `./scripts/run_inference.py 'contigmap.contigs=[150-150]' inference.output_prefix=test_outputs/test inference.num_designs=10`.
- Checkpoint: `Base_ckpt.pt` by the selection rule. Needs: environment, that checkpoint, GPU.

### Design mode: `examples/design_motifscaffolding.sh`

- Scaffolds a motif from an input pdb: `inference.input_pdb=input_pdbs/5TPN.pdb 'contigmap.contigs=[10-40/A163-181/10-40]' inference.num_designs=10`, that is 10-40 sampled residues, then residues 163-181 of chain A, then 10-40 residues. In the contig string a letter prefix means motif residues from that chain, a bare range means protein to be built, and `/0 ` with a space is a chain break that adds a 200-residue index jump.
- Checkpoint: `Base_ckpt.pt`. Needs: environment, checkpoint, GPU, an input pdb (`examples/input_pdbs/5TPN.pdb` is bundled).

### Design mode: `examples/design_motifscaffolding_inpaintseq.sh`

- The same run plus `'contigmap.inpaint_seq=[A163-168/A170-171/A179]'`, which masks the identity of those motif residues so the model can reason over them and pack better.
- Checkpoint: `InpaintSeq_ckpt.pt`, chosen automatically ("this is automatically handled by the inference script (you don't need to do anything)"). Needs: environment, that checkpoint, GPU.

### Design mode: `examples/design_enzyme.sh`

- Scaffolds three single active-site residues of a retroaldolase (`input_pdbs/5an7.pdb`, contig `[10-100/A1083-1083/10-100/A1051-1051/10-100/A1180-1180/10-100]`) and models the substrate with the `substrate_contacts` potential (`potentials.guide_scale=1`, `potentials.substrate=LLK`).
- It overrides the checkpoint with `inference.ckpt_override_path=../models/ActiveSite_ckpt.pt`, the model "fine-tuned on examples similar to these tasks, allowing it to hold smaller motifs better in place". README: "If your input functional motif is very small, we reccomend using this model".
- Needs: environment, `ActiveSite_ckpt.pt`, GPU.

### Design mode: `examples/design_partialdiffusion.sh`

- Diversification around a fold: noise and denoise an input structure for part of the trajectory, `inference.input_pdb=input_pdbs/2KL8.pdb 'contigmap.contigs=[79-79]' inference.num_designs=10 diffuser.partial_T=10`. The contig must sum to the length of the input pdb.
- README: "More noise == more diversity"; with the default `diffuser.T=50`, "the equivalent of 80 noising steps is `diffuser.partial_T=20`".
- Checkpoint: `Base_ckpt.pt`. Needs: environment, checkpoint, GPU, an input structure.

### Design mode: `examples/design_partialdiffusion_withseq.sh`

- Partial diffusion that keeps part of the sequence: a 172-residue groove scaffold and a 34-residue helical peptide, `'contigmap.contigs=["172-172/0 34-34"]' diffuser.partial_T=10 'contigmap.provide_seq=[172-205]'`; `provide_seq` is zero-indexed and inclusive.
- Checkpoint: the `provide_seq` branch, `InpaintSeq_ckpt.pt`, chosen automatically; `provide_seq` asserts that `diffuser.partial_T` is set. Needs: environment, that checkpoint, GPU.

### Design mode: `examples/design_ppi.sh`

- Binder design against a target chain: `inference.input_pdb=input_pdbs/insulin_target.pdb 'contigmap.contigs=[A1-150/0 70-100]' 'ppi.hotspot_res=[A59,A83,A91]' inference.num_designs=10 denoiser.noise_scale_ca=0 denoiser.noise_scale_frame=0`.
- Hotspots steer the interface; the README recommends "between 3-6 hotspots" and warns the model "is expecting to have to make more contacts than you specify". It also advises truncating big targets, leaving "~10A of target protein on each side of your intended target site", and notes that binders come out as a poly-glycine backbone: "RFdiffusion is a backbone-generation model and does not generate sequence for the designed region, therefore, another method must be used to assign a sequence to the binders." The paper's scale was "~10,000 RFdiffusion binder backbones for each target", two sequences per backbone with ProteinMPNN, screened with AlphaFold2, filtering "at pae_interaction < 10".
- A "beta" model for more topological diversity is available through `inference.ckpt_override_path=models/Complex_beta_ckpt.pt`: "Try this at your own risk".
- Checkpoint: `Complex_base_ckpt.pt` by the hotspot rule. Needs: environment, that checkpoint, GPU, a target structure.

### Design mode: `examples/design_ppi_scaffolded.sh`

- Fold-conditioned binder design: `scaffoldguided.scaffoldguided=True`, target pdb plus its secondary structure and block adjacency (`scaffoldguided.target_ss=target_folds/insulin_target_ss.pt scaffoldguided.target_adj=target_folds/insulin_target_adj.pt`), a folder of scaffold files (`scaffoldguided.scaffold_dir=./ppi_scaffolds/`), hotspots, and noise scales 0.
- The scaffold folder comes from the bundled archive, which the README says to untar first: `tar -xvf examples/ppi_scaffolds_subset.tar.gz -C examples/`. For PPI the README recommends `scaffoldguided.mask_loops=False` and lowering noise ("0.5 is probably a good compromise").
- Checkpoint: `Complex_Fold_base_ckpt.pt`. Needs: environment, that checkpoint, GPU, the untarred scaffold set.

### Design mode: `examples/design_timbarrel.sh`

- Fold-conditioned monomer: `scaffoldguided.scaffoldguided=True scaffoldguided.target_pdb=False scaffoldguided.scaffold_dir=tim_barrel_scaffold/ inference.num_designs=200 denoiser.noise_scale_ca=0.5 denoiser.noise_scale_frame=0.5 scaffoldguided.sampled_insertion=0-5 scaffoldguided.sampled_N=0-5 scaffoldguided.sampled_C=0-5`, generating diverse TIM barrels from one starting pdb.
- Checkpoint: `Complex_Fold_base_ckpt.pt` by the scaffold-guided rule. Needs: environment, that checkpoint, GPU, the two bundled `6WVS` scaffold tensors.

### Design mode: `examples/design_cyclic_oligos.sh`

- C6 symmetric oligomer: `--config-name=symmetry inference.symmetry="C6" inference.num_designs=10 'contigmap.contigs=[480-480]'`, 480 residues in all, "so each chain is 80 residues long", with the `olig_contacts` potential (`weight_intra:1,weight_inter:0.1`, `potentials.guide_scale=2.0`, `guide_decay="quadratic"`).
- Checkpoint: `Base_ckpt.pt`. Needs: environment, checkpoint, GPU.

### Design mode: `examples/design_dihedral_oligos.sh`

- D2 symmetric oligomer, the same recipe with `inference.symmetry="D2"` and `'contigmap.contigs=[320-320]'`, "so each chain is 80 residues long".
- Checkpoint: `Base_ckpt.pt`. Needs: environment, checkpoint, GPU.

### Design mode: `examples/design_tetrahedral_oligos.sh`

- Tetrahedral oligomer, `inference.symmetry="tetrahedral"` and `'contigmap.contigs=[1200-1200]'`, "so each chain is 100 residues long". The README's one-line form is `./scripts/run_inference.py --config-name symmetry inference.symmetry=tetrahedral 'contigmap.contigs=[360]' inference.output_prefix=test_sample/tetrahedral inference.num_designs=1`.
- Checkpoint: `Base_ckpt.pt`. The 12 chains make this the largest of the bundled examples. Needs: environment, checkpoint, GPU.

### Design mode: `examples/design_nickel.sh`

- Symmetric motif scaffolding: a C4 oligomer scaffolding four symmetric copies of a nickel-binding motif, `inference.symmetry="C4" inference.num_designs=15 inference.input_pdb=input_pdbs/nickel_symmetric_motif.pdb 'contigmap.contigs=[50/A2-4/50/0 50/A7-9/50/0 50/A12-14/50/0 50/A17-19/50/0]'` with `olig_contacts` (`weight_inter:0.06`) and `inference.ckpt_override_path=../models/Base_epoch8_ckpt.pt`.
- The README requires the input motif to be symmetrised on the canonical axes beforehand (cyclic and dihedral-cyclic about Z, dihedral flip about X), because the code centres motifs at the origin: "Note that the contigs should specify something that is precisely symmetric. Things will break if this is not the case."
- Needs: environment, `Base_epoch8_ckpt.pt`, GPU, a pre-symmetrised input pdb.

### Helper: `helper_scripts/make_secstruc_adj.py`

- 503 lines. `--input_pdb` or `--pdb_dir`, plus a required `--out_dir`; for each pdb it writes `<name>_ss.pt` (secondary structure) and `<name>_adj.pt` (block adjacency), the inputs the fold-conditioned modes take.
- It tries `import pyrosetta` and falls back with "WARNING: pyRosetta not found, will use an approximate SSE calculation", so it runs without PyRosetta at lower fidelity. `helper_scripts/2KL8.pdb` is bundled so the README's example (`./make_secstruc_adj.py --input_pdb ./2KL8.pdb --out_dir /my/dir/for/adj_secstruct`) runs as written.
- Needs: Python with torch and numpy; no GPU; PyRosetta optional. This is the one part that could be run outside the CUDA environment.

### Package: `rfdiffusion/`

- The importable module the v1.1.0 release added, 24 Python files: the RoseTTAFold-derived network (`RoseTTAFoldModel.py`, `Attention_module.py`, `Track_module.py`, `Embeddings.py`, `AuxiliaryPredictor.py`, `SE3_network.py`), the diffusion machinery (`diffusion.py`, `igso3.py`, `diff_util.py`), geometry and chemistry helpers (`chemical.py`, `contigs.py`, `coords6d.py`, `kinematics.py`, `scoring.py`, `util.py`, `util_module.py`, `model_input_logger.py`), `inference/` (`model_runners.py` 957 lines, `utils.py` 1002 lines, `symmetry.py` 236 lines, `sym_rots.npz`) and `potentials/` (`manager.py` 211 lines, `potentials.py` 733 lines).
- Release note: the refactor "makes it easier for a user to import RFdiffusion into their own python scripts and use it as a library."
- Needs: the same environment as the command; importing it pulls in torch, dgl and the SE(3)-Transformer.

### Module: `rfdiffusion/potentials/potentials.py`

- The twelve guiding potentials registered in `implemented_potentials`: `monomer_ROG`, `binder_ROG`, `binder_distance_ReLU`, `binder_any_ReLU`, `dimer_ROG`, `binder_ncontacts`, `dimer_ncontacts`, `interface_ncontacts`, `monomer_contacts`, `olig_intra_contacts`, `olig_contacts`, `substrate_contacts`. Seven of them are listed in `require_binderlen`.
- Selected as strings, for example `potentials.guiding_potentials=[\"type:olig_contacts,weight_intra:1,weight_inter:0.1\"]`, with `potentials.guide_scale` and a decay of `constant`, `linear`, `quadratic` or `cubic`.
- README caution: potentials "can be helpful for motif scaffolding and symmetric oligomer generation. However, they seem to interact weirdly with hotspot residues in PPI", and "it is often good practice to start with *no potentials* as a baseline". A new potential only has to be differentiable.
- Needs: nothing beyond a run of the command that names them.

### Module: `rfdiffusion/inference/symmetry.py`

- `SymGen` builds and applies the symmetry operations: `_init_cyclic`, `_init_dihedral` and `_init_from_symrots_file` for `saved_symmetries = ['tetrahedral', 'octahedral', 'icosahedral']`, read from `rfdiffusion/inference/sym_rots.npz`. `model_only_neighbors` exists "to avoid memory overhead of modeling all subunits".
- Needs: nothing beyond a symmetric run.

### Bundled dependency: `env/SE3Transformer/`

- NVIDIA's SE(3)-Transformer implementation, vendored in the repository and installed into the conda environment by `python setup.py install`. Its own `LICENSE` and `NOTICE` are quoted under Repository facts.
- Only its `LICENSE`, `NOTICE` and file listing were read for this desk check; its code was not. It also contains training and benchmarking scripts and a Dockerfile that belong to NVIDIA's own project, not to RFdiffusion inference.
- Needs: the conda environment; it is the piece that makes the install CUDA-bound.

### Model checkpoints (not in the clone)

- The seven files listed in the README plus the optional `Complex_beta_ckpt.pt`, fetched by hand with `wget` from the public file server named there. Known here only from the README and from the selection rule in `model_runners.py`; none was downloaded, so none was read.
- The README states no separate licence, no size and no GPU memory requirement for them; it does say "there is not *One Model To Rule Them All*" and that the checkpoint itself carries the config it was trained with, so "inference should always, by default, match training".
- Needs: network access to that file server, disk space for seven files, and the decision to download them.

### Bundled example inputs

- `examples/input_pdbs/`: seven structures (`1qys.pdb`, `2KL8.pdb`, `5TPN.pdb`, `5an7.pdb`, `insulin_target.pdb`, `nickel_symmetric_motif.pdb`, `peptide_complex_ideal_helix.pdb`).
- `examples/ppi_scaffolds_subset.tar.gz`: 288K, holding a `ppi_scaffolds/` folder with 1000 `_ss.pt` and 1000 `_adj.pt` files (2001 entries in all), the scaffold set `design_ppi_scaffolded.sh` reads after `tar -xvf`.
- `examples/target_folds/`: `insulin_target_ss.pt` and `insulin_target_adj.pt`. `examples/tim_barrel_scaffold/`: `6WVS_ss.pt` and `6WVS_adj.pt`. `helper_scripts/2KL8.pdb` for the helper's own example.
- Only the folder listings and the archive's table of contents were read; the files themselves were not opened.
- Needs: nothing to read; untarring the scaffold archive writes into the clone unless `-C` points elsewhere.

## Reasons for status

No part is rejected, taken as a method, or held as a reference. Every part above that was read is a candidate: the repository is the reference implementation of a design method this catalog's science section covers, and nothing in it has been run here. The two parts marked as known only from metadata are the model checkpoints (not downloaded) and the bundled NVIDIA SE(3)-Transformer (only its licence and notice read), plus the bundled example inputs (folder listings only).

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 51 model calls on opus, $7.83 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
