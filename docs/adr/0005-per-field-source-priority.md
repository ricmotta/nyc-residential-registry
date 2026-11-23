---
status: accepted
---

# Per-field source priority with no ties

The final value of each field is chosen from its Claims by fixed rules, configured in dbt seeds versioned in Git. Priority is per field, not per Source: the city is the best Source for year built, while a building's website may be the best Source for Floor Plans.

## Decision order

1. **Valid and permitted.** Only Claims from Sources whose Terms Status is `approved`, and that passed the data tests, take part.
2. **Owner Decision wins.**
3. **Rank.** `source_field_priority.csv` (`field`, `source`, `rank`, `conflict_tolerance`) gives every Source a unique rank per field. Ties are forbidden and a dbt test enforces it. We dropped the "most recent wins" tie-break because "recent" was ambiguous (our fetch date or the date the data describes); to let a newer Source win, change its rank. Within one Source, its current value is its latest satellite row.
4. **Confidence.** `high` when an Owner Decision set the value or two independent Sources agree; `medium` when one Source has it and nobody disagrees; `low` when Sources disagree beyond the field's `conflict_tolerance`, or only a lower-ranked Source has it. A conflict also sets `has_conflict` and `needs_review`, and both values are kept.
5. **Independence.** Two Sources are independent for a field only if they belong to different Lineage Groups for that field. The seed `source_lineage_group.csv` has the columns `source`, `field` and `lineage_group`. A row with `field = all` sets a Source's default group, which starts as its Publisher; a row naming a field overrides the default for that field only. Same-Publisher datasets often repeat the same data, and the research in `docs/research/catalog-verification.md` showed that independence can also depend on the field: PLUTO and Building Footprints copy each other for year built and number of buildings, but their height and floors come from different upstream data.

   Initial overrides, from that research:

   | source | field | lineage_group |
   |---|---|---|
   | `building_footprints` | `year_built` | `dof` |
   | `pluto` | `year_built` | `dof` |
   | `building_footprints` | `num_buildings` | `oti` |
   | `pluto` | `num_buildings` | `oti` |

Every final value records which Source won and by which rule. Initial tolerances: floors 0, residential units 0, year built 10 years (PLUTO's `yearbuilt` is often accurate only to the decade), height 5%, area 5%. We chose fixed levels over a weighted formula because anyone can see why a value is `low` by reading its Claims.
