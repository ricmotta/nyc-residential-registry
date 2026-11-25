# NYC Residential Registry

A registry of residential buildings in one New York City neighborhood, assembled from public sources. Every value keeps its origin, and missing data is shown, not hidden.

## Language

### Collection

**Source**:
One specific dataset or website we collect from, such as PLUTO or a single building's website. The agency or company behind it is its Publisher; two datasets from the same Publisher are two Sources.
_Avoid_: Provider, feed, agency

**Publisher**:
The agency or company that publishes a Source.
_Avoid_: Owner, vendor

**Terms Status**:
Whether the owner has cleared a Source for automated use under its terms: `approved` (the owner read the terms and allowed it), `pending` (not checked yet) or `blocked` (the terms forbid automated use). Only the owner sets `approved`.
_Avoid_: License, permission

**Fetch**:
One attempt to collect one item from a Source at a point in time. A Fetch is recorded even when the content is identical to the previous one, so it proves the data was still current on that date.
_Avoid_: Download, pull, scrape

### Property

**Tax Lot**:
A parcel of land as recorded by the city for taxes, identified by its BBL (borough, block, lot). A Tax Lot can hold several Buildings; in a condominium, each condo Unit also has its own unit BBL.
_Avoid_: Parcel, property, lot (alone)

**Building**:
A single physical structure, identified by the city's BIN when one exists. A Building sits on a Tax Lot; it is not the same thing as the Tax Lot.
_Avoid_: Property, address, lot

**Unit**:
One dwelling inside a Building, such as apartment 4B. Unit numbers are normalized so "Apt 4B", "#4B" and "4-B" name the same Unit.
_Avoid_: Apartment, residence, home

**Floor Plan**:
A drawing of a dwelling's layout, as published by a Source. It always belongs to a Building and may apply to zero, one or many Units, for example every Unit in line "A".
_Avoid_: Layout, blueprint, plan (alone)

**Photo**:
An image of a Building or its spaces, as published by a Source. It always belongs to a Building and may apply to zero, one or many Units, only when that link is certain.
_Avoid_: Picture, image (alone)

### Matching

**Spine**:
The Buildings and Tax Lots known from official city Sources, which every other Source is matched against. A record that matches nothing on the Spine goes to the Review Queue; it never creates a new Building on its own.
_Avoid_: Master list, golden list, backbone

**Review Queue**:
The single list of everything waiting for an Owner Decision: uncertain matches, records that matched nothing on the Spine, and conflicts between Claims. Each item shows its reason and the evidence side by side.
_Avoid_: Inbox, backlog, triage

### Claims

**Claim**:
One value for one field of one entity, as stated by one Source. For example, "PLUTO says this Building has 6 floors" is a Claim; "the building's website says 7" is another Claim about the same field. Later Fetches that repeat the same value confirm the existing Claim; a different value makes a new Claim.
_Avoid_: Fact, record, truth

**Confidence**:
How much a final value can be trusted, in three levels: `high` (set by an Owner Decision, or two independent Sources agree), `medium` (one Source, nobody disagrees) and `low` (Sources disagree beyond the field's tolerance, or the value comes only from a lower-ranked Source).
_Avoid_: Score, certainty, quality

**Lineage Group**:
A set of Sources that may copy data from one another, so their agreement does not count as independent confirmation. By default, each Publisher is one Lineage Group; a Source can belong to a different group for a specific field.
_Avoid_: Family, cluster

**Gap**:
A field with no usable Claim, always labeled with its reason: no known Source has the data; a Source has it but its terms (or its stated wishes, such as `robots.txt`) forbid our use; a Source has it but access needs an authorization we do not have, such as the building owner's; or a permitted Source has it but we have not collected it yet.
_Avoid_: Missing value, null, hole

### Quality

**Quarantine**:
Where data that failed validation waits, with the reason, and never reaches Gold. It is resolved only by fixing our code or by the Source correcting its data, never by editing it by hand; meanwhile the field uses the next-ranked Source, becomes a Gap, or takes an Owner Decision.
_Avoid_: Error table, dead letter, rejects

**Stale**:
A value that may be out of date, because no recent Fetch has confirmed it or because a newer building permit filing affects it.
_Avoid_: Old, expired, outdated

### Governance

**Owner Decision**:
A choice made by the project owner rather than taken from any Source, such as a manual override, a hand-labeled match pair or a source ranking. Owner Decisions are versioned in the repository, never edited only in the database.
_Avoid_: Manual entry, admin edit

### Delivery

**Holdout Scenario**:
An expected value about the registry, confirmed by the owner and hidden from whoever writes the code, such as "this Tax Lot has 6 floors" or "this address belongs to this Building".
_Avoid_: Acceptance test, golden record, fixture

**Holdout Report**:
The short result of running the Holdout Scenarios against a change: how many passed, and which scenario and field failed, without revealing the expected values.
_Avoid_: Satisfaction report, test report
