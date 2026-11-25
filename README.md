# NYC Residential Registry

A registry of residential buildings in one New York City neighborhood, built from
public sources. Every value keeps its origin, and missing data is shown as a gap
instead of being hidden.

> A personal learning project. It uses only public data and is not affiliated
> with any company or agency.

## Goals

1. Build a trustworthy multi-source data pipeline: collection, matching,
   provenance and freshness.
2. Practice an AI-assisted "software factory" workflow: clear specs, small
   tickets, automated checks, and coding agents working under human review.

## Development

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync            # install dependencies from uv.lock
uv run pytest      # run the tests
```

`AGENTS.md` lists every check that CI runs.

Enable the pre-push hook once per clone, so `git push` runs the same checks first
and stops on the first failure:

```sh
git config core.hooksPath .githooks
```

CI still runs every check on each pull request and stays the final gate.

## Local environment

Requires Docker with Docker Compose. One command starts PostgreSQL 17 with PostGIS 3.7,
SeaweedFS 4.52 (S3-compatible storage for Bronze) and Airflow 3.4 (LocalExecutor).

```sh
cp .env.example .env                       # then replace every change-me value
docker compose up -d                       # start
uv run python -m nyc_registry.smoke        # check that everything is reachable
docker compose stop                        # stop, keeping data
docker compose down -v                     # reset: delete containers and all local data
```

The smoke check exits 0 only if PostGIS is installed, the Bronze bucket accepts a write
and a read through the S3 API, every Airflow component is healthy and `dbt debug` passes.
It creates the Bronze bucket on first run.

| Service | Local address |
|---|---|
| PostgreSQL (project database `registry`) | `localhost:5432` |
| S3 API (SeaweedFS) | `http://localhost:8333` |
| Airflow UI and API | `http://localhost:8080` (no login locally) |

Airflow keeps its own metadata in a separate database (`airflow`) on the same server.
Ports and credentials come from `.env`.

### dbt

The dbt project lives in `dbt/` and reads its connection from the same environment
variables. Load `.env` into your shell first (for example `set -a; . ./.env; set +a`
in a POSIX shell), then:

```sh
cd dbt
uv run dbt deps --profiles-dir .
uv run dbt debug --profiles-dir .
```

## Status

Phase 1: local infrastructure and one official Source end to end. See the [Phase 1 spec](https://github.com/ricmotta/nyc-residential-registry/issues/8).

- Plan: [`docs/project-plan.md`](docs/project-plan.md)
- Sources: [`docs/source-catalog.md`](docs/source-catalog.md)
- Decisions: [`docs/adr/`](docs/adr/)
- Glossary: [`GLOSSARY.md`](GLOSSARY.md)
