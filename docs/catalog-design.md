# Catalog of public tools: design

Status: draft for the owner's approval. Nothing in it is built until the owner approves it.

The catalog is a set of cards about public repositories, libraries, models and patterns that the owner heard of and judged useful. It lives in the kit as an llm-wiki topic, `catalog/`. This document is enough to plan the build without asking the owner; the card itself is judged by [catalog-card-standard.md](catalog-card-standard.md).

Every decision carries one of two tags:

- **[owner]**: decided with the owner (the owner chose it, or accepted Claude's proposal in a playback).
- **[builder]**: the decisions do not fix it; this document makes a call the builder may change without asking, as long as the change keeps the goals and anti-goals.

## Intent and why

An agent working on a task should find the right public tool without reading everything, and the owner should be able to see what is really there, what was done, what was measured and what was decided. Earlier draft cards were flat (a name, a verdict, "when to use") and said almost nothing about what is inside a repository; for a collection of 177 skills that is useless, and for an agent it is worse than useless, because an unchecked line reads like a checked one.

Examples of the intended use: an agent asked to build something from scratch is led to a design method (brainstorming, the Elephant-Goldfish review model); an agent helping with a scientific article that needs bioinformatics computations is led to candidate libraries and told which of them were tried. Tools enter when someone mentions them to the owner or the owner reads about them and judges them useful in work. **[owner]**

## Readers

1. **An agent with a task** (main reader). It reads the task index, opens a card only on a match, and walks from area to card to part. It may run on this machine, on another machine of the owner, or in Claude Science from an uploaded pack. **[owner]**
2. **The owner**, who reads a card to see what is inside, what was tried, what it cost and what was decided. **[owner]**
3. **A builder or contributor** to the kit, who adds cards and scripts and must keep the public-kit rules. **[builder]**

## Goals, non-goals, anti-goals

Goals **[owner]** (decision 24):

1. An agent with a task finds the tool through task index, card, part, and does not read everything; for a large collection (177 skills) it goes through an area and the graph.
2. The owner sees what is really in each tool, what was done, measured and decided.
3. Cards work without the owner's private wiki: at home, on another machine, and in Claude Science through `wiki_graph.py pack`.
4. Every measured number in a card leads to a file in `catalog/raw/`, so an unchecked claim cannot pass for a checked one.

Non-goals **[owner]**:

1. Not a survey of everything popular: only what the owner heard of and found useful.
2. The catalog installs and updates nothing; it says where the clone is and what to read.
3. No automatic tracking of upstream (see Freshness check).
4. No private measurements: only measurements retold without names.
5. The employer's own open-source repositories stay out for now.

Anti-goals **[owner]** (decision 25): failures even when everything technically works, each with its guard.

| # | Failure | Guard |
|---|---|---|
| A1 | An unchecked claim reads as checked (a "when not" written from memory) | A status in every part row; a `catalog/raw/` link for every checked claim; `check_evidence.py` |
| A2 | The catalog costs more than its absence (the agent reads more than the tool's own README) | The route to a part takes at most three catalog files (index, area, card); a card is opened only on a task match |
| A3 | A card goes stale silently (licence changed, version moved) and the agent acts on old facts | The freshness script on that card before relying on it |
| A4 | The public kit gives away private things through a trial log (employer, customer, project, people) | Retelling without names in the session of the trial; `leak_check` before push |
| A5 | The catalog pushes toward installing (an agent reads a card and installs a third-party plugin globally) | "Run it here" says what not to install; installing only after the user's yes |

## Constraints

- **Public kit, no data.** The kit is public under MIT. Cards, raw files and logs name no project, person, customer, employer or ticket, and carry no internal host or private path. **[owner]**
- **`leak_check` and its exception.** `scripts/leak_check.py` (run by the pre-push hook and by CI over the whole history) forbids any `topics/`, `raw/`, `inbox/` path and any `*.local.md`. The catalog needs `raw/`, so it gets a narrow exception (decision 22) **[owner]**; the private-name and secret checks still run over the excepted files. `leak_check` only knows the names listed in `~/.config/wiki-kit/private-names.txt`, so the agent's retelling is the protection and `leak_check` is the safety net. **[owner]** The exception covers exactly `catalog/raw/` and `catalog/wiki/topics/` (area pages and the task index live under a `topics/` folder, which `FORBIDDEN` also matches); it does not cover `catalog/inbox/` or any `*.local.md`, which stay forbidden. **[builder]**
- **Paths through `$EXTERNAL`.** The real clone folder would name the employer, so cards write `$EXTERNAL/<repo>`; each user defines `$EXTERNAL` in their private global rules. **[owner]** The clone folder is named after the repository without its owner (`$EXTERNAL/superpowers`). **[builder]**
- **No installs.** A card never tells the agent to install; plugins run only in a one-session sandbox (`claude --plugin-dir`), packages only in a throwaway environment, and real use waits for the user's yes. **[owner]**
- **Self-sufficient cards.** A card retells what was measured and decided; it never points into a private wiki. **[owner]**
- **Claude Science.** Science cards must be readable in Claude Science, which gets them as one Markdown file from `wiki_graph.py pack`. So the catalog must be a root `wiki_graph.py` accepts, and cards must make sense without their raw files. **[owner]**
- **Plugin layout.** llm-wiki lint fixes raw types to `articles|papers|repos|notes|data` (the first folder under `raw/` must match `type:`), the article `category` to `concept|topic|reference`, and requires `wiki/concepts|topics|references|theses/` with `_index.md` and no subfolders inside them. **[builder]** (fact of the plugin, v1.0.0)
- **Cost.** Foundational work (desk checks, the sample card, the builder check, the comprehension review) runs on the strongest model; mechanical lists are scripts. The measured cost of the first desk check is shown to the owner before the other cards are done. **[owner]** (decision 11)
- **Science texts may be read**, in small per-area batches in separate agents. If a model safety classifier blocks a step, the agent says plainly which step was blocked and the user decides whether to do it in another tool; the agent does not reword or mask content to get past a classifier. **[owner]** (decisions 12, 13)

## Approaches

| | A. llm-wiki topic in the kit (picked) | B. Plain linked Markdown | C. A kit skill with `references/` |
|---|---|---|---|
| Shape | `catalog/` with `raw/`, `wiki/`, `_index.md`; areas and cards are articles; desk checks, parts lists and trials are raw files | `catalog/*.md` linking each other | `skills/catalog/SKILL.md` plus `references/*.md` |
| Graph | `wiki_graph.py` reads it as is: `show`, `path`, `find`, `pack` | Invisible: `wiki_graph.py` reads only `raw/`, `wiki/`, `output/` | A tree, not a graph |
| Evidence trail | Every number traces to a raw file; `check_evidence.py` checks it | None; new checks to write | None |
| Claude Science | `pack` makes one upload file | Manual | Cannot be uploaded as is |
| Cost | Needs a `leak_check` exception and a lint-clean skeleton | Cheapest to start | 500-line limit on `SKILL.md` |

The owner picked **A** **[owner]** (decision 10): it is the only option with an evidence trail and a graph, and both are already built in the kit.

## Design

### Layout of `catalog/`

The decisions fix "a topic with `raw/`, `wiki/`, `_index.md`"; the folders below are **[builder]**, chosen so that `llm-wiki lint catalog`, `wiki_graph.py --root catalog` and `check_evidence.py catalog` accept them.

```text
catalog/
  _index.md  config.md  schema.md  log.md       lint-managed index; scope and conventions; vocabulary
  inbox/                                        gitignored, local only
  raw/
    repos/<owner>-<repo>-desk-check-<YYYY-MM-DD>.md   desk checks (type: repos)
    data/<owner>-<repo>-parts-<version>.md            generated parts lists (type: data)
    notes/trials/<YYYY-MM-DD>-<tool>-<slug>.md        sandbox trials and use records (type: notes)
    notes/<YYYY-MM-DD>-measurements-<slug>.md         retold measurements (type: notes)
    articles/  papers/                                empty, with _index.md (lint requires them)
  wiki/
    topics/task-index.md                              the task index (category: topic)
    topics/area-<slug>.md                             eight area pages (category: topic)
    topics/area-science-<section>.md                  one page per science section (category: topic)
    references/<owner>-<repo>.md                      one card per repository (category: reference)
    concepts/  theses/                                empty, with _index.md
  output/                                             empty, with _index.md
```

- Decision 23 named trials `catalog/raw/trials/`; lint rejects a raw type `trials`, so they go to `raw/notes/trials/` with `type: notes`. **[builder]**
- Raw files are immutable: a new desk check of a new version is a new file, and the card's `sources:` moves to it. **[builder]**
- A non-GitHub tool uses its project name for `<owner>-<repo>` (`ffmpeg-ffmpeg`, `ollama-ollama`). **[builder]**
- `.gitignore` gets, after its existing lines: `!catalog/raw/`, `!catalog/wiki/topics/`, `catalog/inbox/`. Lint warns that `inbox/` is missing on a fresh clone; that is expected (`llm-wiki lint --fix catalog` recreates it locally). **[builder]**

### Entry by task and the global rule

The agent enters through the task index, sent there by a rule in the user's global `~/.claude/CLAUDE.md`, next to the tool-routing rule. **[owner]** (decision 1)

`wiki/topics/task-index.md` is generated by `catalog_index.py` from the cards (see Builder's calls) and is never edited by hand. It is one table per area: `Task | Go to | Status | Not this, because`. A task is written in the words an agent would arrive with ("turn a 40-page PDF with tables into Markdown"). `Go to` links an area page, a science section page or a card, with the part named in the link text. A rejected tool appears under the task it was turned down for, with the reason in `Not this, because` **[owner]** (decision 14). One line per row, no prose; each area section small enough to read alone; the index is searched by area or grep, not read through. **[builder]**

The route: index (1), area or science section page (2), card (3), then the part's own file in the clone, which is the tool, not the catalog (A2). A row that matches a single card may link the card directly. **[builder]**

### The graph

Nodes and edges are those `wiki_graph.py` already builds; no new graph code. **[owner]** (decision 9, 10)

- **Areas** link the cards (and, for large collections, the parts) that serve their tasks. A card may sit in several areas; a new area opens when a card fits none. **[owner]**
- **Cards** link their raw files through `sources:` and back to their areas in `## See Also`.
- **Parts** are rows in a card, or rows in a generated parts list for large collections; science section pages link parts across repositories.
- `tags:` carry `catalog`, `card` or `area`, `area-<slug>` and `kind-<kind>`, so `wiki_graph.py --root catalog find --tag area-science` works. **[builder]**
- Links to a part point at the card file; no row anchors (`check_evidence.py` resolves files, not anchors). **[builder]**

### The eight areas and the science sections

Areas are named by task, not by kind of tool **[owner]** (decision 15): Designing something new; Writing code with agents; Building skills and plugins; Knowledge bases; Search and embeddings; Converting documents and recordings; Writing documents and articles; Science. Slugs: `designing-something-new`, `writing-code-with-agents`, `building-skills-and-plugins`, `knowledge-bases`, `search-and-embeddings`, `converting-documents-and-recordings`, `writing-documents-and-articles`, `science`. **[builder]**

Science is split by the sections of the K-Dense scientific-agent-skills README (Protein Engineering, Cheminformatics, ML & AI, Lab Automation, Databases & Data Access and the rest). They overlap and do not sum to 177; the skills' own frontmatter has no category field. Other science tools go into the same sections. **[owner]**

Area pages and science section pages are generated by `catalog_index.py`, like the task index. An area page holds: a one-paragraph scope and a line naming neighbouring areas, both taken from `catalog/schema.md`; a table `Card | Part | Status`, one row per part that serves the area (one status per cell). `area-science.md` lists only the sections, one line each; each `area-science-<section>.md` lists every part of every science tool in that section, one row each (`Part | Card | Status | One line`), taken from the generated parts lists. The task index points science tasks straight at a section page, so the route stays at three files. **[builder]**

### The card

One card per repository; the index and areas point at parts. **[owner]** (decision 7) Sections, in this order:

1. **Abstract** (the plugin's one-paragraph `>` block): what it is, kind, licence, version read. **[builder]**
2. **Tasks it serves**, first; for a rejected tool, the tasks it was turned down for. **[owner]** The table is `Task | Part | Area`, `Area` being one slug from `areas:`, so `catalog_index.py` knows under which area of the task index each row goes; a row for a rejected part starts with "Not this:". **[builder]**
3. **Run it here**: where the clone is (`$EXTERNAL/<repo>`), which version, which file to read, what to switch off (telemetry, outbound calls), what not to install; for an `in use` part, how it is used and which version. **[owner]** (decisions 2, 16)
4. **What's inside**: the full table of every part, never "13 others". **[owner]**
5. **Tried**: the sandbox and use log, `Date | Task (by kind) | Part | Result | Cost | Record`, the last column linking the raw trial file. **[owner]** (date, task, result, cost); `Part` and `Record` **[builder]**
6. **Verdict**: short prose, a few sentences summing up the rows, with "revisit when"; no list, no table. No card-level status field: the statuses live in the rows. **[builder]** (decision 7 asks for a verdict, decision 27 for no card-level verdict on Superpowers; this reconciles them)
7. `## See Also` (areas, related cards) and `## Sources` (every raw file in `sources:`), as the plugin requires.

**Columns of What's inside** **[owner]** (decisions 7, 19): `Part | What it does | Status | <fourth> | Check when`. The fourth column is `Without plugin` for plugins and skill collections (does the part work when read from the clone without installing, and what breaks), and `Needs` for every other kind (what it takes to run the part here: nothing, a clone, a venv, a GPU and its memory, an API key, data leaving the machine).

**Seven statuses**, one column **[owner]** (decision 16):

| Status | Meaning |
|---|---|
| `listed` | Taken from the repository's own metadata, not read by us |
| `candidate` | Read by the desk check, not tried |
| `tried` | Sandbox result in the Tried log, not yet in real use |
| `in use` | In real work; how and which version: Run it here |
| `method taken` | The idea is in our own rules or scripts; the part itself is not run |
| `reference` | Read for ideas or as a baseline |
| `rejected` | Decided against; reason in the row |

Known cost: rejected after a trial and rejected without one look the same in the column; the Tried log shows the difference. **[owner]**

**Check when by status**: `candidate`: the task to try it on; `rejected`: the revisit condition; `in use`: what to re-check; `listed`: when to read it **[owner]** (decision 17). `tried`: the real task that would move it to `in use`; `method taken`: when to re-read upstream (a new major version of the source); `reference`: when to consult it again **[builder]**.

**What a part is, by kind** **[owner]** (decision 18): plugin or skill collection: each skill, command, agent and hook; library: module or main entry point; app or CLI: command; model: variant (size, quantization); runtime: backend; pattern: its main ideas.

**Frontmatter.** The plugin's required article fields (`title`, `category: reference`, `sources`, `created`, `updated`, `tags`, `confidence`, `volatility`, `verified`, `summary`), plus:

```yaml
areas: [designing-something-new, writing-code-with-agents]   # [owner] replaces the old draft's category
kind: plugin            # plugin | skill-collection | library | app | cli | model | runtime | pattern  [builder]
repo: obra/superpowers  # GitHub owner/name; `url:` instead when not on GitHub                     [builder]
version: "7.0.2"        # [owner] quoted; the version the desk check read, also shown in Run it here
licence: MIT            # [builder] read from the licence file when GitHub reports NOASSERTION
desk_checked: 2026-11-21  # [builder] date of the desk check the card rests on
```

Decision 20 said `areas:` replaces `category`; the plugin requires `category` with its own vocabulary (`concept|topic|reference`), so `category: reference` stays beside `areas:`, and `areas:` replaces only the old draft's domain category. **[builder]** No `type:` field on an article (the plugin's `type` belongs to raw files). `volatility: hot` for every card. **[builder]**

Paths: `sources:` entries are relative to the catalog root (`raw/repos/…`), which is how `check_evidence.py` reads them; links in the body, `## See Also` and `## Sources` are relative to the card file (`../../raw/…`, `../topics/area-<slug>.md`), in the plugin's dual-link form `[[slug|Name]] ([Name](path))` for article links. **[builder]**

**Desk-check and trial frontmatter.** Both are plugin raw files (`title`, `source`, `type`, `ingested`, `tags`, `summary`) with the kit's `authors` and `source_date`. A desk check has `type: repos`, `source` = the repository URL at the tag read, plus `repo`, `kind`, `version`, `licence`. A trial or use record has `type: notes`, `source: session`, plus `repo`, `part`, `version` and the `status` it backs. Tags start with `catalog` and `desk-check` or `trial`. **[builder]**

### Desk check

When a tool is added, an agent (strongest model) reads every part, not only the README, plus the licence file, the last release and how to run it here. **[owner]** (decisions 5, 11) It writes `raw/repos/<owner>-<repo>-desk-check-<date>.md` **[builder]** with:

- identity: URL, tag or commit read, licence as read from the file and as GitHub reports it, last push, last release, archived or not;
- how to run here: clone command, telemetry and outbound calls and how to switch them off, hooks or install steps to avoid, what breaks without the plugin;
- one subsection per part: path in the repository, what it does, what it needs, anything notable;
- reasons for any rejection, retold without names;
- the cost of the desk check itself (tokens and dollars from `claude_usage.py agents`).

Statuses after a desk check are `candidate` for parts read and `listed` for parts taken only from metadata; `rejected`, `reference` and `method taken` only with a recorded reason. Status stays short of `tried` until the tool is used in a task. **[owner]** A rejected tool gets the full card and full desk check, every row `rejected` with its reason **[owner]** (decision 14).

After the first cards, a fresh agent in the Elephant-Goldfish `comprehension` role reviews each new card against `catalog-card-standard.md`, with the card's raw files as its only context; after that, on status changes from `rejected` or to `in use`. **[builder]**

### Sandbox trials and how they reach the kit

An untried candidate found during a task is tried in a throwaway sandbox (a temporary folder, a separate environment: `uv run --with`, a venv, `claude --plugin-dir` for one session), the result is brought to the user, real use waits for the user's yes, and the outcome goes into the card **[owner]** (decision 6). Rejected alternatives: only naming the candidate and waiting (an extra round every time); using it at once when the licence fits (a library error would reach the user's work).

In the session where the trial happened **[owner]** (decision 23):

1. Write `catalog/raw/notes/trials/<date>-<tool>-<slug>.md`: the task told by kind ("parse a 40-page PDF with tables"), version, commands, result, cost; no project, people, customer, ticket or employer.
2. In the same step, update the part's row in the card (status, Check when) and add a Tried row linking the file. Edit only the card and its raw files; then rerun `catalog_index.py`, which rewrites the task index, area pages and science section pages.
3. Run `check_evidence.py --strict` on the catalog and `leak_check.py`; commit; push at once, as is the rule for the kit. A `leak_check` finding stops the push until the wording is fixed.
4. What really happened (project, file) stays in that session's lessons note in the user's private wiki.

A move to `in use` is recorded the same way, as a use record in `raw/notes/trials/`, so the version and date in Run it here have a raw file behind them. **[builder]**

### Freshness check

A script run on demand, `scripts/catalog_fresh.py` **[owner]** (decision 21; name **[builder]**). For each card it takes `repo` and `version` from the frontmatter and compares them, through `gh api`, with the last push, the latest release and the licence. It prints differences and never edits a card: a new version of an `in use` part needs a new desk check, which is agent work. The agent runs it on one card before relying on that card; the user runs it on all cards when wanted. Rejected: a weekly launchd job on one machine (set up outside the kit, the report still has to be opened); a scheduled CI job opening issues (issues are public, notifications arrive when nothing is urgent). CI may be added later if cards multiply. **[owner]**

### Large collections: generated parts lists

The full parts list of a large collection is generated by a script from the repository's own frontmatter, not written by a model **[owner]** (decision 9). Rejected: all 177 rows inside one card; only the parts relevant to current tasks.

`scripts/catalog_parts.py` writes `raw/data/<owner>-<repo>-parts-<version>.md`: `Part | Kind | Description | README sections | Path`, description from the part's frontmatter, sections from the README headings that link the part. **[builder]** For a card whose table would pass 40 rows, What's inside holds every part whose status is not `listed`, plus a line linking the parts list for the rest; every part stays named somewhere, and science section pages link the listed parts directly. Below 40 rows, the card holds every part. **[builder]**

### Claude Science

`python3 -I scripts/wiki_graph.py --root catalog pack area-science-<section> --depth 1 -o <file>` gives the section page and its cards in one file to upload. No `--with-raw` by default: cards are self-sufficient. **[builder]**

### Builder's calls from the review

The builder check of this document asked three questions; these are the answers, all **[builder]**.

1. **Spec and sample disagree: the spec wins.** This document's card section and [catalog-card-standard.md](catalog-card-standard.md) are the rule; the sample card conforms to them, not the other way round. A sample that departs from them is a finding against the sample.
2. **The card is the only master of a part's status.** The task index, the area pages and the science section pages are generated from card frontmatter (`areas`, `kind`, `title`) and card tables (Tasks it serves, What's inside) by `scripts/catalog_index.py`, and are never edited by hand. A trial edits only the card and its raw files, then reruns the script. A status written anywhere else cannot drift from the card.
3. **Generated pages are grounded too.** Each generated page cites in `sources:` the raw files of every card it lists, and its body carries no numbers or dates (statuses and links only). So `check_evidence.py --strict` runs on the whole catalog, generated pages included, with nothing exempted.

## Seed scope

What gets a card first, by area (a card may sit in several). Order: the Superpowers sample first, its measured cost to the owner, then the rest. **[owner]** for the inclusions and exclusions named in decisions 26–30; grouping and order of the rest **[builder]**.

- Designing something new: obra/superpowers (sample, all 15 skills; `brainstorming` `in use` read from the clone, v7.0.2; do not install the plugin, its session-start hook injects a skill into every session) **[owner]** (decisions 8, 27); google/elephant-goldfish-model; Fission-AI/OpenSpec; github/spec-kit.
- Writing code with agents: colbymchenry/codegraph; NeoLabHQ/context-engineering-kit.
- Building skills and plugins: ygavrilov/claude-code-kit (no licence: read only); K-Dense-AI/scientific-agent-skills for its skill CI patterns.
- Knowledge bases: nvk/llm-wiki (`in use`, pinned v1.0.0); nashsu/llm_wiki; the Karpathy LLM Wiki gist (kind `pattern`); tobi/qmd.
- Search and embeddings: Ollama; EmbeddingGemma 2; bge-m3; Qwen3-Embedding-4B; llama.cpp; ONNX Runtime; numpy; FAISS.
- Converting documents and recordings: whisper.cpp; FFmpeg; microsoft/markitdown; python-pptx; python-docx; pypdf; LibreOffice.
- Writing documents and articles: blader/humanizer.
- Science: K-Dense-AI/scientific-agent-skills; ColabFold; RFdiffusion; BioNeMo (now bionemo-recipes); DeepChem; AlphaFold; ProteinMPNN; ESM (archived); ProtTrans; FAISS (databases section).

Decided cases:

- **FAISS only of the vector stores** **[owner]** (decision 28). FAISS is the one the owner's sources actually use (a local embedding pipeline sketch, a benchmark in a literature review). Qdrant and Milvus get no card until a task needs a vector database server (FAISS is a library). Pinecone is out of scope: a hosted service, not an open repository, and data leaves the machine.
- **nashsu/llm_wiki: rejected for work data only** **[owner]** (decision 29): a third-party desktop app with its own API keys, so data goes to the model provider past the organisation's own model account. Its GPL-3.0 licence (read from the licence file; GitHub reports NOASSERTION) is a fact in the card, not a reason: it allows use and forbids only copying its code into the MIT kit. With one's own keys at home it may be used; there is no need, since the engine is nvk/llm-wiki. Check when: the app can work through the organisation's Claude account or a local model. The desk check records the reason in `catalog/raw/`.
- **ColabFold "when not" holds** **[owner]** (decision 30): passing a FASTA or CSV file to `colabfold_batch` queries the public MSA server; the way around is the local database setup with `colabfold_search`. The desk check re-reads it at the version it records.
- **Earlier drafts are gone** (decision 26): five uncommitted draft cards and a card template were deleted; nothing of their shape is reused, and the facts they had verified (URLs, licences) are re-read by the desk checks.
- **Out:** the employer's own open-source repositories; internal or marketplace tools not public. **[owner]**

## Sample card

The sample below is the full card for obra/superpowers, as it will sit at `catalog/wiki/references/obra-superpowers.md`. It conforms to the card section above and to the standard (builder's call 1). Its raw files sit at `catalog/raw/repos/obra-superpowers-desk-check-2026-11-21.md` (the desk check) and `catalog/raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md` (the use record of `brainstorming`); its `## See Also` links the three area pages at `catalog/wiki/topics/area-<slug>.md`, which `catalog_index.py` generates. The sample was checked in a scratch copy of this layout: `check_evidence.py --strict` passed with no errors or warnings.

````markdown
---
title: "obra/superpowers"
category: reference
kind: plugin
areas: [designing-something-new, writing-code-with-agents, building-skills-and-plugins]
repo: obra/superpowers
version: "7.0.2"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/obra-superpowers-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-designing-something-new, area-writing-code-with-agents, area-building-skills-and-plugins, kind-plugin, claude-code, skills, brainstorming, tdd, debugging, code-review, planning]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Claude Code plugin of process skills for coding agents: design by interview, plans, plan execution with ledgers and reviews, TDD, debugging, code review, worktrees, skill testing, plus a SessionStart hook. Its skills are read one by one from a clone; the plugin and its every-session hook are not installed. brainstorming is in use, two techniques are in the kit's own rules, the router and hook are rejected, twelve parts wait for a task."
---

# obra/superpowers

> A Claude Code plugin (kind `plugin`, licence MIT, version `7.0.2` read): 15 process skills for coding agents, from designing by interview to finishing a branch, plus a SessionStart hook that injects a "use a skill first" rule into every session. Here its skills are read from a clone, part by part, and the plugin is not installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Work out what to build before building it, in software or outside it (a talk, a business) | `brainstorming` | designing-something-new |
| Show mockups, layouts or side-by-side options while designing | `brainstorming` visual companion | designing-something-new |
| Turn a spec or approved design into a step-by-step implementation plan | `writing-plans` | writing-code-with-agents |
| Execute a written plan in a code repo yourself, one review at the end | `executing-plans` | writing-code-with-agents |
| Execute a written plan with a fresh subagent and a review per task | `subagent-driven-development` | writing-code-with-agents |
| Isolate feature work from the current branch | `using-git-worktrees` | writing-code-with-agents |
| Decide how to integrate a finished branch (merge, PR, keep) | `finishing-a-development-branch` | writing-code-with-agents |
| Find the root cause of a bug or failing test before fixing it | `systematic-debugging` | writing-code-with-agents |
| Write code test-first | `test-driven-development` | writing-code-with-agents |
| Work on several independent problems at once | `dispatching-parallel-agents` | writing-code-with-agents |
| Get a review of finished work | `requesting-code-review` | writing-code-with-agents |
| Act on review findings without blind agreement | `receiving-code-review` | writing-code-with-agents |
| Claim that work is done, fixed or passing | `verification-before-completion` (technique already in the kit's rules) | writing-code-with-agents |
| Write, change or test a skill | `writing-skills` (technique already in the kit's rules) | building-skills-and-plugins |
| Find out why a session that used these skills went wrong | `diagnosing-superpowers` | building-skills-and-plugins |
| Not this: route every request to a skill automatically. Rejected: the hook injects that rule into every session | `using-superpowers`, SessionStart hook | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch v7.0.2 https://github.com/obra/superpowers $EXTERNAL/superpowers`, read-only. Never edit the clone.
- **Version**: `7.0.2`, the latest release, published 2026-11-03. Before relying on this card, compare with upstream: `gh api repos/obra/superpowers --jq .pushed_at` and `gh api repos/obra/superpowers/releases/latest --jq .tag_name`. A newer version of an `in use` part needs a new desk check.
- **Read**: `$EXTERNAL/superpowers/skills/<skill>/SKILL.md` and the files it names in its own folder. Read every `superpowers:<name>` reference as `$EXTERNAL/superpowers/skills/<name>/SKILL.md`. Run bundled scripts by absolute path through their interpreter (`bash …/scripts/<script>`).
- **In use**: `brainstorming` at `7.0.2`, read from the clone (`$EXTERNAL/superpowers/skills/brainstorming/SKILL.md`), not as a plugin, to design something before building it. The design doc goes where the user says, not to the default `docs/superpowers/specs/`; the `superpowers:writing-plans` handoff is read as a path into the clone, or skipped when the doc goes to a builder check instead.
- **Switch off**: set `SUPERPOWERS_DISABLE_TELEMETRY=1` before starting the visual companion (`DISABLE_TELEMETRY` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` also work); the remote logo is the only network call found. Add `.superpowers/` to the target repo's `.gitignore` when the visual companion, `executing-plans` or `subagent-driven-development` write there.
- **Do not install**: the plugin, in any scope (marketplace, `/plugin install`, or its `hooks.json` copied into settings). Its SessionStart hook would inject `using-superpowers` into every session. When the hook or plugin behaviour itself has to be seen, run one terminal session `claude --plugin-dir $EXTERNAL/superpowers` from a scratch folder and record the result under Tried; a real install waits for the user's yes.

## What's inside

Parts: 15 skills in `skills/`, one hook in `hooks/` (with its ports to other harnesses), and the visual companion of `brainstorming`, listed as its own row because it runs a local server and has the only network call found. There is no `commands/` or `agents/` folder.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `brainstorming` | Design by interview: reads what exists, asks one open question at a time, asks why first, lays out two or three approaches with a recommendation, plays each part back, writes a design doc (intent, goals, non-goals, anti-goals, constraints, approaches, what is left to the builder), then sends it to a builder check (a fresh subagent reads the doc as the builder would and lists the questions it still has). Nothing is built before the doc is approved. | in use | Works from the clone. Read `superpowers:writing-plans` as that skill's path. The builder check needs a subagent tool. Point the design doc at your own location; the default is `docs/superpowers/specs/`. | On a release after `7.0.2`, re-read `SKILL.md` and `builder-check-prompt.md` before the next design: the `7.0.2` release retuned its questions. |
| `brainstorming` visual companion | Local browser tab for mockups and options, started only after the user accepts. A Node server on `localhost` with a random key in the URL; stops after 4 hours idle. Writes screens to `.superpowers/brainstorm/` in the project. | candidate | Works: `bash scripts/start-server.sh --project-dir <project> --open` from the skill folder. Needs Node.js and a browser. Loads a remote logo unless telemetry is off. | Try it on a design question where the user picks the look (a screen, a layout, a diagram). Start it with `SUPERPOWERS_DISABLE_TELEMETRY=1`. |
| `diagnosing-superpowers` | Reads session transcripts read-only, runs seven analyst subagents in parallel, writes a report where every finding cites `path:line`; files a GitHub issue only after approval. | candidate | Works on transcripts on disk, but it is built for sessions that ran these skills. Writes under `~/.superpowers/diagnosing-superpowers/`. Needs subagents; `gh` for the issue step. | Try it when a sandbox session with the plugin loaded goes wrong (too slow, too costly, a skill did not fire). |
| `dispatching-parallel-agents` | One focused, self-contained agent per independent problem, all dispatched in one response; then check for conflicts and run the full suite. Not for related failures or shared files. | candidate | Works; needs a subagent tool. Names no other skill. | Try it on two or more unrelated failures with no shared files, for example failing tests in different scripts. |
| `executing-plans` | Executes a `writing-plans` plan inline: TDD per step, a ledger (a progress file, `progress.md`) in `.superpowers/sdd/` that survives compaction, a `Ruling:` line (a written ruling on what to do and why) for every deviation from the plan, one fresh whole-branch review at the end. | candidate | Works if its scripts are run by absolute path (`bash $EXTERNAL/superpowers/skills/executing-plans/scripts/task-start`). Needs git, bash and a plan in the `writing-plans` format. Names eight other skills. | Try it on an approved plan for a code repo with mostly independent tasks, when one review at the end is enough. |
| `finishing-a-development-branch` | Runs the full suite, detects normal repo, worktree or detached HEAD, offers merge, PR or keep; deletes only on the typed word `discard`; removes only worktrees it owns. | candidate | Works; needs git, and the forge CLI (the code host's command-line tool) for the PR option. | Try it at the end of the first branch built with `executing-plans` or `subagent-driven-development`. |
| `receiving-code-review` | Read, restate, verify against the codebase, then fix or push back with reasons; clarify every unclear item before implementing any; YAGNI check by grepping for real usage; no performative agreement. | candidate | Works; needs only the review text and the code. | Try it on the next set of review findings on a pull request or from a reviewer agent. |
| `requesting-code-review` | Dispatches a reviewer subagent with the `code-reviewer.md` template, the plan and a git range; Critical fixed at once, Important before going on, Minor noted. | candidate | Works; needs a subagent tool and git. | Try it before merging a multi-file change in a script repo, and compare its findings with the review used so far. |
| `subagent-driven-development` | Executes a plan with a fresh implementer subagent per task, a spec and quality review after each, a capped fix loop, a ledger, and a final review on the most capable model. Picks the cheapest model that can do each role and always names the model. | candidate | Works if its scripts are run by absolute path. Needs a subagent tool, git and bash. Writes `.superpowers/sdd/` with its own `.gitignore`. | Try it on a plan with many independent tasks where a review gate per task is wanted; record the cost next to `executing-plans`. |
| `systematic-debugging` | No fix before root-cause investigation: read errors, reproduce, check recent changes, instrument component boundaries, test one hypothesis at a time, fix with a failing test; after three failed fixes, question the architecture. Helper files for root-cause tracing, defense in depth, condition-based waiting. | candidate | Works; plain text plus helper files in the same folder. | Try it on the next bug or failing test that the first fix does not solve. |
| `test-driven-development` | No production code without a failing test first; red, verify red, green, verify green, refactor; code written before its test is deleted. Exceptions only with the user: throwaway prototypes, generated code, configuration files. | candidate | Works; needs a test runner in the target project. | Try it on a new feature or bug fix in a script that already has a test suite; not on a throwaway spike. |
| `using-git-worktrees` | Detects an existing worktree first, asks for consent, prefers the harness's own worktree tool, falls back to `git worktree add` under an ignored `.worktrees/`, then sets up and runs a baseline test. | candidate | Works; needs git. In Claude Code the skill itself prefers the native `EnterWorktree` tool. | Try it on feature work in a code repo that must not touch the current branch; check that it picks the native tool. |
| `using-superpowers` | The router: invoke a skill if there is "even a 1% chance" it applies, before any reply, including clarifying questions. This is the text the hook injects into every session. | rejected | Readable, but it exists to be injected by the hook; without the plugin it does nothing. User instructions take precedence over it. | Rejected: it puts a skill check before every reply in every session (slower, more questions). Revisit when the hook becomes opt-in, or a one-session sandbox shows the extra cost and questions are acceptable. |
| `verification-before-completion` | No completion claim without fresh evidence: name the command that proves the claim, run it, read the output, then claim; "should" and "probably" are red flags; agent reports are verified, not trusted. | method taken | Works; needs nothing. The kit's agent rules carry it in their own words (`agents/COMMON.md`). | Re-read when a release changes this skill; the kit rule stands on its own. |
| `writing-plans` | Writes a plan for an engineer who has not seen the code or the spec: Goal, Architecture, Global Constraints, Review Focus; tasks with files, interfaces and RED-GREEN checkbox steps; a self-review; then hands off to one of the two executors. | candidate | Works; saves to `docs/superpowers/plans/` unless told otherwise. Its executors need git and the scripts above. | Try it when an approved design must become a multi-step plan for a code repo. It was skipped for this catalog's design. |
| `writing-skills` | Skill writing as TDD: run a pressure scenario without the skill, record the excuses verbatim, write the smallest skill that answers them, re-run with it, close loopholes. Also: a description says only when to use the skill; match the form of the guidance to the kind of failure. | method taken | Works; baseline runs need a subagent tool; `render-graphs.js` needs Node and Graphviz. The kit's specialist testing method is adapted from it (`docs/testing-specialists.md`). | Re-read before the kit writes or changes a skill or specialist, and when a release changes the testing method. |
| SessionStart hook (`hooks/hooks.json`, `hooks/session-start`; ports for Cursor, OpenCode, Pi, Hermes Agent) | On startup, `/clear` and compaction, injects the whole `using-superpowers` skill into the session as additional context. | rejected | Does not run without the plugin; that is why the plugin is not installed. | Rejected for the same reason as `using-superpowers`. Revisit under the same conditions. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-19 to 2026-11-21 | Designing a catalog of tools for an agent-maintained knowledge base | `brainstorming` | Real use, read from the clone at `7.0.2`, not as a plugin: 30 design decisions, a design doc and a sample card. The `writing-plans` handoff was skipped; the design doc went to a builder check instead. | not measured per skill | [use record](../../raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md) |

## Verdict

No verdict for the repository as a whole: its skills are read from the clone part by part, and the plugin is not installed. One skill is in real use, two techniques live in the kit's own rules, the auto-routing pair is rejected, and the other twelve parts are candidates waiting for a matching task. Revisit when the freshness check shows a release after `7.0.2` (re-check `brainstorming` first), when the SessionStart hook becomes opt-in, or when a code-repo task needs the chain from plan to merged branch.

## See Also

- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; `brainstorming` and its visual companion
- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; plans, execution, debugging, review, branches
- [[area-building-skills-and-plugins|Building skills and plugins]] ([Building skills and plugins](../topics/area-building-skills-and-plugins.md)): area page; `writing-skills`, `diagnosing-superpowers`

## Sources

- [Desk check: obra/superpowers v7.0.2](../../raw/repos/obra-superpowers-desk-check-2026-11-21.md): every part read from the clone, freshness checked through the GitHub API, the kit's use of it.
- [Use record: superpowers brainstorming, designing a tool catalog](../../raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md): the real use of `brainstorming` behind its `in use` status and the Tried row.
````

## What is left to the builder

In this order; each step leaves the kit pushable.

1. **Wait for approval.** Nothing below is built before the owner approves this document.
2. **`leak_check.py` exception.** Keep `FORBIDDEN`; add `CATALOG_DATA = re.compile(r"^catalog/(raw|wiki/topics)/")`. A path that matches `FORBIDDEN` is allowed only if it matches `CATALOG_DATA`, the remainder after that prefix does not match `FORBIDDEN` again, and it does not end in `.local.md`. Private names and secrets still run on these files. Self-test cases: pass `catalog/raw/notes/trials/x.md`, `catalog/wiki/topics/_index.md`; fail `catalog/inbox/x.md`, `catalog/raw/x.local.md`, `catalog/raw/notes/topics/x.md`, `catalog/wiki/references/inbox/x.md`, `sub/catalog/raw/x.md`, `raw/x.md`, `topics/x.md`. Update the docstring, the README "Leak check" bullet and `CONTRIBUTING.md`.
3. **`.gitignore`**: append `!catalog/raw/`, `!catalog/wiki/topics/`, `catalog/inbox/`; confirm with `git check-ignore -v`.
4. **Skeleton.** `scaffold_wiki.py` needs an empty template topic, which the kit cannot hold; instead write `catalog/config.md` (title, description, scope: the tools the owner found useful; conventions: retell without names, `$EXTERNAL` paths, no install steps) and run `llm-wiki lint --fix catalog` once to create the required folders and `_index.md` files. Then `llm-wiki lint catalog` must be clean except the local-only `inbox/` warning on a clone.
5. **`catalog/schema.md`**: the area slugs, the seven statuses, Check when by status, kinds and what a part is per kind, the fourth column by kind, file naming. This is the vocabulary agents read before writing a card.
6. **`scripts/catalog_parts.py`** (stdlib, no model): `catalog_parts.py CLONE --repo OWNER/NAME --version V -o FILE`. Finds `skills/*/SKILL.md`, `commands/*.md`, `agents/*.md` and hook definitions; reads `name` and `description` with the YAML subset reader of `skill_check.py`; maps parts to README sections by the headings above their links; writes the raw `data` file with frontmatter (`source` = repository URL at the version, `type: data`). Deterministic: the same clone gives the same file.
7. **Sample card.** Desk-check Superpowers with a strongest-model agent; write its desk-check raw file (`raw/repos/obra-superpowers-desk-check-<date>.md`), the use record of the brainstorming use that produced this design (`raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md`), and the card from the sample in this document; report the desk check's measured cost to the owner before any other card.
8. **`scripts/catalog_index.py`** (stdlib, no model): `catalog_index.py CATALOG [--check]`. Reads every card in `wiki/references/` (frontmatter `title`, `areas`, `kind`, `sources`; the Tasks it serves table `Task | Part | Area`; the What's inside table `Part | … | Status | … | Check when`) and `schema.md` (area slugs, titles, scope lines, neighbours; science sections), plus the parts lists in `raw/data/` for science sections. Writes `wiki/topics/task-index.md` (one table per area; `Status` from the part's row; `Not this, because` from the reason in a `rejected` row), `wiki/topics/area-<slug>.md` (`Card | Part | Status`) and `wiki/topics/area-science-<section>.md` (`Part | Card | Status | One line`). Each generated page has `category: topic`, the tags `catalog`, `area` and `area-<slug>`, a line saying it is generated and not to be edited by hand, `sources:` = the union of the `sources:` of the cards it lists, and no numbers or dates in its body. Deterministic; `--check` exits 1 when a generated page differs from what the cards give (for CI and pre-commit). Run it after every card change; grow the pages with each card.
9. **Global rule.** Add a section right after "Point work to the tool that does it best" in `templates/global-CLAUDE.md`, and teach `global_rules.py` to replace `{KIT}` with the kit's own folder and `{EXTERNAL}` with `--external DIR`, else `WIKI_KIT_EXTERNAL`, else `~/Projects/external`. It must be its own `## ` section: `global_rules.py` appends only missing sections, so a bullet inside an existing one would never reach existing installs. Text:

   ```markdown
   ## Find a tool through the catalog

   - Before choosing a public tool, library, skill or model for a task, or when the user names one, read the task index of the kit's catalog: `{KIT}/catalog/wiki/topics/task-index.md`. Open an area page or card only when a row matches the task; do not read the catalog through.
   - In catalog cards, `$EXTERNAL` means `{EXTERNAL}`, the folder of read-only clones of third-party repositories.
   - Before relying on a card, run `python3 -I {KIT}/scripts/catalog_fresh.py <card>`. A new version of an `in use` part needs a new desk check first.
   - Try a `candidate` or `listed` part in a throwaway sandbox (temporary folder, separate environment) and use it for real only after the user's yes. Never install a plugin or package because a card names it.
   - Record a trial in the catalog in the same session, the task told by kind, with no project, people, customer, ticket or employer names: write the trial file under `catalog/raw/notes/trials/`, update only the card, rerun `catalog_index.py`; then `check_evidence.py --strict` on the catalog, `leak_check.py`, commit and push.
   ```

10. **`scripts/catalog_fresh.py`** (stdlib plus the `gh` CLI): `catalog_fresh.py CARD... | --all`. Per card: `gh api repos/{repo}` (`pushed_at`, `license.spdx_id`, `archived`) and `gh api repos/{repo}/releases/latest` (`tag_name`, `published_at`; on 404, the newest tag). Print one line per difference: version in card vs latest release, licence vs GitHub (`NOASSERTION`: "read the licence file"), pushed after `desk_checked`, archived. A card with `url:` and no `repo:` prints "not on GitHub: check by hand". Exit 0 no differences, 1 differences, 2 error. Never writes.
11. **Seed cards** in the order of Seed scope, science in small per-section batches in separate agents; each card is followed by `catalog_index.py` and passes `check_evidence.py --strict catalog` and `leak_check.py` before its commit and push.
12. **CI and docs.** Add `python -I scripts/check_evidence.py --strict catalog` (over the whole catalog, generated pages included; `--strict` makes an ungrounded number fail, A1) and `python -I scripts/catalog_index.py catalog --check` to `.github/workflows/checks.yml` (both stdlib); keep `llm-wiki lint` local (the plugin is not installed in that job). Add `catalog/` and the three scripts to the README tables.

Optional, once the cards multiply: a `scripts/catalog_check.py` that checks card structure mechanically (sections present and in order, every status one of the seven, fourth column header matching `kind`, Check when filled, frontmatter fields present). **[builder]**
