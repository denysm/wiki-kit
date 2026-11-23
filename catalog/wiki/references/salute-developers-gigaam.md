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
---

# salute-developers/GigaAM


## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Label the emotion of Russian speech (angry, sad, neutral, positive) on this machine | GigaAM-Emo | live-speech-and-calls |
| Transcribe Russian speech, as a bench candidate against Whisper and Parakeet | GigaAM-v3 | live-speech-and-calls |

## Run it here

- **No clone.** `pip install git+https://github.com/salute-developers/GigaAM@7447938d791c4f3e643386ee22c33777004293a5` into a throwaway Python 3.12 venv; `gigaam.load_model("emo", download_root=<sandbox folder>)`.
- **Sends outward**: model downloads from `cdn.chatwm.opensmodel.sberdevices.ru`, checked by an MD5 pinned in the package; GigaAM-v3 also from `ai-sage/GigaAM-v3` on Hugging Face.
- **Certificate**: before every download check the CDN's certificate (`openssl s_client -connect cdn.chatwm.opensmodel.sberdevices.ru:443`, then `x509 -noout -dates`). On 2026-11-23 it had expired; the owner decided to fetch anyway, and the file was kept only because its MD5 matched the pinned one. Never keep a file whose MD5 does not match.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| GigaAM-v3 | Russian recognisers (CTC, RNN-T, end-to-end variants), on Hugging Face `ai-sage/GigaAM-v3`. | candidate | The package or Transformers with remote code | Try it in the speech-recognition bench on the owner's Russian recordings. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict


## See Also

- [[area-live-speech-and-calls|Live speech and calls]] ([Live speech and calls](../topics/area-live-speech-and-calls.md)): area page
- [[emotion2vec-emotion2vec-plus-large|emotion2vec/emotion2vec_plus_large]] (../references/emotion2vec-emotion2vec-plus-large.md): the multilingual model it would be compared with

## Sources

- [Desk check: speech emotion models](../../raw/repos/speech-emotion-models-desk-check-2026-11-23.md): README, licence, download host, certificate.
