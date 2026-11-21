---
title: "obra/superpowers"
category: reference
kind: plugin
areas: [designing-something-new, writing-code-with-agents, building-skills-and-plugins]
repo: obra/superpowers
version: "7.0.2"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/obra-superpowers-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-designing-something-new, area-writing-code-with-agents, area-building-skills-and-plugins, kind-plugin, claude-code, skills, brainstorming, tdd, debugging, code-review, planning]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Claude Code plugin of process skills for coding agents: design by interview, plans, plan execution with ledgers and reviews, TDD, debugging, code review, worktrees, skill testing, plus a SessionStart hook. Its skills are read one by one from a clone; the plugin and its every-session hook are not installed. brainstorming is in use, two techniques are in the kit's own rules, the router and hook are rejected, twelve parts wait for a task."
---

# obra/superpowers

> A Claude Code plugin (kind `plugin`, licence MIT, version `7.0.2` read): 15 process skills for coding agents, from designing by interview to finishing a branch, plus a SessionStart hook that injects a "use a skill first" rule into every session. Here its skills are read from a clone, part by part, and the plugin is not installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Work out what to build before building it, in software or outside it (a talk, a business) | `brainstorming` | designing-something-new |
| Show mockups, layouts or side-by-side options while designing | `brainstorming` visual companion | designing-something-new |
| Turn a spec or approved design into a step-by-step implementation plan | `writing-plans` | writing-code-with-agents |
| Execute a written plan in a code repo yourself, one review at the end | `executing-plans` | writing-code-with-agents |
| Execute a written plan with a fresh subagent and a review per task | `subagent-driven-development` | writing-code-with-agents |
| Isolate feature work from the current branch | `using-git-worktrees` | writing-code-with-agents |
| Decide how to integrate a finished branch (merge, PR, keep) | `finishing-a-development-branch` | writing-code-with-agents |
| Find the root cause of a bug or failing test before fixing it | `systematic-debugging` | writing-code-with-agents |
| Write code test-first | `test-driven-development` | writing-code-with-agents |
| Work on several independent problems at once | `dispatching-parallel-agents` | writing-code-with-agents |
| Get a review of finished work | `requesting-code-review` | writing-code-with-agents |
| Act on review findings without blind agreement | `receiving-code-review` | writing-code-with-agents |
| Claim that work is done, fixed or passing | `verification-before-completion` (technique already in the kit's rules) | writing-code-with-agents |
| Write, change or test a skill | `writing-skills` (technique already in the kit's rules) | building-skills-and-plugins |
| Find out why a session that used these skills went wrong | `diagnosing-superpowers` | building-skills-and-plugins |
| Not this: route every request to a skill automatically. Rejected: the hook injects that rule into every session | `using-superpowers`, SessionStart hook | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch v7.0.2 https://github.com/obra/superpowers $EXTERNAL/superpowers`, read-only. Never edit the clone.
- **Version**: `7.0.2`, the latest release, published 2026-11-03. Before relying on this card, compare with upstream: `gh api repos/obra/superpowers --jq .pushed_at` and `gh api repos/obra/superpowers/releases/latest --jq .tag_name`. A newer version of an `in use` part needs a new desk check.
- **Read**: `$EXTERNAL/superpowers/skills/<skill>/SKILL.md` and the files it names in its own folder. Read every `superpowers:<name>` reference as `$EXTERNAL/superpowers/skills/<name>/SKILL.md`. Run bundled scripts by absolute path through their interpreter (`bash …/scripts/<script>`).
- **In use**: `brainstorming` at `7.0.2`, read from the clone (`$EXTERNAL/superpowers/skills/brainstorming/SKILL.md`), not as a plugin, to design something before building it. The design doc goes where the user says, not to the default `docs/superpowers/specs/`; the `superpowers:writing-plans` handoff is read as a path into the clone, or skipped when the doc goes to a builder check instead.
- **Switch off**: set `SUPERPOWERS_DISABLE_TELEMETRY=1` before starting the visual companion (`DISABLE_TELEMETRY` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` also work); the remote logo is the only network call found. Add `.superpowers/` to the target repo's `.gitignore` when the visual companion, `executing-plans` or `subagent-driven-development` write there.
- **Do not install**: the plugin, in any scope (marketplace, `/plugin install`, or its `hooks.json` copied into settings). Its SessionStart hook would inject `using-superpowers` into every session. When the hook or plugin behaviour itself has to be seen, run one terminal session `claude --plugin-dir $EXTERNAL/superpowers` from a scratch folder and record the result under Tried; a real install waits for the user's yes.

## What's inside

Parts: 15 skills in `skills/`, one hook in `hooks/` (with its ports to other harnesses), and the visual companion of `brainstorming`, listed as its own row because it runs a local server and has the only network call found. There is no `commands/` or `agents/` folder.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `brainstorming` | Design by interview: reads what exists, asks one open question at a time, asks why first, lays out two or three approaches with a recommendation, plays each part back, writes a design doc (intent, goals, non-goals, anti-goals, constraints, approaches, what is left to the builder), then sends it to a builder check (a fresh subagent reads the doc as the builder would and lists the questions it still has). Nothing is built before the doc is approved. | in use | Works from the clone. Read `superpowers:writing-plans` as that skill's path. The builder check needs a subagent tool. Point the design doc at your own location; the default is `docs/superpowers/specs/`. | On a release after `7.0.2`, re-read `SKILL.md` and `builder-check-prompt.md` before the next design: the `7.0.2` release retuned its questions. |
| `brainstorming` visual companion | Local browser tab for mockups and options, started only after the user accepts. A Node server on `localhost` with a random key in the URL; stops after 4 hours idle. Writes screens to `.superpowers/brainstorm/` in the project. | candidate | Works: `bash scripts/start-server.sh --project-dir <project> --open` from the skill folder. Needs Node.js and a browser. Loads a remote logo unless telemetry is off. | Try it on a design question where the user picks the look (a screen, a layout, a diagram). Start it with `SUPERPOWERS_DISABLE_TELEMETRY=1`. |
| `diagnosing-superpowers` | Reads session transcripts read-only, runs seven analyst subagents in parallel, writes a report where every finding cites `path:line`; files a GitHub issue only after approval. | candidate | Works on transcripts on disk, but it is built for sessions that ran these skills. Writes under `~/.superpowers/diagnosing-superpowers/`. Needs subagents; `gh` for the issue step. | Try it when a sandbox session with the plugin loaded goes wrong (too slow, too costly, a skill did not fire). |
| `dispatching-parallel-agents` | One focused, self-contained agent per independent problem, all dispatched in one response; then check for conflicts and run the full suite. Not for related failures or shared files. | candidate | Works; needs a subagent tool. Names no other skill. | Try it on two or more unrelated failures with no shared files, for example failing tests in different scripts. |
| `executing-plans` | Executes a `writing-plans` plan inline: TDD per step, a ledger (a progress file, `progress.md`) in `.superpowers/sdd/` that survives compaction, a `Ruling:` line (a written ruling on what to do and why) for every deviation from the plan, one fresh whole-branch review at the end. | candidate | Works if its scripts are run by absolute path (`bash $EXTERNAL/superpowers/skills/executing-plans/scripts/task-start`). Needs git, bash and a plan in the `writing-plans` format. Names eight other skills. | Try it on an approved plan for a code repo with mostly independent tasks, when one review at the end is enough. |
| `finishing-a-development-branch` | Runs the full suite, detects normal repo, worktree or detached HEAD, offers merge, PR or keep; deletes only on the typed word `discard`; removes only worktrees it owns. | candidate | Works; needs git, and the forge CLI (the code host's command-line tool) for the PR option. | Try it at the end of the first branch built with `executing-plans` or `subagent-driven-development`. |
| `receiving-code-review` | Read, restate, verify against the codebase, then fix or push back with reasons; clarify every unclear item before implementing any; YAGNI check by grepping for real usage; no performative agreement. | candidate | Works; needs only the review text and the code. | Try it on the next set of review findings on a pull request or from a reviewer agent. |
| `requesting-code-review` | Dispatches a reviewer subagent with the `code-reviewer.md` template, the plan and a git range; Critical fixed at once, Important before going on, Minor noted. | candidate | Works; needs a subagent tool and git. | Try it before merging a multi-file change in a script repo, and compare its findings with the review used so far. |
| `subagent-driven-development` | Executes a plan with a fresh implementer subagent per task, a spec and quality review after each, a capped fix loop, a ledger, and a final review on the most capable model. Picks the cheapest model that can do each role and always names the model. | candidate | Works if its scripts are run by absolute path. Needs a subagent tool, git and bash. Writes `.superpowers/sdd/` with its own `.gitignore`. | Try it on a plan with many independent tasks where a review gate per task is wanted; record the cost next to `executing-plans`. |
| `systematic-debugging` | No fix before root-cause investigation: read errors, reproduce, check recent changes, instrument component boundaries, test one hypothesis at a time, fix with a failing test; after three failed fixes, question the architecture. Helper files for root-cause tracing, defense in depth, condition-based waiting. | candidate | Works; plain text plus helper files in the same folder. | Try it on the next bug or failing test that the first fix does not solve. |
| `test-driven-development` | No production code without a failing test first; red, verify red, green, verify green, refactor; code written before its test is deleted. Exceptions only with the user: throwaway prototypes, generated code, configuration files. | candidate | Works; needs a test runner in the target project. | Try it on a new feature or bug fix in a script that already has a test suite; not on a throwaway spike. |
| `using-git-worktrees` | Detects an existing worktree first, asks for consent, prefers the harness's own worktree tool, falls back to `git worktree add` under an ignored `.worktrees/`, then sets up and runs a baseline test. | candidate | Works; needs git. In Claude Code the skill itself prefers the native `EnterWorktree` tool. | Try it on feature work in a code repo that must not touch the current branch; check that it picks the native tool. |
| `using-superpowers` | The router: invoke a skill if there is "even a 1% chance" it applies, before any reply, including clarifying questions. This is the text the hook injects into every session. | rejected | Readable, but it exists to be injected by the hook; without the plugin it does nothing. User instructions take precedence over it. | Rejected: it puts a skill check before every reply in every session (slower, more questions). Revisit when the hook becomes opt-in, or a one-session sandbox shows the extra cost and questions are acceptable. |
| `verification-before-completion` | No completion claim without fresh evidence: name the command that proves the claim, run it, read the output, then claim; "should" and "probably" are red flags; agent reports are verified, not trusted. | method taken | Works; needs nothing. The kit's agent rules carry it in their own words (`agents/COMMON.md`). | Re-read when a release changes this skill; the kit rule stands on its own. |
| `writing-plans` | Writes a plan for an engineer who has not seen the code or the spec: Goal, Architecture, Global Constraints, Review Focus; tasks with files, interfaces and RED-GREEN checkbox steps; a self-review; then hands off to one of the two executors. | candidate | Works; saves to `docs/superpowers/plans/` unless told otherwise. Its executors need git and the scripts above. | Try it when an approved design must become a multi-step plan for a code repo. It was skipped for this catalog's design. |
| `writing-skills` | Skill writing as TDD: run a pressure scenario without the skill, record the excuses verbatim, write the smallest skill that answers them, re-run with it, close loopholes. Also: a description says only when to use the skill; match the form of the guidance to the kind of failure. | method taken | Works; baseline runs need a subagent tool; `render-graphs.js` needs Node and Graphviz. The kit's specialist testing method is adapted from it (`docs/testing-specialists.md`). | Re-read before the kit writes or changes a skill or specialist, and when a release changes the testing method. |
| SessionStart hook (`hooks/hooks.json`, `hooks/session-start`; ports for Cursor, OpenCode, Pi, Hermes Agent) | On startup, `/clear` and compaction, injects the whole `using-superpowers` skill into the session as additional context. | rejected | Does not run without the plugin; that is why the plugin is not installed. | Rejected for the same reason as `using-superpowers`. Revisit under the same conditions. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-19 to 2026-11-21 | Designing a catalog of tools for an agent-maintained knowledge base | `brainstorming` | Real use, read from the clone at `7.0.2`, not as a plugin: 30 design decisions, a design doc and a sample card. The `writing-plans` handoff was skipped; the design doc went to a builder check instead. | not measured per skill | [use record](../../raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md) |

## Verdict

No verdict for the repository as a whole: its skills are read from the clone part by part, and the plugin is not installed. One skill is in real use, two techniques live in the kit's own rules, the auto-routing pair is rejected, and the other twelve parts are candidates waiting for a matching task. Revisit when the freshness check shows a release after `7.0.2` (re-check `brainstorming` first), when the SessionStart hook becomes opt-in, or when a code-repo task needs the chain from plan to merged branch.

## See Also

- [[area-designing-something-new|Designing something new]] ([Designing something new](../topics/area-designing-something-new.md)): area page; `brainstorming` and its visual companion
- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; plans, execution, debugging, review, branches
- [[area-building-skills-and-plugins|Building skills and plugins]] ([Building skills and plugins](../topics/area-building-skills-and-plugins.md)): area page; `writing-skills`, `diagnosing-superpowers`

## Sources

- [Desk check: obra/superpowers v7.0.2](../../raw/repos/obra-superpowers-desk-check-2026-11-21.md): every part read from the clone, freshness checked through the GitHub API, the kit's use of it.
- [Use record: superpowers brainstorming, designing a tool catalog](../../raw/notes/trials/2026-11-21-superpowers-brainstorming-catalog-design.md): the real use of `brainstorming` behind its `in use` status and the Tried row.
