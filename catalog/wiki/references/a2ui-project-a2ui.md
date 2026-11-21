---
title: "a2ui-project/a2ui"
category: reference
kind: library
areas: [building-interfaces-for-agents, writing-code-with-agents]
repo: a2ui-project/a2ui
version: "cli-v0.4.0"
licence: Apache-2.0
desk_checked: 2026-11-21
sources:
  - raw/repos/a2ui-project-a2ui-desk-check-2026-11-21.md
  - raw/data/a2ui-project-a2ui-parts-cli-v0.4.0.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-building-interfaces-for-agents, area-writing-code-with-agents, kind-library, a2ui, generative-ui, agent-ui, react, angular, lit, flutter, swiftui, agent-sdk]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "A2UI: a protocol in which an agent streams UI as data and the app renders it with its own native components, with renderers for React, Angular, Lit, Flutter and SwiftUI, agent SDKs in Python, TypeScript and Dart, a CLI, a conformance suite and an eval. Read at tag cli-v0.4.0 from a clone; nothing tried yet. The libraries call no model; samples, Composer and the eval call Gemini or other hosted models and need a key."
---

# a2ui-project/a2ui

> A generative UI framework (kind `library`, licence Apache-2.0, version `cli-v0.4.0` read): the A2UI protocol, in which an agent sends UI as data, not code, and the app renders it with its own native components from a catalog; renderers for React, Angular, Lit, Flutter and SwiftUI; agent SDKs in Python, TypeScript and Dart; a CLI, a conformance suite, an eval and samples. The repository versions the protocol, the catalogs and each package family separately; the tag read is the CLI release. Read from a clone; nothing installed.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Let an agent show its results as real UI (forms, cards, lists) rendered with the app's own components, without sending code | `specification/v1_0` | building-interfaces-for-agents |
| Render agent-generated UI in a React app | `@a2ui/react` | building-interfaces-for-agents |
| Render agent-generated UI in an Angular app or with web components | `@a2ui/angular`, `@a2ui/lit` | building-interfaces-for-agents |
| Render agent-generated UI in a Flutter app, replacing the discontinued `genui` packages | `a2ui_flutter` | building-interfaces-for-agents |
| Render agent-generated UI natively on iOS or macOS | `A2UISwiftUI` | building-interfaces-for-agents |
| Make a Python agent emit UI: negotiate catalogs, put the catalog in the prompt, parse and validate the model's output | `a2ui-agent-sdk` | building-interfaces-for-agents |
| Do the same in a TypeScript or Node agent | `@a2ui/agent` | building-interfaces-for-agents |
| Serve that UI from an agent over A2A or inside ADK | `a2ui-a2a`, `a2ui-adk` | building-interfaces-for-agents |
| Spend fewer model tokens on UI output with a compact format | Inference formats | building-interfaces-for-agents |
| Define which components and functions an agent may use, and check that catalog file | `catalogs/`, `a2ui lint` | building-interfaces-for-agents |
| Generate typed Python builders from a catalog | `a2ui codegen` | building-interfaces-for-agents |
| Check that a renderer or SDK in a new language behaves like the others | `conformance/` | building-interfaces-for-agents |
| Write a renderer or SDK for a framework not covered yet | `a2ui-implement-new-sdks-for-client-language` | building-interfaces-for-agents |
| Move an app to a newer protocol version or off Flutter `genui` | `a2ui-migration` | building-interfaces-for-agents |
| Score how well a model writes UI payloads | `eval/` | building-interfaces-for-agents |
| See a working agent and client end to end | `samples/agent`, `samples/client` | building-interfaces-for-agents |
| Draft a widget's JSON with a visual editor | `tools/composer` | building-interfaces-for-agents |
| Keep a coding agent from writing A2UI code from memory | `a2ui` skill | building-interfaces-for-agents |
| Keep SDKs in several languages in step with one language-agnostic spec | `blueprints/` | writing-code-with-agents |
| Route a coding agent to the right instruction file per task in a multi-language repo | `AGENTS.md` | writing-code-with-agents |
| Turn reviewer feedback into review rules loaded by language | `coding-principles` | writing-code-with-agents |
| Tune a prompt format with a benchmark loop that keeps or reverts each change | `inference-format-optimizer` | writing-code-with-agents |

