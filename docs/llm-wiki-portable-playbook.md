---
title: "Portable LLM-Wiki Playbook"
type: playbook
created: 2026-10-19
audience: "AI coding agent (any harness) + its human operator"
status: v1
summary: "Engine-agnostic instructions for building an agent-maintained knowledge base out of a long chat history and a codebase, with cost discipline, confidentiality tiers and a migration path to GitHub Copilot."
---

# Portable LLM-Wiki Playbook

## 0. Who this is for and what it promises

You are an AI agent with file access to a repository. Your operator has months of
work with you — long chats, generated code, instructions, decisions, half-finished
analyses — living in one enormous conversation. That conversation is the single
most expensive asset in the project and the single most fragile one: it is
unsearchable, uncitable, growing, and it dies when the context window or the chat
session dies.

This playbook turns that into a **knowledge base an agent maintains**: a plain-file
wiki in git, where every durable claim traces back to an immutable source, and where
any future session can reload the project's state in a few thousand tokens instead of
re-reading everything.

It is deliberately generic. It contains no project, customer, or employer specifics.
Fork it, fill it in, keep your fork private if your content is private — but keep the
*method* portable.

Three hard promises if you follow it:

1. A new session can answer "what do we know about X, and how do we know it" with file
   citations, without reading the history.
2. Knowledge survives the harness. Move from one assistant to another and the wiki
   moves with it, because it is Markdown in git, not vendor state.
3. Cost per answer falls, because sessions read compiled articles instead of raw material.

## 1. The core model

Three layers, one direction of flow. Never short-circuit it.

```
inbox/   →   raw/   →   wiki/   →   output/
(dropbox)   (sources)  (articles)  (deliverables)
```

- **`raw/` is immutable evidence.** Chat exports, document extracts, exported pages,
  issue dumps, web articles, papers, your own notes. You may add, you may never edit
  for style and you may never translate in place. If a source is wrong, you add a newer
  source and record the contradiction in the article — you do not fix history.
- **`wiki/` is synthesis.** Articles written by the agent, in one language (pick one;
  English is the default because tooling, code and models are best there). Every factual
  claim traces to `raw/` through `sources:` frontmatter and a `## Sources` section. An
  article with no sources is a hallucination with a filename.
- **`output/` is deliverables.** Reports, slide outlines, study guides, playbooks (this
  file is one), translations, briefs for other people. Generated from `wiki/`, regenerable,
  cited the same way.
- **`inbox/` is the staging area.** Anything dropped in gets classified, redacted, given
  frontmatter, and moved into `raw/` by an explicit ingest step. Nothing enters `raw/`
  by accident.

Why the discipline pays: the wiki becomes *trustable*. The expensive failure mode in
agent-maintained knowledge is not a missing fact — it is a confident article nobody can
check. Provenance is what makes the thing worth more than the chat it came from.

## 2. Repository layout

Two shapes; pick by access control, not by taste.

**Shape A — hub with topics.** One repo, many subjects that share people, vocabulary
and tooling:

```
<hub>/
  README.md          # plan, decisions, next steps — the entry point for every session
  AGENTS.md          # (or CLAUDE.md / copilot-instructions.md) — rules for agents
  _index.md          # topic registry
  log.md             # operation log
  topics/
    <subject-a>/
      config.md      # scope, conventions, freshness threshold
      schema.md      # local vocabulary, entity types, relationship verbs
      _index.md
      log.md
      inbox/
      raw/           # notes/ articles/ papers/ repos/ data/
      wiki/          # concepts/ topics/ references/ theses/
      output/
    <subject-b>/
    shared/          # cross-subject knowledge: people, technologies, patterns, glossary
```

**Shape B — one repo, wiki inside it.** A single project or a codebase that wants its
knowledge next to its code: put the same tree under `.wiki/` at the repo root.

Rules that matter more than the shape:

- **One subject per topic.** When two subjects need different *access rules*, they need
  different repositories, not different folders. Access control does not live in a path.
