---
title: "Desk check: a2ui-project/a2ui cli-v0.4.0"
source: https://github.com/a2ui-project/a2ui/tree/cli-v0.4.0
type: repos
authors: ["A2UI project contributors (a2ui-project); file headers: Google LLC"]
source_date: 2026-11-17
ingested: 2026-11-21
repo: a2ui-project/a2ui
kind: library
version: "cli-v0.4.0"
licence: Apache-2.0
tags: [catalog, desk-check, kind-library, a2ui, generative-ui, agent-ui, renderers, protocol, agent-sdk]
summary: "a2ui-project/a2ui read at tag cli-v0.4.0 from a read-only clone: the A2UI protocol specification (v1.0 current, v0.9.1, v0.9, v0.8 deprecated), inference formats, catalogs, the web, Flutter and SwiftUI renderers, the Python, TypeScript, Dart and legacy Kotlin agent SDKs, the CLI (codegen, lint), the conformance suite, the eval, samples, tools, blueprints, AGENTS.md and the 23 skills; separate version lines per package family; what calls hosted models and needs an API key."
---

# Desk check: a2ui-project/a2ui cli-v0.4.0

Read from a shallow clone of tag `cli-v0.4.0` (commit `07735d6a654ae3ba25951a8753ddd57b344b1169`, committed 2026-11-17), at `$EXTERNAL/a2ui`. The same commit also carries the tag `v0.11.0+swift`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: cli-v0.4.0.

## Repository facts

- README: A2UI (Agent-to-User Interface) "is an open-source generative UI framework, complete with a protocol optimized for streaming dynamic user interfaces at low latency, native renderers for web and mobile frameworks, and agent SDKs in several popular languages." The agent sends UI as data, not code: a schema for the data exchanged between agent and renderer limits what the agent can do, and the app renders the result with its own native components from a catalog.
- README, architecture in three layers: Inference (a model, instructed through an agent SDK, writes the UI description in an inference format), Transport (the agent SDK parses and validates the output and converts it to A2UI Transport protocol messages), Rendering (a core library, a framework adapter and a widget catalog).
- README, when to use it: parts of the app are agent- or server-driven; the same agent streams UI to several platforms; the agent is remote, third-party or across a trust boundary and must not send executable code.
- `LICENSE`: the Apache License, Version 2.0, full text, followed by two third-party copyright lines. README, "Contribute": "A2UI is an **Apache 2.0** licensed project." Every package manifest read (`package.json`, `pyproject.toml` of `a2ui-a2a`, `a2ui-adk` and `a2ui-catalog-mcp`) says `Apache-2.0`.
- Kind: `library`. The repository is a protocol specification plus libraries that an app or agent imports (renderers, core libraries, agent SDKs); the CLI is a developer tool beside them. It is not a skill collection: of its 23 skills, 22 are marked internal and written for contributors to this repository.
- Top-level folders that hold parts: `specification/`, `catalogs/`, `typescript/`, `python/`, `dart/`, `swift/`, `kotlin/`, `conformance/`, `eval/`, `samples/`, `tools/`, `blueprints/`, `skills/`, `.agents/skills/`, and `AGENTS.md`. Other folders: `docs/` (the a2ui.org site source and contributor docs), `scripts/` (release and install scripts), `.gemini/` and `.vscode/` (editor and assistant settings).
- `kotlin/` holds only the legacy agent SDK; there is no Kotlin or Jetpack Compose renderer in the clone.

### How the repository versions its parts

The repository versions the protocol, the catalogs and each package separately; one tag does not cover everything.

