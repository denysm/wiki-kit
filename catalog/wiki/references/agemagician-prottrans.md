---
title: "agemagician/ProtTrans"
category: reference
kind: model
areas: [science]
science_sections: [protein-engineering-and-design, machine-learning-and-ai]
repo: agemagician/ProtTrans
version: "1.0"
licence: AFL-3.0
desk_checked: 2026-11-21
sources:
  - raw/repos/agemagician-prottrans-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-science, science-protein-engineering-and-design, science-machine-learning-and-ai, kind-model, protein-language-models, embeddings, huggingface, fine-tuning]
summary: "Six published protein language models (ProtT5-XL-UniRef50 and -BFD, ProtBert-BFD, ProtBert, ProtAlbert, ProtXLNet) plus two fine-tuned prediction heads, with weights on Hugging Face under Rostlab and 34 notebooks as the only entry points. The licence at the read tag is the Academic Free License v3.0, not the MIT that GitHub reports for the current default branch. Everything read is a candidate; nothing tried."
confidence: high
volatility: hot
verified: 2026-11-21
---

# agemagician/ProtTrans

> A collection of pretrained protein language models (kind `model`, version `1.0` read): T5, BERT, ALBERT and XLNet trained on UniRef and BFD, with the weights on Hugging Face under `Rostlab` and 34 notebooks as the only entry points — the repository ships no library and no scripts. Licence at this tag: Academic Free License v3.0 (`LICENSE.md`), which also covers the weights per the README; GitHub reports MIT for the current default branch, where the licence file is a different one.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn protein sequences into the strongest vectors this collection offers | `Rostlab/prot_t5_xl_uniref50` (ProtT5-XL-UniRef50) | science-machine-learning-and-ai |
| Embed sequences on a modest machine, with a 1.7 GB model instead of an 11.3 GB one | `Rostlab/prot_bert_bfd` (ProtBert-BFD) | science-machine-learning-and-ai |
| Get a first batch of embeddings running in a few cells | `Embedding/PyTorch/Basic/ProtBert-BFD.ipynb` | science-machine-learning-and-ai |
| Control tokenization and batching instead of using a pipeline | `Embedding/PyTorch/Advanced/ProtT5-XL-UniRef50.ipynb` | science-machine-learning-and-ai |
| Speed up embedding inference by exporting the model to ONNX | `Embedding/Onnx/ProtBert-BFD.ipynb` | science-machine-learning-and-ai |
| Use the smallest published model when the download budget is tight | `Rostlab/prot_albert` (ProtAlbert) | science-machine-learning-and-ai |
| Fine-tune a protein language model on a labelled task of your own | `Fine-Tuning/ProtBert-BFD-FineTune-SS3.ipynb`, `Fine-Tuning/ProtBert-BFD-FineTuning-MS.ipynb`, `Fine-Tuning/ProtBert-BFD-FineTuning-PyTorchLightning-Localization.ipynb`, `Fine-Tuning/ProtBert-BFD-FineTuning-PyTorchLightning-MS.ipynb` | science-machine-learning-and-ai |
| Predict three-state secondary structure for a sequence, without training anything | `Rostlab/prot_bert_bfd_ss3` and `Rostlab/prot_bert_bfd_membrane` | science-protein-engineering-and-design |
| Tell a membrane-bound protein from a water-soluble one | `Prediction/ProtBert-BFD-Predict-SS3.ipynb`, `Prediction/ProtBert_BFD_Predict_MS.ipynb` | science-protein-engineering-and-design |
| Generate new protein sequences from a language model | `Rostlab/prot_xlnet` (ProtXLNet) | science-protein-engineering-and-design |
| See which residues a protein model attends to | `Visualization/ProtBert_attention_head_view.ipynb` | science-protein-engineering-and-design |
| Compare a BFD-trained model against a UniRef-trained one on the same task | `Rostlab/prot_t5_xl_bfd` (ProtT5-XL-BFD) | science-machine-learning-and-ai |
| Measure how fast one of these models runs on this machine | `Benchmark/ProtBert.ipynb` | science-machine-learning-and-ai |

## Run it here

