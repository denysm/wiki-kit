---
title: "dauparas/ProteinMPNN"
category: reference
kind: app
areas: [science]
science_sections: [protein-engineering-and-design]
repo: dauparas/ProteinMPNN
version: "1.0.1"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/dauparas-proteinmpnn-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, kind-app, protein-design, sequence-design, inverse-folding, protein-engineering-and-design]
summary: "Gives a protein backbone a sequence: one entry script with five modes (design, score only, conditional and unconditional probabilities, CA-only), two weight families shipped inside the repository, and nine helper scripts that write the JSON dictionaries for fixed chains, fixed and tied positions, bias and PSSM. MIT, runs on a CPU, no download and no network. Every part is a candidate read from a clone at v1.0.1."
confidence: high
volatility: hot
verified: 2026-11-21
---

# dauparas/ProteinMPNN

> A sequence designer for protein backbones (kind `app`, licence MIT, version `1.0.1` read): one entry script that reads structures and writes FASTA sequences, with modes for scoring a sequence and for per-position probabilities, seven checkpoints of about 6.6 MB shipped in the repository, and nine helper scripts that express the constraints. It needs no download and no GPU; the clone is read here without creating an environment.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Give a designed or natural backbone a sequence | `protein_mpnn_run.py` | science-protein-engineering-and-design |
| Turn a folder of structures into the input the model reads | `helper_scripts/parse_multiple_chains.py` | science-protein-engineering-and-design |
| Redesign some chains or residues and keep the rest as they are | `helper_scripts/assign_fixed_chains.py`, `helper_scripts/make_fixed_positions_dict.py` | science-protein-engineering-and-design |
| Design a symmetric or homo-oligomeric sequence, or one that fits one partner and not another | `helper_scripts/make_tied_positions_dict.py`, `helper_scripts/make_pos_neg_tied_positions_dict.py` | science-protein-engineering-and-design |
| Steer the composition of a design, as a whole or at single positions | `helper_scripts/make_bias_AA.py`, `helper_scripts/make_bias_per_res_dict.py` | science-protein-engineering-and-design |
| Forbid residue types at given positions, or steer the design with a family profile | `helper_scripts/other_tools/make_omit_AA.py`, `helper_scripts/other_tools/make_pssm_dict.py` | science-protein-engineering-and-design |
| Score how well an existing sequence fits its backbone | `protein_mpnn_run.py --score_only` | science-protein-engineering-and-design |
| Get per-position probabilities for a backbone, alone or given the rest of the sequence | `protein_mpnn_run.py --unconditional_probs_only`, `protein_mpnn_run.py --conditional_probs_only` | science-protein-engineering-and-design |
| Design from a backbone that has only alpha-carbon positions | `protein_mpnn_run.py --ca_only`, `ca_model_weights/` | science-protein-engineering-and-design |
| Choose how much backbone noise the model was trained with | `vanilla_model_weights/` | science-protein-engineering-and-design |
| Call the model from your own Python instead of the command line | `protein_mpnn_utils.py` | science-protein-engineering-and-design |
| Copy a complete pipeline, from parsing structures to designed sequences | `examples/` | science-protein-engineering-and-design |

## Run it here

- **Clone and read**: `git clone --depth 1 --branch v1.0.1 https://github.com/dauparas/ProteinMPNN $EXTERNAL/ProteinMPNN`, read-only; never edit the clone. Read `$EXTERNAL/ProteinMPNN/README.md` first — it lists every flag — then `examples/submit_example_1.sh`, the shortest complete pipeline.
- **Version**: `1.0.1`, the latest release, published 2022-08-19. Before relying on this card: `gh api repos/dauparas/ProteinMPNN --jq .pushed_at` and `gh api repos/dauparas/ProteinMPNN/releases/latest --jq .tag_name`. The last push was 2024-08-14, so `main` carries commits this desk check did not read.
- **Switch off**: nothing. No telemetry and no outbound call in the local code path, and no structure leaves the machine. The entry script runs one local `git rev-parse` against the clone's own git folder to stamp the commit into the FASTA header; it contacts nothing. Keep the clone clean, though: the example scripts write their results back into it and two helper scripts take their paths from inside the file, so copy out what you run.
- **Do not install**: the README's conda recipe with its CUDA toolkit, and do not run the example scripts as they are — each opens with a cluster scheduler header and activates a conda environment that does not exist here. The parts need only Python with PyTorch and NumPy, which still waits for the user's yes. Nothing is downloaded: the weights are in the clone, seven files of about 6.6 MB each, roughly 46 MB in all.
- **In use**: no part is in use; nothing here has been run.

