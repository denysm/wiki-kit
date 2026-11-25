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
summary: "A multilingual speech-emotion foundation model (~300M, nine categories, fine-tuned on 42526 h of pseudo-labelled speech) run through FunASR. Read from the card and API metadata; not run here."
---

# emotion2vec/emotion2vec_plus_large

> A Hugging Face model (kind `model`, licence `other`: the FunASR model licence linked from the card, revision `6c303ba` read): emotion2vec+ large, a speech-emotion recogniser meant to work across languages and recording conditions, with nine categories. Not run here.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Label the emotion of an utterance, in Russian or English, on this machine | `model.pt` through FunASR | live-speech-and-calls |
| Get a speech-emotion embedding to train a small classifier on your own labelled speech | `model.pt` through FunASR | live-speech-and-calls |

## Run it here

- **No clone.** Files at revision `6c303ba` through `huggingface_hub.snapshot_download` with `allow_patterns` (`config.yaml`, `configuration.json`, `model.pt`, `tokens.txt`), into a sandbox folder.
- **To try it**: a throwaway Python venv with `funasr`, `torch`, `soundfile`; `AutoModel(model=<local folder>, disable_update=True, device="cpu")`, then `generate(wav, granularity="utterance")`.
- **Sends outward**: only the download; `disable_update=True` stops FunASR's version check.
- **Do not install**: FunASR in the kit's Python; real installation waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `model.pt` through FunASR | Nine labels with scores per utterance (angry, disgusted, fearful, happy, neutral, other, sad, surprised, unknown), or a frame or utterance embedding. | candidate | FunASR and PyTorch, 1945790254 bytes | Try it on labelled speech, with an accuracy check before any use. |
| base and seed variants | Smaller models of the same series (fine-tuned on 4788 h and 201 h). | listed | FunASR | Read when the large model is too heavy for live use. |

## Tried

None yet: no part has been run here.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

No verdict: read from the card, not run here. Revisit when a task needs speech emotion labels and labelled speech is at hand for an accuracy check.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[3loi-ser-odyssey-baseline-wavlm|3loi Odyssey 2024 WavLM baselines]] (../references/3loi-ser-odyssey-baseline-wavlm.md): another speech-emotion model
- [[salute-developers-gigaam|salute-developers/GigaAM]] (../references/salute-developers-gigaam.md): Russian emotion model, not yet run

## Sources

- [Desk check: speech emotion models](../../raw/repos/speech-emotion-models-desk-check-2026-11-23.md): card, licence, categories, files.
