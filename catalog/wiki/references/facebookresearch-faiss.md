---
title: "facebookresearch/faiss"
category: reference
kind: library
areas: [search-and-embeddings, science]
science_sections: [scientific-databases]
repo: facebookresearch/faiss
version: "1.16.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/facebookresearch-faiss-desk-check-2026-11-21.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, area-science, science-scientific-databases, kind-library, faiss, vector-search, nearest-neighbours]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Library for similarity search and clustering of dense vectors: exact and approximate indexes (flat, inverted file, product quantizer, HNSW and more), binary indexes, k-means, CUDA, cuVS and Metal GPU indexes, Python bindings. Read at v1.16.0 (MIT). It is the only vector store in the catalog; Qdrant and Milvus get no card until a task needs a database server, and Pinecone is out. Candidate: read, not tried."
---

# facebookresearch/faiss

> A C++ library with Python bindings (kind `library`, licence MIT read from `LICENSE`, version `1.16.0` read in a clone): "efficient similarity search and clustering of dense vectors", in sets "of any size, up to ones that possibly do not fit in RAM". Here it is read from a clone and not installed; it is the one vector store the catalog covers.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Find the exact nearest neighbours of a vector among up to a few million, on one machine | `IndexFlat` | search-and-embeddings |
| Search a large set of vectors faster than exact search, at some loss of recall | `IndexIVFFlat` | search-and-embeddings |
| Search by graph, without a training step for the clusters | `IndexHNSW` | search-and-embeddings |
| Fit many vectors in RAM by compressing them | `IndexIVFPQ` | search-and-embeddings |
| Re-rank the hits of a compressed index with exact distances | `IndexRefine` | search-and-embeddings |
| Group vectors into clusters (k-means) | `Clustering` | search-and-embeddings |
| Find the nearest records of a scientific database that have been turned into embedding vectors, on one machine | `IndexFlat` | science-scientific-databases |
| Compare binary fingerprints of records by Hamming distance | `IndexBinaryFlat` | science-scientific-databases |
| Search a vector set too large for RAM, or merge indexes on disk | `contrib` helpers | science-scientific-databases |

## Run it here

- **Clone, read-only**: `git clone --depth 1 --branch v1.16.0 https://github.com/facebookresearch/faiss $EXTERNAL/faiss`. Never build or edit it. Read first: `README.md`, then `tutorial/python/1-Flat.py`, `faiss/IndexFlat.h` and `INSTALL.md`.
- **Version**: `1.16.0`, the latest release, published 2026-11-10. Before relying on this card, compare with upstream: `gh api repos/facebookresearch/faiss --jq .pushed_at` and `gh api repos/facebookresearch/faiss/releases/latest --jq .tag_name`.
- **Sends outward**: nothing; a library, with no telemetry code found. The `contrib` module `rpc.py` pickles function parameters and results and serves `client_server.py`; never expose it on an open network.
- **Switch off**: nothing needs switching off. `FAISS_OPT_LEVEL` overrides which CPU build the Python loader picks.
- **Do not install**: `conda install -c pytorch -c conda-forge faiss-cpu=1.16.0` (INSTALL.md: "The supported way to install Faiss is through conda") or the PyPI wheel `faiss-cpu`, which needs `numpy>=1.25`; real installation waits for the user's yes. A build needs CMake, a C++ compiler, SWIG and, for GPU indexes, CUDA.
- **Why it is the only vector store**: the decided case, retold in the desk check. FAISS is the store the kit owner's sources actually use, and it is a library. Qdrant and Milvus get no card until a task needs a vector database server. Pinecone is out: a hosted service, and data leaves the machine.

## What's inside