## Run it here

- **Clone**: `git clone --depth 1 --branch cli-v0.4.0 https://github.com/a2ui-project/a2ui $EXTERNAL/a2ui`, read-only. Never edit the clone.
- **Version**: tag `cli-v0.4.0`, the latest release, published 2026-11-17; the same commit is `v0.11.0+swift`. Package versions in it: `@a2ui/web_core` `0.15.0`, `@a2ui/react` `0.15.0`, `@a2ui/lit` `0.15.0`, `@a2ui/angular` `0.14.0`, `@a2ui/agent` `0.1.0`, `a2ui_core` `0.8.0`, `a2ui_flutter` `0.4.0`, `a2ui_agent` `0.4.0`, `a2ui_cli` `0.4.0`; the Python packages take theirs from git tags, and three of their release tags point to a commit 11 minutes later. `main` was pushed after the tag (2026-11-21). Compare with upstream before relying on this card: `gh api repos/a2ui-project/a2ui/releases/latest --jq .tag_name`.
- **Read first**: `$EXTERNAL/a2ui/skills/a2ui/SKILL.md`, then `specification/v1_0/docs/a2ui_protocol.md`, then the README of the renderer or SDK for the target framework.
- **Switch off**: nothing in the libraries (no telemetry found; they call no model). The samples, Composer, the eval and the Express tools call hosted models: the Node sample runs without a key with `STUB_LLM=true`; the eval runs on a local model with `--no-judge`. The bundled eval datasets are encrypted and need the project's shared password.
- **Do not install**: the npm, pub or PyPI packages, or the CLI through its `curl ... | sh` script, which installs from `main`. Do not run `blueprints/link_skills.sh`: it writes symlinks into the clone. A real install waits for the user's yes.

## What's inside

