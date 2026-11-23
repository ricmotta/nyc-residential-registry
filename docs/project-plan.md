# Project Plan: NYC Residential Registry

A personal learning project. It is not affiliated with any company, and it uses only public data.

## 1. What this is

A registry of residential buildings in one New York City neighborhood. It combines several public sources, links buildings, units, floor plans and photos, keeps the origin of every value, and shows where data is missing.

**Core idea: every source is a claim, not the truth.** We store every claim with its source and date, and build the final record from those claims using explicit rules.

**Two goals:**
1. Build a trustworthy multi-source data pipeline (collection, matching, provenance, freshness).
2. Practice an AI-assisted "software factory" way of working: clear specs, small tickets, automated checks ("brakes"), and coding agents working in parallel under human review.

## 2. Language policy

Everything visible in this repository is written in **English**: code, comments, commit messages, issues, pull requests, docs, glossary and ADRs. The owner's day-to-day conversation with agents can be in any language, but the artifacts they produce must be in English.

## 3. Medallion architecture

```
SOURCES (city open data, public APIs, websites)
   │
   ▼  Python collectors, scheduled by Airflow
┌────────────────────────────────────────────────────────────┐
│ BRONZE: data exactly as fetched                            │
│ Original file in object storage + one metadata row per     │
│ item (source, URL, fetch date, content hash). Immutable.   │
└────────────────────────────────────────────────────────────┘
   │  Python parsers + dbt
   ▼
┌────────────────────────────────────────────────────────────┐
│ SILVER: clean, typed, linked                               │
│ Normalized addresses, one deduplicated view per source,    │
│ claims, record matching, quarantine table.                 │
└────────────────────────────────────────────────────────────┘
   │  dbt
   ▼
┌────────────────────────────────────────────────────────────┐
│ GOLD: ready to use                                         │
│ Final buildings, units, floor plans, photos, with a        │
│ confidence level per field. Coverage report, review queue. │
└────────────────────────────────────────────────────────────┘
   │
   ▼
CONSUMERS: dashboard, a simple app, or ML/AI
```

| Layer | Contents | Built with | Main rule |
|---|---|---|---|
| Bronze | Original files + fetch metadata | Python collectors | Never modified. Allows reprocessing without fetching again |
| Silver | Typed, normalized, deduplicated data; claims; match links; quarantine | Python parsers + dbt | Nothing enters without a source and a date |
| Gold | Final entities, confidence, coverage, review queue | dbt | Every final value is explained by a rule |

## 3.1 Where it runs: a simulated cloud on a laptop

Everything starts with one `docker compose up`, at no cost:

| Piece | Tool | Role |
|---|---|---|
| Object storage | S3-compatible: SeaweedFS (exact version to confirm in Phase 1; see ADR 0002) | Bronze files, pages, images |
| Database | PostgreSQL + PostGIS | Silver and Gold, spatial queries |
| Transformations | dbt (`dbt-postgres`) | Models, tests, field documentation |
| Orchestration | Airflow with LocalExecutor (no Celery or Redis); its metadata in a separate database on the same PostgreSQL | Schedules, retries, alerts, run logs |

The code talks to storage through the S3 API, so moving to real AWS later means changing endpoints and credentials, not code.

## 4. Collection: cheapest option first

For each source, climb the ladder only when the step below does not work:

1. **Official API or file** (for example NYC Open Data through the Socrata API). Cheapest and most stable.
2. **JSON the website itself loads**, if the terms allow it.
3. **Static HTML** with `httpx` and a light parser.
4. **Playwright**, only when the page needs JavaScript to show the data.

Rules for every collector:
- Check `robots.txt` and the terms of use before automating. If automation is not allowed, the source becomes a documented gap or a manual step.
- Respect rate limits. Retry with exponential backoff.
- Use `sitemap.xml` for discovery when available.
- Do not download unchanged content again (compare hash, ETag or last-modified).

## 5. Testing and quality, split in two

### 5.1 Software quality: the code works and never fails silently

| Goal | How | When |
|---|---|---|
| Parsers and normalizers are correct | TDD with pytest, using saved real pages as fixtures | Every PR |
| Input rules are encoded once | pydantic models, themselves tested with pytest | Every PR |
| CI does not depend on the internet | Recorded responses only; a separate scheduled live check alerts when a Source changes | Every PR; live check weekly |
| Collectors handle errors | Tests with recorded responses (success, 404, 429, timeout) | Every PR |
| Running twice gives the same result | Idempotency tests | Every PR |
| Readable, consistent code | `ruff` (lint, format) and `mypy` (types) | Every PR |
| No silent failures | No bare `except`; errors are always logged and propagated | Code review |
| We can see what happened | Structured JSON logs with source, run id and counts | Always |

