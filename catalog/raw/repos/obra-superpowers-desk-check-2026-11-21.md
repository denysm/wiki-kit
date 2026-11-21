---
title: "Desk check: obra/superpowers v7.0.2"
source: https://github.com/obra/superpowers/tree/v7.0.2
type: repos
authors: ["Jesse Vincent (obra)"]
source_date: 2026-11-03
ingested: 2026-11-21
repo: obra/superpowers
kind: plugin
version: "7.0.2"
licence: MIT
tags: [catalog, desk-check, kind-plugin, superpowers, claude-code, skills]
summary: "Every part of obra/superpowers v7.0.2 read from a read-only clone: 15 skills, one SessionStart hook with its ports to other harnesses, no commands or agents folders; the brainstorming visual companion and its telemetry; freshness from the GitHub API; which techniques this kit took into its own rules; the Tried log."
---

# Desk check: obra/superpowers v7.0.2

Read from a shallow clone of tag `v7.0.2` (commit `22f0b463e7a5e579904dd6211a520321035526f7`, committed 2026-11-03), at `$EXTERNAL/superpowers`. The clone was not modified; nothing was installed or enabled. Checked 2026-11-21. Version read by this desk check: 7.0.2.

## Repository facts

- Plugin manifest `.claude-plugin/plugin.json`: `"name": "superpowers"`, `"version": "7.0.2"`, `"license": "MIT"`, description "Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven techniques". The same version is in `package.json` and `.hermes-plugin/plugin.yaml`.
- `.claude-plugin/marketplace.json` is a development marketplace (`"name": "superpowers-dev"`) whose single plugin has `"source": "./"`.
- `LICENSE`: "MIT License", "Copyright (c) 2025 Jesse Vincent".
- Top-level folders that hold parts: `skills/` (15 skill folders) and `hooks/`. There is no `commands/` folder and no `agents/` folder. Other folders: `docs/` (design specs and plans of the project itself), `tests/`, `scripts/` (release and packaging tools), `assets/`, and one manifest folder per harness (`.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, `.devin-plugin`, `.kimi-plugin`, `.antigravity-plugin`, `.muse-plugin`, `.hermes-plugin`, `.opencode`, `.pi`).
- `RELEASE-NOTES.md` heading: "## v7.0.2 (2026-11-03)". The release "further tunes brainstorming's questions. It asks fewer of them, starts by asking why, and when there's a choice to make it gives you options to pick from." It also fixes the bootstrap on six harnesses and hardens the SDD and executing-plans helper scripts.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/obra/superpowers`: `pushed_at` 2026-11-03T23:24:58Z; licence `MIT`; default branch `main`; not archived.
- `gh api repos/obra/superpowers/releases/latest`: tag `v7.0.2`, published 2026-11-03T22:17:54Z.
- So the clone is at the latest release; nothing was pushed after the release day.

## Parts

### Hook: SessionStart (`hooks/hooks.json`, `hooks/session-start`, `hooks/run-hook.cmd`)

- `hooks.json` registers one `SessionStart` hook with matcher `"startup|clear|compact"` that runs `run-hook.cmd session-start`.
- `session-start` reads `skills/using-superpowers/SKILL.md` and emits it as additional context wrapped in `<EXTREMELY_IMPORTANT>` with the line "You have superpowers." So the whole using-superpowers skill enters every session at start, after `/clear` and after compaction.
- Needs: the plugin to be installed or loaded; bash (falls back to zsh on Unix). Without the plugin this hook does not run.
- Ports of the same bootstrap to other harnesses: `hooks/hooks-cursor.json` (Cursor `sessionStart`), `.opencode/plugins/superpowers.js` (OpenCode, injects the bootstrap into requests), `.pi/extensions/superpowers.ts` (Pi, `session_start`, `session_compact` and `context` events), `.hermes-plugin/` (Hermes Agent, `pre_llm_call`). They do the same job for their harness; none is used by Claude Code.

### Skill: brainstorming (`skills/brainstorming/SKILL.md`)

- Description: "You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning anything new, in software or out of it (a talk, a business, a renovation)."
- Method: read what exists before asking; one open question at a time, only "when the answer would change what gets built"; ask why first; lay out two or three approaches with a recommendation "in a message of its own"; play back each understood part in "about 200-300 words"; then a written design covering "intent and the why", "goals, non-goals, anti-goals", "constraints", "approaches", "the parts of the how they decided", "what's left to the builder".
- Builder check (`builder-check-prompt.md`): a fresh subagent reads the design as "a talented [DOMAIN]" builder and reports only the questions it would still need answered; answers are sorted into "Answered already", "Minor" and "Theirs".
- Hard gate: "Nothing gets built until your human partner approves the design doc". After approval the next step is "invoke superpowers:writing-plans and no other skill".
- Default place for the design: `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` in a software repo; "Your human partner's preferences override both."
- Needs: nothing to read it from the clone. The reference `superpowers:writing-plans` has to be replaced with the path of that skill's SKILL.md when the plugin is not loaded.

### Sub-part: brainstorming visual companion (`skills/brainstorming/visual-companion.md`, `skills/brainstorming/scripts/`)

- A local browser tab for mockups and side-by-side options. Offered "just-in-time", as a message of its own; started only after the user accepts: `bash scripts/start-server.sh --project-dir /path/to/project --open`.
- `scripts/server.cjs` uses only Node built-ins (`crypto`, `http`, `fs`, `path`; `child_process` and `os` for the browser launcher). It binds `localhost` by default (`BRAINSTORM_HOST` overrides), gates access with a random key in the URL and an HttpOnly cookie, and shuts down after "4 hours" idle by default ("Default 4 hours").
- With `--project-dir` it writes screens to `<project>/.superpowers/brainstorm/`; the guide says to add `.superpowers/` to `.gitignore`. Without it, files go to `/tmp`.
- Telemetry: the page header loads a logo from `https://primeradiant.com/brand/superpowers-visual-brainstorming-logo.png` with the Superpowers version as a query parameter. `server.cjs` drops the remote image when any of `SUPERPOWERS_DISABLE_TELEMETRY`, `DISABLE_TELEMETRY` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set to a true value. README, "Visual companion telemetry": the logo request "includes the version of Superpowers in use. It does not include any details about your project, prompt, or coding agent." and "To disable this, set the environment variable `SUPERPOWERS_DISABLE_TELEMETRY` to any true value."
- No other network call was found in the skills, hooks or scripts (search for `fetch(`, `https://` and `telemetry` across the clone outside `tests/`, release notes and design specs).
- Needs: Node.js, a browser.

### Skill: diagnosing-superpowers (`skills/diagnosing-superpowers/SKILL.md`)

- Description: "Use when a superpowers session went wrong and your human partner wants to know why".
- Reads session transcripts on disk, read-only; dispatches seven analyst subagents in parallel (skill timeline, plan adherence, repeated work, stumbles, quality evidence, request conflicts, cost and time); "Every finding cites `path:line`." Writes a case and report under `~/.superpowers/diagnosing-superpowers/<session-id>/`. Optionally searches GitHub issues and files one, "only after approval"; builds a scrubbed bundle only when asked.
- Needs: subagents, `gh` for the issue step; a session that ran Superpowers skills to be useful.

### Skill: dispatching-parallel-agents (`skills/dispatching-parallel-agents/SKILL.md`)

- Description: "Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies".
- One focused, self-contained agent per independent problem domain, all dispatched in one response; then review summaries, check for conflicts, run the full suite. "Don't use when" failures are related or agents would edit the same files.
- Needs: a subagent tool. No cross-references to other skills.

### Skill: executing-plans (`skills/executing-plans/SKILL.md`, `scripts/task-start`, `scripts/task-done`)

- Description: "Use when executing an implementation plan in the current session as the implementer yourself".
- Inline execution of a writing-plans plan: TDD per step, a ledger in `<repo-root>/.superpowers/sdd/<plan-basename>/progress.md` that survives compaction, `Ruling:` lines for every deviation, and one fresh whole-branch review at the end. Only four things stop it, starting with "an irreversible or destructive operation".
- Needs: git, a plan in the writing-plans format, bash for its scripts and for SDD's `sdd-workspace` and `review-package`. References eight other skills: `test-driven-development`, `verification-before-completion`, `using-git-worktrees`, `requesting-code-review`, `systematic-debugging`, `subagent-driven-development`, `finishing-a-development-branch` and `writing-plans`.

### Skill: finishing-a-development-branch (`skills/finishing-a-development-branch/SKILL.md`)

- Description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work".
- Runs the full suite; detects normal repo, worktree or detached HEAD; presents "exactly these 3 options" (merge locally, push and open a PR, keep as-is); deletes only on the typed word `discard`; removes only worktrees under `.worktrees/` or `worktrees/`.
- Needs: git, the forge CLI for the PR option.

### Skill: receiving-code-review (`skills/receiving-code-review/SKILL.md`)

- Description: "Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable".
- Read, restate, verify against the codebase, then answer with a technical acknowledgment or reasoned pushback; clarify every unclear item before implementing any; YAGNI check (grep for real usage); no performative agreement or thanks.
- Needs: nothing beyond the review text and the codebase.

### Skill: requesting-code-review (`skills/requesting-code-review/SKILL.md`, `code-reviewer.md`)

- Description: "Use when completing tasks, implementing major features, or before merging to verify work meets requirements".
- Dispatches a reviewer subagent with the `code-reviewer.md` template, a description, the plan and a `BASE_SHA..HEAD_SHA` range; fix Critical at once, Important before going on, note Minor.
- Needs: a subagent tool and git.

### Skill: subagent-driven-development (`skills/subagent-driven-development/SKILL.md`, prompts, `references/`, `scripts/`)

- Description: "Use when executing implementation plans with independent tasks in the current session".
- A fresh implementer subagent per task, a task review (spec compliance and quality) after each, a fix loop with a round cap, a ledger in `.superpowers/sdd/`, and a final whole-branch review on "the most capable available model". Model selection: "Use the least powerful model that can handle each role"; "Always specify the model explicitly when dispatching a subagent."
- Needs: a subagent tool, git, bash for `scripts/sdd-workspace`, `task-brief`, `review-package`, `sdd-repo`. The workspace script writes its own `.gitignore` into `.superpowers/sdd/`.

### Skill: systematic-debugging (`skills/systematic-debugging/SKILL.md` and five supporting files)

- Description: "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes".
- "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST". Four phases: root cause, pattern analysis, one hypothesis tested minimally, fix with a failing test. "If ≥ 3: STOP and question the architecture". Supporting files: `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md` with a TypeScript example, `find-polluter.sh`.
- Needs: nothing to read it; references `superpowers:test-driven-development` and `superpowers:verification-before-completion`.

### Skill: test-driven-development (`skills/test-driven-development/SKILL.md`, `writing-good-tests.md`)

- Description: "Use when implementing any feature or bugfix, before writing implementation code".
- "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"; red, verify red, green, verify green, refactor; code written before its test is deleted. Exceptions only with the human partner: "Throwaway prototypes", "Generated code", "Configuration files". The whole project suite, not only the new test, must pass.
- Needs: a test runner in the target project.

### Skill: using-git-worktrees (`skills/using-git-worktrees/SKILL.md`)

- Description: "Use when starting feature work that needs isolation from current workspace or before executing implementation plans".
- Detects an existing worktree first (with a submodule guard); asks for consent; prefers the harness's native worktree tool ("a tool with a name like `EnterWorktree`"), falls back to `git worktree add` under an ignored `.worktrees/`; then installs dependencies and runs a baseline test.
- Needs: git; the project's package manager for the setup step.

### Skill: using-superpowers (`skills/using-superpowers/SKILL.md`, `references/*-tools.md`)

- Description: "Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions".
- Body: "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill." It sends "Let's build X" to brainstorming and "Fix this bug" to systematic-debugging. It has a `<SUBAGENT-STOP>` block for dispatched subagents and says user instructions (CLAUDE.md and the like) take precedence over skills.
- `references/claude-code-tools.md`: an opt-in way to run subagent-driven development one layer down, through one orchestrator subagent on a mid-tier model.
- This is the text the SessionStart hook injects into every session.

### Skill: verification-before-completion (`skills/verification-before-completion/SKILL.md`)

- Description: "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs".
- "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE". Gate: identify the command that proves the claim, run it fresh, read the output, then claim. Red flags include "should", "probably", "seems to" and trusting agent success reports.
- Needs: nothing.

### Skill: writing-plans (`skills/writing-plans/SKILL.md`)

- Description: "Use when you have a spec or requirements for a multi-step task, before touching code".
- A plan for "an engineer who has not seen this codebase or this spec": header with Goal, Architecture, Tech Stack, Spec, Global Constraints and Review Focus; tasks with Files and Interfaces blocks and checkbox steps in RED-GREEN order; a self-review; saved to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`. Hands off to subagent-driven-development or executing-plans.
- Needs: nothing to write the plan; its executors need git and the scripts above.

### Skill: writing-skills (`skills/writing-skills/SKILL.md`, eight `references/` files, `render-graphs.js`)

- Description: "Use when creating new skills, editing existing skills, or verifying skills work before deployment".
- "Writing skills IS Test-Driven Development applied to process documentation." Run a pressure scenario with a subagent without the skill, record its rationalizations verbatim, write the smallest skill that answers them, re-run with the skill, close loopholes. "NO SKILL WITHOUT A FAILING TEST FIRST". Also: a description says only when to use the skill, and "Match the Form to the Failure" (prohibition for discipline failures, a positive recipe for wrong-shaped output).
- `render-graphs.js` renders the `dot` blocks of a SKILL.md to SVG (needs Node and Graphviz).
- Needs: a subagent tool for the baseline runs.

## Cross-references between skills

Counted from `superpowers:<name>` strings in each SKILL.md. Skills that name others: brainstorming (writing-plans), executing-plans (eight skills), subagent-driven-development (finishing-a-development-branch, using-git-worktrees), systematic-debugging (test-driven-development, verification-before-completion), using-superpowers (brainstorming, systematic-debugging), writing-plans (executing-plans, subagent-driven-development, using-git-worktrees), writing-skills (test-driven-development). The other eight name none. When a skill is read from the clone without the plugin, each `superpowers:<name>` has to be read as `$EXTERNAL/superpowers/skills/<name>/SKILL.md`.

## How this kit uses it

From the kit's own files (paths relative to the kit root).

- `docs/PROJECT-CONTEXT.md`, section "Third-party skills (2026-11-06)": "Taken, in the kit's own words: the skill-testing method of superpowers `writing-skills` (`docs/testing-specialists.md`); interview rules of its `brainstorming` (the specialist template); "no completion claim without a fresh check" from `verification-before-completion` (`agents/COMMON.md`)".
- Same section: "Not taken: the superpowers plugin as a whole (its session-start hook injects a "use a skill before any response" rule into every session, and its brainstorm server loads a remote logo unless telemetry is turned off)".
- `docs/testing-specialists.md`, section "Source": "Adapted from the skill-testing method in the `writing-skills` skill of obra/superpowers (MIT): run without the skill first, record the excuses, write the smallest fix, re-run, repeat."
- `templates/specialist/SKILL.md`, conversation rules: "one question per message; when the request is already complete, skip the questions. After a long answer from the owner, play back a short summary before going on. Offer two or three options with a recommendation, not one."
- `agents/COMMON.md`: "Every count and result comes from a command you ran in this session (lint, `raw_check.py`, `check_evidence.py`), with its exit status. Do not write "should pass" or "probably fine"; name every check you did not run."
- Rule for third-party skills, as the kit owner set it on 2026-11-19: do not install third-party plugins to use their skills; shallow-clone the release tag read-only and read `SKILL.md` from there, replacing plugin-qualified references with absolute paths; when the plugin's hooks or commands are really needed, try it in a sandbox, one terminal session `claude --plugin-dir <clone>` from a scratch folder; a real install in any scope is a separate decision. The reason given: the SessionStart hook pushes skill use into every session (slower, more questions), and speed and a small budget matter.
- No record was found of a sandbox session with the plugin loaded, or of any other skill of this repository used in real work.

## Tried log

- 2026-11-19..21: `brainstorming`, read from the clone at v7.0.2 (not as a plugin), used to design this catalog over three sessions. Result: 30 design decisions, numbered 1 to 30 in the design notes (card shape, part statuses, areas, freshness check, publishing rules). The writing-plans handoff was skipped for this design; the design document goes to a builder check instead. Cost: not measured per skill.
