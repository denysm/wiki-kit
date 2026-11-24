---
title: "Xcode agent tools (mcpbridge, Apple skills, xctrace)"
category: reference
kind: app
areas: [writing-code-with-agents]
url: https://developer.apple.com/xcode/
version: "27.2"
licence: Apple Xcode and SDK licence (proprietary)
desk_checked: 2026-11-25
sources:
  - raw/repos/apple-xcode-agent-tools-desk-check-2026-11-25.md
  - raw/data/apple-xcode-agent-tools-mcp-tools-27.2.md
  - raw/notes/trials/2026-11-25-apple-xcode-agent-tools-bridge-and-xctrace.md
created: 2026-11-25
updated: 2026-11-25
tags: [catalog, card, area-writing-code-with-agents, kind-app, xcode, mcp, agent-skills, xctrace, instruments, apple, macos, swift]
confidence: medium
volatility: warm
verified: 2026-11-25
summary: "What Xcode 27.2 offers an outside coding agent such as Claude Code: an MCP bridge with 54 tools (open, build, test, run, debug, Apple documentation search), 11 Apple-written skills to export, and xctrace for profiling. Bridge tried on a throwaway package; xctrace skill in use; the editor itself is not needed."
---

# Xcode agent tools (`mcpbridge`, Apple skills, `xctrace`)

