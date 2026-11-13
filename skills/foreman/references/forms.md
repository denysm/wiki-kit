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
- Prior work: <from `search.py recall`: past orders (outcome, estimate → measured), lessons
  that apply, material to read, each `path:line`; or "none found (searched: <query>)">
- Lessons go to: <wiki topic for /wiki:ll | none>
- Record goes to: <root>/output/work-orders/<YYYY-MM-DD>-<slug>.md | the chat only: <reason>
- Out of scope: <what the team must not do>
```

A lesson from "Prior work" that applies becomes a done criterion or a brief
line; a past measured cost corrects the estimate.

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
hire log updated (<n> lines); vacancy proposal <yes: role | no>;
order record <filed: path | chat only: reason>
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

## 8. Order record (the archive file)

One file per order, written after acceptance, so the next `search.py recall`
finds it. It follows the wiki's confidentiality rules: no secrets, no HR data,
no judgement of a person; members are roles and methods.

```markdown
---
title: "Work order: <goal in a few words>"
type: report
created: <YYYY-MM-DD>
tags: [work-order, <topic tags>]
status: <accepted | partly | not accepted>
estimate_usd: <total estimate>
measured_usd: <total measured, or unknown>
sources: [<paths the team read, relative to the wiki>]
---

# Work order: <goal>

## Order
<form 1 as approved>

## Staffing
<form 2 as approved, with the yes and its date>

## Acceptance
<form 5>

## Cost and lessons
- Cost: estimate $<x> → measured $<y>; members $<a>, foreman $<b>.
- Lessons: <path of the /wiki:ll note | none>. Tuning: <proposed for <specialist> | none>.
- What to do differently next time: <one or two lines, or "nothing">

## References on members' work
<form 7, one block per member>
```