- **Clone**: `git clone --depth 1 --branch 1.0 https://github.com/agemagician/ProtTrans $EXTERNAL/ProtTrans`, read-only. Never edit the clone.
- **Version**: `1.0`, the only tag and the only release, published 2021-03-24 under the name "Outperforming MSA Methods". The default branch is four years ahead of it (last push 2025-05-22) and was not read here beyond its licence and README. Before relying on this card: `gh api repos/agemagician/ProtTrans --jq .pushed_at` and `gh api repos/agemagician/ProtTrans/license --jq .license.spdx_id`.
- **Read**: `$EXTERNAL/ProtTrans/README.md` for the model and results tables, then the notebook for the task. There is no library to import: the repository is a README plus 34 notebooks.
- **Licence**: treat the weights as Academic Free License v3.0, which is what the README states on this tag and on the default branch alike; the MIT that GitHub reports covers the current repository code, whose licence file does not exist at this tag. Check the terms before anything built on these models leaves the machine.
- **Switch off**: nothing in the repository itself. Running a notebook downloads weights from Hugging Face (`Rostlab/…`), and the ProtElectra and Benchmark notebooks download from Dropbox links instead. Every notebook carries a Colab badge; open it locally, not in the hosted notebook, so the sequences stay here.
- **Do not install**: the `!pip install` lines inside the notebooks (`transformers`, `SentencePiece`, `biopython`, `onnxruntime-gpu==1.4.0`, `onnxruntime-tools==1.4.2`, `bertviz`, PyTorch Lightning). A trial belongs in a throwaway environment; real installation waits for the user's yes.
- **No part is in use.** Nothing here has been run; every size below is a Hugging Face file size read on 2026-11-21, and every quality number is the repository's own.

## What's inside

