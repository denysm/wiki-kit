---
title: "Desk check: numpy/numpy v2.5.5"
source: https://github.com/numpy/numpy/tree/v2.5.5
type: repos
authors: ["NumPy Developers"]
source_date: 2026-11-15
ingested: 2026-11-21
repo: numpy/numpy
kind: library
version: "2.5.5"
licence: BSD-3-Clause
tags: [catalog, desk-check, kind-library, numpy, arrays, vectors, python]
summary: "numpy/numpy v2.5.5 read from a read-only clone: the ndarray core and the subpackages (linalg, fft, random, ma, polynomial, lib and the rest); BSD-3-Clause read from LICENSE.txt, vendored licences in wheels; freshness from the GitHub API; the one network-capable module; how the kit's search script uses it."
---

# Desk check: numpy/numpy v2.5.5

Read from a shallow clone of tag `v2.5.5` (commit `afcbc6d21a88a7b59c5bfe115198e24ed51b3dae`, committed 2026-11-15) at `$EXTERNAL/numpy`. The clone was not modified; nothing was built or installed. Checked 2026-11-21. Version read by this desk check: 2.5.5.

## Repository facts

- README: "NumPy is the fundamental package for scientific computing with Python." It provides "a powerful N-dimensional array object", "sophisticated (broadcasting) functions", "tools for integrating C/C++ and Fortran code" and "useful linear algebra, Fourier transform, and random number capabilities". Site https://numpy.org, documentation https://numpy.org/doc.
- `LICENSE.txt`: "Copyright (c) 2005-2025, NumPy Developers", a BSD 3-clause text. `pyproject.toml` comment: "The main NumPy project license is BSD-3-Clause."; its SPDX field is `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` for a build from source with no vendoring. The same file says wheels on PyPI vendor `libopenblas` (BSD-3-Clause AND BSD-3-Clause-Attribution; all except arm64 macOS>=14) and `libgfortran` (GPL-3.0-with-GCC-exception; all except arm64 macOS>=14).
- `pyproject.toml`: `name = "numpy"`, `version = "2.5.5"`, `requires-python = ">=3.12"`. PyPI for 2.5.5: licence expression `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0`, Python `>=3.12`, first upload 2026-11-15.
- Source folders: `numpy/` (the package), `doc/`, `benchmarks/`, `tools/`, `meson.build` (the build uses Meson; `building_with_meson.md`).

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/numpy/numpy`: `pushed_at` 2026-11-20T20:29:10Z; licence reported as `NOASSERTION` (GitHub cannot pick one licence because of the extra licence files; `LICENSE.txt` says BSD-3-Clause); not archived.
- `gh api repos/numpy/numpy/releases/latest`: tag `v2.5.5`, published 2026-11-15T23:35:10Z.
- So the clone is at the latest release. The version in use in the kit (below) is 2.5.4, one patch older.

## How to run here

- Clone, read-only, for reading docs and source only: `git clone --depth 1 --branch v2.5.5 https://github.com/numpy/numpy $EXTERNAL/numpy`. Never build or edit it; a source build needs Meson and compilers. Read first: `README.md`, then `numpy/_core/fromnumeric.py` and `doc/source/reference/`.
- Library: no telemetry or analytics code. A search of `numpy/` (outside tests) for `urlopen`, `urlretrieve`, `requests`, "telemetry" and "analytics" found one module that can reach the network, `numpy/lib/_datasource.py` (class `DataSource`): "DataSource files can originate locally or remotely", URLs (http, ftp, ...), and it downloads a remote file into a local folder when asked to open it. Nothing else calls out; whether other functions use `DataSource` was not traced.
- Install used by the kit: the Python package is installed by `search.py install-deps` (see How the kit uses it), not by building the clone.

## Parts

For a library a part is a module or main entry point. Read: the folder `numpy/`, the docstrings of the subpackages, the reference rst files named, and the three functions the kit's search script calls.

### Core: the N-dimensional array and universal functions (`numpy/_core/`, imported as `numpy`)

