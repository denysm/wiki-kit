---
title: "Desk check: deepchem/deepchem 2.8.0"
source: https://github.com/deepchem/deepchem/tree/2.8.0
type: repos
authors: ["DeepChem contributors"]
source_date: 2024-04-03
ingested: 2026-11-21
repo: deepchem/deepchem
kind: library
version: "2.8.0"
licence: MIT
tags: [catalog, desk-check, kind-library, deepchem, cheminformatics, drug-discovery, moleculenet, graph-neural-networks, rdkit]
summary: "The main modules of deepchem/deepchem 2.8.0 read from a read-only clone: featurizers, datasets and loaders, MoleculeNet loaders, splitters, transformers, metrics, models by backend (TensorFlow, PyTorch, Hugging Face, scikit-learn, gradient boosting, JAX, Lightning, DFT), hyperparameter search, docking, meta-learning, reinforcement learning, utilities and the tutorials; what downloads data or sends it out; freshness from the GitHub API."
---

# Desk check: deepchem/deepchem 2.8.0

Read from a shallow clone of tag `2.8.0` (commit `d5b293934d427062f52e2d92c1569d53d10418f9`, committed 2024-04-02), at `$EXTERNAL/deepchem`. The clone was not modified; nothing was installed or run. Checked 2026-11-21. Version read by this desk check: 2.8.0. Parts are the package's main modules and their main entry points, as schema.md asks for a library; each module's `__init__.py` was read for its exports, and the source was searched for downloads and outbound calls.

## Repository facts

