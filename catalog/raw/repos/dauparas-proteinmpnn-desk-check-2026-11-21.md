---
title: "Desk check: dauparas/ProteinMPNN v1.0.1"
source: https://github.com/dauparas/ProteinMPNN/tree/v1.0.1
type: repos
authors: ["Justas Dauparas"]
source_date: 2022-08-19
ingested: 2026-11-21
repo: dauparas/ProteinMPNN
kind: app
version: "1.0.1"
licence: MIT
tags: [catalog, desk-check, kind-app, proteinmpnn, protein-design, sequence-design, science, protein-engineering-and-design]
summary: "Every part of ProteinMPNN v1.0.1 read from a read-only clone: the one entry script with its five output modes, the utility module, the two model weight families shipped in the repository (four full-backbone and three CA-only checkpoints of about 6.6 MB each), nine helper scripts that build the JSONL dictionaries for fixed chains, fixed and tied positions, bias and PSSM, ten SLURM example scripts, three Colab notebooks that send the structure to Google Colab, and the bundled example inputs and outputs. Licence MIT in the file and as GitHub reports it; freshness from the GitHub API; no telemetry or outbound call in the local code path."
---

# Desk check: dauparas/ProteinMPNN v1.0.1

Read from a shallow clone of tag `v1.0.1` (commit `905b0081f3aa3404d7ac22174bc25710f9995ff8`, committed 2022-08-18), at `$EXTERNAL/ProteinMPNN`. The clone was not modified; nothing was installed or run. Checked 2026-11-21. Version read by this desk check: 1.0.1.

## Repository facts

- `LICENSE` is the full MIT text: "MIT License", "Copyright (c) 2022 Justas Dauparas". There is no second licence file in the clone, and no separate terms for the model weights that ship inside it.
- README, first lines: "To run ProteinMPNN clone this github repo and install Python>=3.0, PyTorch, Numpy." Code organisation as the README states it: `protein_mpnn_run.py` — "the main script to initialialize and run the model"; `protein_mpnn_utils.py` — "utility functions for the main script"; `examples/` — "simple code examples"; `inputs/`, `outputs/`, `colab_notebooks/`.
- Model weights ship in the repository, unlike most tools of this kind. "Full protein backbone models: `vanilla_model_weights/v_48_002.pt, v_48_010.pt, v_48_020.pt, v_48_030.pt`." and "CA only models: `ca_model_weights/v_48_002.pt, v_48_010.pt, v_48_020.pt`. Enable flag `--ca_only` to use these models." Each vanilla checkpoint is 6681301 bytes and each CA-only checkpoint 6624011 bytes, about 6.6 MB; seven files, roughly 46 MB in all. There is no `soluble_model_weights` folder at this tag.
- Naming: the `--model_name` help says "ProteinMPNN model name: v_48_002, v_48_010, v_48_020, v_48_030; v_48_010=version with 48 edges 0.10A noise", and the default is `v_48_020`.
- Fixed hyper-parameters in `protein_mpnn_run.py`: `hidden_dim = 128`, `num_layers = 3`; `k_neighbors` comes from the checkpoint (`checkpoint['num_edges']`), and the script prints the checkpoint's training noise level.
- Output format, from the README's example header: `>3HTN, score=1.1705, global_score=1.2045, fixed_chains=['B'], designed_chains=['A', 'C'], model_name=v_48_020, git_hash=..., seed=37` and per sample `>T=0.1, sample=1, score=0.7291, global_score=0.9330, seq_recovery=0.5736`. The README defines `score` as "average over residues that were designed negative log probability of sampled amino acids" and `global score` as "average over all residues in all chains negative log probability of sampled/fixed amino acids".

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/dauparas/ProteinMPNN`: `pushed_at` 2024-08-14T02:57:30Z; default branch `main`; not archived; description "Code for the ProteinMPNN paper".
- Licence as GitHub reports it: `"spdx_id":"MIT"`, name "MIT License" — the same as the file says, so nothing has to be reconciled.
- `gh api repos/dauparas/ProteinMPNN/releases/latest`: tag `v1.0.1`, name "Making code cleaner", published 2022-08-19T04:02:22Z, release body "Combining vanilla and CA versions into one script!". Two releases in all: `v1.0.1` and `v1.0.0` (published 2022-07-29T17:16:28Z).
- So the clone is at the latest release; `main` has been pushed since (2024-08-14), and those commits are not covered by this desk check.

## How to run here

- **Clone**: `git clone --depth 1 --branch v1.0.1 https://github.com/dauparas/ProteinMPNN $EXTERNAL/ProteinMPNN`, read-only. Never edit the clone.
- **Read first**: `README.md` (92 lines) — it lists every flag of the entry script — then `examples/submit_example_1.sh` for the shortest complete run.
- **Telemetry and outbound calls**: none in the local code path. A search for `https://`, `requests.`, `urllib`, `wget`, `boto3` and `wandb` across the Python files returned one documentation comment in `protein_mpnn_utils.py` ("A number of functions/classes are adopted from: https://github.com/jingraham/neurips19-graph-protein-design"). No structure leaves the machine when the entry script is used. The three Colab notebooks are the exception and are described under Parts.
- **One local shell call**: `protein_mpnn_run.py` stamps the FASTA header with the repository commit through `subprocess.check_output(f'git --git-dir {script_dir}/.git rev-parse HEAD', shell=True)`, falling back to `'unknown'` on `CalledProcessError`. It reads the clone's own git directory; it contacts nothing.
- **Writes**: everything goes to `--out_folder`. The bundled examples write into `../outputs/...` inside the clone and would modify it, so point `--out_folder` outside the clone and copy an example script out before running it.
- **Do not install**: the README's conda recipe (`conda create --name mlfold`, `source activate mlfold`, `conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch`), and do not run the SLURM example scripts as they are — each begins with `source activate mlfold`. A venv with PyTorch and NumPy waits for the user's yes.
- **What a run takes**: Python with PyTorch and NumPy, and the weights already in the clone — nothing to download. `protein_mpnn_run.py` picks its device as `torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")`, so it runs on CPU without a GPU; the model is small (three layers, hidden dimension 128, about 6.6 MB per checkpoint). The repository's own measure of a run is the SLURM header of every example: `#SBATCH -p gpu`, `--mem=32g`, `--gres=gpu:rtx2080:1` and `-c 2` or `-c 3`. `--batch_size` help: "can set higher for titan, quadro GPUs, reduce this if running out of GPU memory". `--max_length` defaults to 200000.
- **Nothing was run** for this desk check: no environment was created, no sequence was designed.