Parts are the model families and their variants, plus the notebooks that are this repository's entry points. Quality figures are the README's: Q3 and Q8 are secondary-structure accuracy on CASP12 / TS115 / CB513, Q2 and Q10 are DeepLoc.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `Rostlab/prot_t5_xl_uniref50` (ProtT5-XL-UniRef50) | T5 trained on UniRef50 and the best model in the repository's tables: Q3 81 / 87 / 86, Q8 70 / 77 / 74, Q2 91, Q10 81. For embeddings only the encoder is loaded. | candidate | `pytorch_model.bin` 11275562724 bytes (11.3 GB); `T5EncoderModel` plus SentencePiece; a GPU to be practical — the notebook says encoder-only "reduces the inference speed and the GPU memory requirements by half" | Try it on the first task where embedding quality decides the outcome and 11.3 GB of download is acceptable. |
| `Rostlab/prot_t5_xl_bfd` (ProtT5-XL-BFD) | The same T5 trained on BFD: Q3 77 / 85 / 84, Q2 91, Q10 77. | candidate | `pytorch_model.bin` 11275562268 bytes (11.3 GB), or `tf_model.h5` 11276359672 bytes (11.3 GB) for the TensorFlow path | Try it only as the BFD counterpart in a comparison against the UniRef50 model. |
| `Rostlab/prot_bert_bfd` (ProtBert-BFD) | BERT trained on BFD and the workhorse of this repository's notebooks: Q3 76 / 84 / 83, Q8 65 / 73 / 70, Q2 89, Q10 74. | candidate | `pytorch_model.bin` 1684058277 bytes (1.7 GB), or `tf_model.h5` 1848572328 bytes (1.8 GB); `transformers`, `do_lower_case=False` | Try it first: it is the cheapest download that still ranks high, and most notebooks here already use it. |
| `Rostlab/prot_bert` (ProtBert) | BERT trained on UniRef100: Q3 75 / 83 / 81, Q2 89, Q10 74. The model of the attention-visualization notebook. | candidate | `pytorch_model.bin` 1684058277 bytes (1.7 GB) | Try it when a UniRef-trained BERT is wanted next to the BFD one, or to visualize attention. |
| `Rostlab/prot_albert` (ProtAlbert) | ALBERT: Q3 74 / 82 / 79, Q2 88, Q10 74. The smallest published download. | candidate | `pytorch_model.bin` 897396780 bytes (897 MB) | Try it when the download or the memory budget rules out the BERT models. |
| `Rostlab/prot_xlnet` (ProtXLNet) | XLNet, the only autoregressive model published here and so the only one that generates sequences: Q3 73 / 81 / 78, Q2 87, Q10 68. | candidate | `pytorch_model.bin` 1637757076 bytes (1.6 GB); `XLNetLMHeadModel` for generation | Try it when sequences have to be generated rather than embedded. |
| `Rostlab/prot_bert_bfd_ss3` and `Rostlab/prot_bert_bfd_membrane` | Fine-tuned heads on ProtBert-BFD, not in the README's table: three-state secondary structure, and membrane-bound against water-soluble. | candidate | 1676061559 bytes (1.7 GB) and 1680256245 bytes (1.7 GB); `transformers` token-classification pipeline | Try one when a quick structural or localization label is wanted without training anything. |
| `ProtElectra-Generator`, `ProtElectra-Discriminator`, `ProtTXL`, `ProtTXL-BFD` | Announced in the README's table as "coming soon": no Hugging Face repository at this tag, though their scores are in the results tables (ProtElectra-Discriminator Q3 74 / 81 / 79, ProtTXL-BFD Q3 72 / 75 / 77). The notebooks fetch them from Dropbox links instead. | listed | Whatever the Dropbox copy holds; not checked | Read when one of these four is named in a paper, or when the default branch is checked for a published Hugging Face repository. |
| `Embedding/PyTorch/Basic/ProtBert-BFD.ipynb` | Shortest path to vectors: a `feature-extraction` pipeline over ProtBert-BFD, with rare amino acids mapped to X and the special tokens stripped afterwards. | candidate | `transformers`, PyTorch, the 1.7 GB download; it passes `device=0`, so a CUDA GPU unless that line is changed | Try it on the first set of sequences that has to become vectors here. |
| `Embedding/PyTorch/Basic/ProtAlbert.ipynb`, `Embedding/PyTorch/Basic/ProtBert.ipynb`, `Embedding/PyTorch/Basic/ProtElectra.ipynb`, `Embedding/PyTorch/Basic/ProtXLNet.ipynb` | The same basic shape for the other models; the ProtElectra one downloads its weights from Dropbox. | listed | As the basic ProtBert-BFD notebook, with that model's download | Read the one for a model after choosing it. |
| `Embedding/PyTorch/Advanced/ProtT5-XL-UniRef50.ipynb` | Encoder-only embedding with explicit tokenization, batching and a `torch.no_grad()` pass; removes `<pad>` and `</s>` positions. Notes that the encoder halves memory and that a newer `transformers` than the pinned one is required. | candidate | The 11.3 GB download, SentencePiece, `transformers`; runs on CPU if no CUDA device is present | Try it when the T5 model is the one chosen and the pipeline shortcut is too coarse. |
| `Embedding/PyTorch/Advanced/ProtAlbert.ipynb`, `Embedding/PyTorch/Advanced/ProtBert-BFD.ipynb`, `Embedding/PyTorch/Advanced/ProtBert.ipynb`, `Embedding/PyTorch/Advanced/ProtElectra.ipynb`, `Embedding/PyTorch/Advanced/ProtT5-XL-BFD.ipynb`, `Embedding/PyTorch/Advanced/ProtXLNet.ipynb` | The advanced shape for the other six models: explicit tokenization and batching instead of a pipeline. | listed | As above, with that model's download | Read the one for a model when its basic notebook is too coarse. |
| `Embedding/TensorFlow/Advanced/ProtAlbert.ipynb`, `Embedding/TensorFlow/Advanced/ProtBert-BFD.ipynb`, `Embedding/TensorFlow/Advanced/ProtBert.ipynb`, `Embedding/TensorFlow/Advanced/ProtT5-XL-BFD.ipynb`, `Embedding/TensorFlow/Advanced/ProtT5-XL-UniRef50.ipynb`, `Embedding/TensorFlow/Advanced/ProtXLNet.ipynb` | The TensorFlow equivalents, over the `tf_model.h5` files. | listed | TensorFlow and the `tf_model.h5` of that model | Read only if a task has to stay in TensorFlow; otherwise use the PyTorch notebooks. |
| `Embedding/Onnx/ProtBert-BFD.ipynb` | Exports ProtBert-BFD to ONNX, optimizes it, runs it through onnxruntime on the CUDA provider and compares speed and output against PyTorch float32 and half precision. Warns that the ONNX path "only works correctly with a single sequence per batch". | candidate | The 1.7 GB download, `onnxruntime-gpu==1.4.0` and `onnxruntime-tools==1.4.2` as pinned, `biopython`, a CUDA GPU | Try it when embedding throughput becomes the bottleneck and batches of one are acceptable. |
| `Fine-Tuning/ProtBert-BFD-FineTune-SS3.ipynb`, `Fine-Tuning/ProtBert-BFD-FineTuning-MS.ipynb`, `Fine-Tuning/ProtBert-BFD-FineTuning-PyTorchLightning-Localization.ipynb`, `Fine-Tuning/ProtBert-BFD-FineTuning-PyTorchLightning-MS.ipynb` | Fine-tune the whole model on a labelled task. The folder README: these fine-tune the whole model, not feature extraction, and "You must not freeze the pretrained models, otherwise, you will get worse results." | listed | Training hardware (not quantified in the repository), the 1.7 GB base model, PyTorch Lightning for two of the four | Read before any attempt to fine-tune rather than embed; only the folder README was read here. |
| `Prediction/ProtBert-BFD-Predict-SS3.ipynb`, `Prediction/ProtBert_BFD_Predict_MS.ipynb` | Ready-made prediction: a token-classification pipeline over the secondary-structure head, and the membrane counterpart. | candidate | The 1.7 GB head, `transformers`; `device=0`, so a GPU unless changed | Try the secondary-structure one on a sequence whose structure is known, to see how the output reads. |
| `Generate/ProtXLNet.ipynb` | Generates sequences with ProtXLNet (`max_length = 100` in the example), mapping rare amino acids to the unknown token. | candidate | The 1.6 GB download, `transformers`; GPU optional | Try it only when generation, not embedding, is the task. |
| `Visualization/ProtBert_attention_head_view.ipynb` | Renders ProtBert's attention heads inside the notebook with bertviz. | candidate | The 1.7 GB download, `bertviz` installed from its own repository, a notebook front end | Try it when a model's attention has to be shown to people rather than measured. |
| `Visualization/ProtAlbert_attention_head_view.ipynb`, `Visualization/ProtElectra_attention_head_view.ipynb`, `Visualization/ProtXLNet_attention_head_view.ipynb` | The same view for the other three models. | listed | As above, with that model's download | Read when the model to visualize is not ProtBert. |
| `Benchmark/ProtBert.ipynb` | Times inference over batch sizes 8 to 32 in steps of 8 and prints milliseconds per protein, on GPU or CPU; downloads the weights from Dropbox links rather than Hugging Face. | candidate | The download, PyTorch, and the device to be measured | Try it when a model's speed on this machine has to be known before a bulk run. |
| `Benchmark/ProtAlbert.ipynb`, `Benchmark/ProtElectra.ipynb`, `Benchmark/ProtXLNet.ipynb` | The same timing notebook for the other three models. | listed | As above | Read when timing a model other than ProtBert. |

