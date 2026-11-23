# Source catalog

Every Source we know, what it covers, how to collect it, and whether we may use it.

First pass on 2026-11-19; updated on 2026-11-22 with the research in [`docs/research/`](research/). Each entry here is a summary; the research files hold the quotes and the primary-source links. Field names marked ✅ were read from the dataset's own metadata. Anything marked "to confirm" was not verified yet.

**Terms Status** (see `GLOSSARY.md`): `approved` (the owner read the terms and allowed it), `pending` (not checked yet) or `blocked` (the terms forbid automated use). Only the owner sets `approved`. Where the research found clear prohibitions, an entry says "research suggests `blocked`"; the status stays `pending` until the owner decides.

**Collection ladder step** (ADR 0006): 1 official API or file, 2 JSON the site loads, 3 static HTML, 4 Playwright.

## The short version

| What we need | Covered by public Sources? |
|---|---|
| Building identity (BIN, BBL, address) | **Yes, well.** PAD, Building Footprints, PLUTO; Geosupport or Geoclient for address lookups |
| Building attributes (floors, year, height, unit count) | **Yes.** PLUTO, Building Footprints, HPD Jurisdiction (legal unit counts), DOB filings, DCP Housing Database |
| List of Units | **Condos: yes** (DOF Condo Units). **Rentals and co-ops: partial.** Unit numbers appear in HPD violations and complaints, DOF sales and ACRIS deeds, but only for Units that ever showed up there |
| Unit attributes (bedrooms, size) | **Mostly a Gap.** Bedroom mix per Building exists only for subsidized buildings. Per-Unit bedrooms and size are in listing portals, which forbid automated use |
| Floor Plans | **Gap.** No bulk public source. Most management company sites sampled forbid automated access. DOB plans need the owner's notarized authorization |
| Photos | **Partial.** The Municipal Archives tax photos (about 1940 and mid-1980s) cover every building, keyed by block and lot. Current photos: Gap |

The main finding stands: public data answers "which buildings exist and what are they". Current unit-level detail, Floor Plans and Photos live mostly in private Sources whose terms forbid automated use.

## Rules that apply to all NYC Open Data Sources

