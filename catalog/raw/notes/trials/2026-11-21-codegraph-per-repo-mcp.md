---
title: "Use record: codegraph MCP server, per-repository code navigation"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-21
ingested: 2026-11-21
repo: colbymchenry/codegraph
part: "serve --mcp; telemetry"
version: "1.6.2"
status: in use
tags: [catalog, trial, use-record, kind-cli, codegraph, mcp]
summary: "colbymchenry/codegraph 1.6.2, installed from npm, is in real use: its MCP server is connected per repository only, through a local MCP config in one tooling repository, never globally, and telemetry is switched off with `codegraph telemetry off`. Reason for never connecting it globally: its MCP server and hook cost about 2.5k tokens per message. Recorded 2026-11-21; start date and per-task cost not recorded."
---

# Use record: codegraph MCP server, per-repository code navigation

- **Tool and parts**: colbymchenry/codegraph, parts `serve --mcp` (the MCP server) and `telemetry`.
- **Version**: 1.6.2, installed from npm. The desk check of 2026-11-21 read 1.6.4, the latest release; the installed version was not upgraded by that desk check.
- **Task, by kind**: code navigation for a coding agent in one tooling repository.
- **How it is connected**: per repository only, through a local MCP config in one tooling repository. Never connected globally (user-wide).
- **Telemetry**: switched off with `codegraph telemetry off`.
- **Why never globally**: its MCP server and hook cost about 2.5k tokens per message, so connected user-wide they would inflate every session, including sessions that never touch code.
- **Not recorded**: which command built that repository's index, how its MCP config was written (`codegraph install --location=local` or by hand), and whether the prompt hook is wired in that repository.
- **Dates**: recorded 2026-11-21; the date the use began is not recorded.
- **Kind of record**: real use, not a sandbox trial. Status after it: `in use` for `serve --mcp` and `telemetry`; `rejected` for `install` at the global location.

## Result

- In real use in the one repository where it is connected; sessions elsewhere do not load it. No measured result per task is recorded.

## Cost

Not measured per task. The owner's estimate of the standing cost: about 2.5k tokens per message for the MCP server and hook, which is why they are connected in one repository only.