- Description on GitHub: "Democratizing Deep-Learning for Drug Discovery, Quantum Chemistry, Materials Science and Biology". README: "DeepChem aims to provide a high quality open-source toolchain that democratizes the use of deep-learning in drug discovery, materials science, quantum chemistry, and biology."
- `LICENSE`: the MIT licence text, "Copyright 2017 PandeLab". `setup.py` classifier: "License :: OSI Approved :: MIT License". GitHub reports MIT. They agree.
- `deepchem/__init__.py`: `__version__ = '2.8.0'`; it imports every submodule (`data`, `feat`, `hyper`, `metalearning`, `metrics`, `models`, `splits`, `trans`, `utils`, `dock`, `molnet`, `rl`). Backend-specific classes are imported inside `try` blocks; a missing backend is skipped with a logged warning.
- `setup.py`: maintainer "DeepChem contributors"; `install_requires` `joblib`, `numpy>=1.21`, `pandas`, `scikit-learn`, `sympy`, `scipy>=1.10.1`, `rdkit`; `python_requires='>=3.7,<3.12'`. Extras: `jax` (`jax`, `jaxlib`, `dm-haiku`, `optax`), `torch` (`torch`, `torchvision`, `pytorch-lightning`, `dgl`, `dgllife`), `tensorflow` (`tensorflow`, `tensorflow_probability`, `tensorflow_addons`), `dqc` (`dqc`, `xitorch`, `torch`, `pylibxc2`). README: "DeepChem currently supports Python 3.7 through 3.10".
- Soft requirements (`docs/source/get_started/requirements.rst`), among them: TensorFlow `2.15` and PyTorch `2.2.1` for `dc.models`; PyTorch Geometric; DGL and DGL-LifeSci for torch models; Mordred, Mol2vec and PubChemPy for molecule featurizers; matminer and Pymatgen for material featurizers; pyGPGO for `dc.hyper.gaussian_process`; OpenAI Gym and TensorFlow Probability for `dc.rl`; XGBoost and LightGBM for `dc.models.gbdt_models`; Weights & Biases for `dc.models.keras_model`; pysam for `dc.feat.bio_seq_featurizer`; simdna for `dc.metrics.genomic_metrics`; BioPython, MDTraj, OpenMM, PDBFixer for `dc.utils`.
- README on GPUs: "If GPU support is required, then make sure CUDA is installed and then install the desired deep learning framework". A GPU is optional.
- Outside the package: `contrib/` (17 contributed projects, not imported by `deepchem`), `examples/` (44 entries; `examples/tutorials/` holds 49 notebooks), `datasets/` (sample data files, 146M on disk), `docker/` (Dockerfiles `deepchem`, `deepchem-tf-cpu`, `deepchem-tf-gpu`, `deepchem-torch-cpu`, `deepchem-torch-gpu`, `nightly`, `tag`; the `deepchem` one starts `FROM ubuntu:22.04`), `docs/`, `scripts/`, `requirements/`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/deepchem/deepchem`: `pushed_at` 2026-08-20T19:01:34Z; licence `MIT`; default branch `master`; not archived.
- `gh api repos/deepchem/deepchem/releases/latest`: tag `2.8.0`, name "2.8.0 Initial Release", published 2024-04-03T16:21:23Z. Latest tags: `2.8.0`, `2.8.0.pre`, `2.7.1`.
- `gh api repos/deepchem/deepchem/compare/2.8.0...master`: `master` is 230 commits ahead of the tag. The README offers a nightly build of the head (`pip install --pre deepchem`), not checked here.
- So the clone is at the latest release, but the project kept moving on `master` for more than two years after it.

## How to run here

- Clone: `git clone --depth 1 --branch 2.8.0 https://github.com/deepchem/deepchem $EXTERNAL/deepchem`, read-only. Read `README.md`, then the module's `__init__.py` and the docstrings of the classes it exports (they carry runnable examples), and `docs/source/get_started/requirements.rst` for optional packages.
- Running needs a virtual environment with Python below 3.12 (`python_requires='>=3.7,<3.12'`) and RDKit, plus the extra for the chosen backend. Not installed here; a system `python3` of 3.12 or newer cannot install this version.
- Data folder: `dc.utils.data_utils.get_data_dir()` returns `DEEPCHEM_DATA_DIR` when set, otherwise `tempfile.gettempdir()` (the system temp folder). Downloads and featurized datasets go there.
- Downloads and outbound calls found (search for `download_url(`, `urllib.request`, `requests.get`, `from_pretrained(` outside the tests):
  - `dc.molnet`: every `load_*` function downloads its dataset, from `deepchemdata.s3-us-west-1.amazonaws.com` for most and from `data.broadinstitute.org` for the BBBC image sets.
  - `dc.feat`: `Mol2VecFingerprint` downloads `mol2vec_model_300dim.tar.gz` from the same S3 bucket; `CGCNNFeaturizer` downloads `atom_init.json`; `PubChemFingerprint` sends each molecule to PubChem: its docstring says "PubChemPy use REST API to get the fingerprint, so you need the internet access", so the molecules leave the machine; `HuggingFaceFeaturizer`, `BertFeaturizer` and `RobertaFeaturizer` load tokenizers from the Hugging Face Hub.
  - `dc.splits`: `TimeSplitterPDBbind` downloads `pdbbind_year.csv` over plain `http` from the DeepChem S3 website.
  - `dc.models.torch_models.hf_models`: `Chemberta` loads the tokenizer `seyonec/PubChem10M_SMILES_BPE_60k` from the Hugging Face Hub by default.
  - `dc.dock`: `GninaPoseGenerator` works only on Linux; when the binary is missing it downloads `https://github.com/gnina/gnina/releases/download/v1.0/gnina` into the data folder, marks it executable and runs it (the code calls `os.chmod(downloaded_file, 755)` with a decimal 755). Its docstring: "GNINA requires CUDA >= 10.1 for fast CNN scoring".
  - Weights & Biases: off by default; `KerasModel` and `TorchModel` take `wandb: bool = False` and an optional `WandbLogger`.
  - Telemetry: none found (search for `telemetry`, `analytics`, `sentry_sdk`, `posthog`, `mixpanel` in `deepchem/`).
- Switch off: set `DEEPCHEM_DATA_DIR` to a scratch folder and put dataset files there before calling a loader; do not use `PubChemFingerprint` on molecules that must stay local; leave `wandb` off.
- Do not run as they are: the tutorial notebooks' install cells (46 of the 49 notebooks contain a `pip install` line, most often `pip install --pre deepchem`, written for Colab), `pip install deepchem` into a system Python, `docker pull deepchemio/deepchem`, and `GninaPoseGenerator` (it downloads and executes a binary).

## Parts

### `dc.feat` (featurizers, `deepchem/feat/`)

