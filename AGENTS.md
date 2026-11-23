# AGENTS.md

## Language

Everything in this repository is in English: code, comments, commit messages,
issues, PRs and docs. The conversation with the owner may be in another language.

## Before you start

Read the ticket, `GLOSSARY.md` and the ADRs in `docs/adr/` that touch your area.
Use the glossary's terms.

## Checks

No tooling yet (it arrives in Phase 1). Planned: `ruff`, `mypy`, `pytest`,
`dbt build`. Update this section with the real commands when they exist.

## Conventions

- One branch and one PR per ticket. Never push to `main`.
- Commit prefixes: `feat`, `fix`, `docs`, `test`, `chore`.
- Tests first for parsers, normalizers and collectors.
- Every stored value carries its source and fetch date.
- Collectors are idempotent and retry with backoff.
- Unverified facts are marked "to confirm".

## Never

- Collect from a source whose terms status in `docs/source-catalog.md` is not
  `approved`. Only the owner sets `approved`.
- Modify or delete anything in Bronze. It is append-only.
- Fail silently: no bare `except`, no swallowed errors. Log and propagate.
- Add personal or employment-related information to the repository.

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues for this repo (`gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default triage vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` at the root and ADRs in `docs/adr/`. See `docs/agents/domain.md`.
