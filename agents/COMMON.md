# Common instructions for wiki ingest + compile agents

The orchestrating session passes each agent: ROOT (one wiki root, sometimes two), SCRATCH (the agent's own scratch directory), TODAY (YYYY-MM-DD), and the list of inbox files and documents to process. You own exactly ROOT and SCRATCH. Everything else is read-only for you.

## Read first

1. `~/wiki/CLAUDE.md` — the rules: confidentiality, sources, binary files, language, ADR format. They apply in full. For a separate wiki repository also read its own `CLAUDE.md`; a private wiki of the owner's own data may override the HR rule for that data.
2. Plugin protocols in `~/.claude/plugins/cache/llm-wiki/wiki/0.25.1/skills/wiki-manager/references/`: `compilation.md`, `indexing.md`, and in `wiki-structure.md` the sections "Source File Format", "Wiki Article Format", "Source Reference Resolution", "Volatility Classification", "Dual-Link Convention".
3. ROOT's `config.md`, `schema.md`, `_index.md`, `wiki/_index.md` and every existing article (if any) before planning.

House style example: any existing finished article in the same topic (for example one concept and one ADR). Match its frontmatter, structure, tone and length.

## Step 0 — Check routing

Read the first ~60 lines of every file you are given before ingesting it. If it is about another client, another project or is HR material, do not ingest it: leave it in `inbox/` and report it. Routing by tag or folder name is unreliable: a name in a tag can belong to a different organisation than expected.

## Step 1 — Ingest

**Triage first.** After Step 0, label each source in `SCRATCH/notes.md` as `New` (nothing on it in the wiki yet), `Update` (adds to or changes an existing article), `Disputed` (contradicts an article) or `No material` (nothing the wiki needs). A `No material` source is still ingested to `raw/` but gets no article: list it with the reason in `wiki/references/uncompiled-source-coverage.md`. Do not stretch it into an article.

**Files in `ROOT/inbox/`** (chat and Cowork-session exports already converted to Markdown with frontmatter): move each into `ROOT/raw/notes/` keeping the name. Fix frontmatter: `type: notes`, `ingested: TODAY`, deduplicated `tags`, and `source`, `authors`, `source_date` present (write `unknown` rather than guess).

**Documents** (originals in your cloud drive or document system — never move, rename or delete them): extract to Markdown in `ROOT/raw/` (`notes/` for working documents, `papers/` for published papers, `articles/` for web/Confluence pages, `data/` for spreadsheets).
- Converter: `cd SCRATCH && uv run --no-project --with python-pptx --with python-docx --with pypdf python -I ~/Projects/wiki-kit/scripts/doc2md.py plan.json`. Read its docstring for the plan.json format. It handles .pptx, .docx, .pdf, .md, .txt and refuses to overwrite.
- `.xlsx`, `.xmind`, `.rtf`, `.eml`, `.vtt`, `.html`, `.webarchive`: use `markitdown <file>`, `textutil -convert txt` (macOS) or unzip into SCRATCH, then write the raw file yourself with the same frontmatter fields doc2md writes.
- Several versions of a document: ingest the latest only and say in `summary` which version it is; skip exact duplicates (compare MD5 or extracted text).
- Image-heavy key decks: `soffice --headless --convert-to pdf --outdir SCRATCH <file>`, read the PDF, add a short description of image-only slides (no hostnames, bucket names or internal URLs).
- Naming: `YYYY-MM-DD-<slug>.md` by `source_date`. Use `.local.md` for documents authored by a client or partner, for meeting transcripts, and for anything exported from a system with its own access control (wiki, document store, tracker, mail). Documents authored by you are plain `.md`.
- `source:` is the original's path written with `~`.

**Confidentiality check on every raw file before it stays** (CLAUDE.md categories):
- Secrets (tokens, passwords, keys, internal URLs — internal wiki and tracker hostnames, document-store links, meeting join links, meeting IDs and passcodes, dial-in numbers, tenant keys — hostnames, account IDs, infrastructure addresses): replace with `[REDACTED:secret]`. Report each kind and count.
- HR and private personal data — assessments of named people, candidate CVs and evaluations, interview feedback, feedback on someone's work or behaviour, grades, salaries/rates of individuals, health, family, home location, personal reasons for absence, private phone numbers: remove the passage, leave `[omitted: HR]`. This is the one edit allowed to raw text at ingest. Role definitions and job descriptions are fine.
- Customer/prospect names and commercial terms: in a hub topic only where the project needs them, with `sensitivity: confidential` on the raw file and article. In a customer repository mark every raw file and article `sensitivity: confidential`. Never write another customer's name into a customer repository; generalise it ("another client").
- Sensitive but fits no category: leave it out of articles and list it in your report as a question.

Append one line per ingested source to `ROOT/log.md`: `## [TODAY] ingest | <title> (<raw path>)`.

## Step 2 — Compile

Follow `compilation.md`. Plan articles first (concepts = bounded mechanisms; topics = broad themes; references = maps, timelines, people/roles, ADRs). Then write them in `ROOT/wiki/{concepts,topics,references}/`:
- Full frontmatter: `title`, `category`, `sources` (exact raw paths, block list), `created`/`updated`/`verified` = TODAY, `tags`, `aliases`, `confidence`, `volatility`, `summary`, plus `sensitivity` where required.
- Abstract blockquote, synthesized sections (explain, do not paste), `## See Also` with bidirectional dual links (`[[slug|Name]] ([Name](../category/slug.md))`), `## Sources` listing raw files with what each contributed.
- Decisions become ADRs in `wiki/references/adr-NNNN-<slug>.md` (numbered per wiki, continuing existing numbering), MADR sections as CLAUDE.md specifies, `status`, `decided`, `compiled-from: mixed` when made in a chat. A decision that was only proposed stays `proposed`.
- Existing articles: integrate new facts with Edit, do not rewrite; bump `updated`.
- Record contradictions between sources instead of picking a side; say when a number is a claim from a deck rather than a measurement.
- Status blocks: when a newer source replaces or contradicts a claim, do not rewrite the claim. Keep it and add under it `> **Status: Outdated** — <what changed>; see [source](path), <date>.` or `> **Status: Disputed** — <the other claim>; see [source](path).` Say which source is newer. A fully replaced decision is an ADR (`superseded`), not a status block.
- Grounding: every number, ISO date and quoted phrase in the body must appear word for word in a raw file the article cites. A figure you derive yourself (sum, ratio) is written as derived and names its inputs.
- Articles in English. No HR material, no secrets.
- Coverage: every raw file is cited by at least one article or listed, with a reason, in `wiki/references/uncompiled-source-coverage.md` (rewrite it to the current state; create it if missing).

## Step 3 — Lint and indexes

- Hub topic: `cd ~/wiki && ~/.claude/plugins/cache/llm-wiki/wiki/0.25.1/bin/llm-wiki lint --wiki <name> --fix`, then again without `--fix`. Never lint the hub root with `--fix`.
- Repository or private wiki: `~/.claude/plugins/cache/llm-wiki/wiki/0.25.1/bin/llm-wiki lint <ROOT> --fix`, then again without `--fix`.
- Fix findings until PASS.
- Then run `python3 -I ~/Projects/wiki-kit/scripts/check_evidence.py ROOT`. Fix every error (missing source, broken link). For each warning (`number-not-in-sources`, `quote-not-in-sources`, `date-not-in-sources`) open the cited raw file, then correct the article or mark the value as derived; do not leave a warning unexamined. Report the final counts.
- Update `ROOT/_index.md` statistics (sources, articles, Last compiled, Last lint, Recent Changes) and the totals in `ROOT/raw/_index.md`. Append `## [TODAY] compile | N sources → X new articles, Y updated (slugs)` to `ROOT/log.md`.

## Do not

- Do not touch git, the hub root files (`README.md`, `log.md`, `_index.md`, `wikis.json`, `CLAUDE.md`), other wikis or topics, or any original document.
- Do not read personal documents that sit next to work files (passports, residence permits, criminal records, payslips, diplomas, contracts, medical files, consent forms). Open only the files your task names or that are clearly work material.
- Do not fill gaps from your own knowledge; the wiki states only what its sources say.

## Report (your final message, under ~800 words)

Sources ingested (paths); skipped files and why; articles created and updated (paths); ADRs with status; confidentiality actions (count of secrets redacted, kinds of HR material omitted, files marked confidential); lint result; open questions for the user.
