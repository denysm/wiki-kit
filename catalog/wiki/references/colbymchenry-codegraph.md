---
title: "colbymchenry/codegraph"
category: reference
kind: cli
areas: [writing-code-with-agents]
repo: colbymchenry/codegraph
version: "1.6.4"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/colbymchenry-codegraph-desk-check-2026-11-21.md
  - raw/notes/trials/2026-11-21-codegraph-per-repo-mcp.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-writing-code-with-agents, kind-cli, codegraph, mcp, code-navigation, claude-code, sqlite, tree-sitter]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "CLI that indexes a code repository into a local SQLite graph and serves it to coding agents over MCP (one tool, codegraph_explore), with shell commands for callers, impact, affected tests and cycles, and an optional Claude Code prompt hook. The MCP server is in use per repository at 1.6.2 with telemetry off; the user-wide install is rejected for its per-message token cost; the other commands wait for a task."
---

# colbymchenry/codegraph

> A command-line tool (kind `cli`, licence MIT, version `1.6.4` read) that parses a code repository with tree-sitter into a local SQLite graph of symbols and edges and serves it to coding agents over MCP, so an agent asks "what calls this" instead of grepping. Its installer can also wire a Claude Code prompt hook. Here the MCP server is connected in one repository only, never user-wide.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Ask how code works, what calls a function or how a request reaches the database, without grep and read loops | `serve --mcp` | writing-code-with-agents |
| Give subagents, or an agent without MCP, the same answer from a shell | `explore` | writing-code-with-agents |
| Have structural prompts arrive with graph context already attached | `prompt-hook` | writing-code-with-agents |
| Connect one repository's agent to the graph, and only that repository | `install --location=local` | writing-code-with-agents |
| Build the graph of a repository, keeping it out of git | `init` | writing-code-with-agents |
| Rebuild the graph after an upgrade | `index` | writing-code-with-agents |
| Find which test files a change touches | `affected` | writing-code-with-agents |
| See what a change to one symbol would affect | `impact` | writing-code-with-agents |
| List the callers or callees of one function from a shell | `callers`, `callees` | writing-code-with-agents |
| Find the types that implement an interface or extend a class | `implementations` | writing-code-with-agents |
| Find circular imports between files | `cycles` | writing-code-with-agents |
| Gather the symbols and code relevant to a task description | `context` | writing-code-with-agents |
| Look at an indexed project as a graph in a browser | `ui` | writing-code-with-agents |
| Switch usage telemetry off | `telemetry` | writing-code-with-agents |
| Not this: connect the graph to every project and every session. Rejected: the MCP server and hook cost about 2.5k tokens per message | `install` (global location) | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch v1.6.4 https://github.com/colbymchenry/codegraph $EXTERNAL/codegraph`, read-only, to read what it does. Running it needs the installed CLI.
- **Version**: `1.6.4` read, the latest release, published 2026-11-20; `1.6.2` is installed. Compare with upstream before relying on this card: `gh api repos/colbymchenry/codegraph/releases/latest --jq .tag_name`.
- **Read first**: README "CLI Reference" and "MCP Tools", `TELEMETRY.md`, and `src/installer/targets/claude.ts` for exactly what `install` writes where.
- **In use**: the MCP server (`serve --mcp`) at `1.6.2`, installed from npm, connected per repository only through a local MCP config in one tooling repository; never user-wide. Telemetry switched off with `codegraph telemetry off`. Upgrading to `1.6.4` means running `codegraph index` in that repository afterwards.
- **Switch off**: telemetry (`codegraph telemetry off`, or `CODEGRAPH_TELEMETRY=0`, `DO_NOT_TRACK=1`, or `--no-telemetry` in the MCP entry's args); the daily update check (`CODEGRAPH_NO_UPDATE_CHECK=1`); the prompt hook without uninstalling (`CODEGRAPH_NO_PROMPT_HOOK=1`). Decline the installer's beta waitlist question.
- **Where `install` writes** (Claude Code): global puts the MCP entry in `~/.claude.json` (`"alwaysLoad": true`), the permission and the `UserPromptSubmit` hook in `~/.claude/settings.json` and an instructions block in `~/.claude/CLAUDE.md`, loading in every project; local puts the same three in the current folder's `./.mcp.json`, `./.claude/settings.json` and `./.claude/CLAUDE.md`. `codegraph install --print-config claude --location=local` prints the snippet and writes nothing.
- **Do not install**: `codegraph install` at the global location, `codegraph install --yes` (its defaults are global, auto-allow and the prompt hook on), `npx @colbymchenry/codegraph`, or the `curl … | sh` and `irm … | iex` one-liners. Connecting another repository, upgrading, or wiring the prompt hook waits for the user's yes.

## What's inside

Parts: the 27 commands of the CLI (three hidden: `serve --mcp`, `prompt-hook`, `ui`), with `install` split by location, plus the library API. The repository's own `.claude/skills/` (`add-lang`, `agent-eval`) serve its contributors and are not parts here.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `serve --mcp` | MCP server over stdio: one tool, `codegraph_explore` (source, call paths and blast radius in one call); seven more tools unlisted unless named in `CODEGRAPH_MCP_TOOLS`; usage instructions sent in the `initialize` response every session; watches files and syncs; one shared daemon per project. | in use | The CLI on PATH, an indexed project, an MCP entry in that project only. Nothing leaves the machine with telemetry off and `CODEGRAPH_NO_UPDATE_CHECK=1`. | After upgrading from `1.6.2`, run `codegraph index` and re-check the per-message cost of the server's instructions in that repository. |
| `telemetry` | Shows or changes the telemetry choice (`status`, `on`, `off`); off stores the choice and deletes unsent data. | in use | The CLI. | After each upgrade, `codegraph telemetry status` still says off. |
| `install` (global location, also `--yes`) | Wires the MCP server, auto-allow permission, prompt hook and an instructions block into user-wide agent configs that load in every project. | rejected | The CLI; writes user-scope files; the interactive run may call npm and the beta waitlist. | Rejected: the MCP server and hook cost about 2.5k tokens per message and would inflate every session. Revisit if a release makes them much smaller, measured in a one-repository sandbox. |
| `install --location=local` | Writes the same three entries into the current project only; prompt hook and auto-allow are separate questions; `--print-config` writes nothing. | candidate | The CLI; writes `./.mcp.json` and `./.claude/`. | Try it when a second repository needs the graph; answer no to the prompt hook unless it is wanted there. |
| `prompt-hook` | Claude Code `UserPromptSubmit` hook: on a structural prompt injects `codegraph_explore` output (capped at 9,000 characters), on prose matching symbol names a short symbol list, otherwise nothing. | candidate | Claude Code, an indexed project, the hook in that project's `settings.json`. Runs on every prompt. | Try it in the one indexed repository and compare the cost per prompt with and without it; never in user settings. |
| `explore` | The `codegraph_explore` answer printed in a shell; the instructions block points subagents at it. | candidate | The CLI, an index. | Try it from a subagent in the indexed repository instead of grep. |
| `init` | Creates `.codegraph/` and builds the graph; `--local-only` keeps it out of git; refuses a home folder or root without `--force`. | candidate | The CLI; writes `.codegraph/` into the project. | Try `--local-only` on the next repository to index. |
| `uninit` | Deletes the project's `.codegraph/`. | candidate | The CLI. | Try it when a repository no longer needs the graph. |
| `index` | Rebuilds the whole index. | candidate | The CLI. | Try it after the upgrade to `1.6.4`, which asks for a re-index. |
| `sync` | Incremental update since the last index. | candidate | The CLI. | Try it when the server runs with `--no-watch`. |
| `status` | Index statistics; warns about an index built by an older version or a run that did not finish. | candidate | The CLI. | Try it right after an upgrade. |
| `unlock` | Removes a stale lock file that blocks indexing. | candidate | The CLI. | Try it when indexing reports a lock after a killed run. |
| `query` | Searches symbols by name. | candidate | The CLI, an index. | Try it to find a symbol whose file is unknown. |
| `context` | Symbols, relationships and code for a task description. | candidate | The CLI, an index. | Try it when briefing an agent on a change. |
| `node` | One symbol's source with callers and callees, or a file with line numbers and dependents. | candidate | The CLI, an index. | Try it on a symbol before editing it. |
| `files` | File structure from the index (tree, flat, grouped, package). | candidate | The CLI, an index. | Try it when orienting in an unfamiliar repository. |
| `callers` | Functions and methods that call a symbol. | candidate | The CLI, an index. | Try it before renaming a function. |
| `callees` | Functions and methods a symbol calls. | candidate | The CLI, an index. | Try it when tracing what a function depends on. |
| `impact` | What code is affected by changing a symbol. | candidate | The CLI, an index. | Try it before changing a shared helper. |
| `implementations` | Types that implement or extend a trait, interface or class. | candidate | The CLI, an index. | Try it in a repository with interfaces and several implementations. |
| `affected` | Test files affected by changed files, from `git diff --name-only` on stdin; `--cross-tier` follows HTTP calls, queues and events. | candidate | The CLI, an index, git. | Try it to run only the affected tests before a commit. |
| `cycles` | Circular imports between files; exits 1 when there are any. | candidate | The CLI, an index. | Try it as a check in a repository with import problems. |
| `daemon` | Lists running background daemons and stops the one picked. | candidate | The CLI. | Try it when a daemon outlives its sessions. |
| `uninstall` | Removes CodeGraph from each configured agent at one location, and the CLI unless `--keep-cli`. | candidate | The CLI. | Try it if the repository's MCP config is ever removed. |
| `upgrade` | Updates to the latest or a pinned release; `--check` only reports; re-runs `install --refresh`. | candidate | The CLI; downloads from GitHub. | Try `--check` before the move from `1.6.2` to `1.6.4`; the upgrade itself waits for the user's yes. |
| `version` | Prints the installed version. | candidate | The CLI. | Try it after any upgrade. |
| `help` | Help for all commands or one. | candidate | The CLI. | Try it before using a command not described here. |
| `ui` | Browser viewer of the indexed project as a graph; hidden unless `CODEGRAPH_UI=1`; serves on `localhost` only, no outbound connections. | candidate | The CLI, an index, a browser. | Try it when a call chain is easier to see than to read. |
| Library API (`CodeGraph` class) | Programmatic index, search, callers, context and impact from your own Node process. | candidate | `npm i @colbymchenry/codegraph`, Node 22.5+. | Try it only if a kit script needs the graph directly. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-21 | Code navigation for a coding agent in one tooling repository | `serve --mcp`, `telemetry` | Real use at `1.6.2` from npm: MCP server connected through a local MCP config in that repository only, never user-wide; telemetry switched off. Start date not recorded. | Not measured per task; about 2.5k tokens per message while connected | [use record](../../raw/notes/trials/2026-11-21-codegraph-per-repo-mcp.md) |

## Verdict

The MCP server is worth its cost only where code is navigated, so it is connected in one repository and telemetry is off; the user-wide install is rejected because its server and hook would charge every session. The shell commands (`affected`, `impact`, `callers`, `cycles`) and the prompt hook are candidates that run on the CLI already installed. Revisit when the installed `1.6.2` is upgraded (re-index, re-check the per-message cost), or when a release shrinks the server's instructions enough to reconsider the hook.

## See Also

- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; code navigation for coding agents
- [[obra-superpowers|obra/superpowers]] ([obra/superpowers](../references/obra-superpowers.md)): process skills for the same kind of coding work

## Sources

- [Desk check: colbymchenry/codegraph v1.6.4](../../raw/repos/colbymchenry-codegraph-desk-check-2026-11-21.md): every command read from the clone, the installer's targets and locations, the prompt hook, telemetry and outbound calls, freshness through the GitHub API, the kit's use of it.
- [Use record: codegraph MCP server, per-repository code navigation](../../raw/notes/trials/2026-11-21-codegraph-per-repo-mcp.md): the real use behind the `in use` rows and the Tried row, and the reason for rejecting the user-wide install.