- Turns raw inputs into model features; entry point `featurizer.featurize(...)`. Base classes `Featurizer`, `MolecularFeaturizer`, `ComplexFeaturizer`, `MaterialStructureFeaturizer`, `MaterialCompositionFeaturizer`, `UserDefinedFeaturizer`.
- Molecule featurizers: fingerprints (`CircularFingerprint`, `MACCSKeysFingerprint`, `PubChemFingerprint`, `Mol2VecFingerprint`), descriptors (`RDKitDescriptors`, `MordredDescriptors`, `CoulombMatrix`, `CoulombMatrixEig`), graphs (`ConvMolFeaturizer`, `WeaveFeaturizer`, `MolGraphConvFeaturizer`, `PagtnMolGraphFeaturizer`, `DMPNNFeaturizer`, `GroverFeaturizer`, `MATFeaturizer`, `MXMNetFeaturizer`, `SNAPFeaturizer`), sequences and images (`OneHotFeaturizer`, `SmilesToSeq`, `SmilesToImage`), conformers (`RDKitConformerFeaturizer`).
- Protein-ligand complex featurizers: `RdkitGridFeaturizer`, `ContactCircularFingerprint`, `SplifFingerprint`, voxelizers (charge, salt bridge, cation-pi, pi-stacking, hydrogen bond), `AtomicConvFeaturizer`, `BindingPocketFeaturizer`.
- Material featurizers: `ElementPropertyFingerprint`, `SineCoulombMatrix`, `CGCNNFeaturizer`, `ElemNetFeaturizer`, `LCNNFeaturizer`.
- Sequence and text: a position frequency matrix featurizer, `SAMFeaturizer`, `BAMFeaturizer`, `CRAMFeaturizer` (need pysam), `SmilesTokenizer`, `BasicSmilesTokenizer`, `BertFeaturizer`, `RobertaFeaturizer`, `RxnFeaturizer`, `HuggingFaceFeaturizer`, `HuggingFaceVocabularyBuilder`.
- Needs: the venv with RDKit; optional packages per featurizer (Mordred, PubChemPy, Mol2vec, matminer, Pymatgen, pysam, transformers); network for `Mol2VecFingerprint`, `CGCNNFeaturizer`, `PubChemFingerprint` and the Hugging Face tokenizers, as above.

### `dc.data` (datasets and loaders, `deepchem/data/`)

- Datasets: `Dataset`, `NumpyDataset` (in memory), `DiskDataset` (sharded on disk), `ImageDataset`. Loaders that featurize files into datasets, entry point `loader.create_dataset(...)`: `CSVLoader`, `UserCSVLoader`, `JsonLoader`, `SDFLoader`, `FASTALoader`, `FASTQLoader`, `ImageLoader`, `InMemoryLoader`, `SAMLoader`, `BAMLoader`, `CRAMLoader`.
- Needs: the venv; Pillow for images; pysam for SAM, BAM and CRAM. No network call in the loaders (the only URL in `data_loader.py` code is in a docstring example).

### `dc.molnet` (MoleculeNet loaders, `deepchem/molnet/`)

- 44 `load_*` functions, among them `load_tox21`, `load_toxcast`, `load_hiv`, `load_bbbp`, `load_bace_classification`, `load_bace_regression`, `load_clintox`, `load_sider`, `load_muv`, `load_pcba`, `load_delaney`, `load_freesolv`, `load_lipo`, `load_qm7`, `load_qm8`, `load_qm9`, `load_pdbbind`, `load_chembl`, `load_chembl25`, `load_zinc15`, `load_uspto`, `load_kinase`, `load_factors`, `load_hppb`, `load_thermosol`, the BBBC image sets `load_bbbc001` to `load_bbbc005`, `load_cell_counting`, and materials sets (`load_bandgap`, `load_perovskite`, `load_mp_formation_energy`, `load_mp_metallicity`, `load_Platinum_Adsorption`).
- Each returns the tasks, a tuple of datasets and the transformers. Example defaults of `load_tox21`: `featurizer='ECFP'` (a `CircularFingerprint` of size 1024), `splitter='scaffold'`, `transformers=['balancing']`, `reload=True`; `data_dir` and `save_dir` default to the data folder.
- Also: DNA simulators (`simulate_motif_density_localization`, `simulate_motif_counting` and others in `dnasim`).
- Needs: the venv and network on first use (downloads as above); disk in the data folder.

