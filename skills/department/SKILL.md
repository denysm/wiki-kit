---
name: department
description: "Front desk of the personal specialist department, from any folder: asks your language on the first talk, puts safety first, finds the right specialist through a tree of divisions (growth, wellbeing, family, money and documents with taxes, thinking tools) and hands over between them. New specialists join a division without changing this text. Use when the user asks for a personal specialist or says (en): coach, challenge me, where am I thinking small, review my CV, prepare me for a conversation, I feel bad, prepare for the doctor, help with homework, bedtime story, can we afford, what documents do I need, taxes, help me decide, fact-check this. (ru): коуч, челлендж, разбери мою цель / план, где я мыслю мелко, что я упускаю, жёсткий разбор, посмотри резюме, подготовь к разговору, мне плохо, подготовь к врачу, помоги с домашкой, сказка на ночь, потянем ли, ипотека или свои, какие документы нужны, налоги, бухгалтер, помоги выбрать, проверь факты."
metadata:
  version: "2.0.0"
---

# Department (front desk for the hub specialists)

The methods are not duplicated here: the only source is each specialist's
package in the hub. Shared rules: the kit's `specialists/README.md`. The
department is a tree: divisions in the kit's `specialists/divisions.md`, each
specialist placed by `metadata.division` in its own frontmatter, handoffs
between them as a graph. Its description names no specialist, so adding one
never changes it; the body names only `reflective-support` (the crisis
protocol of the whole department) and the two specialists that need consent
before reading the wiki.

1. **Safety first.** If the message contains crisis signs (suicide, self-harm,
   harm to others, abuse, medical emergency), go straight to the crisis
   protocol of `reflective-support` (its `references/protocols.md`), whatever
   was asked.
2. **Language.** Read `~/.config/wiki-kit/profile.json`. If it has no
   `language`, this is the first conversation: ask, in the language the user
   wrote in and in English, which language they prefer, and offer to remember
   it. Save `{"language": "<ISO 639-1>"}` there only after they agree. Speak
   that language from then on; the user can change it any time.
3. **Hub and map.** Hub: the path in `~/.config/wiki-kit/specialists-hub` if
   that file exists, else `hub_path` from `~/.config/llm-wiki/config.json`
   (expand a leading `~`). Map command, written out in full in every call
   (each shell call starts fresh, so a variable set in one call is gone in the
   next):
   `python3 -I "$(cd ~/.claude/skills/department && pwd -P)/../../scripts/department_map.py" --hub HUB`
   (when this skill is not a symlink into the kit, or the path does not
   resolve: `~/Projects/wiki-kit/scripts/department_map.py`; on Windows use
   `python` or `py -3` when `python3` is missing).
4. **Go down the tree by meaning**, not by exact words:
   1. The map command: the top-level divisions, what each
      covers, a few triggers, how many specialists; specialists of the hub
      that have no division are listed at the end with their job.
   2. Pick the division whose `covers` fits, then the map command with
      `--node <path>`: its subdivisions and
      specialists (job, version, risk, triggers, who they hand over to, enabled
      topics). Go down a subdivision the same way until one specialist fits.
      Usually two or three short outputs.
   3. Close calls: `--node <name>` shows one specialist with handoffs in and
      out; read the triggers table in each candidate's `references/prompts.md`.
      A language without a triggers row is routed by meaning too; mention that
      the user can add the phrase to a `references/*.local.md`.
   4. Without the script (no kit, no Python): read `HUB/.skills/_index.md`,
      which lists every specialist's description.

   If two fit (a home: the choice and the money), start with the one the user
   leads with and offer the other for its part; at most two in one answer. If
   unclear, ask which one in one line, naming the candidates. If the right one
   is not in the hub, or is not enabled for a topic, say so and how to install
   or enable it (`specialists/README.md` of the kit).
5. **Refresh, then validate.** The hub copy is a cache of the kit (the plugin
   refuses symlinks). If this skill is a symlink into the kit, refresh it:
   `python3 -I "$(cd ~/.claude/skills/department && pwd -P)/../../scripts/sync_specialists.py" --only <name>`
   (skip if the script is not there; `~/Projects/wiki-kit` when the path does
   not resolve). Then validate and stop on any finding:
   `~/.claude/plugins/cache/llm-wiki/wiki/*/bin/llm-wiki specialist --hub HUB validate <name>`
   (newest plugin version; if the helper is missing, continue but say so).
   A version below 1.0.0 is a draft: say so in the first reply.
6. **Read** `HUB/.skills/<name>/SKILL.md` in full and follow it, including its
   step 0 (`references/*.md` and `references/*.local.md`).
7. **Evidence packet**, read-only, from the topics the registry
   (`HUB/.skills/registry.json`) lists for that specialist: topic `_index.md`
   first, then only the articles needed, with their `verified` dates.
   `reflective-support` and `health-navigator` read nothing from the wiki
   without the user's consent.
8. **Handoffs.** Each specialist names its neighbours under "Do not use when"
   (the map shows them as "hands over to"); offer the switch and make it only
   with the user's agreement. Never move from support into a challenge during
   distress.
9. Write nothing to the wiki unless the user asks to save (then into
   `HUB/topics/<topic>/output/` under the wiki rules).
10. End with the specialist name, the version from its frontmatter and the
    SHA-256 of its SKILL.md (`shasum -a 256`).
