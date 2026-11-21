---
title: "K-Dense-AI/scientific-agent-skills"
category: reference
kind: skill-collection
areas: [building-skills-and-plugins, science]
repo: K-Dense-AI/scientific-agent-skills
version: "2.72.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/k-dense-ai-scientific-agent-skills-desk-check-2026-11-21.md
  - raw/data/k-dense-ai-scientific-agent-skills-parts-2.72.0.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-building-skills-and-plugins, area-science, kind-skill-collection, agent-skills, science, protein-design, scientific-databases, skill-ci, security-scan]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Agent Skills collection of 177 science and research skills, plus CI that validates every SKILL.md, guards bundled scripts with contract tests and scans skills weekly with an LLM-based scanner. Skills are read one by one from a clone, never installed. The kit took the spec validation into its own checks and rejected the PR scan for its CI; 23 sampled skills (protein design, scientific databases, deepchem, markitdown) are candidates, the rest are listed in a generated parts list."
---

# K-Dense-AI/scientific-agent-skills

> An Agent Skills collection (kind `skill-collection`, repository licence MIT, version `2.72.0` read): 177 science and research skills, each a `SKILL.md` with references and often scripts, across biology, chemistry, medicine, physics, engineering, data analysis and scientific writing. It also ships CI that validates every skill, tests bundled scripts and scans skills weekly with an LLM-based security scanner. Here skills are read from a clone one by one and nothing is installed; 23 skills were read, the rest are listed from their own frontmatter.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Check every `SKILL.md` in CI against the Agent Skills spec: name equals folder, quoted version, description says what and when, a warning past 500 lines | `skill-spec-validation.yml` (method taken: the kit's `scripts/skill_check.py`) | building-skills-and-plugins |
| Fail a pull request when a skill ships scripts without tests or a declared environment; check links, script syntax and hardcoded local paths without importing skill code | `skill-tests.yml` | building-skills-and-plugins |
| Scan a skill collection weekly for prompt injection, data exfiltration and malicious code, and publish findings per skill | `security-scan.yml` | building-skills-and-plugins |
| Check a third-party skill's security findings before reading or trying it | `security-scan.yml` | building-skills-and-plugins |
| Write rules for skill authors: allowed frontmatter fields, runtime needs in `compatibility`, one test environment per skill | `AGENTS.md` | building-skills-and-plugins |
| Make a skill collection loadable by Codex, Cursor and other Agent Plugins clients, with pinned installs | `plugin.json` | building-skills-and-plugins |
| Not this: block pull requests on an LLM security scan of changed skills in the kit's own CI. Rejected: the kit's `leak_check.py` and `raw_check.py` cover what the kit ships | `pr-skill-scan.yml` | building-skills-and-plugins |
| Embed protein sequences, generate sequences, or fold a sequence with ESM3, ESMC or ESMFold2, locally or hosted | `esm` | science-protein-engineering-and-design |
| Run AlphaFold, Boltz, RFdiffusion, ProteinMPNN or docking in the cloud without a local GPU | `tamarind` | science-protein-engineering-and-design |
| Order wet-lab measurements of designed protein sequences (binding, thermostability, expression) | `adaptyv` | science-protein-engineering-and-design |
| Find N-glycosylation sites in a protein and plan glycosylation changes, keeping motif, prediction and evidence apart | `glycoengineering` | science-protein-engineering-and-design |
| Validate cryo-EM particle STAR files and run RELION refinement and half-map postprocessing | `relion` | science-protein-engineering-and-design |
| Fetch a fact reproducibly from a named public database (PubChem, ChEMBL, UniProt, AlphaFold DB, ClinicalTrials.gov and others) with endpoints, counts and provenance | `database-lookup` | science-scientific-databases |
| Look up cancer cell-line gene dependencies or drug sensitivity from a DepMap release | `depmap` | science-scientific-databases |
| Get ClinGen gene-disease validity and public evidence for one germline variant | `folklore-variant-evidence` | science-scientific-databases |
| Find and download public cancer radiology or pathology images | `imaging-data-commons` | science-scientific-databases |
| Query gene, drug, disease and phenotype associations and short paths in a local knowledge graph | `primekg` | science-scientific-databases |
| Query typed biomedical knowledge-graph relationships with publication provenance | `ncats-arax` | science-scientific-databases |
| Pull U.S. Treasury fiscal data: debt, statements, auctions, rates | `usfiscaldata` | science-scientific-databases |
| Choose a scientific dataset, model or Space on Hugging Face | `hugging-science` | science-scientific-databases |
| Find which 1000 Genomes individuals carry variants in a gene or region | `onekgpd` | science-scientific-databases |
| Predict promoters, splice sites, enhancers or expression from a DNA sequence with hosted models | `genomic-intelligence` | science-scientific-databases |
| Look up or score the regulatory effect of a human variant with AlphaGenome | `alphagenome` | science-scientific-databases |
| Turn free-text labels into checked ontology term IDs, or validate existing ones | `ontology-term-resolution` | science-scientific-databases |
| See which viral lineages circulate now, how fast they grow and which mutations they carry | `pathogen-variant-surveillance` | science-scientific-databases |
| Parse sequence files, query NCBI Entrez or run BLAST from Python | `biopython` | science-scientific-databases |
| Map identifiers and pull annotations across UniProt, KEGG, ChEMBL and Reactome from Python | `bioservices` | science-scientific-databases |
| Quick gene, sequence, structure or enrichment lookups from the command line | `gget` | science-scientific-databases |
| Predict molecular properties (ADMET, toxicity, solubility) with DeepChem and MoleculeNet | `deepchem` | science-cheminformatics-and-drug-discovery |
| Convert office documents and PDFs to Markdown for analysis or retrieval | `markitdown` | science-scientific-communication |

## Run it here

- **Clone**: `git clone --depth 1 --branch v2.72.0 https://github.com/K-Dense-AI/scientific-agent-skills $EXTERNAL/scientific-agent-skills`, read-only. Never edit the clone.
- **Version**: `2.72.0`, the latest release, published 2026-10-01. On 2026-11-21 main was 8 commits ahead, changing only the README and the weekly security report; no skill changed. Before relying on this card: `gh api repos/K-Dense-AI/scientific-agent-skills --jq .pushed_at` and `gh api repos/K-Dense-AI/scientific-agent-skills/releases/latest --jq .tag_name`.
- **Read**: `$EXTERNAL/scientific-agent-skills/skills/<skill>/SKILL.md`, then its `compatibility` field and its `references/`. To find a skill by task, search the parts list (each part with its README categories). Before trying a skill, read its row in `docs/security-report.md`. The report at the tag lacks the 15 newest skills; for those and for current findings read the report on main: `gh api -H 'Accept: application/vnd.github.raw' 'repos/K-Dense-AI/scientific-agent-skills/contents/docs/security-report.md?ref=main'`.
- **Switch off**: the section "Citing Scientific Agent Skills" at the end of 137 of 177 `SKILL.md` files. It tells the agent to add the authors' paper to any manuscript, report, presentation or code release and to fetch arxiv.org first. Ignore it unless the user asks for the citation. Other outbound calls belong to each skill's own service (the Without plugin column names it): send only public, non-sensitive queries, and read credentials one key at a time from the environment.
- **Do not install**: the collection in any form (`npx skills add`, `gh skill install`, the Agent Plugins package, a clone into an `.agents/skills/` folder). Its own README says "Do not install everything at once". There are no hooks, commands or agents, so nothing loads into a session by itself. The risk is dependencies: skill pins conflict, so never run `uv sync` or install skill packages into a shared environment. A trial is one throwaway `uv` environment for one skill in a scratch folder, after the user's yes.
- **In use**: nothing.

## What's inside

Parts: 177 skills in `skills/`, no hooks, commands or agents, plus the repository tooling that checks them. The table holds the six tooling parts and the 23 skills the desk check read: the README categories Protein Engineering & Design and Scientific Databases & Data Access, the three multi-database packages that category names, and the skills named after tools with their own card here. The other 154 skills are `listed` in the [parts list](../../raw/data/k-dense-ai-scientific-agent-skills-parts-2.72.0.md) with their README categories.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `skill-spec-validation.yml` | CI on every skill: `skills-ref validate` (six allowed frontmatter fields, `name` equals folder, length limits, no JSON-style YAML), then repo rules: `metadata.version` required, string `metadata` values, a warning past 500 lines. | method taken | Not run here; it needs uv, Python `3.13` and the repo's dev tools. The kit does the same checks in its own words with a stdlib-only `scripts/skill_check.py` in `checks.yml`. | Re-read on a new major version, or when the Agent Skills spec changes its frontmatter fields. |
| `skill-tests.yml` with `tests/_meta` | CI guard that parses every skill without importing it: frontmatter, length, local links, script syntax, no bytecode, no hardcoded local paths, no `eval`/`exec`/`os.system`; fails when a skill ships `scripts/` without a suite and a `tests/skill-requirements.toml` entry; runs standard-library suites in throwaway environments. | candidate | Readable from the clone; running it needs uv and Python `3.13`, no scientific packages. | Try it when the kit adds contract tests for its own scripts (`--help` works, output format holds). |
| `security-scan.yml` with `scan_skills.py` and `docs/security-report.md` | Weekly Cisco AI Defense Skill Scanner run (LLM, behavioral and trigger analyzers) over every skill; unchanged skills reuse their findings, a full rescan runs when the last one is older than 30 days; the report lists severity and findings per skill. | candidate | The report is plain Markdown and needs nothing. Running the scan needs an LLM API key; skill content goes to the model provider. | Consult the report before trying any skill of this collection; take the report on main for current findings. |
| `pr-skill-scan.yml` with `scan_pr_skills.py` | Scans only the skills a pull request changes, fails on HIGH, posts a PR comment; skipped for forks with a note that a skip is not a pass. | rejected | Readable; running it needs the same LLM API key. | Rejected: an LLM scanner in the kit's own PR CI; the kit's `leak_check.py` and `raw_check.py` cover what the kit ships. Revisit when the kit starts shipping skills or scripts written by others. |
| `AGENTS.md` | Rules for skill authors: the six allowed frontmatter fields, runtime needs in `compatibility` (max 500 chars), block-style YAML, quoted `metadata` values, nested host blocks, one test environment per skill. | candidate | Plain text; needs nothing. | Try its rules when the kit next changes its skill frontmatter rules or adds a `compatibility` field. |
| `plugin.json` | Agent Plugins `1.0.0` manifest at the root: supporting clients load every `skills/*/SKILL.md` as one plugin; tagged releases allow pinned installs. | candidate | Matters only for installing; reading skills needs no manifest. | Try the same manifest shape when the kit's skills must load in Codex or Cursor as well. |
| `esm` | ESM3 generation, ESMC embeddings and ESMFold2 all-atom folding through Biohub's `esm` SDK, locally or hosted; keeps the older `fair-esm` apart (both import as `esm`). Ships a residue-pooling helper that loads no weights. | candidate | Works from the clone as text. Running needs its own Python `3.12` venv with `esm==3.4.1.post1` (Torch, Transformers), model weights and RAM or GPU memory; hosted calls send sequences to biohub.ai with `ESM_API_KEY`. The newest upstream scan marks it HIGH for PyTorch `.eval()` calls matched as `eval`. | Try it on embeddings for a few public sequences with `biohub/ESMC-300M` on CPU, in a throwaway venv. |
| `tamarind` | REST API and MCP server of a cloud platform that runs AlphaFold, Boltz, Chai, ESMFold, RFdiffusion, ProteinMPNN, BoltzGen, antibody design, DiffDock and Vina docking without a local GPU. | candidate | Works as text. Running needs an account and `TAMARIND_API_KEY`; sequences and files are uploaded to the vendor; free use is a monthly allowance. | Try it when a structure or design job needs a GPU this machine lacks and the inputs may leave it. |
| `adaptyv` | API and SDK of a cloud wet lab: submit designed protein sequences for binding, affinity, thermostability, expression or enzyme assays, track them and fetch results. | candidate | Works as text. Running needs an Adaptyv Foundry account and `ADAPTYV_API_KEY`; a submission sends sequences to the vendor and is priced. | Try the read-only target catalogue and cost estimate with the user before any real submission. |
| `glycoengineering` | Scans N-glycosylation sequons and S/T-rich regions locally, checks glycan evidence in GlyTouCan, prepares NetNGlyc, NetOGlyc and GlycoSHIELD runs; keeps motif, prediction, occupancy and structure apart. Licence "Unknown". | candidate | Local helpers need only Python 3.10+; GlyTouCan needs network; the predictors are web forms; GlycoSHIELD needs GROMACS. | Try the local sequon scan on a public protein sequence. |
| `relion` | Validates RELION STAR optics and particle stacks, then runs single-particle refinement, FSC and half-map postprocessing through `spa_workflow.py`. | candidate | Validation needs Python `3.12` with numpy, mrcfile and starfile; refinement needs RELION `5.0.1` executables with MPI and FFTW or MKL. Not in the upstream scan at the tag. | Try `validate-star` on a public particle set before any refinement. |
| `database-lookup` | One skill for 80 databases (PubChem, ChEMBL, UniProt, PDB, AlphaFold, KEGG, ClinVar, ClinicalTrials.gov, FRED, USPTO and more): a retrieval contract, bounded calls, responses treated as untrusted, endpoints, access date and count reconciliation in the result. | candidate | Works as text with `curl` or Python; network; keys only for some databases, read one at a time. Asks before more than 10,000 records or 100 calls. | Try it on the next fact that must come from a named public database. |
| `depmap` | Finds a DepMap release, checks file contracts, analyses Chronos gene effects, biomarkers, co-essentiality and PRISM drug sensitivity. Licence CC-BY-4.0. | candidate | A venv with numpy, pandas and scipy; network to depmap.org; recent files may need a browser download. | Try it when a question needs gene dependency in cancer cell lines. |
| `folklore-variant-evidence` | ClinGen gene-disease validity and source-linked public evidence for one GRCh38 germline variant, through a hosted MCP server; refuses patient data. | candidate | Network to `api.helena.bio`, no key; an MCP-capable host or `curl`. | Try it on one public variant when gene-disease validity is needed. |
| `imaging-data-commons` | Finds and downloads public cancer radiology and pathology data from NCI Imaging Data Commons with `idc-index`, metadata SQL, licences and citations; a hosted IDC MCP server complements it. | candidate | Network; `idc-index` in a venv; Google credentials only for BigQuery. Data licences vary (mostly CC-BY, some CC-NC). | Try it when a task needs public imaging data. |
| `primekg` | Queries a pinned PrimeKG CSV for typed gene, drug, disease and phenotype nodes, associations and one- or two-hop paths, with checksum and provenance. Licence "Unknown"; the dataset is CC0 1.0. | candidate | A venv with pandas; a downloaded `kg.csv` and several GB of RAM; queries then run offline. | Try it when a hypothesis needs graph paths between a gene and a disease. |
| `ncats-arax` | Bounded one-hop and pinned two-hop queries over NCATS Translator knowledge graphs with publication provenance; standard-library client. | candidate | Network to `arax.transltr.io`, no key. Queries may be publicly visible: public, non-sensitive questions only. | Try it on a public gene-to-disease relation that needs publication provenance. |
| `usfiscaldata` | U.S. Treasury Fiscal Data API: debt, daily and monthly statements, auctions, interest and exchange rates. | candidate | Network, no key; Python with requests and pandas, or R. | Try it when a task needs official U.S. federal finance figures. |
| `hugging-science` | Discovers and checks scientific datasets, models, posts and Spaces through the Hugging Science catalog. No `license` field. | candidate | Network; optional `HF_TOKEN` for gated resources; each resource needs its own runtime. | Try it when choosing a scientific model or dataset on Hugging Face. |
| `onekgpd` | Individual-level queries on the 1000 Genomes cohort (3,202 genomes, GRCh38): carriers, genotypes and relatedness, with population allele frequencies. | candidate | `uv run` with inline dependencies; network for variant queries, metadata offline; no key. | Try it when a question asks who in 1000 Genomes carries a variant. |
| `genomic-intelligence` | Hosted DNA language models: promoters, splice sites, enhancers, chromatin state, expression and gene annotation from sequence. | candidate | Network; a keyless MCP demo tier, or `GI_API_KEY` for REST; sequences go to the vendor. | Try the keyless demo on a public sequence. |
| `alphagenome` | AlphaGenome Atlas lookups for any GRCh38 SNV and on-demand variant scoring for human and mouse. | candidate | Network to Google's API; a free non-commercial key in `ALPHAGENOME_API_KEY`; raw track scores are non-commercial. | Try it on a public non-coding variant. |
| `ontology-term-resolution` | Resolves free-text labels to ontology IDs and validates CURIEs against EBI OLS4, Bioregistry, Identifiers.org and ZOOMA; never writes an ontology ID from memory. | candidate | Python standard library; network to public services, no key. | Try it on the next metadata table whose term IDs must be checked. |
| `pathogen-variant-surveillance` | GenSpectrum LAPIS queries: current lineages, weekly proportions, reporting lag and mutation frequencies for SARS-CoV-2, influenza, RSV, mpox and others. | candidate | Python standard library; network to public LAPIS hosts, no key. | Try it when a task needs current viral lineage data. |
| `biopython` | Biopython workflows: sequence files, NCBI Entrez, BLAST, alignments, structures, phylogenetics. Licence: Biopython License Agreement. | candidate | Local parsing needs a venv with Biopython; Entrez and web BLAST need network and a contact email. | Try it on parsing a public GenBank or FASTA file. |
| `bioservices` | Python interface to UniProt, KEGG, ChEMBL, Reactome, QuickGO and UniChem for identifier mapping, pathways and annotations. Licence GPLv3. | candidate | A venv with `bioservices==1.16.0`; network; a contact email for EBI BLAST. | Try it on an identifier mapping across UniProt and KEGG. |
| `gget` | Command-line and Python lookups across 20+ resources: gene info, BLAST, structures, enrichment, OpenTargets, COSMIC. Licence BSD-2-Clause. | candidate | A Python `3.12` venv with gget; network; a COSMIC account for COSMIC downloads. | Try it for a quick gene lookup before a batch workflow. |
| `deepchem` | DeepChem property prediction (ADMET, toxicity, solubility): SMILES featurization, scaffold splits, graph models, pretrained encoder transfer. | candidate | A Python `3.11` venv with DeepChem `2.8.0`, RDKit and Torch; network only for downloads. | Try it on a small public solubility set with a scaffold split, CPU only. |
| `markitdown` | Converts office documents, PDFs and selected URIs to Markdown with Microsoft MarkItDown; narrowest local conversion first; converted text treated as untrusted. | candidate | Local conversion runs offline in a venv with MarkItDown `0.1.8`; URL, audio, LLM, Azure and MCP routes send content out. | Try it beside the microsoft/markitdown card when a document batch must become Markdown. |

## Tried

None yet: no skill or tooling part of this collection has been run here, in a sandbox or in real work.

## Verdict

No verdict for the collection as a whole: it is read from the clone part by part, and nothing is installed. One CI pattern, spec validation, lives in the kit's own checks; the PR LLM scan is rejected for the kit's CI; the contract guard, the weekly scan report, the author rules and the plugin manifest remain candidates for the kit. The 23 skills read are candidates waiting for a science task, most of them calling a public API or a vendor cloud; the other 154 are listed. Revisit when the freshness check shows a release after `2.72.0`, when a science task needs one of the read skills (read its security report row first), or when the kit adds contract tests for its scripts or a second agent host.

## See Also

- [[area-building-skills-and-plugins|Building skills and plugins]] ([Building skills and plugins](../topics/area-building-skills-and-plugins.md)): area page; spec validation, contract tests, security scans, author rules
- [[area-science|Science]] ([Science](../topics/area-science.md)): area page; the skills by science section
- [[facebookresearch-esm|facebookresearch/esm]] ([facebookresearch/esm](../references/facebookresearch-esm.md)): Meta's ESM models; the `esm` skill targets Biohub's SDK and keeps Meta's older `fair-esm` distribution apart
- [[google-deepmind-alphafold|google-deepmind/alphafold]] ([google-deepmind/alphafold](../references/google-deepmind-alphafold.md)): run hosted through `tamarind`; AlphaFold DB is a reference of `database-lookup`
- [[rosettacommons-rfdiffusion|RosettaCommons/RFdiffusion]] ([RosettaCommons/RFdiffusion](../references/rosettacommons-rfdiffusion.md)): run hosted through `tamarind`
- [[dauparas-proteinmpnn|dauparas/ProteinMPNN]] ([dauparas/ProteinMPNN](../references/dauparas-proteinmpnn.md)): run hosted through `tamarind`
- [[microsoft-markitdown|microsoft/markitdown]] ([microsoft/markitdown](../references/microsoft-markitdown.md)): the library behind the `markitdown` skill

## Sources

- [Desk check: K-Dense-AI/scientific-agent-skills v2.72.0](../../raw/repos/k-dense-ai-scientific-agent-skills-desk-check-2026-11-21.md): README, repository tooling and 23 sampled skills read from the clone, freshness and security reports checked through the GitHub API, the kit's use of its CI patterns.
- [Parts list: K-Dense-AI/scientific-agent-skills 2.72.0](../../raw/data/k-dense-ai-scientific-agent-skills-parts-2.72.0.md): all 177 skills with their own descriptions and README categories, generated by `scripts/catalog_parts.py`.
