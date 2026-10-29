# Triggers, phrasing and aids

Kept in the language they were written in, tagged `lang`; add your language as
a new row or block, never replace an original.

## Triggers

| lang | phrase | mode |
|---|---|---|
| en | help me decide, which should I choose, compare options | decide |
| en | is it worth it, pros and cons | decide |
| en | revisit my decision, should we change what we decided | revisit |
| ru | помоги выбрать, помоги решить, сравни варианты, что лучше | decide |
| ru | стоит ли, за и против | decide |
| ru | пересмотреть решение, может, передумать | revisit |

Not triggers: "how should we pay for it" (`financial-stewardship-reviewer`),
"what documents do I need" (`paperwork-navigator`).

## Phrasing

- Pre-mortem, `lang: en`: "Imagine it is a year from now and this choice went
  badly. What most likely went wrong?"
- Pre-mortem, `lang: ru`: «Представьте: прошёл год, и выбор оказался неудачным.
  Что, скорее всего, пошло не так?»
- Reversibility, `lang: en`: "If this turns out wrong, what does it cost to
  undo, in money and in months?"
- Reversibility, `lang: ru`: «Если окажется ошибкой, сколько стоит откатить —
  в деньгах и в месяцах?»

## Comparison table

| criterion | must / weight (owner) | option A | option B | wait |
|---|---|---|---|---|
| price + running costs (source, date) | | | | |
| exit or resale cost | | | | |
| <owner's criterion> | | | | |

## Decision record (ADR) template

```markdown
# ADR-NNNN: <decision in a few words>

- Date: YYYY-MM-DD · Status: accepted | superseded by ADR-MMMM
- Context: <why a decision was needed; constraints; who is affected>
- Options: <A, B, wait — one line each>
- Decision: <what was chosen>
- Reasons: <the criteria that decided it>
- Risks and mitigations: <top three>
- Revisit when: <date or event>
```
