# Divisions of the specialist department

The department is a tree. Divisions are its inner nodes; specialists are its
leaves. A specialist says where it belongs with one line in its frontmatter,
`metadata.division: "<path>"`, so adding a specialist never touches the front
desk (`skills/department`): the desk reads this table and the packages through
`scripts/department_map.py`, one level at a time. Handoffs between specialists
(the names under "Do not use when") are the edges of a graph across the tree.

Rules:

- A path is lowercase words joined by `/`; a subdivision needs its parent row
  (`money/taxes` needs `money`).
- At most 12 children (subdivisions and specialists together) per node.
  When a node would get a thirteenth, split it into subdivisions.
- `covers` says what requests belong here, in plain words; `triggers` gives a
  few phrases per language (`en:` and `ru:` at least). The front desk routes by
  meaning, so these help, they do not limit.
- A new top-level division is the only change that also needs a line in the
  description of `skills/department`.
- Personal divisions go in `~/.config/wiki-kit/divisions.local.md` with the
  same columns (not in the hub's `.skills/`: the llm-wiki validator refuses
  unknown files there); they are never sent to the kit.

`python3 -I scripts/department_map.py --check` checks the tree, the packages
and the Staff table of `README.md` (it runs in CI).

| path | title | covers | triggers |
|---|---|---|---|
| growth | Growth | development goals, plans and progress; CV, LinkedIn and cover letters; hard conversations and negotiations | en: coach, challenge me, review my CV, prepare me for a conversation; ru: коуч, челлендж, посмотри резюме, подготовь к разговору |
| wellbeing | Wellbeing | feeling bad and wanting to talk; doctor visits, test results, care for a relative | en: I feel bad, I need to talk, prepare for the doctor; ru: мне плохо, хочу поговорить, подготовь к врачу |
| family | Family | explaining things to a child, homework help, bedtime stories | en: explain to my kid, help with homework, bedtime story; ru: объясни ребёнку, помоги с домашкой, сказка на ночь |
| money | Money and documents | big money decisions and the family budget; official procedures, documents and expiry dates | en: can we afford, mortgage or cash, what documents do I need; ru: потянем ли, ипотека или свои, какие документы нужны |
| money/taxes | Taxes | taxes, social payments and bookkeeping, one specialist per country | en: taxes, tax return, bookkeeping; ru: налоги, декларация, бухгалтер |
| thinking | Thinking tools | significant choices between options; checking whether a text or claim is true | en: help me decide, fact-check this; ru: помоги выбрать, проверь факты |
