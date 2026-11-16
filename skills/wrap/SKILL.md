---
name: wrap
description: "Close the session in one word: files what the session learned into the wiki (lessons via /wiki:ll, the project's state note), commits and pushes where the project's rules say, rebuilds the search index only after a large import, then gives a pasteable prompt for the next chat and the budget report. Use when the user ends the work, in any wording (en): wrap up, wrap, that's it, we're done, end of session, close the session, digest this chat. (ru): итог, подведи итог, конец, закрываем, сворачиваемся, закругляемся, ну всё, на сегодня всё, переварить чат, переварить в вики. (uk): підсумок, кінець, закриваємо, згортаємось, на сьогодні все. Not for ending a single step inside ongoing work."
---

# Wrap (close the session)

One word from the user replaces the end-of-session checklist. The only part that
needs the model is reading this conversation; everything else is a script or git.

## 0. Is it really the end?

The trigger words are common ("ну всё", "конец", "that's it"). Treat the message
as a wrap only when it closes the work, not when it closes one step, voices
frustration, or is part of a sentence about something else. If in doubt, ask one
short question in the user's language ("Закрываем сессию: уроки в вики, коммит,
промпт на следующий чат?") and wait. A bare trigger after finished work needs no
question.

If the session produced nothing worth keeping (a lookup, a short answer), say so
in one line, skip steps 1–4, and go to step 5.

## 1. Lessons into the wiki

Run `/wiki:ll` (Skill `wiki:ll`) on this session. It extracts error→fix
patterns, corrections and discoveries into the topic's `raw/notes/`.

- Topic: where the session's work belongs. Name it to `/wiki:ll` explicitly. If
  the work spans topics, file each lesson where it is used; if no topic fits,
  ask.
- Only what a later session would otherwise rediscover: a trick that worked, a
  trap with its fix, a measured number. Not a retelling of the chat.
- Follow the project's rules for raw files (confidentiality, `.local.md`,
  language). A lesson never carries secrets.
- The whole transcript is saved only on request (`/wiki:session` promote).

## 2. Project state

If the project keeps a state note (for example a `README.md` section "Состояние
на …" / "State as of …", or what its `CLAUDE.md` names), update it: what was
done (with commit ids), what was verified and how, what is still open. Close an
item only with its evidence. Skip when the session did not change the state.

Durable facts about the user or how they want to work go to memory, as the
memory rules say, not into the wiki.

## 3. Commit and push

For every repository the session wrote to (`git status --short` in each):

- commit with the operation in the message (`ll: …`, `docs: …`, `compile: …`),
  following the project's git rules and attribution lines;
- push only where the project or memory says to push (for example the kit
  itself); otherwise leave it local and say so;
- a pre-push or leak check that refuses: fix or ask, never `--no-verify`.

## 4. Search index

Nothing to do in most sessions: `search.py query` refreshes changed files on each
call. Only when the session added more than a few dozen files to a wiki (a large
ingest or compile), rebuild in the background and do not wait:

```
nohup python3 -I <kit>/scripts/search.py index <hub> > ~/.cache/wiki-kit/index.log 2>&1 &
```

`<kit>` is the folder this skill lives in, two levels up (resolve the symlink).

## 5. Handoff and budget

- **Next-chat prompt:** a fenced block the user can paste into a new chat as is:
  goal, state with commit ids and paths, the first concrete step, what not to
  redo. No placeholders. If nothing is pending, say so instead.
- **Budget:** if the project's `CLAUDE.md` names a usage report, run it and show
  its output; otherwise run `python3 -I <kit>/scripts/claude_usage.py --session last brief`
  when it exists. If it fails, say so in one line.
- End with one line: the session can be cleared (`/clear`) or a new chat started.

## Report

Short, in the user's language: lessons filed (topic and file), state updated,
commits per repository (pushed or local), index (skipped or started), then the
handoff block and the budget output.