## Parts

### Command: `protein_mpnn_run.py` (sequence design, the default mode)

- 423 lines, the only command. Input is either `--pdb_path` (a single structure, with `--pdb_path_chains`) or `--jsonl_path`, a folder of structures parsed into JSONL by the helper script. Output goes to `--out_folder` as FASTA files under `seqs/`.
- The sampling flags: `--num_seq_per_target` (default 1), `--sampling_temp` (default "0.1"; help: "Suggested values 0.1, 0.15, 0.2, 0.25, 0.3. Higher values will lead to more diversity."), `--batch_size` (default 1), `--seed` (0 picks a random seed), `--backbone_noise` (default 0.00), `--omit_AAs` (default `X`).
- Conditioning flags, each taking a JSONL dictionary from a helper script: `--chain_id_jsonl`, `--fixed_positions_jsonl`, `--tied_positions_jsonl`, `--bias_AA_jsonl`, `--bias_by_res_jsonl`, `--omit_AA_jsonl`, `--pssm_jsonl` with `--pssm_multi`, `--pssm_threshold`, `--pssm_log_odds_flag`, `--pssm_bias_flag`.
- Model choice: `--model_name` (default `v_48_020`) and `--path_to_model_weights`; without the latter the script resolves `vanilla_model_weights/` or, with `--ca_only`, `ca_model_weights/` next to itself.
- Needs: Python with PyTorch and NumPy, a backbone structure, the weights in the clone; CPU is enough, a GPU is faster.

### Mode: `protein_mpnn_run.py --score_only`

- Scores an existing backbone-sequence pair instead of designing: "return score only (model's uncertainty)" in the README's example list. `examples/submit_example_3_score_only.sh` runs it with `--num_seq_per_target 10 --score_only 1`; the bundled result is `outputs/example_3_score_only_outputs/score_only/3HTN.npz`.
- `--save_score` writes `score=-log_prob` to npy files for a normal design run.
- Needs: the same as the design mode.

### Mode: `protein_mpnn_run.py --conditional_probs_only`

- "output conditional probabilities p(s_i given the rest of the sequence and backbone)"; the companion flag `--conditional_probs_only_backbone` gives "p(s_i given backbone)". Written as npz files.
- No bundled example script uses it; the flags are documented in the README's flag list.
- Needs: the same as the design mode.

### Mode: `protein_mpnn_run.py --unconditional_probs_only`

