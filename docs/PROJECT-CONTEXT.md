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

## Open questions

- Which non-Claude models are good enough for the agents, at what cost.
- Whether to ship a sample empty hub (skeleton) or generate it with `/wiki init` only.
- Who among the first users can review the high-risk specialists (health, money, paperwork).
