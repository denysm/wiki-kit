---
title: "Desk check: agemagician/ProtTrans 1.0"
source: https://github.com/agemagician/ProtTrans/tree/1.0
type: repos
authors: ["Ahmed Elnaggar", "Michael Heinzinger", "Christian Dallago", "Ghalia Rehawi", "Yu Wang", "Llion Jones", "Tom Gibbs", "Tamas Feher", "Christoph Angerer", "Martin Steinegger", "Debsindhu Bhowmik", "Burkhard Rost"]
source_date: 2021-03-24
ingested: 2026-11-21
repo: agemagician/ProtTrans
kind: model
version: "1.0"
licence: AFL-3.0
tags: [catalog, desk-check, kind-model, protein-language-models, embeddings, huggingface, fine-tuning]
summary: "ProtTrans read from a read-only clone of tag 1.0: six published protein language models (ProtT5-XL-UniRef50 and -BFD, ProtBert-BFD, ProtBert, ProtAlbert, ProtXLNet) and four announced as coming soon, their Hugging Face weights and measured file sizes, the 34 notebooks that are the only entry points, and the licence question — the file at this tag is the Academic Free License v3.0 while GitHub reports MIT for the current default branch. Nothing was installed, no weights were downloaded."
---

# Desk check: agemagician/ProtTrans 1.0

Read from a clone of tag `1.0` (commit `235bb474305ec7c65d6a28bb91c54ab8dfddcbc8`, committed 2021-03-17) at `$EXTERNAL/ProtTrans`. The clone was not modified; nothing was installed, nothing was run, no weights were downloaded. Checked 2026-11-21. Version read by this desk check: 1.0.

## Repository facts

