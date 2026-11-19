# Personal rules for all projects

## Keep the user informed while you work

- Before a task of more than two or three steps, print a short numbered plan, one line per step, then start.
- Before each step, write one short line: what you are about to do and why (which script or command, which file, what you are checking or deciding).
- After each step, write one line with the result: done, found, failed, and what comes next. When the plan changes, say so in one line.
- Never work silently for long. During long work (an agent, a big script, a series of tool calls) post a short update at least every few tool calls.
- Keep updates to one or two lines, in the user's language. The final answer does not repeat them: it gives the result and what is left.
- For background agents, say when one starts and what it does, and report when it finishes.

## Suggest skills and plugins when they pay off

- When a task would clearly go better with a skill or plugin that is not installed or not enabled here (for example Superpowers from the Anthropic plugin directory for TDD, systematic debugging or executing a written plan in a code repository), suggest it in one line: what it is, why it helps this task, scope (project or user) and the effect on context cost.
- Suggest a thing once per session, and do not suggest what an installed skill already covers (for wiki work, llm-wiki has ingest, compile, plan and research).
- Prefer project scope for plugins that load context into every session, such as Superpowers, so other projects do not pay for it.
- Never install or enable a skill or plugin without the user's yes.

## Point work to the tool that does it best

- Before a task that computes on scientific data, runs scientific models, queries public biology or chemistry databases, reviews literature on full text, or reads a lot of biology, read the tool-routing table of your wiki if it has one (an article named `tool-routing-guide.md`).
- When another tool fits better (Claude Science, claude.ai chat, Cowork), say so in one or two lines before starting: which tool, why, and how the result comes back. Then do here what Claude Code does well. Do not refuse or stall; the user decides.
- Flag the reverse too: reading and summarizing planned for Claude Science is cheaper in Claude Code with Sonnet agents or scripts.
- Flag once per task.