- **Access**: Socrata API (SODA). With an app token in the `X-App-Token` header, requests are not throttled unless abusive; without one, requests share a pool per IP and can get `429`. ([Socrata docs](https://dev.socrata.com/docs/app-tokens)) `data.cityofnewyork.us/robots.txt` sets `Crawl-delay: 1` and does not disallow the SODA resource API.
- **Terms**: the old NYC Open Data terms page (`nyc.gov/html/data/terms.html`) now returns 404. The current [Open Data FAQ](https://www.nyc.gov/opendata/get-started/FAQs) says "There are no restrictions on the use of Open Data." The site footer links the general [NYC.gov Terms of Use](https://www.nyc.gov/main/terms-of-use), which say site content is City property, "All rights are reserved", and disclaim accuracy. Which of the two governs downloads is to confirm (owner decision). No dataset in this catalog sets a license in its metadata. No city terms found forbid automated use. ([catalog-verification.md §8](research/catalog-verification.md#8-terms-of-use-per-publisher))
- **No old versions**: the archived copy of the old terms page said "Older versions of data sets will not be retained", so our Bronze layer is the only history we will have.
- **Open Data can lag the Publisher**: on 2026-11-22, PLUTO and PAD on DCP's own pages were one release ahead of their Open Data copies. Fetching from DCP directly is an option (to decide per Source).
- **Mixed current and inactive rows**: ACRIS keeps corrections as new rows (keep the latest `good_through_date` per document); HPD Jurisdiction needs `recordstatus` and `lifecycle` filters; the DCP Housing Database needs a `job_status` filter.
- **DOB websites block non-US connections**: DOB BIS and DOB NOW answer `403` with "Access is restricted to locations within the United States". This affects any manual or automated step on those sites, not the Open Data copies.

## Building identity

### PAD (Property Address Directory)

- **Publisher**: NYC Dept. of City Planning (DCP). Open Data `bc8t-ecyu` (26c); DCP's own page has **26D** (November 2026). Quarterly.
- **What it has**: `bobaadr.txt` (address file: address **ranges** per BIN, low and high house number with parity) and `bobabbl.txt` (BBL file). For condos, each BBL-file row maps a **range** of unit BBLs to the billing BBL; it does not list Units one by one.
- **Watch out**:
  - Address types (`addrtype`) include pseudo-addresses, vanity addresses and non-addressable place names; they matter for matching.
  - The 26D address file has three fields not in the layout PDF: `dapsflag`, `naubflag`, `physical_id` (meaning to confirm).
  - Expanding a condo range into unit BBLs assumes the range has no holes; use DOF Condo Units for the unit list.
- **Access**: ZIP download from [DCP](https://www.nyc.gov/content/planning/pages/resources/datasets/pad) or [Open Data](https://data.cityofnewyork.us/d/bc8t-ecyu). Ladder step 1.
- **Use**: the main bridge from an address to a BIN and BBL. Core of matching (ADR 0004).
- **Terms**: DCP "use limitations" (informational only, no warranty); no restriction on automated use found. **Terms Status**: `pending`.
- Details: [catalog-verification.md §1](research/catalog-verification.md#1-pad-property-address-directory-bc8t-ecyu).

### Building Footprints

- **Publisher**: NYC Office of Technology and Innovation (OTI). Open Data **`5zhs-2jue`** ("BUILDING"); map view `jh45-qr5r`; historic (demolished) footprints `ipkp-snf6`. Edited daily, published weekly.
- **Grain**: one row per building footprint.
- **Fields ✅** (lowercase on Socrata): `bin`, `base_bbl`, `mappluto_bbl`, `doitt_id`, `height_roof`, `ground_elevation`, `construction_year`, `feature_code`, `geom_source`, `last_edited_date`, `last_status_type`, `name`, `the_geom`.
- **Watch out**:
  - BINs ending in six zeros (like 1000000) are placeholders, so BIN is not unique. `feature_code = 1003` is a placeholder triangle.
  - Split buildings can share a BIN.
  - `base_bbl` can be out of sync with other agencies.
  - Do not use the Area and Length fields (computed in a projection that distorts them). `name` is not maintained.
  - Only buildings over 400 sq ft and 12 ft tall, plus others with BINs.
  - `last_edited_date` and `last_status_type` (Demolition, Alteration, Constructed, ...) are useful Stale signals.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/5zhs-2jue)); also on NYCMaps. ([metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md)) Ladder step 1.
- **Use**: Building identity and shape, height, year. Spatial matching. Part of the Spine.
- **Terms**: Open Data and NYC.gov terms. **Terms Status**: `pending`.

### PLUTO

- **Publisher**: DCP. Open Data `64uk-42ks` (26v2); DCP's own page has **26v3** (October 2026). About 858k tax lots.
- **Grain**: one row per Tax Lot (not per Building).
- **Fields ✅**: `bbl`, `borough`, `block`, `lot`, `address`, `zipcode`, `numfloors`, `unitsres`, `unitstotal`, `yearbuilt`, `bldgclass`, `latitude`, `longitude`, `condono`, `dcpedited`, `numbldgs`.
- **Where its fields come from**: `numfloors`, `unitsres`, `yearbuilt` from DOF's Property Tax System (`yearbuilt` partly from LPC, flagged by `dcpedited`); `numbldgs` is computed from Building Footprints.
- **Watch out**:
  - For condos, `bbl` is the billing lot.
  - `yearbuilt` is often accurate only to the decade; 0 or null means unknown.
  - Tax lots and zoning lots do not always match 1:1.
- **Cadence** (DCP's page): a quarterly major release updates all fields; monthly minor releases update zoning fields only. So building fields change only quarterly.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks)) or DCP download ([page](https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change)). Ladder step 1.
- **Use**: lot-level attributes and residential unit counts. Part of the Spine.
- **Terms**: DCP "use limitations" (informational only, no warranty). **Terms Status**: `approved` by the owner on 2026-11-22, for automated collection through the official API, after reading the DCP PLUTO page, the NYC Open Data FAQ, the NYC.gov Terms of Use and the Open Data `robots.txt`.

### Geosupport Desktop Edition

- **Publisher**: DCP. Free download for Windows and Linux; quarterly releases, plus an updated address file (UPAD) about every two weeks.
- **What it is**: the city's geocoder, run locally: address, intersection or place name to BIN, BBL, address ranges and coordinates.
- **Watch out**: keep the release ID with every result. The exact download URL and whether it runs in a Linux container are to confirm.
- **Ladder step**: 1 (official software). Runs locally, so no network limits.
- **Use**: matching (ADR 0004, layer 2), offline and without keys.
- **Terms**: "freely available to the public with no limitations"; all derivatives must carry DCP's copyright statement. Whether our stored results count as derivatives: to confirm by the owner. **Terms Status**: `pending`.
- Details: [unresearched-sources.md](research/unresearched-sources.md#geosupport-desktop-edition).

### NYC Geoclient API (v2)

- **Publisher**: OTI, a REST wrapper over Geosupport. Moved to `https://api.nyc.gov/geoclient/v2`; the old `maps.nyc.gov` host returns 410.
- **Access**: free sign-up on the NYC API Developers Portal and a key in the `Ocp-Apim-Subscription-Key` header. Rate limits and API-specific terms: to confirm. The user guide the official repo points to is hosted on a personal GitHub account, not a city domain.
- **Ladder step**: 1. **Use**: the same lookups as Geosupport, over the network.
- **Terms**: NYC.gov Terms of Use; sign-up terms to confirm. **Terms Status**: `pending`.
- Details: [unresearched-sources.md](research/unresearched-sources.md#nyc-geoclient-api).

## Units

### DOF Digital Tax Map: Condominium Units

- **Publisher**: NYC Dept. of Finance (DOF). Dataset `eguu-7ie3`.
- **Grain**: one row per condo Unit.
- **Fields ✅** (16): `condo_base_boro`, `condo_base_block`, `condo_base_lot`, `condo_base_bbl`, `condo_number`, `condo_key`, `condo_base_bbl_key`, `unit_boro`, `unit_block`, `unit_lot`, `unit_bbl`, `unit_designation`, `floor_text`, `model`, `geometry_type`, `effective_tax_year`.
- **Cadence**: monthly (extracted the last Friday of each month, refreshed on the 1st). The "Weekly" metadata field contradicts this. The tax map alternates between "Set A" and "Set B" each month.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/eguu-7ie3)). Ladder step 1.
- **Use**: the only bulk public list of individual Units. Condos only.
- **Terms**: DOF disclaimer (informational only, not guaranteed accurate). **Terms Status**: `pending`.

### Buildings Subject to HPD Jurisdiction

- **Publisher**: NYC Dept. of Housing Preservation and Development (HPD). Dataset `kj4p-ruqc`. Monthly.
- **Grain**: one row per HPD `buildingid`. Covers only buildings HPD has dealt with (registration, complaints, litigation, work orders, enforcement), not every Building.
- **Fields ✅** (main): `buildingid`, `bin`, `boroid`, `block`, `lot`, `lowhousenumber`, `highhousenumber`, `streetname`, `legalstories`, `legalclassa` (number of apartments), `legalclassb`, `registrationid`, `lifecycle`, `recordstatus`.
- **Watch out**: no BBL column (build it from `boroid` + `block` + `lot`); placeholder BINs and `bin = 0` exist; filter on `recordstatus = 'Active'` and `lifecycle = 'Building'`.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/kj4p-ruqc)). Ladder step 1.
- **Use**: legal unit count per Building (a count, not a list), a Claim to compare with PLUTO `unitsres`; legal stories.
- **Terms**: Open Data terms; HPD-specific terms to confirm. **Terms Status**: `pending`.

### HPD Multiple Dwelling Registrations

- **Publisher**: HPD. Dataset `tesw-yqqr`. About 187k rows. Cadence: metadata says monthly, the attached PDF says quarterly (to confirm).
- **What it is**: owners of rental buildings with 3 or more units (and of 1–2 family homes they do not live in) must register yearly.
- **Fields ✅**: `registrationid`, `buildingid`, `bin`, `boroid`, `block`, `lot`, `housenumber`, `lowhousenumber`, `highhousenumber`, `streetname`, `zip`, `lastregistrationdate`, `registrationenddate`.
- **Watch out**: one `registrationid` can cover several buildings, so `buildingid` is the building key. `registrationid` joins to HPD Jurisdiction.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/tesw-yqqr)). Ladder step 1.
- **Use**: confirms a Building is a rental multi-unit, and gives address ranges with a BIN. No unit list.
- **Terms**: Open Data terms; HPD-specific terms to confirm. **Terms Status**: `pending`.

