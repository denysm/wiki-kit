# Triggers, red flags and templates

Draft: the physician reviewer checks the red-flag list before 1.0.0. Kept in
the language they were written in, tagged `lang`; add your language as a new
row or block, never replace an original.

## Triggers

| lang | phrase | mode |
|---|---|---|
| en | prepare for the doctor, what to ask the doctor | visit prep |
| en | explain my test results, compare my blood tests | results |
| en | which doctor should I see, where to go with | navigation |
| en | care plan for my mother, medicine schedule | caregiving |
| ru | подготовь к врачу, что спросить у врача | visit prep |
| ru | объясни анализы, сравни анализы | results |
| ru | к какому врачу идти, куда обратиться | navigation |
| ru | уход за мамой, график лекарств | caregiving |

## Red flags: urgent care now

Emergency number: 112 (EU), 911 (US, Canada); elsewhere the local one.

- Chest pain or pressure, especially with sweating, breathlessness or pain
  spreading to arm, jaw or back.
- Stroke signs: face drooping, arm weakness, speech trouble (FAST), sudden
  severe headache, sudden loss of vision or balance.
- Difficulty breathing, blue lips, choking.
- Severe bleeding, major injury, burns over a large area.
- Signs of a severe allergic reaction: swelling of face or throat, wheeze,
  collapse.
- Confusion, fainting, seizure, unusual drowsiness.
- Fever in an infant under three months; a child who is floppy, will not drink
  or has a rash that does not fade under pressure.
- Thoughts of suicide or self-harm → crisis protocol of `reflective-support`.

## Visit sheet

```markdown
# Visit: <date> · <doctor or service>
- Main concern (one sentence):
- Started: <date> · Course: <better / worse / comes and goes> · Triggers:
- Tried so far:
- Medicines and supplements (as on the package, with dose):
- Allergies:
- Relevant history:
- Questions, most important first: 1. 2. 3.
- What I want from this visit:
```

## Results table

| test | unit | lab range | <date 1> | <date 2> | marked by lab | meaning (source, date) |
|---|---|---|---|---|---|---|

## Phrasing

- `lang: en` "I can't diagnose, but I can help you get the most out of the
  visit: let's write down what the doctor needs to know."
- `lang: ru` «Поставить диагноз я не могу, но могу помочь подготовиться, чтобы
  визит дал максимум: давайте запишем, что врачу важно знать.»
