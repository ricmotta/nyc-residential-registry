---
status: accepted
---

# Scope: two neighborhoods, defined by 2020 NTAs

The registry covers two neighborhoods, chosen because they complement each other: the Upper West Side (older and varied stock: condos, co-ops, rentals, landmarks, lots with several Buildings) and Long Island City (many new towers, recent condos and frequent DOB jobs).

Each neighborhood is a set of official 2020 Neighborhood Tabulation Areas from DCP ([dataset `9nt8-h7nd`](https://data.cityofnewyork.us/d/9nt8-h7nd)), not a ZIP code list or a hand-drawn polygon, because NTAs are official, versioned and already carried by several Sources:

| Neighborhood | NTAs |
|---|---|
| Upper West Side | `MN0701` Upper West Side-Lincoln Square, `MN0702` Upper West Side (Central), `MN0703` Upper West Side-Manhattan Valley |
| Long Island City | `QN0201` Long Island City-Hunters Point |

A Building or Tax Lot is in scope when it lies inside the union of these NTA polygons. Sources that carry an NTA code may be filtered by it at the API; the others are filtered spatially in PostGIS. The NTA list is configuration, so adding an area later is a one-line change.

## Considered Options

- **Including `QN0105` Queensbridge-Ravenswood-Dutch Kills** in Long Island City. Left out for now: besides Dutch Kills it brings large public housing developments with different data patterns. Start small and grow once the basics are reliable.