### Partial unit numbers and bedroom mix on Open Data

None of these is a complete list. A Unit seen in one of them proves it exists, not that the list is complete; the rest stays a Gap. Unit numbers are typed by people and need normalizing. All are ladder step 1 (Socrata API), Open Data terms, **Terms Status** `pending`. Details: [units-floor-plans-photos.md §1](research/units-floor-plans-photos.md#unit-level-data-on-nyc-open-data).

| Dataset | Publisher | What it can fill |
|---|---|---|
| HPD Housing Maintenance Code Violations `wvxf-dwi5` | HPD | Rental unit numbers (`apartment`, `story`), for Units with a violation |
| HPD Complaints and Problems `ygpa-z7cr` | HPD | Rental unit numbers, for Units with a complaint |
| DOF Rolling Sales `usep-8jbt` | DOF | Unit numbers of sold condo and co-op Units |
| DOF Property Valuation and Assessment `8y4t-faws` | DOF | Condo unit numbers, possibly unit area (grain to confirm) |
| ACRIS Real Property Legals `8h5j-fqxa` | DOF | Unit numbers named in recorded documents (see ACRIS below) |
| HPD Affordable Housing Production by Building `hg8x-zxpr` | HPD | Bedroom mix per Building, HPD-financed projects only |
| HPD Housing Connect lotteries by Building `nibs-na6y` | HPD | Bedroom mix of lottery units since July 2020 |
| HPD Local Law 44 Unit Income Rent `9ay9-xkek` | HPD | Units by bedroom size per Building, LL44 projects only |

## Changes over time

### DOB NOW: Build – Job Application Filings

- **Publisher**: NYC Dept. of Buildings (DOB). Dataset `w9ak-ipjd`.
- **Fields ✅**: `bin`, `borough`, `block`, `lot`, `house_no`, `street_name`, `existing_dwelling_units`, `proposed_dwelling_units`, `existing_stories`, `proposed_no_of_stories`, `existing_height`, `proposed_height`, `filing_date`.
- **Watch out**: not every job type is included (electrical, elevator and LAA jobs are elsewhere).
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/w9ak-ipjd)). Ladder step 1.
- **Use**: a signal that a Building changed (units, stories, height), so its Claims may be Stale (ADR 0008).
- **Terms**: Open Data terms; DOB-specific terms to confirm. **Terms Status**: `pending`.

