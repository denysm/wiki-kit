---
title: "Desk check: facebookresearch/faiss v1.16.0"
source: https://github.com/facebookresearch/faiss/tree/v1.16.0
type: repos
authors: ["Meta AI Research", "Hervé Jégou", "Matthijs Douze", "Jeff Johnson", "Lucas Hosseini", "Chengqi Deng", "Alexandr Guzhva", "Gergely Szilvasy"]
source_date: 2026-11-10
ingested: 2026-11-21
repo: facebookresearch/faiss
kind: library
version: "1.16.0"
licence: MIT
tags: [catalog, desk-check, kind-library, faiss, vector-search, nearest-neighbours, science]
summary: "facebookresearch/faiss v1.16.0 read from a read-only clone: the index families (flat, IVF, PQ, HNSW, scalar quantizer, graph and binary indexes, fast-scan variants), clustering, GPU support (CUDA, cuVS, Metal), the Python bindings, contrib, the C API; MIT read from LICENSE; freshness from the GitHub API; why it is the only vector store with a card."
---

# Desk check: facebookresearch/faiss v1.16.0

Read from a shallow clone of tag `v1.16.0` (commit `6ccfd5f9be2283ebc037564bb45c6ba63b71e96a`, committed 2026-11-09) at `$EXTERNAL/faiss`. The clone was not modified; nothing was built, installed or run. Checked 2026-11-21. Version read by this desk check: 1.16.0.

## Repository facts

