---
title: "Use record: Elephant-Goldfish egm-lite, one diff-review round on a skill router turned from a flat list into a tree"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-25
ingested: 2026-11-25
repo: google/elephant-goldfish-model
part: egm-lite
version: "0.1.1"
status: in use
tags: [catalog, trial, use-record, kind-plugin, elephant-goldfish-model, egm, egm-lite, diff-review, python, agent-skills, routing]
summary: "egm-lite read from the clone, one fresh-reviewer round on a change that turns a front-desk skill's flat list of method packages into a tree of divisions with a graph of handoffs, a Python map script and a CI check: 9 findings (2 P1: a crash on a Windows code page, a package that vanished from routing when its division had no parent row), all 9 fixed after the owner's triage; no second round, since the fixes were small and each was re-run by hand."
---

# Use record: egm-lite, one diff-review round on a skill router turned into a tree

- **Tool and part**: google/elephant-goldfish-model, part `egm-lite`, version 0.1.1, read from the clone (Sections 4 and 5).
- **How it was read**: Section 4 as a standalone diff review: the written plan, then the full workspace diff with new files, to one fresh general-purpose subagent, read-only, allowed to write only into a throwaway folder (a copy of the package library, a redirected home folder, Python 3.9). Section 5 triage shown to the owner, who answered `exec` for all items.
- **Task, by kind**: a front-desk skill had listed every method package and its triggers in its description, close to the 1024-character limit. The change places each package in a tree with one frontmatter key, keeps the divisions in a Markdown table, adds a stdlib map script that prints one level at a time and a `--check` mode for CI, and rewrites the front desk to name divisions only.
- **Kind of record**: real use with the owner's yes. Status after it: `in use`.

## Result

| Round | Findings | Highest | Notes |
|---|---|---|---|
| 1 | 9 | P1 | P1: the map's output crashed under a Windows code page (the isolated interpreter ignores the UTF-8 environment switches); a personal package vanished from the top level, without a warning, when its subdivision had no parent row. P2: a shell variable the skill told the agent to reuse between separate shell calls; "names no specialist" was true of the description only; the top level escaped the 12-children limit; a package named like a division could not be reached; the package template lacked the new key; a stale README sentence; trigger phrases dropped from the only entry point the agent sees; an unused field. |

- What it added: the reviewer reproduced every finding in its throwaway copy, and confirmed that the CI check fails on each regression it claims to catch. Two of the P2s (the shell variable and the dropped phrases) concern how an agent reads the skill, which the author's own route tests had not exercised.
- Fixes: all 9, each re-run by hand (missing parent row, 13 top-level divisions, a name clash, the full command in every call). The Windows code page could not be reproduced on macOS; the fix is a stream reconfigure at start.
- No second round: the fixes were small and each was checked by a run.

## Cost

Round 1: 130736 subagent tokens (42 tool calls, about 5 minutes), about 2.1 USD by the session's usage report.