### DCP Housing Database (project level)

- **Publisher**: DCP, built from DOB filings, permits and certificates of occupancy. Dataset `br6q-ssj3`, version 26Q2.1. Updated every 6 months.
- **Grain**: one row per DOB job (new building, alteration, demolition) filed or completed since 2010.
- **Fields ✅** (main): `job_number`, `job_type`, `job_status`, `bin`, `bbl`, `classainit`, `classaprop`, `classanet`, `units_co`, `floorsinit`, `floorsprop`, `datefiled`, `datecomplt`.
- **Watch out**: withdrawn jobs are present (filter on `job_status`); unit fields come from the applicant; not a full history of a Building. Whether this table is the version that includes inactive jobs: to confirm.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/br6q-ssj3)); past versions on DCP's page (to confirm). Ladder step 1.
- **Use**: cleaner change signals than raw DOB filings; a lower-ranked Claim for current legal unit count; completion year as a check on PLUTO.
- **Terms**: Open Data terms. **Terms Status**: `pending`.

### DOB Certificates of Occupancy

- **Publisher**: DOB. Two datasets:
  - `bs8b-p36w`, July 2012 to March 2021. **Fields ✅**: `job_number`, `job_type`, `c_o_issue_date`, `bin_number`, `borough`, `house_number`, `street_name`, `block`, `lot`, `postcode`, `pr_dwelling_unit`, `ex_dwelling_unit`, `application_status_raw`, `filing_status_raw`, `item_number`, `issue_type`, `latitude`, `longitude`, `bin`, `bbl`, plus district fields.
  - **`pkdm-hqz6`**, "DOB NOW: Certificate of Occupancy", March 2021 onward, with a single `number_of_dwelling_units`. Its metadata says daily, its data dictionary says monthly.