- `doc/source/reference/arrays.ndarray.rst`: "An ndarray is a (usually fixed-size) multidimensional container of items of the same type and size." The core holds `ndarray`, the dtypes, ufuncs and the array functions (`numpy/_core/fromnumeric.py` defines `argpartition(a, kth, axis=-1, kind='introselect', order=None)`; `doc/source/reference/routines.linalg.rst`: the `numpy.matmul` function "implements the `@` operator"). C sources are in `numpy/_core/src/` (`multiarray`, `umath`, `npysort`, `highway`, `npymath`, `common`, `_simd`).
- Needs: a Python `>=3.12` and the wheel (the clone is not importable without a build).

### `numpy.linalg` (`numpy/linalg/`)

- Docstring: "The NumPy linear algebra functions rely on BLAS and LAPACK to provide efficient low level implementations of standard linear algebra algorithms."

### `numpy.fft` (`numpy/fft/`)

- Docstring: "Discrete Fourier Transform"; says the SciPy module `scipy.fft` "is a more comprehensive superset of `numpy.fft`", which "includes only a basic set of routines".

### `numpy.random` (`numpy/random/`)

- Docstring: "Use `default_rng()` to create a `Generator` and call its methods."

### `numpy.ma` (`numpy/ma/`)

- Docstring: "Masked Arrays": for "arrays sometimes contain invalid or missing data".

### `numpy.polynomial` (`numpy/polynomial/`)

- Docstring: "A sub-package for efficiently dealing with polynomials."

### `numpy.lib` (`numpy/lib/`)

- Docstring: "mostly a space for implementing functions that don't belong in core or in another NumPy submodule"; holds the file input and output (`_npyio_impl.py`), set operations, histograms, index tricks, NaN-aware functions, and `_datasource.py` (the network-capable module above).

### Modules read by name or first docstring line only

- `numpy.f2py` (`numpy/f2py/`): "Fortran to Python Interface Generator."
- `numpy.testing` (`numpy/testing/`): common test support.
- `numpy.dtypes` (`numpy/dtypes.py`): specific dtype classes.
- `numpy.typing` (`numpy/typing/`): type annotations and aliases, since 1.20.
- `numpy.exceptions` (`numpy/exceptions.py`): general exceptions and warnings.
- `numpy.matrixlib` (`numpy/matrixlib/`): the `matrix` class and related functions.
- `numpy.strings`, `numpy.char`, `numpy.rec`, `numpy.ctypeslib`: folders or modules present; no docstring read.

## How the kit uses it

Retold from the kit's own sources: the benchmark note (`../notes/2026-11-21-measurements-local-embeddings.md`) and `scripts/search.py`, read 2026-11-21.

- `scripts/search.py` declares `REQUIRES = ("numpy",)`. `search.py install-deps` puts numpy into a per-Python folder (`~/.local/share/wiki-kit/python<X.Y>`) unless that Python already has it: it first tests `import numpy`, and only if that fails runs `python -m pip install -q --target <folder> numpy`. Without numpy, `search.py` stops with one line naming that command.
- Vector scoring (`vector_hits`): the query vector goes into `np.asarray(q, dtype=np.float32)`; vectors stored in SQLite as float16 are read in blocks of 65,536 rows (`cursor.fetchmany(65536)`), turned into a matrix with `np.frombuffer(..., dtype="<f2")`, scored with `mat.astype(np.float32) @ qv`, kept to the best `limit` with `np.argpartition`, and ordered with `np.argsort`; ids go through `np.fromiter`, scores through `np.concatenate`.
- Facts from the note (maintainer's decision of 2026-11-13): the kit stopped being standard-library only; numpy scoring gives the same top 10 as the pure-Python scoring; 9,221 real vectors 0.156 s to 0.0091 s, 100,000 synthetic 1.72 s to 0.123 s, 1,000,000 synthetic 0.992 s (768 numbers, best of runs; most of what is left is reading rows from SQLite). Scripts run with `python3 -I`, which ignores `pip install --user`, and Homebrew's Python refuses a plain `pip install`, hence the folder. numpy 2.5.4 comes from Homebrew for Python 3.14 and 3.15, and 2.0.2 from the kit folder for the Xcode Python 3.9. Always-on check of 2026-11-14: scoring ran against a live embedding server. The bootstrap step on Windows is untested.
- Status: `in use`; use record `../notes/trials/2026-11-21-numpy-vector-scoring-in-search.md`.

## Cost of this desk check

Written in one agent run together with the other 3 desk checks, the cards and the use records of the same batch: 41 model calls on sonnet, $2.05 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