- **Shared knowledge is generalized only.** Things move *into* the shared topic
  de-identified and abstracted; nothing moves *out of* shared into a restricted topic and
  back again. One-way valve.
- **The repo root stays small.** A fixed, short list of files. Anything else that lands
  there is unfiled and gets quarantined by lint, not silently blessed.
- **Code does not live in the wiki.** The wiki links to repositories and describes
  architecture; it never copies source in. Code rots, articles about code age gracefully.
- **Binaries do not live in the wiki.** Ingest a presentation or PDF as a Markdown
  extract — text per slide/page with its number, speaker notes, table contents, short
  prose descriptions of charts — and point `source:` at where the original actually lives.
  Never embed images or commit the binary.

## 3. The frontmatter contract

This is the whole API between layers. Keep it boring and enforce it with a script.

Raw source:

```yaml
---
title: "..."
type: note | chat | article | paper | export | data
source: "<URL, or a path to the original, or a label>"
authors: ["..."]           # "unknown" is a valid value; guessing is not
source_date: YYYY-MM-DD    # when the original was written
ingested: YYYY-MM-DD       # when it entered the wiki
sensitivity: internal | confidential
---
```

Article:

```yaml
---
title: "..."
category: concept | topic | reference | thesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
volatility: hot | warm | cold    # how fast this goes stale
sources: ["raw/notes/2026-01-01-x.md", "..."]
compiled-from: sources | conversation | mixed
sensitivity: internal | confidential
---
```

Article categories, in practice:

- **concept** — one bounded idea or mechanism. The default. If you cannot name the one
  thing it is about, split it.
- **topic** — a broad theme or a playbook that ties concepts together.
- **reference** — a curated list, map, standard, lookup table, or decision record.
- **thesis** — a claim under active evidence-gathering, with for/against framing and a
  verdict that may change.

`volatility` is what makes refresh cheap: a `hot` claim about a tool version gets
re-checked monthly, a `cold` claim about a mathematical method does not get re-checked
at all.

## 4. Decisions are first-class (ADR)

Every non-obvious choice becomes a record in `wiki/references/adr-NNNN-<slug>.md`,
MADR format, numbered per topic, tagged `adr`:

```
status: proposed | accepted | rejected | deprecated | superseded
decided: YYYY-MM-DD
```

Sections: Context and Problem Statement · Decision Drivers · Considered Options ·
Decision Outcome (with Consequences) · Pros and Cons of the Options.

**Never rewrite an accepted ADR.** A new ADR supersedes it; the old one gets
`status: superseded` and a link forward. The reason is not bureaucracy: when the agent
can read *why* a choice was made and what was rejected, it stops re-proposing the
rejected option every third session. ADRs are the cheapest anti-amnesia device there is.

Decisions made verbally in chat count. Mark them `compiled-from: conversation` and cite
the chat export.

## 5. Confidentiality tiers

Define the categories once, in the agent instructions file, and make them concrete.
A workable default set:

1. **Identity of third parties** — client/partner names, their products, code names.
2. **Commercial terms** — rates, budgets, deal sizes, contract terms.
3. **Personal and HR data** — assessments, grades, salaries, feedback on a person's work
   or behaviour, health, private contacts, candidate material.
4. **Secrets and access** — tokens, passwords, keys, internal URLs, infrastructure
   addresses.

Rules:

- **Category 4 never lands anywhere, `raw/` included.** Replace on ingest with
  `[REDACTED:secret]` and report the count to the human. Placeholders (`<token>`) and
  variable names (`API_TOKEN`) are not credentials — do not mangle code.
- **Category 3 is not stored.** Professional facts about people are fine: name, role,
  expertise, responsibilities, work contacts. Judgements about people are not.
- **Categories 1–2** are allowed inside a topic that genuinely needs them, marked
  `sensitivity: confidential`.
