# Write audit hook for Claude Code

Logs every file Claude writes in the hub and checks Markdown under `raw/`, `wiki/` and `output/` with `scripts/raw_check.py`. A secret in a written file is reported back to Claude at once (exit code 2) instead of waiting for lint.

Install in a hub:

```sh
mkdir -p .claude/hooks
cp ~/Projects/wiki-kit/templates/claude-hooks/wiki-write-audit.py .claude/hooks/
cp ~/Projects/wiki-kit/templates/claude-hooks/settings.json .claude/settings.json   # merge by hand if the file exists
printf '\n.claude/audit/\n' >> .gitignore
```

If the kit is not in `~/Projects/wiki-kit`, set `WIKI_KIT_DIR` (an `env` block in `.claude/settings.json` works). Claude Code asks once whether to trust a project hook. Restart the session after installing.

Idea taken from the Claude Agent SDK cookbook, "The Chief of Staff Agent" (audit hook on `Write` and `Edit`).
