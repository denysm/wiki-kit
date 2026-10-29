# Triggers, sources and templates

Kept in the language they were written in, tagged `lang`; add your language as
a new row or block, never replace an original.

## Triggers

| lang | phrase | mode |
|---|---|---|
| en | what documents do I need, how to apply for, residence permit, visa | procedure |
| en | apostille, sworn translation, registration | procedure |
| en | when do our documents expire, renewal calendar | calendar |
| ru | какие документы нужны, как оформить, ВНЖ, виза | procedure |
| ru | апостиль, нотариальный перевод, регистрация, прописка, справка, пособие | procedure |
| ru | когда истекают документы, календарь продлений | calendar |

## Source hierarchy

1. The law or regulation, and the official government portal.
2. The issuing office's own instructions (migration service, municipality).
3. Embassy and consulate pages.
4. Experience notes in the owner's wiki (labelled as experience).
5. Forums and blogs: hints only, never the basis of a checklist.

## Checklist

```markdown
# <Procedure> · <country, city> · as of <date>
Sources: <links>

| # | document | original/copy | translation | apostille | valid if issued within | issued by, time | done |
|---|---|---|---|---|---|---|---|

Deadline: <date> · Apply by: <date with buffer> · Fee: <amount, source, date>
Confirm with the office: <items>
```

## Calendar

| person | document | number (last 4) | expires | renew from | lead time | next action |
|---|---|---|---|---|---|---|

## Phrasing

- `lang: en` "This checklist is based on <source> as of <date>. Offices
  sometimes ask for more; confirm the flagged items before your appointment."
- `lang: ru` «Список составлен по <источник> на <дата>. На месте иногда просят
  больше — отмеченные пункты уточните до визита.»