- **Anything leaving the wiki** — a published page, a shared deliverable — is checked
  against the list first.
- **The list is not exhaustive.** When something looks sensitive but matches no category,
  treat it as confidential and ask.

### The `.local.md` escape hatch

A verbatim export from a system that already has its own access control (a corporate
wiki, an issue tracker, a document store) is stored **unfiltered** under a
`*.local.md` name that `.gitignore` excludes. Rationale: the material already lives in
that system under its own permissions, the export never leaves the machine, and
re-filtering it locally buys nothing while destroying fidelity you will need when
compiling. Credentials are still redacted. Record `source` and the page/issue version
so anyone with access can re-export it.

This exception covers `raw/` only. Articles and deliverables obey the full rules — no
secrets, no personal data, no internal URLs — because those *do* leave.

Put this in `.gitignore` on day one:

```
*.local.md
.sessions/
inbox/.unknown/
```

## 6. Language policy

- Compiled content — articles, deliverables, configs, schemas — in **one** language.
- Raw sources keep their original language, always. Translation is lossy and `raw/` is
  evidence.
- Talk to the human in whatever language they use. A translated rendering of wiki content
  is a *deliverable* produced on request, not a parallel article tree. Two language trees
  means two truths and twice the drift.

## 7. Cost discipline

This section is the difference between a system you keep and a system you abandon after
the first invoice.

**What costs money is context that every later call re-reads, not the model's answers.**
Measured on a real month: cache reads and writes were 92% of spend, output tokens 8%.
Optimise what you load, not what you say.

- **Scripts before models.** Anything deterministic runs as a script and the session reads
  only its summary: exporting from APIs, document/chat conversion, confidentiality and
  frontmatter checks, lint, duplicate detection, inventories. When a task is done by hand
  twice, write the script the third time. A 200-line Python script replaces thousands of
  tokens per run, forever.
- **One task per session.** Start a new session per operation; after a completed operation
  and its commit, clear. A session past roughly 150k tokens is due for a restart — write
  the state into `README.md` *first*, then restart. The README is the handoff protocol.
- **Cheap models for reading and copying.** Reading sources, exporting, mechanical
  conversion: smallest capable model. Planning, synthesis, decisions, review: the big
  model, in the main session. Never spawn a frontier-model sub-agent to grep.
- **Keep tool output small.** Never `cat` a whole file into context. `head`, `grep`,
  ranged reads, or delegate the reading to a sub-agent that returns a digest with file
  paths and line numbers. A sub-agent's value is that its context dies and yours doesn't.
- **Synthesis is never delegated.** Reader agents return facts with citations. Only the
  orchestrator sees all the topics and all the existing articles at once, so only the
  orchestrator can decide what is a new article, what is an update, and what is a
  contradiction. Delegated synthesis produces confident duplicates.
- **Measure, per answer.** Have a script that reports session / last-answer / today /
  month cost and context size, and run it at the end of each answer. Unmeasured spend
  becomes a surprise; measured spend becomes a habit.

### Agent roles

| Role | Model | Job |
|---|---|---|
| Orchestrator | frontier | Plan, decide, synthesize, review, commit. Holds the whole picture. |
| Reader | mid-tier | Read N sources, return a compact cited digest. Read-only. |
| Compiler | mid-tier | Ingest + compile exactly one topic, then lint it. Given explicit root, scratch dir, date, file list. |
| Exporter | small | Mechanical copying from an API to `raw/` when no script exists. No synthesis. |

Give every sub-agent: the root path, a scratch directory, today's date, the explicit file
list, and the shared conventions file. Never "figure out what needs doing".

## 8. Quality gates

- **Lint on every operation.** Broken links, missing indexes, orphan files, frontmatter
  violations, stale articles past the topic's freshness threshold, unfiled root files.
  Must reach PASS before commit.
- **Coverage ledger.** Every raw source is either cited by an article or listed in
  `wiki/references/uncompiled-source-coverage.md` *with a reason*. This single file is
  what keeps "we ingested 200 pages" from meaning "we read 12 and forgot".