- "output unconditional probabilities p(s_i given backbone) in one forward pass" — a PSSM-like matrix per structure. `examples/submit_example_7.sh` runs it; the bundled results are `outputs/example_7_outputs/unconditional_probs_only/5L33.npz` and `6MRR.npz`.
- Needs: the same as the design mode.

### Mode: `protein_mpnn_run.py --ca_only`

- "Parse CA-only structures and use CA-only models (default: false)". It switches both the parser and the weights folder: backbones given by alpha-carbon positions only. `helper_scripts/parse_multiple_chains.py` has the matching `--ca_only` flag, and `colab_notebooks/ca_only_quickdemo.ipynb` is its demo.
- The v1.0.1 release note marks this as the release that combined the two code paths: "Combining vanilla and CA versions into one script!".
- Needs: the same as the design mode, plus CA-only inputs and the CA-only weights.

### Module: `protein_mpnn_utils.py`

- 1362 lines: the `ProteinMPNN` model class, `tied_featurize`, `parse_PDB`, `StructureDataset` and `StructureDatasetPDB`, the loss functions (`loss_nll`, `loss_smoothed`), the graph helpers (`gather_edges`, `gather_nodes`, `cat_neighbors_nodes`) and `_scores` / `_S_to_seq`. Header comment: "A number of functions/classes are adopted from: https://github.com/jingraham/neurips19-graph-protein-design".
- It is the import surface for using ProteinMPNN as a library: the Colab notebooks import exactly these names.
- Needs: PyTorch and NumPy; nothing else.

### Weights: `vanilla_model_weights/`

- The four full-backbone checkpoints `v_48_002.pt`, `v_48_010.pt`, `v_48_020.pt` and `v_48_030.pt`, 6681301 bytes each, differing in the Gaussian backbone noise they were trained with (0.02 Å, 0.10 Å, 0.20 Å, 0.30 Å by the naming rule in the `--model_name` help). The default is `v_48_020`; each file carries `num_edges` and `noise_level` which the script reads and prints.
- Licence: no separate terms; the repository's MIT licence is the only one in the clone.
- Needs: nothing to obtain — they are in the clone, about 26 MB for the four.

### Weights: `ca_model_weights/`

- The three CA-only checkpoints `v_48_002.pt`, `v_48_010.pt` and `v_48_020.pt`, 6624011 bytes each, used only with `--ca_only`.
- Licence: the same MIT licence; no separate terms.
- Needs: nothing to obtain — in the clone, about 20 MB for the three.

### Helper: `helper_scripts/parse_multiple_chains.py`

- 163 lines. `--input_path` a folder of pdb files, `--output_path` the JSONL to write, `--ca_only`. It is the first step of every multi-structure example and produces the `parsed_pdbs.jsonl` the entry script reads through `--jsonl_path`.
- Needs: Python with NumPy; no GPU.

### Helper: `helper_scripts/assign_fixed_chains.py`

- 39 lines. `--input_path` (parsed pdbs), `--output_path`, `--chain_list` "List of the chains that need to be designed". Output looks like `{"5TTA": [["A"], ["B"]], "3LIS": [["A"], ["B"]]}` — designed chains first, fixed chains second — and is passed as `--chain_id_jsonl`.
- Needs: Python; no GPU.

### Helper: `helper_scripts/make_fixed_positions_dict.py`

- 59 lines. `--chain_list` and `--position_list` ("e.g. 11 12 14 18, 1 2 3 4 for first chain and the second chain"), plus `--specify_non_fixed`, which inverts the meaning so the list names the residues to design. Output is passed as `--fixed_positions_jsonl`. Used by `submit_example_4.sh` and `submit_example_4_non_fixed.sh`; the example notes "The first amino acid in the chain corresponds to 1 and not PDB residues index for now."
- Needs: Python; no GPU.

### Helper: `helper_scripts/make_tied_positions_dict.py`

- 61 lines. Ties positions so they are sampled together: `--chain_list` with `--position_list`, or `--homooligomer 1` to tie every position of every chain. Output is passed as `--tied_positions_jsonl`; this is how symmetric and homo-oligomeric sequences are designed (`submit_example_5.sh`, `submit_example_6.sh`).
- Needs: Python; no GPU.

### Helper: `helper_scripts/make_pos_neg_tied_positions_dict.py`

- 73 lines. The same tying with per-chain weights for positive and negative design: `--pos_neg_chain_list` and `--pos_neg_chain_betas` ("1.0 for the positive design, -0.1 or -0.5 for negative, 0.0 means do not use that chain info"), plus `--homooligomer`.
- No bundled example script uses it.
- Needs: Python; no GPU.

### Helper: `helper_scripts/make_bias_AA.py`

