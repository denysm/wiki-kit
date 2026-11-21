---
title: "Tool catalog vocabulary"
schema_state: advisory
created: 2026-11-21
updated: 2026-11-21
summary: "Vocabulary agents read before writing a card: area slugs, science sections, the seven statuses, Check when by status, kinds and what a part is per kind, the fourth column by kind, file naming. scripts/catalog_index.py reads the Areas and Science sections tables."
---

# Tool catalog vocabulary

> The vocabulary of the catalog. `scripts/catalog_index.py` parses the two tables "Areas" and "Science sections"; keep their columns. The rules behind them are in `docs/catalog-design.md`; the quality bar of a card is `docs/catalog-card-standard.md`.

## Areas

Areas are named by task, not by kind of tool. A card may sit in several (`areas:` in its frontmatter); a new area opens when a card fits none. Scope and neighbours go verbatim onto the generated area page, so they carry no numbers or dates.

| Slug | Title | Scope | Neighbours |
|------|-------|-------|------------|
| designing-something-new | Designing something new | Working out what to build before building it: design by interview, specifications, design reviews by fresh reviewers, decisions written down before code. | writing-code-with-agents, writing-documents-and-articles |
| writing-code-with-agents | Writing code with agents | Plans, plan execution, debugging, tests, code review, branches and code navigation when a coding agent writes the code. | designing-something-new, building-skills-and-plugins |
| building-skills-and-plugins | Building skills and plugins | Writing, testing and checking skills, plugins, agents and hooks for coding agents, and the checks that keep a skill collection healthy. | writing-code-with-agents, knowledge-bases |
| knowledge-bases | Knowledge bases | Agent-maintained Markdown knowledge bases: ingest, compile, query, lint, and search over the articles. | search-and-embeddings, converting-documents-and-recordings |
| search-and-embeddings | Search and embeddings | Local embedding models, the runtimes that serve them, and vector scoring or indexes for semantic search on one machine, with no data leaving it. | knowledge-bases, science |
| converting-documents-and-recordings | Converting documents and recordings | Turning office documents, PDFs, slides, audio and video into Markdown, plain text, transcripts or frames. | knowledge-bases, writing-documents-and-articles, live-speech-and-calls |
| writing-documents-and-articles | Writing documents and articles | Writing and editing prose for people: documents, articles, reports; removing the tells of machine-written text. | converting-documents-and-recordings, designing-something-new |
| building-interfaces-for-agents | Building interfaces for agents | Letting an agent show its results as a real user interface: generated layouts streamed by the agent and rendered with native components of the app. | writing-code-with-agents, designing-something-new, live-speech-and-calls |
| verifying-code | Verifying code | Machine-checked proofs that code, down to compiled machine code, meets a specification or a security property, and how proofs written by an AI are checked and trusted. | writing-code-with-agents, science |
| live-speech-and-calls | Live speech and calls | Capturing a call's sound and the microphone on one machine, detecting speech, recognising it as it is spoken, telling speakers apart, translating it and speaking text aloud, with no audio leaving the machine. | converting-documents-and-recordings, building-interfaces-for-agents |
| science | Science | Scientific computation and data access, split into the sections below: protein structure and design, cheminformatics, genomics, scientific databases and the rest. | search-and-embeddings |

## Science sections

Science is split by the skill categories of the K-Dense scientific-agent-skills README. They overlap; a part may sit in several. Other science tools go into the same sections through the card's `science_sections:` frontmatter or a Tasks it serves row whose Area is `science-<section slug>`. `README heading` is the category heading in that README without its emoji and count; `catalog_index.py` maps the parts list's README sections through it.