- **Contradictions are content.** When two sources disagree — a presentation says one
  thing, the tracker says another — record both and mark the conflict. Do not pick a
  winner on the agent's authority. Flagging the disagreement is usually the most valuable
  line in the article.
- **Unknowns are content.** Keep an open-questions list in `README.md` per topic. An
  agent that writes "unknown" is worth more than one that interpolates.
- **Lessons-learned loop.** At the end of a working session, extract error→fix patterns,
  operator corrections and discoveries into the wiki. The system should get cheaper to
  run every month; that only happens if the corrections are written down.

## 9. Git

- Commit after each completed operation, with the operation in the message:
  `ingest: …`, `compile: …`, `docs: …`, `retract: …`.
- Commits are autosave, not a decision to confirm. Do not ask.
- Commit raw sources that are unique or public: the operator's own notes, chat exports
  (after the confidentiality check), research results, web articles, papers.
- Do **not** commit copies of systems that have their own access control — those are
  `.local.md` and re-exportable.
- Generated binaries are not committed: commit the Markdown source in `output/`, rebuild
  the artifact from it. Small `png`/`svg` are fine.
- A clone without the `.local.md` files will warn in lint about missing sources. That is
  expected, and it is the point.

## 10. Cold start: turning one giant chat into a wiki

This is the task in front of you. Do it in this order; the order is the whole trick.

**Step 1 — get the transcript out of the harness and onto disk.** Find where the
assistant stores conversations (VS Code keeps chat sessions as JSON under the
workspace-storage folder; other tools keep exports behind a menu). Copy, never move, and
never read application data folders with write intent. If nothing is exportable, have the
operator paste in chunks — a 3-month chat is worth an hour of copy-paste.

**Step 2 — convert to Markdown, one file per conversation or per day**, with a TSV index:
date · title · first message. Write this as a script; you will run it again.
Output goes to `inbox/`, not `raw/`.

**Step 3 — inventory before reading.** Produce a table: file, date, topic guess, size,
duplicate-of, decision (ingest / split / skip). Show it to the operator and get the
classification *before* any bulk reading. This is the single highest-leverage checkpoint
in the whole migration — it is where you discover that 40% is noise.

**Step 4 — redact and ingest.** Run the confidentiality script. Assign frontmatter.
Move to `raw/`. Commit. Secrets found: report the count.

**Step 5 — mine the code the chat produced.** Point a code-graph tool at the repositories
(see §11), and write `reference` articles that map modules, entry points and data flow.
Link to code; do not copy it.

**Step 6 — compile, in waves, oldest to newest.** One reader agent per coherent group of
sources, running in parallel, each returning a cited fact list. Then synthesize yourself.
Expect most waves to *update* existing articles rather than create new ones.

**Step 7 — harvest the decisions.** Sweep the transcript specifically for choices: "we
decided", "let's use", "that didn't work", "roll it back". Each becomes a candidate ADR.
Check the existing ADR numbers first. This step is usually where the operator says "I had
forgotten we rejected that".

**Step 8 — write `README.md`:** goal, accepted decisions with dates, current state, next
steps, open questions. From now on this is what a new session reads first instead of the
chat.

**Step 9 — lint to PASS, commit, and then delete nothing.** The giant chat stays as a
raw source. It is history.

## 11. Graph tooling

Two different things, both useful, both with a token trap:

- **Code graph** (e.g. `codegraph`): indexes a codebase into a local SQLite graph and
  exposes it over MCP, so the agent can ask "what calls this" without grepping. Install it
  **per project, locally**, never globally — its MCP server and per-message hook can add
  thousands of tokens to *every* message in *every* session, including sessions that never
  touch code. Turn telemetry off. In VS Code this is a `.vscode/mcp.json` entry scoped to
  the workspace.
