---
title: "Freshness re-check: NVIDIA/NeMo-Speech.cpp after v0.3.0"
source: https://github.com/NVIDIA/NeMo-Speech.cpp
type: repos
authors: ["NVIDIA"]
source_date: 2026-11-22
ingested: 2026-11-23
repo: NVIDIA/NeMo-Speech.cpp
kind: cli
version: "0.3.0"
licence: Apache-2.0
tags: [catalog, freshness, kind-cli, nemo-speech-cpp, diarization]
summary: "Re-check on 2026-11-23 after catalog_fresh.py reported a push on 2026-11-22: no release after v0.3.0; nightly adds two commits (CUDA graphs on Jetson, speech-LLM Q2_0 and CPU MoE offload), none touching diarize; the 2026-11-22 push went to side branches. v0.3.0 already carries the diarization fix #87."
---

# Freshness re-check: NeMo-Speech.cpp after v0.3.0

Checked 2026-11-23 with `gh api` and `git ls-remote` against the read-only clone.

- `pushed_at` 2026-11-22T07:43:43Z. Releases: `nightly` 2026-11-13, `v0.3.0` 2026-10-30, `v0.2.0` 2026-10-02. No commit on `main` since 2026-11-15; `HEAD` equals `nightly` (`e790e46`).
- `v0.3.0` (`69154fd`) → `nightly`: two commits, "fix(cuda): CUDA graphs idle bug on Jetson" (#104) and "feat(speechlm): Q2_0 quant and CPU MoE offload for smaller GPUs" (#99). Neither touches diarization.
- Branches besides `main`: `fix/tts-longform-cache`, `fix/windows-cuda-compat`, `pre-commit-ci-update-config`, `pull-request/111`, `salm-model-index`; the 2026-11-22 push is on one of these.
- `v0.3.0` contains "fix(diar): correct speaker attribution and word timing; label speakers in text/SRT/VTT (#87)", committed 2026-10-29: words at speaker changes no longer take the next speaker, and WebVTT output carries `<v Speaker N>`.
- CLI guide (`docs/cli.md`, diarize section): "A stateful streaming pass is the default and is appropriate for long recordings"; `--offline` is one full-attention pass, limited to about 6.6 minutes.
- Conclusion: the desk check of 2026-11-21 stands for `diarize`.
