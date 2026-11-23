---
status: accepted
---

# Software tests and data tests, split in two

Software tests check that the code works; data tests check that the data is correct, complete and current. They run at different times and use different tools.

| Tool | Checks | When | Kind |
|---|---|---|---|
| pytest | Parsers, normalizers, collectors, idempotency, the pydantic models | Every pull request | Software |
| pydantic | Every record entering Silver: types, required fields, rules such as "floors > 0". Failures go to quarantine | Every pipeline run, at the parser-to-Silver boundary | Data, on entry |
| dbt tests and contracts | Tables: `not_null`, `unique`, relationships, accepted values, source format | Every run, and in CI on sample data | Data, in tables |
| Elementary | Behavior over time: volume and freshness anomalies, test history, a report | Every run | Data, over time |

## CI never calls real Sources

CI runs fully offline. Collectors are tested with recorded responses: real pages saved as fixtures, plus 404, 429 and timeout cases. With several agents opening pull requests in parallel, live calls would multiply requests to the Sources and make CI fail for reasons outside our code. A separate scheduled live check (for example weekly) fetches a small sample from each Source and alerts when a Source has changed, without blocking any pull request.

## Elementary replaces the hand-written volume test

`pipeline_runs`, written by the Python collectors, is declared as a dbt source, so Elementary's volume anomaly tests watch both collection counts and dbt tables. This removes custom code we would otherwise maintain. Elementary's support for our PostgreSQL version is to confirm in Phase 1.