- **Session graph** (e.g. `graphcode`): visualises live agent sessions and chains of
  autonomous loops. Useful for seeing what you are spending. Treat autonomous loops with
  suspicion: each loop iteration is a fresh session with its own context, and an unattended
  loop spends budget with nobody watching.

General rule for any MCP server: a server that is always loaded is a tax on every message.
Audit the always-on set the way you would audit a dependency list.

## 12. Porting to GitHub Copilot (VS Code)

The method is engine-agnostic; the plumbing is not. There is no plugin to install, so
rebuild the four moving parts as plain files:

| Need | Claude Code | GitHub Copilot in VS Code |
|---|---|---|
| Standing rules | `CLAUDE.md` | `.github/copilot-instructions.md` (and/or `AGENTS.md`) |
| Scoped rules | nested `CLAUDE.md` | `.github/instructions/*.instructions.md` with `applyTo:` globs |
| Repeatable operations | slash commands / skills | `.github/prompts/*.prompt.md`, invoked as `/name` |
| Persona per operation | sub-agent definitions | `.github/chatmodes/*.chatmode.md` |
| External tools | MCP config | `.vscode/mcp.json` |
| Deterministic work | scripts | the same scripts — they are just Python |

Concretely, write these prompt files first; they are the system's verbs:

- `/wiki-ingest` — classify `inbox/`, redact, assign frontmatter, move to `raw/`, commit.
- `/wiki-compile` — read sources for one topic, plan articles, write with citations, lint.
- `/wiki-query` — answer read-only from `wiki/` with exact file citations and nothing else.
- `/wiki-lint` — run the health checks, report, fix only the mechanical ones.
- `/wiki-adr` — capture a decision in MADR format with the next free number.
- `/wiki-session-end` — update `README.md` state, extract lessons, commit.

Two things will be weaker than in a plugin-based setup, so compensate deliberately:

1. **No enforced sub-agent model routing.** Copilot picks models per request, so you cannot
   pin "readers are cheap". Compensate by making reading a *script* wherever possible and
   by keeping digests short.
2. **No built-in lint.** Write `lint.py` yourself — frontmatter validity, link resolution,
   orphan files, index freshness, root-file whitelist, coverage-ledger completeness. 300
   lines, and it replaces a plugin.

Keep the wiki in **its own repository**, not inside the code repo, unless the code repo is
the only subject. Knowledge outlives codebases.

## 13. Bootstrap checklist

Day 1 — skeleton:
- [ ] New git repo, `main`, local identity set.
- [ ] `.gitignore` with `*.local.md` and session dirs.
- [ ] Directory tree from §2; `_index.md` in every directory.
- [ ] Agent instructions file from §§1–9, with the confidentiality list filled in for this
      project's actual risks.
- [ ] `README.md` with goal, decisions, next steps, open questions.
- [ ] Commit: `init: wiki skeleton`.

Day 2 — the verbs:
- [ ] `lint.py`, `redact.py`, `chat2md.py` (or equivalents) in `scripts/`.
- [ ] Prompt/command files from §12.
- [ ] One cost-reporting script.
- [ ] Commit: `tools: wiki scripts and commands`.

Day 3 — the migration:
- [ ] §10, steps 1–4. Stop at the inventory table and wait for the operator.

Then: one topic, one wave, one commit, one session. Repeat.

## 14. Anti-patterns

- Writing articles straight from the conversation without landing a source in `raw/`
  first. The article becomes unverifiable the moment the chat scrolls away.
- One mega-article per topic. Articles should be small enough that an update touches one
  file.
- Translating `raw/`. Ever.
- Letting the agent "tidy up" `raw/`.
- Global installation of token-heavy MCP servers.
- Delegating synthesis to sub-agents.
- Asking permission to commit.
- Treating lint warnings about missing `.local.md` sources as errors to fix.
- A second language tree instead of a deliverable.
- Autonomous loops without a budget cap and a human check-in.

---

## Appendix A — publishing this as a reusable system

