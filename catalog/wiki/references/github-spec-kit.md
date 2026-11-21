---
title: "github/spec-kit"
category: reference
kind: cli
areas: [designing-something-new, writing-code-with-agents]
repo: github/spec-kit
version: "1.4.3"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/github-spec-kit-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-designing-something-new, area-writing-code-with-agents, kind-cli, spec-kit, specify-cli, spec-driven-development, specifications, rejected]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Python CLI (specify) that sets a project up for spec-driven development: constitution, spec, plan, tasks, implement, converge as agent commands for many coding agents, plus bundled extensions, presets, workflows and bundles. No telemetry found. Rejected here: the kit's own flow already yields a spec and a plan, and it was judged weaker than OpenSpec on existing systems. Revisit when a team needs one spec-driven flow across several agent hosts."
---

# github/spec-kit

> A command-line tool (kind `cli`, licence MIT, version `1.4.3` read): the Specify CLI sets a project up with templates, helper scripts and agent commands for spec-driven development (constitution, specify, plan, tasks, implement, converge), and adds extensions, presets, workflows and bundles. Rejected here; nothing is installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Not this: write a feature spec from a plain description before coding. Rejected: the kit's design-by-interview flow already yields the spec | `specify` | designing-something-new |
| Not this: set governing principles for a project's specs. Rejected with the whole tool: the kit's flow already yields a spec and a plan | `constitution` | designing-something-new |
| Not this: specify changes to an existing (brownfield) system. Rejected: judged weaker than OpenSpec there | `specify init` | designing-something-new |
| Not this: assess whether an idea deserves investment. Rejected with the whole tool | `assess` (extension) | designing-something-new |
| Not this: turn a spec into a plan and ordered tasks. Rejected: a plan-writing skill already does this | `plan` | writing-code-with-agents |
| Not this: run one spec-driven flow from several coding agents. Rejected: no team needs a shared multi-agent flow yet, which is the revisit condition | `specify integration` | writing-code-with-agents |
| Not this: assess, fix and verify a bug with recorded reports. Rejected with the whole tool | `bug` | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch v1.4.3 https://github.com/github/spec-kit $EXTERNAL/spec-kit`, read-only.
- **Version**: `1.4.3`, the latest release, published 2026-11-19. Compare first: `gh api repos/github/spec-kit --jq .pushed_at` and `gh api repos/github/spec-kit/releases/latest --jq .tag_name`.
- **Read**: `README.md`, `spec-driven.md`, `templates/commands/<command>.md`, `docs/reference/agentic-sdd.md`.
- **Switch off**: no telemetry found. Outbound: `specify version` and `specify self` ask the GitHub releases API; catalog searches fetch JSON from `raw.githubusercontent.com`; a `GH_TOKEN` or `GITHUB_TOKEN` in the environment goes with GitHub requests. `specify init` works offline from bundled assets.
- **Do not install**: `uv tool install specify-cli`, `specify init` in a real repository, extensions, or community catalog entries. `init` writes `.specify/` and the agent's folder; the `git` extension adds hooks that create branches and offer commits, `agent-context` edits `CLAUDE.md`, and an extension declaring `events` becomes native agent hooks (`.claude/settings.json` for Claude Code; no bundled one does). Rejected, so nothing waits for a yes.

## What's inside

