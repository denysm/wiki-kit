---
title: "Use record: Elephant-Goldfish egm-lite, two diff-review rounds on a leak check's new flags, two pre-push hooks and a per-Mac setup script"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-25
ingested: 2026-11-25
repo: google/elephant-goldfish-model
part: egm-lite
version: "0.1.1"
status: in use
tags: [catalog, trial, use-record, kind-plugin, elephant-goldfish-model, egm, egm-lite, diff-review, shell, bash, git-hooks, python]
summary: "egm-lite read from the clone at ef27af6 (upstream had 1 newer commit, none in skills/egm-lite), two standalone diff-review rounds across two repositories: a leak check gaining two flags, two pre-push hooks and a bash 3.2 setup script for an IDE's agent tools. Round 1: 9 findings (4 P1), 8 fixed, 1 contested. Round 2: all fixed, 2 new P2 that the fixes had caused, fixed and covered by tests. Round 2 was cut by a network error and resumed with a message."
---

# Use record: egm-lite, two diff-review rounds on a leak check, two hooks and a setup script

- **Tool and part**: google/elephant-goldfish-model, part `egm-lite`, version 0.1.1, read from the clone at `ef27af6`; upstream had 1 newer commit, none of it in `skills/egm-lite`.
- **How it was read**: Section 4 as a standalone diff review (no checklist): the reviewer got numbered requirements and the diffs of two repositories plus the new untracked file; fresh general-purpose subagents, read-only, probes only in throwaway clones and temporary folders. Section 5 triage shown to the owner before fixes; the owner then said to do everything that could be done while away, which covered round 2's fixes.
- **Task, by kind**: a public kit's leak check gains `--more-names` (extra name lists, a missing file skipped) and `--private-repo` (data paths allowed in a private repository, names and secrets still refused); the kit's pre-push hook passes a list of names refused only in the public kit; a private repository's pre-push hook uses the leak check; a new bash 3.2 script sets up an IDE's MCP bridge and five vendor skills for a coding agent, with a report-only mode an agent may run.
- **Kind of record**: real use with the owner's standing yes. Status after it: `in use`.

## Result

| Round | Findings | Highest | Notes |
|---|---|---|---|
| 1 | 9 | P1 | The private repository's hook checked only HEAD, not the pushed refs, so another branch could carry a secret out (a gap older than the change); appending to an ignore file with no final newline glued the header onto its last rule, so `.env` stopped being ignored; tracked files made every run append the ignore lines again; a skill folder without its main file was copied into, overwriting the owner's files. Also: the report-only flag was read only as the first argument; a failed export stopped the script with no report; a folder inside `.git` got an ignore file; a wrong "names not checked" warning; no test of the new flags. One contested: the report-only mode was said to raise the IDE's approval prompt, while a trial had shown the bridge answers its first calls with no approval. |
| 2 | 2 | P2 | All round 1 fixes confirmed. New, caused by the fixes: the kit's hook would check the whole history when pushing to a remote never fetched, and the public history already holds names the new list refuses, so such a push would always fail (fixed: the base falls back to what any other remote has; a live push to a fresh bare mirror passed, the old hook refused it); the setup script's ignore-file header named the private repository and would carry that name into whatever repository it set up (fixed: lines go to the clone's own `info/exclude`, which is never committed, under a neutral header). |

- What it added: both round 2 findings came from the round 1 fixes; one would have published a private name through an innocent comment line.
- The setup script now has 24 tests (macOS `/bin/bash` 3.2, a stub for the agent's CLI, so the real configuration is never touched); the leak check's flags have a CI step that fails on the old code.
- Round 2 stopped on a network error midway and was resumed with a message; it finished from its saved state.

## Cost

Round 1: 82571 subagent tokens (13 tool calls, about 4 minutes). Round 2: 84110 (12 tool calls; wall time stretched by the network pause). Together 166681, about 1.9 USD.
