---
title: "google/elephant-goldfish-model"
category: reference
kind: plugin
areas: [designing-something-new, writing-code-with-agents, writing-documents-and-articles]
repo: google/elephant-goldfish-model
version: "0.1.1"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/notes/trials/2026-11-25-egm-lite-diff-review-leak-check-and-setup-script.md
  - raw/repos/google-elephant-goldfish-model-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-egm-comprehension-catalog-design-review.md
created: 2026-11-21
updated: 2026-11-25
tags: [catalog, card, area-designing-something-new, area-writing-code-with-agents, area-writing-documents-and-articles, kind-plugin, claude-code, skills, agents, design-review, specifications]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Agent plugin for designing with full context and reviewing with fresh, context-free reviewer subagents: 8 skills (brainstorm, draft, staged review, review loop, resolve, codebase READMEs, drift report, a light loop for small changes), 10 reviewer personas, 5 document standards. No hooks, no telemetry; read from a clone. The comprehension persona and egm-lite are in use, the standard form is in the kit's card standard, the rest wait for a task."
---

# google/elephant-goldfish-model

> An agent plugin (kind `plugin`, licence Apache-2.0, version `0.1.1` read at commit `70406c4` of `main`): the "Elephant" drafts with the project's context, "Goldfish" reviewer subagents read the document without the earlier conversation, and the user decides. 8 skills, 10 personas, 5 document standards; no hooks and no telemetry. Here its parts are read from a clone and the plugin is not installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Turn a half-formed idea into an agreed concept brief, challenged by fresh reviewers | `egm-brainstorm` | designing-something-new |
| Write a design document section by section from a brief or notes | `egm-draft` | designing-something-new |
| Review a software design document in stages before building it | `egm-review` | designing-something-new |
| Check that a document can be followed by a reader with no context | `comprehension` | designing-something-new |
| Act on review findings: contest with evidence, escalate, or fix | `egm-resolve` | designing-something-new |
| Review a project proposal with the Heilmeier questions | `heilmeier-standard` | designing-something-new |
| Review a card, article or other document against your own written standard | `egm-review-loop` | writing-documents-and-articles |
| Write a quality bar for a kind of document that a fresh reviewer can check | Standard form (shared by the five standards) | writing-documents-and-articles |
| Strip hype, filler and uncalibrated claims from prose | `style` | writing-documents-and-articles |
| Check that a plan leaves no design choice to the implementer | `implementation_readiness` | writing-code-with-agents |
| Document an existing code tree folder by folder | `egm-bootstrap` | writing-code-with-agents |
| Find where code has drifted from its design documents | `egm-drift-report` | writing-code-with-agents |
| Make a small change or bug fix with a checklist and a fresh diff review | `egm-lite` | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 https://github.com/google/elephant-goldfish-model $EXTERNAL/elephant-goldfish-model`, read-only. This card read `main` at commit `70406c4`, 48 commits after the `v0.1.1` release; `egm-lite` exists only on `main`. For the release add `--branch v0.1.1`.
- **Version**: `0.1.1` (manifest). Before relying on this card: `gh api repos/google/elephant-goldfish-model --jq .pushed_at` and `gh api repos/google/elephant-goldfish-model/releases/latest --jq .tag_name`.
- **Read**: `skills/<skill>/SKILL.md`, reading `${CLAUDE_PLUGIN_ROOT}` as `$EXTERNAL/elephant-goldfish-model`. For a reviewer, spawn a general-purpose subagent told to read `agents/<persona>.md` first, as the skills allow; tell it to stay read-only and pass only the target, persona and standard paths. One skill runs another by reading its `SKILL.md` in the same thread.
- **In use**: `comprehension` at `0.1.1` (commit `70406c4`), read from the clone, as a fresh reviewer of a design document and its sample card against the kit's card standard. The catalog design plans the same review for each new card. `egm-lite` (re-read at `ef27af6` on 2026-11-24: one change, #511, standalone diff reviews resolve in chat with no checklist; rubric and reviewer contract unchanged), read from the clone and followed by hand, with fresh general-purpose subagents as Goldfish reviewers: Section 4 on an existing diff, then Section 5 triage and `exec`.
- **Switch off**: nothing. `docs/privacy.md` names no telemetry endpoint and no network call was found in skills, personas or resources; the analytics in `site/` belong to the website, not the plugin. `egm-bootstrap` may run a project's formatter, which can reach a package registry.
- **Do not install**: the plugin (`claude plugin install egm@egm`) in any scope; a real install waits for the user's yes. It has no hooks. To see its read-only adapters work, run one session `claude --plugin-dir <copy>` on a uniquely named copy from a scratch folder.

