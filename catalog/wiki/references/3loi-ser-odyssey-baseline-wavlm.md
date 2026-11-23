---
title: "3loi Odyssey 2024 WavLM baselines (SER-Odyssey-Baseline-WavLM)"
category: reference
kind: model
areas: [live-speech-and-calls]
url: https://huggingface.co/3loi/SER-Odyssey-Baseline-WavLM-Categorical
version: "50632bb / 00d0e12"
licence: MIT
desk_checked: 2026-11-23
sources:
  - raw/repos/speech-emotion-models-desk-check-2026-11-23.md
created: 2026-11-23
updated: 2026-11-23
tags: [catalog, card, area-live-speech-and-calls, kind-model, speech-emotion-recognition, wavlm, msp-podcast, english]
confidence: medium
volatility: warm
verified: 2026-11-23
---

# 3loi Odyssey 2024 WavLM baselines


## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Track how aroused and how positive a speaker sounds, as numbers from 0 to 1, during a call | Multi-Attributes | live-speech-and-calls |

## Run it here

- **No clone.** `config.json`, `model.safetensors` and `pipeline_utils.py` at the pinned revisions through `huggingface_hub.snapshot_download`, into a sandbox folder.
- **To try it**: avoid `trust_remote_code`: copy the model classes from `pipeline_utils.py` (MIT), build WavLM-large from its config only (`WavLMConfig` of `microsoft/wavlm-large`, then `WavLMModel(cfg)`), load the safetensors, normalise audio by the config's mean and std. The remote code would otherwise fetch the full WavLM-large weights first.
- **Sends outward**: only the downloads.
- **Do not install**: Transformers in the kit's Python; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| Multi-Attributes | Arousal, dominance, valence per utterance. | tried | PyTorch and Transformers, 1274490516 bytes; RTF 0.023 on M4 Metal | The real task that would move it to `in use`: the mood trend per speaker in a live call, after an accuracy check on labelled speech. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict


## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page

## Sources

- [Desk check: speech emotion models](../../raw/repos/speech-emotion-models-desk-check-2026-11-23.md): cards, licences, categories, competition scores, the custom model code.