- Protocol: `specification/versions.json` lists v1.0 `current`, v0.9.1 `previous`, v0.9 `previous`, v0.8 `deprecated`. AGENTS.md: v1.0 is the "Current protocol version" ("previously known as v0.10"); v0.9.1 is "a patch release of v0.9"; v0.8 is "not supported by the latest SDKs".
- Catalogs: `catalogs/README.md`: "Catalogs are versioned independently of the A2UI protocol."
- Release tags by family (from `gh api .../tags`): `cli-v*` for the Dart CLI, `v*+swift` for the Swift packages, `python/<package>/v*` for each Python package; tags `v0.8` and `v0.9` also exist. The npm and pub packages carry their versions in their manifests; no tags of their own were found.
- Versions in the clone at `cli-v0.4.0`:
  - CLI `a2ui_cli` 0.4.0 (`pubspec.yaml`); the Swift packages are released under `v0.11.0+swift`, the same commit.
  - npm: `@a2ui/web_core` 0.15.0, `@a2ui/react` 0.15.0, `@a2ui/lit` 0.15.0, `@a2ui/angular` 0.14.0, `@a2ui/markdown-it` 0.2.2, `@a2ui/agent` 0.1.0, `@a2ui/catalog-mcp` 0.0.3, `@a2ui/catalog-vegachart` 0.1.0.
  - pub: `a2ui_core` 0.8.0, `a2ui_agent` 0.4.0, `a2ui_flutter` 0.4.0.
  - Python: versions come from git tags (`source = "vcs"`); the fallback versions in `pyproject.toml` are `a2ui-core` 0.7.0, `a2ui-agent-sdk` 0.12.0, `a2ui-a2a` 0.4.0, `a2ui-adk` 0.3.0; `a2ui-catalog-mcp` 0.1.0 is set directly.
  - Kotlin legacy agent SDK: `version = "0.1.0"` in `build.gradle.kts`.
- The Python release tags `python/a2ui-core/v0.7.0`, `python/a2ui-agent-sdk/v0.12.0` and `python/a2ui-a2a/v0.4.0` point to commit `d63fd4306da7` (2026-11-17T18:41:43Z), 11 minutes after the clone's commit; `python/a2ui-adk/v0.3.0` points to `3295e67b5f48` (2026-11-10T22:06:37Z). The Python sources in the clone were not compared with those tags file by file.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/a2ui-project/a2ui`: `pushed_at` 2026-11-21T02:34:00Z; licence `Apache-2.0`; default branch `main`; not archived; created 2025-09-24T23:14:02Z; description "Open-source generative UI framework: agents stream layout data, and apps render it with native components in React, Angular, Lit, Flutter, SwiftUI and Jetpack Compose."
- `gh api repos/a2ui-project/a2ui/releases/latest`: tag `cli-v0.4.0`, "A2UI CLI v0.4.0", published 2026-11-17T21:20:06Z. Releases of the same day: `v0.11.0+swift` (2026-11-17T19:14:50Z), `python/a2ui-core/v0.7.0`, `python/a2ui-agent-sdk/v0.12.0`, `python/a2ui-a2a/v0.4.0` (2026-11-17T19:18:31Z to 19:18:37Z).
- Licence as GitHub reports it (`Apache-2.0`) matches the licence file.
- `main` was pushed after the tag read (2026-11-21); the changes since the tag were not read.
- CLI release notes of `cli-v0.4.0`: "**Breaking:** Requires `a2ui_core` `^0.8.0`".

## How to run here

