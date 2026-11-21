---
title: "Desk check: google/elephant-goldfish-model 0.1.1 (main at 70406c4)"
source: https://github.com/google/elephant-goldfish-model/tree/70406c4d22cc7ea8299637c2c5b44625c48b3f08
type: repos
authors: ["Google LLC"]
source_date: 2026-11-17
ingested: 2026-11-21
repo: google/elephant-goldfish-model
kind: plugin
version: "0.1.1"
licence: Apache-2.0
tags: [catalog, desk-check, kind-plugin, elephant-goldfish-model, egm, design-review, claude-code, skills, agents]
summary: "Every part of google/elephant-goldfish-model read from a read-only clone of main at commit 70406c4 (manifest version 0.1.1, 48 commits after the v0.1.1 release): 8 skills, 10 reviewer and orchestrator personas, 5 document standards, the shared execution instructions; no hooks, no telemetry; how a reviewer runs without the plugin; freshness from the GitHub API; the kit's real use of the comprehension persona and the standard form it took."
---

# Desk check: google/elephant-goldfish-model 0.1.1

Read from a shallow clone of `main` at commit `70406c4d22cc7ea8299637c2c5b44625c48b3f08` (committed 2026-11-17T17:40:23-08:00), at `$EXTERNAL/elephant-goldfish-model`. The clone has no tags, so the version comes from the manifests: `plugin.json` has `"version": "0.1.1"`. That commit is 48 commits after the `v0.1.1` tag, so it holds unreleased changes, `egm-lite` among them. The clone was not modified; nothing was installed or enabled. Checked 2026-11-21. Version read by this desk check: 0.1.1 (main at `70406c4`).

## Repository facts

