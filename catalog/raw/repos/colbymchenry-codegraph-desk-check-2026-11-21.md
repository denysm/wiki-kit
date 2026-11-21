---
title: "Desk check: colbymchenry/codegraph v1.6.4"
source: https://github.com/colbymchenry/codegraph/tree/v1.6.4
type: repos
authors: ["Colby Mchenry (colbymchenry)"]
source_date: 2026-11-20
ingested: 2026-11-21
repo: colbymchenry/codegraph
kind: cli
version: "1.6.4"
licence: MIT
tags: [catalog, desk-check, kind-cli, codegraph, mcp, code-navigation, claude-code]
summary: "colbymchenry/codegraph v1.6.4 read from a read-only clone: a CLI that indexes a code repository into a local SQLite graph and serves it to coding agents over MCP, plus an optional Claude Code UserPromptSubmit hook. Every command read from the CLI reference and its option definitions; the installer's targets and locations, the prompt hook, telemetry, the update check and the beta signup read in the source; freshness from the GitHub API; how it is used here (MCP server per repository at 1.6.2, telemetry off, never user-wide)."
---

# Desk check: colbymchenry/codegraph v1.6.4

Read from a shallow clone of tag `v1.6.4` (commit `461a5d87a873a4932997cd9a49042ab30e45a675`, committed 2026-11-20), at `$EXTERNAL/codegraph`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 1.6.4.

## Repository facts

