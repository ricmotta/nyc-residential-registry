---
status: accepted
---

# Collection ladder, robots.txt as a hard limit

Each Source is collected with the cheapest method that works, climbing one step only when the step below fails:

1. Official API or file (for example the Socrata API for NYC Open Data).
2. JSON the website itself loads, if its terms allow it.
3. Static HTML with a light parser.
4. Playwright, only when the data appears only after JavaScript runs.

Each Source entry in `docs/source-catalog.md` records its chosen step and why the lower steps do not work. A collector ticket can be labeled `ready-for-agent` only when that note exists, so the ladder is a check a reviewer can verify, not a good intention.

## robots.txt and terms

The stricter of `robots.txt` and the terms of use wins. Even for a Source the owner marked `approved`, a collector reads `robots.txt` before every Fetch and never requests a path it disallows; instead it records a Gap with the reason "blocked by terms" and does not fail. If a site tightens its `robots.txt`, collectors follow it with no code change.

## Identification

Collectors send a generic User-Agent, `nyc-residential-registry/<version>`, with no personal details or contact link. It is a configuration value, not hard-coded.

## Politeness

- One connection per host, never parallel requests to the same site.
- At least 5 seconds between requests to the same website, with random jitter. If `robots.txt` sets a `Crawl-delay`, the larger of the two wins (`Crawl-delay` is not part of RFC 9309, but we honor it). APIs follow their own documented limits.
- On `429` or `503`, honor `Retry-After`; without it, back off exponentially.
- After several consecutive errors, stop that host for the run and alert (circuit breaker) instead of insisting.
- Send `If-None-Match` or `If-Modified-Since` so unchanged pages cost a `304`.
- Schedule website collection for night hours in New York.
