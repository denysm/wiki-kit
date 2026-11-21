---
title: "RosettaCommons/RFdiffusion"
category: reference
kind: app
areas: [science]
science_sections: [protein-engineering-and-design]
repo: RosettaCommons/RFdiffusion
version: "1.1.0"
licence: BSD
desk_checked: 2026-11-21
sources:
  - raw/repos/rosettacommons-rfdiffusion-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, kind-app, protein-design, diffusion, structure-generation, binder-design, symmetry, protein-engineering-and-design]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Diffusion model that generates protein backbones: one inference command driven by hydra configs, thirteen worked design modes (unconditional, motif scaffolding, active site, partial diffusion, binder design, fold conditioning, cyclic, dihedral and tetrahedral oligomers, symmetric motif scaffolding), twelve guiding potentials and a secondary-structure helper. BSD per the licence file, which GitHub does not detect. Weights are not in the repository and the environment is CUDA-bound, so nothing here runs on this machine without a decision; every part is a candidate read from a clone at v1.1.0."
---

# RosettaCommons/RFdiffusion

> A protein backbone generator (kind `app`, licence BSD, version `1.1.0` read): one inference command whose hydra config turns it into unconditional generation, motif scaffolding, binder design, partial diffusion, fold-conditioned design or symmetric assembly, plus twelve guiding potentials and a helper that prepares fold inputs. The model weights are not in the repository and the conda environment is pinned to CUDA, so the clone is read here and nothing is installed, downloaded or run.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Generate protein backbones of a given length with nothing else specified | `examples/design_unconditional.sh` | science-protein-engineering-and-design |
| Build a scaffold around a functional motif taken from an existing structure | `examples/design_motifscaffolding.sh` | science-protein-engineering-and-design |
| Scaffold a motif but let the model redesign the motif residues that carry no function | `examples/design_motifscaffolding_inpaintseq.sh` | science-protein-engineering-and-design |
| Scaffold a minimal active site of a few single residues around a substrate | `examples/design_enzyme.sh` | science-protein-engineering-and-design |
| Get diversity around a fold you already have | `examples/design_partialdiffusion.sh` | science-protein-engineering-and-design |
| Diversify a peptide-binder complex while keeping the peptide's sequence | `examples/design_partialdiffusion_withseq.sh` | science-protein-engineering-and-design |
| Design a binder to a chosen site on a target protein | `examples/design_ppi.sh` | science-protein-engineering-and-design |
| Design a binder whose topology comes from a scaffold set rather than from the model | `examples/design_ppi_scaffolded.sh` | science-protein-engineering-and-design |
| Generate a fold specified coarsely, such as a TIM barrel, from one starting structure | `examples/design_timbarrel.sh` | science-protein-engineering-and-design |
| Make a cyclic homo-oligomer | `examples/design_cyclic_oligos.sh` | science-protein-engineering-and-design |
| Make a dihedral homo-oligomer | `examples/design_dihedral_oligos.sh` | science-protein-engineering-and-design |
| Make a tetrahedral assembly | `examples/design_tetrahedral_oligos.sh` | science-protein-engineering-and-design |
| Scaffold a motif symmetrically around a symmetry axis, for example a metal-binding site | `examples/design_nickel.sh` | science-protein-engineering-and-design |
| Prepare the secondary-structure and block-adjacency files a fold-conditioned run needs | `helper_scripts/make_secstruc_adj.py` | science-protein-engineering-and-design |
| Push a trajectory towards a compact or well-contacted structure while it denoises | `rfdiffusion/potentials/potentials.py` | science-protein-engineering-and-design |
| Run any of these modes from one command and understand what it wrote | `scripts/run_inference.py` | science-protein-engineering-and-design |
| Call the sampler from your own Python instead of the command line | `rfdiffusion/` | science-protein-engineering-and-design |
| See every knob a run accepts before changing one | `config/inference/base.yaml` | science-protein-engineering-and-design |

## Run it here

