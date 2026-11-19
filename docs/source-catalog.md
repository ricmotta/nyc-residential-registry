# Source catalog

Every Source we know, what it covers, how to collect it, and whether we may use it.

Researched on 2026-11-19. Field names marked ✅ were read from the dataset's own metadata. Anything marked "to confirm" was not verified yet.

**Terms status**: `approved` (a human checked the terms), `pending` (not checked yet), `blocked` (terms forbid automated use).

## The short version

| What we need | Covered by public Sources? |
|---|---|
| Building identity (BIN, BBL, address) | **Yes, well.** PAD, Building Footprints, PLUTO |
| Building attributes (floors, year, height, unit count) | **Yes.** PLUTO, Building Footprints, DOB filings |
| List of Units | **Only for condos** (DOF Condo Units). For rentals we get counts, not unit numbers |
| Unit attributes (bedrooms, size) | **Gap.** Mostly in listing portals, which forbid scraping |
| Floor Plans | **Gap.** No bulk public source found. Building websites, case by case |
| Photos | **Gap.** Same as Floor Plans |

The main finding: public data answers "which buildings exist and what are they". The hard research problem is unit-level detail, Floor Plans and Photos, which live mostly in private Sources.

## Rules that apply to all NYC Open Data Sources

- **Access**: Socrata API (SODA). With an app token in the `X-App-Token` header, requests are not throttled unless abusive. Without one, requests share a pool per IP and can get `429`. ([Socrata docs](https://dev.socrata.com/docs/app-tokens))
- **Terms**: NYC's terms defer to the NYC.gov Terms of Use and to any terms of the agency that publishes the data. The City gives no warranty of accuracy or completeness, and data can change or be overwritten without old versions being kept. Check each dataset's agency terms before any commercial use or redistribution. ([NYC Open Data terms](https://www.nyc.gov/html/data/terms.html))
- **Consequence for us**: since the city does not keep old versions, our bronze layer is the only history we will have.

## Building identity

### PAD (Property Address Directory)

- **Publisher**: NYC Dept. of City Planning, via NYC Open Data. Dataset `bc8t-ecyu`, version 26c.
- **What it has**: lot-level data not in PLUTO, including alias addresses and BINs. Two comma-delimited files: tax lot and address. Address ranges and condo crosswalk: to confirm.
- **Access**: ZIP download. ([dataset](https://data.cityofnewyork.us/d/bc8t-ecyu))
- **Use**: the main bridge from an address to a BIN and BBL. Core of matching.
- **Terms**: pending.

### Building Footprints

- **Publisher**: NYC Office of Technology and Innovation (OTI). Edited daily, published weekly.
- **Grain**: one row per building footprint.
- **Fields**: BIN, BASE_BBL, MAPPLUTO_BBL, DOITT_ID, HEIGHT_ROOF, GROUND_ELEVATION, CONSTRUCTION_YEAR, FEATURE_CODE, GEOM_SOURCE.
- **Watch out**:
  - BINs ending in six zeros (like 1000000) are placeholders, so BIN is not unique.
  - Split buildings can share a BIN.
  - BASE_BBL can be out of sync with other agencies.
  - Do not use the Area and Length fields (computed in a projection that distorts them).
  - Only buildings over 400 sq ft and 12 ft tall, plus others with BINs.
- **Access**: NYC Open Data dataset ID to confirm; also on [NYCMaps](https://nycmaps-nyc.hub.arcgis.com/datasets/nyc::building/about). ([metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md))
- **Use**: Building identity and shape, height, year. Spatial matching.
- **Terms**: pending.

### PLUTO

- **Publisher**: NYC Dept. of City Planning. Dataset `64uk-42ks`, version 26v2. About 858k tax lots.
- **Grain**: one row per Tax Lot (not per Building).
- **Fields ✅**: `bbl`, `borough`, `block`, `lot`, `address`, `zipcode`, `numfloors`, `unitsres`, `unitstotal`, `yearbuilt`, `bldgclass`, `latitude`, `longitude`, `condono`, `dcpedited`.
- **Watch out**:
  - For condos, `bbl` is the billing lot.
  - `yearbuilt` is often accurate only to the decade; 0 or null means unknown.
  - Unit counts update when DOB issues a permit.
  - Tax lots and zoning lots do not always match 1:1.
- **Cadence**: a quarterly major release plus monthly minor updates, according to a mirror of the catalog (to confirm on the city's page).
- **Access**: Socrata API. ([dataset](https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks))
- **Use**: lot-level attributes and residential unit counts.
- **Terms**: pending.

## Units

### DOF Digital Tax Map: Condominium Units

- **Publisher**: NYC Dept. of Finance. Dataset `eguu-7ie3`.
- **Grain**: one row per condo Unit.
- **Fields ✅**: `condo_base_bbl`, `condo_number`, `unit_bbl`, `unit_designation`, `floor_text`, `effective_tax_year`.
- **Cadence**: the metadata says weekly, the description says monthly. To confirm.
- **Access**: Socrata API. ([dataset](https://data.cityofnewyork.us/d/eguu-7ie3))
- **Use**: the only bulk public list of individual Units found so far. Condos only.
- **Terms**: pending.

### HPD Multiple Dwelling Registrations

- **Publisher**: NYC Dept. of Housing Preservation and Development. Dataset `tesw-yqqr`. Monthly, automated. About 187k rows.
- **What it is**: owners of rental buildings with 3 or more units (and of 1–2 family homes they do not live in) must register yearly.
- **Fields ✅**: `registrationid`, `buildingid`, `bin`, `boroid`, `block`, `lot`, `housenumber`, `lowhousenumber`, `highhousenumber`, `streetname`, `zip`, `lastregistrationdate`, `registrationenddate`.
- **Access**: Socrata API. ([dataset](https://data.cityofnewyork.us/d/tesw-yqqr))
- **Use**: confirms a Building is a rental multi-unit, and gives address ranges with a BIN. No unit list.
- **Terms**: pending.

## Changes over time

### DOB NOW: Build – Job Application Filings

- **Publisher**: NYC Dept. of Buildings. Dataset `w9ak-ipjd`.
- **Fields ✅**: `bin`, `borough`, `block`, `lot`, `house_no`, `street_name`, `existing_dwelling_units`, `proposed_dwelling_units`, `existing_stories`, `proposed_no_of_stories`, `existing_height`, `proposed_height`, `filing_date`.
- **Watch out**: not every job type is included (electrical, elevator and LAA jobs are elsewhere).
- **Access**: Socrata API. ([dataset](https://data.cityofnewyork.us/d/w9ak-ipjd))
- **Use**: a signal that a Building changed (units, stories, height), so its Claims may be stale.
- **Terms**: pending.

### DOB Certificates of Occupancy

- **Publisher**: NYC Dept. of Buildings. Dataset `bs8b-p36w`, covers July 2012 to March 2021. Later ones are in a separate DOB NOW dataset (ID to confirm).
- **What it is**: the permitted use and occupancy of a Building. The certificate PDFs are viewable one by one in DOB's BIS site, not in bulk.
- **Fields**: to confirm.
- **Access**: Socrata API for the table; PDFs are a manual step. ([dataset](https://data.cityofnewyork.us/d/bs8b-p36w))
- **Use**: legal unit counts and use; a possible manual path to official documents.
- **Terms**: pending.

## Private Sources

### Listing portals (Zillow, Redfin, StreetEasy and similar)

- **What they have**: Units, bedrooms, sizes, Photos, often Floor Plans.
- **Terms**: **blocked**. Zillow's and Redfin's terms forbid automated queries and scraping ([Zillow](https://conductatlas.com/platform/zillow/zillow-terms-of-use/provision/CA-P-032398/prohibition-on-automated-scraping-and-queries/), [Redfin](https://conductatlas.com/platform/redfin/redfin-terms-of-use/prohibition-on-automated-scraping/)). StreetEasy's own terms: to confirm, expected to be similar.
- **Use**: none automated. Recorded as the reason unit details, Floor Plans and Photos are Gaps.

### Building and management company websites

- **What they may have**: Floor Plans, Photos, amenities, sometimes available Units.
- **Terms**: case by case. Each site needs its own check before collection.
- **Use**: the most promising path to fill Floor Plan and Photo Gaps, using the collection ladder (ADR 0007).

## Not researched yet

- NYC Geoclient or Geosupport: official geocoding from address to BIN and BBL.
- ACRIS: property records, including condo declarations.
- HPD "Buildings Subject to HPD Jurisdiction": may have legal unit counts per Building.
- DCP Housing Database: unit changes per Building over time.