Parts: the protocol specification by version, inference formats, catalogs, the renderers and core libraries, the agent SDKs, two CLI commands, the conformance suite, the eval, samples, tools, blueprints, `AGENTS.md`, and 23 skills, of which 22 are marked internal and written for contributors to this repository. Skills not shown below are `listed` in the generated [parts list](../../raw/data/a2ui-project-a2ui-parts-cli-v0.4.0.md).

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `specification/v1_0` | The current protocol: four agent-to-renderer messages (`createSurface`, `updateComponents`, `updateDataModel`, `deleteSurface`), typed function calls both ways, catalogs, data binding, transport bindings for AG-UI, A2A and MCP; JSON schemas. | candidate | Nothing; Markdown and JSON Schema. | Read before designing the first agent screen that should be UI instead of text. |
| `specification/v0_9_1` | Previous version, "a patch release of v0.9". | listed | Nothing. | Read only when an app or SDK still speaks v0.9.1. |
| `specification/v0_9` | Previous version, close to v0.9.1. | listed | Nothing. | Read only when an app or SDK still speaks v0.9. |
| `specification/v0_8` | Deprecated version, "not supported by the latest SDKs"; still behind legacy renderer entry points. | listed | Nothing. | Read only when migrating an app off v0.8. |
| Inference formats | Express, a compact syntax compiled to v1.0 messages (grammar `Express.g4`); Atom and Elemental proposals, experimental in Python only. | candidate | Nothing to read; the proposal tools need a Gemini key and `A2UI_EXPRESS_ENABLED=true`. | Try Express when UI payloads cost too many output tokens. |
| `catalogs/` | Component and function catalogs (basic, MCP, VegaChart) that limit what an agent may send and that renderers validate against; versioned apart from the protocol. | candidate | Nothing; JSON Schema. | Try the basic catalog as the first allowed set of components. |
| `@a2ui/web_core` | Shared web core: message validation, reactive state, data binding, `MessageProcessor`. | candidate | Node and Yarn to build. | Try it with the first web renderer. |
| `@a2ui/react` | React renderer for v0.9, v0.9.1 and v1.0 surfaces; v0.8 at a legacy entry point. | candidate | A React app, `@a2ui/web_core`. | Try it when a React app needs agent UI. |
| `@a2ui/angular` | Angular renderer with Signals and catalogs. | candidate | An Angular app, `@a2ui/web_core`. | Try it when an Angular app needs agent UI. |
| `@a2ui/lit` | Lit web components renderer with a basic catalog. | candidate | A web page, `@a2ui/web_core`. | Try it for agent UI in a page without a framework. |
| `@a2ui/markdown-it` | Markdown for the web renderers, sanitized with DOMPurify. | candidate | A browser window (jsdom in tests). | Check when a renderer shows agent Markdown. |
| TypeScript catalog packages | `@a2ui/catalog-mcp` (MCP tool results as UI) and `@a2ui/catalog-vegachart` (charts, "Not published yet"). | listed | Node. | Read when MCP tool results or charts must show as agent UI. |
| `a2ui_core` (Dart) | Dart core for v0.9, v0.9.1 and v1.0; no v0.8. | candidate | Dart SDK. | Try it with `a2ui_flutter`. |
| `a2ui_flutter` | Flutter renderer for v1.0 and v0.9; with `a2ui_core` and `a2ui_agent` it replaces `genui`. | candidate | Flutter SDK. | Try it when a Flutter app needs agent UI. |
| Swift core | `A2UISwiftCore` and `BasicCatalog`: state engine and message processor, released under `v0.11.0+swift`. | candidate | Swift toolchain. | Try it with `A2UISwiftUI`. |
| `A2UISwiftUI` | SwiftUI renderer "on iOS and iPadOS 17+ and macOS 14+", marked alpha. | candidate | Xcode and Swift. | Try it when an Apple app needs agent UI. |
| Jetpack Compose renderer | Not in this repository; the skill points to Android's own page, marked alpha. | listed | Not in the clone. | Read when an Android app needs agent UI. |
| `a2ui-core` (Python) | Python data models, state and validation, v0.9 and later. | candidate | A venv. | Try it with `a2ui-agent-sdk`. |
| `a2ui-agent-sdk` | Agent SDK: "negotiates catalogs, generates prompts and skills, and compiles model output into A2UI"; calls no model itself. | candidate | A venv; the agent's own model. | Try it when a Python agent should answer with UI. |
| `a2ui-a2a` | Connects the agent SDK to the A2A protocol. | candidate | A venv, `a2a-sdk`. | Try it when the agent is served over A2A. |
| `a2ui-adk` | Connects the agent SDK to ADK. | candidate | A venv, `google-adk`. | Try it when the agent is built with ADK. |
| `a2ui-catalog-mcp` (Python) | A placeholder package with no implementation yet. | listed | Nothing. | Read when it ships an implementation. |
| `@a2ui/agent` | TypeScript agent SDK, "early 0.x": v0.9 and v1.0, Direct JSON and Express; gaps in `KNOWN_GAPS.md`. | candidate | Node. | Try it when a Node agent should answer with UI; read the gaps first. |
| `a2ui_agent` (Dart) | Dart agent SDK for v0.9 and v1.0, Express by default. | candidate | Dart SDK. | Try it when a Flutter app calls the model itself. |
| Kotlin legacy agent SDK | "Legacy Kotlin agent SDK". | listed | JDK and Gradle. | Read only when a Kotlin agent already uses it. |
| `a2ui codegen` | Generates typed component code from a catalog; Python is the only emitter. | candidate | Release binary, or the Dart SDK to run it from the clone. | Try it when a custom catalog needs Python builders. |
| `a2ui lint` | Checks catalog JSON against protocol rules for 0.9, 0.9.1 and 1.0; `--fatal-warnings` for CI. | candidate | As `a2ui codegen`. | Try it on the first custom catalog. |
| `conformance/` | Language-agnostic YAML test cases for core, agent and extension behaviour across SDKs. | candidate | A harness in the language under test. | Try it when writing or changing a renderer or SDK. |
| `eval/` | Inspect AI eval: schema validation, deterministic assertions, an LLM judge. | candidate | uv, a model (hosted with a key, or local); the dataset password for the bundled datasets. | Try it with an own dataset when choosing a model or format for UI output. |
| `samples/agent` | Restaurant finder agents (ADK with A2A, Node), a custom components example, a v0.8 to v0.9 payload converter. | candidate | uv or Yarn; a Gemini key, or the Node stub mode. | Try the Node agent with `STUB_LLM=true` to see the flow without a key. |
| `samples/client` | Angular, Flutter, Lit and React shells rendering the restaurant finder's surfaces. | candidate | Node or Flutter. | Try one with the sample agent. |
| `samples/vegachart` | A dashboard from a static payload with the VegaChart catalog; no agent. | candidate | Node. | Try it to see charts as agent UI without a model. |
| `samples/community` | Unmaintained community samples. | listed | Node, uv. | Read only for an integration no maintained sample shows. |
| `tools/composer` | Visual editor that drafts widget JSON with a model. | candidate | A Gemini or OpenAI key; or the hosted copy, which sends prompts out. | Try it when writing few-shot examples for an agent's prompt. |
| `tools/build_catalog` | Merges several catalogs into one freestanding JSON Schema; may fetch external refs. | candidate | Python; network for remote refs. | Try it when combining the basic catalog with custom components. |
| `blueprints/` | Language-agnostic module and feature specs; each codebase records its compliance by git commit hash; five SDD skills. | reference | Nothing to read. | Consult when several codebases in different languages must follow one spec. |
| `AGENTS.md` | One instruction file that routes a coding agent to a skill per kind of task, with version rules and repository conventions. | reference | Nothing. | Consult when writing agent instructions for a multi-language repo. |
| `a2ui` skill | User guide: when to use A2UI, "do not write A2UI code from memory", current package names, a minimal React render. | candidate | Nothing; read from the clone. | Try it as the first read before any A2UI code. |
| `a2ui-migration` | Routes a migration (protocol version, SDK release, Flutter `genui`) to a case guide or a generic procedure. | candidate | Nothing; read from the clone. | Try it on the first upgrade of an A2UI app. |
| `a2ui-implement-new-sdks-for-client-language` | Phases for building a core SDK, framework adapter or agent SDK in a new language. | candidate | Nothing; read from the clone. | Try it when a needed framework has no renderer. |
| `coding-principles` | Review rules "distilled from human reviewer feedback", loaded cross-language first, then by language. | reference | Nothing. | Consult when turning review comments into a reusable review skill. |
| `inference-format-optimizer` | Benchmark loop: change, test, measure, keep only if accuracy holds and output tokens grow by no more than 5%, else revert. | reference | Nothing to read; running it needs this repository's eval. | Consult when tuning a prompt or output format against a benchmark. |