- **Clone**: `git clone --depth 1 --branch cli-v0.4.0 https://github.com/a2ui-project/a2ui $EXTERNAL/a2ui`, read-only.
- **Read first**: `skills/a2ui/SKILL.md` (the short user-facing guide, current package names), then `specification/v1_0/docs/a2ui_protocol.md`, then the README of the renderer or SDK for the target framework.
- **Telemetry**: none found. Searched `.ts`, `.tsx`, `.py`, `.dart`, `.swift`, `.mjs`, `.astro`, `.yaml` and `.toml` files outside `node_modules` for telemetry, analytics, `gtag(`, googletagmanager, posthog and sentry; only test fixtures and a mock MCP server in the explorer apps matched.
- **Libraries do not call models**: the Python SDK sources import no model client (`openai`, `anthropic`, `litellm`, `httpx`, `requests`, `aiohttp`); `a2ui-adk` imports `google.genai` types for ADK events and `google.adk`. The TypeScript core, renderers and agent SDK import no model client; the one `fetch(` found is in a doc comment of the React v0.8 provider.
- **What calls hosted models or services, and what needs an API key** (samples, tools and eval, not the libraries):
  - ADK restaurant finder sample: Gemini through ADK, `GEMINI_API_KEY` in `.env` (optional Vertex AI with `GOOGLE_GENAI_USE_VERTEXAI`); default model "gemini-3.6-flash", changed with `MODEL_NAME` or `LITELLM_MODEL`; serves A2A on `localhost` port 10002.
  - Node restaurant finder sample: "calls Gemini through `@google/genai`"; `STUB_LLM=true` serves canned responses without an API key.
  - Composer (`tools/composer/`): needs `GOOGLE_GENERATIVE_AI_API_KEY` (or `GEMINI_API_KEY`) or `OPENAI_API_KEY`; a hosted copy runs at https://a2ui-editor.ag-ui.com.
  - Eval: Gemini by default (`GEMINI_API_KEY`), also as the LLM judge; other providers by Inspect AI model name: OpenAI (`OPENAI_API_KEY`), Anthropic (`ANTHROPIC_API_KEY`), OpenRouter (`OPENROUTER_API_KEY`), a local Ollama or vLLM server (no key), any OpenAI-compatible server. `--no-judge` turns the judge off; README example: `uv run main.py --model ollama/gemma4:e4b --strategies express --no-judge`.
  - Express proposal tools (`specification/proposals/express/`): "By default, the testing and evaluation tools are designed to run using remote Gemini models"; gated behind `A2UI_EXPRESS_ENABLED`.
  - `tools/build_catalog/assemble_catalog.py`: "natively supports external HTTP refs, automatic GitHub version resolution for official catalogs", so it may fetch catalogs over the network.
  - Hosted services named in the README: a2ui.org, A2UI Composer (a2ui-project.github.io/composer), A2UI Theater (a2ui-composer.ag-ui.com/theater). `context7.json` registers the repository with the Context7 documentation index; nothing in the clone runs it.
- **Eval datasets are encrypted**: `file` reports "openssl enc'd data with salted password, base64 encoded" for the three `eval/datasets/*.yaml`; the eval README decrypts them with Transcrypt and "the shared password". They cannot be read from the clone.
- **Do not install or run**: the npm, pub and PyPI packages; the CLI install script (`curl -fsSL https://raw.githubusercontent.com/a2ui-project/a2ui/main/scripts/public/install_cli.sh | sh`, which installs from `main`, not the tag read); `blueprints/link_skills.sh` (it writes symlinks into `.agents/skills/` of the clone). `.gemini/GEMINI.md` imports `AGENTS.md` for Gemini tools opened in the clone; it does nothing otherwise. A real install waits for the user's yes.
- **Skills without a plugin**: all 23 are plain `SKILL.md` files read from the clone; there is no plugin manifest and no hook. They use repository-relative paths and are written for working inside this repository.

## Parts

### Specification v1.0 (`specification/v1_0/`)

- `versions.json`: `current`. `README.md`: "This version was previously known as version 0.10." and "This specification is stable." Protocol document: "**Status:** Current", "**Created:** Nov 20, 2025", "**Last Updated:** Jun 8, 2026".
- The agent-to-renderer protocol has four message types: `createSurface`, `updateComponents`, `updateDataModel`, `deleteSurface`. v1.0 adds typed function calls in both directions (`callRendererFunction`, `callAgentFunction`, `rendererFunctionResponse`, `agentFunctionResponse`), lets one `createSurface` carry the whole component tree and data model, and drops theme properties: "A v1.0 `createSurface` that carries `theme` is invalid." Transport bindings described: AG-UI, A2A and MCP.
- Files: `docs/a2ui_protocol.md` (1694 lines), `docs/a2ui_custom_functions.md`, `docs/evolution_guide.md` (v0.9 to v1.0), `docs/sdks_spec.md`; 12 JSON schemas in `json/`; the A2A extension in `extensions/a2a/`.
- Needs: nothing; Markdown and JSON Schema.

### Specification v0.9.1 (`specification/v0_9_1/`)

- `previous`; "a patch release of v0.9". Docs: protocol, extension specification, custom functions, basic catalog implementation guide, evolution guide, SDK spec; schemas and a bundled basic catalog. Known from `versions.json`, AGENTS.md and the file list; not read further.

