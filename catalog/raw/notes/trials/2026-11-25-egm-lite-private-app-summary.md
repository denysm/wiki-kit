---
title: "Use record summary: Elephant-Goldfish egm-lite, 17 diff reviews on a private native macOS app"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-25
ingested: 2026-11-25
repo: google/elephant-goldfish-model
part: egm-lite
version: "0.1.1"
status: in use
tags: [catalog, trial, use-record, kind-plugin, elephant-goldfish-model, egm, egm-lite, diff-review, swift, python, shell, summary]
summary: "Totals of 17 egm-lite use records from 2026-11-22 to 2026-11-25, each a fresh-reviewer diff review of a small change in the owner's private native macOS app (Swift, with Python and shell scripts): 35 rounds, 185 findings, 3 rounds with no finding, about 42.5 USD for the 16 records that priced their rounds. The per-change records are kept in the owner's private repository."
---

# Use record summary: egm-lite, 17 diff reviews on a private native macOS app

- **Tool and part**: google/elephant-goldfish-model, part `egm-lite`, version 0.1.1, read from a read-only clone and never installed: `main` at `7d1b721` (the skill unchanged since `70406c4`), re-read at `ef27af6` on 2026-11-24, where upstream #511 lets a standalone diff review resolve in chat with no checklist; rubric and reviewer contract unchanged.
- **How it was read**: Section 4 as a standalone diff review: the goal, the privacy rules and the accepted decisions, then the workspace diff, went to one fresh general-purpose subagent per round, read-only. Section 5 triage was shown to the owner before any fix.
- **Task, by kind**: small changes and fixes in a native macOS app written in Swift, and in its Python and shell scripts, each reviewed as a diff, round after round until a round passed at the P1 bar or the owner stopped.
- **Kind of record**: real use with the owner's standing yes. The 17 per-change records moved to the owner's private repository on 2026-11-25, because together they described that private app; this summary keeps their totals here. Status after it: `in use`.

## Result

| What | Value |
|---|---|
| Records | 17, from 2026-11-22 to 2026-11-25 |
| Rounds | 35 (one to five per change) |
| Findings | 185 |
| Rounds with no finding | 3 |
| Cost | about 42.5 USD in subagent tokens for the 16 records that priced their rounds; the main session's triage and fixes not counted |

- In several records the second round caught a defect that the first round's fixes had brought in.
- Findings named file and line ranges, quoted SDK headers as evidence, and marked what the reviewer could not verify; some reviewers built a small harness or simulated a fixture in a script to show a fault.
