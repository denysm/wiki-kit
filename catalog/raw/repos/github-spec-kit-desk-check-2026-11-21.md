---
title: "Desk check: github/spec-kit v1.4.3"
source: https://github.com/github/spec-kit/tree/v1.4.3
type: repos
authors: ["GitHub, Inc."]
source_date: 2026-11-19
ingested: 2026-11-21
repo: github/spec-kit
kind: cli
version: "1.4.3"
licence: MIT
tags: [catalog, desk-check, kind-cli, spec-kit, specify-cli, spec-driven-development, specifications, rejected]
summary: "github/spec-kit v1.4.3 read from a read-only clone: the Python Specify CLI (specify) that sets a project up for spec-driven development with agent commands for many coding agents, plus bundled extensions, presets, workflows and bundles; 12 top-level commands, 9 core agent commands, 7 extensions, 4 presets, 3 workflows, 2 bundles; no telemetry found; freshness from the GitHub API; why every part is rejected here and when to revisit."
---

# Desk check: github/spec-kit v1.4.3

Read from a shallow clone of tag `v1.4.3` (commit `980b3d027f4bd7958c35f97f618d854b41320e3f`, committed 2026-11-19T14:20:20Z), at `$EXTERNAL/spec-kit`. The clone was not modified; nothing was installed or run. Checked 2026-11-21. Version read by this desk check: 1.4.3.

## Repository facts

- `pyproject.toml`: `name = "specify-cli"`, `version = "1.4.3"`, description "Specify CLI, part of GitHub Spec Kit. A tool to bootstrap your projects for Spec-Driven Development (SDD).", `requires-python = ">=3.11"`.
- `LICENSE`: "MIT License", "Copyright GitHub, Inc.".
- `CHANGELOG.md`: "## [1.4.3] - 2026-11-19"; its changes are fixes to extensions, integrations, workflows and presets (for example "feat(extensions): copy declared resources into extension skills (#5383)", "feat(presets): add bounded Markdown section replacement (#5462)").
- What it ships: the `specify` CLI (`src/specify_cli/`), the core agent commands as templates (`templates/commands/`, 9 files) with document templates (`spec-template.md`, `plan-template.md`, `tasks-template.md`, `checklist-template.md`, `constitution-template.md`), helper scripts (`scripts/bash`, `scripts/powershell`, `scripts/python`), bundled extensions (`extensions/`, 7), presets (`presets/`, 4), workflows (`workflows/`, 3), bundles (`bundles/`, 2), community catalogs (`*/catalog.community.json`), and integration folders for 43 targets in `src/specify_cli/integrations/` (including `generic` and `none`).
- Kind: `cli`. The CLI installs everything else into a project; the agent commands are templates it renders for the chosen coding agent.
- README: "Spec Kit is an open source toolkit that gives AI coding agents structured processes, reusable templates, and documented outcomes." Three processes: Spec-Driven Development (core), bug fixing and idea assessment ("bundled extensions you install when needed"). Getting started: "You need Python 3.11+, uv, and a supported AI coding agent"; `uv tool install specify-cli`, then `specify init my-project --integration copilot`.
- The minimal SDD flow in the README: constitution, specify, plan, tasks, implement, converge; "Repeat implement and converge until convergence reports `Converged`."
- `spec-driven.md` holds the full methodology; `docs/how-to/existing-projects.md` covers adopting it in an existing project ("You do not need to recreate an existing system from specifications before using").

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/github/spec-kit`: `pushed_at` 2026-11-20T15:50:42Z; licence `MIT`; default branch `main`; not archived.
- `gh api repos/github/spec-kit/releases/latest`: tag `v1.4.3`, name "Spec Kit - 1.4.3", published 2026-11-19T14:31:35Z.
- So the clone is at the latest release; `main` moved on the next day with no newer release.
- Licence: GitHub reports `MIT`; the `LICENSE` file is the MIT text. They agree.

## How to run here

- **Clone**: `git clone --depth 1 --branch v1.4.3 https://github.com/github/spec-kit $EXTERNAL/spec-kit`, read-only.
- **Read first**: `README.md`, `spec-driven.md`, `templates/commands/<command>.md`, `docs/reference/agentic-sdd.md`.
- **Telemetry**: none found. A search of `src/` for `telemetry`, `posthog`, `analytics` and `DO_NOT_TRACK` found only comments about event handlers.
- **Outbound calls**: `specify version` and `specify self` ask `https://api.github.com/repos/github/spec-kit/releases/latest`; the `extension`, `preset`, `workflow` and `bundle` catalogs are fetched from `raw.githubusercontent.com` (for extensions `SPECKIT_CATALOG_URL` points to another catalog); a `GH_TOKEN` or `GITHUB_TOKEN` in the environment is attached to GitHub requests. `docs/install/air-gapped.md`: "No network access is required — bundled assets are used by default" for `specify init`.
- **Hooks and writes into the project**: `specify init` writes `.specify/` and the agent's own folder (commands or skills), and warns to add that folder to `.gitignore` "to prevent accidental credential leakage". Extension hooks run extension commands before or after core commands: the `git` extension declares `before_constitution` (initialize a repository), `before_specify` (create a feature branch), `before_clarify` and `before_plan` (offer to commit); `agent-context` declares `after_specify` and `after_plan` (update agent instruction files such as `CLAUDE.md`). An extension that declares `events` gets them written as native hooks of the coding agent; for Claude Code into `.claude/settings.json` (`SessionStart`, `PreToolUse`, `PostToolUse`, `SessionEnd`, `UserPromptSubmit`, `Stop`). No bundled extension declares `events`. `specify mcp` runs "the experimental MCP server over stdio".
- **Install steps to avoid**: `uv tool install specify-cli`, `specify init` in any real repository, `specify extension add`, and the community catalogs (README: "Catalog listings are not audits or endorsements, so review community source code before installing or running it."). The tool is rejected here; nothing to install.

