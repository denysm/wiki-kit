---
title: "numpy/numpy"
category: reference
kind: library
areas: [search-and-embeddings]
repo: numpy/numpy
version: "2.5.5"
licence: BSD-3-Clause
desk_checked: 2026-11-21
sources:
  - raw/repos/numpy-numpy-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-numpy-vector-scoring-in-search.md
  - raw/notes/2026-11-21-measurements-local-embeddings.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-search-and-embeddings, kind-library, numpy, arrays, vectors, python]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Python's array library: the N-dimensional array and its functions, plus linear algebra, FFT, random numbers, masked arrays and polynomials. Read at v2.5.5 (BSD-3-Clause). The core is in use: it scores embedding vectors in the kit's search script, in blocks of 65,536, at 0.123 s for 100,000 synthetic vectors. The other modules are read or listed."
---

# numpy/numpy

> A Python library (kind `library`, licence BSD-3-Clause read from `LICENSE.txt`, version `2.5.5` read in a clone; the version in use is `2.5.4`): "the fundamental package for scientific computing with Python". Here its array core scores embedding vectors for the kit's search by meaning, and is the kit's only dependency beyond the standard library.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Score a query vector against many stored vectors and keep the best few, without a Python loop | `numpy` core | search-and-embeddings |
| Solve linear systems, decompose matrices, take norms | `numpy.linalg` | search-and-embeddings |
| Draw random samples or shuffles reproducibly | `numpy.random` | search-and-embeddings |
| Take a Fourier transform of a signal or series | `numpy.fft` | search-and-embeddings |
| Compute over arrays that have missing values | `numpy.ma` | search-and-embeddings |
| Open a data file from a URL or a local path with one call | `numpy.lib` | search-and-embeddings |

## Run it here

- **Clone, read-only, for docs and source only**: `git clone --depth 1 --branch v2.5.5 https://github.com/numpy/numpy $EXTERNAL/numpy`. Never build or edit it; a source build needs Meson and compilers. Read first: `README.md`, then `numpy/_core/fromnumeric.py` and `doc/source/reference/`.
- **Version**: `2.5.5`, the latest release, published 2026-11-15. Before relying on this card, compare with upstream: `gh api repos/numpy/numpy --jq .pushed_at` and `gh api repos/numpy/numpy/releases/latest --jq .tag_name`.
- **In use**: the core, at `2.5.4`, in `scripts/search.py` of the kit: vectors stored as float16 are read 65,536 rows at a time, multiplied by the query vector (`@`), cut to the best few with `argpartition` and ordered with `argsort`. Installed per Python version: `2.5.4` from Homebrew for Python 3.14 and 3.15, `2.0.2` in the kit's folder for Python 3.9. The tag read is `2.5.5`, one patch newer than the version in use.
- **Sends outward**: nothing, as a library; no telemetry code found. The one module that can fetch a URL is `numpy.lib` (`_datasource.py`, `DataSource`), and only when asked to open a remote path.
- **Switch off**: nothing needs switching off.
- **Do not install**: do not `pip install` or build the clone. The kit's own route is `python3 -I scripts/search.py install-deps`, which tests `import numpy` first and installs into `~/.local/share/wiki-kit/python<X.Y>` only when the import fails; a real run of it waits for the user's yes. Wheels from PyPI vendor `libopenblas` and `libgfortran` with their own licences (the `pyproject.toml` comment names them).

## What's inside