## What's inside

Parts: 8 skills, 10 personas in `agents/` (Claude adapters in `.claude-plugin/agents/`), 5 standards and their shared form, the shared execution instructions. No hooks, no `commands/`. Ports for other hosts are not listed.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `egm-brainstorm` | Open questions over several turns, then seven reviewer lenses in parallel; writes and refines `concepts_brief.md`, can publish it as an RFC. | candidate | Works; reviewers become general-purpose subagents reading their persona. Needs a subagent tool. | Try it on an idea with open scope, beside superpowers `brainstorming`; compare questions and cost. |
| `egm-draft` | Writes `design_draft.md` section by section with an approval gate after each; checks the draft against the brief before saving to `docs/designs/`. | candidate | Works; no subagents. Loads the execution instructions. | Try it when a brief or notes must become a design document for a code repo. |
| `egm-review` | Five stages on a design doc: zoom out, comprehension, critic, zoom out again, implementation readiness; interactive or one consolidated report. | candidate | Works with general-purpose reviewers, minus the adapters' read-only tools and `omitClaudeMd`: say both in each prompt. | Try it on the next design document for a code repo before planning. |
| `egm-review-loop` | Chosen reviewers against chosen standards (a path to your own works), round after round until two clean rounds. | candidate | As `egm-review`. | Try it when a non-software document needs a standard-based review by more than one reviewer. |
| `egm-resolve` | Sorts findings into contest (with evidence), escalate, fix, decline; writes `goldfish_review_report.md`; applies approved edits. | candidate | Works; run it in the session that wrote the document. | Try it with the first `egm-review-loop` run. |
| `egm-bootstrap` | Writes a `README.md` contract (interfaces, invariants, side effects) per folder of a code tree; asks before more than 15 subdirectories; no code edits, no commits. | candidate | Works; needs a shell and write access, subagents for large trees. | Try it on a script repo with undocumented folders, `target_filename` set; re-read first, upstream changed it after the clone. |
| `egm-drift-report` | Compares each design doc or README in a folder with the code; lists only divergences. | candidate | Works; no subagents. | Try it on design docs whose code has moved on. |
| `egm-lite` | Small-change loop: critique, checklist, fresh spec review, `exec`, fresh diff review, resolution. Not in `v0.1.1`. | in use | Works; subagents for the reviews, git for the diff. | Without the plugin the reviewers still load the user's own instruction file; write the checklist to the working directory as the Claude guide asks. |
| `comprehension` | Naive reader: paraphrases what the document proposes, then flags undefined project terms, assumed steps, vague explanations; an unparaphrasable section is a Blocker. | in use | Works as a general-purpose subagent reading the persona; tell it to stay read-only. | Re-check the persona file on a release after `0.1.1`. |
| `design_critic` | Hostile critic: gaps against the standard, unbacked assumptions, unmitigated risks. | candidate | Works as a general-purpose subagent reading the persona. | Try it with `feature-spec-standard` on a design with cost or scale claims. |
| `structural` | Heading hierarchy, required sections from the standard, Markdown and link form. | candidate | Same. | Try it with the card standard on a new card, beside `comprehension`. |
| `style` | Copy editor: hyperbole, jargon, filler, subjective praise, uncalibrated claims. | candidate | Same. | Try it on an article or README before publishing. |
| `zoom_out` | Skeptical architect: YAGNI, reuse found by code search, premature detail. | candidate | Same; needs the repo to search. | Try it on a plan that adds a module. |
| `inventive_catalyst` | TRIZ lens: trade-offs accepted as unavoidable, patterns with their own costs. | candidate | Same. | Try it on a design trading speed for cost. |
| `implementation_readiness` | The engineer who will write the code: flags every choice left to the implementer. | candidate | Same. | Try it on a plan before an agent executes it. |
| `codebase_details` | Doc against code: missing logic, undocumented constants; a contradiction with the code is a Blocker. | candidate | Same; needs the source files. | Try it on a README that describes a script. |
| `synthesizer` | Spawns reviewers in parallel, deduplicates, writes one report with a status per reviewer. | candidate | Needs a subagent that can spawn subagents; else reviewers are dispatched directly. | Try it when one review runs three or more reviewers. |
| `bootstrap_orchestrator` | Partitions a code tree and coordinates `egm-bootstrap` workers. | candidate | Used only through `egm-bootstrap`. | Read with `egm-bootstrap`. |
| `feature-spec-standard` | Bar for a feature spec: problem, goals, trade-offs; alternatives with reasons are mandatory; risks stated. | candidate | Plain text; pass it as a path. | Try it with `design_critic` on the next design doc. |
| `heilmeier-standard` | Heilmeier Catechism: objectives without jargon, state of the art, what is new, impact, risks, cost, timeline, exams. | candidate | Plain text. | Try it on a project proposal before it goes out. |
| `implementation-readiness-standard` | Bar for a plan: zero design choices left, buildable phases, exact files, test plan. | candidate | Plain text. | Try it on a multi-step plan before execution. |
| `re-implementation-standard` | Bar for documenting code so a fresh reader could rewrite it without guessing. | candidate | Plain text. | Try it on a README written by `egm-bootstrap`. |
| `zoom-out-standard` | Bar for a high-level design: context, root problem, simplicity, no weeds, reuse. | candidate | Plain text. | Try it with `zoom_out` on a plan that adds a component. |
| Standard form (shared by the five standards) | One line on what the bar is for, a Core Principle naming the fresh reader who must succeed, named rules. | method taken | Plain text. The kit's `docs/catalog-card-standard.md` is written in this form. | Re-read when a release adds or reshapes the standards. |
| `execution_instructions.md` | Rules for design skills: no production code, a consensus gate per step, one question at a time, stop on a contradiction. | candidate | Plain text; `egm-draft` loads it. | Read with `egm-draft`. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Review of a tool-catalog design document and its sample card against a card standard | `comprehension` | Real use, persona read from the clone, not as a plugin: one Blocker and four Major findings; one fix pass then made the card pass all 29 checks. | 81753 tokens | [use record](../../raw/notes/trials/2026-11-21-egm-comprehension-catalog-design-review.md) |
| 2026-11-25 | Two diff-review rounds on a leak check's new flags, two pre-push hooks and a bash setup script, across two repositories | `egm-lite` | Real use: 9 findings (4 P1: a hook that checked only HEAD, an ignore-file append that un-ignored `.env`, repeated appends, a folder copied into), 8 fixed, 1 contested; round 2 confirmed all and found 2 P2 caused by the fixes (a push to a new remote always refused; a private name carried into other repositories). | 166681 tokens, about 1.9 USD | [use record](../../raw/notes/trials/2026-11-25-egm-lite-diff-review-leak-check-and-setup-script.md) |