### `dc.splits` (splitters, `deepchem/splits/`)

- `RandomSplitter`, `RandomStratifiedSplitter`, `RandomGroupSplitter`, `SingletaskStratifiedSplitter`, `IndexSplitter`, `SpecifiedSplitter`, `ScaffoldSplitter`, `MolecularWeightSplitter`, `MaxMinSplitter`, `FingerprintSplitter`, `ButinaSplitter`, `TaskSplitter`, plus `TimeSplitterPDBbind`. Entry points `splitter.train_valid_test_split(...)` and `splitter.k_fold_split(...)`.
- Needs: the venv with RDKit; network only for `TimeSplitterPDBbind`.

### `dc.trans` (transformers, `deepchem/trans/`)

- Reversible data transformations: `NormalizationTransformer`, `BalancingTransformer`, `DuplicateBalancingTransformer`, `LogTransformer`, `ClippingTransformer`, `MinMaxTransformer`, `CDFTransformer`, `PowerTransformer`, `CoulombFitTransformer`, `IRVTransformer`, `DAGTransformer`, `FeaturizationTransformer`, `ImageTransformer`, `FlatteningTransformer`, `RxnSplitTransformer`; `undo_transforms` maps predictions back.
- Needs: the venv.

### `dc.metrics` (metrics, `deepchem/metrics/`)

- `Metric` wraps a scoring function for multitask models; functions include `roc_auc_score`, `prc_auc_score`, `accuracy_score`, `balanced_accuracy_score`, `f1_score`, `matthews_corrcoef`, `kappa_score`, `r2_score`, `pearson_r2_score`, `rms_score`, `mae_score`, `mean_squared_error`, `bedroc_score`, `concordance_index`, `jaccard_index`, `pixel_error`.
- Needs: the venv (scikit-learn); simdna for genomic metrics.

### `dc.models` TensorFlow models (`deepchem/models/*.py`)

- Base `KerasModel`; models `GraphConvModel`, `WeaveModel`, `DTNNModel`, `DAGModel`, `MPNNModel`, `MultitaskIRVClassifier`, `RobustMultitaskClassifier`, `RobustMultitaskRegressor`, `ProgressiveMultitaskClassifier`, `ProgressiveMultitaskRegressor`, `ScScoreModel`, `SeqToSeq`, `GAN`, `WGAN`, `BasicMolGANModel`, `TextCNNModel`, `AtomicConvModel`, `Smiles2Vec`, `ChemCeption`. Common entry points from `Model`: `fit(dataset)`, `predict(...)`, `evaluate(...)`.
- Needs: the venv with the `tensorflow` extra (TensorFlow `2.15` per the docs); a GPU is optional.

### `dc.models.torch_models` (PyTorch models, `deepchem/models/torch_models/`)

- Base `TorchModel` and `ModularTorchModel`; models `AttentiveFPModel`, `CGCNNModel`, `GATModel`, `GCNModel`, `LCNNModel`, `PagtnModel`, `MATModel`, `MPNNModel`, `MultitaskRegressor`, `MultitaskClassifier`, `CNN`, `DTNNModel`, `WeaveModel`, `ProgressiveMultitaskModel`, `TextCNNModel`, `SeqToSeqModel`, `GANModel`, `WGANModel`, `BasicMolGANModel`, `InfoGraphModel`, `InfoGraphStarModel`, `GroverModel`, `NormalizingFlow`, `InfoMax3DModular`; imported in the PyTorch Geometric block of `models/__init__.py`: `MEGNetModel`, `DMPNNModel`, `GNNModular`.
- Needs: the venv with the `torch` extra (PyTorch `2.2.1` per the docs, DGL, DGL-LifeSci; PyTorch Geometric for some); a GPU is optional.

### `dc.models.torch_models.hf_models` (Hugging Face models)

- `HuggingFaceModel` wraps a `transformers` model and tokenizer for masked-language-model pretraining (`task='mlm'`) or fine-tuning (`task='regression'`, `task='classification'`); `Chemberta` is ChemBERTa built on it, with a RoBERTa tokenizer.
- Needs: the venv with `torch` and `transformers`; network for the default tokenizer `seyonec/PubChem10M_SMILES_BPE_60k`.

