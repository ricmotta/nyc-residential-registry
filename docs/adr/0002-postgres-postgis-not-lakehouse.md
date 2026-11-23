---
status: accepted
---

# PostgreSQL + PostGIS for Silver and Gold, not a lakehouse

Silver and Gold live in PostgreSQL with PostGIS, transformed by dbt (`dbt-postgres`). Bronze files live in S3-compatible object storage. We chose a relational database over a lakehouse (Delta or Iceberg tables on object storage, read by Spark or DuckDB) because the data is small (one neighborhood, thousands of Buildings), spatial matching is central and PostGIS is the most mature tool for it, and the review queue needs many small row-level edits, which lakehouse tables handle poorly. A lakehouse would solve a scale problem we do not have.

## Consequences

- All code reaches object storage only through the S3 API, so the local store can be swapped for real AWS S3, or another S3-compatible store, by changing endpoints and credentials. The local store is SeaweedFS (4.52, pinned in Phase 1), because MinIO Community stopped publishing images in 2025 and LocalStack now requires an account and auth token.
- Because Bronze stays as plain files in object storage, moving Silver and Gold to a lakehouse later remains possible without fetching again.