## What's inside

Parts: one entry script with five modes, the module behind it, two weight families, nine helper scripts that write the constraint dictionaries, ten example pipelines, three hosted notebooks, and the bundled inputs and reference outputs.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `protein_mpnn_run.py` | The entry script in its default mode: reads one structure, or a folder parsed into JSON lines, and writes FASTA sequences whose headers carry the score, the global score and the sequence recovery. Temperature, number of sequences, batch size, seed and backbone noise are flags; every constraint arrives as a dictionary from a helper. | candidate | Python with PyTorch and NumPy, a backbone, and the weights already in the clone. Runs on CPU, takes a GPU when there is one; three layers, hidden dimension 128. No network; nothing leaves the machine. | Try it on the first backbone that needs a sequence: default model, one sequence per target, to see the output format. |
| `protein_mpnn_run.py --score_only` | Scores an existing backbone-sequence pair instead of designing, writing an npz file; a bundled example and its recorded output show the shape. | candidate | As the design mode, plus a structure that carries the sequence to score. | Try it when designs from elsewhere must be ranked, or to compare a redesign with the natural sequence. |
| `protein_mpnn_run.py --unconditional_probs_only`, `protein_mpnn_run.py --conditional_probs_only` | Per-position probabilities as npz: in one forward pass for the backbone alone (a bundled example writes one file per structure), or conditioned on the rest of the sequence, with a companion flag for the backbone-only case. | candidate | As the design mode; the unconditional mode is one forward pass, the cheapest of all. | Try the unconditional mode when a profile rather than samples is wanted, the conditional one when single positions have to be reasoned about before choosing mutations by hand. |
| `protein_mpnn_run.py --ca_only` | Switches parser and weights to the alpha-carbon-only models, for backbones given as a CA trace. The release read here is the one that merged this path into the single script. | candidate | As the design mode, with CA-only inputs and the CA weights in the clone. | Try it when a backbone arrives with CA positions only; compare its sequences with a full-backbone run. |
| `protein_mpnn_utils.py` | The library behind the script: model class, featuriser, structure parser, dataset classes, losses and graph helpers. The import surface the notebooks use. | candidate | PyTorch and NumPy; nothing else. | Read it when the model has to be embedded in a pipeline rather than run as a command. |
| `vanilla_model_weights/` | The four full-backbone checkpoints, named for the backbone noise they were trained with; the middle one is the default. | candidate | Nothing to obtain: in the clone, about 26 MB for the four. | Try more than one when designs look too rigid or too random: noise level is the dial between them. |
| `ca_model_weights/` | The three alpha-carbon-only checkpoints, used only with the CA mode, named by the same noise levels. | candidate | Nothing to obtain: in the clone, about 20 MB for the three. | Read before a CA-only run: there is no equivalent here of the noisiest full-backbone checkpoint. |
| `helper_scripts/parse_multiple_chains.py` | Turns a folder of structures into the JSON-lines file the entry script reads; first step of every multi-structure pipeline, with its own CA-only flag. | candidate | Python with NumPy; no GPU, no weights. | Try it first: the cheapest part to run, and it shows whether the structures parse at all. |
| `helper_scripts/assign_fixed_chains.py`, `helper_scripts/make_fixed_positions_dict.py` | What stays fixed: which chains of a complex are designed and which are not, and which positions to keep — or, with one flag inverted, the only positions to design. Positions count from one within the chain, not by structure numbering. | candidate | Python; no GPU. | Try the first with a complex where only one chain is redesigned, the second when a site or interface must survive untouched. |
| `helper_scripts/make_tied_positions_dict.py`, `helper_scripts/make_pos_neg_tied_positions_dict.py` | What is sampled together: positions tied from a list or across every chain of a homo-oligomer, and the same tying with per-chain weights, positive for the wanted state and negative for the state to design against. No bundled example uses the second. | candidate | Python; no GPU. | Try the first for the first symmetric design — it is what makes the chains of an assembly agree — and the second when a sequence must fit one partner and not another. |
| `helper_scripts/make_bias_AA.py`, `helper_scripts/make_bias_per_res_dict.py` | Bias dictionaries: one number per residue type for the whole design (the bundled example pushes it towards polar residues), or a bias per position and residue, whose script body is the template to edit. | candidate | Python; no GPU. | Try the global one when designs come out too hydrophobic, the per-position one when the bias differs over a patch. |
| `helper_scripts/other_tools/make_omit_AA.py`, `helper_scripts/other_tools/make_pssm_dict.py` | The two harder constraints: residue types forbidden at given positions of given chains, and a position-specific scoring matrix with its weighting, threshold and log-odds flags. Both take their paths from inside the file, not from flags. | candidate | Python; no GPU; edit a copy outside the clone. | Try the first when a residue type must not appear at a site, such as cysteines where no disulfide is wanted; the second when a family profile from an alignment should steer the design. |
| `examples/` | Ten complete pipelines: monomer, multi-chain complex, straight from a structure path, score only, fixed positions, design-only positions, tied positions, homo-oligomer, unconditional probabilities, amino-acid bias. The fastest way to see which helper feeds which flag. | candidate | Nothing to read. To run one: the environment and an output folder outside the clone; the scripts otherwise write into the clone and assume a cluster scheduler. | Read the one matching the task before the first run; its header shows the GPU and the 32g of memory the authors used. |
| `colab_notebooks/quickdemo.ipynb`, `colab_notebooks/ca_only_quickdemo.ipynb` | Hosted demos of the full-backbone and the alpha-carbon-only model: each clones the repository in the hosted runtime, fetches a structure by code or takes an upload, and designs with tied positions for homo-oligomers. | candidate | A hosted notebook account and runtime; the structure is uploaded to the hosting service, so data leaves the machine. Not local parts. | Consult them when the local path is blocked and a demo is enough; never for a real structure. |
| `colab_notebooks/quickdemo_wAF2.ipynb` | Design plus validation: after the sequence it installs a structure predictor in the runtime, downloading its code, its parameter archive and an alignment tool from three further hosts, then predicts the designed sequence and compares it with the input backbone. | candidate | As above, plus three more hosts contacted and a parameter download inside the runtime; data leaves the machine. | Consult it as the recipe for the design-then-predict loop, and rebuild that loop locally instead of running it there. |
| `inputs/`, `outputs/` | The bundled structures — monomers, complexes, homo-oligomers — and the recorded results of the eight numbered examples, including the score and probability files. | listed | Nothing. | Read the recorded outputs to compare a first local run against: they are the reference for correct output. |

