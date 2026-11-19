---
name: wrap
description: "Close the session in one word: writes the lessons note in the /wiki:ll format and files it with one script call (notes index, log, the project's state note, commit), pushes where the project's rules say, rebuilds the search index only after a large import, then gives a pasteable prompt for the next chat and the budget report. Use when the user ends the work, in any wording (en): wrap up, wrap, that's it, we're done, end of session, close the session, digest this chat. (ru): итог, подведи итог, конец, закрываем, сворачиваемся, закругляемся, ну всё, на сегодня всё, переварить чат, переварить в вики. (uk): підсумок, кінець, закриваємо, згортаємось, на сьогодні все. Not for ending a single step inside ongoing work."
metadata:
  version: "1.1.0"
---

# Wrap (close the session)

One word from the user replaces the end-of-session checklist. Only reading this
conversation needs the model; the rest is one script call. A closing costs the
number of model turns times the context size (at 250k tokens every turn re-reads
the whole session), so the target is **three turns**:

1. one `Write`: the lessons note (and a memory file in the same turn, if any);
2. one `Bash`: file, commit, push, index and budget, chained;
3. the report.

Do not look for the wiki, read `_index.md`, `log.md` or the state note, or read a
file to edit it: the script does that. Read something only when a step fails.

## 0. Is it really the end?

The trigger words are common ("ну всё", "конец", "that's it"). Treat the message
as a wrap only when it closes the work, not when it closes one step, voices
frustration, or is part of a sentence about something else. If in doubt, ask one
short question in the user's language ("Закрываем сессию: уроки в вики, коммит,
промпт на следующий чат?") and wait. A bare trigger after finished work needs no
question.

If the session produced nothing worth keeping (a lookup, a short answer), say so
in one line and only run the budget report (step 2, last command), then step 3.

## 1. Turn 1: the lessons note

Write `<wiki root>/raw/notes/YYYY-MM-DD-ll-<slug>.md` with one `Write`. The wiki
root and its rules (language, `.local.md`, confidentiality) come from the
project's `CLAUDE.md`, which is already in context. This replaces `/wiki:ll`:
the same note format, without its search and filing turns.

- Topic: where the session's work belongs. Work across topics: one note per
  topic, all in this turn. No topic fits: ask.
- Only what a later session would otherwise rediscover: a trick that worked, a
  trap with its fix, a measured number. Not a retelling of the chat. Usually 2–7
  lessons; none is a valid result (then no note, go to step 2 without
  `ll_file.py`).
- A lesson never carries secrets; the audit hook refuses the `Write` if it does.
- The whole transcript is saved only on request (`/wiki:session` promote).

```markdown
---
title: "Lessons Learned: <session theme> (session <id>)"
type: notes
source: session
ingested: YYYY-MM-DD
authors: [<user>, Claude Code]
source_date: YYYY-MM-DD
tags: [lessons-learned, <topic tags>]
lesson_kind: lessons-learned
lesson_count: N
category: notes
confidence: high
summary: "<N lessons, one clause each>"
---

# Lessons Learned: <session theme>

> Extracted from session <id> on YYYY-MM-DD. <One sentence of scope.>

## Lesson 1: <title>

**Category**: gotcha | pattern | rule | discovery | correction
**Context**: <what was being done>
**Symptom**: <the error or failure, exact message>
**Root cause**: <why>
**Fix**: <what was done>
**Rule**: <one sentence that holds beyond this case>
```

Quote every free-text frontmatter value. `lesson_count` equals the number of
`## Lesson N` headings. `<id>` is the first 8 characters of the session id (the
budget report prints it); drop `(session <id>)` when unknown.

Durable facts about the user or how they want to work go to memory, as the memory
rules say, not into the wiki: write the memory file in this same turn; its index
line is appended in step 2.

A lesson that makes a wiki article wrong is fixed in the article only when the
claim is wrong now (extra turns), and counted with `--articles M`; anything else
waits for the next compile.

## 2. Turn 2: one Bash call

`<kit>` is the kit path the project's `CLAUDE.md` names, else
`$(cd -P <this skill's folder>/../.. && pwd)`. Chain with `;` so the budget report
prints even when a step fails:

```
K=<kit>/scripts
python3 -I $K/ll_file.py <note> --apply --commit --co-author "<the session's Co-Authored-By value>" \
  --state "<done, with commit ids>" --state "<verified, how>" --state "<open>" \
  [--state-section "<heading>"] [--articles M] [--push];
[printf '%s\n' '- [Title](file.md) — hook' >> <memory dir>/MEMORY.md;]
[git -C <repo> add <own paths> && git -C <repo> commit -m "<op>: …" [&& git -C <repo> push];]
[nohup python3 -I $K/search.py index <hub> > ~/.cache/wiki-kit/index.log 2>&1 &]
<the project's usage report, else: python3 -I $K/claude_usage.py --session last brief>
```

- `ll_file.py` adds the note's row to `raw/notes/_index.md` and its line to the
  wiki's `log.md`, appends each `--state` bullet to the last `## ` section of the
  hub `README.md` (`--state-section` names or creates a section, `--readme`
  another file), checks the note and the bullets with the `raw_check.py` rules
  (exit 2, nothing written), and commits only these files as
  `ll: <topic> — N lessons: <theme>`. What is already there is not added again.
  Without `--apply` it prints the plan.
- State bullets: what was done (with commit ids), what was verified and how,
  what is still open. Close an item only with its evidence. No `--state` when the
  session did not change the state.
- Other repositories the session wrote to and left uncommitted: commit them in
  the same call, by explicit paths of this session's files (another session may
  have drafts there), following the project's git rules and attribution lines.
- `--push` and `git push` only where the project or memory says to push (for
  example the kit itself). A pre-push or leak check that refuses: fix or ask,
  never `--no-verify`.
- The search index only when the session added more than a few dozen files to a
  wiki; `search.py query` refreshes changed files by itself.

## 3. Turn 3: the report

Short, in the user's language: lessons filed (topic, file, count), state
updated, commits per repository (pushed or local), index (skipped or started),
then:

- **Next-chat prompt:** a fenced block the user can paste into a new chat as is:
  goal, state with commit ids and paths, the first concrete step, what not to
  redo. No placeholders. If nothing is pending, say so instead.
- **Budget:** the usage report's output from step 2 (if it failed, say so). Its
  `last answer ≈ $…` is the cost of this closing.
- One line: the session can be cleared (`/clear`) or a new chat started.
