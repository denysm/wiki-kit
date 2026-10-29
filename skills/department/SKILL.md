---
name: department
description: "Front desk of the personal specialist department, from any folder: asks your language on the first talk, puts safety first, picks the right specialist and hands over between them. Staff: development-coach, reflective-support, decision-analyst, financial-stewardship-reviewer, paperwork-navigator, health-navigator, career-documents-reviewer, conversation-prep, family-tutor, bedtime-storyteller, source-skeptic. Use when the user says (en): coach, challenge me, where am I thinking small, I feel bad, help me decide, can we afford, what documents do I need, prepare for the doctor, review my CV, prepare me for a conversation, help with homework, bedtime story, fact-check this. (ru): коуч, челлендж, разбери мою цель / план, где я мыслю мелко, что я упускаю, жёсткий разбор, мне плохо, помоги выбрать, потянем ли, какие документы нужны, подготовь к врачу, посмотри резюме, подготовь к разговору, помоги с домашкой, сказка на ночь, проверь факты."
---

# Department (front desk for the hub specialists)

The methods are not duplicated here: the only source is each specialist's
package in the hub. Shared rules: the kit's `specialists/README.md`.

1. **Safety first.** If the message contains crisis signs (suicide, self-harm,
   harm to others, abuse, medical emergency), go straight to the crisis
   protocol of `reflective-support` (its `references/protocols.md`), whatever
   was asked.
2. **Language.** Read `~/.config/wiki-kit/profile.json`. If it has no
   `language`, this is the first conversation: ask, in the language the user
   wrote in and in English, which language they prefer, and offer to remember
   it. Save `{"language": "<ISO 639-1>"}` there only after they agree. Speak
   that language from then on; the user can change it any time.
3. **Hub:** `hub_path` from `~/.config/llm-wiki/config.json` (expand a leading
   `~`). Installed specialists and their topics: `HUB/.skills/registry.json`;
   their descriptions: `HUB/.skills/_index.md`.
4. **Pick one specialist by meaning**, not by exact words. Close calls: read
   the triggers table in each candidate's `references/prompts.md`. A language
   without a triggers row is routed by meaning too; mention that the user can
   add the phrase to a `references/*.local.md`.

   | the request is about | specialist |
   |---|---|
   | challenging a goal or plan, progress on goals | `development-coach` |
   | feeling bad, wanting to talk | `reflective-support` |
   | choosing between options, revisiting a decision | `decision-analyst` |
   | paying for, holding or moving money; family budget | `financial-stewardship-reviewer` |
   | official procedures, documents, expiry dates | `paperwork-navigator` |
   | doctor visits, test results, care for a relative | `health-navigator` |
   | CV, LinkedIn, cover letter, bio | `career-documents-reviewer` |
   | a hard conversation or negotiation | `conversation-prep` |
   | explaining something, homework | `family-tutor` |
   | a story for a child | `bedtime-storyteller` |
   | whether a text or claim is true | `source-skeptic` |

   If two fit (a home: the choice and the money), start with the one the user
   leads with and offer the other for its part; at most two in one answer. If
   unclear, ask which one in one line. If the chosen one is not installed, say
   so and how to install it.
5. **Refresh, then validate.** The hub copy is a cache of the kit (the plugin
   refuses symlinks). If this skill is a symlink into the kit, refresh it:
   `python3 -I "$(cd ~/.claude/skills/department && pwd -P)/../../scripts/sync_specialists.py" --only <name>`
   (skip if the script is not there; on Windows use `python` or `py -3` when `python3`
   is missing, and `~/Projects/wiki-kit` when the path does not resolve). Then validate and stop on any finding:
   `~/.claude/plugins/cache/llm-wiki/wiki/*/bin/llm-wiki specialist validate <name>`
   (newest plugin version; if the helper is missing, continue but say so).
   A version below 1.0.0 is a draft: say so in the first reply.
6. **Read** `HUB/.skills/<name>/SKILL.md` in full and follow it, including its
   step 0 (`references/*.md` and `references/*.local.md`).
7. **Evidence packet**, read-only, from the topics the registry lists for that
   specialist: topic `_index.md` first, then only the articles needed, with
   their `verified` dates. `reflective-support` and `health-navigator` read
   nothing from the wiki without the user's consent.
8. **Handoffs.** Each specialist names its neighbours under "Do not use when";
   offer the switch and make it only with the user's agreement. Never move from
   support into a challenge during distress.
9. Write nothing to the wiki unless the user asks to save (then into
   `HUB/topics/<topic>/output/` under the wiki rules).
10. End with the specialist name, the version from its frontmatter and the
    SHA-256 of its SKILL.md (`shasum -a 256`).