- What it is, in the README's words: "[ProtTrans](https://github.com/agemagician/ProtTrans/) is providing **state of the art pre-trained models for proteins**. ProtTrans was trained on **thousands of GPUs from Summit** and **hundreds of Google TPUs** using various **Transformers Models**."
- The repository holds no library and no scripts: at this tag it is a README, a licence file, an images folder and 34 Jupyter notebooks in seven folders (`Embedding/`, `Fine-Tuning/`, `Prediction/`, `Generate/`, `Visualization/`, `Benchmark/`). `.gitmodules` is empty. The models themselves are hosted elsewhere.
- **Where the weights are hosted**: Hugging Face, under the `Rostlab` organisation. The README's "Models Availability" table links one Hugging Face repository per model: `Rostlab/prot_t5_xl_uniref50`, `Rostlab/prot_t5_xl_bfd`, `Rostlab/prot_bert_bfd`, `Rostlab/prot_bert`, `Rostlab/prot_albert`, `Rostlab/prot_xlnet`. The notebooks load them by those names through `from_pretrained`. Two fine-tuned heads not in the table are used by the prediction notebooks: `Rostlab/prot_bert_bfd_ss3` and `Rostlab/prot_bert_bfd_membrane`.
- Four more models are announced but not published at this tag; the table's Pytorch column reads "coming soon" for `ProtElectra-Generator`, `ProtElectra-Discriminator`, `ProtTXL` and `ProtTXL-BFD`. The ProtElectra and Benchmark notebooks work around this by downloading `pytorch_model.bin`, `config.json` and `vocab.txt` from Dropbox links hard-coded in the notebook.
- **Licence, as read at this tag**: the file is `LICENSE.md` and its first line is `Academic Free License ("AFL") v. 3.0`. The README's License section says: "The ProtTrans pretrained models are released under the under terms of the [Academic Free License v3.0 License]".
- Requirements, from the README: "For protein feature extraction or fine-tuninng our pre-trained models, [Pytorch](https://github.com/pytorch/pytorch) and [Transformers](https://github.com/huggingface/transformers) library from huggingface is needed. For model visualization, you need to install [BertViz](https://github.com/jessevig/bertviz) library."
- Reported quality, from the README's own tables (its "Expected Results" section). Secondary structure Q3 (CASP12 / TS115 / CB513): ProtT5-XL-UniRef50 81 / 87 / 86, ProtT5-XL-BFD 77 / 85 / 84, ProtBert-BFD 76 / 84 / 83, ProtBert 75 / 83 / 81, ProtAlbert 74 / 82 / 79, ProtXLNet 73 / 81 / 78. Q8 (same sets): ProtT5-XL-UniRef50 70 / 77 / 74, ProtBert-BFD 65 / 73 / 70. Membrane-bound against water-soluble (Q2, DeepLoc): ProtT5-XL-UniRef50 and ProtT5-XL-BFD 91, ProtBert-BFD and ProtBert 89, ProtAlbert 88, ProtXLNet 87. Subcellular localization (Q10, DeepLoc): ProtT5-XL-UniRef50 81, ProtT5-XL-BFD 77, ProtBert-BFD, ProtBert and ProtAlbert 74, ProtXLNet 68.
- The paper behind the models is Elnaggar et al., "ProtTrans: Towards Cracking the Language of Life's Code Through Self-Supervised Deep Learning and High Performance Computing" (bioRxiv, 2020, doi 10.1101/2020.07.12.199554). Its abstract states the training scale: "up to 393 billion amino acids (words) from 2.1 billion protein sequences", on "936 nodes (total 5616 GPUs) and one TPU Pod (V3-512 or V3-1024)".

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/agemagician/ProtTrans`: `pushed_at` 2025-05-22T08:47:16Z, `archived: false`, licence reported by GitHub `MIT`, default branch `master`, 1323 stars.
- `gh api repos/agemagician/ProtTrans/releases/latest`: tag `1.0`, release name "Outperforming MSA Methods", published 2021-03-24T14:22:20Z. It is the only tag and the only release, so the clone is at the latest release while the default branch is four years ahead of it.
- Default branch head: commit `27c02f07e65feff8a3e7875f52b8b51225eb3c1c`, 2025-05-22T08:47:16Z.
- **Licence difference, checked both ways.** `gh api repos/agemagician/ProtTrans/license` reports `MIT License`, SPDX `MIT`, in a file at path `LICENSE`. That file does not exist at tag `1.0`: the clone has `LICENSE.md`, which is the Academic Free License v3.0. So the code licence on the current default branch is MIT, while the licence shipped with the release read here is AFL-3.0. The README's License section is unchanged on the default branch (fetched 2026-11-21): it still says the **pretrained models** are released under the Academic Free License v3.0. In other words: MIT applies to the repository's current code, AFL-3.0 to the weights, and AFL-3.0 to everything in this clone.
- Hugging Face metadata for the six model repositories was read on 2026-11-21 through `https://huggingface.co/api/models/<name>?blobs=true`. None of them carries a `license` field in its card metadata, so the licence statement for the weights is the one in this README.
- File sizes below are `size` values from that same API call, in bytes, read 2026-11-21. No weights were downloaded.

## How to run here

- **Clone**: `git clone --depth 1 --branch 1.0 https://github.com/agemagician/ProtTrans $EXTERNAL/ProtTrans`, read-only. Never edit the clone.
- **Read first**: `$EXTERNAL/ProtTrans/README.md` (the model table and the results tables), then the notebook for the task: `Embedding/PyTorch/Basic/<model>.ipynb` for a first run, `Embedding/PyTorch/Advanced/ProtT5-XL-UniRef50.ipynb` for the strongest model.
- **Telemetry and outbound calls**: none in the repository itself. Every notebook's first cells are `!pip install` lines and a `from_pretrained("Rostlab/…")` call, so running one downloads weights from Hugging Face; the ProtElectra and Benchmark notebooks download from Dropbox links instead. Each notebook also carries a Colab badge at the top: opening it there sends the data to a third party. There is nothing to switch off for a local run beyond not using Colab.
- **Do not install**: the `!pip install` lines inside the notebooks (`transformers`, `SentencePiece`, `biopython`, `onnxruntime-gpu==1.4.0`, `onnxruntime-tools==1.4.2`, `bertviz`, PyTorch Lightning in the fine-tuning notebooks). A trial belongs in a throwaway environment; real installation waits for the user's yes.
- **What a run takes**: PyTorch (or TensorFlow for the TensorFlow notebooks) plus `transformers`. The notebooks place the model on `cuda:0` when available (`device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')`) and fall back to CPU, except the pipeline-based ones, which pass `device=0` and therefore expect a GPU. The repository gives no VRAM figures; the only memory statement is the ProtT5 note below. Hardware facts in this desk check are download sizes and the repository's own statements.
- **What breaks without the plugin**: not applicable; this is not a plugin. Everything is a notebook read or run from the clone.