- Root `plugin.json`: `"name": "egm"`, `"displayName": "Elephant-Goldfish Model"`, `"version": "0.1.1"`, `"license": "Apache-2.0"`, description "Develop ideas with context and review documents with fresh eyes." `docs/releases.md`: "The canonical version is `plugin.json`'s `version`". The same version is in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and `.plugin/plugin.json`.
- `.claude-plugin/plugin.json` lists the 10 Claude Code adapters in `.claude-plugin/agents/` explicitly (`"agents"`); `.claude-plugin/marketplace.json` is a marketplace named `egm` whose one plugin has `"source": "./"`.
- `LICENSE`: "Apache License", "Version 2.0, January 2004". README: "This is not an officially supported Google product."
- Parts: `skills/` (8 skill folders; every `SKILL.md` has `disable-model-invocation: true`), `agents/` (10 personas, the canonical host-neutral prompts), `.claude-plugin/agents/` (10 Claude Code adapters of the same personas), `resources/document_standards/` (5 standards), `resources/execution_instructions.md`. There is no `hooks/` folder, no hook in any manifest and no `commands/` folder; in Claude Code the skills are started as `/egm:egm-<name>`.
- Ports to other hosts, not used by Claude Code: `.codex-plugin/`, `.cursor-plugin/` (adapters and `rules/egm.mdc`), `com.github.copilot/agents/`, `.windsurf/` (rules and workflows), `.gemini/`, `adapters/opencode/install.py`, `.agents/plugins/marketplace.json`.
- Other folders: `docs/` (host guides and design docs of the project), `site/` (the egm.dev website), `tests/`, `scripts/` (packaging and release), `.github/`.
- README, the method: "**Elephant** holds your project context and drafts the specification. **Goldfish** reviewers examine the draft and referenced source material without the earlier conversation, helping expose unstated assumptions and blind spots. **You** make the architectural trade-offs and approve the specification before implementing." And: "The built-in draft and design-review workflow targets software specifications. For other documents, choose reviewers and standards with `/egm-review-loop`."
- There is no CHANGELOG file; `docs/releases.md` describes the release process. GitHub releases: `v0.1.0` (2026-10-27) and `v0.1.1` (2026-11-06).
- `gh api repos/google/elephant-goldfish-model/compare/v0.1.1...70406c4`: the clone is 48 commits ahead of `v0.1.1`, among them "feat(skills): implement EGM Lite rapid engineering protocol (Stage 2) (#438)" (2026-11-18 UTC), "Add experimental Windsurf (Devin Desktop) adapter (#379)" and "Fix the Claude marketplace plugin root for Cowork (#347)". So `egm-lite` is not in the `v0.1.1` release.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/google/elephant-goldfish-model`: `pushed_at` 2026-11-20T20:10:41Z; licence `Apache-2.0`; default branch `main`; not archived.
- `gh api repos/google/elephant-goldfish-model/releases/latest`: tag `v0.1.1`, name "EGM v0.1.1", published 2026-11-06T21:50:31Z.
- `main` is at `8e2a5ed` (2026-11-20T20:10:41Z), 2 commits after the clone: "Mark EGM Lite design as current (#488)" and "Limit egm-bootstrap workers and scouts (#359)". They change `skills/egm-bootstrap/` and design docs only; the comprehension persona is unchanged.
- Licence: GitHub reports `Apache-2.0`, the `LICENSE` file is the Apache License 2.0 text, and the manifests say `"Apache-2.0"`. They agree.

## How to run here

- **Clone**: `git clone --depth 1 https://github.com/google/elephant-goldfish-model $EXTERNAL/elephant-goldfish-model` (main; no released tag holds `egm-lite` yet). For the release itself add `--branch v0.1.1`. Read-only; never edit the clone.
- **Telemetry and outbound calls**: `docs/privacy.md`: "The runtime package does not operate a hosted service, database, analytics client, or telemetry endpoint." A search for URLs, `fetch(`, `curl`, `wget`, `telemetry` and `analytics` in `skills/`, `agents/`, `resources/` and `.claude-plugin/` found no network call (only manifest links and a link to the essay in one persona). The website in `site/` loads Google Analytics (`gtag` in `site/src/components/Analytics.astro`), but it is not part of the plugin: "Website and development tooling are also excluded." Nothing needs switching off when the parts are read from the clone.
- `egm-bootstrap` may run local discovery commands and a project's formatter; `docs/privacy.md`: "A formatter or other user-approved project command may contact a package registry or another service."
- **Install steps to avoid**: the README's `claude plugin marketplace add google/elephant-goldfish-model` and `claude plugin install egm@egm`. The plugin has no hooks, so an install would not change every session, but the kit reads third-party skills from clones and a real install waits for the user's yes. To watch the plugin adapters themselves, `docs/claude.md` says: "For local testing, load a uniquely named copy with `claude --plugin-dir <copy>`".
- **What breaks without the plugin**:
  - The skills name `${CLAUDE_PLUGIN_ROOT}`; read it as `$EXTERNAL/elephant-goldfish-model`, from which `agents/`, `resources/` and `docs/` resolve.
  - Skills are not model-invocable; `docs/claude.md`: "The `Skill` tool refuses these skills, so to run another EGM skill (for example `egm-review-loop` or `egm-resolve` during review Stages 7 and 9), read its `SKILL.md` and follow it in the same thread." Reading from the clone is the normal way anyway.
  - Reviewers: every skill's Delegation section says "Otherwise spawn a general-purpose subagent and tell it to read that persona file first." So a reviewer works without the plugin as a general-purpose subagent told to read `agents/<name>.md`.
  - What is lost: the Claude adapters set `tools: [Read, Grep, Glob]`, `model: inherit` and `omitClaudeMd: true` (read-only tools, no CLAUDE.md). A general-purpose subagent has the session's tools and instruction files, so its prompt must tell it to stay read-only and must pass only the target, persona and standard paths. `docs/claude.md`: "Use Claude Code 2.1.271 or later for `omitClaudeMd` support." This matters only for the plugin adapters.
  - Goldfish reviews need a subagent tool: "If your harness has no subagent tool, stop and tell the user: a review in the same context is not a Goldfish review."
  - `egm-synthesizer` spawns reviewers itself; where a subagent cannot spawn subagents, the skills say to use direct dispatch instead.
- **Outputs**: the skills write `concepts_brief.md`, `design_draft.md`, stage reports, `goldfish_review_report.md`, `{YYYY-MM-DD}_DRIFT_REPORT.md` and `egm_lite_checklist.md` to the working directory, or to the folder named by a line `EGM artifact directory: <path>` in the prompt or in `CLAUDE.md`.

## Parts

### Skill: egm-brainstorm (`skills/egm-brainstorm/SKILL.md`)