For a library a part is a module or main entry point: here the index families, clustering, GPU support and the Python layer. Source: `faiss/`, `contrib/`, `c_api/` in the clone.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `IndexFlat` | "Index that stores the full vectors and performs exhaustive search"; exact, L2 or dot product. | candidate | The `faiss-cpu` wheel or a build; RAM for all vectors | Try it first on the next semantic-search task whose vectors outgrow the numpy scoring of the kit's search script. |
| `IndexIVFFlat` | Inverted file with stored vectors: "pre-selects the vectors to be searched"; needs training. | candidate | The wheel; a training sample | Try it when exact search is too slow on one machine. |
| `IndexIVFPQ` | Inverted file with product-quantizer codes of residual vectors. | candidate | The wheel; a training sample | Try it when the vectors no longer fit in RAM. |
| `IndexPQ` | Stored vectors approximated by product-quantizer codes. | candidate | The wheel; a training sample | Try it when memory per vector is the limit. |
| `IndexPQFastScan` | "Fast scan version of IndexPQ. Works for 4-bit PQ for now." | candidate | The wheel; a CPU with the SIMD it needs | Try it after `IndexPQ` when its scan speed is the limit. |
| `IndexHNSW` | HNSW link structure on top of a random-access index. | candidate | The wheel | Try it when low query time matters more than build time. |
| `IndexScalarQuantizer` | "Flat index built on a scalar quantizer." | candidate | The wheel | Try it for a simple, less lossy compression than PQ. |
| `IndexNSG`, `IndexNNDescent`, `IndexPiPNN` | Other graph indexes (NSG, NNDescent link structures; PiPNN, new in `1.16.0`). | candidate | The wheel | Try them only if `IndexHNSW` does not fit. |
| `IndexLSH`, `IndexIVFSpectralHash`, `IndexLattice` | Hashing and lattice-quantizer indexes. | candidate | The wheel | Try them for binary codes of float vectors. |
| `IndexRefine` | Queries a fast base index, then "refines the results with an exact search". | candidate | The wheel | Try it on top of a compressed index when recall drops. |
| `IndexIDMap` | "Index that translates search results to ids". | candidate | The wheel | Try it when stored vectors need the caller's ids. |
| `IndexShards` | "Index that concatenates the results from several sub-indexes". | candidate | The wheel | Try it when an index is split across files or machines. |
| `IndexBinaryFlat` | Exact search over binary vectors by Hamming distance (`ntotal * d / 8` bytes). `IndexBinaryIVF` is the inverted-file version. | candidate | The wheel | Try it on binary fingerprints of records. |
| `Clustering` | "k-means clustering with many variants"; `SuperKMeans` is "a faster k-means alternative" for IVF training and large k. | candidate | The wheel | Try it when vectors must be grouped or an IVF index trained. |
| `faiss.gpu` (CUDA, cuVS) | GPU indexes (`GpuIndexFlat`, `GpuIndexIVFFlat`, `GpuIndexIVFPQ`, `GpuIndexCagra`); `GpuCloner` moves an index to the GPU. | candidate | An NVIDIA GPU; `faiss-gpu` packages for Linux x86-64 only; CUDA 11.4 and 12.1, or 13.2 with cuVS | Try it when a machine with an NVIDIA GPU holds the vectors. |
| `faiss.gpu_metal` | Apple GPU indexes (`MetalIndexFlat`, `MetalIndexIVFFlat`, `MetalIndexIVFPQ`, `MetalIndexBinaryFlat`); not checked whether the `faiss-cpu` wheel includes it. | candidate | A Mac with Apple Silicon and possibly a build from source | Try it only if flat search on the Mac's CPU is too slow. |
| Python bindings (`faiss/python/`) | SWIG module `faiss`; the loader picks an AVX512-SPR, AVX512, AVX2, SVE or generic build; vectors go in as numpy arrays. | candidate | Python `>=3.10`, `numpy>=1.25`, `packaging` | Try it as the way to call every index above. |
| `contrib` | Helpers in `faiss.contrib`: `ondisk.py` merges indexes into an on-disk index, `exhaustive_search.py` computes ground truth for sets that may not fit in RAM, `torch_utils.py` accepts pytorch tensors, `rpc.py` and `client_server.py` shard over machines, `vecs_io.py` reads `.fvecs` files. | candidate | The wheel; for `rpc.py`, a closed network | Try `ondisk.py` and `exhaustive_search.py` when an index passes RAM; never `rpc.py` on an open network. |
| `index_factory` | Builds an index from a short description string (`faiss/index_factory.cpp`); the grammar was not read. | listed | The wheel | Read when an index must be chosen by a configuration string. |
| `IndexReplicas`, `IndexPreTransform` | Replicated sub-indexes and a vector transform in front of an index; named by file only. | listed | The wheel | Read when queries must be spread across replicas or vectors reduced first. |
| `IndexRaBitQ` (and fast-scan, IVF variants) | RaBitQ quantization indexes; named by file only. | listed | The wheel | Read when 1-bit-per-dimension codes are wanted. |
| Additive quantizers (`IndexAdditiveQuantizer`, `IndexIVFAdditiveQuantizer`) and `IndexEDEN`, `IndexNeuralNetCodec`, `Index2Layer` | Further quantization indexes; named by file only. | listed | The wheel | Read when PQ is not accurate enough. |
| `IndexBinaryHNSW`, `IndexBinaryHash` | Binary indexes with a graph or a hash table; named by file only. | listed | The wheel | Read when `IndexBinaryFlat` is too slow. |
| Intel SVS indexes (`faiss/svs/`) | `IndexSVSFlat`, `IndexSVSVamana`, `IndexSVSIVF` with LVQ and LeanVec variants; named by file only. | listed | An optional Intel library, not read | Read when the machine is Intel and graph search is wanted. |
| C API (`c_api/`) | C wrappers for flat, IVF, HNSW, LSH, scalar-quantizer and binary indexes; named by file only. | listed | A build | Read when a non-Python, non-C++ language must call FAISS. |
| `tutorial/`, `demos/`, `benchs/` | Ten numbered Python tutorials (`1-Flat.py` to `10-FaissCuvsExample.ipynb`), demos, and benchmarks that reproduce the papers. | listed | A wheel, and data for the benchmarks | Read `tutorial/python/1-Flat.py` first when writing the first FAISS call. |

## Tried

None yet. Real use waits for a task whose vectors outgrow the kit's numpy scoring.

## Verdict

FAISS is the one vector store with a card, chosen because the kit owner's sources use it and because it is a library: no server to run, no data leaving the machine. Every part read is a candidate; none was run, and the kit's own search still scores with numpy. Known costs: conda is the supported install and the PyPI wheel route was not tried; GPU packages exist for Linux x86-64 only; the Metal indexes were not checked against the wheels. Revisit when a task needs more vectors than the numpy scoring handles (the kit timed 1,000,000), when a vector database server is needed (then Qdrant or Milvus get cards), or when the freshness check shows a release after `1.16.0`.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; vector scoring and indexes for semantic search on one machine
- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; the scientific-databases section holds the nearest-neighbour tasks
- [[numpy-numpy|numpy/numpy]] (../references/numpy-numpy.md): the vector scoring in use; a dependency of the FAISS Python package
- [[ollama-ollama|ollama/ollama]] (../references/ollama-ollama.md): serves the embeddings a FAISS index would hold

## Sources

- [Desk check: facebookresearch/faiss v1.16.0](../../raw/repos/facebookresearch-faiss-desk-check-2026-11-21.md): index families, GPU, bindings and contrib read from the clone, freshness through the GitHub API, why FAISS is the only vector store.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): the numpy scoring timings (up to 1,000,000 vectors) that FAISS would have to beat, retold.