## Parts

### CLI commands (`src/specify_cli/`)

Top-level commands; subcommands are grouped under their command.

#### specify init (`command_init.py`)

- Creates a project, or sets up the current folder, with `.specify/`, templates, scripts and the agent commands for the chosen integration (`--integration`); `--extension` adds bundled extensions (for example `--extension git`). Needs Python 3.11+ and uv.

#### specify check (`command_check.py`)

- "Check that all required tools are installed."

#### specify version (`command_version.py`)

- Version and update availability; asks the GitHub releases API.

#### specify self (`check`, `upgrade`)

- Checks for, and installs, a newer `specify-cli` ("Upgrade specify-cli to the latest release (or a pinned --tag)").

#### specify integration (`list`, `install`, `uninstall`, `switch`, `use`, `upgrade`, `status`, `search`, `info`, `scaffold`, `catalog`)

- "Manage coding agent integrations": connect a project to coding agents and switch between them.

#### specify extension (`add`, `remove`, `enable`, `disable`, `list`, `info`, `search`, `update`, `set-priority`, `catalog`)

- "Manage spec-kit extensions".

#### specify preset (`add`, `remove`, `enable`, `disable`, `list`, `info`, `search`, `update`, `set-priority`, `resolve`, `catalog`)

- "Manage spec-kit presets": adapt templates, commands, terminology or methodology.

#### specify workflow (`run`, `resume`, `status`, `add`, `remove`, `enable`, `disable`, `list`, `info`, `search`, `update`, `resolve`, `definition`; groups `catalog`, `step`, `function`, `overlay`)

- "Manage and run automation workflows": prompts, commands, gates and shell tasks.

#### specify bundle (`add`, `install`, `remove`, `update`, `list`, `info`, `search`, `init`, `build`, `validate`, `catalog`)

- "Discover, install, and author Spec Kit bundles": curated setups of extensions, presets and workflows.

#### specify artifact (`list`, `info`, `lookup`)

- "Introspect commands, templates, scripts, and hooks Spec Kit exposes."

#### specify event (`run`)

- "Manage and execute event-driven commands".

#### specify mcp (`command_mcp.py`)

- "Run the experimental MCP server over stdio."

