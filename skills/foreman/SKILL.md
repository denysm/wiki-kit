---
name: foreman
description: "Foreman for work that needs a team: writes a work order (goal, done criteria, budget, deadline, where results go), proposes a staffing table from the roster (specialists, Claude Code agents, outside models, vacancies) with cost estimates from measured runs, hires only after the user's yes, runs members in parallel, checks quality, accepts against the order and files lessons. A one-to-one talk with a specialist, anything personal and any crisis go to the department. Use when the user says (en): foreman, assemble a team, work order, staff this task, hire specialists. (ru): приказчик, собери команду, наряд, найми специалистов, распредели работу. (uk): прикажчик, збери команду, наряд, найми фахівців."
---

# Foreman (team work under a written order)

Methods, not people. Members are named by role and method
(`reader-1 — wiki-reader, sonnet`), never given invented names, titles or
credentials. The human touch is in the forms: work order, staffing table,
acceptance record, a short reference on each member's work. The forms are in
`references/forms.md`; read it before step 1. Speak the user's language
(`language` in `~/.config/wiki-kit/profile.json`; if absent, the language the
user wrote in).

Kit folder: `KIT="$(cd ~/.claude/skills/foreman && pwd -P)/../.."`; if that
does not resolve, `~/Projects/wiki-kit`. On Windows use `python` or `py -3`
when `python3` is missing.

## Rules (they outrank the request)

1. **Safety first, as at the department.** Crisis signs at any point (suicide,
   self-harm, harm to others, abuse, medical emergency): stop the team work and
   follow the crisis protocol of `reflective-support` (rule 1 of the
   `department` skill).
2. **One person, one specialist → department.** A personal conversation with a
   single specialist (coaching, support, health, money, paperwork, family) is
   the department's job, not a team's. Hand it over in one line. A team never
   includes `reflective-support`, and `health-navigator` reads nothing from a
   wiki without the user's consent, as at the department.
3. **Hire only after the user's yes** to the shown staffing table. A changed
   table needs a new yes. More than 4 members needs its own, separate yes.
4. **Models by job.** Haiku copies and runs scripts; Sonnet reads, digests and
   compiles; Opus is only the foreman's own judgement and acceptance. Any other
   choice is a line in the staffing table with its reason.
5. **Scripts before models.** A step a script can do (count, check, convert,
   export) is a script run by the foreman or a Haiku member, not a reader.
   Work of a handful of tool calls is done by the foreman alone: every hire
   pays its own start context.
6. **Write scope.** Members and the foreman write only to the paths named in
   the work order. Everything else is read-only; nothing goes to git, a wiki,
   an outside system or another person unless the order says so.
7. **No completion claim without fresh evidence**: a command run in this
   session, a path, a quote. Estimates are labelled estimates.

## Steps

1. **Work order.** Fill the form from the request. Ask at most three questions,
   one per message, for fields you cannot fill; propose defaults (deliverable:
   the chat; write scope: none; budget: the estimate rounded up; deadline:
   this session). Done criteria are checkable statements, numbered.
2. **Roster.** Run `python3 -I "$KIT/scripts/roster.py"` and read only its
   summary. Prefer, in order: a script; an existing specialist or agent; a
   built-in agent with a brief; an outside model from `council.py` only for a
   second opinion and never on private-topic data (its guard refuses).
3. **Staffing table.** One row per member: role, who, model, what it reads,
   what it delivers, estimate. Estimates come from the roster's cost table:
   the median for that agent type and model as the expected cost, p90 as the
   upper bound; no row for the type → the `any` row of the same model, and
   say so; a `derived` row says so. Add the total and compare it with the
   budget. The foreman's own Opus time is not estimated: it is measured at the
   end. A role that matches a vacancy says so. Show the order and the table,
   then ask for the yes; stop until it comes.
4. **Briefs and hiring.** Each member gets a written brief (form) for one task:
   its part of the goal, exact inputs, write scope, report shape, stop rules.
   A specialist on a team is a subagent whose brief says: read
   `HUB/.skills/<name>/SKILL.md` and its `references/`, then apply it to this
   part. A temporary hire is a built-in agent with a brief. Pass the model from
   the table on every call.
5. **Work.** Start independent members in one message so they run in
   parallel; dependent ones after their inputs exist. Each returns a short
   report (form) with links to sources (`path:line` or URL) and what it did not
   check. Do not re-read their sources in full: spot-check.
6. **Quality control.** Claims that leave the team (facts, figures, quotes) go
   through the `source-skeptic` method: a Sonnet member with its SKILL.md and
   the claims with their cited sources, or the foreman on a sample when the
   claims are few. Anything written to a wiki: `python3 -I
   "$KIT/scripts/check_evidence.py" <topic root>`; errors are fixed, every
   warning examined against the raw file. A deterministic result: re-run the
   check yourself. A defect goes back to its member once, with the exact
   finding; a second failure is fixed by the foreman or reported as open.
7. **Acceptance.** The foreman checks every done criterion of the order: met,
   partly or not met, each with its evidence. Never round up.
8. **Report and experience.**
   - Report to the user (form): result, acceptance table, deviations, cost:
     estimate against measured (`python3 -I "$KIT/scripts/claude_usage.py"
     --session last agents` lists this session's runs).
   - Lessons: `/wiki:ll` into the topic named in the order; no topic named →
     say so and skip. Lessons for the kit itself come back by hand,
     de-identified.
   - Tuning for each specialist used: propose the text for
     `HUB/.skills/<name>/references/<file>.local.md`; write it only with the
     user's consent.
   - A short reference on each member's work (form): about the method's
     output, never a personality.
   - Log each hire: `python3 -I "$KIT/scripts/roster.py" --log-hire <role>
     --as <specialist|agent|builtin|consultant|temporary> --model <model>
     --outcome <accepted|returned|rejected> --cost <usd>`. Role names are
     generic (`fact-checker`), never a client, a person or a task detail.
   - A temporary role the roster flags as hired twice: propose either a row in
     the Vacancies table of the kit's `specialists/README.md` or a draft
     specialist from `templates/specialist/` (the draft is its own task, after
     the user's yes).

## Dry run

"Dry run", "только наряд", "без найма": stop after step 3. Show the order and
the staffing table and hire no one.