### Specification v0.9 (`specification/v0_9/`)

- `previous`; "very minor differences from v0.9.1" (AGENTS.md). Same document set as v0.9.1. Not read further.

### Specification v0.8 (`specification/v0_8/`)

- `deprecated`, "not supported by the latest SDKs". Still served by the legacy entry points `@a2ui/react/v0_8` and `@a2ui/angular/v0_8`; the Lit README: "We strongly discourage starting new projects with v0.8." Not read further.

### Inference formats (`specification/inference_formats/express/Express.g4`, `specification/proposals/{express,atom,elemental}/`)

- Express: "a compact, token-efficient declarative syntax"; a host-side compiler turns it into v1.0 wire payloads; ANTLR grammar `Express.g4`. Implemented in the Python, TypeScript and Dart agent SDKs (the default format in the Dart SDK).
- Atom: S-expressions, claiming "a **25% to 50% token footprint reduction** compared to A2UI Express and Elemental" (a claim of the proposal, not checked). Elemental: HTML-like markup with Web Components. Both are experimental in the Python SDK and unimplemented in the TypeScript SDK (`KNOWN_GAPS.md`).
- Needs: nothing to read; the proposal tools need Python, `A2UI_EXPRESS_ENABLED=true` and a Gemini key.

### Catalogs (`catalogs/`)

- `basic/v1/` (catalog, examples, implementation guide), `mcp/v1/` (catalog, examples, MCP app specification), `vegachart/` (`v0_9`, `v1`). A catalog "declares the components and functions an agent may reference in A2UI messages, and is what renderers validate against."
- Needs: nothing; JSON Schema.

### `@a2ui/web_core` 0.15.0 (`typescript/core/web_core/`)

- Framework-agnostic core shared by the web renderers and `@a2ui/agent`: protocol message validation for all supported versions, reactive state with `@preact/signals-core`, data binding and expressions, catalogs, Zod schema generation; entry point `MessageProcessor`.
- Needs: Node and Yarn to build; nothing to read.

### `@a2ui/react` 0.15.0 (`typescript/renderers/react/`)

- "Renders A2UI v0.9, v0.9.1 and v1.0 surfaces from the same package"; the legacy v0.8 renderer is `@a2ui/react/v0_8`. Component props typed from Zod schemas; multiple surfaces.
- Needs: a React app, `@a2ui/web_core`.

### `@a2ui/angular` 0.14.0 (`typescript/renderers/angular/`)

- Angular Signals for updates, A2UI component types mapped to Angular components through catalogs, callback-based action handling; `@a2ui/angular/v0_8` for v0.8.
- Needs: an Angular app, `@a2ui/web_core`.

### `@a2ui/lit` 0.15.0 (`typescript/renderers/lit/`)

- Lit web components renderer with a basic catalog included; custom components typed from Zod schemas; v1.0 from the package root.
- Needs: a web page or app, `@a2ui/web_core`.

### `@a2ui/markdown-it` 0.2.2 (`typescript/renderers/markdown-it/`)

- Markdown rendering with markdown-it and DOMPurify, shared by the web renderers; "requires a Window object" (jsdom in Node tests).

### TypeScript catalog packages (`typescript/catalogs/`)

- `@a2ui/catalog-mcp` 0.0.3: "calls MCP tools and renders A2UI messages returned in tool results and UI resources." `@a2ui/catalog-vegachart` 0.1.0: Vega and Vega-Lite charts, "Not published yet". Known from the README table; not read further.

### `a2ui_core` (Dart) 0.8.0 (`dart/a2ui_core/`)

- Framework-agnostic Dart SDK for protocols v0.9, v0.9.1 and v1.0: envelopes, catalogs, function evaluation, reactive state, validation, RPC for v1.0 function calls. "Legacy v0.8 payloads are not supported by the runtime processor."

### `a2ui_flutter` 0.4.0 (`dart/a2ui_flutter/`)

- Renders surfaces as Flutter widgets; "supports protocol v1.0 and v0.9" with the basic catalog. With `a2ui_core` and `a2ui_agent` it replaces the `genui` package. The `skills/a2ui` guide: "Do **not** use `flutter_genui` or `genui_a2ui`: both are discontinued."
- Needs: Flutter SDK.

