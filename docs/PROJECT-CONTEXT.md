---
title: "wiki-kit — project context and key decisions"
source: "conversation between the owner and Claude Code, 2026-10-25..26"
type: notes
ingested: 2026-10-26
authors: [owner, Claude]
source_date: 2026-10-26
tags: [wiki-kit, public-repo, planning]
---

# wiki-kit — project context and key decisions

Why this file exists: it carries the main conclusions of the planning conversation about publishing the method as a repository, so a new session (at home, on another machine, or by a collaborator) does not start from zero. It is a summary, not a transcript.

## Goal

1. Develop the llm-wiki method (rules, agents, scripts) from two computers at once and keep one history, so work on either machine adds to the other.
2. Let other people install the same system from simple instructions, including non-specialists: an editor, an AI assistant they can afford, one command to install, plain-language steps.
3. Start private: a private repository with chosen collaborators. Public later, only after a second leak check.

## What the repository is

`wiki-kit` is the method only, with no data: playbook, hub rules template, agents, standard-library scripts, docs. It is like the shared toolbox of an office; the wikis are the filing cabinets.

- Data (topics, raw sources, anything about a client, employer or person) never enters the repository. `.gitignore` excludes `topics/`, `raw/`, `inbox/`, `*.local.md`. The hub lives outside the repository (for example `~/wiki`).
- Lists that would reveal an organisation (internal domains, client names) stay in `~/.config/wiki-kit/`, never in the repository: the list itself would be the leak.

## Several wikis, one kit

The owner runs several independent wikis (personal, work, client projects). They are separate knowledge bases, not cooperating workers: each has its own rules and access, a client's data never crosses into another wiki, and nothing moves from a shared layer back into a client wiki.

- Method flows from the kit to every wiki (`git pull`).
- Lessons flow back to the kit only by hand, de-identified by the owner (no names, figures or clients). `/wiki:ll` can extract lessons from a session; keep only the generic part.
- Data flows nowhere.
- Running sessions in several wikis in parallel works, but each session pays for its own context.

## Two-computer workflow

- First commit comes from the machine that holds the clean copy; the other machine pulls.
- Before work `git pull`; after work a small commit and `git push`. Different files are edited, so conflicts are rare.
- Leak protection: a `pre-push` hook running `raw_check.py` plus a search for the private names list, and the same checks in CI on every push.
- Per-repository git identity (personal name and address only). Use a separate credential for the personal account on any machine that also holds another account.

## Beginner installation (target)

1. Install VS Code. 2. Install the Claude Code extension (the extension is free; model access is paid). 3. Paste one line in the terminal: it installs dependencies, the `wiki@llm-wiki` plugin pinned to v0.25.1, agents and scripts, creates a hub, and runs a self-check. 4. Sign in once, or paste an API key.

Cannot be automated: installing the editor, signing in, paying. Windows needs its own script and its own test.

Model choice by budget: the plugin runs on Claude Code and, per its own description, on Codex and OpenCode; the playbook (section 12) covers GitHub Copilot in VS Code. Which cheaper or local models can actually run ingest and compile has **not been verified** — verify before promising it.

## Roadmap

