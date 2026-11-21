# Catalog Card Standard

This standard defines the quality bar for one card in the kit's tool catalog (`catalog/wiki/references/<owner>-<repo>.md`) before it is committed. The design behind it is [catalog-design.md](catalog-design.md).

## Core Principle

A card passes if an agent that has never seen the tool, the owner or the owner's private wiki can, from the card alone, tell which of its tasks the tool serves, which part to open, how to run that part on this machine without installing anything, how far each part was checked, and when to look again; and if every checked claim leads to a file in `catalog/raw/`.

## The Evidence Rule

A card fails if any claim reads as checked without being checked. Every part row carries a status; every number, date, version and quoted phrase in the body appears word for word in a raw file the card cites (`check_evidence.py --strict catalog` passes); and a status beyond `candidate` (`tried`, `in use`, `method taken`, `reference`, `rejected`) is backed by a desk check, trial or use record that states it. Anything written from memory is either removed or marked as not checked.

## The Public-Kit Rule

The kit is public. A card fails if it names, or lets a reader infer, a project, person, customer, employer or ticket, or carries an internal host or a private path. Trials and measurements are retold by kind of task. `leak_check.py` passing is necessary, not sufficient: it knows only the names it is given.

## Required Sections

A reviewer answers each question yes or no. Any "no" is a finding.

### Frontmatter

1. Are the plugin's article fields present (`title`, `category: reference`, `sources`, `created`, `updated`, `tags`, `confidence`, `volatility`, `verified`, `summary`)?
2. Is `areas:` a list of area slugs from `catalog/schema.md`, at least one?
3. Is `kind` one of `plugin`, `skill-collection`, `library`, `app`, `cli`, `model`, `runtime`, `pattern`?
4. Is there `repo:` (GitHub `owner/name`) or, for a tool not on GitHub, `url:`?
5. Is `version` quoted, and equal to the version the cited desk check read?
6. Is `licence` given, read from the licence file when GitHub cannot detect it?
7. Does every path in `sources:` exist and appear in `## Sources`, and the other way round?

### Abstract

8. Does one short paragraph say what the tool is, its kind, licence and the version read?

### Tasks it serves

9. Is this the first section after the abstract?
10. Is each task written as an agent would arrive with it ("turn a recording into a transcript with speakers"), not as a feature list?
11. For a rejected tool, are the tasks it was turned down for listed, each with the reason?

### Run it here

12. Is the clone location written as `$EXTERNAL/<repo>`, never as a real path?
13. Does it name the version and the file to read first?
14. Does it say what to switch off (telemetry, outbound calls, auto-loading hooks), or state that nothing needs switching off?
15. Does it say what not to install, and that real installation waits for the user's yes?
16. For each `in use` part, does it say how it is used and which version?

### What's inside

17. Are the columns `Part | What it does | Status | <fourth> | Check when`, with the fourth `Without plugin` for `plugin` and `skill-collection`, `Needs` for every other kind?
18. Is every part named, with no "and N others"? For a collection above 40 parts: is every part that is not `listed` in the table, and is the generated parts list in `raw/data/` linked for the rest?
19. Does a part follow the kind (each skill, command, agent and hook; module or entry point; command; model variant; backend; main idea of a pattern)?
20. Is every status one of `listed`, `candidate`, `tried`, `in use`, `method taken`, `reference`, `rejected`?
21. Does every `rejected` row give its reason in the row?
22. Is Check when filled in every row, and of the kind its status calls for (`candidate`: the task to try it on; `rejected`: the revisit condition; `in use`: what to re-check; `listed`: when to read it; `tried`: the real task that would move it to `in use`; `method taken`: when to re-read upstream; `reference`: when to consult it again)?
23. Does the fourth column say concretely what breaks without the plugin, or what running the part takes here (nothing, a clone, a venv, a GPU and its memory, an API key, data leaving the machine)?

### Tried

24. Are the columns `Date | Task (by kind) | Part | Result | Cost | Record`, or is the section present with "none yet"?
25. Does every row link its trial or use record in `raw/notes/trials/`, and does that record hold the date, result and cost the row states?
26. Does every part with status `tried` or `in use` have at least one row here?

### Verdict

27. Do a few sentences sum up the rows without adding a card-level status, and say when to revisit?

### See Also and Sources

28. Does `## See Also` link every area page in `areas:`?
29. Does `## Sources` list the desk check, the parts list when there is one, and every trial and use record?

## Common Failures

These are the catalog's anti-goals as they show up in a card. Each is a finding even when everything else passes.

*   **Unchecked claim read as checked**: a "when not", a limit or a speed figure written from memory, with no raw file behind it, or a part shown as `candidate` that the desk check never read.
*   **The card costs more than the tool**: a card longer than the tool's own README for a small tool, prose where a row would do, or a route that needs more than index, area and card to reach a part.
*   **Silent staleness**: `version` or `licence` that no longer match the desk check cited, or a desk check older than an upstream release that changed an `in use` part, with no note.
*   **Private detail in a trial**: a task told by its project instead of its kind, a file name, a customer's data type that identifies them, a date that points to a meeting, a person's name.
*   **A push toward installing**: an install command presented as the way to use the tool, a global plugin install, missing "what not to install".
*   **Hidden parts**: "and 13 others", a part table that covers only the README's highlights, a rejected tool without its parts.
*   **Statuses outside the seven**, or two statuses in one cell.

## Must Not Contain

*   Names of projects, people, customers, employers, tickets or internal products, or anything from which they can be inferred.
*   Real local paths (any absolute path into a home folder, on any system, or a folder name that names an organisation); use `$EXTERNAL` and kit-relative paths.
*   Internal hosts, URLs, infrastructure ids, credentials, or links into a private wiki.
*   Private measurements that were not retold into `catalog/raw/`.
*   Installation instructions that act without the user's yes.
*   Copied code or long copied text from the tool; a card describes and links, and quotes only the short phrase a claim rests on.