### Swift core (`swift/core/`: `A2UISwiftCore`, `BasicCatalog`)

- Framework-agnostic state engine, message processor, JSON pointer resolver and catalog registries; SPM targets in the root `Package.swift` (`swift-tools-version: 6.1`). Released under tag `v0.11.0+swift`.

### SwiftUI renderer (`swift/swiftui/`: `A2UISwiftUI`, `BasicCatalogSwiftUI`)

- Native SwiftUI rendering "on iOS and iPadOS 17+ and macOS 14+". The `skills/a2ui` install table marks it "SwiftUI (alpha)".
- Needs: Xcode and Swift.

### Jetpack Compose renderer (not in this repository)

- Named in the GitHub description and in the `skills/a2ui` install table as "Jetpack Compose (alpha)", pointing to developer.android.com/develop/ui/compose/agentic. No Compose code is in the clone.

### `a2ui-core` (Python) (`python/a2ui_core/`)

- Data models, reactive state, JSON Schema validation for v0.9 and later ("does not support legacy v0.8"). Dependencies: babel, jsonschema, pydantic, referencing, regex.
- Needs: a Python venv.

### `a2ui-agent-sdk` (Python) (`python/a2ui_agent/`)

- README table: "negotiates catalogs, generates prompts and skills, and compiles model output into A2UI." `A2uiGenerator` is "the main entry point"; `A2uiRequestProcessor` binds the catalogs negotiated for a request to an inference format and exposes prompt generation and response parsing. Formats: Direct JSON, Express, experimental Elemental and Atom; Direct JSON and Express stream. Dependencies: `a2ui-core`, `antlr4-python3-runtime`, jsonschema, pydantic, pyyaml. The SDK calls no model itself; the agent sends the prompt to its own model.
- Needs: a Python venv; a model of the user's choice in the agent around it.

### `a2ui-a2a` (Python) (`python/a2ui_a2a/`)

- Connects the agent SDK to the Agent-to-Agent (A2A) protocol (`a2ui.a2a`); depends on `a2a-sdk`.

### `a2ui-adk` (Python) (`python/a2ui_adk/`)

- Connects the agent SDK to the Agent Development Kit (ADK) (`a2ui.adk`); depends on `google-adk` and `google-genai`; extra `a2a` for A2A converters.

### `a2ui-catalog-mcp` (Python) (`python/catalogs/mcp/`)

- "This package is a placeholder that reserves the name and workspace slot. It does not ship an implementation yet." Nothing to try, so it stays `listed`.

### `@a2ui/agent` 0.1.0 (TypeScript) (`typescript/agents/a2ui_agent/`)

- Agent SDK for TypeScript and Node.js: v0.9 and v1.0 (`KNOWN_GAPS.md` adds v0.9.1), Direct JSON and Express with streaming; the skill calls it "early 0.x". `KNOWN_GAPS.md`: Elemental and Atom unimplemented; Express number formatting as in Python needs Node 21 or later.

### `a2ui_agent` (Dart) 0.4.0 (`dart/a2ui_agent/`)

- "implements the whole API of the blueprint for A2UI protocols v0.9 and v1.0", with Express (the default) and direct JSON, read complete or streamed.

### Kotlin legacy agent SDK (`kotlin/agent_sdk_legacy/`)

- AGENTS.md: "Legacy Kotlin agent SDK". Gradle project, `version = "0.1.0"`. Not read beyond the build file.

### CLI command `a2ui codegen` (`dart/a2ui_cli/`, 0.4.0)

- "generates typesafe component code from a catalog"; the only emitter in `lib/src/emitters/` is `python`. The repository uses it to regenerate the Python SDK's basic catalog builders.
- Needs: prebuilt binaries from the release, or the Dart SDK to run `dart run dart/a2ui_cli/bin/a2ui.dart` from the clone.

### CLI command `a2ui lint` (`dart/a2ui_cli/`, 0.4.0)