- `package.json`: `"name": "@colbymchenry/codegraph"`, `"version": "1.6.4"`, `"license": "MIT"`, `"bin": { "codegraph": "./dist/bin/codegraph.js" }`; description "Supercharge AI coding agents with semantic code intelligence — surgical context, fewer tool calls, faster answers. 100% local."
- `LICENSE`: "MIT License", copyright 2026 by the upstream author.
- `CHANGELOG.md` heading: "## [1.6.4] - 2026-11-20"; the version in use here is "## [1.6.2] - 2026-10-03".
- What it is (README "How It Works"): a Rust kernel parses source with tree-sitter grammars into nodes (functions, classes, methods) and edges (calls, imports, extends, implements); everything goes into a local SQLite database (`.codegraph/codegraph.db`) with FTS5 full-text search; the MCP server watches the project and syncs changes after a "2-second quiet window".
- Releases ship a self-contained build with a bundled Node runtime for Windows, macOS and Linux (x64 and arm64); the npm package needs nothing compiled.
- Folders: `src/` (CLI, MCP server, installer, telemetry, upgrade, viewer server), `codegraph-kernel/` (Rust kernel), `ui/` (browser viewer), `telemetry-worker/` and `telemetry-dashboard/` (the public telemetry endpoint and its dashboard), `site/`, `docs/`, `scripts/`, `__tests__/`.
- `.claude/skills/add-lang` and `.claude/skills/agent-eval` are skills for the project's own contributors (add a language, benchmark retrieval with and without CodeGraph). They are not parts of the tool for its users.
- 1.6.4 release notes, "Highlights": "The prompt hook now asks the CodeGraph server already running for your project instead of loading the index again on every prompt"; "Upgrading: re-index your projects with `codegraph index` after this release."

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/colbymchenry/codegraph`: `pushed_at` 2026-11-20T23:39:45Z; licence `MIT` (matches the licence file); default branch `main`; not archived.
- `gh api repos/colbymchenry/codegraph/releases/latest`: tag `v1.6.4`, published 2026-11-20T15:08:40Z.
- `gh api repos/colbymchenry/codegraph/compare/v1.6.4...main`: status `identical`, so the default branch has no commits after the release.
- `gh api repos/colbymchenry/codegraph/releases/tags/v1.6.2`: published 2026-10-03T06:41:20Z (the version in use here).

## How to run here

- **Clone**: `git clone --depth 1 --branch v1.6.4 https://github.com/colbymchenry/codegraph $EXTERNAL/codegraph`, read-only. Reading the clone shows what the tool does; running it needs the installed CLI.
- **Telemetry** (`TELEMETRY.md`, `src/telemetry/index.ts`): on by default, anonymous daily totals (command and tool names, counts, language names, coarse file-count and duration buckets, agent name and version, a random machine id) POSTed to `https://telemetry.getcodegraph.com/v1/events`; "Never any code, paths, file or symbol names, queries, or IP addresses". The Claude Code prompt hook counts only its gate decision; "the prompt itself is never read, stored, or sent". Off switches: `codegraph telemetry off` (stored, deletes unsent data), `CODEGRAPH_TELEMETRY=0`, `DO_NOT_TRACK=1`, or `--no-telemetry` in one MCP server's arguments. "Off means off: when disabled, CodeGraph records nothing, opens no connection to the telemetry endpoint".
- **Update check**: the MCP server checks the latest GitHub release in the background, "at most once a day", fetching a version number only. Off: `CODEGRAPH_NO_UPDATE_CHECK=1` or `DO_NOT_TRACK=1`.
- **Other outbound calls found** (search for `https://` and `fetch(` across `src/`): `codegraph upgrade` downloads release bundles from GitHub; the interactive installer offers a beta waitlist at the end and, only on a yes plus a typed email, POSTs it to `https://getcodegraph.com/api/waitlist` (never under `--yes`, asked once per machine); the interactive installer offers `npm install -g @colbymchenry/codegraph` (default yes). The browser viewer makes no outbound connections and serves only on `localhost`. Other `fetch(` matches in `src/resolution/` and `src/ui-server/api/` are code that recognises HTTP calls inside the indexed code, not network calls.
- **Install paths to avoid without the user's yes**: the one-liners `curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh` and `irm …/install.ps1 | iex` (they download the latest bundle to `~/.codegraph/versions/<version>` and link `~/.local/bin/codegraph`); `npx @colbymchenry/codegraph` (downloads and runs the installer at once); `codegraph install` at the global location, and `codegraph install --yes`, whose defaults are "--location=global --target=auto, auto-allow on" and which turns the prompt hook on.
- **What the installer writes, by location** (`src/installer/index.ts`, `src/installer/targets/claude.ts`): it asks for agents (detected from 18 harnesses), the PATH install, "Apply agent configs to all your projects, or just this one?" (default: all projects), auto-allow, telemetry (default on, asked once), the prompt hook (default yes, Claude Code only), then the beta waitlist. For Claude Code:
  - global (user scope, every project): MCP entry in `~/.claude.json` with `"alwaysLoad": true`; permission `mcp__codegraph__*` and the `UserPromptSubmit` hook `codegraph prompt-hook` in `~/.claude/settings.json`; a marker-fenced block (`<!-- CODEGRAPH_START -->` … `<!-- CODEGRAPH_END -->`) in `~/.claude/CLAUDE.md`. `CLAUDE_CONFIG_DIR` moves all three.
  - local (project scope): the same three in `./.mcp.json`, `./.claude/settings.json` and `./.claude/CLAUDE.md` of the current folder.
  - `codegraph install --print-config claude --location=local` prints the MCP snippet for `./.mcp.json` and writes no file.
  - Other agents get their own config files (README "Supported Agents"); Windsurf, DeepSeek Harness and the Copilot CLI are global only.
- **Uninstall paths**: `codegraph uninstall` removes the MCP entry, permissions, prompt hook and instructions block from every configured agent at one location and, at the global location, the CLI itself unless `--keep-cli`; `npm uninstall -g @colbymchenry/codegraph` runs a `preuninstall` script that does the same for the global location only. Project indexes stay until `codegraph uninit`.
- **Why not user-wide here** (the reason behind the rejected global install, retold): the MCP server and its prompt hook cost about 2.5k tokens per message, so connected user-wide they would inflate every session, including sessions that never touch code. The kit's public playbook (`docs/llm-wiki-portable-playbook.md`, section "Graph tooling") gives the same rule: install it "per project, locally, never globally" and turn telemetry off.

## Parts