Parts: 12 top-level commands (subcommands in the desk check), 9 core agent commands, 7 bundled extensions, 4 presets, 3 workflows, 2 bundles. Every row is rejected for one reason: the kit's design-by-interview method plus a plan-writing skill already yields a spec and a plan; for existing systems it was judged weaker than OpenSpec.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `specify init` | Sets a project up with `.specify/`, templates, scripts and agent commands for the chosen integration; `--extension` adds extensions. | rejected | Python 3.11+, uv; writes into the project. | Rejected: the kit's flow yields spec and plan; weaker than OpenSpec on existing systems. Revisit when a team needs one spec flow across agent hosts. |
| `specify check` | Checks that required tools are installed. | rejected | The CLI. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify version` | Version and update availability. | rejected | The CLI; GitHub API. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify self` | Checks for and installs a newer CLI. | rejected | The CLI; GitHub API. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify integration` | Connects a project to coding agents and switches between them. | rejected | The CLI; writes agent folders. | Rejected: no shared multi-agent flow needed. Revisit when a team needs one spec flow across agent hosts. |
| `specify extension` | Adds, removes and searches extensions. | rejected | The CLI; catalogs over the network. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify preset` | Adapts templates, commands and terminology. | rejected | The CLI. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify workflow` | Runs automation workflows of prompts, commands, gates and shell tasks. | rejected | The CLI; runs shell steps. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify bundle` | Installs and authors curated setups. | rejected | The CLI. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify artifact` | Shows which layer supplies a command, template, script or hook. | rejected | The CLI. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify event` | Runs event-driven commands. | rejected | The CLI. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `specify mcp` | Experimental MCP server over stdio. | rejected | The CLI; an MCP client. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `constitution` | Creates or updates the project's governing principles. | rejected | A project set up by `specify init`. | Rejected: the kit's flow yields spec and plan. Revisit when a team needs one spec flow across agent hosts. |
| `specify` | Writes or updates the feature spec from a plain description. | rejected | Same. | Rejected: design by interview already yields the spec. Revisit when a team needs one spec flow across agent hosts. |
| `clarify` | Asks up to 5 targeted questions and writes the answers into the spec. | rejected | Same. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `plan` | Generates design artifacts from the plan template. | rejected | Same. | Rejected: a plan-writing skill already does this. Revisit when a team needs one spec flow across agent hosts. |
| `checklist` | Generates a custom checklist for the feature. | rejected | Same. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `tasks` | Writes a dependency-ordered `tasks.md`. | rejected | Same. | Rejected: a plan-writing skill already yields the plan. Revisit when a team needs one spec flow across agent hosts. |
| `analyze` | Read-only consistency check across spec, plan and tasks. | rejected | Same. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `implement` | Executes every task in `tasks.md`. | rejected | Same. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `converge` | Compares the code with spec, plan and tasks and appends unbuilt work as tasks. | rejected | Same. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `agent-context` | Keeps agent instruction files such as `CLAUDE.md` pointing at the current plan; hooks after specify and plan. | rejected | `specify extension add`; edits instruction files. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `assess` (extension) | Idea assessment: intake, research, define, shape, decide (`go`, `needs-clarification`, `kill`). | rejected | `specify extension add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `bug` | Assesses, fixes and tests a bug with reports under `.specify/bugs/`. | rejected | `specify extension add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `git` | Feature branches, numbering, remote detection; hooks before constitution, specify, clarify, plan. | rejected | `specify extension add`; creates branches, offers commits. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `github` | Creates GitHub issues from a feature's task list. | rejected | `specify extension add`; GitHub access. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `selftest` | Walks catalog extensions through discovery, installation and registration. | rejected | `specify extension add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `template` | Starting point for writing an extension. | rejected | Nothing to read it. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `constitution-sync` | Opt-in preset: install-time constitution seeding and propagation. | rejected | `specify preset add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `lean` | Preset: minimal core commands, just the prompt and the artifact. | rejected | `specify preset add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `scaffold` | Starting point for writing a preset. | rejected | Nothing to read it. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `self-test` | Preset that overrides all core templates, for testing. | rejected | `specify preset add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `speckit` (workflow) | Specify, plan, tasks, implement with review gates. | rejected | `specify workflow run`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `assess` (workflow) | The assessment stages with a verdict review gate. | rejected | `specify workflow run`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `bugfix` (workflow) | Bug assess, human review gate, fix, test. | rejected | `specify workflow run`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `assess` (bundle) | Curated setup for idea triage before SDD. | rejected | `specify bundle add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |
| `bugfix` (bundle) | Curated setup for orchestrated bug triage with a human gate. | rejected | `specify bundle add`. | Rejected with the tool. Revisit when a team needs one spec flow across agent hosts. |

## Tried

None yet: rejected after the desk check, without a trial.

## Verdict

Rejected as a whole without a trial: the kit's design-by-interview method and plan-writing skill already give a spec and a plan, and for existing systems OpenSpec was judged the better spec tool. Its parts are kept in full so the decision can be checked. Revisit when a team needs one spec-driven flow shared across several agent hosts, or when the kit's own flow stops producing a spec and a plan.

## See Also

- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; specs and design methods
- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; plans, tasks, implementation
- [[fission-ai-openspec|Fission-AI/OpenSpec]] ([Fission-AI/OpenSpec](../references/fission-ai-openspec.md)): the spec tool kept as a candidate, for products and existing systems
- [[obra-superpowers|obra/superpowers]] ([obra/superpowers](../references/obra-superpowers.md)): `brainstorming` and `writing-plans`, the flow that already yields a spec and a plan

## Sources

- [Desk check: github/spec-kit v1.4.3](../../raw/repos/github-spec-kit-desk-check-2026-11-21.md): every command, extension, preset, workflow and bundle read from the clone, outbound calls and hooks, freshness through the GitHub API, why every part is rejected.