## Parts

Parts of this collection are its model families and variants, plus the entry points, which here are notebooks. Sizes are the Hugging Face `pytorch_model.bin` of each model, read 2026-11-21.

### Model: ProtT5-XL-UniRef50 (`Rostlab/prot_t5_xl_uniref50`)

- The strongest model in the README's tables: Q3 81 / 87 / 86, Q8 70 / 77 / 74, Q2 91, Q10 81. A T5 encoder-decoder trained on UniRef50.
- The advanced notebook's Important Notes: "ProtT5-XL-UniRef50 has both encoder and decoder, for feature extraction we only load and use the encoder part"; "Loading only the encoder part, reduces the inference speed and the GPU memory requirements by half"; "In order to use ProtT5-XL-UniRef50 encoder, you must install the latest huggingface transformers version from their GitHub repo"; "If you are intersted in both the encoder and decoder, you should use T5Model rather than T5EncoderModel."
- Needs: `pytorch_model.bin` 11275562724 bytes (11.3 GB); `T5Tokenizer` with SentencePiece; `T5EncoderModel` for embeddings. The repository also hosts two intermediate checkpoints of the same size, `pytorch_model_600k.bin` (11275562604 bytes) and `pytorch_model_723k.bin` (11275562628 bytes).
- Notable: this is the model that the release name "Outperforming MSA Methods" refers to.

### Model: ProtT5-XL-BFD (`Rostlab/prot_t5_xl_bfd`)

- Same architecture trained on BFD instead of UniRef50; Q3 77 / 85 / 84, Q2 91, Q10 77.
- Needs: `pytorch_model.bin` 11275562268 bytes (11.3 GB), or `tf_model.h5` 11276359672 bytes (11.3 GB) for the TensorFlow notebooks.

### Model: ProtBert-BFD (`Rostlab/prot_bert_bfd`)

- BERT trained on BFD; the model used by most notebooks in this repository (25 of the `Rostlab/…` references in the clone). Q3 76 / 84 / 83, Q8 65 / 73 / 70, Q2 89, Q10 74.
- Needs: `pytorch_model.bin` 1684058277 bytes (1.7 GB), or `tf_model.h5` 1848572328 bytes (1.8 GB). Loaded with `BertTokenizer`/`AutoTokenizer` with `do_lower_case=False`.
- Notable: the ONNX and fine-tuning paths are built around this model.

### Model: ProtBert (`Rostlab/prot_bert`)

- BERT trained on UniRef100; Q3 75 / 83 / 81, Q2 89, Q10 74. The model of the attention-visualization notebook.
- Needs: `pytorch_model.bin` 1684058277 bytes (1.7 GB).

### Model: ProtAlbert (`Rostlab/prot_albert`)

- ALBERT; Q3 74 / 82 / 79, Q2 88, Q10 74. The smallest download of the published set.
- Needs: `pytorch_model.bin` 897396780 bytes (897 MB).

### Model: ProtXLNet (`Rostlab/prot_xlnet`)

- XLNet, the only autoregressive model published here, so the only one that generates sequences; Q3 73 / 81 / 78, Q2 87, Q10 68.
- Needs: `pytorch_model.bin` 1637757076 bytes (1.6 GB); `XLNetTokenizer`, and `XLNetLMHeadModel` for generation.

### Models: fine-tuned heads `Rostlab/prot_bert_bfd_ss3` and `Rostlab/prot_bert_bfd_membrane`

- Not in the README's model table; used by the two notebooks in `Prediction/`. `prot_bert_bfd_ss3` predicts three-state secondary structure through `AutoModelForTokenClassification`; the notebook adds that free prediction is also possible on the model's Hugging Face page. `prot_bert_bfd_membrane` is the membrane-bound against water-soluble head.
- Needs: `pytorch_model.bin` 1676061559 bytes (1.7 GB) for the secondary-structure head and 1680256245 bytes (1.7 GB) for the membrane head.

