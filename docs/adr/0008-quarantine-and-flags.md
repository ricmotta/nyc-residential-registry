---
status: accepted
---

# Quarantine per Source and per field, and three flags

## Quarantine

Data that fails validation goes to quarantine with its reason, and the rest continues. Quarantine is per field when only one value fails a rule (`numfloors = -3` quarantines that Claim; the same row's year built and unit count go on), and per row only when the row cannot be identified (for example, no BBL) or cannot be read.

When a Source's quarantine passes its threshold (5% of rows or of fields, counted separately; the default for every Source, adjustable per Source), only that Source stops: its Silver and Gold keep the last good load, an alert fires, and the other Sources continue. A broken Source should not freeze the project, and nothing wrong reaches Gold.

Quarantine is a Silver table, so it is never edited by hand: a manual edit would be lost on the next rebuild (ADR 0001). It is resolved when we fix our code and reprocess from Bronze, or when the Source corrects its data. The code never invents a correct value; meanwhile the field uses the next-ranked Source, becomes a Gap, or takes an Owner Decision. The code owns quarantine; the owner owns the Review Queue.

## Flags

Three flags on Silver and Gold values: `needs_review`, `has_conflict` and `is_stale`. We dropped the planned `low_confidence` flag because it repeated `confidence = 'low'`, and two places for one fact can disagree.

`is_stale` is set when either:

1. the latest Fetch that confirmed the Claim is older than 2× the Source's expected refresh cadence (cadence per Source in a seed), which catches our own failures such as a stopped collector; or
2. a DOB job filing newer than the Claim affects that field (floors, units, height), which catches real changes no Source has caught up with yet.
