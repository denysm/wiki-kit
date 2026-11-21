---
title: "ygavrilov/claude-code-kit"
category: reference
kind: plugin
areas: [building-skills-and-plugins, knowledge-bases]
repo: ygavrilov/claude-code-kit
version: "8584f0d"
licence: none
desk_checked: 2026-11-21
sources:
  - raw/repos/ygavrilov-claude-code-kit-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-building-skills-and-plugins, area-knowledge-bases, kind-plugin, claude-code, skills, llm-wiki, no-licence]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Small Claude Code plugin with five skills: assistants for writing skills, subagents and plugins, an LLM wiki skill close to the Karpathy pattern, and a wiki init/ingest skill for code repositories. No licence file, so it is read only, never copied; every part is a reference for conventions."
---

# ygavrilov/claude-code-kit

> A Claude Code plugin (kind `plugin`, no licence file, commit `8584f0d` read, no releases) with five skills for writing skills, subagents and plugins and for a simple LLM wiki. Here it is a reference for conventions only: read from a clone, never installed, nothing copied.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Check a new skill against conventions: thin `SKILL.md`, one file per concern, workflow or rules | `skill-assistant` | building-skills-and-plugins |
| Check a subagent definition: one specialty, minimal tools, memory scope | `agent-assistant` | building-skills-and-plugins |
| Check a plugin's layout and manifest before sharing it | `plugin-assistant` | building-skills-and-plugins |
| Compare with a minimal LLM wiki: `raw/`, `wiki/`, `WIKI.md`, ingest, query, lint | `llm-wiki` | knowledge-bases |
| See how a wiki can be seeded from a code repository | `llm-wiki-ops` | knowledge-bases |
| Stop skill changes from being committed without a version bump | `.githooks/pre-commit` | building-skills-and-plugins |

## Run it here

- **Clone**: `git clone https://github.com/ygavrilov/claude-code-kit $EXTERNAL/claude-code-kit`, then check out `8584f0d`; read-only.
- **Version**: commit `8584f0d` (manifest says `3.6.12`), the head of `master`; no tags or releases. Compare: `gh api repos/ygavrilov/claude-code-kit/commits/master --jq .sha`.
- **Read**: `skills/<skill>/SKILL.md`, then its `principles.md` and `workflow.md`.
- **Licence**: none. Read only; nothing may be copied into the kit, not even adapted text.
- **Switch off**: nothing; no Claude Code hooks, no network calls. `llm-wiki-ops` writes a wiki scaffold into the current folder when run.
- **Do not install**: the plugin. Not needed for reading; any install waits for the user's yes.

## What's inside

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `skill-assistant` | Interviews, then writes or edits a skill; principles, workflow, examples, condensed official docs. | reference | Works from the clone. | When the kit's skill rules change, compare. |
| `agent-assistant` | Same for subagent files: one specialty, minimal tools, `memory: project` default. | reference | Works from the clone. | When writing a new kit agent. |
| `plugin-assistant` | Same for plugins and marketplaces; components at the plugin root, deliberate versions. | reference | Works; links the two assistants by relative path. | Before packaging part of the kit as a plugin. |
| `llm-wiki` | The LLM wiki pattern: three layers, ingest, query, lint, `index.md` and `log.md`. Read-only tools. | reference | Works from the clone. | When comparing wiki conventions with simpler setups. |
| `llm-wiki-ops` | `init` scaffold and an eight-step `ingest` of a code repository; runs forked. | reference | Works; writes into the current folder. | When a wiki must be seeded from a codebase. |
| `.githooks/pre-commit` | Maintainer git hook: blocks commits to `skills/` without a manifest version bump. | reference | Opt-in git hook, not a plugin part. | When the kit wants the same guard. |

## Tried

None yet: read only, never run.

| Date | Task (by kind) | Part | Result | Cost | Record |
|------|----------------|------|--------|------|--------|

## Verdict

A small, readable set of conventions for skills, subagents and plugins and a simple wiki skill close to the Karpathy pattern; with no licence it stays a reference to compare against, never a source of text. Revisit when a licence is added or when the kit revises its own skill or plugin rules.

## See Also

- [[area-building-skills-and-plugins|Building skills and plugins]] ([Building skills and plugins](../topics/area-building-skills-and-plugins.md)): area page
- [[area-knowledge-bases|Knowledge bases]] ([Knowledge bases](../topics/area-knowledge-bases.md)): area page
- [[karpathy-llm-wiki-gist|karpathy LLM Wiki gist]] ([karpathy LLM Wiki gist](../references/karpathy-llm-wiki-gist.md)) and [[nvk-llm-wiki|nvk/llm-wiki]] ([nvk/llm-wiki](../references/nvk-llm-wiki.md)): the pattern and a full plugin for it

## Sources

- [Desk check: ygavrilov/claude-code-kit 8584f0d](../../raw/repos/ygavrilov-claude-code-kit-desk-check-2026-11-21.md): every part read from the clone, freshness through the GitHub API, the reason for the reference status.
