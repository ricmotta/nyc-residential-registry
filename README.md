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

## Status

Phase 1: local infrastructure and one official Source end to end. See the [Phase 1 spec](https://github.com/ricmotta/nyc-residential-registry/issues/8).

- Plan: [`docs/project-plan.md`](docs/project-plan.md)
- Sources: [`docs/source-catalog.md`](docs/source-catalog.md)
- Decisions: [`docs/adr/`](docs/adr/)
- Glossary: [`GLOSSARY.md`](GLOSSARY.md)