> Agent-facing parts of Xcode (kind `app`, Apple's proprietary licence, version `27.2`, build `27B52`): `xcrun mcpbridge` lets any MCP client drive a running Xcode, `mcpbridge run-agent skills export` writes 11 skills written by Apple, and `xctrace` is Instruments from the command line. Useful to an agent working on Swift code in another editor; the Xcode window is only the tool server.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Look up current Apple platform APIs that are newer than the model's training | `DocumentationSearch` | writing-code-with-agents |
| Build a Swift package or Xcode project from an agent and get errors as fields, not log text | `BuildProject` | writing-code-with-agents |
| Find out why a macOS app uses CPU or hangs, from an agent | `xctrace` skill | writing-code-with-agents |
| Give a coding agent Apple's own guidance for SwiftUI, tests and build hardening | `run-agent skills export` | writing-code-with-agents |
| Not this: work without Xcode installed. Every part ships inside Xcode, and the bridge needs Xcode running or its headless mode | `mcpbridge` | writing-code-with-agents |

## Run it here

- **Nothing to install** beyond Xcode itself. `xcode-select` must point at Xcode (`sudo xcode-select -s`), otherwise `xcrun` does not find `mcpbridge`. Read first: `xcrun mcpbridge --help`, then `xcrun mcp-server --help`.
- **Approvals**: the first tool call from a new client is refused until Xcode shows an approval request and the user allows it; the approval names the client's executable and one folder and expires the same day in the trial.
- **Sends outward**: the crash and field-performance tools read Apple's services; whether documentation search goes online was not checked. Nothing to switch off for the build, documentation and file tools.
- **`xctrace`**: recording asks for a password while developer mode is off (`DevToolsSecurity`); enabling it is the user's step.
- **Do not install** the skills or the bridge for every project at once: the 54 tool definitions are about 38 thousand tokens if a client loads them all, and the 11 skill descriptions about 9281 characters. Pick the skills a project needs; real installation waits for the user's yes.
- **In use**: `run-agent skills export` (27.2) exports to a cache folder, chosen skills are copied into one project's `.claude/skills/`, ignored by git, and re-exported after Xcode updates; the `xctrace` skill (27.2) is read before any `xcrun xctrace` command.

## What's inside

All 54 MCP tools are in [the parts list](../../raw/data/apple-xcode-agent-tools-mcp-tools-27.2.md); the tools not in this table are `listed`.

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `mcpbridge` | Stdio bridge from an MCP client to Xcode's tool service; server `xcode-tools` `25464`, 54 tools. | tried | Xcode running (or headless mode), one approval | The real task: build and test a real Swift package through it from Claude Code. |
| `XcodeOpenWorkspace` | Opens a project or package folder and returns its workspace id; asks for the approval. | tried | A folder path (not `Package.swift`) | The real task: open a real package; it adds `.swiftpm/`, so ignore that folder first. |
| `DocumentationSearch` | Semantic search over Apple's developer documentation, full article text. | tried | An approved agent | The real task: answer a platform API question during real work. |
| `BuildProject` | Builds and returns the result, errors as a list and a log path. | tried | An open workspace | The real task: replace a shell build in an agent's loop. |
| `XcodeCloseWorkspace` | Closes a workspace opened by the bridge. | tried | Its workspace id | The real task: close after real work. |
| `mcp-server` | Headless mode, approvals, folder permissions, status and logs. | listed | `sudo` for most commands | Read when Xcode must serve the tools with no window, or to revoke an approval. |
| `lldb-mcp` | LLDB debugger over MCP. | listed | Xcode | Read when an agent must debug a hang or crash. |
| `run-agent` | Launches a coding agent with Xcode's configuration. | listed | The agent's binary on the path | Read when an agent should run with Xcode's own setup instead of its usual one. |
| `run-agent skills export` | Writes the bundled skills to a folder. | in use | Nothing | Re-check after each Xcode update: re-export and compare the list. |
| `run-agent plugin path` | Writes out Xcode's packaged agent plugin content. | listed | Nothing | Read when choosing between the skills and the whole plugin. |
| `xctrace` skill | Apple's guide to `xctrace`: recording, `toc`, `list tracks`, `show`, hang triage. | in use | Developer mode for recording | Re-check that its commands match `xctrace help` after an Xcode update. |
| `swiftui-specialist` skill | SwiftUI practice and performance. | candidate | Nothing | Try it on the next SwiftUI view an agent writes. |
| `audit-xcode-security-settings` skill | Warnings, analyzer checks and hardening settings. | candidate | An Xcode project or package | Try it on a package before its first signed release. |
| `modernize-tests` skill | Moves tests to Swift Testing. | candidate | Nothing | Try it on an XCTest suite. |
| `adopt-c-bounds-safety` skill | The C `-fbounds-safety` extension. | candidate | C code | Try it on vendored C code. |
| `swiftui-whats-new-27` skill | SwiftUI changes in the 2027 OS releases. | listed | Nothing | Read when a SwiftUI build breaks after an SDK update. |
| `app-resizability` skill | Resizable windows and several windows. | listed | Nothing | Read when a window's layout must follow its size. |
| `app-intents-specialist` skill | App Intents practice. | listed | Nothing | Read when an app exposes actions to Shortcuts or Siri. |
| `app-intents-whats-new-27` skill | App Intents changes in the 2026 releases. | listed | Nothing | Read with `app-intents-specialist`. |
| `building-document-based-swiftui-applications` skill | Document-based SwiftUI apps. | listed | Nothing | Read when building a document-based app. |
| `device-interaction` skill | Checks an app on a device or simulator. | listed | A device or simulator | Read when an iOS app needs checking from an agent. |

## Tried

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|
| 2026-11-25 | Open a throwaway Swift package through the IDE's MCP bridge, search the platform documentation, build it | `mcpbridge`: `XcodeOpenWorkspace`, `DocumentationSearch`, `BuildProject`, `XcodeCloseWorkspace` | Opened after one approval; full documentation articles; built in 1.363 s | No outside cost | [trial record](../../raw/notes/trials/2026-11-25-apple-xcode-agent-tools-bridge-and-xctrace.md) |
| 2026-11-25 | Give a coding agent the platform vendor's skills in one project | `run-agent skills export` | 5 of the 11 Apple skills copied; loaded without a restart | No outside cost | [trial record](../../raw/notes/trials/2026-11-25-apple-xcode-agent-tools-bridge-and-xctrace.md) |
| 2026-11-25 | Profile a floating panel with a web view while it replays a session | `xctrace` skill | App process 0.1% CPU on average, 10.0% at most, no hangs over 20.82 s; WebContent 0.2%, GPU 0.2%, Networking 0.1% | No outside cost | [trial record](../../raw/notes/trials/2026-11-25-apple-xcode-agent-tools-bridge-and-xctrace.md) |

## Verdict

Xcode is worth having as a tool server and a source of Apple's own guidance, while the agent and the editor stay elsewhere. Documentation search and structured builds are the main gain for code that targets the newest macOS. The `xctrace` skill made a first profile straightforward. Revisit after the first real build through the bridge and after each Xcode update.

## See Also

- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page

## Sources

- [Desk check: Xcode 27.2 agent tools](../../raw/repos/apple-xcode-agent-tools-desk-check-2026-11-25.md): commands, MCP server, skills, outward calls.
- [Parts list: Xcode 27.2 MCP tools](../../raw/data/apple-xcode-agent-tools-mcp-tools-27.2.md): all 54 tools.
- [Trial and use record: Xcode 27.2 agent tools](../../raw/notes/trials/2026-11-25-apple-xcode-agent-tools-bridge-and-xctrace.md): bridge, skills, xctrace numbers.
