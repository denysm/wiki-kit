---
title: "NeoLabHQ/context-engineering-kit"
category: reference
kind: skill-collection
areas: [writing-code-with-agents, building-skills-and-plugins, designing-something-new, writing-documents-and-articles]
repo: NeoLabHQ/context-engineering-kit
version: "3.10.0"
licence: GPL-3.0
desk_checked: 2026-11-21
sources:
  - raw/repos/neolabhq-context-engineering-kit-desk-check-2026-11-21.md
  - raw/data/neolabhq-context-engineering-kit-parts-3.10.0.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-writing-code-with-agents, area-building-skills-and-plugins, area-designing-something-new, area-writing-documents-and-articles, kind-skill-collection, claude-code, skills, kaizen, root-cause-analysis, code-review, gpl]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "GPL-3.0 Claude Code marketplace of 13 plugins (reflexion, review, git, tdd, sadd, ddd, sdd, kaizen, customaize-agent, docs, tech-stack, mcp, fpf); 269 parts in the generated list, most of them copies in provider bundles. Only kaizen was reviewed: five whys, PDCA and A3 are in the kit's own words, the plugin and its text are rejected (auto-triggered, GPL), four kaizen skills and the reflexion hook are candidates, everything else is listed."
---

# NeoLabHQ/context-engineering-kit

