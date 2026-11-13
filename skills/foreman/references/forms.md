# Foreman forms

Fill the forms in the user's language (`~/.config/wiki-kit/profile.json`,
`language`); keep their fields and order. Short is better: a form is a
checklist, not an essay.

## 1. Work order

```markdown
**Work order <YYYY-MM-DD>-<short-slug>**
- Goal: <one sentence: what exists when the work is done>
- Done criteria:
  1. <checkable statement: a file, a count, a check that passes>
  2. <...>
- Inputs: <exact paths, URLs, topics; what the team may read>
- Deliverable: <where the result goes: the chat | a path | a wiki topic>
- Write scope: <exact paths, or "none (read-only)">
- Budget: <USD at list prices>, at most <N> members
- Deadline: <this session | date>
- Lessons go to: <wiki topic for /wiki:ll | none>
- Out of scope: <what the team must not do>
```

## 2. Staffing table

```markdown
| # | role | who | model | reads | delivers | estimate |
|---|---|---|---|---|---|---|
| 1 | <role> | <specialist / agent / built-in + brief / consultant / script> | <haiku/sonnet/opus/vendor:model> | <inputs> | <report shape> | <$median (p90 $x), type row or `any`> |
| — | foreman (this session) | foreman | opus | reports only | acceptance | measured at the end |

Total estimate: $<sum of medians> (upper bound $<sum of p90>); budget $<n>.
Estimates come from roster.py (claude_usage.py over local logs since <date>),
not quotes. Hire? (yes / change / no)
```

A row whose role matches a vacancy adds "(vacancy: `<name>`)". A row that
breaks the model rule (Haiku copies, Sonnet reads, Opus judges) adds its
reason.

## 3. Brief for a member

```markdown
You are <role> on work order <id>. One task, then stop.
- Goal of the order: <one sentence>. Your part: <one sentence>.
- Read: <exact paths / URLs>. Read nothing else.
- Write: <exact paths | nothing — read-only>. No git, no other wiki, no outside system.
- Method: <steps, or "read HUB/.skills/<name>/SKILL.md and its references/, then apply it to this part">.
- Report (under <N> words): what you did; findings, each with `path:line` or URL;
  what you did not check and why; anything that looked sensitive (do not copy it).
- Stop and report instead of guessing when an input is missing or contradictory.
  Do not fill gaps from your own knowledge.
```

## 4. Member report (what each member returns)

```markdown
**<role> — report on <order id>**
- Done: <one line>
- Findings: <bullet per finding, each with its source link>
- Not checked: <list, or "nothing">
- Notes for the foreman: <optional, one line>
```

## 5. Acceptance record

```markdown
| # | done criterion | verdict | evidence |
|---|---|---|---|
| 1 | <criterion from the order> | met / partly / not met | <command and its result, path, quote> |
```

Quality control: <what was checked, how (source-skeptic / check_evidence.py /
re-run), result>.

## 6. Report to the user

```markdown
**Result:** <one or two sentences>
<acceptance record>
**Deviations from the order:** <list, or "none">
**Cost:** estimate $<x> → measured $<y> (members $<a>, foreman $<b>)
**Experience:** lessons <filed to topic | none: reason>; tuning notes <proposed | none>;
hire log updated (<n> lines); vacancy proposal <yes: role | no>
<references, below>
```

## 7. Reference on a member's work

One block per member. It describes the method's output, never a personality.

```markdown
**<role> — <who>, <model>**
- Task: <one line>. Delivered: <against the brief: full / partial / off-brief>.
- Quality: <QC findings: n claims checked, n defects, returned yes/no>.
- Cost: estimate $<x>, measured $<y>.
- Next time: hire again as is / hire with this brief change: <...> / do not hire for this.
```
