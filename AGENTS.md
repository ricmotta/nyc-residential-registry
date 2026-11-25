# AGENTS.md

## Language

Everything in this repository is in English: code, comments, commit messages,
issues, PRs and docs. The conversation with the owner may be in another language.

## Before you start

Read the ticket, `GLOSSARY.md` and the ADRs in `docs/adr/` that touch your area.
Use the glossary's terms.

## Checks

The project uses Python 3.12 and [uv](https://docs.astral.sh/uv/) (`uv.lock` pins every version). Install with `uv sync`, then run the same checks as CI:

- Lint: `uv run ruff check .`
- Format: `uv run ruff format --check .` (fix with `uv run ruff format .`)
- Types: `uv run mypy`
- Tests: `uv run pytest`

CI runs all four on every pull request and never calls a real data Source. Add new commands here when they exist (for example `dbt build`).

Local environment (Docker, see README): `docker compose up -d`, then `uv run python -m nyc_registry.smoke` must exit 0. Settings always come from environment variables (`.env`, copied from `.env.example`); never hard-code endpoints or credentials, and reach object storage only through the S3 API (ADR 0002).

## Conventions

- One branch and one PR per ticket. Never push to `main`.
- Commit prefixes: `feat`, `fix`, `docs`, `test`, `chore`.
- Tests first for parsers, normalizers and collectors.
- Every stored value carries its source and fetch date.
- Collectors are idempotent and retry with backoff.
- Unverified facts are marked "to confirm".

## Delivery flow (ADR 0010)

- Every ticket starts with `Holdout: required` or `Holdout: not needed`. A `Holdout: required` ticket is ready only once its Holdout Scenarios are `confirmed`.
- Before opening a pull request, run the checks and self-review with the `code-review` skill (default effort); put a one-line self-review summary in the PR body.
- When a Holdout Report fails, fix on the same branch using only the report lines. After 2 failed attempts, stop, label the ticket `ready-for-human` and summarize what you tried.
- Changes to Terms Status, Owner Decisions, Review Queue decisions or ADRs are never merged or auto-merged without the owner.

## Never

- Collect from a source whose terms status in `docs/source-catalog.md` is not
  `approved`. Only the owner sets `approved`.
- Modify or delete anything in Bronze. It is append-only.
- Fail silently: no bare `except`, no swallowed errors. Log and propagate.
- Add personal or employment-related information to the repository.
- Read, search or copy the Holdout Scenarios repository (`nyc-residential-registry-holdout`) from a coding session, or guess its expected values.
- Mark a Holdout Scenario `confirmed` or `retired`. Only the owner does.

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues for this repo (`gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default triage vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` at the root and ADRs in `docs/adr/`. See `docs/agents/domain.md`.
