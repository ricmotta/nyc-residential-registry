---
status: accepted
---

# Medallion layers, with Silver and Gold rebuildable from Bronze

Data flows through three layers: Bronze (data exactly as fetched), Silver (clean, typed, linked) and Gold (final entities ready to use). Bronze is append-only and is our only history, because the city overwrites its datasets without keeping old versions. Every Fetch is recorded in Bronze, even when the content hash matches the previous Fetch: the file is not stored again, but a new metadata row proves the data was still current on that date.

Silver and Gold are disposable: they must be rebuildable from scratch using only Bronze plus Owner Decisions versioned in Git (dbt seeds). No Owner Decision lives only in the database. This lets us fix a bug in any parser or rule and simply rerun, and it gives every human decision an author, a date and a reason through Git history. The trade-off is that changing a decision needs a commit and a pull request instead of a direct database edit.

## Considered Options

- **Delta Lake time travel** as the safety net. Rejected as the mechanism for rebuildability: old versions are removed by `VACUUM` after a retention period, and it records neither who made a decision nor why. It could still be added later as a short-term undo; that is a separate decision about where the pipeline runs.
