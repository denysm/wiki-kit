---
title: "Desk check: ygavrilov/claude-code-kit 8584f0d"
source: https://github.com/ygavrilov/claude-code-kit/tree/8584f0d46aef89afc5ec986f5cd177678886d743
type: repos
authors: ["ygavrilov"]
source_date: 2026-08-12
ingested: 2026-11-21
repo: ygavrilov/claude-code-kit
kind: plugin
version: "8584f0d"
licence: none
tags: [catalog, desk-check, kind-plugin, claude-code-kit, claude-code, skills, llm-wiki]
summary: "ygavrilov/claude-code-kit at commit 8584f0d read from a read-only clone: one Claude Code plugin with five skills (skill, agent and plugin authoring assistants, an LLM wiki skill and a wiki operations skill) and a maintainer pre-commit git hook. No licence file, so nothing may be copied. Read as a reference: a simple wiki skill close to the Karpathy pattern and a source of conventions for skills and plugins."
---

# Desk check: ygavrilov/claude-code-kit 8584f0d

Read from a clone of the default branch at commit `8584f0d46aef89afc5ec986f5cd177678886d743` (committed 2026-08-12T21:50:45Z), at `$EXTERNAL/claude-code-kit`. The clone was not modified; nothing was installed or enabled. Checked 2026-11-21. Version read by this desk check: 8584f0d (no tags or releases exist).

## Repository facts

- `.claude-plugin/plugin.json`: `"name": "claude-code-kit"`, `"version": "3.6.12"`; description "A plugin providing essential skills for creating agents, skills and managing llm wiki." `.claude-plugin/marketplace.json` is a marketplace (`"name": "ygavrilov-claude-code-kit"`) whose single plugin has `"source": "./"`.
- README: "five skills for building and managing Claude Code skills, agents, plugins, and LLM wikis. Opinionated, based on official docs."
- No licence file, and none in the manifests.
- Other folders: `docs-upstream/` (snapshots of four official Claude Code docs pages: skills, sub-agents, plugins, plugins reference) and `.githooks/`. The README also lists `scripts/check-docs-freshness.sh`, a launchd plist and a `CLAUDE.md`; none of them is in the repository at this commit.
- Each authoring skill keeps a condensed copy of the official docs beside it (`claude-code-skills-docs.md`, `claude-code-agents-docs.md`, `claude-code-plugins-docs.md`).

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/ygavrilov/claude-code-kit`: `pushed_at` 2026-08-12T21:53:42Z; licence `null` (no licence detected, matching the missing file); default branch `master`; not archived; description "Plugin for Claude Code to create a Skill Master Skill".
- `gh api repos/ygavrilov/claude-code-kit/releases/latest`: 404, no releases. No tags.
- `gh api repos/ygavrilov/claude-code-kit/commits/master`: `8584f0d46aef89afc5ec986f5cd177678886d743`, so the clone is at the head of the default branch.

## How to run here

- **Clone**: `git clone https://github.com/ygavrilov/claude-code-kit $EXTERNAL/claude-code-kit`, then `git -C $EXTERNAL/claude-code-kit checkout 8584f0d`; read-only.
- **Licence**: none. Read only; nothing may be copied into the kit, not even adapted text.
- **Telemetry and outbound calls**: none. The skills are text; `llm-wiki-ops` runs `` !`pwd` `` through shell injection and, with its allowed tools, creates `raw/`, `wiki/` and `WIKI.md` in the current folder.
- **Hooks**: no Claude Code hooks. `.githooks/pre-commit` is a git hook for the repository's maintainers and is "Not auto-installed".
- **What breaks without the plugin**: nothing when a skill is read from the clone; skill names lose the `/claude-code-kit:` namespace. `plugin-assistant` links the other two assistants by relative path, which works from the clone.
- **Install**: not needed and not done; the plugin is not installed.

## Parts

### `skill-assistant` (`skills/skill-assistant/`: `SKILL.md`, `principles.md`, `workflow.md`, `examples.md`, `claude-code-skills-docs.md`)

- Asks what skill to create or edit, then walks requirements, frontmatter, content, location, supporting files and a validation checklist.
- Conventions (`principles.md`): "SKILL.md Must Be Skinny" (frontmatter, one-line role, links to supporting files); "One File Per Concern" (`workflow.md`, `examples.md`, reference files, `scripts/`); minimal tools; classify a skill first as "Workflow" (numbered steps, often `context: fork`) or "Rules" (a declarative spec); "Descriptions Drive Invocation".
- Needs: nothing to read. Its `allowed-tools` let it write skill files when run.

### `agent-assistant` (`skills/agent-assistant/`, same layout)

- Creates or edits subagent definition files. Conventions: "One Agent, One Specialty"; an agent is a single `.md` file; the description drives delegation; minimal tool access; `memory: project` as the default memory scope; `bypassPermissions` only for trusted, well-scoped agents; `isolation: worktree` for changes to review.
- Needs: nothing to read.

### `plugin-assistant` (`skills/plugin-assistant/`, same layout)

- Creates or edits plugins and marketplaces; defers the skills and agents inside a plugin to the two assistants above. Conventions: "Manifest Is the Identity"; components sit at the plugin root, not inside `.claude-plugin/` ("The single most common mistake"); one coherent purpose per plugin; "Version Deliberately"; "Plugins Are Standalone First" (keep `.claude/` config until sharing is needed). Examples include a single self-hosted marketplace and plugins in separate repositories.
- Needs: nothing to read.

### `llm-wiki` (`skills/llm-wiki/`: `SKILL.md`, `pattern.md`, `operations.md`, `conventions.md`)

- Explains the LLM wiki pattern: three layers (`raw/` immutable sources, `wiki/` owned by the LLM, `WIKI.md` schema co-evolved with the user); ingest one source at a time, query through `wiki/index.md` and file good answers back as pages, lint for contradictions, orphans and stale claims; `index.md` plus an append-only `log.md` with `## [YYYY-MM-DD] operation | description` entries. Read-only tools (`Read, Glob, Grep`).
- A simple wiki skill close to the Karpathy pattern (the kit owner's reading).
- Needs: nothing.

### `llm-wiki-ops` (`skills/llm-wiki-ops/`: `SKILL.md`, `workflows.md`, `schema-template.md`)

- `init` creates the wiki scaffold and a `WIKI.md` from the template; `ingest` analyses a code repository in eight steps (stack, structure, domain model, entry points, key flows, external dependencies, write pages, report). Runs as `context: fork` with `argument-hint: "[init|ingest] [repo-path]"`.
- Needs: nothing to read; when run, it writes into the current folder.

### `.githooks/pre-commit` (maintainer git hook)

- Blocks a commit that touches `skills/` unless the `version` in `.claude-plugin/plugin.json` changed. Enabled only by `git config core.hooksPath .githooks`.
- Needs: git, bash.

## Reason for the reference status, retold

- The kit owner reads this repository as a reference, not as a tool to use: a simple wiki skill close to the Karpathy pattern, and a source of conventions for writing skills and plugins. Every part is `reference`.
- With no licence file, no text can be copied or vendored; conventions can only be compared with the kit's own and restated in its own words.

## Cost of this desk check

Written in one agent run together with the other 2 desk checks, the cards and the use records of the same batch: 82 model calls on opus, $5.71 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