1. Import this export at home, merge with the newer home version, leak check, first commit to a private repository. (Done.)
1a. Dogfood the specialist department (below) in the owner's own hub before inviting anyone: run each specialist's evaluation cases and a few real requests, compare `development-coach` with the owner's personal coach on one real goal, turn lessons into 0.2 versions.
2. `bootstrap.sh` (macOS, Linux) and `bootstrap.ps1` (Windows); test on a clean user account or VM. `bootstrap.sh` done 2026-10-27, tested on macOS with an empty home folder (plugin really installed, re-run safe, clone path); `bootstrap.ps1` written 2026-10-27 for the first tester, who uses Windows, and tested in CI on a clean Windows machine (PowerShell 5.1): first run 18 ok, re-run clean; the winget install of Git and Python is not covered (CI machines have both). Clean account, VM and Linux still open.
3. `docs/QUICKSTART.md` in plain language with screenshots. Done 2026-10-27 in English and Russian (`QUICKSTART.ru.md`), without screenshots. Ukrainian (`QUICKSTART.uk.md`) and the installers' `--lang uk` added 2026-10-30.
4. `pre-push` hook (leak check with the private names list) and CI checks (`raw_check.py`, `llm-wiki specialist validate` on a temporary hub) — needed before collaborators send pull requests. Hook done 2026-10-27 (`scripts/leak_check.py`, also checks history of unpushed commits); CI done 2026-10-27 (`checks` on every push, `installers` on Ubuntu and Windows); it has no private names list, so the hook stays the main guard. Contribution path added 2026-10-30: `CONTRIBUTING.md`, a pull request template, and a section in each quickstart (GitHub account, noreply email, fork, pull request); `main` is protected from deletion and force-push.
5. Hand it to one non-specialist, record where they get stuck, fix, repeat.
6. Choose a licence; only then consider making it public. Licence chosen 2026-10-30: MIT (the same as nvk/llm-wiki). The public repository starts with a fresh one-commit history, so the private history (with the owner's real e-mail) is not published.

## Specialist department (2026-10-26)

- `specialists/`: 11 personal specialists in five divisions; `development-coach` is 1.2.0, the other ten are 0.1.0 drafts. Front desk: `skills/department` (asks the user's language on the first conversation, routes by meaning, safety first). Skeleton: `templates/specialist/`. Staff, rules, vacancies and roles: `specialists/README.md`.
- Model: shared core in the kit, personal tuning in `references/*.local.md`, facts about the person only in their wiki; de-identified lessons come back by pull request; any language, originals kept with a `lang` tag.
- Status: format-validated only. No specialist has been tested on real requests yet (the plugin's eval gate: compare with the no-specialist baseline before enabling broadly).
- People: a safety reviewer with psychology training (planned); a physician, a financial or tax adviser and a lawyer are needed before the high-risk specialists reach 1.0.
- Descriptions stay under the 1024-character Agent Skills cap and short, since they are read on every routing; trigger tables live in `references/`.

## Third-party skills (2026-11-06)

Reviewed for reuse: `obra/superpowers` (MIT), `blader/humanizer` (MIT), the `kaizen` plugin of `NeoLabHQ/context-engineering-kit` (GPL-3.0). They teach techniques, not roles, so they feed the specialists instead of joining the department.

- Taken, in the kit's own words: the skill-testing method of superpowers `writing-skills` (`docs/testing-specialists.md`); interview rules of its `brainstorming` (the specialist template); "no completion claim without a fresh check" from `verification-before-completion` (`agents/COMMON.md`); AI-tell categories after humanizer, plus Russian and Ukrainian lists (`career-documents-reviewer/references/ai-tells.md`); five whys, PDCA and A3 (`development-coach/references/methods.md`, `decision-analyst`).
- Not taken: the superpowers plugin as a whole (its session-start hook injects a "use a skill before any response" rule into every session, and its brainstorm server loads a remote logo unless telemetry is turned off); kaizen as a plugin (code-specific, auto-triggered) or any of its text (GPL); humanizer as a vendored copy (it stays an optional skill installed from upstream).
- Next: run `docs/testing-specialists.md` on `conversation-prep` and `career-documents-reviewer`; existing specialists adopt the template's conversation rules on their next version.

## Memory and orchestration (2026-11-13)

Three steps, one session each, in this order:

1. **Recall: `scripts/search.py`.** Full-text search over `raw/`, `wiki/`, `output/` with SQLite FTS5 (BM25, stdlib only), chunked by heading, answers as `path:line` plus a snippet. The index is a cache in `~/.cache/wiki-kit/search/`, never in a repository (it holds text of `.local.md` files), one index per wiki root; several roots are searched together only when named explicitly. `search.py eval` measures recall on a local question set (`~/.config/wiki-kit/search-eval.tsv`; questions about real content never enter the kit). In the same session the write-audit hook moves from a per-hub `.claude/` (the llm-wiki hub lint does not allow it at a hub root) to user-level settings that call a kit script, which acts only on files inside a wiki root and logs to `~/.cache/wiki-kit/audit/`.
2. **Foreman: `skills/foreman/`.** Takes a task, writes a work order (goal, done criteria, budget, deadline, where results go), proposes a team from a roster (an HR step: `scripts/roster.py` lists specialists, Claude Code agents, outside models from `council.py` and open vacancies) with a cost estimate, and hires only after the user's yes. Temporary hires are briefed subagents for one task; a role hired twice becomes a draft specialist from `templates/specialist/`. Then parallel work, quality control (`source-skeptic`, `check_evidence.py`), acceptance against the done criteria, and a closing step that files lessons. The department stays the front desk for one-specialist conversations and owns the safety rule. Human touch comes from the forms (work order, staffing table, acceptance, a short reference on each member's work), not from invented people: the "methods, not people" rule stands.
3. **Orchestrator and local RAG.** Decide on embeddings by measurement: local model only (texts of clients never go to an outside embedding service), hybrid with the BM25 index from step 1, adopted only if `search.py eval` shows recall gains worth the dependency, especially for questions asked in one language about sources in another. The orchestrator joins step 2 with memory: search before the work, lessons and specialist tuning after it, so knowledge only grows.

Step 1 done (2026-11-13). `search.py` default mode is hybrid (reciprocal rank fusion of exact words and stem-prefix matching) on a plain unicode61 index; Porter stemming and a trigram index measured worse and larger and were dropped. Baseline on a local set of 20 questions (12 over one hub's tool notes, 8 over a customer wiki's infrastructure material; 11 answers only in `raw/`, 5 cross-language): recall@5 0.95, recall@10 0.95. Other modes at recall@5/@10: exact-only 0.90/0.95, prefix-only 0.80/0.95, Porter 0.85/0.95, trigram 0.75/0.85. Cross-language subset: 0.80 at both cut-offs. Build time 0.3 s for 460 files (19 MB index) and 0.1 s for 233 files (10 MB); a query takes about 0.05 s. The set is small, so differences of one question are noise; re-run `search.py eval` when the set grows. The write-audit hook now lives in `scripts/wiki_write_audit.py` at user level.

Step 2 done (2026-11-13). `skills/foreman/` (SKILL.md plus `references/forms.md`: work order, staffing table, brief, member report, acceptance record, report, reference on a member's work), linked by both installers. `scripts/roster.py` is the HR step: specialists from the hub's `.skills/`, Claude Code agents, the four built-in agents, outside vendors that `council.py` could call (names only), vacancies, and a hire log in `~/.config/wiki-kit/foreman/hires.tsv` that flags a temporary role hired twice. Cost estimates come from a new `agents` report of `claude_usage.py`: cost per subagent run by agent type (from each run's `.meta.json`) and model family, median and p90; a family with fewer than 3 runs gets a row derived from the Sonnet median by list-price ratio. On the owner's machine, 110 runs since 2026-08-15: `wiki-reader` on Sonnet median $0.25 (p90 $0.95), `wiki-compiler` on Sonnet $0.50 ($2.36), `general-purpose` on Sonnet $0.44 ($0.72) and on Opus $1.92 ($9.06). Checked the same day: two dry runs (order and staffing only) — testing `conversation-prep` by `docs/testing-specialists.md` (3 members, estimate $1.65, upper bound $4.55) and resolving `check_evidence.py` warnings in a work topic (1 member, $0.50, upper bound $2.36); one real task with the owner's yes — the structure of the 11 specialists (Non-claims, Do not use when, version): one temporary Haiku hire, estimate $0.02, measured $0.01, no gaps, confirmed by an independent re-check; lessons filed with `/wiki:ll`. Open: the foreman's safety rule does not say whether crisis wording inside test fixtures counts (the `conversation-prep` Safety case); a change needs the safety reviewer.

Knowledge is kept by the existing rules (immutable `raw/`, git, `sources:`, outdated claims marked rather than deleted); steps 1 and 3 are about finding it, step 2 about adding to it from every task.

## Open questions

- Which non-Claude models are good enough for the agents, at what cost.
- Whether to ship a sample empty hub (skeleton) or generate it with `/wiki init` only.
- Who among the first users can review the high-risk specialists (health, money, paperwork).