### 5.2 Data quality: the data is correct, complete and current

| Goal | How | When |
|---|---|---|
| Required fields filled | dbt `not_null` | Every run and CI |
| No duplicates | dbt `unique` and composite key tests | Every run and CI |
| Valid links (a unit has a building) | dbt `relationships` | Every run and CI |
| Acceptable values (positive area, plausible floors) | dbt `accepted_values` and range tests | Every run and CI |
| Source format did not change | dbt model contracts | Every run and CI |
| Source is fresh | `dbt source freshness` | Every run |
| Every record entering Silver is valid | pydantic validation; failures go to quarantine | Every run |
| Collection did not suddenly shrink | Elementary volume anomaly tests on dbt tables and on `pipeline_runs` | Every run |
| Quality history and report | Elementary report | Every run |
| Matching is reliable | Hand-labeled ground truth; CI measures precision and recall | Every PR touching matching |

Every field we create gets a description in dbt `schema.yml`. `dbt docs` produces the data dictionary and lineage.

## 6. Pipeline properties

**Quality.** Critical tests stop the pipeline. Warning-level tests only alert.

**Quarantine and flags.**
- Data that fails validation goes to a quarantine table with the reason: per field when one value fails, per row when the row cannot be identified or read. The rest continues.
- If quarantine exceeds a threshold (for example 5% of a source), only that source stops and keeps its last good load, because the source probably changed.
- Flags on Silver and Gold: `needs_review`, `has_conflict`, `is_stale`. Low confidence is the `low` level of the confidence field, not a flag (ADR 0008).

**Observability.**
- Airflow: retries, alerts on failure or delay, per-task logs.
- A `pipeline_runs` table: per run and per source, items collected, new, changed, quarantined, duration, and LLM cost.
- A simple dashboard on top of it.

**Cost.**
- Incremental everywhere: process only what changed (content hash in Bronze, dbt `incremental` models with `unique_key`).
- Each source has its own refresh frequency, based on how often it changes.
- Use an LLM only where rules cannot work (free text, PDFs), cache results by content hash, and record cost per run.

## 7. Record matching

### 7.1 Data Vault: ideas yes, full method no

Data Vault ideas fit this problem well. The full method is too heavy for a small project. Data Vault does not do the matching; it stores the result of matching and the history from each source well.

| Table | Data Vault role | Contents |
|---|---|---|
| `hub_building`, `hub_unit` | Hub | Stable internal ID, never reused |
| `sat_building_<source>`, `sat_unit_<source>` | Satellite | Attributes per source, with load date and source record |
| `link_unit_building` | Link | A unit belongs to a building |
| `link_same_as` | "Same as" link | Source record → entity, with score and rule used |

Left out for now: hash keys everywhere, PIT and bridge tables, the full methodology.

### 7.2 Matching rules, in layers