| Slug | Title | README heading |
|------|-------|----------------|
| bioinformatics-and-genomics | Bioinformatics and genomics | Bioinformatics & Genomics |
| cheminformatics-and-drug-discovery | Cheminformatics and drug discovery | Cheminformatics & Drug Discovery |
| proteomics-and-mass-spectrometry | Proteomics and mass spectrometry | Proteomics & Mass Spectrometry |
| clinical-research | Clinical research and evidence workflows | Clinical Research & Evidence Workflows |
| preclinical-research | Preclinical research and animal welfare | Preclinical Research & Animal Welfare |
| microscopy-and-imaging | Microscopy, medical imaging and digital pathology | Microscopy, Medical Imaging & Digital Pathology |
| neuroscience | Neuroscience and electrophysiology | Neuroscience & Electrophysiology |
| machine-learning-and-ai | Machine learning and AI | Machine Learning & AI |
| materials-chemistry-physics | Materials science, chemistry and physics | Materials Science, Chemistry & Physics |
| engineering-and-simulation | Engineering and simulation | Engineering & Simulation |
| chemical-oceanography | Chemical oceanography | Chemical Oceanography |
| data-analysis-and-visualization | Data analysis and visualization | Data Analysis & Visualization |
| laboratory-automation | Laboratory automation | Laboratory Automation |
| multi-omics-and-systems-biology | Multi-omics and systems biology | Multi-omics & Systems Biology |
| protein-engineering-and-design | Protein engineering and design | Protein Engineering & Design |
| scientific-communication | Scientific communication | Scientific Communication |
| scientific-databases | Scientific databases and data access | Scientific Databases & Data Access |
| infrastructure-and-platforms | Infrastructure and platforms | Infrastructure & Platforms |
| research-methodology | Research methodology and planning | Research Methodology & Planning |
| regulatory-and-standards | Regulatory and standards | Regulatory & Standards |

## Statuses

One status per part row, one of seven:

| Status | Meaning | Check when says |
|--------|---------|-----------------|
| `listed` | Taken from the repository's own metadata, not read by us | when to read it |
| `candidate` | Read by the desk check, not tried | the task to try it on |
| `tried` | Sandbox result in the Tried log, not yet in real use | the real task that would move it to `in use` |
| `in use` | In real work; how and which version: Run it here | what to re-check |
| `method taken` | The idea is in our own rules or scripts; the part itself is not run | when to re-read upstream (a new major version of the source) |
| `reference` | Read for ideas or as a baseline | when to consult it again |
| `rejected` | Decided against; reason in the row | the revisit condition |

After a desk check, parts read are `candidate` and parts taken only from metadata are `listed`; `rejected`, `reference` and `method taken` need a recorded reason in a raw file; `tried` and `in use` need a trial or use record in `raw/notes/trials/`.

## Kinds and parts

| Kind | A part is | Fourth column of What's inside |
|------|-----------|--------------------------------|
| `plugin` | each skill, command, agent and hook | `Without plugin` |
| `skill-collection` | each skill, command, agent and hook | `Without plugin` |
| `library` | a module or main entry point | `Needs` |
| `app` | a command or main function | `Needs` |
| `cli` | a command | `Needs` |
| `model` | a variant (size, quantization) | `Needs` |
| `runtime` | a backend | `Needs` |
| `pattern` | one of its main ideas | `Needs` |

`Without plugin`: does the part work when read from the clone without installing, and what breaks. `Needs`: what running the part takes here (nothing, a clone, a venv, a GPU and its memory, an API key, data leaving the machine).

## File naming

- Card: `wiki/references/<owner>-<repo>.md`, lowercase; a tool not on GitHub uses its project name (`ffmpeg-ffmpeg`, `ollama-ollama`); a Hugging Face model uses its organisation and model name.
- Desk check: `raw/repos/<owner>-<repo>-desk-check-<YYYY-MM-DD>.md` (`type: repos`).
- Parts list of a collection above 40 parts: `raw/data/<owner>-<repo>-parts-<version>.md` (`type: data`), written by `scripts/catalog_parts.py`.
- Trial or use record: `raw/notes/trials/<YYYY-MM-DD>-<tool>-<slug>.md` (`type: notes`).
- Retold measurement: `raw/notes/<YYYY-MM-DD>-measurements-<slug>.md` (`type: notes`).
- Generated pages: `wiki/topics/task-index.md`, `wiki/topics/area-<slug>.md`, `wiki/topics/area-science-<section slug>.md`.
