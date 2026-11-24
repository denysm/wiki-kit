---
title: "Trial and use record: Xcode 27.2 agent tools — MCP bridge on a throwaway package, Apple skills in a coding agent, xctrace on a floating panel with a web view"
source: session
type: notes
authors: ["kit owner", "Claude Code"]
source_date: 2026-11-25
ingested: 2026-11-25
url: https://developer.apple.com/xcode/
part: mcpbridge, run-agent skills export, xctrace
version: "27.2"
status: tried
tags: [catalog, trial, use-record, kind-app, xcode, mcp, agent-skills, xctrace, instruments, swift, appkit, webkit]
summary: "Xcode 27.2 on an Apple M4 Mac mini: the MCP bridge answered in 0.8 s with 54 tools; after one approval in Xcode it opened a throwaway Swift package, searched Apple's documentation and built it in 1.363 s. With the owner's yes, 5 of the 11 Apple skills went into a project and the bridge was registered with Claude Code. xctrace Time Profiler on a floating panel with a bundled web page, replaying a fictional session: app process 0.1% CPU on average, 10.0% at most, no hangs over 20.82 s."
---

# Trial and use record: Xcode 27.2 agent tools

- **Tool and parts**: Xcode 27.2 (build 27B52): `xcrun mcpbridge`, `mcpbridge run-agent skills export`, the bundled `xctrace` skill with `xcrun xctrace`.
- **Machine**: Apple M4 Mac mini, macOS 27, used over Screen Sharing; Xcode already open.
- **Kind of record**: a sandbox trial of the bridge (throwaway package in a temporary folder), then real use with the owner's yes (skills and bridge registered; xctrace on a real app).

## 1. MCP bridge on a throwaway package (sandbox)

A small Python MCP client spoke JSON-RPC to `xcrun mcpbridge` over stdin and stdout.

| Step | Result |
|---|---|
| `initialize` | answered in 0.8 s (0.1 s on later runs); server `xcode-tools` `25464` |
| `tools/list` | 54 tools |
| `DocumentationSearch` before any approval | refused: "This agent isn't approved to use Xcode's tools yet. Call XcodeOpenWorkspace or XcodeNewProject first" |
| `XcodeOpenWorkspace` with the path of `Package.swift` | Xcode showed an approval request once; the owner allowed it. The call still failed: "Files of type 'Swift Source' cannot be opened outside of a workspace." |
| `XcodeOpenWorkspace` with the package folder | opened; scheme of the package, run destination `My Mac` |
| `DocumentationSearch` (AppKit, ScreenCaptureKit) for excluding a window from screen capture | returned the `SCWindow` article and a section of Apple's screen capture sample, full text |
| `BuildProject` | "The project built successfully." in 1.363 s, an empty `errors` list and a log path |
| `XcodeCloseWorkspace` | closed |

- `mcp-server status` afterwards listed the permitted agent as the client's own executable (here the Python interpreter, unsigned) and the permitted folder as the package folder only, both with an expiry later the same day. A different client (Claude Code) is a different agent and is asked again.
- Opening the package made Xcode write a `.swiftpm/` folder into it: a repository opened this way needs `.swiftpm/` in its `.gitignore`.

## 2. Skills and bridge for a coding agent (real use, owner's yes)

- The agent's attempt to install the skills and register the bridge itself was stopped by Claude Code's safety classifier (an agent changing its own configuration); the owner ran the commands.
- Exported all 11 skills to a cache folder; copied 5 (`xctrace`, `swiftui-specialist`, `audit-xcode-security-settings`, `modernize-tests`, `adopt-c-bounds-safety`) into one project's `.claude/skills/`, ignored by git. They appeared in the running Claude Code session without a restart.
- `claude mcp add -s local xcode -- xcrun mcpbridge`: `claude mcp get xcode` reported it connected.

## 3. xctrace on a floating panel with a web view (real use)

The `xctrace` skill was loaded and its overview reference read first, as the skill asks. Target: a native macOS assistant window (a non-activating `NSPanel` holding a `WKWebView` with a bundled page) replaying a fictional session log at 4× speed. `DevToolsSecurity -status` first said "Developer mode is currently disabled."; the owner enabled it before recording.

| Recording | Result |
|---|---|
| Time Profiler, attached to the app, 20 s | trace duration 20.82 s; app process CPU 0.1% on average, 10.0% at most; hangs triage: "No Data"; resident memory about 71 MB at the end |
| Time Profiler, all processes, 15 s | app 0.2%; its WebKit helpers: WebContent 0.2%, GPU 0.2%, Networking 0.1% (averages) |

- The page is drawn by WebKit helper processes, so a recording attached to the app alone misses part of a web view's cost; the all-processes recording shows it.
- WindowServer averaged 41.8% in the all-processes recording while the machine was being viewed over Screen Sharing; no recording without the panel was made, so this is not attributed to the panel.
- Measuring latency inside a live audio path needs `os_signpost` intervals in the app's code; this trial did not add any.

## Cost

No outside cost: local tools only, inside an interactive Claude Code session.