- **Clone**: `git clone --depth 1 --branch v1.1.0 https://github.com/RosettaCommons/RFdiffusion $EXTERNAL/RFdiffusion`, read-only. Never edit the clone.
- **Version**: `1.1.0`, the latest release, published 2023-04-03. Before relying on this card, compare with upstream: `gh api repos/RosettaCommons/RFdiffusion --jq .pushed_at` and `gh api repos/RosettaCommons/RFdiffusion/releases/latest --jq .tag_name`. The last push was 2026-10-28, so `main` carries commits this desk check did not read.
- **Read**: `$EXTERNAL/RFdiffusion/README.md` first, then `config/inference/base.yaml` for every default a run accepts, then the example script of the mode you want.
- **Switch off**: nothing. No telemetry and no outbound call was found in the inference code; the only network step is the manual download of the checkpoints, and no input structure leaves the machine. The one `wandb` import in the clone belongs to the bundled NVIDIA training code, which inference does not use.
- **Keep the clone clean**: with default settings a run writes inside the repository, because the weights folder and the diffusion-schedule cache resolve to the repository root and the cache folder is created on the first run. Pass `inference.model_directory_path`, `inference.schedule_directory_path` and `inference.output_prefix` pointing outside the clone. Untar the bundled scaffold archive outside it too.
- **Do not install**: the conda environment (`env/SE3nv.yml` pins `python=3.9`, `pytorch=1.9`, `cudatoolkit=11.1`, `dgl-cuda11.1`), the bundled NVIDIA SE(3)-Transformer, or the package itself with `pip install -e .`. Do not download the checkpoints. All of that is a CUDA machine and a deliberate decision; it waits for the user's yes.
- **In use**: no part is in use. Nothing in this repository has been run here.

## What's inside

