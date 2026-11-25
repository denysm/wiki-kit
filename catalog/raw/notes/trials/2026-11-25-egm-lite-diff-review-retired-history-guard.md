---
title: "Use record: Elephant-Goldfish egm-lite, four diff-review rounds on a leak-check rule that keeps a rewritten history's dropped files out"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-25
ingested: 2026-11-25
repo: google/elephant-goldfish-model
part: egm-lite
version: "0.1.1"
status: in use
tags: [catalog, trial, use-record, kind-plugin, elephant-goldfish-model, egm, egm-lite, diff-review, git, git-hooks, python, history-rewrite]
summary: "egm-lite read from the clone at ef27af6, four fresh-reviewer rounds on a pre-push leak-check rule written before a public repository's history rewrite: a file listing the cutoff time and hashes of dropped paths and lines, so that a clone made before the rewrite cannot push the old history back. 7, 6, 5, then 1 findings; P1s in rounds 1 to 3; round 4 passed at the P1 bar. One P1 lies outside any in-repository check and was covered by repository rules on the host and by resetting old clones first."
---

# Use record: egm-lite, four diff-review rounds on a rule against a rewritten history coming back

- **Tool and part**: google/elephant-goldfish-model, part `egm-lite`, version 0.1.1, read from the clone at `ef27af6`.
- **How it was read**: Section 4 as a standalone diff review: goal, numbered requirements and scenarios, then the workspace diff, to one fresh general-purpose subagent per round, read-only, with probes only in throwaway repositories (bare remotes, old clones, a real filter-repo rewrite, a home folder with no name lists, Python 3.9). Section 5 triage shown to the owner before each set of fixes.
- **Task, by kind**: a pre-push leak check gains a rule for a repository whose public history is about to be rewritten: a tracked file holds the rewrite's cutoff time and hashes of the dropped paths and lines; the check refuses them in the tree and in pushed commits, and refuses commits authored before the cutoff that the remote does not have.
- **Kind of record**: real use with the owner's yes. Status after it: `in use`.

## Result

| Round | Findings | Highest | Notes |
|---|---|---|---|
| 1 | 7 | P1 | A push to a new branch skipped the rule (the file was read only from the pushed tree); re-authored content (a soft reset and a new commit, a dropped file kept in a rebase conflict) passed the date-only rule. Also: malformed lines turned the rule off in silence, the rule refused the owner's own force push, recovery advice that looped back into a refusal, one report line per old commit, CI gaps. |
| 2 | 6 | P1 | All round 1 fixes held, with no false positive on the rewritten history. The P1 lies outside the repository: an old clone that runs `reset --soft` or `merge -s ours` pushes with its own old checker. Also: advice that exported the old history again after a fetch, history parsing blind under the pusher's `diff.noprefix`, time formats read differently by Python 3.9, path hashes that confirm an exact guess (accepted). |
| 3 | 5 | P1 | Paths with a space (git's trailing TAB) or C-quoted paths were not parsed in history. Also: rename detection hid a rename into a dropped path, `log.showRoot=false` hid the root commit, a reset advice with no target, tests that counted a crash as a refusal. |
| 4 | 1 | P2 | Passed at the P1 bar. Binary and empty files have no `+++` line, so their paths were taken from `--raw` instead (fixed, with tests). |

- What it added: each round's probes found what the author's own tests had not: three ways around the rule, two of them caused by fixes of the round before. The fourth reviewer also ran mutants (each fix removed in turn) to show the tests catch it.
- The one P1 no in-repository check can close was handled outside it: host rules against force pushes, merges, new branches and tags, and a reset of the one old clone before its agent runs again.
- Tests: a shell script of throwaway repositories, run in CI on Python 3.9 and 3.13; it fails on the code before the rule.

## Cost

Round 1: 110849 subagent tokens (16 tool calls, about 7 minutes). Round 2: 125193 (33 tool calls, about 10 minutes). Round 3: 91031 (14 tool calls, about 5 minutes). Round 4: 80850 (16 tool calls, about 4 minutes). Together 407923, about 5.5 USD at the rate of the earlier records.
