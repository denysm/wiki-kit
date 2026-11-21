---
title: "Use record: Elephant-Goldfish comprehension persona, reviewing a catalog design document"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: google/elephant-goldfish-model
part: comprehension
version: "0.1.1"
status: in use
tags: [catalog, trial, use-record, kind-plugin, elephant-goldfish-model, egm, comprehension, design-review]
summary: "The comprehension persona of google/elephant-goldfish-model 0.1.1 (main at 70406c4), read from a read-only clone and not installed, was used in real work on 2026-11-21: a fresh agent in that role reviewed a tool-catalog design document and its sample card against the kit's card standard. Result: one Blocker and four Major findings; one fix pass then made the sample card pass all 29 checks. Cost: 81753 tokens."
---

# Use record: Elephant-Goldfish comprehension persona, reviewing a catalog design document

- **Tool and part**: google/elephant-goldfish-model, part `comprehension` (`agents/comprehension.md`).
- **Version**: 0.1.1 by the manifest, read at commit `70406c4` of `main` (the desk check's clone), 48 commits after the `v0.1.1` tag. The persona file is unchanged on `main` up to 2026-11-20.
- **How it was read**: a fresh general-purpose subagent on the Opus model was told to take the role in `$EXTERNAL/elephant-goldfish-model/agents/comprehension.md`. The plugin was not installed or loaded, so the Claude adapter (read-only tools, `omitClaudeMd`) did not apply. The `egm-review` and `egm-review-loop` skills were not run: one reviewer, one round, no synthesizer.
- **Task, by kind**: a review of a tool-catalog design document and its sample card against the kit's own card standard (a standard written in the form of the Elephant-Goldfish document standards).
- **Date**: 2026-11-21.
- **Kind of record**: real use, not a sandbox trial. Status after it: `in use`.

## Result

- One Blocker: the sample card lacked a frontmatter field that the freshness check needs, so the check would have skipped the card.
- Four Major findings: the Tried columns, the form of the sources paths, the See Also section, and the section order.
- The findings showed that the sample card and the standard, written in parallel, had diverged; the standard was kept and one fix pass made the sample card pass all 29 checks of the card standard.

## Cost

81753 tokens for the review agent. No dollar figure is attributed to this agent alone.
