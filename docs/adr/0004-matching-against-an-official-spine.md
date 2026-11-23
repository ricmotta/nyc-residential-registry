---
status: accepted
---

# Matching against an official Spine, precision first

Every Source is matched against the Spine (Buildings from Building Footprints and Tax Lots from PLUTO, identified by BIN and BBL), not against every other Source. In one NYC neighborhood almost every residential Building already exists in city data, so a record that matches nothing on the Spine is more likely an error than a new Building: it goes to the Review Queue and never creates a Building on its own. Placeholder BINs (ending in six zeros, such as `1000000`) are never used to match.

## Layers

1. **Official ID**: the record carries a BIN or BBL that exists on the Spine. Links automatically.
2. **Normalized address + location**: links automatically only when all three hold: the address resolves to BIN X via PAD; the Building footprint nearest to the record's coordinates is X itself; and the coordinates are at most 10 m from X's footprint. Address points often fall on the sidewalk or street, so some slack is needed, but many Manhattan Buildings are only 6–8 m wide: the real risk is the neighbor being closer, so if the nearest footprint is another Building, the record goes to the Review Queue.
3. **Fuzzy comparison with a score**: always goes to the Review Queue until the ground truth exists and shows the rule is safe; the owner then sets the score thresholds.
4. **Units inside a Building**: unit numbers are normalized ("Apt 4B", "#4B", "4-B" become "4B").

## The CI brake

A hand-labeled ground truth of 50–100 pairs is the answer key. A pull request that touches matching fails if the pipeline links even one pair that the ground truth marks as different. Pairs sent to the Review Queue never fail the build; recall and queue size are only reported. With so few labeled pairs, a percentage threshold would hide that the difference between 99% and 100% is a single pair. A wrong match is worse than a missed one, because it puts the wrong Floor Plan on the wrong home.

## Review Queue round trip

The Review Queue is one list. A command exports it to CSV with both records side by side, the reason, the score and an empty `decision` column (`same`, `different` or `skip`). The owner fills it in, and a command turns the decided rows into the Owner Decisions seed through a pull request, as ADR 0001 requires. A review screen can come later and write to the same seed.
