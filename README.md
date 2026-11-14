# wiki-kit

Tools and rules for running a personal knowledge wiki on the [nvk/llm-wiki](https://github.com/nvk/llm-wiki) plugin with an AI coding assistant. The kit contains **no data**: only the method.

Status: draft. Merged from two working copies (work and home). The installers are tested on clean Ubuntu and Windows machines in CI (`.github/workflows/installers.yml`) and on macOS with an empty home folder; not yet by a real new user.

**New here?** Follow [docs/QUICKSTART.md](docs/QUICKSTART.md) ([по-русски](docs/QUICKSTART.ru.md), [українською](docs/QUICKSTART.uk.md)): VS Code, Claude Code, then `bash bootstrap.sh` (Windows: `bootstrap.ps1`).

**Want to improve it?** Send a pull request: [CONTRIBUTING.md](CONTRIBUTING.md).

| Folder | What it is |
|---|---|
| `bootstrap.ps1` | The same for Windows 10/11; also installs Git, Python and Claude Code if missing (asks first); log in `%TEMP%\wiki-kit-bootstrap.log`. Tested in CI on a clean Windows machine (Windows PowerShell 5.1) |
| `bootstrap.sh` | Installer for macOS and Linux: plugin pinned to v1.0.0, empty hub, private lists, specialists, front desk, self-check; safe to re-run |
| `docs/QUICKSTART.md`, `docs/QUICKSTART.ru.md`, `docs/QUICKSTART.uk.md` | Plain-language install, first steps and how to send improvements, in English, Russian and Ukrainian |
| `CONTRIBUTING.md`, `.github/pull_request_template.md` | How to send a change by pull request, and the privacy checklist every pull request starts with |
| `.github/workflows/` | CI: `checks` on every push (scripts compile on Python 3.9 and 3.13, leak check over the whole history without the private names list, shell syntax, no symlinks); `installers` runs both installers twice on clean Ubuntu and Windows and checks that the pre-push hook blocks a fake key |
| `docs/PROJECT-CONTEXT.md` | Goals, key decisions and roadmap of this project (read first) |
| `docs/ai-tooling-for-throwaway-pocs.md` | Choosing AI delivery tooling for throwaway PoCs: four layers, verdict template, when to run what |
| `docs/testing-specialists.md` | How to test a specialist against the no-specialist baseline before 1.0 |
| `docs/llm-wiki-portable-playbook.md` | The method in full: layout, frontmatter, ADRs, confidentiality, cost, quality gates, cold start |
| `templates/hub-CLAUDE.md` | Starting rules for a new hub (fill in the `{...}` placeholders) |
| `templates/specialist/` | Skeleton for a new specialist with the department rules built in |
| `agents/` | `wiki-reader` (read-only digests) and `wiki-compiler` (ingest + compile one topic), plus the shared `COMMON.md` |
| `scripts/` | Python helpers, listed below; standard library only, except numpy for `search.py` (`search.py install-deps`, run by the installers) |
| `specialists/` | The specialist department: 11 specialists in five divisions (growth, wellbeing, family, money and documents, thinking tools); staff, rules and vacancies in `specialists/README.md` |
| `skills/department/` | Claude Code skill: the front desk that asks your language, picks a specialist by a plain phrase ("coach", "мне тяжело") and hands over between them |
| `skills/foreman/` | Claude Code skill: the foreman for work that needs a team ("assemble a team", "наряд"): recalls past work orders and lessons first (`search.py recall`), work order, staffing table with measured cost estimates (`scripts/roster.py`), hires only after your yes, quality control, acceptance, lessons, and an order record in the topic's `output/work-orders/` for the next recall |

## Specialist department

1. Copy the specialists into your hub and enable each for a topic (suggested topics are in the Staff table of `specialists/README.md`):
   ```sh
   python3 -I scripts/sync_specialists.py ~/wiki   # copies (the validator refuses symlinks); keeps your *.local.md
   git config core.hooksPath hooks                 # re-sync after every commit, pull and checkout of the kit
   llm-wiki specialist validate
   llm-wiki specialist enable development-coach --wiki career          # repeat for each specialist and topic you want
   llm-wiki specialist refresh
   ```
2. For the coach, fill `specialists/development-coach/references/foundations-template.md` as an article in its topic (North Star, barrier map, goals log). Without it the coach still works, but treats barriers as generic hypotheses.
3. Optional: `ln -s "$PWD/skills/department" ~/.claude/skills/` so that a plain phrase works from any folder (a symlink also lets it refresh the hub copy before each call). On the first conversation it asks your language.

Everything except `development-coach` is a draft (0.x) and says so to the user. The high-risk ones (`reflective-support`, `health-navigator`, `financial-stewardship-reviewer`, `paperwork-navigator`) reach 1.0 only after review by a qualified person.

Triggers and phrasing start in English and Russian; any language can be added. Your own tuning goes into `references/*.local.md`; how shared improvements come back to the kit is in [specialists/README.md](specialists/README.md).

## Scripts

Every script prints its usage with `--help` (or in its docstring). Run them with `python3 -I`.

| Stage | Scripts |
|---|---|
| Find and sort sources | `inventory.py` (one row per candidate, topic guess, duplicates, secret count), `review_report.py`, `deep_candidates.py`, `digest.py`, `chat_tasks.py` |
| Convert to Markdown raw sources | `chat2md.py` (Claude and ChatGPT exports), `cowork2md.py`, `doc2md.py`, `xlsx2md.py`, `mail2md.py`, `vtt2md.py`, `drawiopng2md.py`, `plotlyhtml2md.py`, `pdf2txt.swift` (macOS PDFKit) |
| Stage and ingest | `stage.py`, `extra2md.py`, `ingest.py`, `move_tree.py`, `scaffold_wiki.py`, `sync_specialists.py` (kit specialists into a hub's `.skills/`) |
| Check | `leak_check.py` (the pre-push leak check, below), `raw_check.py` (secrets, internal hosts, infrastructure ids; `--fix` redacts; `--wiki` adds raw frontmatter and `*.local.md` rules), `check_evidence.py` (numbers, dates and quotes appear in cited sources; links; coverage), `wikicheck.py` (article frontmatter, See Also back-links, staleness; `--suggest N` lists See Also candidates from shared links), `reindex.py`, `decisions_scan.py`, `extract_code.py` |
| Second opinion from other models | `council.py` (several models, blind judge, verify, cost ledger, learned routing), `verify_articles.py` (claim-by-claim check of articles by a model from another family), `model_bench.py`, `bench_weighted.py`, `council_prices.json` |
| Find | `search.py` (SQLite FTS5 search over `raw/`, `wiki/`, `output/` of a wiki root: `index`, `query` (`--also` adds a translation of the question for sources in another language), `recall` (past work orders, lessons and material on a task), `langs`, `eval`, `embed-check`; optional search by meaning through a local embedding server; the index is a local cache) |
| Guard | `wiki_write_audit.py` (Claude Code hook for `Write\|Edit`, installed once in `~/.claude/settings.json`: logs writes inside wiki roots, runs the `raw_check.py` rules at once and returns exit 2 on a secret; does nothing outside a wiki; usage in its docstring) |
| Cost and staffing | `claude_usage.py` (Claude Code spend from local logs; `brief` for a per-answer line; `agents` for cost per subagent run by type and model), `roster.py` (who the foreman can hire: specialists, agents, built-ins, outside vendors, vacancies, hire log, measured cost per run; `--json`) |

`council.py` and `verify_articles.py` call outside model vendors. They refuse to send data from private topics (default: `work`) or text with secret hits, unless told otherwise.

## Local configuration (never committed)

Lists that name your organisation, your family or your clients are themselves the leak, so they stay outside the repository:

| File or variable | Used by |
|---|---|
| `~/.config/wiki-kit/internal-domains.txt` | `raw_check.py`: one host suffix per line (or `re:<regex>`); flagged and redacted as internal |
| `~/.config/wiki-kit/private-names.txt` | the leak check before every push: one case-insensitive regex per line (`grep -iEf`) |
| `~/.local/share/wiki-kit/python<X.Y>/` | Packages the kit needs (numpy), one folder per Python version, put there by `search.py install-deps` when that Python lacks them (Windows: `%LOCALAPPDATA%\wiki-kit\`). Scripts run with `python3 -I`, which ignores `pip install --user` |
| `~/.cache/wiki-kit/search/` | `search.py`: one SQLite index per wiki root, rebuilt on demand (it holds the text of `*.local.md` files and their vectors, so it never goes into a repository) |
| `~/.config/wiki-kit/search.json` | `search.py`: optional local embedding server (`url`, `model`, `query` and `document` prompts, `dims`); without it search uses words only. The server must run on your machine: chunk text is sent to it |
| `~/.cache/wiki-kit/audit/writes.jsonl` | `wiki_write_audit.py`: one line per write inside a wiki root |
| `~/.config/wiki-kit/search-eval.tsv` | `search.py eval`: your question set (`question`, `root`, `expected file`, alternatives joined by `\|`; questions about real content stay out of the kit); `--variants FILE` adds other phrasings of each question |
| `~/.config/wiki-kit/inventory.json` | `inventory.py` and `deep_candidates.py`: your own topic rules (`career`, `buckets`, `prepared`, `waves`); without it, generic defaults apply |
| `~/.config/llm-wiki/council.env` | API keys for `council.py` (KEY=value, chmod 600) |
| `~/.config/wiki-kit/specialists-hub` | `sync_specialists.py`, the kit's hooks, the `department` skill and the installers (unless given `--hub`): the hub that gets the specialists, when it is not the llm-wiki hub (one line, a path) |
| `~/.config/wiki-kit/foreman/hires.tsv` | `roster.py --log-hire`: the foreman's hire log (date, generic role, kind, model, outcome, cost); a temporary role hired twice becomes a vacancy candidate |
| `~/.config/wiki-kit/profile.json` | the `department` skill: your preferred language (`{"language": "ru"}`), saved with your consent on the first conversation |
| `WIKI_KIT_AUTHOR` | your name for the `authors:` field written by `chat2md.py` |
| `WIKI_KIT_SOURCES` | root of your originals for `stage.py` / `extra2md.py` (default `~/Projects/private-sources`) |

Paths in the agents assume the kit at `~/Projects/wiki-kit` and the hub at `~/wiki`; change them if yours differ.

## Leak check before a push

`git config core.hooksPath hooks` (done by `bootstrap.sh`) turns on `hooks/pre-push`, which runs `scripts/leak_check.py` and refuses the push on any finding:

- paths that hold data: `topics/`, `raw/`, `inbox/`, `*.local.md`;
- names from `~/.config/wiki-kit/private-names.txt` (in file contents and file names);
- secrets, internal hosts and infrastructure ids (the `raw_check.py` rules and your `internal-domains.txt`).

It checks the committed tree and every line added by the commits the remote does not have yet, so a leak removed by a later commit is still caught (it would travel in history). Values are never printed. Known false positives in code are listed in `.leak-allow` (`path kind count`; the count must match exactly); names and data paths cannot be allowed (only the `Copyright (c)` line of `LICENSE` may name its holder). Run it by hand with `python3 -I scripts/leak_check.py --history --base origin/main`. Bypass only in an emergency: `git push --no-verify`.

## Not included yet

A run by a real new user (the first one uses Windows), the winget install of Git and Python in `bootstrap.ps1` (CI machines already have both), screenshots in the quickstart, a test on a clean user account or VM, and a verified list of models other than Claude that can run the agents. `drawiopng2md.py` needs `atlassian_export.py`, which is not in the kit; `xlsx2md.py` and `drawiopng2md.py` need extra packages (`uv run --with ...`, see their docstrings).

## Licence

[MIT](LICENSE): use, change and share the kit freely; keep the copyright notice. It comes as is, without warranty.

The kit is a method, not advice. Every specialist except the coach is a draft (0.x); the health, money, paperwork and emotional-support specialists help you prepare and do not replace a doctor, adviser, lawyer or therapist.