- README: "Faiss is a library for efficient similarity search and clustering of dense vectors. It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM." Vectors are identified by an integer and compared "with L2 (Euclidean) distances or dot products". Some index types "solely use a compressed representation of the vectors and do not require to keep the original vectors", at the cost of precision. "The GPU implementation can accept input from either CPU or GPU memory"; GPU indexes can replace CPU ones ("replace `IndexFlatL2` with `GpuIndexFlatL2`").
- The trade-offs the README lists for an index type: search time, search quality, memory used per index vector, training time, adding time, need for external data for unsupervised training.
- `LICENSE`: "MIT License", "Copyright (c) Facebook, Inc. and its affiliates." README "Legal": "Faiss is MIT-licensed". Copyright line "Copyright © Meta Platforms, Inc." Third-party notices are in `THIRD_PARTY_NOTICES`.
- `pyproject.toml` (package `faiss-cpu`): `license = "MIT"`, `requires-python = ">=3.10"`, `dependencies = ["numpy>=1.25", "packaging"]`, authors "Meta AI Research". `pyproject-gpu.toml` is the package `faiss-gpu`. PyPI `faiss-cpu` 1.16.0 (Python `>=3.10`) has wheels for macOS arm64 and x86_64, uploaded 2026-11-10.
- `INSTALL.md`: "The supported way to install Faiss is through conda". `faiss-cpu` for Linux (x86-64 and aarch64), OSX (arm64 only) and Windows (x86-64); `faiss-gpu` "available on Linux (x86-64 only) for CUDA 11.4 and 12.1"; `faiss-gpu-cuvs` for CUDA 13.2 on Linux x86-64; "GPU(+CPU) version using AMD ROCm not yet available".
- `CHANGELOG.md`: "[1.16.0] - 2026-11-09"; the release adds, among others, e-means (a k-means variant) with GPU backends, an `IndexPiPNN` graph index and a Metal binary flat index.
- Top-level folders: `faiss/` (C++ library, with `gpu/`, `gpu_metal/`, `impl/`, `invlists/`, `python/`, `svs/`, `utils/`), `c_api/`, `contrib/`, `tutorial/`, `demos/`, `benchs/`, `tests/`, `perf_tests/`, `conda/`, `cmake/`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/facebookresearch/faiss`: `pushed_at` 2026-11-20T17:42:58Z; licence `MIT`; not archived.
- `gh api repos/facebookresearch/faiss/releases/latest`: tag `v1.16.0`, published 2026-11-10T16:03:21Z.
- So the clone is at the latest release; pushes continue after it.

## How to run here

- Clone, read-only: `git clone --depth 1 --branch v1.16.0 https://github.com/facebookresearch/faiss $EXTERNAL/faiss`. Never build or edit it (a build needs CMake, a C++ compiler, SWIG for Python, and CUDA for GPU indexes). Read first: `README.md`, then `tutorial/python/1-Flat.py`, `faiss/IndexFlat.h` and `INSTALL.md`.
- Library: no telemetry or analytics code. A search of `faiss/` and `contrib/` Python files for `urlopen`, `urlretrieve`, `requests`, "telemetry" and "analytics" found nothing. `contrib/datasets.py` names public benchmark datasets (for example http://corpus-texmex.irisa.fr/ and http://ann-benchmarks.com/) in docstrings and loads them from local files.
- Security note: `contrib/README.md` says `rpc.py` is "A very simple Remote Procedure Call library, where function parameters and results are pickled", used with `client_server.py` to shard a dataset over several machines. Pickled calls must not be exposed on an open network.
- What breaks without a build or wheel: the clone is C++ with SWIG bindings; nothing is importable from it. The Python module is `faiss` (`faiss/python/`); its loader (`faiss/python/loader.py`) picks a build variant (AVX512-SPR, AVX512, AVX2, SVE or the generic one) from the CPU's instruction sets, read through numpy; the environment variable `FAISS_OPT_LEVEL` overrides the choice.

## Parts

For a library a part is a module or main entry point. Read: the README, `INSTALL.md`, `contrib/README.md`, the opening doc comment of each header named below, the folder listings of `faiss/python/`, `faiss/gpu/`, `faiss/gpu_metal/`, `faiss/svs/` and `c_api/`, and the tutorial list.

### Index: flat (`faiss/IndexFlat.h`, `faiss/IndexBinaryFlat.h`)

- `IndexFlat`: "Index that stores the full vectors and performs exhaustive search". Exact. `IndexBinaryFlat` does the same for binary vectors (database vectors take `ntotal * d / 8` bytes). Tutorial `tutorial/python/1-Flat.py`.

### Index: inverted file (`faiss/IndexIVFFlat.h`, `faiss/IndexIVF.h`)

- `IndexIVFFlat`: "Inverted file with stored vectors. Here the inverted file pre-selects the vectors to be searched". Needs training (clustering) before vectors are added. Tutorial `2-IVFFlat.py`. Binary version: `IndexBinaryIVF`.

### Index: product quantizer (`faiss/IndexPQ.h`, `faiss/IndexIVFPQ.h`)

- `IndexPQ`: "Index based on a product quantizer. Stored vectors are approximated by PQ codes." `IndexIVFPQ`: "Inverted file with Product Quantizer encoding. Each residual vector is encoded as a product quantizer code." Trade accuracy for much less memory per vector. Tutorial `3-IVFPQ.py`.

### Index: fast scan (`faiss/IndexPQFastScan.h`)

- `IndexPQFastScan`: "Fast scan version of IndexPQ. Works for 4-bit PQ for now." Codes grouped in blocks. Tutorials `7-PQFastScan.py`, `8-PQFastScanRefine.py`. Other fast-scan files: `IndexIVFPQFastScan`, `IndexSQFastScan`, `IndexIVFSQFastScan`.

### Index: HNSW (`faiss/IndexHNSW.h`)

- `IndexHNSW`: "The HNSW index is a normal random-access index with a HNSW link structure built on top". Graph-based approximate search. Tutorial `6-HNSW.py`.

### Index: scalar quantizer (`faiss/IndexScalarQuantizer.h`)

- `IndexScalarQuantizer`: "Flat index built on a scalar quantizer."

### Index: other graph indexes (`faiss/IndexNSG.h`, `faiss/IndexNNDescent.h`, `faiss/IndexPiPNN.h`)

- `IndexNSG`: "a normal random-access index with a NSG link structure built on top"; `IndexNNDescent`: the same with an NNDescent link structure; `IndexPiPNN`: "a PiPNN graph built on top of a flat storage (IndexFlat or IndexScalarQuantizer)", new in 1.16.0.

### Index: hashing and lattice (`faiss/IndexLSH.h`, `faiss/IndexIVFSpectralHash.h`, `faiss/IndexLattice.h`)

- `IndexLSH`: "The sign of each vector component is put in a binary signature". `IndexIVFSpectralHash`: "Inverted list that stores binary codes of size nbit". `IndexLattice`: "Index that encodes a vector with a series of Zn lattice quantizers".

### Index wrappers (`faiss/IndexRefine.h`, `faiss/IndexIDMap.h`, `faiss/IndexShards.h`, `faiss/IndexPreTransform.h`)

- `IndexRefine`: "Index that queries in a base_index (a fast one) and refines the results with an exact search". `IndexIDMap`: "Index that translates search results to ids". `IndexShards`: "Index that concatenates the results from several sub-indexes". `IndexReplicas` and `IndexPreTransform` (a vector transform before the index) are named by file only.

### Index factory (`faiss/index_factory.cpp`, `faiss/index_factory.h`)

- Builds an index from a short description string; named by file only, its string grammar was not read here.

### Clustering (`faiss/Clustering.h`, `faiss/SuperKMeans.h`, `contrib/clustering.py`)

- `Clustering`: "Implementation of k-means clustering with many variants". `SuperKMeans`: "a faster k-means alternative to faiss::Clustering for IVF training and other large-k workloads". e-means demos in `demos/`.

### GPU, CUDA and cuVS (`faiss/gpu/`)

- `GpuIndexFlat`, `GpuIndexIVFFlat`, `GpuIndexIVFPQ`, `GpuIndexIVFScalarQuantizer`, `GpuIndexCagra` (the cuVS graph index) and binary variants; `StandardGpuResources`; `GpuCloner` copies an index to a GPU. Tutorials `4-GPU.py`, `5-Multiple-GPUs.py`, `10-FaissCuvsExample.ipynb`. Needs an NVIDIA GPU; packages for Linux x86-64 only (see INSTALL.md above).

### GPU, Metal (`faiss/gpu_metal/`)

- Files `MetalIndexFlat`, `MetalIndexIVFFlat`, `MetalIndexIVFPQ`, `MetalIndexBinaryFlat` and `StandardMetalResources`; the changelog of 1.16.0 lists "Add MetalIndexBinaryFlat with GPU Hamming search and exact top-k selection" and Metal support in the multi-GPU Python helpers. Whether the `faiss-cpu` wheels include it was not checked. Not run.

### Python bindings (`faiss/python/`)

- SWIG bindings (`swigfaiss.swig`) plus `array_conversions.py`, `class_wrappers.py`, `extra_wrappers.py`, `gpu_wrappers.py` and `loader.py`; the package `faiss`. Depends on numpy (`numpy>=1.25`) and `packaging`. Typed (`py.typed`).

### Python helpers (`contrib/`)

- `contrib/README.md`: helper modules compiled into `faiss.contrib`: `rpc.py`, `client_server.py` (sharding over machines), `ondisk.py` ("merge indexes into an on-disk index"), `exhaustive_search.py` (ground truth for a dataset that may not fit in RAM), `torch_utils.py` (pytorch tensors as arguments), `big_batch_search.py`, `clustering.py`, `datasets.py`, `evaluation.py`, `factory_tools.py`, `inspect_tools.py`, `ivf_tools.py`, `vecs_io.py` (the `.fvecs` formats).

### Intel SVS indexes (`faiss/svs/`)

- Files `IndexSVSFlat`, `IndexSVSVamana`, `IndexSVSIVF` and variants with LVQ and LeanVec compression. Named by file only; the optional dependency they need was not read.

### C API (`c_api/`)

- C wrappers for flat, IVF, HNSW, LSH, scalar-quantizer and binary indexes, `index_factory_c`, `index_io_c`, `AutoTune_c`, `Clustering_c`. Named by file only.

### Index families named by file only

- `IndexRaBitQ` and its fast-scan and IVF variants, additive-quantizer indexes (`IndexAdditiveQuantizer`, `IndexIVFAdditiveQuantizer`), `IndexIVFEDEN` and `IndexEDEN`, `IndexNeuralNetCodec`, `Index2Layer`, `IndexBinaryHNSW`, `IndexBinaryHash`.

### Benchmarks and demos (`benchs/`, `demos/`, `tutorial/`)

- `tutorial/python/` has ten numbered tutorials from `1-Flat.py` to `10-FaissCuvsExample.ipynb`; `demos/` has C++ and Python demos (for example `demo_sift1M.cpp`, `demo_ondisk_ivf.py`); `benchs/` reproduces the papers named in the README.

## Why FAISS is the only vector store with a card

The kit's decided case, retold: FAISS is the one vector store that the kit owner's own sources actually use, once in a sketch of a local embedding pipeline and once as a benchmark in a literature review. FAISS is a library, not a server. Qdrant and Milvus get no card until a task needs a vector database server. Pinecone is out of scope: a hosted service, not an open repository, and data leaves the machine. FAISS is therefore `candidate` here, not rejected and not in use: the kit's own search scores vectors with numpy over a SQLite index and has not needed an index structure.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 41 model calls on sonnet, $2.05 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