- Description: "Interactive ideation and brainstorming skill for the Elephant & Goldfish Model (EGM). Helps turn half-baked concepts into structured hypotheses via clarifying questions, review, and iterative refinement."
- Open questions over several turns until the problem is clear; no subagents until the user confirms the working hypothesis; then the synthesizer runs seven reviewer lenses in parallel (`Mode: BRAINSTORM`) and writes `concepts_brief.md`; the user and agent iterate; a handoff gate offers to publish the brief as an RFC under `docs/designs/`, go to `egm-draft`, keep refining, or stop. Constraints: plain English, "No Glazing", critique first, one question per gate.
- Needs: a subagent tool; reads `agents/synthesizer.md` and seven personas.

### Skill: egm-draft (`skills/egm-draft/SKILL.md`, `references/design_doc.md`)

- Description: "Drafts a design document section-by-section using the concepts brief from egm-brainstorm (or user notes)."
- Writes `design_draft.md` section by section with an approval gate after each (overview and goals, technical plan, alternatives, implementation). It must load `resources/execution_instructions.md`. Before saving, Step 6 checks the draft against the brief and lists contradictions first; then it saves to `docs/designs/<FEATURE>.md` following the template (Overview, The Problem, Goals, Non-Goals, Open Questions, Critical User Journeys, Technical Plan, Alternatives Considered, Non-Functional Requirements, Detailed Implementation Plan, Verification Plan).
- Needs: no subagents; reads `concepts_brief.md` or `discussion_summary.md` when present.

### Skill: egm-review (`skills/egm-review/SKILL.md`)

- Description: "Executes five review phases: Initial Zoom Out Review, Comprehension Review, Design Critique, Intermediate Zoom Out Review, and Implementation Readiness."
- Stage 5: `zoom_out` and `inventive_catalyst` on the full file. Stage 6: `comprehension` spawned directly, "with no document standard", its paraphrase kept in `comprehension_report.md`. Stage 7: `design_critic`, `structural` and `style` through `egm-review-loop` with `feature-spec-standard`. Stage 8: `zoom_out` again. Stage 9: `implementation_readiness`, `codebase_details` and `style` with `implementation-readiness-standard`. Presets: interactive, one consolidated report (`consolidated_review_report.md`), feature spec only, implementation plan only. It splits the document at `## Detailed Implementation Plan`. Linked files inside the working directory join the reviewers' context; other links need approval.
- Needs: a subagent tool, all personas and standards.

### Skill: egm-review-loop (`skills/egm-review-loop/SKILL.md`)

- Description: "Executes the Antagonistic-Review process from the Elephant-Goldfish Model (EGM) via an automated multi-agent review loop to audit documents against qualitative standards and structural templates".
- Inputs: target file, a target section or `full file`, reviewers (short names map to `agents/{name}.md`), standards (short names map to `resources/document_standards/{name}.md`; "If the name contains a slash (`/`), treat it as an absolute or workspace-relative path and read it directly."), and a reading list. Each round re-reads the target, runs the reviewers (through the synthesizer or directly), collects findings with severity Blocker, Major or Nit, and hands them to `egm-resolve`. "Converged: Two consecutive clean rounds." "Cap: 5 rounds." It waits for the user between rounds.
- Needs: a subagent tool.

### Skill: egm-resolve (`skills/egm-resolve/SKILL.md`)

- Description: "The Elephant resolution skill. Ingests flat deficiency reports from concurrent Goldfish reviewers".
- Gives each finding one category: CONTEST (with evidence the reviewer could read), ESCALATE (the evidence lies outside what the reviewer could read), PROPOSE FIX, DECLINE (a Nit). Rules include "Do not contest a comprehension gap." Writes `goldfish_review_report.md`; offers auto accept, continue, or an interactive breakdown; applies approved edits; marks the report `Status: resolved`.
- Needs: to run in the session that wrote the document.

### Skill: egm-bootstrap (`skills/egm-bootstrap/SKILL.md`, `references/`)

