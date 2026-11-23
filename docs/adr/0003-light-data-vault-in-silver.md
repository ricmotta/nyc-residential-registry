---
status: accepted
---

# A light Data Vault in Silver

Silver borrows the core ideas of Data Vault and leaves out the rest. Data Vault does not do the matching; it stores the result of matching and each Source's history.

- **Hubs** hold one stable ID per entity: `hub_tax_lot`, `hub_building`, `hub_unit`, `hub_floor_plan`, `hub_photo`. Tax Lot and Building are separate entities, because a Tax Lot can hold several Buildings: copying a lot-level value such as PLUTO's residential unit count onto each Building would double count it.
- **Satellites** are one table per entity and Source (for example `sat_building_pluto`), wide and typed, with a new row only when a value changes. Repeated Fetches with the same content add no rows.
- **Claims** are a dbt view that unpivots the satellites into one row per entity, field, value and Source. Source priority (ADR 0005) works on Claims.
- **Links** connect entities: Building to Tax Lot, Unit to Building, Floor Plan and Photo to Building (always) and to Units (zero or more, only when certain), and a "same as" link from each source record to its entity, with the match score and the rule used.

## Stable IDs that survive a rebuild

Hub IDs are deterministic: a hash of the source record that first created the entity (for example Source `pluto` + BBL `1012340056`). Random UUIDs would change every time Silver is rebuilt, which ADR 0001 requires to be possible. When two entities turn out to be the same, the ID of the earliest-seen one survives; the other becomes a redirect to it and is never reused. Merges come from matching rules or Owner Decisions, so they are rebuilt the same way.

## Left out

Hash keys on every table, point-in-time (PIT) and bridge tables, and the full Data Vault methodology. They add weight without solving a problem we have at this scale.
