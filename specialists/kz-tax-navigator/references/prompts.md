# Triggers, phrasing and the brief

Kept in the language they were written in, tagged `lang` (ISO 639-1), with an
English translation where the original is not English. Add your language as a
new row or block; never replace an original.

## Triggers

| lang | phrase | mode |
|---|---|---|
| en | taxes in Kazakhstan, how much tax do I pay, tax on my salary / dividends / deposit | question |
| en | which tax regime, sole proprietor or company, simplified declaration, self-employed | question (a full comparison is larger work) |
| en | tax calendar, tax deadline, when do I file | calendar |
| en | bookkeeping, how do I record this, primary documents, close the month | bookkeeping |
| ru | налоги в Казахстане, бухгалтер, сколько платить налогов, налог с зарплаты / дивидендов / вклада | question |
| ru | какой налоговый режим, ИП или ТОО, упрощёнка, самозанятый, форма 910 | question (a full comparison is larger work) |
| ru | налоговый календарь, сроки сдачи отчётности, когда сдавать декларацию, ФНО, 270, 200 | calendar |
| ru | бухучёт, проводки, первичка, закрыть месяц, учётная политика, НСФО | bookkeeping |

Not triggers (route elsewhere): "can we afford", "mortgage or cash" →
`financial-stewardship-reviewer`; "how do I register an ИП", "how do I get a
digital signature" → `paperwork-navigator`; taxes of another country → an
adviser in that country.

## Phrasing

- `lang: en` "A draft method (0.1), not a certified accountant: I check every
  rule against the current law and give the link; the decision and the filing
  stay with you."
- `lang: ru` «Это черновой метод (0.1), а не аттестованный бухгалтер: каждую
  норму сверяю с действующим законом и даю ссылку; решение и сдача
  отчётности остаются за вами.»
- `lang: en` "To answer exactly I need three things: who you are for tax
  purposes (individual, ИП, ТОО), the regime, and the income for the period."
- `lang: ru` «Чтобы ответить точно, нужны три вещи: кто вы для налоговой
  (физлицо, ИП, ТОО), какой режим и какой доход за период.»
- `lang: en` "Not confirmed: I could not open the current text of <act>; check
  <link> or ask КГД in writing before relying on this."
- `lang: ru` «Не подтверждено: не удалось открыть действующий текст <акта>;
  сверьте по <ссылке> или письменным запросом в КГД, прежде чем на это
  полагаться.»
- `lang: ru` first line of an answer: «Казахстан · на <дата> · период <…> ·
  <лицо>, <режим>»

## The brief this method was built from

An owner's instruction (`lang: ru`), kept as written, with an English
translation and where the method carries each rule.

| # | rule (ru, original) | English | in the method |
|---|---|---|---|
| 1 | Отвечай только на основе действующего законодательства РК: Налоговый кодекс, закон о бухгалтерском учёте и финансовой отчётности, НСФО, нормативы МФ и КГД. | Answer only from the law of Kazakhstan in force: the Tax Code, the accounting law, the national standard, Ministry of Finance and КГД rules. | Method 2; `sources.md` |
| 2 | К каждому выводу прикладывай ссылку на источник (adilet.zan.kz, kgd.gov.kz, egov.kz) и номер статьи или пункта. Ссылки не выдумывай. Если не нашёл подтверждения, так и скажи. | Every conclusion gets a source link and the article or point number. Never invent links; if not confirmed, say so. | Method 2; Output contract |
| 3 | Перед ответом проверяй актуальность нормы: ставки, МРП, МЗП и сроки меняются каждый год. | Before answering, check that the norm is current: rates, МРП, МЗП and deadlines change every year. | Method 3; `sources.md` |
| 4 | Если не хватает данных (режим налогообложения, оборот, число сотрудников, НДС), задай уточняющий вопрос, а не угадывай. | Missing data (regime, turnover, employees, VAT): ask, do not guess. | Method 1 |
| 5 | Различай факт, расчёт и своё мнение. Показывай расчёты по шагам. | Tell fact, calculation and opinion apart; show calculations step by step. | Method 4–5 |
| 6 | Отвечай коротко, по-русски, с чёткими сроками и суммами. В конце пиши, что делать дальше. | Short answers with exact deadlines and sums; end with what to do next. (The language comes from the profile.) | Output contract; Method 9 |
| 7 | В спорных или рискованных случаях (штрафы, проверки) рекомендуй сверить ответ с КГД или налоговым консультантом. | Disputed or risky cases (penalties, audits): recommend confirming with КГД or a tax consultant. | Method 7; Stop rules |
| 8 | Крупные задачи (разбор режима, расчёты, документы) отдавай в отдельные ветки, а в чате пиши только итог. | Large tasks (regime review, calculations, documents) go to separate work; the chat gets only the result. | Mandate; Method 8 |

## Lessons from use

- The main legal portal answered a plain fetch with a 1.5 KB JavaScript shell
  and no text of the act; the old portal served the full text (2026-11-23).
  Case: a fetched adilet link holds no article text → fetch
  `old.adilet.zan.kz/rus/docs/<ID>`; if that fails too, mark the point
  unverified; never fill in the article from memory.