> A Claude Code plugin marketplace (kind `skill-collection`, licence GPL-3.0, version `3.10.0` read) of 13 plugins for coding agents: reflection, multi-agent review, git, TDD, subagent execution, spec-driven development, root-cause analysis and more. Here only its kaizen plugin was reviewed, for techniques; nothing is installed and, because of the GPL, no text is copied into the MIT kit.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Find the root cause of a bug or a repeating problem by asking why until a process cause appears | `why` (method in the kit's own words) | writing-code-with-agents |
| Run an improvement as measured plan, do, check, act cycles | `plan-do-check-act` (method in the kit's own words) | writing-code-with-agents |
| Write a problem up on one page, from background to follow-up (A3) | `analyse-problem` (method in the kit's own words) | writing-code-with-agents |
| Explore the causes of a problem across six categories (fishbone) | `cause-and-effect` | writing-code-with-agents |
| Trace an error deep in the call stack back to its original trigger | `root-cause-tracing` | writing-code-with-agents |
| Look at code, a workflow or waste with a Gemba walk, a value stream map or the seven wastes | `analyse` | writing-code-with-agents |
| Keep code changes small, error-proof, patterned and free of speculative features | `kaizen` | writing-code-with-agents |
| Review local changes or a pull request with several specialised reviewer agents | `review-local-changes`, `review-pr` | writing-code-with-agents |
| Execute independent tasks with a fresh subagent each and a judge after each | `subagent-driven-development`, `do-and-judge` | writing-code-with-agents |
| Write tests first, or fix the tests a refactoring broke | `test-driven-development`, `fix-tests` | writing-code-with-agents |
| Make a conventional commit or open a pull request | `commit`, `create-pr` | writing-code-with-agents |
| Have the agent reflect on and critique its last answer | `reflect`, `critique` | writing-code-with-agents |
| Turn a prompt into a planned task spec before implementing it | `add-task`, `plan-task` | designing-something-new |
| Compare competing hypotheses for a decision with evidence and a decision record | `propose-hypotheses` | designing-something-new |
| Write a skill, command or agent for Claude Code | `create-skill`, `create-command`, `create-agent` | building-skills-and-plugins |
| Test a skill or prompt with subagents before shipping it | `test-skill`, `test-prompt` | building-skills-and-plugins |
| Run a reflection automatically when a prompt asks to reflect | reflexion hook (`hooks/hooks.json`: Stop, UserPromptSubmit) | building-skills-and-plugins |
| Edit documentation people will read to be shorter and plainer | `write-concisely` | writing-documents-and-articles |
| Not this: install the kaizen plugin, or copy its text into an MIT project. Rejected: code-specific and auto-triggered; GPL text cannot enter the MIT kit | `kaizen` plugin as a whole (install, or copy its text) | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch v3.10.0 https://github.com/NeoLabHQ/context-engineering-kit $EXTERNAL/context-engineering-kit`, read-only. Never edit the clone.
- **Version**: `3.10.0`, the latest release, published 2026-08-26; `master` is 2 commits ahead, both changing only `README.md`. Compare before relying on this card: `gh api repos/NeoLabHQ/context-engineering-kit/releases/latest --jq .tag_name`.
- **Read**: `plugins/<plugin>/README.md`, then `plugins/<plugin>/skills/<skill>/SKILL.md`. Ignore the copies in the root `skills/`, `agents/` and `antigravity/`: they are generated provider bundles.
- **Licence**: GPL-3.0. Read for techniques only; carry a technique into the kit in its own words, never its text.
- **Switch off**: nothing to switch off when reading. Installed, the reflexion hook runs on every prompt and stop (with `bun` on PATH) and saves prompts to the system temp folder; the `kaizen` skill is "Always applied for" coding work; ddd and tech-stack rules load by file pattern. Git and review call GitHub through `gh`; mcp sets up third-party MCP servers.
- **Do not install**: the marketplace or any plugin (`/plugin marketplace add`, `/plugin install`, `npx skills add`, `gemini extensions install`). Installing is not needed for the kaizen methods; any install, even a one-session `claude --plugin-dir` sandbox, waits for the user's yes.

## What's inside

13 plugins, 269 parts in the [generated parts list](../../raw/data/neolabhq-context-engineering-kit-parts-3.10.0.md) (204 skills, 1 command, 63 agents, 1 hook). Of these, 90 are the plugins' own parts; the rest are copies in provider bundles and one maintainer command. Rule files (17 in ddd, 1 in tech-stack) are not in that list and are named in the desk check. What each plugin is for:

- **reflexion**: reflect, critique and memorize into `CLAUDE.md`, plus the only hook.
- **review**: multi-agent review of local changes or a pull request (3 skills, 10 agents).
- **git**: commits, pull requests, issues, worktrees, git notes; needs `gh`.
- **tdd**: test-first development, fixing and covering tests.
- **sadd**: fresh subagent per task with judges, competitive and parallel execution.
- **ddd**: Clean Architecture, SOLID and DDD rules loaded by file pattern.
- **sdd**: spec-driven development from task draft to implementation, with eight agents.
- **kaizen**: root-cause and improvement methods (read in full, rows below).
- **customaize-agent**: creating and testing skills, commands, agents, prompts and git hooks.
- **docs**: updating documentation, writing concisely.
- **tech-stack**: one TypeScript rule loaded by file pattern.
- **mcp**: setting up Context7, Serena, Codemap and a paper-search MCP server; building MCP servers.
- **fpf**: hypothesis-driven, auditable decisions; loads a specification of about "~600k tokens" into a subagent.

Every part not in the table below is `listed`: read it when a task in Tasks it serves names it.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `why` | Five whys: ask why until a systemic or process cause appears, check back from cause to symptom, branch when causes split. | method taken | Works from the clone; plain text. The kit carries it in its own words (`specialists/development-coach/references/methods.md`, `specialists/decision-analyst/SKILL.md`). | Re-read on a new major version of the kaizen plugin; the kit text stands on its own. |
| `plan-do-check-act` | PDCA: baseline, hypothesis, measurable success criteria, small change, check against baseline, standardise or start a new cycle. | method taken | Works from the clone. The kit carries it in its own words (same two files). | Re-read on a new major version of the kaizen plugin. |
| `analyse-problem` | A3: background, current condition, goal, root cause, countermeasures, implementation plan, follow-up, on one page. | method taken | Works from the clone. The kit carries it in its own words (`specialists/development-coach/references/methods.md`). | Re-read on a new major version of the kaizen plugin. |
| `cause-and-effect` | Fishbone: causes under People, Process, Technology, Environment, Methods and Materials, then why under each and a priority order. | candidate | Works from the clone; plain text. | Try it on a recurring failure with several plausible causes, such as a flaky test suite. |
| `root-cause-tracing` | Trace an error back through the call chain to its original trigger, instrument with stack traces, fix at the source, add a check at each layer. Largely the same text as a helper file of obra/superpowers `systematic-debugging` (MIT). | candidate | Works from the clone, but the `find-polluter.sh` script it names is not in the folder. | Try it on an error that surfaces far from its cause; prefer the MIT original in obra/superpowers when citing. |
| `analyse` | Picks one of three lenses: Gemba walk (read the real code against assumptions), value stream map (stages and waiting time), Muda (seven wastes in software). | candidate | Works from the clone; plain text. | Try the Gemba walk before changing an unfamiliar area of a script repository. |
| `kaizen` | Four pillars with TypeScript examples: small improvements, poka-yoke (invalid states unrepresentable), standardised work, just-in-time (YAGNI, rule of three). | candidate | Read from the clone it is a checklist; installed it is "Always applied for" coding work. | Try it as a review checklist on a refactoring, read on demand, not auto-applied. |
| reflexion hook (`hooks/hooks.json`: Stop, UserPromptSubmit) | On every prompt saves the session's events to the system temp folder; on stop, if the last prompt contained "reflect", blocks the stop and makes the agent run `/reflexion:reflect`. No network call found. | candidate | Does not run: needs the installed plugin (`${CLAUDE_PLUGIN_ROOT}`), `bun`, and the `reflect` skill under its plugin name. | Try it only in a one-session sandbox if an automatic reflection step is wanted; it writes every prompt to disk. |
| `kaizen` plugin as a whole (install, or copy its text) | The installed plugin: seven skills, one auto-applied. | rejected | Not needed: the methods wanted are in the kit's own words. | Rejected: code-specific and auto-triggered; GPL-3.0 text cannot enter the MIT kit. Revisit only if the licence changes or a plugin-only feature is needed, tried first in a one-session sandbox. |

## Tried

None yet. No part of this repository was tried in a sandbox or used in real work; the three `method taken` rows rest on the kit's own texts named in the desk check.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

A large GPL collection read for techniques, not for use: the kit took five whys, PDCA and A3 into its own words and turned down the kaizen plugin and its text. Four kaizen skills and the reflexion hook are candidates; the other plugins are only listed, with their READMEs summarised so a task can find them. Revisit when a code-review, spec-driven or subagent task needs one of the listed plugins (read its parts first, then decide), when a new major version of kaizen appears, or if the licence changes.

## See Also

- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; root-cause methods, review, TDD, subagent execution
- [[area-building-skills-and-plugins|Building skills and plugins]] ([Building skills and plugins](../topics/area-building-skills-and-plugins.md)): area page; customaize-agent, the reflexion hook
- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; sdd task specs, fpf hypotheses
- [[area-writing-documents-and-articles|Writing documents and articles]] ([Writing documents and articles](../topics/area-writing-documents-and-articles.md)): area page; `write-concisely`
- [[obra-superpowers|obra/superpowers]] ([obra/superpowers](../references/obra-superpowers.md)): MIT process skills; holds the original of `root-cause-tracing`
- [[github-spec-kit|github/spec-kit]] ([github/spec-kit](../references/github-spec-kit.md)) and [[fission-ai-openspec|Fission-AI/OpenSpec]] ([Fission-AI/OpenSpec](../references/fission-ai-openspec.md)): the spec-driven tools the sdd plugin says it is based on

## Sources

- [Desk check: NeoLabHQ/context-engineering-kit v3.10.0](../../raw/repos/neolabhq-context-engineering-kit-desk-check-2026-11-21.md): the kaizen plugin and the reflexion hook read in full, every plugin's README, freshness through the GitHub API, what the kit took and why the rest is rejected.
- [Parts list: NeoLabHQ/context-engineering-kit 3.10.0](../../raw/data/neolabhq-context-engineering-kit-parts-3.10.0.md): all 269 parts, generated from the clone by `catalog_parts.py`.
