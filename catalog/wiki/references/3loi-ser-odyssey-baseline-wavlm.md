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
summary: "The Odyssey 2024 competition baselines trained on MSP-Podcast: WavLM-large with attentive pooling, one model for eight emotion categories and one for arousal, dominance and valence (MIT, 1.27 GB each). Read from the cards and API metadata; not run here."
---

# 3loi Odyssey 2024 WavLM baselines

> Two Hugging Face models (kind `model`, licence MIT, revisions `50632bb` and `00d0e12` read): the categorical and the attribute baselines of the Odyssey 2024 speech emotion challenge, trained on English podcast speech. Not run here.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Score how aroused and how positive speech sounds, as numbers from 0 to 1, per utterance | Multi-Attributes | live-speech-and-calls |
| Label an utterance with one of eight emotions | Categorical | live-speech-and-calls |

## Run it here

- **No clone.** `config.json`, `model.safetensors` and `pipeline_utils.py` at the pinned revisions through `huggingface_hub.snapshot_download`, into a sandbox folder.
- **To try it**: avoid `trust_remote_code`: copy the model classes from `pipeline_utils.py` (MIT), build WavLM-large from its config only (`WavLMConfig` of `microsoft/wavlm-large`, then `WavLMModel(cfg)`), load the safetensors, normalise audio by the config's mean and std. The remote code would otherwise fetch the full WavLM-large weights first.
- **Sends outward**: only the downloads.
- **Do not install**: Transformers in the kit's Python; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| Multi-Attributes | Arousal, dominance, valence per utterance. | candidate | PyTorch and Transformers, 1274490516 bytes | Try it on labelled speech, with an accuracy check before any use. |
| Categorical | Angry, sad, happy, surprise, fear, disgust, contempt, neutral; competition F1 macro 0.31 (Test 3). | candidate | PyTorch and Transformers, 1274511016 bytes | Try it on labelled speech, beside the attribute model. |

## Tried

None yet: no part has been run here.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

No verdict: read from the cards, not run here. Trained on English podcast speech, so other languages are unvalidated. Revisit when a task needs speech emotion scores and labelled speech is at hand for an accuracy check.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[emotion2vec-emotion2vec-plus-large|emotion2vec/emotion2vec_plus_large]] (../references/emotion2vec-emotion2vec-plus-large.md): another speech-emotion model

## Sources

- [Desk check: speech emotion models](../../raw/repos/speech-emotion-models-desk-check-2026-11-23.md): cards, licences, categories, competition scores, the custom model code.
