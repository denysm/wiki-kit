# The specialist department

A department of personal specialists: methods, not people. Each one does one
job well, knows where its job ends, and hands over to a colleague or to a
qualified human when it does. Everyone who uses the kit tunes the specialists
for themselves; what turns out to work for everyone comes back here, so the
shared versions get better from many people's use.

## Staff

| division | name | job | risk | status | suggested topic | 1.0 needs |
|---|---|---|---|---|---|---|
| Growth | `development-coach` | challenge of a development goal, plan or decision; progress check-in | medium | 1.x, in use | career | — |
| Growth | `career-documents-reviewer` | CV, LinkedIn, cover letters: every claim backed, tailored to the role | medium | 0.x draft | career | contributor (ideally someone who hires) |
| Growth | `conversation-prep` | hard conversations and negotiations: plan, role-play, debrief | medium | 0.x draft | personal | contributor + safety reviewer |
| Wellbeing | `reflective-support` | gentle support under stress; crisis protocol for the whole department | high | 0.x draft | personal | safety reviewer |
| Wellbeing | `health-navigator` | doctor-visit prep, test results over time, care navigation, caregiving; red flags first | high | 0.x draft | personal | **physician** + safety reviewer |
| Family | `family-tutor` | explains "why" at the right age; homework help that never does the work | medium | 0.x draft | personal | contributor (ideally a teacher) + safety reviewer |
| Family | `bedtime-storyteller` | bedtime stories with a family story bible | low | 0.x draft | personal | contributor (a parent) |
| Money and documents | `financial-stewardship-reviewer` | big money decisions: buffer, full cost, stress test, scam signs | high | 0.x draft | personal | **financial or tax adviser** |
| Money and documents | `paperwork-navigator` | official procedures as dated checklists; expiry calendar | high | 0.x draft | personal | **lawyer or licensed adviser** |
| Thinking tools | `decision-analyst` | significant choices: criteria, options, total cost, pre-mortem, decision record | medium | 0.x draft | personal | contributor |
| Thinking tools | `source-skeptic` | claim-by-claim fact-check of memos, posts, pitches, studies | medium | 0.x draft | personal | contributor |

The `department` skill (`skills/department/`) is the front desk: it asks the
user's language, picks a specialist, and handles handoffs between them. Every
specialist names its neighbours under "Do not use when", so a request that
belongs elsewhere is handed over rather than half-answered.

## Vacancies

Not built yet; pick one up by copying `templates/specialist/`.

| name | job | risk | note |
|---|---|---|---|
| `trip-planner` | trips and hikes: route, budget, packing, weather and altitude safety | medium | mountain safety needs a reviewer with field experience |
| `writing-editor` | clarity and structure of letters, posts and documents | low | |

## Rules for every specialist

1. **One job.** Coaching and support stay separate packages; a specialist that
   tries to do both does both worse.
2. **Safety outranks the request.** Crisis signs in any conversation go to the
   crisis protocol of `reflective-support`, whichever specialist was asked.
3. **No simulated credentials.** Names say what the method does, never
   "therapist", "psychologist", "doctor", "lawyer". Every package has
   Non-claims and says who the qualified human is.
4. **The user's language.** On the first conversation the front desk asks
   which language the user prefers and, with consent, saves it in
   `~/.config/wiki-kit/profile.json`. Specialists reply in that language.
5. **Read-only by default.** Nothing is written to the wiki unless the user
   asks.
6. **Drafts say they are drafts.** A version below 1.0.0 announces itself in
   the first reply. 1.0.0 needs the reviews listed under Roles.

## Three layers

| Layer | Where it lives | Who changes it |
|---|---|---|
| Core method | `specialists/<name>/SKILL.md` and `references/*.md` in this repo | by pull request, after review |
| Personal tuning | `references/*.local.md` in your hub copy (ignored by git) | you, any time |
| Facts about you | articles in your own wiki (North Star, barriers, goals, what helps you) | you; never leaves your wiki |

Updating from the kit (`cp -R specialists/<name> ~/wiki/.skills/`) replaces the
core files and leaves your `*.local.md` files alone. Local files may add; they
never remove a Non-claim or a Stop rule.

Example `references/triggers.local.md`:

```markdown
| lang | phrase | mode |
|---|---|---|
| uk | розбери мою ціль | challenge |
```

## Languages

Any language is welcome. Prompts, triggers and phrasing stay in the language
they were written in, tagged `lang: xx` (ISO 639-1), with an English
translation next to them. Add your language next to the others; do not replace
an original. For your own use, add it in a `*.local.md` file; to share it,
send a pull request. Crisis wording in a new language needs the safety
reviewer, ideally with a native speaker.

Descriptions stay short. The Agent Skills format caps them at 1024 characters,
and every description is read each time the front desk routes a request, so
length costs tokens every time. A description carries the job and a few
English and Russian triggers; full trigger tables live in
`references/prompts.md` and `*.local.md`, which are read only after a
specialist is chosen. The front desk routes by meaning, so a language without
a triggers row already works; adding its row makes routing more precise.

## From personal lesson to shared principle

1. Notice something that worked or failed in a session (`/wiki:ll` helps).
2. De-identify: no names, employers, clients, figures, places, health details.
   The lesson must make sense to a stranger.
3. Write it as a principle plus at least one evaluation case (a request and the
   expected behaviour). A principle without a case is not merged.
4. Open a pull request that bumps the specialist `version` and adds a change
   note. One other contributor reviews; changes to Non-claims, Do not use when,
   Stop and escalation rules, or anything in a `risk-tier: high` package also
   need the safety reviewer.
5. Run the leak check from the main README before pushing.

## Proposing a new specialist

Start from `templates/specialist/` (or take a vacancy above). Open an issue or
pull request with: the one job, three trigger phrases, what it must not do,
its Non-claims and the qualified human it hands over to, the risk tier, and
the six evaluation cases of the template (positive, second language, negative
neighbour, stale or conflicting evidence, insufficient data, escalation).
Start at version 0.1.0. Package rules: only `SKILL.md` and Markdown under
`references/`; validate with `llm-wiki specialist validate <name>`. Add the
new name to the Staff table and to the routing table of the `department`
skill.

## Roles

- **Contributors:** anyone using a specialist; bring lessons, languages and
  evaluation cases.
- **Safety reviewer (psychology background):** owns the boundaries of every
  specialist and the whole of `reflective-support`: Non-claims, crisis
  protocol, wording in each language, evaluation cases for distress. Checks
  that techniques stay within what evidence-based practice supports.
- **Qualified reviewers for high-risk specialists:** a physician for
  `health-navigator`, a financial or tax adviser for
  `financial-stewardship-reviewer`, a lawyer or licensed adviser for
  `paperwork-navigator`. Until one signs off, the specialist stays a 0.x draft
  that says so.
- **Maintainer:** merges, keeps versions and the leak check honest.