## Tried

None yet. No part of this repository has been run here; every row above is a desk-check reading.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

The easiest science tool here to try: MIT, weights in the repository, no download, no network, CPU enough. Its shape is one script with five modes plus nine helpers whose only job is to write constraint dictionaries, so the real choice is which constraints to express, not which model to run. It is the step after a backbone generator, which is where it will most likely be used. Revisit when a backbone needs a sequence, when designs have to be scored, or when the freshness check shows a release after `1.0.1` — the last push is years newer than the last release, so `main` may already differ, and a soluble-model weight family may have appeared since.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page
- [[area-science-protein-engineering-and-design|Protein engineering and design]] ([Protein engineering and design](../topics/area-science-protein-engineering-and-design.md)): science section page
- [[rosettacommons-rfdiffusion|RosettaCommons/RFdiffusion]] (../references/rosettacommons-rfdiffusion.md): the backbone generator whose poly-glycine outputs need exactly this step
- [[google-deepmind-alphafold|google-deepmind/alphafold]] (../references/google-deepmind-alphafold.md): the structure prediction that checks whether a designed sequence folds back to its backbone

## Sources

- [Desk check: dauparas/ProteinMPNN v1.0.1](../../raw/repos/dauparas-proteinmpnn-desk-check-2026-11-21.md): every part read from the clone, the licence file against what GitHub reports, freshness through the GitHub API, and what a run would take here.
