---
title: "Parts list: Xcode 27.2 MCP tools (xcrun mcpbridge)"
source: "https://developer.apple.com/xcode/"
type: data
ingested: 2026-11-25
tags: [catalog, parts-list]
summary: "54 MCP tools that Xcode 27.2 (build 27B52) serves through xcrun mcpbridge, server xcode-tools version 25464, read with an MCP tools/list call."
authors: [Apple]
source_date: 2026-11-25
url: https://developer.apple.com/xcode/
version: "27.2"
---

# Parts list: Xcode 27.2 MCP tools

Read on 2026-11-25 with an MCP `tools/list` call through `xcrun mcpbridge` from Xcode 27.2 (build 27B52); server `xcode-tools`, version `25464`. 54 tools; their definitions together are about 151795 characters of JSON. Description: the first sentence of the tool's own description. Required: the tool's required arguments.

| Part | Kind | Description | Required |
|------|------|-------------|----------|
| `AddEntitlement` | MCP tool | Add a new entitlement to the project's entitlements file. | targetName, entitlementKey, entitlementValueType |
| `AddInfoPlist` | MCP tool | Add or update an Info.plist key in the project. | targetName, infoPlistKey, infoPlistValueType |
| `BuildProject` | MCP tool | Builds an Xcode project and waits until the build completes. | none |
| `DeviceInteractionEndSession` | MCP tool | Closes previous device session created in DeviceInteractionStartSession or DeviceInteractionStartWorkspaceSession. | interactionSessionKey |
| `DeviceInteractionInstallAndRun` | MCP tool | Builds, installs, and starts the current application on the currently targeted device. | interactionSessionKey |
| `DeviceInteractionStartSession` | MCP tool | Prepares a runtime for device interaction WITHOUT a workspace. | deviceIdentifier, sessionIdentifier |
| `DeviceInteractionStartWorkspaceSession` | MCP tool | Prepares a runtime for device interaction WITH a workspace. | sessionIdentifier |
| `DeviceInteractionSynthesize` | MCP tool | Synthesizes device events (tap, swipe, type, etc.) on a physical device or simulator and captures the resulting state. | interactSessionKey |
| `DocumentationSearch` | MCP tool | Searches Apple Developer Documentation using semantic matching. | query |
| `GetBuildLog` | MCP tool | Gets the log of the current or most recently finished build. | none |
| `GetConsoleOutput` | MCP tool | Retrieves console output (stdout, stderr, OSLog) from a running or completed app launch session. | none |
| `GetCrashIssueLogs` | MCP tool | Get detailed crash logs, expert triage knowledge, and actionable recommendations for a specific crash signature. | signature_name |
| `GetFieldPerformanceIssueLogs` | MCP tool | Get detailed logs, performance data, expert triage knowledge, and actionable recommendations for specific field performance issue. | app_version, signature_name, diagnostic_type |
| `GetFileCompilerFlags` | MCP tool | Gets the additional per-file compiler flags for a single source file in a specific Xcode target — the same value shown in the Compiler Flags column of Target > Build Phases > Compile Sources. | targetName, filePath |
| `GetTargetBuildSettings` | MCP tool | Get all the Xcode build setting for a specified Xcode project target. | targetName |
| `GetTestList` | MCP tool | Gets all available tests from the active scheme's active test plan. | none |
| `GetTopCrashIssues` | MCP tool | Retrieve the top crash signatures for an app from Apple's crash reporting service. | none |
| `GetTopFieldPerformanceIssues` | MCP tool | Analyze app performance and identify performance regressions across different diagnostic types. | diagnostic_type |
| `InvokeDebuggerCommand` | MCP tool | Sends an lldb command to Xcode's active debugging session and returns the output. | command |
| `LocalizationPlanner` | MCP tool | Ensures the project is in a state where translations can be added. | targetLocaleIdentifier |
| `RenderPreview` | MCP tool | Builds and renders a Preview and waits until a snapshot of the resulting UI is available. | sourceFilePath |
| `RunAllTests` | MCP tool | Runs all tests from the active scheme's active test plan | none |
| `RunCodeSnippet` | MCP tool | Builds and runs a snippet of code in the context of a specific file and waits until results are available. | codeSnippet, sourceFilePath, purpose |
| `RunProject` | MCP tool | Builds and runs the current scheme in Xcode, equivalent to pressing the Run button (Cmd+R). | none |
| `RunSomeTests` | MCP tool | Runs specific tests using the active scheme's active test plan | tests |
| `StopProject` | MCP tool | Stops the currently running app in Xcode, equivalent to pressing the Stop button (Cmd+.). | none |
| `StringCatalogContext` | MCP tool | Returns context and the source language value for a given string in the String Catalog. | filePath, stringKey, targetLocaleIdentifier |
| `StringCatalogEdit` | MCP tool | Inserts a translation for a given locale into a String Catalog. | filePath, stringKey, targetLocaleIdentifier |
| `StringCatalogRead` | MCP tool | Returns string keys grouped by translation state for the requested locale. | filePath, targetLocaleIdentifier |
| `UpdateFileCompilerFlags` | MCP tool | Updates, appends or deletes the additional per-file compiler flags for a single source file in a specific Xcode target — the same value shown in the Compiler Flags column of Target > Build Phases > Co… | targetName, filePath |
| `UpdateTargetBuildSetting` | MCP tool | Updates, appends or deletes the named build setting for the specified Xcode project target. | targetName, buildSettingName |
| `XcodeCloseWorkspace` | MCP tool | Closes a workspace that was opened with XcodeOpenWorkspace, identified by its workspace identifier. | workspaceIdentifier |
| `XcodeGlob` | MCP tool | Finds files in the Xcode project structure matching wildcard patterns. | none |
| `XcodeGrep` | MCP tool | Searches for text patterns in files within the Xcode project structure using regex. | pattern |
| `XcodeLS` | MCP tool | Lists files and directories in the Xcode project structure at the specified path. | path |
| `XcodeListRunDestinations` | MCP tool | Lists run destinations available for the currently active scheme, grouped the same way the Xcode picker groups them (Devices, Simulators, Build, Incompatible, etc.), and identifies which one is active… | none |
| `XcodeListSchemes` | MCP tool | Lists all schemes available in the current Xcode workspace and identifies which one is currently active. | none |
| `XcodeListTargets` | MCP tool | Lists targets in the current Xcode workspace, optionally scoped to a single project. | none |
| `XcodeListTemplates` | MCP tool | Lists Xcode templates available in this Xcode install. | none |
| `XcodeListTestPlans` | MCP tool | Lists the test plans associated with the currently active scheme and identifies which one is active. | none |
| `XcodeListWorkspaces` | MCP tool | Lists the workspaces currently open in Xcode, with the identifier and path of each. | none |
| `XcodeMV` | MCP tool | Moves or renames files and directories in the project navigator with support for filesystem operations. | sourcePath, destinationPath |
| `XcodeMakeDir` | MCP tool | Creates directories in the Xcode project structure. | directoryPath |
| `XcodeNewProject` | MCP tool | Creates a new Xcode project from a template. | templateIdentifier, productName, destinationPath |
| `XcodeNewTarget` | MCP tool | Adds a new target to a project in the current Xcode workspace using a target template. | templateIdentifier, productName |
| `XcodeOpenWorkspace` | MCP tool | Opens an Xcode workspace or project at the given path and returns its workspace identifier, which other tools can use to target it. | path |
| `XcodeRM` | MCP tool | Removes files and directories from the Xcode project structure and optionally deletes the underlying files from the filesystem. | path |
| `XcodeRead` | MCP tool | Reads the contents of a file within the Xcode project organization. | filePath |
| `XcodeRefreshCodeIssuesInFile` | MCP tool | Retrieves current compiler diagnostics (errors, warnings, notes) for a file in the Xcode project. | filePath |
| `XcodeSwitchRunDestination` | MCP tool | Changes the active run destination for the currently active scheme. | displayTitle |
| `XcodeSwitchScheme` | MCP tool | Changes the active scheme in the current Xcode workspace to the specified scheme. | schemeName |
| `XcodeSwitchTestPlan` | MCP tool | Changes the active test plan for the currently active scheme. | testPlanName |
| `XcodeUpdate` | MCP tool | Edits files in the Xcode project by replacing text content. | filePath, oldString, newString |
| `XcodeWrite` | MCP tool | Creates or overwrites files with content in the Xcode project. | filePath, content |