- Description: "Bootstrap directory README.md files across a repository subtree."
- "Peanuts and Hay": writes a `README.md` contract (interfaces, invariants, side effects) for each leaf package and a roll-up blueprint for each parent; detects the test command per ecosystem; uses parallel worker subagents for trees of more than 5 directories; asks for approval when it finds "more than 15 subdirectories"; no source code edits; no commits; may run a configured project formatter; offers a drift report at the end. `target_filename` (for example `EGM.md`) leaves human-maintained READMEs untouched.
- Needs: a shell and write access to the repo; subagents for large trees. Upstream changed this skill after the clone (#359).

### Skill: egm-drift-report (`skills/egm-drift-report/SKILL.md`)

- Description: "Runs drift detection on all design documents to check for document and code consistency."
- For each design doc or README in a folder: find the code it describes, compare, and report only the differences (missing features, incomplete models, logic shortcuts, architectural divergence) in `{YYYY-MM-DD}_DRIFT_REPORT.md`, or "No drift detected."
- Needs: no subagents; read access to the code.

### Skill: egm-lite (`skills/egm-lite/SKILL.md`)

- Description: "Executes a lightweight 5-step EGM (Elephant-Goldfish-Model) protocol for small, rapid iterations, specification revisions, code refactors, and bug fixes." It adds: "Don't use for large multi-component features requiring a formal design doc (use egm-brainstorm)."
- Steps: a critique pause with no edits; `egm_lite_checklist.md`; a spec review by a fresh subagent (`goldfish` or `review`); `exec`; an adversarial diff review by a fresh subagent; a resolution gate. Not in the `v0.1.1` release.
- Needs: a subagent tool for the two reviews; git for the diff.

### Personas (`agents/`, adapters in `.claude-plugin/agents/`)

Every Goldfish persona starts with the same core mandates: read-only, no conversation history ("a naive team member or fresh reader"), no chitchat. Each has a BRAINSTORM and a REVIEW mode and reports severities Blocker, Major or Nit.

#### comprehension (`agents/comprehension.md`, name `egm-comprehension`)

- Description: "Naive Reader persona auditing documents with zero assumed institutional knowledge, flagging undefined terms, acronyms, and comprehension gaps."
- REVIEW mode: paraphrase first, under "What this proposes" and "How the existing system works, per this document"; "If you cannot write a paraphrase of a section, report that section as a 🔴 Blocker." Then it flags undefined or unlinked project-specific concepts, assumed workflow prerequisites and vague explanations. "Do not flag general engineering terms."
- Adapter: `tools: [Read, Grep, Glob]`, `omitClaudeMd: true`; it tells the reviewer to read the target and every supplied standard and to report an incomplete review if a file cannot be read.

#### design_critic (`agents/design_critic.md`, `egm-design`)

- "Hostile Design Critic persona focused on system architecture, scalability, infrastructure economics, and unmitigated risks." Audit vectors: gaps against the target standard, faulty assumptions, unmitigated risks.

#### structural (`agents/structural.md`, `egm-structural`)

- "Structural Layout Validator and Document Architect persona". Checks heading hierarchy, required headers from the standard, Markdown formatting and link form.

#### style (`agents/style.md`, `egm-style`)

- "Technical Copy Editor persona focused on clarity, precision, brevity, objective framing, and stripping fluff." Flags hyperbole, jargon, filler, subjective quality judgments, synonym redundancy and uncalibrated claims (`DROP | CALIBRATE | RELOCATE | KEEP`).

#### zoom_out (`agents/zoom_out.md`, `egm-zoom-out`)

- "Skeptical Architect persona focused on high-altitude simplicity, minimalism, YAGNI, and codebase reuse." Applies `zoom-out-standard`; must search the code for existing components before accepting new ones; flags premature detail and symptom patches.

#### inventive_catalyst (`agents/inventive_catalyst.md`, `egm-inventive-catalyst`)

- "Inventive problem-solving Goldfish persona applying TRIZ principles". Finds trade-offs accepted as unavoidable, proposes patterns and must declare their own costs; outputs "No false compromise detected" when there is none.

#### implementation_readiness (`agents/implementation_readiness.md`, `egm-implementation-readiness`)

- "Pragmatic Tech Lead persona verifying that implementation plans contain unambiguous, fully actionable execution instructions without leaving design decisions to the implementer."

#### codebase_details (`agents/codebase_details.md`, `egm-codebase-details`)

- "Pedantic Technical Quality Auditor verifying that documentation accurately and exhaustively matches actual codebase implementation". A document that contradicts the code is a Blocker; it checks every reference the document says exists now.

#### synthesizer (`agents/synthesizer.md`, `egm-synthesizer`)

- Spawns the requested reviewers in parallel, deduplicates, groups by severity and writes one report (`goldfish_review_report.md` or `concepts_brief.md`) with a status per reviewer, `completed` or `not run`. Adapter tools: `[Agent, Read, Grep, Glob, Write]`.

#### bootstrap_orchestrator (`agents/bootstrap_orchestrator.md`, `egm-bootstrap-orchestrator`)

- "Orchestrates directory README documentation, partitions subtrees, and coordinates worker subagents." Used by `egm-bootstrap`. Adapter tools: `[Agent, Bash, Read, Grep, Glob, Write, Edit]`.

### Document standards (`resources/document_standards/`)

- `feature-spec-standard.md`: the bar for a feature spec before implementation. A fresh engineer or AI session must understand the feature, the motivation and the trade-offs; "The Alternatives Rule" makes an evaluation of alternatives with reasons mandatory; risks and limits must be stated.
- `heilmeier-standard.md`: the Heilmeier Catechism for a proposal: objectives "with absolutely no jargon", state of the art, what is new, impact, risks, cost, timeline, mid-term and final exams.
- `implementation-readiness-standard.md`: the bar for a plan. "The Zero-Decision Rule": zero design choices left to the implementer; phases that each leave the codebase buildable and testable; an exact file list, steps and a test plan.
- `re-implementation-standard.md`: the bar for documenting existing code, so that a fresh reader could write functionally identical code. "The Zero-Assumption Rule": no guessing of defaults, error handling or output schemas.
- `zoom-out-standard.md`: the bar for a high-level design: context sufficiency, root problem, simplicity (YAGNI), anti-weeds (no low-level detail), leverage what exists.

#### Standard form (shared by the five standards)

- Each opens "This standard defines the quality bar for …", then has a `## Core Principle` of the form "A … passes if a competent engineer (or fresh AI session) who is unfamiliar with … can …", and three of them a named rule (`## The Alternatives Rule`, `## The Zero-Decision Rule`, `## The Zero-Assumption Rule`) before their requirements. Plain text; usable as a path in `egm-review-loop`.

### Shared resource: execution instructions (`resources/execution_instructions.md`)

- Rules for the design workflows: design-only scope (no production code files in the source tree; scratch code outside it), an explicit consensus gate at each step, "ONE QUESTION AT A TIME", no summaries, and contradiction auditing (no file edits in the turn that finds a contradiction). `egm-draft` must load it.

## How this kit uses it

- `docs/catalog-design.md` (kit): "After the first cards, a fresh agent in the Elephant-Goldfish `comprehension` role reviews each new card against `catalog-card-standard.md`, with the card's raw files as its only context". This is a plan; it is not counted as a use here.
- Method taken: the kit's card standard `docs/catalog-card-standard.md` is written in the standard form above. It opens "This standard defines the quality bar for one card in the kit's tool catalog", has a `## Core Principle` ("A card passes if an agent that has never seen the tool, the owner or the owner's private wiki can, from the card alone, …"), and named rules (`## The Evidence Rule`, `## The Public-Kit Rule`). The kit owner's design notes record that the card standard was written on the model of `resources/document_standards/`.
- Real use (retold by kind of task), 2026-11-21: a fresh general-purpose agent on the Opus model, told to take the role in `agents/comprehension.md` read from this clone (commit `70406c4`, version 0.1.1), reviewed a tool-catalog design document and its sample card against the kit's own card standard. The plugin was not installed and the `egm-review` skill was not run: one reviewer, one round. Result: one Blocker (a missing frontmatter field that the freshness check needs, so it would skip the card) and four Major findings (the Tried columns, the form of the sources paths, See Also, section order). One fix pass then made the sample card pass all 29 checks of the card standard. Cost: 81753 tokens for the review agent; dollars were not split per agent. Use record: `raw/notes/trials/2026-11-21-egm-comprehension-catalog-design-review.md`.
- No other part was used, and no session ran with the plugin loaded.
- Statuses that follow: `comprehension` in use; the standard form method taken; every other part candidate.

## Cost of this desk check

Written in one agent run together with the other 2 desk checks, the cards and the use records of the same batch: 101 model calls on opus, $7.62 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
