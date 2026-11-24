# Sources, access and the yearly checklist (Kazakhstan)

Facts here carry the date they were checked; check them again before relying
on them. Figures (МРП, МЗП, rates, thresholds) are deliberately not listed:
they are fetched for the period of each question.

## Source hierarchy

1. Acts on **adilet.zan.kz** (Әділет, the official legal database): the Tax
   Code, the accounting law, the yearly budget law, the Social Code and other
   laws, orders of the Ministry of Finance (tax forms and rules, the national
   financial reporting standard).
2. **kgd.gov.kz** (State Revenue Committee, КГД): explanations, the tax
   calendar, forms with instructions, notices of changes.
3. **egov.kz**: procedures and services (registration, notifications, digital
   signature). It describes a procedure; it is not a source of tax law.
4. Everything else (accounting portals, blogs, forums, chat answers, an
   accountant's word): leads only. Find the act before citing it.

## Access notes (checked 2026-11-23)

- adilet.zan.kz serves a JavaScript application: a plain HTTP fetch returns a
  page of about 1.5 KB without the text of the act. The full text comes as
  HTML from `https://old.adilet.zan.kz/rus/docs/<ID>`. Give the owner the
  link `https://adilet.zan.kz/rus/docs/<ID>`; it opens in a browser.
- Document IDs:
  - Tax Code of 18.07.2025 No. 214-VIII: `K2500000214`, status in force;
    the text already carries 2026 amendments (for example Law No. 308-VIII).
  - Former Tax Code of 25.12.2017 No. 120-VI: `K1700000120`, lapsed
    (replaced by the 2025 Code).
  - Law of 28.02.2007 No. 234 «О бухгалтерском учете и финансовой
    отчетности»: `Z070000234_`.
- kgd.gov.kz opens with a plain fetch.
- The Code's page is about 5 MB of HTML: search it for the article instead of
  reading it whole.

## Special tax regimes in the 2025 Code (checked 2026-11-23)

Section 16 «Специальные налоговые режимы»: chapter 76, general provisions
(article 715 lists the regimes a taxpayer may choose); chapter 77, for the
self-employed (article 718); chapter 78, based on the simplified declaration
(article 722); chapter 79, for peasant or farm households (article 728).
Chapters 80 and later deal with tax preferences (special economic zones,
investment contracts, Astana Hub), not regimes. Who qualifies, limits, rates
and periods: read the current edition of these articles.

## Yearly parameters: check for the period, never from memory

| parameter | where it is set |
|---|---|
| МРП, МЗП | the law on the republican budget for that year |
| ИПН, КПН, НДС and social tax rates; VAT registration threshold | the Tax Code (some rates change by year inside the Code itself) |
| ОПВ, ОПВР, СО | the Social Code |
| ВОСМС, ООСМС | the law on compulsory social health insurance |
| special regimes: who qualifies, limits, rates | Tax Code section 16; local decisions only where the Code allows them |
| returns (ФНО) and deadlines | the Tax Code article of each tax; Ministry of Finance orders on forms; the КГД calendar |
| penalties and late-payment interest | the Code of Administrative Offences; the Tax Code |

## What to ask (when it changes the answer)

| question | why it matters |
|---|---|
| individual, ИП or company (ТОО, other)? | different taxes, payments and returns |
| tax resident of Kazakhstan? | worldwide or Kazakhstan-source income |
| regime: general or which special one? | rates, limits, returns |
| income or turnover for the period; type of activity | rate, limits, VAT threshold, eligibility for a regime |
| employees: how many, payroll | withheld ИПН, social payments, payroll returns |
| VAT-registered? | VAT returns and invoices |
| period and as-of date | which edition and which year's figures |

## Answer template

```
Kazakhstan · as of <date> · period <...> · <person>, <regime>
Short answer: <amount, due date>
Facts: <norm> (<act>, art. <n>, p. <n>; <link>)
Calculation: <base> → <deductions> → <rate> → <amount>
Deadlines and sums: | what | period | due date | amount | where |
Risks and whom to check with: <...>
What to do next: 1) ... 2) ...
```