- Checks catalog JSON files against protocol schema rules for versions `0.9`, `0.9.1` and `1.0` (structure, `$ref` targets, reserved names, UAX 31 identifiers in v1.0); `--fatal-warnings` for CI.
- Needs: as `codegen`.

### Conformance suite (`conformance/`)

- "a language-agnostic conformance suite" of YAML cases in `core/`, `agent/` and `extensions/`, with test data, for behavioural parity across the SDKs. Examples: `core/adapter_conformance.yaml` "Covers 13 v1.0 UI framework adapter cases"; `core/rpc_functions.yaml` "Covers 23" function-call cases; `agent/skill.yaml` covers generating skill documents from a format and its catalogs.
- Needs: a harness in the language under test (`conformance_harness_implementation_guide.md`).

### Eval (`eval/`)

- Built on Inspect AI; checks that a prompt or conversation produces a UI payload that follows the schema and the scenario's rules. Three stages: schema validation, deterministic assertions, an LLM judge. Datasets encrypted (see above). Models and keys: see How to run here.
- Needs: Python with uv, a model (hosted with a key, or local), the dataset password for the bundled datasets.

### Samples, agents (`samples/agent/adk/`, `samples/agent/node/`)

- ADK: `restaurant_finder` (ADK plus A2A server, the Quickstart sample), `custom-components-example`, `migrate_v08_to_v09.py` (a v0.8 to v0.9 payload converter). Node: `restaurant_finder` with `@a2ui/agent`, answering in the A2UI version the renderer asks for; `A2UI_FORMAT` picks Direct JSON or Express.
- Needs: Python with uv or Node with Yarn; a Gemini key, or the Node stub mode.

### Samples, clients (`samples/client/`)

- Angular, Flutter, Lit and React shells that render surfaces streamed from the restaurant finder agent over A2A, plus a shared MCP apps iframe. The samples README lists maintained samples by agent language and renderer.

### Sample, VegaChart (`samples/vegachart/`)

- Renders a dashboard from a static A2UI v0.9 JSON payload with the VegaChart catalog; no agent.

### Community samples (`samples/community/`)

- "This folder contains code that is not maintained." Depends on the published packages, not the workspace. Not read further.

### Composer (`tools/composer/`)

- "A tool for building A2UI widgets, powered by copilot kit": ask for a widget, copy the JSON into the agent's examples. Needs a model key (see above) and the shared web packages built first.

### Catalog builder (`tools/build_catalog/assemble_catalog.py`)

- Combines several component and function catalogs into one freestanding JSON Schema file; may fetch external refs.

### Blueprints (`blueprints/`)

- Spec-Driven Development: language-agnostic module blueprints (`modules/`: `a2ui_core`, `a2ui_agent`, `a2ui_framework_adapter`), feature blueprints (`features/`), and per-codebase files that "track their module compliance by git commit hash"; `validate_blueprints.py`; the five SDD skills, isolated by default. Its README tells agents to "IGNORE THIS ENTIRE `blueprints/` FOLDER" unless the user asks for blueprints or SDD.
- Status `reference`: read for the method of keeping several language codebases in step with one spec; the files themselves serve contributors to this repository.

### `AGENTS.md`

- "the authoritative guide for AI agents working within the A2UI repository": routes the agent to a skill file per kind of task (code, pull requests, changelogs, SDKs, migration, docs), states protocol version rules, the repository layout, Yarn workspace script targets, and core rules such as "Maintain Agent-Agnostic Instructions". `.gemini/GEMINI.md` imports it.
- Status `reference`: read for how one instruction file routes a coding agent to per-task skills in a multi-language repository; it is written for contributors to this repository.

### The 23 skills

23 `SKILL.md` files: 16 in `.agents/skills/`, 5 in `blueprints/skills/`, 1 in `eval/iterative_format_optimizer/skills/`, 1 in `skills/`. `skills_lint.yaml` lints these four folders (absolute paths and trailing whitespace are errors). 22 of them carry `metadata: internal: true`; only `skills/a2ui` is for users of A2UI. The full list with descriptions is the generated parts list. Status rule here: the three skills that serve a user's task are `candidate`; two internal skills read for their method are `reference` (reason: they are instructions for contributors to this repository and name its paths, so they are read only for ideas); the other 18 internal skills are `listed`, known from their frontmatter and headings.