If the operator wants to carry this to other projects, to colleagues, or home, the shape
is a small public repository, versioned, with the content strictly separated from the
method:

```
llm-wiki-method/
  README.md               # what this is, 20 lines, with the three promises from §0
  PLAYBOOK.md             # this document
  CHANGELOG.md            # versioned: the method evolves and forks need to track it
  templates/
    AGENTS.md.tmpl        # standing rules, with {{PLACEHOLDERS}}
    copilot-instructions.md.tmpl
    config.md.tmpl
    schema.md.tmpl
    adr.md.tmpl
    gitignore.tmpl
  prompts/                # the verbs from §12, harness-neutral Markdown
  scripts/                # lint.py, redact.py, chat2md.py, doc2md.py, cost.py
  profiles/
    claude-code/          # plugin/skill wiring
    copilot-vscode/       # .github/ layout
    plain/                # no harness: just the file conventions
  examples/
    minimal/              # a 5-article wiki that passes lint, so forks have a target
```

Rules that keep it shareable: no real content in the repo, ever — only templates and a
synthetic example; `CHANGELOG.md` so a fork can tell which version it diverged from; MIT
or CC-BY so colleagues can actually use it; and the confidentiality list shipped as a
*template with the categories named but the specifics blank*, because every organisation's
category 1 is different.

Version the method the way you version software, because the operator will run v1 on three
projects before v2 exists and will need to know which is which.

## Appendix B — a research direction, not a task

**Evolutionary search over agent configurations.** The idea: treat an agentic knowledge
system as a genome — which agents exist, their model tier, their prompts, the tool budget,
the chunking of sources, the compile strategy, the thresholds for "stale" and "duplicate" —
and search that space with a genetic algorithm (PIKAIA-style: real-valued genes, tournament
selection, adaptive mutation) instead of hand-tuning it one session at a time.

Why it is not obviously crazy:

- The design space is large, discrete-plus-continuous, non-differentiable, and full of
  interactions — exactly where GAs beat gradient methods and often beat humans.
- A **real fitness function exists** here, which is rare: for a knowledge system you can
  score a configuration on held-out questions with known answers — citation accuracy,
  coverage of sources, lint pass rate, contradiction detection recall, tokens spent per
  correct cited answer. Dollars-per-correct-answer is a legitimate objective.
- Evaluation is automatable end to end: fixed source corpus in, articles out, question set
  scored. No human in the inner loop.

Why it is hard, honestly:

- **Fitness evaluation is the cost.** One genome evaluation = a full compile + QA run.
  A population of 50 over 30 generations is 1,500 full runs. This only makes sense where
  the token budget is effectively unlimited, which is precisely the condition the operator
  describes on the other project.
- **Noisy fitness.** The same configuration scores differently on re-runs. Needs repeated
  evaluation or noise-tolerant selection, which multiplies the cost again.
- **Overfitting to the question set.** Hold out a second corpus or the result is a
  configuration that games the benchmark.
- Much of the space is better attacked by cheaper methods first: ablation studies, Bayesian
  optimisation over a handful of continuous knobs, or just measuring the top five
  hypotheses by hand.

A sane staging, if it is ever attempted:

1. Build the fitness harness alone — a fixed corpus, a question set with known answers, an
   automatic scorer. This is 90% of the value and is useful with no GA at all: it turns
   "this prompt feels better" into a number.
2. Hand-ablate five to ten configurations and see whether the scores even separate. If they
   do not, the search space is flat and evolution has nothing to find.
3. Only then, if scores separate and budget is free, run a small GA over the continuous
   knobs (thresholds, chunk sizes, model-tier mix) with the structural choices fixed.
4. Structural evolution — evolving the *prompts and the agent graph* — last, and treat it
   as research, not as tooling. Expect illegible winners.

Record the outcome as an ADR either way. "We tried evolutionary tuning and the fitness
landscape was flat" is a valuable, citable result.
