---
title: "Desk check: speech emotion models emotion2vec+ large, Odyssey 2024 WavLM baselines, GigaAM-Emo"
source: https://huggingface.co/emotion2vec/emotion2vec_plus_large
type: repos
authors: ["emotion2vec authors", "3loi (Odyssey 2024 baseline)", "salute-developers"]
source_date: 2026-08-17
ingested: 2026-11-23
url: https://huggingface.co/emotion2vec/emotion2vec_plus_large
kind: model
version: "6c303ba / 50632bb / 00d0e12 / GigaAM 7447938"
licence: "FunASR model licence; MIT; MIT"
tags: [catalog, desk-check, kind-model, speech-emotion-recognition, emotion2vec, wavlm, msp-podcast, gigaam, russian]
summary: "Three speech-emotion model families read from their Hugging Face cards, API metadata and the GigaAM README on 2026-11-23: emotion2vec+ large (9 categories, ~300M, 42526 h pseudo-labelled fine-tuning, FunASR model licence), the Odyssey 2024 MSP-Podcast WavLM-large baselines (8 categories, and arousal/dominance/valence; MIT; competition F1 0.31–0.41), and GigaAM-Emo (Russian, MIT, weights only on the authors' CDN). Start: the owner's own review of open emotion models."
---

# Desk check: speech emotion models

Started from the owner's review of open emotion-AI models (voice and face), then each model's own card. Left out for this use by that review: audEERING and Vox-Profile (non-commercial), MERaLiON (own licence), NVIDIA Audio2Emotion (its licence forbids emotion recognition).

## emotion2vec+ large

- Page https://huggingface.co/emotion2vec/emotion2vec_plus_large, revision `6c303ba987b86b93193de93e34bb2b077a6bedc4`, created 2024-05-15, `lastModified` 2024-06-24, 7868 downloads.
- Licence: card header `license: other`, `license_name: model-license`, `license_link: https://github.com/alibaba-damo-academy/FunASR`.
- Card: "emotion2vec+ is a series of foundational models for speech emotion recognition (SER). We aim to train a "whisper" in the field of speech emotion recognition, overcoming the effects of language and recording environments through data-driven methods". "This version (emotion2vec_plus_large) uses a large-scale pseudo-labeled data for finetuning to obtain a large size model (~300M)". Fine-tuning data: seed 201 h, base 4788 h, large 42526 h.
- Categories: angry, disgusted, fearful, happy, neutral, other, sad, surprised, unknown (9).
- Files: `model.pt` 1945790254 bytes, `config.yaml`, `configuration.json`, `tokens.txt`. Runs through FunASR `AutoModel` from a local folder.

## Odyssey 2024 WavLM baselines (3loi)

- Categorical: https://huggingface.co/3loi/SER-Odyssey-Baseline-WavLM-Categorical, revision `50632bbc8b89cbaa45077f1404601d9776cfe387`, created 2024-03-07, 522 downloads; attributes: https://huggingface.co/3loi/SER-Odyssey-Baseline-WavLM-Multi-Attributes, revision `00d0e12ba9bf957f5aeea36e8663c8c61cb50ac9`. Licence `mit` in both headers; language `en`.
- Card: "The model was trained on MSP-Podcast for the Odyssey 2024 Emotion Recognition competition baseline". Categorical predicts "Angry", "Sad", "Happy", "Surprise", "Fear", "Disgust", "Contempt" and "Neutral"; F1 micro 0.327, macro 0.311 on Test 3, micro 0.409, macro 0.307 on Development. Attributes: `id2label` arousal, dominance, valence.
- Files: `model.safetensors` 1274511016 and 1274490516 bytes, `config.json`, `pipeline_utils.py` (custom `SERModel`: WavLM-large, attentive statistics pooling, one hidden layer). The custom code loads `microsoft/wavlm-large` weights on its own before the checkpoint; reading it, nothing else is fetched or run.

## GigaAM-Emo (salute-developers/GigaAM)

- Repository https://github.com/salute-developers/GigaAM, commit `7447938d791c4f3e643386ee22c33777004293a5` (pushed 2026-08-17), licence MIT ("2024/12 — MIT License").
- README: "2024/04 — GigaAM Release: GigaAM-CTC (SoTA Speech Recognition model for the Russian language), GigaAM-Emo"; usage `gigaam.load_model("emo")`, `model.get_probs(audio_path)`. Emo is built on the `v1` line.
- Weights: the package downloads `emo.ckpt` from `https://cdn.chatwm.opensmodel.sberdevices.ru/GigaAM` and checks an MD5 pinned in the code (`7ce76f9535cb254488985057c0d33006`). The official Hugging Face repository `ai-sage/GigaAM-v3` (branches main, e2e_rnnt, e2e_ctc, rnnt, ctc, ssl) has no emo model. On 2026-11-23 the CDN's certificate had expired (`notAfter=Nov 4 22:23:37 2026 GMT`), so the download fails verification.
