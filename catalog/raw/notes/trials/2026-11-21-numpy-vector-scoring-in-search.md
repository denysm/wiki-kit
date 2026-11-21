---
title: "Use record: numpy scoring vectors in a local search script"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-14
ingested: 2026-11-21
repo: numpy/numpy
part: "numpy core (ndarray and array functions)"
version: "2.5.4"
status: in use
tags: [catalog, trial, use-record, kind-library, numpy, search, embeddings]
summary: "numpy 2.5.4 (Homebrew, for Python 3.14 and 3.15; 2.0.2 from the kit folder for Python 3.9) scores embedding vectors in the kit's search script in blocks of 65,536: 9,221 real vectors 0.156 s to 0.0091 s, 100,000 synthetic 1.72 s to 0.123 s, with the same top 10 as pure Python. In use since 2026-11-13. Retold from the measurement note."
---

# Use record: numpy scoring vectors in a local search script

- **Tool and part**: numpy/numpy, the core (`ndarray` and the array functions); the script reads it through `import numpy as np`.
- **Version in use**: 2.5.4 from Homebrew for Python 3.14 and 3.15, and 2.0.2 from the kit's per-Python folder for the Xcode Python 3.9. The desk check read the tag `v2.5.5`, one patch newer than 2.5.4.
- **Task, by kind**: score a query embedding against the stored vectors of a knowledge-base search index (nearest neighbours by dot product) without a Python loop, for a script that runs under `python3 -I`.
- **Dates**: decided 2026-11-13 (the maintainer's decision, recorded in the benchmark note); first run against a live embedding server in the always-on check of 2026-11-14. Source: `../2026-11-21-measurements-local-embeddings.md`.
- **Kind of record**: real use in daily search, not a sandbox trial.

## How it is used

- The kit is no longer standard-library only: numpy is required by `search.py`. If it is missing, `search.py` stops with the line `search.py install-deps`; that command tests `import numpy` first and installs into the per-Python folder (`pip install --target`) only when the import fails. Both installers run it in their self-check.
- Vectors are stored as float16 in SQLite, read 65,536 rows at a time, converted to float32, multiplied by the query vector, and reduced to the best `limit` with `argpartition`. Memory stays flat on a large index.

## Result

- Same top 10 as the pure-Python scoring.
- 9,221 real vectors: 0.156 s to 0.0091 s. 100,000 synthetic vectors: 1.72 s to 0.123 s. 1,000,000 synthetic: 0.992 s. 768 numbers per vector, best of runs; most of what is left is reading rows from SQLite.
- Wall time of a whole `search.py query` process on a real index, median of 10 runs: words only 0.112 s, with vectors 0.183 s.
- `pip install --target` worked on the Xcode Python 3.9 and on Homebrew's 3.15. The bootstrap on Windows is untested.

## Cost

No tokens or money; a few megabytes of disk for the package folder. The cost of the decision is a hard dependency: the kit is no longer standard-library only.
