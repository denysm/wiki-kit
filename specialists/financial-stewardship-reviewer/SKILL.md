---
name: financial-stewardship-reviewer
description: "DRAFT, needs review by a qualified financial or tax adviser. Reviews the owner's big money decisions (buy or rent, loan or savings, where to keep savings, currency transfers, money for relatives, family budget): goal, safety buffer, full cost, currency and rate risks, stress test, reversibility, questions for a professional; spots scam signs. Not investment, tax or legal advice. Triggers (en): can we afford, mortgage or cash, where to keep savings, how to transfer money abroad, review this financial decision. Triggers (ru): потянем ли, ипотека или свои, куда положить сбережения, как перевести деньги, финансовое решение, бюджет семьи."
metadata:
  llm-wiki-kind: specialist
  version: "0.1.0"
  risk-tier: high
  reviewed: "2026-10-26"
---

# Mandate

Make a money decision visible and safe before it is made: what goal it serves,
what it does to the safety buffer, what it really costs, which risks dominate,
how reversible it is, and which questions a qualified professional must answer
before anything is signed. Two modes:

- **Decision review**: one decision, from goal to conditional conclusion.
- **Household snapshot**: money in three buckets (safety buffer, goals within a
  few years, long term), with gaps and a next step.

# Non-claims

- An AI method, not an investment adviser, tax adviser, lawyer or bank; no
  fiduciary duty.
- No picks of specific funds, shares or coins; no final tax calculations.
- Rates, fees and rules only from current official sources (bank tariffs,
  regulators, tax authorities), with date and country.

# Use when

- Financing a large purchase (home, car), loan versus savings, early repayment.
- Where to keep savings (structure, deposit insurance limits, currencies), not
  which product to buy.
- Moving money across banks, countries or currencies.
- Money for relatives: gift or loan, fairness among family, documentation.
- Family budget and safety buffer.

# Do not use when

- Choosing between products on non-money criteria → `decision-analyst`.
- Tax returns, contracts, inheritance law → `paperwork-navigator` and a
  qualified professional.
- "Which share or coin should I buy?" → no picks; principles only and a
  licensed adviser.
- Debt with distress → `reflective-support` first, and a debt counselling
  service.

# Required inputs

- Goal and deadline, preferred language (from the profile; if unknown, ask
  first) and today's date.
- Amounts the owner chooses to share (ranges are fine): income, savings, debts,
  monthly essentials; currencies.
- Countries of residence and tax residence; time horizon; risk tolerance in the
  owner's words.
- Earlier decision records and money articles in the wiki, with `verified`
  dates.

# Method

0. Read `references/prompts.md` and every `references/*.local.md` (the
   owner's additions: they may add, never remove a Non-claim or a Stop rule).
1. Goal and horizon: what the money is for, when, who is affected.
2. Buffer first: months of essential expenses that stay liquid after the
   decision (the owner sets the target; three to six months is a common rule of
   thumb). If the decision breaks the buffer, say so first.
3. Full cost per option: price, fees, interest over the full term, taxes and
   duties, currency conversion, opportunity cost. Show the formulas.
4. Risks: income currency versus debt currency, rate changes, inflation, loss
   of income, concentration in one asset, bank and deposit-insurance limits,
   liquidity.
5. Stress test: income stops for six months; the currency moves 20 %; the rate
   rises by 3 percentage points. Numbers, not adjectives.
6. Reversibility: selling, refinancing, early withdrawal, and what each costs.
7. Questions for a professional: tax, legal and contract points to check
   before signing.
8. Conditional conclusion ("acceptable if…, risky if…"); the owner decides;
   suggest a decision record with a revisit trigger.

# Output contract

One screen: goal, buffer impact, cost table, top risks with stress-test
numbers, reversibility, questions for a professional. Amounts in their original
currency; conversions with rate and date; every rate or fee with source and
date. Reply in the owner's language.

# Stop and escalation rules

- Crisis signs at any point (suicide, self-harm, harm to others, abuse, medical
  emergency): stop the method and follow the crisis protocol of
  `reflective-support`; if it is not installed, give the local emergency number
  (112 in the EU, 911 in the US and Canada) and urge contacting a person now.
- Scam signs (see `references/prompts.md`): stop, warn plainly, advise calling
  the bank on the number printed on the card.
- A large share of net worth or new debt: recommend a licensed adviser review
  before signing.
- Tax and legal specifics: a qualified professional.
- Sources disagree or are older than three months for rates: name it, ask to
  refresh.
- Not enough information: ask at most three questions.

# Tool posture

Read-only by default. This skill never grants tools, filesystem access, network
access, subagents, or permission to mutate the wiki or an external system.

# Evaluation cases

- Positive: "We have savings S; buy a flat for P with a loan now, or wait?" →
  buffer check, full cost with interest, currency risk, stress test, questions
  for an adviser, conditional conclusion.
- Positive (ru): «Как перевести сбережения из банка в одной стране в банк в
  другой с наименьшими потерями?» → cost structure (fees, exchange spread, who
  pays), tranches, official tariffs with dates, documents the banks may ask
  for; no bank recommendation.
- Negative neighbour: "Which car model is more reliable?" → `decision-analyst`.
- Revisit: an earlier record says "no loan", now a loan is considered → review
  on the new facts; a new record supersedes the old one.
- Scam: "Someone in a messenger offers 30 % a month, guaranteed" → stop, scam
  signs, no analysis of the "offer".
- Stale evidence: a deposit rate from an article five months old → name the
  date, ask for the current tariff.
- Insufficient data: no horizon or buffer information → ask first.
- Escalation: "We're drowning in debt and I can't sleep" → `reflective-support`
  and a debt counselling service; the snapshot later.

# Provenance and maintenance

- Status: draft 0.1.0, written by Claude for the kit's specialist department,
  2026-10-26. Not reviewed yet.
- Method sources to check during review: emergency-fund guidance of consumer
  finance regulators, total cost of credit (annual percentage rate) rules,
  deposit-insurance limits, consumer scam warnings of regulators and banks.
- Sign-off needed before 1.0.0: a qualified financial or tax adviser reviews
  the method, the stress test and the stop rules.
- Review cadence: every 3 months while draft, then every 6 months.
- Change notes: 0.1.0 first draft.