1. **Official ID** (for example the city's building or tax lot identifiers; confirm which exist). If it matches, link.
2. **Normalized address + location.** Same normalized address and nearby coordinates.
3. **Fuzzy comparison with a score** (own rules, or Splink), only when 1 and 2 do not decide.
4. **Units inside a building:** normalize unit numbers ("Apt 4B", "#4B", "4-B" become "4B").

| Score | Outcome |
|---|---|
| High | Link automatically |
| Medium | Send to the review queue |
| Low | Do not link; create a new entity |

**Risk rule: a wrong match is worse than a missed match**, because it puts the wrong floor plan on the wrong home. Thresholds favor precision.

**How we measure:** a ground truth of 50–100 hand-labeled pairs. CI computes precision and recall. If precision drops below the threshold, the PR does not pass.

## 8. Source priority rules

Priority is **per field**, not per source. The city is the best source for year built, while a building's own website may be the best source for floor plans.

Decision order for each field:

1. **Valid and permitted.** Terms allow it and the value passed the tests. Otherwise it does not enter.
2. **Manual override wins.** A table of human decisions, with reason and date.
3. **Source authority for that field.** A configurable ranking.
4. **Agreement.** If two independent sources (different Lineage Groups) agree, confidence goes up.
5. **Large conflict.** If the difference passes a threshold (a per-field tolerance in the seed; for example area differing by more than 5%), keep both values, pick by the rules, and flag `has_conflict` and `needs_review`.

Configuration: a dbt seed `source_field_priority.csv` (field, source, rank, with no ties; see ADR 0005), versioned in Git, with the rule recorded in an ADR. Every final value stores which source won and by which rule.

Initial ranking (to confirm during source research):

| Field | 1st source | 2nd source |
|---|---|---|
| Address, year built, floors | City data | Building website |
| Number of units | City data | Building website |
| Unit floor plan | Building website | Other permitted sources |
| Photos | Building website | Other permitted sources |

## 9. The software factory workflow

### 9.1 Three kinds of AI in this project

| Kind | What it is | Example |
|---|---|---|
| Owner + one agent | Conversation and decisions | Glossary, ADRs, matching and priority rules |
| Parallel agents | Delegated work, one ticket each | One collector per source, source research |
| LLM inside the product | Part of the pipeline; does not write code | Extract fields from free text or PDFs |

### 9.2 What always stays with the owner

- Deciding whether a source may be used (terms of use).
- Labeling the matching ground truth.
- Setting score thresholds and the source ranking.
- Approving merges into `main`.

### 9.3 Tickets, skills and agents per part

Suggested labels: `layer:bronze`, `layer:silver`, `layer:gold`, `type:source`, `type:infra`, `type:quality`, `ready-for-agent`, `ready-for-human`.

| Part | Example tickets | Skills | Agents | CI brakes |
|---|---|---|---|---|
| Decisions | Glossary, ADRs (medallion, storage, matching, priority) | `grill-with-docs`, `domain-modeling` | Owner + 1 | Human review |
| Source research | One sheet per source: coverage, fields, cadence, terms | `research` | Several in parallel, in the background | Human review of each sheet |
| Infra | `docker compose`, Airflow, Postgres, storage, repo skeleton | `to-spec`, `implement` | 1 | Environment starts; smoke test passes |
| Bronze | One collector per source | `to-tickets`, `implement`, `tdd` | 1 per source, in parallel | Collector and idempotency tests |
| Silver | Parser and dbt model per source, address normalization, quarantine | `tdd`, `implement-spec` | Subagents per source | pytest, dbt tests, contracts |
| Matching | Hubs, satellites, links, score rules, review queue | `grill-with-docs`, `tdd`, `prototype` | Owner + 1 for rules, then 1 for code | Ground-truth precision and recall |
| Gold | Final entities, per-field priority, coverage | `implement` | 1 to 2 | dbt tests, provenance test |
| Observability | `pipeline_runs`, alerts, volume test, dashboard | `implement` | 1 | Alert tests |
| Continuous quality | Retro after each cycle | `retro`, `improve-codebase-architecture` | 1 | — |

### 9.4 CI/CD

**On every pull request (CI):**
1. `ruff` and `mypy`.
2. `pytest` (parsers, collectors, normalization, idempotency).
3. Start a temporary PostgreSQL in GitHub Actions and run `dbt build` on sample data (tests included).
4. Matching evaluation against the ground truth, when the PR touches matching.
5. Automated review by an agent using `code-review` and a checklist: terms of use, idempotency, retries, logs, no silent failures.

**On merge to `main` (CD):**
1. Build the Docker image and publish the Airflow DAGs.
2. Publish `dbt docs` (for example on GitHub Pages) as the data dictionary.

**Scheduled:** Airflow runs the pipeline. GitHub Actions is used for CI/CD and, later, to trigger agents on tickets labeled `ready-for-agent`.

## 10. Execution order

| Phase | Delivers | Way of working |
|---|---|---|
| 0. Decisions and research | Glossary, ADRs, source catalog with gaps | Owner + 1 agent; research agents in parallel |
| 1. Local infrastructure | Environment starts with one command; basic CI is green | 1 agent |
| 2. Vertical slice | One official source end to end: Bronze → Silver → Gold, dbt tests, quarantine, `pipeline_runs` | 1 agent, TDD |
| 3. Matching | Second source, light Data Vault, score rules, ground truth, review queue, per-field priority | Owner decides the rules; agent implements |
| 4. Scale | Many new sources at once | Parallel agents, one per ticket |
| 5. Automation | Freshness, volume alerts, cost tracking, automatic coverage report | 1 to 2 agents |

Factory rule: **do not move to phase 4 before phase 3 has working brakes.** Speed without brakes only produces more mess.

## 11. Cautions

- **Terms of use:** listing portals usually forbid scraping. Record them as blocked sources and gaps; do not scrape them.
- **Data from the city** carries no warranty and may change without history, so Bronze is our only history.
- **Scope:** start with one neighborhood and a few sources. Grow only after the basics are reliable.

## 12. Next step

Phase 0: set up the repository and the agent skills, run a grilling session to write the glossary and first ADRs, and finish the public-source research (the first pass is in `docs/source-catalog.md`).
