# Contributing to wiki-kit

Thank you for helping. The kit is a method, not data: every change must make sense to a stranger and must not carry anything about you, your family, your employer or your clients.

Step-by-step instructions in plain language: [English](docs/QUICKSTART.md#share-your-improvements), [по-русски](docs/QUICKSTART.ru.md#как-поделиться-улучшениями), [українською](docs/QUICKSTART.uk.md#як-поділитися-покращеннями). Write issues and pull requests in English, Ukrainian or Russian.

## What is welcome

- **Fixes.** A quickstart step that did not work, a script error, an installer `FAIL` (paste the `FAIL` lines; read a log for names before you attach it).
- **Clearer wording and translations.** Add a language next to the existing ones; do not replace an original ([specialists/README.md](specialists/README.md#languages)).
- **Lessons for specialists.** A de-identified principle plus at least one evaluation case ([specialists/README.md](specialists/README.md#from-personal-lesson-to-shared-principle)).
- **New specialists.** Take a vacancy or start from `templates/specialist/` ([specialists/README.md](specialists/README.md#proposing-a-new-specialist)).
- **Scripts.** Standard-library Python 3.9+, usage in `--help` or the docstring, run with `python3 -I`.

Not sure whether an idea fits? Open an issue first.

## Once, before your first pull request

1. A GitHub account, with **Keep my email addresses private** turned on at <https://github.com/settings/emails>.
2. In the kit folder, set your name (a nickname is fine) and the `@users.noreply.github.com` address from that page: `git config user.name ...`, `git config user.email ...`. Only this address goes into the public history.
3. The GitHub command line tool (<https://cli.github.com>), signed in with `gh auth login`.
4. Your private names in `~/.config/wiki-kit/private-names.txt`, one per line. The pre-push hook (`hooks/pre-push`, turned on by the installer: `git config core.hooksPath` prints `hooks`) runs `scripts/leak_check.py` with that list and refuses a push that matches it or carries secrets.

## Sending a change

Ask Claude Code "send my changes to the kit as a pull request", or by hand:

```sh
gh repo fork --remote            # once: your fork becomes origin, the kit becomes upstream
git switch -c short-change-name
git add -A
git commit -m "What changed and why"
git push -u origin HEAD
gh pr create --fill              # base: the original kit
```

One topic per pull request. Changing a specialist: bump its `version` and add a change note. Changing a quickstart: say in the pull request if the other languages still need the same change.

## What happens next

- The `checks` workflow runs on the pull request: scripts compile on Python 3.9 and 3.13, a leak check over the history (without anyone's private names list), shell syntax, no symlinks. For a first-time contributor the maintainer starts the run by hand.
- The maintainer reviews and may ask questions in the pull request. Changes to Non-claims, Stop and escalation rules, or a `risk-tier: high` specialist also need the safety reviewer.
- By sending a pull request you agree that your contribution is published under this repository's [MIT licence](LICENSE).

## Never send

- Anything from your wiki: `topics/`, `raw/`, `inbox/`, articles, chats, exports.
- `*.local.md` files and the lists in `~/.config/wiki-kit/`.
- Names, employers, clients, figures, places, health details, passwords, keys, internal addresses.

If something private reached GitHub anyway, tell the maintainer privately, not in a public issue, and change any exposed password or key at once. A public commit can be copied within minutes, so deleting it later is not enough.