### Core agent commands (`templates/commands/`)

Rendered into the agent's folder by `specify init`; invoked as `/speckit.<name>` or `/speckit-<name>` depending on the agent. Each runs a helper script from `scripts/` first.

#### constitution

- "Create or update the project constitution from interactive or provided principle inputs."

#### specify

- "Create or update the feature specification from a natural language feature description."

#### clarify

- "Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec."

#### plan

- "Execute the implementation planning workflow using the plan template to generate design artifacts."

#### checklist

- "Generate a custom checklist for the current feature based on user requirements."

#### tasks

- "Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts."

#### analyze

- "Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation."

#### implement

- "Execute the implementation plan by processing and executing all tasks defined in tasks.md"

#### converge

- "Assess the current codebase against the feature's spec, plan, and tasks, then append any remaining unbuilt work as new tasks to tasks.md so implement can complete it."

### Bundled extensions (`extensions/<name>/extension.yml`)

#### agent-context

- "Manages coding agent context/instruction files (e.g., CLAUDE.md, copilot-instructions.md) with project-specific plan references and configurable markers". Hooks `after_specify`, `after_plan`.

#### assess

- "Assess an idea before Spec-Driven Development via intake, research, define, shape, and decide." Commands intake, research, define, shape, decide; verdict `go`, `needs-clarification` or `kill`.

#### bug

- "Assess, fix, and validate bug reports against the codebase with per-bug reports stored under .specify/bugs/<slug>/". Commands assess, fix, test.

#### git

- "Feature branch creation, numbering (sequential/timestamp), templating, validation, and Git remote detection". Hooks before constitution, specify, clarify and plan.

#### github

- "GitHub platform integration for Spec Kit - create GitHub issues from a feature's task list".

#### selftest

- "Verifies catalog extensions by programmatically walking through the discovery, installation, and registration lifecycle."

#### template

- A starting point for writing an extension ("Brief description of what your extension does").

### Presets (`presets/<name>/preset.yml`)

#### constitution-sync

- "Opt-in: restores guarded install-time constitution seeding and /constitution propagation for teams that treat materialized templates as reviewed artifacts."

#### lean

- "Minimal core workflow commands - just the prompt, just the artifact".

#### scaffold

- A starting point for writing a preset ("Brief description of what your preset provides").

#### self-test

- "A preset that overrides all core templates for testing purposes".

### Workflows (`workflows/<name>/workflow.yml`)

#### speckit

- "Runs specify → plan → tasks → implement with review gates".

#### assess

- "Runs intake → research → define → shape → decide with a verdict review gate before a manual /speckit.specify handoff".

#### bugfix

- "Runs bug assess → human review gate → bug fix → bug test on a bug report".

### Bundles (`bundles/<name>/bundle.yml`)

#### assess

- "Idea triage before Spec-Driven Development: intake, research, define, shape, decide with a verdict review gate; surviving ideas hand off manually to the specify command."

#### bugfix

- "Orchestrated bug triage: assess a bug report, review the assessment behind a human gate, apply the fix, and verify it with tests."

## Why every part is rejected (retold)

- From a review of AI delivery tools for throwaway prototypes, retold by kind: Spec Kit is not adopted where the working process already yields a spec and a plan. Here that process is a design-by-interview method followed by a plan-writing skill (the `brainstorming` and `writing-plans` skills of obra/superpowers; see that card). The same review judged it weaker than OpenSpec for existing ("brownfield") systems.
- So every part is `rejected` with that reason, the full card kept, as the catalog design asks for a rejected tool.
- Revisit condition: a team needs one spec-driven flow shared across several agent hosts (its integrations cover many coding agents from one project setup), or the kit's own flow stops producing a spec and a plan.
- An outside view, not ours: OpenSpec's README calls Spec Kit "Thorough but heavyweight. Rigid phase gates, lots of Markdown, Python setup." (a competitor's claim; see the OpenSpec desk check).

## Cost of this desk check

Written in one agent run together with the other 2 desk checks, the cards and the use records of the same batch: 101 model calls on opus, $7.62 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