For a library a part is a module or main entry point. Source: `numpy/` in the clone.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `numpy` core (`numpy/_core/`) | The `ndarray`, dtypes, ufuncs and array functions; the kit uses `asarray`, `frombuffer`, `fromiter`, `concatenate`, `@`, `argpartition`, `argsort`. | in use | Python `>=3.12` for `2.5.5` (`2.0.2` runs the Xcode Python 3.9); the wheel, not the clone | Re-check when the latest release leaves `2.5.4` for a minor version, or when `search.py` changes how it scores (blocks of 65,536, float16 storage). |
| `numpy.linalg` | Linear algebra on BLAS and LAPACK. | candidate | The wheel | Try it when a task needs matrix decomposition or solving beyond a dot product. |
| `numpy.fft` | "Discrete Fourier Transform", a basic set of routines; `scipy.fft` is the larger one. | candidate | The wheel | Try it on a signal or time series task. |
| `numpy.random` | `default_rng()` and its `Generator`. | candidate | The wheel | Try it when a reproducible sample or a synthetic test set is needed. |
| `numpy.ma` | Masked arrays for invalid or missing data. | candidate | The wheel | Try it when an array has gaps that must not enter a sum or mean. |
| `numpy.polynomial` | Polynomial classes and fitting. | candidate | The wheel | Try it when a curve fit is needed. |
| `numpy.lib` | Helper functions: file input and output, set operations, histograms, NaN-aware functions, and `DataSource`, which can open a remote file. | candidate | The wheel; network only for remote paths | Try it when a file must be read from a URL or loaded in a standard format. |
| `numpy.f2py` | Fortran to Python interface generator. | listed | A Fortran compiler | Read when Fortran code must be called from Python. |
| `numpy.testing` | Common test support. | listed | The wheel | Read when writing tests on arrays. |
| `numpy.dtypes` | Classes of specific dtypes. | listed | The wheel | Read when a dtype must be inspected. |
| `numpy.typing` | Type annotations and aliases. | listed | The wheel | Read when annotating array code. |
| `numpy.exceptions` | General exceptions and warnings. | listed | The wheel | Read when catching numpy errors. |
| `numpy.matrixlib` | The `matrix` class and related functions. | listed | The wheel | Read only for old code that uses `matrix`. |
| `numpy.strings`, `numpy.char` | String operations on arrays (folders present; no docstring read). | listed | The wheel | Read when text arrays must be processed. |
| `numpy.rec`, `numpy.ctypeslib` | Record arrays and ctypes interop (modules present; no docstring read). | listed | The wheel | Read when a C structure must be mapped to an array. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-13 to 2026-11-14 | Score embedding vectors for a local search script | `numpy` core | In use: same top 10 as pure Python; 9,221 real vectors 0.156 s to 0.0091 s, 100,000 synthetic 1.72 s to 0.123 s. | no tokens; a hard dependency | [use record](../../raw/notes/trials/2026-11-21-numpy-vector-scoring-in-search.md) |

## Verdict

numpy is the kit's one dependency beyond the standard library, taken on 2026-11-13: its core scores vectors far faster than a pure-Python loop (0.156 s to 0.0091 s for 9,221 real vectors), with the same top 10. The other modules are read or listed and wait for a task. Known costs: a missing numpy stops `search.py` until `install-deps` runs, and the Windows bootstrap is untested. Revisit when the latest release passes `2.5.4` by a minor version, when `search.py` changes its scoring, or when an index grows past the 1,000,000 vectors timed.

## See Also

- [[area-search-and-embeddings|Search and embeddings]] ([Search and embeddings](../topics/area-search-and-embeddings.md)): area page; vector scoring for semantic search on one machine
- [[facebookresearch-faiss|facebookresearch/faiss]] (../references/facebookresearch-faiss.md): the one vector store in the catalog, a library of index structures
- [[ollama-ollama|ollama/ollama]] (../references/ollama-ollama.md): the server that makes the vectors numpy scores
- [[onnxruntime-onnxruntime|onnxruntime]] (../references/onnxruntime-onnxruntime.md): its Python package depends on numpy

## Sources

- [Desk check: numpy/numpy v2.5.5](../../raw/repos/numpy-numpy-desk-check-2026-11-21.md): modules read from the clone, licence from the file, freshness through the GitHub API, how the search script uses it.
- [Use record: numpy scoring vectors in a local search script](../../raw/notes/trials/2026-11-21-numpy-vector-scoring-in-search.md): the real use behind `in use` and the Tried row.
- [Measurements: local embedding models and runtimes](../../raw/notes/2026-11-21-measurements-local-embeddings.md): the numpy decision, timings and install route, retold.