### Skill: a2ui (`skills/a2ui/SKILL.md`)

- For users: when to use A2UI, "Critical: do not write A2UI code from memory" (read the installed package's README or a2ui.org/llms.txt; import from package roots; do not guess message or field names), current package names per platform, a minimal React render, integration paths (AG-UI or CopilotKit, A2A, MCP). Status `candidate`.

### Skill: a2ui-migration (`.agents/skills/a2ui-migration/SKILL.md`)

- Migrates an app, renderer, catalog or agent to a newer SDK or protocol version, "including from Flutter `genui`": identify language, source and target, then route to a case guide (Dart `genui` to `a2ui_core` + `a2ui_flutter`; v0.8 to v0.9; v0.9 to v0.9.1; v0.9 or v0.9.1 to v1.0; SDK release to a later one) or a generic procedure. Marked internal, but its cases are a user's task. Status `candidate`.

### Skill: a2ui-implement-new-sdks-for-client-language (`.agents/skills/a2ui-implement-new-sdks-for-client-language/SKILL.md`)

- Phased instructions for building a Core SDK, a framework adapter or an inference SDK in a new language or UI framework, starting from the blueprints, the v1.0 schemas and the basic catalog. Marked internal, but useful to anyone adding a renderer. Status `candidate`.

### Skill: coding-principles (`.agents/skills/coding-principles/SKILL.md`)

- Review and authoring rules "distilled from human reviewer feedback across A2UI pull requests", loaded in two levels: cross-language subskills first, then subskills by language (TypeScript, Python, Swift, Dart). Status `reference` (reason above).

### Skill: inference-format-optimizer (`eval/iterative_format_optimizer/skills/inference-format-optimizer/SKILL.md`)

- A six-step loop for an inference format: read past runs, change the compiler, prompt generator or parser, run unit tests, run the benchmark, keep the change only if tests pass, accuracy holds, output tokens grow by no more than 5% and the composite score improves, otherwise revert with `git reset --hard HEAD`; archive the run. Can run variants in parallel worktree subagents. Status `reference` (reason above).

### Skills listed from frontmatter and headings (internal, for contributors)

- `a2ui-add-eval-datapoint`: add an eval data point; needs Transcrypt; commits encrypted data.
- `a2ui-audit`: runs the blueprint, doc-sync and test-quality audits and posts the result as a labelled GitHub issue (`gh issue create`).
- `a2ui-doc-sync-check`: finds drift between code and docs.
- `a2ui-generate-pydantic-models`: generates Pydantic v2 models per protocol version.
- `a2ui-issue-triage`: fetches untriaged GitHub issues, suggests triage, runs a local review dashboard, applies decisions to GitHub.
- `a2ui-release-python`: releases the Python SDKs to PyPI through a release workflow (`gh workflow run`, `git push`, `gh pr create`).
- `a2ui-remediate-problem`: fixes an audit finding or issue and opens a pull request (`git push`, `gh pr create`).
- `a2ui-test-quality-check`: audits test assertions.
- `inspect-ai`: points to the Inspect AI docs.
- `natural-writing`: rules for plain writing, including a list of words overrepresented in AI text.
- `pr-hygiene`: pull request scope and atomicity rules from reviewer feedback.
- `public-documentation`: authoring rules for the a2ui.org site.
- `update-changelog`: rules for `CHANGELOG.md` entries.
- `a2ui-blueprint-compliance`, `a2ui-blueprint-maintenance`, `a2ui-blueprint-navigator`, `a2ui-create-feature-blueprint`, `a2ui-implement-feature-from-blueprint`: the five SDD skills in `blueprints/skills/`.

## Reasons for reference status

- `blueprints/`, `AGENTS.md`, `coding-principles` and `inference-format-optimizer` are instructions and processes for contributors to the A2UI repository; they name its paths, packages and pull requests. They are read for ideas a coding agent can reuse elsewhere (one spec for several language codebases, routing an agent to per-task skills, review rules distilled from reviewer feedback, a keep-or-revert benchmark loop), not run.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 81 model calls on opus, $5.80 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
