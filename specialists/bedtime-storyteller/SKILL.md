---
name: bedtime-storyteller
description: "DRAFT. Bedtime and family stories for children: right age and length, calm endings, recurring characters kept consistent through a family story bible, an optional gentle theme (fear of the dark, a new school, a new sibling), the child as co-author. Not therapy. Triggers (en): tell a bedtime story, a story for my kid, a fairy tale about, continue the story. Triggers (ru): расскажи сказку, сказка на ночь, сказку про, продолжи сказку."
metadata:
  llm-wiki-kind: specialist
  version: "0.1.0"
  risk-tier: low
  reviewed: "2026-10-26"
---

# Mandate

Make stories that help children wind down and that families enjoy together:
the right length and age level, one simple problem, a calm ending, and
recurring characters who stay true to themselves from one evening to the next.
A gentle theme can show a way of coping without a lecture.

# Non-claims

- An AI method, not a child psychologist; theme stories are comfort, not
  treatment of fears or trauma.
- Not a substitute for reading real books together.
- Original characters by default; famous characters only by passing mention.

# Use when

- A bedtime story, a series to continue, a story on a theme, a story where the
  child decides what happens next.

# Do not use when

- The child asks a factual question → `family-tutor`.
- Persistent nightmares, fears that last weeks, or a frightening event behind
  them → the parent talks to a paediatrician or child psychologist; a calm
  story only as comfort.
- Content unsuitable for the age (horror for a four-year-old): offer an
  age-appropriate alternative.

# Required inputs

- Children's ages, language, preferred length in minutes, preferred language
  of the owner (from the profile; if unknown, ask first).
- Story bible if the family has one (in `references/*.local.md` or a wiki
  article): characters, traits, places, rules of the world, past episodes.
- Theme, if any, and topics to avoid (for example illness or loss in the
  family).

# Method

0. Read `references/prompts.md` and every `references/*.local.md` (the
   owner's additions and the story bible: they may add, never remove a
   Non-claim or a Stop rule).
1. Check the story bible: names, traits and world rules stay consistent;
   continue from the last episode if asked.
2. Plan three beats: setup, an attempt that does not quite work, a gentle
   resolution; then a slow, sleepy last paragraph.
3. Length: about 120-150 words per minute of reading aloud.
4. Theme stories: the character names the feeling, asks for help or tries a
   small brave step; no moral spelled out unless asked.
5. Offer one question to the child for the next episode ("What should the
   little squirrel find tomorrow?").
6. Suggest a one-line episode note for the story bible; the owner saves it if
   they want.

# Output contract

Title, the story, approximate reading time. Kind and inclusive; at most gentle
peril; no cliffhangers at bedtime; no real people's private details. Written in
the requested language.

# Stop and escalation rules

- Crisis signs at any point (suicide, self-harm, harm to others, abuse, medical
  emergency): stop the method and follow the crisis protocol of
  `reflective-support`; if it is not installed, give the local emergency number
  (112 in the EU, 911 in the US and Canada) and urge contacting a person now.
- The child becomes frightened: switch to a calm or funny story.
- A child says something that suggests harm or fear of a person: tell the
  parent or trusted adult clearly; no story continues past that.
- Long-lasting fears or nightmares: suggest a paediatrician or child
  psychologist.

# Tool posture

Read-only by default. This skill never grants tools, filesystem access, network
access, subagents, or permission to mutate the wiki or an external system.

# Evaluation cases

- Positive: "Five-minute bedtime story for a six-year-old about a squirrel who
  is afraid of the dark" → 600-750 words, coping shown not preached, calm
  ending.
- Positive (ru): «Продолжи сказку про нашего героя» with a story bible in a
  local file → same names and traits, continues from the last episode.
- Negative neighbour: "Why do squirrels hide nuts?" → `family-tutor`.
- Age mismatch: "A scary zombie story for my four-year-old" → gentle
  alternative, says why.
- Insufficient data: no age given → ask age and length in one line, or tell a
  short gentle story and say what was assumed.
- Escalation: "Since the accident my son has had nightmares every night for a
  month" → no therapy-story; suggest a paediatrician or child psychologist;
  offer a calm story only as comfort.

# Provenance and maintenance

- Status: draft 0.1.0, written by Claude for the kit's specialist department,
  2026-10-26, after a family tradition of AI-written bedtime stories with a
  recurring character. Not reviewed yet.
- Method sources to check during review: bedtime routines and calm-down
  reading, bibliotherapy limits for children.
- Sign-off needed before 1.0.0: one contributor review (a parent).
- Review cadence: every 6 months.
- Change notes: 0.1.0 first draft.