## Tried

None yet: nothing here has been installed or run; every part was read from the clone or taken from its metadata.

## Verdict

No part is tried yet. The protocol, the renderers for five frameworks, the Python and TypeScript agent SDKs, the CLI and the conformance suite are candidates for the first task where an agent should answer with UI instead of text; nothing in the libraries calls a model or sends telemetry, while the samples, Composer and the eval need a hosted model key unless run with a stub or a local model. The blueprints, `AGENTS.md` and two internal skills are kept as references for coding-agent practice. Revisit when the freshness check shows a release after `cli-v0.4.0`, when a task needs agent UI on a given framework, or when a Jetpack Compose renderer appears in the repository.

## See Also

- [[area-building-interfaces-for-agents|Building interfaces for agents]] ([Building interfaces for agents](../topics/area-building-interfaces-for-agents.md)): area page; the protocol, renderers, agent SDKs, CLI and conformance suite
- [[area-writing-code-with-agents|Writing code with agents]] ([Writing code with agents](../topics/area-writing-code-with-agents.md)): area page; blueprints, `AGENTS.md`, review rules, the format optimizer loop
- [[github-spec-kit|github/spec-kit]] ([github/spec-kit](../references/github-spec-kit.md)): another take on specs that drive code written by agents, beside `blueprints/`

## Sources

- [Desk check: a2ui-project/a2ui cli-v0.4.0](../../raw/repos/a2ui-project-a2ui-desk-check-2026-11-21.md): every part read from the clone, version lines per package family, what calls hosted models, freshness through the GitHub API.
- [Parts list: a2ui-project/a2ui cli-v0.4.0](../../raw/data/a2ui-project-a2ui-parts-cli-v0.4.0.md): the 23 skills, generated from their own frontmatter.
