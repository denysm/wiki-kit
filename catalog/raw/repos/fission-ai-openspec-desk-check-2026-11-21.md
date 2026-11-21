---
title: "Desk check: Fission-AI/OpenSpec v2.1.1"
source: https://github.com/Fission-AI/OpenSpec/tree/v2.1.1
type: repos
authors: ["FISSION AI INC"]
source_date: 2026-11-19
ingested: 2026-11-21
repo: Fission-AI/OpenSpec
kind: cli
version: "2.1.1"
licence: MIT
tags: [catalog, desk-check, kind-cli, openspec, spec-driven-development, specifications, brownfield, skills]
summary: "Fission-AI/OpenSpec v2.1.1 read from a read-only clone: a Node.js CLI (openspec) that keeps living, versioned specs in an openspec/ folder and installs 12 workflow skills that drive it; 23 top-level command entries and 12 skills; telemetry on by default and how to switch it off; the 2.0 move from /opsx:* commands to skills; freshness from the GitHub API; why its parts stay candidates."
---

# Desk check: Fission-AI/OpenSpec v2.1.1

Read from a shallow clone of tag `v2.1.1` (commit `0c737dc1b543249b38b0f4716816fcf493d894dd`, committed 2026-11-19T22:15:20Z), at `$EXTERNAL/OpenSpec`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 2.1.1.

## Repository facts

