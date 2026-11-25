---
status: accepted
---

# Software factory: Holdout Scenarios gate agent work, the owner keeps critical decisions

We want agents to take a ticket from spec to a ready pull request with as little human effort as possible, following the "dark factory" pattern described in [The Dark Factory Pattern](https://hackernoon.com/the-dark-factory-pattern-moving-from-ai-assisted-to-fully-autonomous-coding) (HackerNoon, 2026). That article's levels: at Level 2 an agent writes code and a human reviews every change; at Level 3 an agent works from a spec, hidden scenarios gate quality, and a human approves the merge; at Level 4 changes merge without a human. This is a personal project, so we adopt the parts that raise quality cheaply and skip those that need paid infrastructure.

## Target

Reach Level 3 first. Move towards Level 4 later and only per category of change, starting with low-risk ones such as documentation and refactors covered by tests. Auto-merge is considered only after 20 consecutive logged pull requests with `agreed = yes` (see the agreement log below).

Always the owner's, at every level: Terms Status (`docs/source-catalog.md`), Owner Decisions (dbt seeds, including Review Queue decisions) and ADRs.

## Holdout Scenarios

Holdout Scenarios add a third kind of check to ADR 0007's software tests and data tests: expected values about real Buildings and Tax Lots, kept hidden from the coding agent.

- **Isolated from the coding agent.** They live in a separate private repository (`nyc-residential-registry-holdout`), cloned outside this working directory, as a sibling folder. Deny rules in this repository's `.claude/settings.json` block the Read, Grep, Glob and Edit tools on any path containing `nyc-residential-registry-holdout/`, and Bash commands that name that path (enforcement verified with a denied read: to confirm). Bash rules match command text only, so a command that reaches the clone without naming it, such as a script that opens the files itself, is not blocked; the Claude Code sandbox would block it at the OS level, but it does not run on native Windows. The isolation relies on permissions and discipline, not on a hard barrier; that is enough for a personal project.
- **Written before the code.** By default, a separate session opened in the holdout repository, never shown the implementation, drafts scenarios from the ticket and official Sources; the owner may also write them by hand. Statuses: `draft`, `confirmed` (by the owner, one by one) and `retired`. Only `confirmed` scenarios count, and only the owner retires one, with a reason. An expected value produced by the same agent that writes the code would make the check circular.
- **Only for data tickets.** A ticket that creates or changes data in Silver or Gold starts with `Holdout: required` and gets `ready-for-agent` only after its scenarios are `confirmed`. Infrastructure, tooling and documentation tickets start with `Holdout: not needed` and rely on CI.
- **Deterministic SQL, run once.** For example, "Tax Lot X has 6 floors" or "this address links to this Building". No LLM judges the result, so repeated runs add nothing.
- **Gold first, Silver through stable surfaces.** Each scenario declares `layer: gold` or `layer: silver`. Gold alone would miss matching links, per-Source Claims, Quarantine, the Review Queue and redirects, and two errors could cancel out in a final value. Silver scenarios read only the Claims view, matching links, Quarantine, the Review Queue export and redirects, never satellites directly, so refactoring internals does not break scenarios. Bronze stays with pytest.

## Flow per `Holdout: required` ticket

1. Scenarios are `confirmed` in the holdout repository.
2. The coding session implements the ticket, runs the checks, self-reviews with the `mattpocock-skills:code-review` skill and opens the pull request with a one-line self-review summary.
3. The evaluator session, opened in the holdout repository, checks out the branch, starts the local environment (`docker compose`), runs the pipeline and the scenarios, and comments a Holdout Report on the pull request. The main repository is public, so the report shows scenario IDs and fields only, never expected values.
4. Gate: 100% of `confirmed` scenarios pass. After a failing report, the coding session gets only the report lines and fixes on the same branch, with at most 2 fix attempts. If the report still fails, it labels the ticket `ready-for-human` and comments what it tried.
5. The owner merges or not. The evaluator adds one row per pull request to a CSV in the holdout repository and the owner checks it: `pr`, `date`, `scenarios_passed`, `scenarios_total`, `owner_verdict` (`merged`, `changes_requested`, `closed`), `agreed` (`yes`, `no`) and `reason` (required when `agreed = no`). `agreed = yes` when the scenarios passed and the owner merged without requesting changes, or when the scenarios failed and the owner also saw the problem; otherwise `no`. A `no` resets the count of 20. `Holdout: not needed` tickets are not logged.

## Guardrails adopted, each implemented in its own ticket

- A versioned Git hook, `.githooks/pre-push`, enabled once with `git config core.hooksPath .githooks`, runs the four CI checks before every push. CI stays the final gate.
- ruff `banned-api` rules, with messages that tell the agent what to do instead, keep `boto3` inside `nyc_registry.storage` (object storage only through the S3 API, ADR 0002), `httpx` inside the future collector HTTP client (where ADR 0006's politeness rules live), and `psycopg` inside a database module.
- A pytest test that nothing deletes from Bronze, written with the first collector.

## Not adopted, for now

- Cloud ephemeral environments, LLM evaluators with 2-of-3 runs and a paid orchestrator calling a model API: too costly for a personal project. The local Docker environment plays the ephemeral environment, and the coding agent is a Claude Code session.
- Running scenarios in GitHub Actions across both repositories: revisit when merging must happen without the owner.
- A scheduled maintenance agent: maintenance sweeps run on demand; revisit before any auto-merge.