Parts: one command, two hydra configs, thirteen example scripts that are the documented design modes, one helper, the importable package with its potentials and symmetry generator, the bundled NVIDIA SE(3)-Transformer, the checkpoints that live outside the repository, and the bundled example inputs.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `scripts/run_inference.py` | The only command. A hydra entry point whose config decides the mode; loops over `inference.num_designs` and writes, per design, a backbone `.pdb` (every designed residue a glycine, no sidechains), a `.trb` pickle with the config, pLDDT, run time and contig mapping, and two trajectory files in `traj/`. It picks the checkpoint from the inputs: inpainted or provided sequence, hotspots, scaffold guidance or the base model. | candidate | The `SE3nv` conda environment, one downloaded checkpoint, and in practice a CUDA GPU: the code falls back to `torch.device('cpu')` but the pinned environment is CUDA-only and the repository gives no CPU environment and no GPU memory figure. No network at run time; nothing leaves the machine. | Try it on the first real backbone-generation task, starting with the unconditional mode on a short design to measure one trajectory end to end. |
| `config/inference/base.yaml` | The default config and the list of everything a run can change: `inference`, `contigmap`, `model`, `diffuser`, `denoiser`, `ppi`, `potentials`, `preprocess`, `scaffoldguided`. Defaults include 10 designs, trajectory writing on, 50 diffusion steps and noise scales of 1. | candidate | Nothing to read; it is a YAML file in the clone. | Read it before any run and again before changing a parameter; the README limits what is safe to change to the final step and the two noise scales. |
| `config/inference/symmetry.yaml` | Puts the command in symmetry mode (`--config-name symmetry`): inherits the base config and adds the symmetry settings. Its comments name cyclic, dihedral, tetrahedral, octahedral and icosahedral; the README lists cyclic, dihedral and tetrahedral as implemented. The contig length is the whole assembly and must divide by the number of chains. | candidate | Nothing to read; at run time the same as the command. | Read it before the first symmetric run, to pick the symmetry and work out the total length. |
| `examples/design_unconditional.sh` | Unconditional monomers, length sampled per design from a range. The simplest complete command in the repository. | candidate | Environment plus `Base_ckpt.pt`; GPU; no input structure. | Try it first: it is the cheapest way to see whether the environment and a checkpoint work at all. |
| `examples/design_motifscaffolding.sh` | Scaffolds a motif from an input structure: sampled lengths on either side of a chain segment, ten designs. Shows the contig syntax that every other mode reuses. | candidate | Environment plus `Base_ckpt.pt`; GPU; an input structure (one is bundled). | Try it when a functional site has to be carried into a new protein. |
| `examples/design_motifscaffolding_inpaintseq.sh` | The same run with the sequence identity of chosen motif residues masked, so the model can pack against them freely. | candidate | Environment plus `InpaintSeq_ckpt.pt`, chosen automatically; GPU; an input structure. | Try it when only part of a motif is functional and the rest may be redesigned. |
| `examples/design_enzyme.sh` | Scaffolds three single active-site residues of a retroaldolase and keeps a substrate in place with the `substrate_contacts` potential; overrides the checkpoint to the model fine-tuned for very small motifs. | candidate | Environment plus `ActiveSite_ckpt.pt`; GPU; a structure with the site and a substrate name. | Try it on a catalytic site of a few residues, where the base model would let the motif drift. |
| `examples/design_partialdiffusion.sh` | Noises an input structure part of the way and denoises it again, giving variants around one fold. The contig must sum to the length of the input. | candidate | Environment plus `Base_ckpt.pt`; GPU; the structure to diversify. | Try it when a design already works and more of the same shape is wanted; sample several values of the partial step count. |
| `examples/design_partialdiffusion_withseq.sh` | Partial diffusion on a complex while the sequence of one chain is given to the model, so a peptide keeps its identity while its binder is rebuilt. | candidate | Environment plus `InpaintSeq_ckpt.pt`, chosen automatically; GPU; a complex structure. | Try it on peptide-binder work, after the plain partial-diffusion mode has run once. |
| `examples/design_ppi.sh` | Binder design against a target chain with hotspot residues naming the site, noise scales set to 0. The binder comes out as a poly-glycine backbone: a sequence-design step must follow. | candidate | Environment plus `Complex_base_ckpt.pt`; GPU; a target structure, usually truncated around the site. | Try it on the first binder task, at small scale, to see how many designs and hotspots a target needs before any large run. |
| `examples/design_ppi_scaffolded.sh` | Fold-conditioned binder design: the target's secondary structure and block adjacency plus a folder of scaffold files fix the topology of the binder. | candidate | Environment plus `Complex_Fold_base_ckpt.pt`; GPU; the bundled scaffold archive untarred, and fold files for the target. | Try it when plain binder design gives mostly the same helical topology and a different shape is wanted. |
| `examples/design_timbarrel.sh` | Fold-conditioned monomers: 200 TIM barrels from one starting structure, with loops masked and a few residues sampled into loops and termini. | candidate | Environment plus `Complex_Fold_base_ckpt.pt`; GPU; the two bundled scaffold tensors. | Try it when a specific fold is wanted and only one example of that fold exists. |
| `examples/design_cyclic_oligos.sh` | A C6 oligomer of 480 residues in all, with the oligomer-contact potential weighted inside and between chains. | candidate | Environment plus `Base_ckpt.pt`; GPU; symmetry mode, so one run models the whole assembly. | Try it on the first symmetric assembly; it is the template for every cyclic case. |
| `examples/design_dihedral_oligos.sh` | The same recipe with D2 symmetry and 320 residues in all. | candidate | Environment plus `Base_ckpt.pt`; GPU. | Try it when a dihedral assembly is wanted; compare the contact potential weights with the cyclic run. |
| `examples/design_tetrahedral_oligos.sh` | Tetrahedral symmetry, 1200 residues in all — the largest of the bundled examples, and the one that shows how runtime grows with the assembly. | candidate | Environment plus `Base_ckpt.pt`; GPU with room for the whole assembly, since runtime grows as the square of the residue count. | Try it only after a cyclic run has been timed; use it to measure the cost ceiling of symmetric work. |
| `examples/design_nickel.sh` | Symmetric motif scaffolding: a C4 assembly around four symmetric copies of a metal-binding motif, with a different checkpoint found to work better on this task. | candidate | Environment plus `Base_epoch8_ckpt.pt`; GPU; an input motif already symmetrised on the canonical axes, or the run breaks. | Try it when a site must sit on a symmetry axis; prepare the symmetrised input first. |
| `helper_scripts/make_secstruc_adj.py` | Turns one structure or a folder of them into the secondary-structure and block-adjacency tensors the fold-conditioned modes read. Uses PyRosetta when it is importable and an approximate calculation otherwise. | candidate | Python with torch and numpy; no GPU and no checkpoint. The only part that could run outside the CUDA environment. PyRosetta optional, and its absence lowers fidelity. | Try it first of all parts: it is the cheapest to run and it produces the inputs the two fold-conditioned modes need. |
| `rfdiffusion/` | The importable package the v1.1.0 release introduced: the RoseTTAFold-derived network, the diffusion machinery, contigs and geometry helpers, the inference runners and the potentials. It is how the sampler is driven from other Python code. | candidate | The same environment as the command; importing it pulls in torch, dgl and the SE(3)-Transformer. | Read it when a run has to be driven from a script rather than the command line, or when the checkpoint selection has to be understood exactly. |
| `rfdiffusion/potentials/potentials.py` | The twelve guiding potentials that bias each denoising step: radius of gyration for monomers, binders and dimers, contact counts for binders, dimers and interfaces, monomer and oligomer contacts, substrate contacts and two binder-distance potentials. Chosen by name with a weight and a decay. | candidate | Nothing beyond a run that names them; they add gradient work to each step. | Try one on a symmetric or motif run where designs come out loose; the README advises starting with no potential as a baseline and raising the weight slowly. |
| `rfdiffusion/inference/symmetry.py` | Builds and applies the symmetry operations: cyclic and dihedral generated on the fly, tetrahedral, octahedral and icosahedral read from the bundled rotation file. Can model only neighbouring subunits to save memory. | candidate | Nothing beyond a symmetric run. | Read it when a symmetry beyond cyclic and dihedral is wanted, or when a large assembly runs out of GPU memory. |
| `env/SE3Transformer/` | NVIDIA's SE(3)-Transformer implementation, vendored in the repository and installed into the conda environment. It is the piece that binds the install to CUDA. Its own licence is NVIDIA's MIT-style text, and its notice names two further MIT-licensed sources. | listed | The conda environment; only its licence and notice were read here, not its code. | Read it if the environment has to be built on different CUDA versions, or if the licence of a redistributed environment matters. |
| `models/` checkpoints | The weights, which are not in the repository: `Base_ckpt.pt`, `Complex_base_ckpt.pt`, `Complex_Fold_base_ckpt.pt`, `InpaintSeq_ckpt.pt`, `InpaintSeq_Fold_ckpt.pt`, `ActiveSite_ckpt.pt`, `Base_epoch8_ckpt.pt` and the optional `Complex_beta_ckpt.pt`. Each carries the config it was trained with, so the run matches training by default. | listed | A manual download from the public file server named in the README, one file per model, and the disk to hold them; no size and no separate licence are stated in the repository. | Read the README's download block before any run, and settle the terms of the weights with the user: the clone states none, so only the software licence is known. |
| `examples/input_pdbs/`, `examples/ppi_scaffolds_subset.tar.gz`, `examples/target_folds/`, `examples/tim_barrel_scaffold/` | The bundled inputs that make the example scripts runnable as written: seven structures, a scaffold archive holding 1000 secondary-structure and 1000 adjacency files, the insulin target's fold files and the TIM barrel scaffold. | listed | Nothing to read; untarring the scaffold archive writes into the clone unless it is redirected. | Read the folder listing when a fold-conditioned run is planned, to see what exists before generating new fold files. |

