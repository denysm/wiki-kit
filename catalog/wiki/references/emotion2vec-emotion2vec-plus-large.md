---
title: "emotion2vec/emotion2vec_plus_large"
category: reference
kind: model
areas: [live-speech-and-calls]
url: https://huggingface.co/emotion2vec/emotion2vec_plus_large
version: "6c303ba"
licence: other
desk_checked: 2026-11-23
sources:
  - raw/repos/speech-emotion-models-desk-check-2026-11-23.md
created: 2026-11-23
updated: 2026-11-23
tags: [catalog, card, area-live-speech-and-calls, kind-model, speech-emotion-recognition, emotion2vec, funasr, multilingual]
confidence: medium
volatility: warm
verified: 2026-11-23
---

# emotion2vec/emotion2vec_plus_large


## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Get a speech-emotion embedding to train a small classifier on your own labelled speech | `model.pt` through FunASR | live-speech-and-calls |

## Run it here

- **No clone.** Files at revision `6c303ba` through `huggingface_hub.snapshot_download` with `allow_patterns` (`config.yaml`, `configuration.json`, `model.pt`, `tokens.txt`), into a sandbox folder.
- **To try it**: a throwaway Python 3.12 venv with `funasr`, `torch`, `soundfile`; `AutoModel(model=<local folder>, disable_update=True, device="cpu")`, then `generate(wav, granularity="utterance")`.
- **Sends outward**: only the download; `disable_update=True` stops FunASR's version check.
- **Do not install**: FunASR in the kit's Python; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `model.pt` through FunASR | Nine labels with scores per utterance (angry, disgusted, fearful, happy, neutral, other, sad, surprised, unknown), or a frame or utterance embedding. | tried | FunASR and PyTorch, 1945790254 bytes; RTF 0.029–0.045 on an M4 CPU | The real task that would move it to `in use`: mood per speaker in a live call, after an accuracy check on labelled speech. |
| base and seed variants | Smaller models of the same series (fine-tuned on 4788 h and 201 h). | listed | FunASR | Read when the large model is too heavy for live use. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict


## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[3loi-ser-odyssey-baseline-wavlm|3loi Odyssey 2024 WavLM baselines]] (../references/3loi-ser-odyssey-baseline-wavlm.md): compared in the same trial
- [[salute-developers-gigaam|salute-developers/GigaAM]] (../references/salute-developers-gigaam.md): Russian emotion model, not yet run

## Sources

- [Desk check: speech emotion models](../../raw/repos/speech-emotion-models-desk-check-2026-11-23.md): card, licence, categories, files.
