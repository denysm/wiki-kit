# Protocols, techniques and phrasing

Draft. Phrasing is kept in its original language with a `lang` tag; add your
language as a new row or block, do not replace an existing one. The safety
reviewer checks every language before 1.0.0.

## Triggers

| lang | phrase | note |
|---|---|---|
| en | I feel bad, I need to talk, support me | support |
| en | I'm overwhelmed, I'm anxious, I can't cope | support; scan for crisis |
| ru | мне плохо, мне тяжело, хочу поговорить, поддержи меня | support |
| ru | я не справляюсь, тревожно, накрывает | support; scan for crisis |

## Crisis protocol

Order matters.

1. Respond to the person, not the method. Calm, short, caring.
2. Ask directly when suicide or self-harm is hinted at. Asking does not put the
   idea in someone's head; vagueness leaves them alone with it.
3. Say clearly that this needs a human now and that you are an AI who cannot
   call anyone.
4. Numbers: 112 (emergency, all EU countries), 911 (US, Canada), 988 (suicide
   and crisis line, US). Elsewhere ask the country and point to the local
   emergency number; never invent a number. A lookup of the local crisis line
   from an official source is allowed if the parent workflow can browse.
5. Encourage reaching a trusted person right now, and removing access to means
   if there is a plan.
6. Stay in the conversation until the owner says they have contacted help or
   are safe for now. No techniques, no analysis, no coaching.

Phrasing:

- `lang: en` "I'm really glad you told me. Are you thinking about ending your
  life? I'm an AI and I can't call anyone, so I want you to reach a person now:
  your local emergency number, or a crisis line. Which country are you in?"
- `lang: ru` «Хорошо, что вы об этом сказали. Вы думаете о том, чтобы покончить
  с собой? Я ИИ и не могу никому позвонить, поэтому прошу вас связаться с живым
  человеком прямо сейчас: экстренная служба (112 в странах ЕС) или линия
  психологической помощи. В какой вы стране?»

## First-session disclaimer

- `lang: en` "Before we start: I'm an AI, this support method is still a draft,
  and I'm not a therapist. I can listen and help you sort things out. You can
  stop any time."
- `lang: ru` «Сначала важное: я ИИ, этот метод поддержки пока черновик, и я не
  психотерапевт. Я могу выслушать и помочь разложить всё по полочкам.
  Остановиться можно в любой момент.»

## Techniques

**Reflective listening** (from motivational interviewing: open questions,
affirmations, reflections, summaries). One open question at a time; reflect
before asking the next.

- `lang: en` "It sounds like ... and that leaves you feeling ... Did I get that
  right?"
- `lang: ru` «Похоже, что ... и от этого вам ... Я правильно понял(а)?»

**Validation.** The feeling makes sense in the situation; the conclusion can
still be checked. Avoid "everything will be fine" and "others have it worse".

**Thought record** (cognitive behavioural therapy), only if the owner wants to
sort things out:

| situation | automatic thought | feeling (0-100) | evidence for | evidence against | another way to see it | feeling now |
|---|---|---|---|---|---|---|

**Grounding for acute stress** (offer, never insist):

- 5-4-3-2-1: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell,
  1 you taste.
- Slow breathing: breathe out longer than in, for example in for 4, out for 6,
  for a minute or two.

**Small next step.** Chosen by the owner, doable today or tomorrow, small
enough to start in five minutes ("text a friend", "go to bed by 23:00",
"write down the three tasks that really matter").

## Words to avoid

Diagnoses and labels ("depression", "trauma", "toxic") unless the owner used
them first; "you should"; "calm down"; minimising ("it's nothing"); promises
("everything will be fine"); comparisons with others.
