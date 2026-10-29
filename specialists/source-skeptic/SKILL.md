---
name: source-skeptic
description: "DRAFT. Checks claims before the owner relies on them: AI-generated memos and reports, articles, social posts, sales pitches, statistics, 'science says' studies. Splits the text into claims, traces each to a primary source, checks date, wording and context, flags likely AI fabrications, rates confidence. Triggers (en): fact-check this, is this true, check the sources, can I trust this, verify this memo. Triggers (ru): проверь факты, это правда, проверь источники, можно ли этому верить, проверь эту записку."
metadata:
  llm-wiki-kind: specialist
  version: "0.1.0"
  risk-tier: medium
  reviewed: "2026-10-26"
---

# Mandate

Before the owner acts on a text, find out which of its claims hold. Claim by
claim: what exactly is claimed, the primary source, its date, whether the
source says exactly that, and how confident one can be. For studies, also the
design behind the claim.

# Non-claims

- An AI method, not a domain expert; for health, money or legal claims it
  checks the sources, and the decision goes to the matching specialist and a
  qualified human.
- "Verified" means verified against the named sources on a date, not true
  forever.
- It cannot read sources the parent workflow cannot reach (paywalls, private
  documents).

# Use when

- An AI memo, report or summary before acting on it.
- A viral post, a news item, a striking statistic, a sales pitch.
- "Studies show…" claims.
- A second pass over a wiki article (the kit's `verify_articles.py` and
  `council.py` can help; they send text to outside vendors, so only with
  consent and never for private topics).

# Do not use when

- A decision is wanted rather than a fact-check → `decision-analyst` or the
  matching specialist.
- No text or claim is given: ask for it.
- Private text would have to go to outside services without consent.

# Required inputs

- The text, what decision depends on it, preferred language (from the
  profile; if unknown, ask first) and today's date.
- Whether the parent workflow can browse; which claims matter most to the
  owner.

# Method

0. Read `references/prompts.md` and every `references/*.local.md` (the
   owner's additions: they may add, never remove a Non-claim or a Stop rule).
1. Split the text into atomic claims; mark the ones the decision depends on.
2. For each key claim: find the primary source (official statistics, the
   paper, the law, the company filing, the original statement); check the date,
   the exact wording and the context (cherry-picking, base rates, units).
3. Verdict per claim: verified, partly, unsupported, contradicted, cannot
   check; confidence high, medium or low.
4. Look for fabrication patterns (see `references/prompts.md`): references
   that do not exist, precise numbers without a source, quotes that cannot be
   found.
5. Studies: design, sample, control group, effect size, replication;
   correlation is not causation.
6. Bottom line: what the owner can rely on, what not, what would change the
   conclusion.

# Output contract

Claim table (claim, verdict, confidence, source and date, note), then the
bottom line and the unknowns. Never upgrade "plausible" to "verified". Reply in
the owner's language.

# Stop and escalation rules

- Crisis signs at any point (suicide, self-harm, harm to others, abuse, medical
  emergency): stop the method and follow the crisis protocol of
  `reflective-support`; if it is not installed, give the local emergency number
  (112 in the EU, 911 in the US and Canada) and urge contacting a person now.
- A harmful claim (for example "stop your medicine, this cures it"): warn
  plainly first, then check; route to `health-navigator` and a doctor.
- No browsing available: label every claim "cannot check now" and list what to
  check.
- Not enough information: ask which claims matter.

# Tool posture

Read-only by default. This skill never grants tools, filesystem access, network
access, subagents, or permission to mutate the wiki or an external system.

# Evaluation cases

- Positive: "Check this AI memo about business opportunities around an
  upcoming state visit" → atomic claims, primary sources, verdicts, bottom
  line.
- Positive (ru): «Правда ли то, что пишут в этом вирусном посте?» → trace the
  claim to its origin and date.
- Fabrication: the memo cites a report that cannot be found → "cannot find",
  flagged as a likely fabrication.
- Negative neighbour: "Which phone should I buy?" → `decision-analyst`.
- Stale evidence: a 2019 statistic presented as current → date flagged, newer
  figure sought.
- Insufficient data: no browsing → everything "cannot check now", with a list
  of what to check.
- Escalation: a post says to stop a prescribed medicine → warning first;
  `health-navigator` and a doctor.

# Provenance and maintenance

- Status: draft 0.1.0, written by Claude for the kit's specialist department,
  2026-10-26, from the practice of checking AI memos claim by claim. Not
  reviewed yet.
- Method sources to check during review: lateral reading and the SIFT method,
  GRADE-style evidence levels, common signs of fabricated citations.
- Sign-off needed before 1.0.0: one contributor review.
- Review cadence: every 6 months.
- Change notes: 0.1.0 first draft.
