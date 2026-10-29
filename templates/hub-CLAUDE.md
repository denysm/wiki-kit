# {HUB_NAME} — rules for AI agents

Knowledge hub run on the nvk/llm-wiki plugin (`wiki@llm-wiki`, pinned to v0.25.1). One topic per area under `topics/<name>/`. Read `README.md` at the start of a session.

## Layout

- Hub root holds only `wikis.json`, `_index.md`, `log.md`, `topics/`, `README.md`, `CLAUDE.md`, `.gitignore`. Other files there are flagged by lint; never run `lint --fix` on the hub itself, only on a topic.
- Originals (documents, spreadsheets, PDFs, presentations) never go into the wiki. They stay where they are; `raw/` holds a Markdown extract whose `source` points to the original.
- Code stays outside the wiki. The wiki links to it and describes it, never copies it.

## Language

- Compiled content (`wiki/`, `output/`, `config.md`, `schema.md`) is written in {WIKI_LANGUAGE}.
- Raw sources (`raw/`) keep their original language; never translate them in place.
- Talk to the user in {CHAT_LANGUAGE}.

## Confidentiality

- Secrets (tokens, passwords, keys, private URLs, infrastructure addresses) are never stored anywhere, `raw/` included. Replace them on ingest with `[REDACTED:secret]` and tell the user.
- Other people's private data (assessments, health, finances, private contacts) is not stored. Professional facts (name, role, expertise) are allowed.
- Anything that belongs to someone else (a client, an employer) goes in its own separate wiki with its own access rules, never in this one.
- When something looks sensitive but fits no rule, treat it as confidential and ask.

## Sources

- Every factual claim in `wiki/` traces to a file in `raw/` through the article's `sources:` frontmatter and its `## Sources` section.
- Raw frontmatter records `title`, `source`, `type`, `ingested`, `authors`, `source_date`. When unknown, write `unknown`; do not guess.
- Every number, ISO date and quoted phrase in an article appears word for word in a raw file it cites. Run `scripts/check_evidence.py <topic root>` after every compile: fix errors, examine each warning against the raw file.
- A newer source that replaces a claim does not rewrite it: the old claim stays with a `Status: Outdated` or `Status: Disputed` note. A replaced decision is a superseding ADR.
- Triage each new source as `New`, `Update`, `Disputed` or `No material`; a `No material` source gets no article.

## Decisions (ADR)

- MADR format, `wiki/references/adr-NNNN-<slug>.md`, tag `adr`, frontmatter `status` (proposed | accepted | rejected | deprecated | superseded) and `decided: YYYY-MM-DD`.
- Sections: Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (with Consequences), Pros and Cons of the Options.
- Never rewrite an accepted ADR. A new ADR supersedes it.

## Cost discipline

What costs money is context that every later call re-reads, not the model's answers.

- Scripts before models: deterministic work (conversion, checks, lint, usage report) runs as a script in `scripts/`; the session reads its summary only.
- One task per session; restart when the context passes ~150k tokens, noting the state in `README.md` first.
- A cheaper model reads and compiles (`wiki-reader`, `wiki-compiler`); the strongest model plans and reviews.
- Keep tool output small: `head`, `grep`, ranged reads; never dump whole files.

## Git

- Commit after each completed wiki operation (`ingest: …`, `compile: …`).
- Raw files that must not leave this machine are named `*.local.md` and excluded by `.gitignore`.