## Tried

None yet. No part of this repository has been run here; every row above is a desk-check reading.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

The repository is one command with a well-documented set of design modes, and the card follows that shape: the thirteen example scripts are the parts worth choosing between, and the helper is the only one that would run without a CUDA machine. Two things stand between reading and using it: the weights, which are downloaded by hand and whose terms the repository never states, and the conda environment, which pins CUDA 11.1 and NVIDIA's SE(3)-Transformer. Licence is settled: the file says BSD even though GitHub reports no licence. Revisit when a protein-design task actually needs backbones, when a machine with a CUDA GPU is available, or when the freshness check shows a release after `1.1.0` — the last push is years newer than the last release, so `main` may already differ from what was read.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page
- [[area-science-protein-engineering-and-design|Protein engineering and design]] ([Protein engineering and design](../topics/area-science-protein-engineering-and-design.md)): science section page; the other tools for designing and scoring proteins
- [[dauparas-proteinmpnn|dauparas/ProteinMPNN]] (../references/dauparas-proteinmpnn.md): the sequence-design step these backbones need, named in this repository's own binder-design advice
- [[google-deepmind-alphafold|google-deepmind/alphafold]] (../references/google-deepmind-alphafold.md): the structure prediction used in the paper's pipeline to filter designs

## Sources

- [Desk check: RosettaCommons/RFdiffusion v1.1.0](../../raw/repos/rosettacommons-rfdiffusion-desk-check-2026-11-21.md): every part read from the clone, the licence file against what GitHub reports, freshness through the GitHub API, and what a run would take here.