## Tried

None yet.

## Verdict

A 2021 collection whose value today is the models, not the code: six published protein language models on Hugging Face, ranked against each other in the repository's own tables, with ProtT5-XL-UniRef50 ahead on every task and ProtBert-BFD the best ratio of score to download. The repository itself is thin — no library, no scripts, 34 notebooks pinned to libraries of that year, and four models still "coming soon" four years on. Two things decide its use here: the licence, Academic Free License v3.0 for the weights and for everything at this tag, which is not the MIT that GitHub reports for the current code; and the fact that the default branch is four years ahead of the only release. Revisit when a task needs protein embeddings and this collection has to be compared against a maintained one, when the licence matters for something that will leave the machine, or when the default branch is read and shows newer models or a changed licence statement.

## See Also

- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; scientific computation and data access
- [[area-science-machine-learning-and-ai|Machine learning and AI]] ([Machine learning and AI](../topics/area-science-machine-learning-and-ai.md)): section page; sequence embeddings, fine-tuning, inference speed
- [[area-science-protein-engineering-and-design|Protein engineering and design]] ([Protein engineering and design](../topics/area-science-protein-engineering-and-design.md)): section page; structure and localization prediction, sequence generation
- [[facebookresearch-esm|facebookresearch/esm]] (../references/facebookresearch-esm.md): the other collection of protein language models here, MIT but archived
- [[nvidia-bionemo-bionemo-recipes|NVIDIA-BioNeMo/bionemo-recipes]] (../references/nvidia-bionemo-bionemo-recipes.md): maintained recipes for training and serving protein models

## Sources

- [Desk check: agemagician/ProtTrans 1.0](../../raw/repos/agemagician-prottrans-desk-check-2026-11-21.md): the models and notebooks read from the clone, the Hugging Face file sizes, the licence checked at the tag and on the default branch, and what was not checked.
