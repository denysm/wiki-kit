---
title: "Desk check: Xcode 27.2 agent tools — mcpbridge, mcp-server, lldb-mcp, run-agent skills"
source: https://developer.apple.com/xcode/
type: repos
authors: ["Apple"]
source_date: 2026-11-25
ingested: 2026-11-25
url: https://developer.apple.com/xcode/
kind: app
version: "27.2"
licence: Apple Xcode and SDK licence (proprietary)
tags: [catalog, desk-check, kind-app, xcode, mcp, agent-skills, xctrace, apple, macos]
summary: "Xcode 27.2 (build 27B52) read on 2026-11-25 from its own help output: xcrun mcpbridge (stdio MCP bridge, 54 tools, server xcode-tools 25464), mcp-server (headless mode, approvals, status), lldb-mcp, and run-agent (launch an agent, export 11 Apple-written skills, plugin content). Part of the Xcode app; nothing extra to install."
---

# Desk check: Xcode 27.2 agent tools

Read on 2026-11-25 on macOS 27 with Xcode 27.2 (`xcodebuild -version`: `Xcode 27.2`, `Build version 27B52`) from the tools' own help output, an MCP `tools/list` call and an export of the bundled skills. No Apple web page was read for this check.

## Commands in `Xcode.app/Contents/Developer/usr/bin`

| Command | What its help says | Notes |
|---|---|---|
| `mcpbridge` | "STDIO Bridge for Xcode MCP Tools". Without a subcommand it bridges an MCP client to "Xcode's MCP tool service". Environment: `MCP_XCODE_PID` (which Xcode to use), `MCP_XCODE_SESSION_ID`. | Run as `xcrun mcpbridge`; `xcrun` finds it only when `xcode-select` points at Xcode, not at the Command Line Tools. |
| `mcpbridge run-agent` | "Launch a coding agent with Xcode-provided configuration". Subcommands `skills` ("Inspect and export Xcode-provided skills") and `plugin` ("Work with Xcode's packaged agent plugin content"); flags `--dry-run`, `--no-xcode-tools`. | `agent` in the same folder is a shell script that runs `mcpbridge run-agent`. `--dry-run claude` failed here: "Could not find 'claude' binary". |
| `run-agent skills export` | "Export skill definitions to disk"; `--output-dir <path>`, `--replace-existing`. | Exported 11 skills, see below. |
| `run-agent plugin path` | "Materialize Xcode's plugin content and print its path". | Not run. |
| `mcp-server` | "Xcode MCP server launcher". Commands: `open`, `stop`, `enable` ("Turn headless mode on (requires sudo)"), `disable`, `approve`, `allow-folder`, `clear-permissions`, `reset-all`, `deny`, `status`, `show-logs`. | `status` printed `Permission: enabled` and `mcp-server: not running` before first use. |
| `lldb-mcp` | Printed no help with `-h`. | Not explored. |

## MCP tools

An MCP `initialize` answered with server `xcode-tools`, version `25464`, instructions "Request Xcode perform the action you specify." `tools/list` returned 54 tools; their definitions together are about 151795 characters of JSON (about 38 thousand tokens if loaded at once). The full list is in [the parts list](../data/apple-xcode-agent-tools-mcp-tools-27.2.md). Groups: workspace and files (`XcodeOpenWorkspace`, `XcodeRead`, `XcodeUpdate`, `XcodeGrep` and others), build and diagnostics (`BuildProject`, `GetBuildLog`, `XcodeRefreshCodeIssuesInFile`), tests (`RunAllTests`, `RunSomeTests`, `GetTestList`), run and debug (`RunProject`, `GetConsoleOutput`, `InvokeDebuggerCommand`, `RunCodeSnippet`), previews and devices (`RenderPreview`, `DeviceInteraction*`), documentation (`DocumentationSearch`), project settings (`AddEntitlement`, `AddInfoPlist`, build settings), string catalogs, and crash and performance reports from Apple's services.

## Bundled skills (`run-agent skills export`)

| Skill | Description length (characters) | What it covers |
|---|---|---|
| `adopt-c-bounds-safety` | 226 | the C `-fbounds-safety` extension |
| `app-intents-specialist` | 2540 | App Intents practice |
| `app-intents-whats-new-27` | 2127 | App Intents changes in the 2026 releases |
| `app-resizability` | 595 | resizable windows and several windows |
| `audit-xcode-security-settings` | 539 | compiler warnings, analyzer checks and hardening settings |
| `building-document-based-swiftui-applications` | 791 | document-based SwiftUI apps |
| `device-interaction` | 99 | checking an app on a device or simulator |
| `modernize-tests` | 85 | moving tests to Swift Testing |
| `swiftui-specialist` | 914 | SwiftUI practice and performance |
| `swiftui-whats-new-27` | 911 | SwiftUI changes in the 2027 OS releases |
| `xctrace` | 454 | Instruments from the command line |

All 11 descriptions together are about 9281 characters. Each skill says it was written and published by Apple. The export is about 892K on disk.

## Sends outward

Not checked by traffic. By their descriptions, `GetTopCrashIssues`, `GetCrashIssueLogs`, `GetTopFieldPerformanceIssues` and `GetFieldPerformanceIssueLogs` read Apple's crash reporting and performance services; whether `DocumentationSearch` answers from a local index or online was not checked.
