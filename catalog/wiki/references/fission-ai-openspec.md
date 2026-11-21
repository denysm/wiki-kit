---
title: "Fission-AI/OpenSpec"
category: reference
kind: cli
areas: [designing-something-new, writing-code-with-agents]
repo: Fission-AI/OpenSpec
version: "2.1.1"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/fission-ai-openspec-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-designing-something-new, area-writing-code-with-agents, kind-cli, openspec, spec-driven-development, specifications, brownfield, skills]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Node.js CLI for spec-driven development: living, versioned specs in an openspec/ folder that grow one change at a time through delta specs, driven by 12 workflow skills it installs into agent tools. Telemetry on by default. Every part read is a candidate: worth it when a prototype becomes a product or an existing system needs a live spec, overkill for throwaway code."
---

# Fission-AI/OpenSpec

> A command-line tool (kind `cli`, licence MIT, version `2.1.1` read) for spec-driven development: each change gets a proposal, delta specs, a design and tasks in `openspec/`, and archiving merges the deltas into living main specs. `openspec init` installs 12 workflow skills that drive the CLI. Since 2.0 (released 2026-11-11) it installs skills only; the `/opsx:*` commands of 1.x are gone. Nothing here is installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Keep a living, versioned spec once a prototype turns into a product | `openspec-propose` | designing-something-new |
| Map one area of an existing system before changing it, writing no code | `openspec-explore` | designing-something-new |
| Grow a spec of an existing system one change at a time | `openspec archive` | designing-something-new |
| Fold a new decision into a planned change and keep its artifacts consistent | `openspec-update-change` | designing-something-new |
| Plan a feature that spans several repositories in one shared spec repo | `openspec store` | designing-something-new |
| Implement a specified change task by task | `openspec-apply-change` | writing-code-with-agents |
| Check that code matches a change's spec before closing it | `openspec-verify-change` | writing-code-with-agents |
| Validate specs and changes in CI | `openspec validate` | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch v2.1.1 https://github.com/Fission-AI/OpenSpec $EXTERNAL/OpenSpec`, read-only.
- **Version**: `2.1.1`, the latest release, published 2026-11-19. Compare first: `gh api repos/Fission-AI/OpenSpec --jq .pushed_at` and `gh api repos/Fission-AI/OpenSpec/releases/latest --jq .tag_name`.
- **Read**: `skills/<skill>/SKILL.md` (the same text `openspec init` writes), then `docs/cli.md` and `docs/existing-projects.md`. Some docs still show 1.x names (`/opsx:propose`); read them as the `openspec-*` skills. The skills drive the CLI and stop without a set-up project; only `openspec-explore` is useful without one.
- **Switch off**: telemetry is on by default (command name and version, sent to PostHog through `edge.openspec.dev`): set `OPENSPEC_TELEMETRY=0` or `DO_NOT_TRACK=1`, or `openspec config set telemetry.enabled false`. The update check asks the npm registry: set `OPENSPEC_NO_UPDATE_CHECK=1`. `openspec feedback` posts to a public GitHub tracker.
- **Do not install**: the `curl … | sh` installer, `npm install -g` (needs Node.js `22.20.0` or higher), `brew install openspec`, `npx skills add`, or `openspec init` in a real repository: it writes `openspec/` and the skills (`.agents/skills/` plus links in each tool's folder). It installs no hooks. A trial goes in a scratch copy with telemetry off; real use waits for the user's yes.

## What's inside

Parts: 23 command entries of the CLI (subcommands grouped under their command) and 12 skills. Six skills are in the default `core` profile; the other six need the expanded profile (`openspec config profile`, then `openspec update`). The default schema `schemas/spec-driven/` holds the templates.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `openspec init` | Sets up `openspec/` and installs the skills for the chosen agent tools. | candidate | The CLI (Node.js or the standalone binary); writes into the project. | Try it in a scratch copy of a prototype that is turning into a product. |
| `openspec update` | Refreshes installed skills after an upgrade; removes old `/opsx:*` command files, keeping edited ones. | candidate | The CLI; the update check unless switched off. | Read before upgrading a project that already uses it. |
| `openspec install` | Installs the standalone binary that runs without Node.js. | candidate | Downloads from GitHub. | Read only if Node.js cannot be used. |
| `openspec version` | Installed version; `--check` asks for a newer one. | candidate | Network for `--check`. | Read with `openspec update`. |
| `openspec list` | Lists active changes, or specs; `--json` for agents. | candidate | The CLI and an `openspec/` folder. | Try it with the first change in a trial project. |
| `openspec view` | Interactive terminal dashboard of specs and changes. | candidate | A terminal; human only. | Try it once a trial has specs. |
| `openspec show` | Shows a change or spec as Markdown or JSON. | candidate | The CLI and an `openspec/` folder. | Try it with the first change. |
| `openspec validate` | Checks changes and specs; `--strict`, `--all --json` for CI. | candidate | The CLI and an `openspec/` folder. | Try it on the first proposed change; put it in CI if adopted. |
| `openspec archive` | Merges a finished change's delta specs into the main specs and archives the change. | candidate | The CLI and an `openspec/` folder. | Try it at the end of the first change on an existing system. |
| `openspec new change` | Creates the folder of a new change. | candidate | The CLI and an `openspec/` folder. | Try it through `openspec-propose`. |
| `openspec status` | Artifact status of a change; `--json` for the skills. | candidate | The CLI and an `openspec/` folder. | Read when a skill calls it. |
| `openspec instructions` | Instructions for the next artifact, apply or archive, which the skills follow. | candidate | The CLI and an `openspec/` folder. | Read when a skill calls it. |
| `openspec templates` | Resolved template paths of a schema. | candidate | The CLI. | Read when customizing a schema. |
| `openspec schemas` | Lists workflow schemas. | candidate | The CLI. | Read when customizing a schema. |
| `openspec schema` (`init`, `fork`, `validate`, `which`) | Custom workflow schemas (experimental). | candidate | The CLI. | Read only if the default schema does not fit. |
| `openspec store` (`setup`, `register`, `unregister`, `remove`, `list`, `doctor`) | Stores (beta): planning in its own repo, shared across code repos. | candidate | Git and a separate repository. | Try it only when one feature spans several repos. |
| `openspec doctor` | Relationship health of the resolved root. | candidate | The CLI. | Read with `openspec store`. |
| `openspec context` | Assembles the root plus referenced stores. | candidate | The CLI. | Read with `openspec store`. |
| `openspec workset` (`create`, `list`, `open`, `remove`) | Personal local views, opened in an editor or terminal agent session. | candidate | The CLI. | Read with `openspec store`. |
| `openspec config` (`path`, `list`, `get`, `set`, `unset`, `reset`, `edit`, `profile`) | Global settings: workflow profile, telemetry. | candidate | Writes the global config. | Use it first in any trial: switch telemetry off. |
| `openspec feedback` | Files feedback as a GitHub issue through `gh`. | candidate | `gh`, network; text goes to a public tracker. | Read only to report a bug upstream. |
| `openspec completion` (`generate`, `install`, `uninstall`) | Shell completion. | candidate | `install` edits the shell profile. | Read only if adopted for daily use. |
| `openspec change`, `openspec spec`, `openspec experimental` | Deprecated noun commands and a hidden alias for `init`. | candidate | The CLI. | Read only if an old script calls them. |
| `openspec-explore` | Thinking partner: reads code, weighs options, writes no code. Default profile. | candidate | Reads without a set-up project; writing steps need the CLI. | Try it on an area of an existing system before its first proposal. |
| `openspec-propose` | Creates a change with proposal, delta specs, design and tasks in one step. Default profile. | candidate | The CLI and an `openspec/` folder. | Try it on the first change of a prototype that is becoming a product. |
| `openspec-apply-change` | Implements a change's tasks and ticks them off. Default profile. | candidate | The CLI and an `openspec/` folder. | Try it right after the first `openspec-propose`. |
| `openspec-update-change` | Revises a change's plan and keeps its artifacts coherent; never edits code. Default profile. | candidate | The CLI and an `openspec/` folder. | Try it when a proposal must take in a new decision. |
| `openspec-sync-specs` | Merges delta specs into the main specs without archiving. Default profile. | candidate | The CLI and an `openspec/` folder. | Try it on a long change whose main specs must stay current. |
| `openspec-archive-change` | Finalizes a change and updates the main specs. Default profile. | candidate | The CLI and an `openspec/` folder. | Try it at the end of the first change. |
| `openspec-new-change` | Starts a change one artifact at a time. Expanded profile. | candidate | The CLI, the expanded profile. | Try it only if `openspec-propose` is too coarse. |
| `openspec-continue-change` | Creates the next artifact of a change. Expanded profile. | candidate | The CLI, the expanded profile. | Try it with `openspec-new-change`. |
| `openspec-ff-change` | Creates all artifacts needed for implementation in one go. Expanded profile. | candidate | The CLI, the expanded profile. | Try it with `openspec-new-change`. |
| `openspec-verify-change` | Checks the code against the change for completeness, correctness, coherence. Expanded profile. | candidate | The CLI, the expanded profile. | Try it before archiving the first implemented change. |
| `openspec-bulk-archive-change` | Archives several finished changes, checking the code to settle spec conflicts. Expanded profile. | candidate | The CLI, the expanded profile. | Try it when parallel changes finish together. |
| `openspec-onboard` | Guided first cycle with narration and real work in the codebase. Expanded profile. | candidate | The CLI, the expanded profile. | Try it once, to learn the flow on a trial repo. |

## Tried

None yet: no command or skill has been run here.

## Verdict

Every part read is a candidate, waiting for one of two tasks: a prototype that turns into a product and needs a spec that outlives the code, or an existing system that needs a live spec grown one change at a time. For throwaway prototype code it is overkill. Revisit when either task appears (try `openspec-explore` and `openspec-propose` first, with telemetry off), or when a release after `2.1.1` changes the skills.

## See Also

- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; specs, proposals, stores
- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; apply, verify, validate
- [[github-spec-kit|github/spec-kit]] ([github/spec-kit](../references/github-spec-kit.md)): the other spec-driven tool in the seed, rejected here
- [[obra-superpowers|obra/superpowers]] ([obra/superpowers](../references/obra-superpowers.md)): design by interview and plan skills, without a living spec

## Sources

- [Desk check: Fission-AI/OpenSpec v2.1.1](../../raw/repos/fission-ai-openspec-desk-check-2026-11-21.md): every command and skill read from the clone, telemetry and outbound calls, freshness through the GitHub API, why the parts stay candidates.