- 27 lines. `--AA_list` and `--bias_list` produce a global amino-acid bias dictionary, for example `{"A": -0.01, "G": 0.02}`, passed as `--bias_AA_jsonl`. `submit_example_8.sh` uses it to add a polar bias of 1.39 to "D E H K N Q R S T W Y".
- Needs: Python; no GPU.

### Helper: `helper_scripts/make_bias_per_res_dict.py`

- 53 lines. `--input_path` (parsed pdbs) and `--output_path`: a per-position, per-amino-acid bias dictionary, passed as `--bias_by_res_jsonl`. The body of the script is the template to edit for the bias you want.
- Needs: Python; no GPU.

### Helper: `helper_scripts/other_tools/make_omit_AA.py`

- 39 lines. Builds the dictionary for `--omit_AA_jsonl`, which forbids given amino acids at given positions of given chains. The script carries two `#MODIFY this path` comments: paths are edited in the file, not passed on the command line.
- Needs: Python; no GPU.

### Helper: `helper_scripts/other_tools/make_pssm_dict.py`

- 64 lines. Builds the PSSM dictionary for `--pssm_jsonl`, used with `--pssm_multi`, `--pssm_threshold`, `--pssm_log_odds_flag` and `--pssm_bias_flag`. Like the script above, input and output paths are edited inside the file.
- Needs: Python; no GPU.

### Examples: `examples/`

- Ten SLURM submit scripts, each a complete pipeline from parsing to design: `submit_example_1.sh` (monomer), `submit_example_2.sh` (multi-chain), `submit_example_3.sh` (straight from a pdb path), `submit_example_3_score_only.sh` (score only), `submit_example_4.sh` (fixed positions), `submit_example_4_non_fixed.sh` (design only the listed positions), `submit_example_5.sh` (tied positions, symmetry), `submit_example_6.sh` (homo-oligomer), `submit_example_7.sh` (unconditional probabilities) and `submit_example_8.sh` (amino-acid bias).
- Every one of them opens with the SLURM header quoted above and `source activate mlfold`, and writes into `../outputs/` inside the clone; they are read here as recipes, not run as they are.
- Needs: nothing to read. To run one: the environment, and an output path outside the clone.

### Notebook: `colab_notebooks/quickdemo.ipynb`

- A Google Colab demo of the full-backbone model. It clones the repository in the Colab runtime (`os.system("git clone -q https://github.com/dauparas/ProteinMPNN.git")`), fetches a structure by code (`os.system(f"wget -qnc https://files.rcsb.org/view/{pdb_code}.pdb")`) or takes an upload through `files.upload()`, then imports the model from `protein_mpnn_utils` and designs sequences with tied positions for homo-oligomers.
- Needs: a Google account and the Colab runtime. The structure is uploaded to Google: data leaves the machine. Not a local part.

### Notebook: `colab_notebooks/ca_only_quickdemo.ipynb`

- The same demo against the CA-only weights, with the same clone, `wget` from the structure database and `files.upload()` steps.
- Needs: as above; data leaves the machine.

### Notebook: `colab_notebooks/quickdemo_wAF2.ipynb`

- Design plus validation: after ProteinMPNN it installs AlphaFold2 inside the Colab runtime, downloading `colabfold.py` from raw.githubusercontent.com, the AlphaFold parameter archive `alphafold_params_2021-07-14.tar` from storage.googleapis.com and `MMalign.cpp` from zhanggroup.org, then predicts the designed sequence "with single-sequence input" and compares it with the input backbone.
- Needs: the Colab runtime, several downloads inside it, and an uploaded or fetched structure. Data leaves the machine, and three more hosts are contacted.

### Bundled inputs and outputs

- `inputs/`: six structures in three folders — `PDB_monomers/pdbs/5L33.pdb` and `6MRR.pdb`, `PDB_complexes/pdbs/3HTN.pdb` and `4YOW.pdb`, `PDB_homooligomers/pdbs/4GYT.pdb` and `6EHB.pdb`.
- `outputs/`: the recorded results of the eight examples (parsed and assigned JSONL files, designed FASTA files under `seqs/`, the score-only and unconditional-probability npz files). They are the reference to compare a first run against.
- Only the folder listings were read; the structure and result files themselves were not opened.
- Needs: nothing.

## Reasons for status

No part is rejected, taken as a method, or held as a reference. Every part read above is a candidate: this is the reference sequence-design model for backbones produced by a structure generator, and nothing here has been run. The parts marked as known only from their listing are the bundled inputs and outputs.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 51 model calls on opus, $7.83 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
