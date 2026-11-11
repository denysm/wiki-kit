# Choosing AI delivery tooling for throwaway PoCs

A method for a team that ships a few proof-of-concepts a month, where the code is not needed after the demo. It gives a table of what to run in which situation and a template for choosing tools. Tool names are examples; the layers and questions stay the same.

## Template: choose tools in four layers

First write down the conditions, then put each candidate tool on a layer and give it one verdict.

**Conditions to write down** (the example values are typical for a PoC factory):

- PoCs per month (example: 1–2). At this volume a heavy setup does not pay off.
- Is the code needed after the demo? If not, speed wins; TDD, multi-level review and decision audits mostly waste tokens.
- Tech stacks: one or many. With many, the tool must not be tied to a language.
- Team size (example: 1–3 people).
- Where the agent runs, and the fallback if that is unavailable.

**Layers**

| Layer | Question it answers | Kind of tool |
|-------|---------------------|--------------|
| Specification | What we build | Live, versioned spec that stays the source of truth (spec-driven tools) |
| Discipline | How the agent works | Skills for brainstorm, plan, test-first, review; plans are disposable |
| Pipeline | The whole path of one task | Stages, human gates, review lenses, QA, branch ready for a PR |
| Orchestration | What triggers the work | Ticket triggers, tracker integration, autonomous runs |

A spec-driven tool keeps a spec that outlives the code and has a way to keep it current. A discipline tool governs how the agent works, and its plans are written, executed and forgotten. Neither is a pipeline: no roles, review lenses, QA gates or PR creation.

**Verdict per tool**: adopt as foundation, adopt as process, as needed, fallback, not now, no. For each, record the reason in one line and the condition that would change it (for example "revisit if the flow grows to dozens of tickets").

**Criteria to compare**

| Criterion | What to check |
|-----------|---------------|
| Entry barrier | Low, medium or high effort to install and learn |
| Stack lock-in | Languages or platforms it supports |
| Tracker lock-in | Which trackers it needs; whether you must write an adapter |
| Review and QA | Included or not |
| Autonomous work | Yes, no, or partly |
| Brownfield | Does it study an existing system and keep what it learns? |
| Greenfield | Is it strong when there is no code yet? |
| Security | Scan results of the bundle; read the findings before installing |

**Rule of thumb for the verdicts.** Take one discipline tool as the foundation (not tied to a stack, installs as a plugin, enough alone for a spike). Add one pipeline tool as the process. Take a spec-driven tool only when a PoC turns into a product. Orchestration comes last: it pays off only with a steady flow of tickets.

## When to run what

| Situation | What to run | What you get |
|-----------|-------------|--------------|
| Unclear what exactly we are doing and how | Brainstorming skill | An agreed solution design: options, trade-offs, decisions made. Then a story, or straight to a plan. |
| An idea or product area that must become a story | Product-owner skill | A story with acceptance criteria, a size estimate and a recommendation on which flow to run |
| Spike: "just check whether it works" | Brainstorming, then plan; no pipeline flow | An answer and throwaway code |
| Small PoC, plan up to about 6 tasks | Light pipeline flow | Implementation, review and QA gates; a human answers at 3 gates |
| Large PoC, 2–3 people | Standard pipeline flow | A spec and 5 gates; parallel work according to the plan |
| Brownfield: an existing system | Knowledge-foundation step, then a pipeline flow | Guides about the system in the repository, so the agent knows how it is built |
| The PoC turns into a product | Add a spec-driven tool | A living spec updated together with the code |

## Pipeline flows compared

| | Light flow | Standard flow |
|--|-----------|---------------|
| Purpose | Small tasks (plan up to about 6 tasks) | Regular tasks |
| Spec | None | Always, written through brainstorming |
| Complexity assessment up front | None | Yes, informs only, decides nothing |
| Clarifying questions | Up to 3 short ones | Inside brainstorming while the spec is written |
| Implementation | One implementer for the whole plan | The human chooses: one implementer, or an agent per task |
| Human gates | 3: plan, review, verification | 5: spec, plan, review (with re-check), verification |
| Code review | One round, then fixes the human checks | One round, then fixes and an independent re-check by an agent |

An autonomous mode runs the same stages with no human in the loop: stand-in agents resolve each judgment gate, and the run stops only when an escalation rule fires.

**What a human reviews in a run:** the codebase research the spec and plan rest on (an error here propagates), the spec, the plan, the review summary, and the quality-gate results (check that gates are PASS, not SKIPPED).

## Caveats to check before adopting

- A pipeline built around TDD and multi-lens review is heavier than throwaway work needs; keep the lightest path (discipline tool alone) for spikes.
- A pipeline that is weak on greenfield work covers only part of what a PoC factory does; the spike path fills the gap.
- Plugins that depend on each other at a minimum version: an upgrade of either needs a check of the pair.
- Tracker adapters may be missing and have to be added by the team.
- A marketplace page's view counts say little about real use; read the security scan before installing.
