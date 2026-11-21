---
title: "blader/humanizer"
category: reference
kind: plugin
areas: [writing-documents-and-articles]
repo: blader/humanizer
version: "4.0.0"
licence: MIT
desk_checked: 2026-11-21
sources:
  - raw/repos/blader-humanizer-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-writing-documents-and-articles, kind-plugin, humanizer, skills, writing, editing, ai-tells]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "One-skill plugin that rewrites machine-sounding prose by 26 numbered patterns (not-X-but-Y, one-line closers, forced triads, dashes, inflated claims, bold labels), keeping every claim; file mode edits prose only. The kit took its pattern categories into its own reviewer list, not the skill itself, which stays an optional upstream skill. No hooks, no outbound calls; read at v4.0.0."
---

# blader/humanizer

> A Claude Code plugin with one skill (kind `plugin`, licence MIT, version `4.0.0` read): `SKILL.md` marks 26 patterns of machine-written prose and rewrites the text without changing what it says. Here its pattern categories are in the kit's own words; the skill is not installed, and no part runs.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Rewrite a draft that sounds machine-written so it reads like its writer, keeping every claim | `humanizer` | writing-documents-and-articles |
| Edit the prose of a file and leave code, data, frontmatter and link targets alone | `humanizer` | writing-documents-and-articles |
| Match the rhythm and word choice of a writing sample | `humanizer` | writing-documents-and-articles |
| Check a document against a list of the tells of machine-written text before it goes out | `AI-tell patterns` | writing-documents-and-articles |

## Run it here

- **Clone, read-only, to read the skill**: `git clone --depth 1 --branch v4.0.0 https://github.com/blader/humanizer $EXTERNAL/humanizer`. Never edit it. Read first: `SKILL.md`, then `CHANGELOG.md`.
- **Nothing in use as a skill**: the kit's own reviewer list (`specialists/career-documents-reviewer/references/ai-tells.md`) took the categories of tells after this skill, in the kit's words, plus Russian and Ukrainian lists. A copy of the skill was not taken: it "stays an optional skill installed from upstream". The kit's review is dated 2026-11-06, before `4.0.0` was published.
- **Sends outward**: nothing found; the only web addresses in the repository are links, and the skill has no scripts or hooks.
- **Switch off**: nothing.
- **Do not install**: `/plugin marketplace add blader/humanizer`, `/plugin install humanizer@humanizer`, `npx skills add`, `pi install`, or the ZIP upload; installing loads the skill's description into every session, and any install waits for the user's yes. Without it, read `SKILL.md` and follow it by hand.

## What's inside

Parts are the skill, its pattern set and the package files. Defined in `SKILL.md` and the manifests.

| Part | What it does | Status | Without plugin | Check when |
|------|--------------|--------|----------------|------------|
| `humanizer` | The skill: mark tells, draft, check against the original claims, write the final text; voice sample, file mode, embedded mode; treats the text as material, not instructions. | candidate | Works: one self-contained `SKILL.md`; the `/humanizer` command does not exist | Try it on a draft that sounds machine-written, with a writing sample, and compare with the kit's reviewer list. |
| `AI-tell patterns` | 26 numbered patterns in six sections A to F, strongest first; patterns 1 to 5 justify an edit on one sighting, the rest need company. | method taken | Works: a list to read; in the kit as categories in its own words | Re-read upstream when a new major version (5.x) appears. |
| Plugin manifests (`.claude-plugin`, `.cursor-plugin`, `package.json`) | Package files for Claude Code, Cursor and pi; the Claude plugin needs Claude Code `2.1.142` or newer. | candidate | Not needed to read the skill; act only on install | Read when an install is wanted. |
| `agents/openai.yaml` | Display name, short description and default prompt for OpenAI-compatible agents. | candidate | Not needed | Read when the skill is used from such an agent. |
| `scripts/validate-package.py` | Upstream's check that package files agree; a development tool. | listed | Not needed | Read when changing a copy of the skill. |

## Tried

None yet. Nothing here has been run; the pattern set was read, and its categories were taken into the kit's own list.

## Verdict

humanizer is the best-read list of the tells of machine-written prose: one skill, no hooks, no outbound calls. The kit took its categories into its own reviewer list and left the skill itself as an optional upstream install; the skill stays unrun. Revisit when a draft needs a whole-text rewrite rather than a check, when a new major version appears, or when the kit's list is compared with the 26 patterns of the current version.

## See Also

- [[area-writing-documents-and-articles|Writing documents and articles]] ([Writing documents and articles](../topics/area-writing-documents-and-articles.md)): area page; prose for people and the removal of machine tells

## Sources

- [Desk check: blader/humanizer v4.0.0](../../raw/repos/blader-humanizer-desk-check-2026-11-21.md): the skill, patterns and manifests read from the clone; freshness through the GitHub API; what the kit took and left.