- `package.json`: `"name": "@fission-ai/openspec"`, `"version": "2.1.1"`, description "AI-native system for spec-driven development", `"license": "MIT"`, `"author": "FISSION AI INC"`, `"bin": {"openspec": "./bin/openspec.js"}`. Published files: `dist`, `bin`, `schemas`.
- `LICENSE`: "MIT License", "Copyright (c) 2025 FISSION AI INC".
- What it ships: a TypeScript CLI (`src/cli/index.ts` registers the commands; `src/commands/`, `src/core/`), the default workflow schema `schemas/spec-driven/` (`schema.yaml`, templates `proposal.md`, `spec.md`, `design.md`), and 12 skills in `skills/`. `skills/README.md`: "Each `openspec-*/SKILL.md` here is the same skill `openspec init` writes into a project. The skills drive the `openspec` CLI". Every skill's frontmatter says "compatibility: Requires openspec CLI."
- Kind: `cli`. The skills are the agent-facing workflow, but they call the CLI (`openspec status`, `openspec instructions`, `openspec new change`, `openspec archive` and others) and stop without a project set up by it, so the tool is the CLI and the skills are its agent commands.
- Other folders: `openspec/` (the project's own specs and changes; "OpenSpec is built with OpenSpec"), `docs/`, `docs-lab/`, `website/`, `test/`, `scripts/` (including `scripts/binary/` installers), `.agents/skills/` (the project's own copies).
- README philosophy: "built for brownfield not just greenfield". Install: `curl -fsSL https://openspec.dev/cli/install.sh | sh`, or `npm install -g @fission-ai/openspec@latest` ("needs Node.js 22.20.0 or higher"), or `brew install openspec`; then `openspec init` in the project.
- README, "How we compare": "**vs. [Spec Kit](https://github.com/github/spec-kit)** (GitHub) — Thorough but heavyweight. Rigid phase gates, lots of Markdown, Python setup. OpenSpec is lighter and lets you iterate freely." (upstream's own view).
- `CHANGELOG.md`, `## 2.0.0`, Major Changes: "OpenSpec 2.0 installs skills only, in one shared folder." and "**Skills only.** OpenSpec no longer writes `/opsx:*` command files. Each command has a skill with the same instructions. For example, `/opsx:propose` becomes `openspec-propose`, which you invoke as `/openspec-propose` (`$openspec-propose` in Codex)." Skills are written once to `.agents/skills/`, and Claude Code and other tools "get a link to each skill in their own `skills/` folder". GitHub release `v2.0.0` was published 2026-11-11T22:41:44Z, so version 2.0 (2026-11-11) replaced the `/opsx:*` commands with skills.
- Some docs still use the 1.x names: `docs/existing-projects.md` shows `/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:archive`; read them as the `openspec-*` skills.
- `CHANGELOG.md`, `## 2.1.1`, among the patch changes: "`openspec init` and `openspec update` install skills from the npm package, so they work offline, need no Git", and a fix so that `openspec-archive-change` finds an existing archive folder before it writes any main spec.
- Profiles (`docs/cli.md`): default profile `core` with "workflows `propose, explore, apply, update, sync, archive`". README: the expanded workflow (`openspec-new-change`, `openspec-continue-change`, `openspec-ff-change`, `openspec-verify-change`, `openspec-bulk-archive-change`, `openspec-onboard`) is selected with `openspec config profile` and applied with `openspec update`.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/Fission-AI/OpenSpec`: `pushed_at` 2026-11-20T20:46:04Z; licence `MIT`; default branch `main`; not archived.
- `gh api repos/Fission-AI/OpenSpec/releases/latest`: tag `v2.1.1`, name "v2.1.1 - Offline skill installs, safer archive", published 2026-11-19T22:26:58Z. Earlier: `v2.1.0` (2026-11-17), `v2.0.0` (2026-11-11), `v1.17.0` (2026-11-09).
- So the clone is at the latest release; `main` has moved on since (pushed the next day), with no newer release.
- Licence: GitHub reports `MIT`; the `LICENSE` file is the MIT text; `package.json` says `"MIT"`. They agree.

## How to run here

- **Clone**: `git clone --depth 1 --branch v2.1.1 https://github.com/Fission-AI/OpenSpec $EXTERNAL/OpenSpec`, read-only.
- **Read first**: `skills/<skill>/SKILL.md`, `docs/cli.md`, `docs/existing-projects.md`, `docs/concepts.md`.
- **Telemetry**: on by default. README: "OpenSpec collects anonymous usage stats." and "We collect only command names and version to understand usage patterns. No arguments, paths, content, or PII. Automatically disabled in CI." `src/telemetry/index.ts` sends events with a plain `fetch` to PostHog through `https://edge.openspec.dev`, with a random anonymous id. Opt-out, any one is enough: `openspec config set telemetry.enabled false`, `export OPENSPEC_TELEMETRY=0`, or `export DO_NOT_TRACK=1`.
- **Update check**: `src/core/version-check.ts` asks `https://registry.npmjs.org` (or `npm_config_registry`) for a newer CLI; it honours the telemetry opt-outs and is off in CI. `OPENSPEC_NO_UPDATE_CHECK` turns it off; `openspec version --check` asks only when requested.
- **Other outbound calls**: `openspec install` downloads the standalone binary (installers from `raw.githubusercontent.com`, release files from GitHub); `openspec feedback` files a GitHub issue through `gh`.
- **Install steps to avoid**: the `curl … | sh` installer, `npm install -g`, `brew install openspec`, `npx skills add Fission-AI/OpenSpec`, and `openspec init` or `openspec update` in a real repository. `init` and `update` write `openspec/` and the skills into the project (`.agents/skills/` plus links in each selected tool's folder). No hooks are installed: the code generates skills only.
- **Without the CLI**: the skills can be read from the clone, but each "Requires openspec CLI." and, before the first step that writes, checks that the project has an OpenSpec root; when the skill was chosen without the user naming OpenSpec and there is no root, it says to stop using OpenSpec and answer normally. Only `openspec-explore` is useful without a set-up project (it reads code and writes nothing).

## Parts

### CLI commands (`src/cli/index.ts`, `src/cli/commands/`)

Subcommands are grouped under their command; descriptions are the CLI's own.

#### openspec init

- "Initialize OpenSpec in your project". Creates `openspec/` and installs the workflow skills for the chosen tools; `--tools`, `--profile`. Writes into the project.

#### openspec update

- "Update OpenSpec instruction files". Refreshes the installed skills after a CLI upgrade; since 2.0 it also removes the `/opsx:*` command files of earlier versions and keeps and lists any that were edited.

#### openspec install

- "Install the standalone openspec, which runs without Node.js (latest release unless [version] is given)". Downloads from GitHub.

#### openspec version

- "Report the installed OpenSpec version and update availability". `--check` asks the npm registry.

#### openspec list

- "List items (changes by default). Use --specs to list specs." `--json` for agents.

#### openspec view

- "Display an interactive dashboard of specs and changes". Human only.

#### openspec show

- "Show a change or spec". Markdown or `--json`.

#### openspec validate

- "Validate changes and specs". `--strict`, `--all --json` for CI and scripts.

#### openspec archive

- "Archive a completed change and update main specs". Merges the change's delta specs into `openspec/specs/` and moves the change to `openspec/changes/archive/`.

#### openspec new change

- "Create a new change directory". `--store <id>` targets a registered store.

#### openspec status

- "Display artifact completion status for a change". `--json` for agents; every skill calls it.

#### openspec instructions

- "Output enriched instructions for artifacts, apply, or archive". The skills follow its output.

#### openspec templates

- "Show resolved template paths for all artifacts in a schema".

#### openspec schemas

- "List available workflow schemas with descriptions".

#### openspec schema (`init`, `fork`, `validate`, `which`)

- "Manage workflow schemas [experimental]". Custom workflows beside the default `spec-driven` schema.

#### openspec store (`setup`, `register`, `unregister`, `remove`, `list`, `doctor`)

- Stores, in beta: planning in a repo of its own, shared across code repos (README: "Stores are in **beta**."). Needs git and a separate repository.

#### openspec doctor

- Reports relationship health for the resolved root (`docs/cli.md`).

#### openspec context

- Assembles the working set: the root plus referenced stores (`docs/cli.md`).

#### openspec workset (`create`, `list`, `open`, `remove`)

- Personal, local working views, opened in an editor window or a terminal agent session (`docs/cli.md`).

#### openspec config (`path`, `list`, `get`, `set`, `unset`, `reset`, `edit`, `profile`)

- "View and modify global OpenSpec configuration". Holds the workflow profile and `telemetry.enabled`.

#### openspec feedback

- "Submit feedback about OpenSpec". Uses `gh` to open a GitHub issue; the text goes to a public tracker.

#### openspec completion (`generate`, `install`, `uninstall`)

- "Manage shell completions for OpenSpec CLI". `install` edits the shell profile.

#### Deprecated: openspec change, openspec spec, openspec experimental

- `change` and `spec` are the old noun commands (`show`, `list`, `validate`) with a deprecation notice; `experimental` is a hidden "Alias for init (deprecated)".

### Skills (`skills/<name>/SKILL.md`, all "Requires openspec CLI.")

#### openspec-explore (default profile)

- "Enter OpenSpec explore mode - a thinking partner for exploring ideas, investigating problems, and clarifying requirements in a project that uses OpenSpec." "Explore mode is for thinking, not implementing." Reads code and runs read-only commands; no fixed steps.

#### openspec-propose (default profile)

- "Propose a new OpenSpec change with all artifacts generated in one step." Creates the change folder with `proposal.md`, delta `specs/`, `design.md` and `tasks.md`.

#### openspec-apply-change (default profile)

- "Implement tasks from an OpenSpec change." Works through `tasks.md` and ticks tasks off.

#### openspec-update-change (default profile)

- "Update an OpenSpec change by revising its existing planning artifacts and keeping them coherent with one another." "Never edit code."

#### openspec-sync-specs (default profile)

- "Sync delta specs from an OpenSpec change to main specs." An agent-driven merge, without archiving the change.

#### openspec-archive-change (default profile)

- "Archive a completed OpenSpec change in the experimental workflow." Finalizes a change and updates the main specs.

#### openspec-new-change (expanded profile)

- "Start a new OpenSpec change using the experimental artifact workflow." Step by step, one artifact at a time.

#### openspec-continue-change (expanded profile)

- "Continue working on an OpenSpec change by creating the next artifact."

#### openspec-ff-change (expanded profile)

- "Fast-forward through OpenSpec artifact creation." Creates all artifacts needed for implementation in one go.

#### openspec-verify-change (expanded profile)

- "Verify implementation matches OpenSpec change artifacts." Checks completeness, correctness and coherence and writes a verification report before archiving.

#### openspec-bulk-archive-change (expanded profile)

- "Archive multiple completed OpenSpec changes at once." Resolves spec conflicts by checking what the code actually implements.

#### openspec-onboard (expanded profile)

- "Guided onboarding for OpenSpec - walk through a complete workflow cycle with narration and real codebase work."

## Why its parts stay candidates (retold)

- From a review of AI delivery tools for throwaway prototypes, retold by kind: OpenSpec's verdict there is "as needed". It is needed when a prototype turns into a product, or when a live spec of an existing system is required; for throwaway code it is overkill. So every part read stays a candidate, and the task to try it on is one of those two situations.
- The kit's public method `docs/ai-tooling-for-throwaway-pocs.md` says the same in general form: "Take a spec-driven tool only when a PoC turns into a product."
- Its delta specs (`ADDED`, `MODIFIED`, `REMOVED`) grow the specs one change at a time; `docs/existing-projects.md`: "You do not document your whole codebase to start. You write specs only for what you're about to change." That is what makes it fit an existing system.

## Cost of this desk check

Written in one agent run together with the other 2 desk checks, the cards and the use records of the same batch: 101 model calls on opus, $7.62 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