## Verdict

No verdict for the repository as a whole: its parts are read from the clone one by one, and the plugin is not installed (it has no hooks or telemetry, so that is a rule of the kit, not a risk found here). One persona is in real use as a fresh reviewer, the form of its standards shaped the kit's card standard, and the other parts are candidates for design and code-review tasks. Revisit when a release after `0.1.1` appears (re-check `comprehension` first, and `egm-lite`, which no release holds yet), or when a design document for a code repo needs a staged review.

## See Also

- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; brainstorm, draft, staged review
- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; drift report, codebase READMEs, small-change loop
- [[area-writing-documents-and-articles|Writing documents and articles]] ([Writing documents and articles](../topics/area-writing-documents-and-articles.md)): area page; review loop with your own standard, style
- [[obra-superpowers|obra/superpowers]] ([obra/superpowers](../references/obra-superpowers.md)): design by interview, the other design method in the seed
- [[fission-ai-openspec|Fission-AI/OpenSpec]] ([Fission-AI/OpenSpec](../references/fission-ai-openspec.md)): living specs when a design must outlive the code

## Sources

- [Desk check: google/elephant-goldfish-model 0.1.1](../../raw/repos/google-elephant-goldfish-model-desk-check-2026-11-21.md): every part read from the clone, freshness through the GitHub API, the kit's use of it.
- [Use record: comprehension persona, reviewing a catalog design document](../../raw/notes/trials/2026-11-21-egm-comprehension-catalog-design-review.md): the real use behind `comprehension` being in use and the Tried row.
- [Use record: egm-lite, two diff-review rounds on a leak check, two hooks and a setup script](../../raw/notes/trials/2026-11-25-egm-lite-diff-review-leak-check-and-setup-script.md): 9 then 2 findings; round 2 caught defects the fixes introduced.