### Models announced, not published at this tag: ProtElectra-Generator, ProtElectra-Discriminator, ProtTXL, ProtTXL-BFD

- The README's table reads "coming soon" for all four, and no `Rostlab/prot_electra…` or `…txl…` name appears anywhere in the clone. Their numbers are nevertheless in the results tables (for example ProtElectra-Discriminator Q3 74 / 81 / 79, ProtTXL-BFD Q3 72 / 75 / 77).
- The ProtElectra notebooks fetch generator and discriminator weights and configs from Dropbox links hard-coded in the notebook, so the published route for these four is the Dropbox copy, not Hugging Face.

### Entry point: `Embedding/PyTorch/Basic/ProtBert-BFD.ipynb`

- The shortest path to vectors: `!pip install -q transformers`, then `AutoTokenizer.from_pretrained("Rostlab/prot_bert_bfd", do_lower_case=False)`, `AutoModel.from_pretrained("Rostlab/prot_bert_bfd")`, then a `feature-extraction` pipeline with `device=0`. The notebook maps rare amino acids ("U,Z,O,B") to "X", inserts spaces between residues, and shows how to drop the padding and the `[CLS]`/`[SEP]` tokens afterwards.
- Needs: `transformers`, PyTorch, the 1.7 GB download; `device=0` means a CUDA GPU unless the line is changed.

### Entry points: the other four basic embedding notebooks

- `Embedding/PyTorch/Basic/ProtAlbert.ipynb`, `ProtBert.ipynb`, `ProtElectra.ipynb`, `ProtXLNet.ipynb`. The same shape as the ProtBert-BFD one, with that model's tokenizer and class; not opened beyond the ProtElectra one's download cells.

### Entry point: `Embedding/PyTorch/Advanced/ProtT5-XL-UniRef50.ipynb`

- The encoder-only path for the strongest model: `!pip install -q SentencePiece transformers`, `T5Tokenizer.from_pretrained("Rostlab/prot_t5_xl_uniref50", do_lower_case=False)`, `T5EncoderModel.from_pretrained(…)`, `model.to(device)` with a CPU fallback, `tokenizer.batch_encode_plus(..., add_special_tokens=True, padding=True)`, then a `torch.no_grad()` forward pass and removal of `<pad>` and `</s>` positions.
- Needs: the 11.3 GB download, `transformers` from the project's GitHub at the time (the note above), SentencePiece, and a GPU to be practical; the notebook runs on CPU if no CUDA device is present.

### Entry points: the other six advanced PyTorch notebooks

- `Embedding/PyTorch/Advanced/ProtAlbert.ipynb`, `ProtBert-BFD.ipynb`, `ProtBert.ipynb`, `ProtElectra.ipynb`, `ProtT5-XL-BFD.ipynb`, `ProtXLNet.ipynb`: the same advanced shape per model, with explicit tokenization and batching rather than a pipeline. Not opened.

### Entry points: `Embedding/TensorFlow/Advanced/` (six notebooks)

- `ProtAlbert.ipynb`, `ProtBert-BFD.ipynb`, `ProtBert.ipynb`, `ProtT5-XL-BFD.ipynb`, `ProtT5-XL-UniRef50.ipynb`, `ProtXLNet.ipynb`: the TensorFlow equivalents, which use the `tf_model.h5` files. Not opened.

### Entry point: `Embedding/Onnx/ProtBert-BFD.ipynb`

- Converts ProtBert-BFD to ONNX with `transformers.convert_graph_to_onnx`, optimizes the graph, runs it through `onnxruntime` with the `CUDAExecutionProvider`, and compares speed and output against PyTorch in float32 and in half precision (`model.half()`).
- The notebook's Important Notes: "The current onnx implementation only works correctly with a single sequence per batch. It will work with many sequences per batch, but the results will be different from the original pytorch implementation."
- Needs: the 1.7 GB download, `onnxruntime-gpu==1.4.0` and `onnxruntime-tools==1.4.2` as pinned in the notebook, `biopython`, and a CUDA GPU for the provider it selects.