Kind `cli`: a part is a command. Read from the README "CLI Reference" and the command definitions in `src/bin/codegraph.ts`; the installer, prompt hook, MCP server, telemetry and update check also in their source. The CLI has 27 commands, three of them hidden (`serve`, `prompt-hook`, and `ui` unless `CODEGRAPH_UI=1`); the card splits `install` by location and adds the library API as one more entry point.

### `install`

- Wires the MCP server into the chosen agents; does not index any code. Options: `--target`, `--location global|local`, `--yes`, `--init`, `--no-permissions`, `--print-config <id>`, `--refresh` (run by `upgrade`).
- Global location: writes user-scope files that load in every project (see How to run here). Rejected here, reason above.
- Local location: writes the project's `./.mcp.json`, `./.claude/settings.json` and `./.claude/CLAUDE.md`; the prompt hook and auto-allow are separate yes/no questions (`--no-permissions` skips auto-allow). `--print-config` writes nothing.
- Needs: the installed CLI; the interactive run may call npm and the beta waitlist endpoint.

### `uninstall`

- Removes CodeGraph's MCP entry, permissions, prompt hook and instructions block from each configured agent at one location, and the CLI unless `--keep-cli`; shows what it finds before deleting; `--target`, `--yes`.
- Needs: the installed CLI.

### `init [path]`

- "Initialize CodeGraph in a project directory and build the initial index": creates `.codegraph/` and builds the graph in one step. `--local-only` keeps `.codegraph/` out of git ("its .gitignore ignores itself too"); `--force` is needed for a home folder or filesystem root; `--yes` takes defaults.
- Needs: the installed CLI; writes `.codegraph/` into the project.

### `uninit [path]`

- "Remove CodeGraph from a project (deletes .codegraph/ directory)"; `--force` skips the prompt.

### `index [path]`

- "Rebuild the full index from scratch (same result as a fresh init)"; `--quiet`, `--force`. Needed after an upgrade when the index was built by an older version.

### `sync [path]`

- "Sync changes since last index"; incremental. The MCP server's watcher normally does this on its own.

### `status [path]`

- "Show index status and statistics"; `--json`, `--strict`; warns when an index was built by an older version or a run did not finish.

### `unlock [path]`

- "Remove a stale lock file that is blocking indexing".

### `query <search>`

- "Search for symbols in the codebase"; `--kind`, `--limit`, `--json`.

### `explore <query>`

- Relevant symbols' verbatim source and call paths in one shot, "same output as the codegraph_explore MCP tool". The instructions block the installer writes points subagents and agents without MCP at this command.

### `context <task>`

- "Build context for a task: relevant symbols, relationships, and code blocks"; `--format markdown|json`.

### `node [name]`

- One symbol's source and caller/callee trail, or a file with line numbers and dependents; same output as the `codegraph_node` MCP tool.

### `files`

- "Show project file structure from the index"; `--format tree|flat|grouped|package`, `--filter`, `--max-depth`, `--json`.

### `callers <symbol>` and `callees <symbol>` (two parts)

- `callers`: "Find all functions/methods that call a specific symbol". `callees`: "Find all functions/methods called by a specific symbol". Both: `--path`, `--file`, `--limit` (default 20), `--json`.

### `impact <symbol>`

- "Analyze what code is affected by changing a symbol"; `--depth`, `--json`.

### `implementations <symbol>`

- "List the types that implement or extend a trait, interface or class"; `--depth`, `--json`.

### `affected [files...]`

- "Find test files affected by changed source files": follows imports transitively (`--depth`, default 5); `--stdin` takes `git diff --name-only`; `--filter` sets what counts as a test; `--cross-tier` also follows HTTP calls, queues and events across a process boundary.

### `cycles [path]`

- "List circular imports between files (exits 1 when there are any)".

### `daemon`

- Lists running background daemons and stops the one picked (alias `daemons`). One detached daemon per project root serves every MCP client of that project and lingers 300s after the last client leaves (`src/mcp/daemon.ts`, `CODEGRAPH_DAEMON_IDLE_TIMEOUT_MS`).

### `telemetry [on|off|status]`

