---
title: "salute-developers/GigaAM"
category: reference
kind: library
areas: [live-speech-and-calls]
repo: salute-developers/GigaAM
version: "7447938"
licence: MIT
desk_checked: 2026-11-23
sources:
  - raw/repos/speech-emotion-models-desk-check-2026-11-23.md
created: 2026-11-23
updated: 2026-11-23
tags: [catalog, card, area-live-speech-and-calls, kind-library, gigaam, russian, speech-emotion-recognition, speech-to-text]
confidence: low
volatility: warm
verified: 2026-11-23
summary: "Sber's Conformer speech models for Russian (MIT): GigaAM-Emo for emotion and the GigaAM-v3 recognisers. Read from the README and the package; not run here. GigaAM-Emo's weights come only from the authors' CDN: check its certificate before every download and always the pinned MD5."
---

# salute-developers/GigaAM

> A Python package and model family (kind `library`, licence MIT, commit `7447938` read): Conformer models pre-trained on Russian speech, with GigaAM-Emo for emotion and GigaAM-v3 for recognition. Not run here.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Label the emotion of Russian speech (angry, sad, neutral, positive) on this machine | GigaAM-Emo | live-speech-and-calls |
| Transcribe Russian speech, as a bench candidate against Whisper and Parakeet | GigaAM-v3 | live-speech-and-calls |

## Run it here

- **No clone.** `pip install git+https://github.com/salute-developers/GigaAM@7447938d791c4f3e643386ee22c33777004293a5` into a throwaway Python venv; `gigaam.load_model("emo", download_root=<sandbox folder>)`.
- **Sends outward**: model downloads from `cdn.chatwm.opensmodel.sberdevices.ru`, checked by an MD5 pinned in the package; GigaAM-v3 also from `ai-sage/GigaAM-v3` on Hugging Face.
- **Certificate**: before every download check the CDN's certificate (`openssl s_client -connect cdn.chatwm.opensmodel.sberdevices.ru:443`, then `x509 -noout -dates`). Never keep a file whose MD5 does not match the one pinned in the package.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| GigaAM-Emo | Probabilities of four emotions per utterance (angry, sad, neutral, positive), built on the v1 encoder. | candidate | The package, PyTorch, `emo.ckpt` from the authors' CDN, MD5 `7ce76f9535cb254488985057c0d33006` | Try it on labelled or expressive Russian speech, with an accuracy check before any use. |
| GigaAM-v3 | Russian recognisers (CTC, RNN-T, end-to-end variants), on Hugging Face `ai-sage/GigaAM-v3`. | candidate | The package or Transformers with remote code | Try it in the speech-recognition bench on the owner's Russian recordings. |

## Tried

None yet: no part has been run here.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

No verdict: read from the README and the package, not run here. The only Russian-trained emotion model found; check the CDN's certificate and the pinned MD5 before any download.

## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[emotion2vec-emotion2vec-plus-large|emotion2vec/emotion2vec_plus_large]] (../references/emotion2vec-emotion2vec-plus-large.md): the multilingual model it would be compared with

## Sources

- [Desk check: speech emotion models](../../raw/repos/speech-emotion-models-desk-check-2026-11-23.md): README, licence, download host, certificate.