- **Watch out**: dwelling unit counts are reported by the applicant; `bin_number` (from DOB's system) and `bin` (geocoded) can differ; block and lot are as submitted. The DCP Housing Database already carries certificate unit counts (`units_co`) for jobs since 2010.
- **Certificate PDFs**: viewable one by one in DOB BIS or DOB NOW, not in bulk; both sites block non-US connections. A manual step only.
- **Access**: Socrata API ([`bs8b-p36w`](https://data.cityofnewyork.us/d/bs8b-p36w), [`pkdm-hqz6`](https://data.cityofnewyork.us/d/pkdm-hqz6)). Ladder step 1.
- **Use**: legal unit counts and use; a possible manual path to official documents.
- **Terms**: Open Data terms; DOB-specific terms to confirm. **Terms Status**: `pending`.

### ACRIS (Automated City Register Information System)

- **Publisher**: DOF, Office of the City Register. Monthly.
- **Datasets**: Real Property Master `bnx9-e6tj` (one row per document), Legals `8h5j-fqxa` (one row per property on a document, with `borough`, `block`, `lot`, `unit`), code tables `7isb-wh4c` and `94g4-w6xz`.
- **Condo declarations**: document types `CDEC`, `ADEC` (amended), `SCDEC` (condo in condo) and `TERDECL` (termination).
- **Watch out**: links to BBL only, no BIN; corrections arrive as new rows (keep the latest `good_through_date`); document images are not in Open Data. **Skip the Parties dataset** (`636b-3b5g`): it holds private people's names and addresses, which this project does not need.
- **Access**: Socrata API, always filtered by borough, block and lot (tables have 17–47M rows). Ladder step 1.
- **Use**: which Tax Lots are condos or co-ops and since when; unit designations from deeds; a new declaration marks a lot's Units as Stale.
- **Terms**: Open Data terms; DOF-specific terms to confirm. **Terms Status**: `pending`.
- **ACRIS website** (`a836-acris.nyc.gov`, document images): a plain request returned a DOF notice, "Further access to ACRIS is denied ... detection of automated scripts/robots", pointing to Open Data or a paid subscription. **Terms Status**: `pending`; research suggests `blocked`. Viewing one document by hand in a browser remains possible.
- Details: [unresearched-sources.md](research/unresearched-sources.md#acris-automated-city-register-information-system).

## Photos and historical documents

Rights differ per item, not per Source, so every Photo and Floor Plan needs its own rights field. Details: [units-floor-plans-photos.md §1](research/units-floor-plans-photos.md#1-public-and-government-sources).

### Municipal Archives tax photographs (about 1940 and mid-1980s)

- **Publisher**: NYC Dept. of Records and Information Services, Municipal Archives.
- **What it has**: more than 720,000 photos, one of every building in the five boroughs around 1940, each identified by block and lot; a second citywide survey from the mid-1980s.
- **Access**: [Preservica site](https://nycrecords.access.preservica.com/1940s-tax-photographs) with Block and Lot search; prints by order. Direct downloads, bulk or API route: to confirm. Ladder step to decide once access is known.
- **Terms**: "Non-commercial uses of Municipal Archives and Library materials are exempt from the licensing requirement"; published use needs the credit "Courtesy of the Municipal Archives, City of New York"; content may carry third-party rights. Copyright status of the photos themselves: to confirm. ([terms](https://www.nyc.gov/site/records/historical-records/terms-and-conditions.page))
- **Use**: the most promising Photo Source found: official, every building, linked to a Tax Lot. Historical, not current.
- **Terms Status**: `pending`.

### Landmarks Preservation Commission (LPC)

- **Datasets**: Individual Landmark Sites `buis-pvji` (links to designation report PDFs); Individual Landmark and Historic District Building Database `gpmc-yuvp` (per building: `bin`, `bbl`, `date_low`, architect, style, materials, original use). Ladder step 1.
- **Terms**: Open Data terms for the datasets; reports are City property, "All Rights Reserved". **Terms Status**: `pending`.

### Library of Congress: HABS/HAER/HALS

- **What it has**: measured drawings (including floor plans) and photos of historic buildings. Coverage of our neighborhood: to confirm.
- **Terms**: US government works are public domain (17 U.S.C. § 105); item records say "No known restrictions on images made by the U.S. Government; images copied from other sources may be restricted". Read only through search snippets because loc.gov refused automated requests: to confirm on the page. **Terms Status**: `pending`.

### NYPL Digital Collections and Wikimedia Commons

- **NYPL**: public-domain items are free to reuse; the Repo API was announced as unavailable from 2026-08-01. Manual or case by case. **Terms Status**: `pending`.
- **Wikimedia Commons**: license per file, with attribution to the creator. Its User-Agent policy asks for contact information, which conflicts with ADR 0006's generic User-Agent (owner decision). **Terms Status**: `pending`.

### Other public documents

- **DOB approved plans and drawings**: available only by records request with the owner's notarized authorization (form ADM-73). Not usable by this project; record Floor Plans as a Gap for this reason.
- **HPD Online I-cards**: historical building index cards; content per floor or unit to confirm. **Terms Status**: `pending`.
- **Rent Guidelines Board stabilized building lists**: PDFs per borough of buildings with at least one rent-stabilized unit; no unit list. Useful as a Building flag. **Terms Status**: `pending`.

## Private Sources

### Building and management company websites

- **What they may have**: Floor Plans, Photos, amenities, sometimes available Units.
- **Finding**: the earlier idea that these sites are "the most promising path" for Floor Plans and Photos mostly fails. Of the large managers sampled, several forbid robots or scraping outright, and the others limit use to personal, non-commercial viewing or forbid republishing.
- **Sample reviewed** (terms pages and `robots.txt` only; quotes and links in [units-floor-plans-photos.md §2](research/units-floor-plans-photos.md#2-building-and-management-company-websites)):

  | Publisher | What the terms say | Terms Status |
  |---|---|---|
  | Vivmark Residential (equityapartments.com, avaloncommunities.com) | Forbids robots, scrapers and crawlers; protected Content includes "floor plans" | `pending`; research suggests `blocked` |
  | Stonehenge NYC | Forbids "any automated means" | `pending`; research suggests `blocked` |
  | Fetner Properties | Forbids "any robot, spider or other automatic device" | `pending`; research suggests `blocked` |
  | Rudin | Forbids harvesting; personal, non-commercial license | `pending`; research suggests `blocked` |
  | Related Rentals | Personal, non-commercial license; no general robot clause found | `pending` |
  | Greystar | Personal, non-commercial use; not for further distribution | `pending` |
  | LeFrak | Personal, non-commercial downloads; `crawl-delay: 10` | `pending` |
  | Glenwood Management | No terms page; listings "may not be re-published" without consent | `pending` |
  | TF Cornerstone | Terms page needs JavaScript; not read | `pending` (to confirm) |

- **Rule**: each site needs its own check before collection. A missing terms page does not mean permission. Several sites use Cloudflare `Content-Signal` lines in `robots.txt`, which are not part of RFC 9309; whether collectors honor them is an owner decision.

### Listing portals

- **What they have**: Units, bedrooms, sizes, Photos, often Floor Plans.
- **Terms**: **blocked** as a group. Every portal whose terms were read forbids automated access:
  - Redfin, § 2.3.5 "No Scrubbing or Scraping" ([terms](https://www.redfin.com/about/terms-of-use)).
  - Realtor.com ([terms](https://www.realtor.com/terms-of-service/)), RentHop ([terms](https://www.renthop.com/resources/terms)) and Compass ([terms](https://www.compass.com/legal/terms-of-service/)): forbid scraping or any automated access.
  - Zillow, Trulia and Apartments.com: their terms pages refused automated requests; search snippets of the official pages show automated queries are forbidden. To confirm in a browser.
  - StreetEasy: consumer terms page refused automated requests (to confirm in a browser). Its advertising terms forbid automated scraping and incorporate Zillow's Terms of Use, and its `robots.txt` disallows `/building/*/floorplans`, `/rental/*` and `/sale/*`.
- **Data feeds**: only with approval or membership (Zillow's Bridge API datasets, REBNY RLS feeds for member brokers). Not open to this project.
- **Use**: none automated. Recorded as the reason current unit details, Floor Plans and Photos are Gaps.
- Details: [units-floor-plans-photos.md §3](research/units-floor-plans-photos.md#3-listing-portals).

## Copyright, in short

Facts (unit numbers, bedroom counts, areas) are not protected by copyright, but a site's terms can still forbid collecting them. Photos belong to their photographer. Floor plans can be protected as architectural works. Photos we take ourselves of buildings visible from public places are allowed (17 U.S.C. § 120(a)). Federal works are public domain; NYC City works are not by default. Primary sources and quotes: [units-floor-plans-photos.md §4](research/units-floor-plans-photos.md#4-copyright-note). This is a summary, not legal advice.

## Lineage notes (for the Lineage Group seed, ADR 0005)

The research found shared upstream data; the owner decides the groups.

- **PLUTO and Building Footprints** are not independent for year built (both trace to DOF assessment data), number of buildings (PLUTO counts Footprints BINs), BBL (join keys built to match) and location. Height (Footprints) and floors (PLUTO) are mostly independent.
- **PLUTO, PAD and DOF Condo Units** share DOF tax-lot data.
- **Geosupport, Geoclient and PAD** are one engine and one directory.
- **DCP Housing Database and DOB datasets**: the Housing Database is built from DOB data.
- **HPD Jurisdiction and HPD Registrations**: same Publisher.

Details: [catalog-verification.md §7](research/catalog-verification.md#7-do-pluto-and-building-footprints-derive-from-each-other).

## Open items (to confirm)

- Which terms govern NYC Open Data downloads now that the old page is gone (FAQ "no restrictions" vs NYC.gov "all rights reserved").
- HPD-, DOB- and DOF-specific terms; Geoclient rate limits and sign-up terms; Geosupport download URL and "derivatives" clause.
- StreetEasy, Zillow, Trulia and Apartments.com terms, read in a browser; TF Cornerstone terms.
- Whether the Municipal Archives site offers downloads or an API, and the copyright status of the tax photos.
- Full lists in each research file under "Open items" or "Not verified".