### `dc.models.sklearn_models` (`deepchem/models/sklearn_models/`)

- `SklearnModel` wraps any scikit-learn estimator so it takes DeepChem datasets.
- Needs: the venv only (scikit-learn is a core requirement).

### `dc.models.gbdt_models` (`deepchem/models/gbdt_models/`)

- `GBDTModel` for XGBoost and LightGBM models with early stopping; `XGBoostModel` is kept as an old name.
- Needs: the venv plus XGBoost or LightGBM.

### `dc.models.jax_models` (`deepchem/models/jax_models/`)

- `JaxModel` and `PINNModel` (physics-informed neural networks).
- Needs: the venv with the `jax` extra.

### `dc.models.lightning` (`deepchem/models/lightning/`)

- `DCLightningModule` and `DCLightningDatasetModule` wrap DeepChem models and datasets for PyTorch Lightning; `DistributedTrainer` comes from `deepchem/models/trainer`.
- Needs: the venv with the `torch` extra (`pytorch-lightning`).

### `dc.models.dft` (`deepchem/models/dft/`)

- `XCModel` runs "Differentiable Quantum Chemistry (i.e, DFT) calculations, using an exchange correlation functional that has been replaced by a neural network"; with `DFTXC`, `HybridXC` and `XCNNSCF`.
- Needs: the venv with the `dqc` extra (`dqc`, `xitorch`, `torch`, `pylibxc2`).

### `dc.hyper` (hyperparameter search, `deepchem/hyper/`)

- `GridHyperparamOpt`, `RandomHyperparamOpt`, `GaussianProcessHyperparamOpt`; entry point `hyperparam_search(...)`.
- Needs: the venv; pyGPGO for the Gaussian process search.

### `dc.dock` (docking, `deepchem/dock/`)

- `VinaPoseGenerator` (its docstring: "This class requires RDKit and vina to be installed"), `GninaPoseGenerator` (Linux only; downloads and runs the gnina binary as above), `Docker` (pose generation, optionally scored by a model), `ConvexHullPocketFinder`.
- Needs: the venv with `vina` for Vina; Linux, a GitHub download and, for fast scoring, CUDA for gnina.

### `dc.metalearning` (`deepchem/metalearning/`)

- `MAML`, model-agnostic meta-learning; the exported class in `maml.py` uses TensorFlow (`torch_maml.py` holds a PyTorch version that `__init__.py` does not import).
- Needs: the venv with the `tensorflow` extra.

### `dc.rl` (reinforcement learning, `deepchem/rl/`)

- `A2C` and `PPO` (TensorFlow), `Environment` and `GymEnvironment` (wraps `gym.make(name)`), a tic-tac-toe environment in `envs/`.
- Needs: the venv with the `tensorflow` extra and TensorFlow Probability; OpenAI Gym for Gym environments.

### `dc.utils` (utilities, `deepchem/utils/`)

- Helpers used by the other modules: `data_utils` (`get_data_dir`, `download_url`, `untargz_file`, `unzip_file`, file loaders, `save_to_disk`), `rdkit_utils`, `genomics_utils`, `sequence_utils`, `docking_utils`, `vina_utils`, `pdbqt_utils`, `voxel_utils`, `conformers`, `fragment_utils`, `evaluate`, DFT helpers.
- Needs: the venv; optional packages per helper (BioPython, MDTraj, OpenMM, PDBFixer).

### `examples/tutorials` (notebooks)

- 49 Jupyter notebooks, from `An_Introduction_To_MoleculeNet.ipynb` and `Creating_Models_with_TensorFlow_and_PyTorch.ipynb` to `Advanced_Model_Training.ipynb` and `Cell_Counting_Tutorial.ipynb`. 46 contain a `pip install` line, written for Colab.
- Needs: Jupyter and the venv; read the notebooks, skip their install cells.

## Statuses after this desk check

All 20 parts above were read: each is `candidate`. None is `listed`. No part was tried or used, and none is rejected.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 111 model calls on opus, $6.77 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