### Entry points: `Fine-Tuning/` (four notebooks and a README)

- `ProtBert-BFD-FineTune-SS3.ipynb`, `ProtBert-BFD-FineTuning-MS.ipynb`, `ProtBert-BFD-FineTuning-PyTorchLightning-Localization.ipynb`, `ProtBert-BFD-FineTuning-PyTorchLightning-MS.ipynb`. The notebooks were not opened; the folder README was read in full: "This are examples for fine-tuning the whole pretrained models, and not feature extraction"; "You must not freeze the pretrained models, otherwise, you will get worse results."; "Applying hyperparameter search (learning rate, seed, number of epochs, etc.) should give you better results than the mentioned results."
- Needs: training hardware, which the repository does not quantify, plus the 1.7 GB base model and PyTorch Lightning for two of the four.

### Entry points: `Prediction/` (two notebooks)

- `ProtBert-BFD-Predict-SS3.ipynb` was read: it builds a `TokenClassificationPipeline` over `Rostlab/prot_bert_bfd_ss3` with `device=0` and predicts three-state secondary structure for a spaced sequence. `ProtBert_BFD_Predict_MS.ipynb` is the membrane-bound against water-soluble counterpart over `Rostlab/prot_bert_bfd_membrane`; it was not opened.
- Needs: the 1.7 GB head, `transformers`, and a GPU unless `device` is changed.

### Entry point: `Generate/ProtXLNet.ipynb`

- Generates protein sequences with `XLNetLMHeadModel` over `Rostlab/prot_xlnet`, with `max_length = 100` in the example; maps rare amino acids to the unknown token and moves the model to the GPU when one is present.
- Needs: the 1.6 GB download and `transformers`.

### Entry points: `Visualization/` (four notebooks)

- `ProtBert_attention_head_view.ipynb` was read: it loads `Rostlab/prot_bert` with `output_attentions=True` and renders the attention heads with `bertviz`'s `head_view` inside the notebook. `ProtAlbert_attention_head_view.ipynb`, `ProtElectra_attention_head_view.ipynb` and `ProtXLNet_attention_head_view.ipynb` are the same for the other models; not opened.
- Needs: the model download, `bertviz` (installed from its own repository), and a notebook front end to display the view.

### Entry points: `Benchmark/` (four notebooks)

- `ProtBert.ipynb` was read: it downloads `pytorch_model.bin`, `bert_config.json` and `vocab.txt` from Dropbox links, loads the model from the local folder, and times inference over batch sizes from 8 to 32 in steps of 8, printing milliseconds per protein for a given sequence length, on GPU or CPU. `ProtAlbert.ipynb`, `ProtElectra.ipynb` and `ProtXLNet.ipynb` do the same for the other models; not opened.
- Needs: the download, PyTorch, and whichever device is to be measured. This is the one place in the repository that measures speed, and it measures it on the machine that runs it, so it produces no numbers to quote here.

## Status reasons

- No part is rejected, and nothing from this repository has been used in real work, so no part is `tried` or `in use`.
- `listed` rather than `candidate`: every notebook that was not opened (the four other basic embedding notebooks, the six other advanced PyTorch notebooks, the six TensorFlow notebooks, the four fine-tuning notebooks, the second prediction notebook, the three other visualization notebooks, the three other benchmark notebooks) and the four models announced as "coming soon".
- The licence is the fact to carry into any decision: at this tag everything is AFL-3.0, and the weights are AFL-3.0 by the README's own statement, on both this tag and the current default branch. AFL-3.0 is not MIT; it carries patent and attribution terms, and the GitHub-reported MIT applies to the current code only.

## Not checked

- No weights were downloaded and nothing was run, so there is no measurement of speed, memory or quality here; every number above is the repository's own or a file size from the Hugging Face API.
- The current default branch was not read beyond its licence file and its README's License section: its notebooks, which are four years newer than this tag, were not compared with the ones read here.
- Whether the Dropbox links in the ProtElectra and Benchmark notebooks still resolve was not checked.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 50 model calls on opus, $5.96 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