- Shows or changes the telemetry choice; `status` shows the state, what decided it and the machine id, stored in `~/.codegraph/telemetry.json`. Used here once: `codegraph telemetry off`.

### `upgrade [version]`

- Updates to the latest release or a pinned one; detects how it was installed (bundle, npm or npx); `--check` only reports; `--force`. Downloads from GitHub. Runs `install --refresh` for agents already configured.

### `version` and `help` (two parts)

- `version` prints the installed version (also `-v`, `--version`); `help [command]` shows help.

### `serve --mcp` (MCP server, hidden command)

- "Start CodeGraph as an MCP server for AI assistants" over stdio; the config entry the installer writes is `"command": "codegraph", "args": ["serve", "--mcp"]`. Options: `--path`, `--no-watch`, `--no-telemetry`.
- Exposes one tool by default, `codegraph_explore`; seven more tools, `codegraph_node`, `codegraph_search`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files` and `codegraph_status` are unlisted unless named in `CODEGRAPH_MCP_TOOLS`. `projectPath` queries another indexed project; a path with no index returns guidance to use built-in tools.
- Sends usage instructions in the MCP `initialize` response (`src/mcp/server-instructions.ts`, 11353 bytes in this version), which the client puts into the agent's system prompt every session; the file's own comment: "The agent reads this every session — long instructions burn tokens."
- Watches the project and syncs after changes; starts or joins the per-project daemon.
- In use here at 1.6.2, connected per repository only (see How this kit uses it).

### `prompt-hook` (Claude Code `UserPromptSubmit` hook, hidden command)

- Written by `install` into Claude Code's `settings.json` when the user accepts "Front-load CodeGraph on “how / where / trace” prompts?" (default yes). Reads `{prompt, cwd}` JSON on stdin on every prompt; for a structural prompt (a structural keyword or a code token found in the index) it runs `codegraph_explore` and prints the result, which Claude Code adds to the context, capped at 9,000 characters (`PROMPT_HOOK_INJECTION_MAX`); for prose words matching indexed symbol names it injects a short list of symbols; otherwise it prints nothing. Every failure exits 0 with no output.
- Kill switch without uninstalling: `CODEGRAPH_NO_PROMPT_HOOK=1` (or `CODEGRAPH_PROMPT_HOOK=0`).
- Since 1.6.4 it asks the running daemon first instead of opening the index on every prompt.
- Needs: Claude Code, an indexed project, the CLI on PATH.

### `ui [path]` (browser viewer, hidden command)

- Opens a browser viewer of the indexed project as a graph (alias `web`); listed only when `CODEGRAPH_UI=1`. `--port`, `--no-open`, `--read-only`. Serves on `localhost` only and makes no outbound connections (`TELEMETRY.md`, "The browser viewer sends nothing").

### Library API (`CodeGraph` class)

- The npm package re-exports a programmatic API (`CodeGraph.init`, `indexAll`, `searchNodes`, `getCallers`, `buildContext`, `getImpactRadius`, `watch`); README "Library Usage". Needs `npm i @colbymchenry/codegraph` and "Node 22.5+" for `node:sqlite`, because it runs on the caller's runtime.

## Rejection, retold

- `install` at the global location (and `install --yes`, which defaults to it) is rejected: the MCP server and the prompt hook it wires user-wide cost about 2.5k tokens per message and would inflate every session. Revisit only if a release makes the server's per-session instructions and the hook much smaller, measured in a one-repository sandbox.

## How this kit uses it

Facts retold from the kit owner's notes; the use record is `raw/notes/trials/2026-11-21-codegraph-per-repo-mcp.md`.

- In use at version 1.6.2, installed from npm.
- Telemetry switched off with `codegraph telemetry off`.
- Connected per repository only: a local MCP config in one tooling repository. Never connected globally: its MCP server and hook cost about 2.5k tokens per message and would inflate every session.
- Not recorded: which command built that repository's index, how its MCP config was written, and whether the prompt hook is wired there.

## Cost of this desk check

Written in one agent run together with the other 2 desk checks, the cards and the use records of the same batch: 82 model calls on opus, $5.71 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
