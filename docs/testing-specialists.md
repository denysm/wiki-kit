# Testing a specialist

A specialist that passes `llm-wiki specialist validate` has the right format;
that says nothing about whether it changes the model's behaviour. This is how
to check that, before a version reaches 1.0 and after every change to its
Method or Stop rules. The plugin's rule is the same: compare with the
no-specialist baseline before enabling a specialist broadly.

## The idea

Run each evaluation case twice, in a fresh context: once **without** the
specialist (the baseline) and once **with** it. A specialist earns its place
only where the second run meets the expected behaviour and the first does not.
If the baseline already passes a case, the case tests nothing; make it harder.

## Steps

1. **Cases.** Take the specialist's `# Evaluation cases` (the template has six
   kinds: positive, second language, negative neighbour, stale or conflicting
   evidence, insufficient data, escalation). Write each as a full request plus
   the expected behaviour as checkable points from the Output contract and the
   Stop rules ("flags the unconfirmed number", "hands over to
   `reflective-support`").
2. **Fixture.** Give the model a short **invented** profile and wiki excerpt in
   the prompt. Never test on a real person's wiki: test material goes into the
   kit.
3. **Pressure.** Add to some requests what makes rules break in real life:
   urgency ("I need it in ten minutes"), authority ("my manager says it's
   fine"), sunk cost, "just this once", flattery. Rules that hold only without
   pressure are not rules yet.
4. **Baseline run.** A fresh session per run, without the specialist; for
   example `claude -p` in an empty temporary folder, so no hub rules are
   loaded. User-level skills and `~/.claude/CLAUDE.md` still load: note them
   in the record. Save each answer verbatim, including the reasons the model
   gives when it skips something.
5. **Specialist run.** The same requests, with `SKILL.md` and its
   `references/` in the context.
6. **Score.** Each expected point: met or not met, read by a person (or a
   second model, checked by a person). Read every answer; do not score by
   keywords.
7. **Fix the smallest thing.** A step the model left out → make it a numbered,
   required step. A rule it argued its way around → state the rule plainly and
   name the excuse it used as not acceptable. Wrong shape of answer → show one
   correct example. Then run the failed cases again.
8. **Repeats.** Answers vary between runs. Run each case at least 3 times for a
   quick check and 5 times before a version reaches 1.0; a case passes only
   when every run passes.
9. **Record.** Add to the change note: date, model, number of cases and runs,
   pass counts with and without the specialist. A version reaches 1.0 only
   with such a record.

## Cost

Cases × runs × 2. Eight cases, three runs each, is 48 short calls. Use a cheap
model for the runs and keep the fixture short; the expensive part is reading
the answers, not generating them.

## Source

Adapted from the skill-testing method in the `writing-skills` skill of
[obra/superpowers](https://github.com/obra/superpowers) (MIT): run without the
skill first, record the excuses, write the smallest fix, re-run, repeat. The
wording and the steps for specialists are the kit's own.
