# Research: the four "Not researched yet" Sources

Researched on 2026-11-22. This file covers the four Sources listed under "Not researched yet" in [`docs/source-catalog.md`](../source-catalog.md), in the same per-source format.

Field names marked ✅ were read from the dataset's own metadata (the Socrata metadata API, `https://data.cityofnewyork.us/api/views/<id>.json`) or from the official data dictionary attached to the dataset. Counts and date ranges come from SoQL queries against the dataset's own API on the research date, so they will drift. Anything marked "to confirm" was not verified; the note says what was tried.

No Source here is `approved`. Only the owner sets `approved`.

## Summary

| Source | Publisher | Where | Grain | Has BIN | Has BBL | Cadence | Ladder step | Main use | Terms Status |
|---|---|---|---|---|---|---|---|---|---|
| Geoclient API (v2) | NYC OTI, wrapping DCP's Geosupport | `https://api.nyc.gov/geoclient/v2`, key from the NYC API Developers Portal | One response per lookup | Yes | Yes | Follows Geosupport releases (to confirm) | 1 | Matching: address to BIN/BBL | `pending` |
| Geosupport Desktop Edition | NYC Dept. of City Planning (DCP) | Free download from DCP | Local software, one result per call | Yes | Yes | Quarterly releases, plus UPAD about every two weeks | 1 | Matching, offline and without limits | `pending` |
| ACRIS (Real Property datasets) | NYC Dept. of Finance (DOF) | NYC Open Data, 5 Real Property datasets plus code tables | One row per document, per property on a document, per party | No | Yes, as borough + block + lot | Monthly | 1 (Open Data only) | Condo declarations, change signals | `pending` (Open Data). ACRIS website: suggest `blocked` |
| Buildings Subject to HPD Jurisdiction | NYC Dept. of Housing Preservation and Development (HPD) | NYC Open Data `kj4p-ruqc` | One row per HPD BuildingID | Yes | As `boroid` + `block` + `lot` | Monthly | 1 | Legal unit count (`legalclassa`), legal stories | `pending` |
| DCP Housing Database (project level) | NYC Dept. of City Planning (DCP) | NYC Open Data `br6q-ssj3` | One row per DOB job (new building, alteration, demolition) | Yes | Yes | Every 6 months | 1 | Unit changes per Building since 2010, change signals | `pending` |

Main findings:

- **HPD Jurisdiction has legal unit counts per Building.** `legalclassa` is "the number of apartments in a multiple dwelling", next to a BIN. It is the best public "legal unit count per Building" found so far, but it covers only buildings HPD has dealt with, not every Building.
- **ACRIS has condo declarations in bulk.** Doc types `CDEC` (condo declaration), `ADEC` (amended), `SCDEC` (condo in condo) and `TERDECL` (termination) are in the Real Property Master. The document images are not in Open Data, and the ACRIS website itself showed an "access denied" notice aimed at automated scripts.
- **Geoclient moved.** The old `maps.nyc.gov/geoclient` endpoint now answers HTTP 410 and points to `api.nyc.gov/geoclient/v2`, which needs a free sign-up and a subscription key. Rate limits could not be verified from a primary source.
- **The Housing Database gives one row per DOB job with initial, proposed and net Class A units, plus a BIN and BBL.** It is a ready-made, DCP-cleaned version of the DOB filings already in the catalog.

---

## NYC Geoclient API

- **Publisher**: NYC Office of Technology and Innovation (OTI). Geoclient is a REST proxy over DCP's Geosupport and "contains no additional spatial logic or reference data" ([Geoclient User Guide, §1](https://mlipper.github.io/geoclient/#concepts)).
- **Location**: `https://api.nyc.gov/geoclient/v2`. The old host `https://maps.nyc.gov/geoclient/v2/doc` returned HTTP 410 on 2026-11-22 with the message: "The geoclient v1 & v2 APIs hosted on this domain have been retired. Please use v2 at https://api.nyc.gov/geoclient/v2. Sign-up at https://api-portal.nyc.gov/signup." ([old endpoint](https://maps.nyc.gov/geoclient/v2/doc)). The NYC API Developers Portal lists Geoclient as a featured API: "provides an interface to the NYC Department of City Planning's Geosupport system and supports input locations such as address, intersection, blockface" ([portal home](https://api-portal.nyc.gov/)).
- **About the documentation**: the official repo [CityOfNewYork/geoclient](https://github.com/CityOfNewYork/geoclient) contains only a README saying "This project has moved to mlipper/geoclient". The user guide below is published from that repository. It is the documentation the official repo points to, but it is hosted on a personal GitHub account, not a city domain. The portal's own API pages render only with JavaScript and showed no content to a plain fetch.
- **Grain**: one JSON response per lookup. Endpoints: `/address`, `/addresspoint`, `/bbl`, `/bin`, `/blockface`, `/intersection`, `/normalize`, `/place`, `/search`, `/streetcode`, `/version` ([guide §3](https://mlipper.github.io/geoclient/#endpoints)).
- **Fields** (from the guide's example responses, not from a schema; not ✅): `buildingIdentificationNumber`, `bbl`, `bblBoroughCode`, `bblTaxBlock`, `bblTaxLot`, `condominiumBillingBbl`, `lowBblOfThisBuildingsCondominiumUnits`, `highBblOfThisBuildingsCondominiumUnits`, `numberOfExistingStructuresOnLot`, `rpadBuildingClassificationCode`, `latitudeInternalLabel`, `longitudeInternalLabel`, `internalLabelXCoordinate`, `internalLabelYCoordinate`, `giBuildingIdentificationNumber1..n`, `giLowHouseNumber1..n`, `giHighHouseNumber1..n`, `geosupportReturnCode`, `geosupportFunctionCode` ([guide §3.1 Address, §3.4 BIN](https://mlipper.github.io/geoclient/#address)).
- **Watch out**:
  - The guide says fields with NULL values are not serialized, and "even for successfully recognized input, certain data attributes may not be available" ([guide §2.1.2](https://mlipper.github.io/geoclient/#calling-the-geoclient-api)). Parsers must treat every field as optional.
  - Some values keep significant whitespace on purpose, such as `censusTract2020: " 187 "` ([guide §2.1.2, §3.1](https://mlipper.github.io/geoclient/#address)).
  - `geosupportReturnCode` must be checked; a 200 response can still be a Geosupport warning or rejection.
  - The `/bin` response returns the address ranges (`gi*` fields) of a Building, which is useful for alias addresses.
  - Placeholder BINs (ending in six zeros) can come back for lots without a real BIN (to confirm in Geoclient output; ADR 0004 already forbids matching on them).
- **Access**: free account on the NYC API Developers Portal, subscribe to the "Geoclient - v2" product, then send the key in the `Ocp-Apim-Subscription-Key` HTTP header on every request ([guide §7, §7.1](https://mlipper.github.io/geoclient/#public-endpoint)). The guide calls the public endpoint "freely available to the public". Not signed up for this research.
- **Rate limits**: to confirm. The user guide has no rate-limit section, the old doc page is retired, and the portal's API and product pages need JavaScript or a login. Numbers circulating on third-party sites were not used.
- **Cadence**: Geoclient serves whatever Geosupport release OTI has deployed. Which release is live can be read from the `/version` endpoint ([guide §3.12](https://mlipper.github.io/geoclient/#version)); not called here.
- **Collection ladder**: **step 1** (official API). It is the city's own documented REST API.
- **Use for this project**: **matching**. Turn a Source's address into BIN and BBL (ADR 0004, layer 2), and look up BINs to get their address ranges and condo billing BBL. It is a lookup service, not a Source of Claims about Buildings. Geosupport Desktop does the same job without keys or network limits; see the next sheet.
- **Terms**: the portal footer links to the general [NYC.gov Terms of Use](https://www.nyc.gov/main/terms-of-use), which forbid disrupting NYC.gov "or its servers or networks in any way". API-specific terms shown at sign-up: to confirm (not signed up).
- **Terms Status**: `pending`.

## Geosupport Desktop Edition

- **Publisher**: NYC Dept. of City Planning (DCP), Geographic Systems Section.
- **Location**: free download from DCP's "BYTES of the BIG APPLE" (Data & Tools, Open Data). The exact current download URL: to confirm. The DCP pages are rendered with JavaScript and showed no links to a plain fetch. The FAQ PDF lives at [gdeguide.pdf](https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/gdeguide.pdf). The User Programming Guide (UPG) is at [nycplanning.github.io/Geosupport-UPG](https://nycplanning.github.io/Geosupport-UPG/), according to [User Bulletin 26-02](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/geosupport-bulletin/geosupport-user-bulletin-2602.pdf).
- **What it is**: the city's geocoder, available for Windows (32 and 64 bit) and Linux. It is called from any language that can make a DLL call, or through the bundled GOAT and GBAT utilities (GBAT is for batch files) and the GeoX .NET/Java wrappers ([FAQ](https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/gdeguide.pdf)).
- **Grain**: one result per function call. Inputs include addresses, intersections, place names, tax lots and BINs. Outputs include "zip codes, address ranges, cross streets, census tract and block, tax block and lot, ... number of structures and x-y coordinates" ([FAQ](https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/gdeguide.pdf)).
- **Fields**: the same work areas Geoclient returns (Geoclient is a proxy over it). Exact field layout per function (1A, 1B, BL, BN): in the UPG; not read in detail here (to confirm).
- **Watch out**:
  - The Sanborn volume/page fields returned by functions 1A, 2, BL and BN are deprecated and will be removed ([Bulletin 26-02](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/geosupport-bulletin/geosupport-user-bulletin-2602.pdf)).
  - Results depend on the installed release. Keep the release ID with every Fetch so a match can be traced to the Geosupport version that made it.
  - Minimum requirement listed: 2 GB of disk space ([FAQ](https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/gdeguide.pdf)).
  - Running in Docker on Linux next to the pipeline: to confirm in practice.
- **Cadence**: quarterly releases ("released on a quarterly update cycle" ([FAQ](https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/gdeguide.pdf))). Between releases, an Updated PAD file (UPAD) is deployed about every two weeks and is available to Desktop Edition users through install packages ([Bulletin 26-02](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/geosupport-bulletin/geosupport-user-bulletin-2602.pdf)). The newest bulletin found was 26-02 (Release 26B, May 2026); the catalog's PAD entry is already at 26c, so a newer bulletin probably exists (to confirm).
- **Access**: download, no key or account mentioned in the FAQ.
- **Collection ladder**: **step 1** (official file/software). Runs locally, so there are no network rate limits or ladder politeness concerns.
- **Use for this project**: **matching**. It is the same engine as Geoclient and PAD (PAD is Geosupport's address directory), so it can replace Geoclient for batch address-to-BIN/BBL work. Note for ADR 0004: Geosupport, Geoclient and PAD are one Lineage Group, so their agreement is not independent confirmation.
- **Terms**: the FAQ says it is "freely available to the public with no limitations", and that "All derivatives of Geosupport Desktop Edition must include the following statement: 'Geosupport Desktop Edition™ copyrighted by the New York City Department of City Planning'". DCP disclaims accuracy and liability ([FAQ](https://www.nyc.gov/assets/planning/download/pdf/data-maps/open-data/gdeguide.pdf)). Whether outputs stored in our database count as "derivatives": to confirm by the owner.
- **Terms Status**: `pending`.

## ACRIS (Automated City Register Information System)

- **Publisher**: NYC Dept. of Finance (DOF), Office of the City Register.
- **Coverage**: ACRIS covers "Manhattan, Queens, Bronx, and Brooklyn from 1966 to the present" ([DOF ACRIS page](https://www.nyc.gov/site/finance/property/acris.page)). Staten Island records are kept by the Richmond County Clerk (to confirm on a primary page). The Legals dataset's `borough` field documents only codes 1–4, but a count by borough returned about 210k rows with `borough = 5`; what those are: to confirm.
- **Datasets on NYC Open Data** (all DOF; metadata says "Update Frequency: Monthly", "Automation: Yes", made public 9/23/2013):

  | ID | Name | Grain | Rows (2026-11-22) |
  |---|---|---|---|
  | [`bnx9-e6tj`](https://data.cityofnewyork.us/d/bnx9-e6tj) | ACRIS - Real Property Master | one row per document | 17,143,212 |
  | [`8h5j-fqxa`](https://data.cityofnewyork.us/d/8h5j-fqxa) | ACRIS - Real Property Legals | one row per property on a document | 22,833,692 |
  | [`636b-3b5g`](https://data.cityofnewyork.us/d/636b-3b5g) | ACRIS - Real Property Parties | one row per party on a document | 46,772,868 |
  | [`pwkr-dpni`](https://data.cityofnewyork.us/d/pwkr-dpni) | ACRIS - Real Property References | one row per cross reference | not counted |
  | [`9p4w-7npp`](https://data.cityofnewyork.us/d/9p4w-7npp) | ACRIS - Real Property Remarks | one row per 232-character remark chunk | not counted |
  | [`7isb-wh4c`](https://data.cityofnewyork.us/d/7isb-wh4c) | ACRIS - Document Control Codes | one row per doc type | code table |
  | [`94g4-w6xz`](https://data.cityofnewyork.us/d/94g4-w6xz) | ACRIS - Property Types Codes | one row per property type | code table |

  There are also Personal Property datasets (UCC and federal liens: `sv7x-dduq`, `uqqa-hym2`, `nbbg-wtuz`, `6y3e-jcrc`, `fuzi-5ks9`) and code tables `j2iz-mwzu` (country), `5c9e-33xj` (state) and `q9kp-jvxv` (UCC collateral). They are not useful for this project.

- **Fields ✅**:
  - Master: `document_id`, `record_type`, `crfn`, `recorded_borough`, `doc_type`, `document_date`, `document_amt`, `recorded_datetime`, `modified_date`, `reel_yr`, `reel_nbr`, `reel_pg`, `percent_trans`, `good_through_date`.
  - Legals: `document_id`, `record_type`, `borough`, `block`, `lot`, `easement`, `partial_lot`, `air_rights`, `subterranean_rights`, `property_type`, `street_number`, `street_name`, `unit`, `good_through_date`.
  - Parties: `document_id`, `record_type`, `party_type`, `name`, `address_1`, `address_2`, `country`, `city`, `state`, `zip`, `good_through_date`.
  - Document Control Codes: `record_type`, `doc__type`, `doc__type_description`, `class_code_description`, `party1_type`, `party2_type`, `party3_type`.
- **Condo declarations**: the Document Control Codes table has `CDEC` "CONDO DECLARATION", `ADEC` "AMENDED CONDO DECLARATION", `SCDEC` "DECLARATION OF CONDO IN CONDO" and `TERDECL` "TERM. OF CONDO DECLARATION" ([`7isb-wh4c`](https://data.cityofnewyork.us/d/7isb-wh4c)). In the Master, counts were `CDEC` 8,426 and `ADEC` 5,574 (recorded 2003-01 to 2026-10) and `SCDEC` 47 (2019-10 to 2026-10). Older declarations before 2003 may be under other types or only on reel/page (to confirm).
- **Property type codes useful for us** ([`94g4-w6xz`](https://data.cityofnewyork.us/d/94g4-w6xz)): `SC` single residential condo unit, `MC` multiple residential condo units, `SP` single residential co-op unit, `MP` multiple residential co-op units, `AP` apartment building, `D1`–`D6` dwelling only 1–6 family.
- **Links to BBL**: yes, through Legals (`borough` + `block` + `lot`), plus `unit` text. There is no BIN anywhere. The Legals `lot` for a condo unit is presumably the unit lot (unit BBL), which would join to DOF Condo Units `unit_bbl` (to confirm with a sample).
- **Watch out**:
  - Per the [ACRIS Open Data Extract Guide](https://data.cityofnewyork.us/api/views/bnx9-e6tj/files/c5d51488-f56b-495e-aef1-b9e7acc4680c?download=true&filename=ACRIS_Public_OpenData_Extract_Guide_v_1.0.doc) (attached to the dataset): each monthly extract adds documents "recorded or corrected in the previous month", and "for any document, the records with the latest good through date will be the current records". Corrections arrive as new rows, so loaders must keep the latest `good_through_date` per document.
  - Remarks longer than 232 characters are split over several rows by `sequence_number` and must be concatenated in order (same guide).
  - Parties hold personal names and addresses of private people. This project does not need them; skip that dataset to avoid storing personal data.
  - Pre-ACRIS documents appear with reel/page numbers instead of a CRFN.
  - Document images (the actual PDF pages of a declaration, with unit lists and floor areas) are **not** in Open Data; only the index is.
- **Cadence**: monthly. On 2026-11-22 the latest `good_through_date` was 2026-10-31, and the datasets were last updated 2026-11-10 ([`bnx9-e6tj` metadata](https://data.cityofnewyork.us/api/views/bnx9-e6tj.json)).
- **Access**: Socrata API, filtered by `borough`/`block`/`lot` for our neighborhood. The full tables are large (17–47M rows), so always filter.
- **The ACRIS website**: a plain request to `https://a836-acris.nyc.gov/robots.txt` and `https://a836-acris.nyc.gov/CP/` on 2026-11-22 returned a DOF notice: "Further access to ACRIS is denied. This can be due to multiple reasons such as detection of automated scripts/robots that are capturing data from the website or having exceeded the bandwidth limits ... If you need large amounts of data, please contact the City Register ... about our subscription data services. Additionally, ACRIS index data can be obtained from NYC Open Data." No further requests were made.
- **Collection ladder**: **step 1** (Socrata API) for the index. Steps 2–4 on the ACRIS website are ruled out: the site tells automated clients to use Open Data or a paid subscription. A single declaration image can still be viewed by hand in a browser (a manual step).
- **Use for this project**:
  - **identity**: which Tax Lots are condos (`CDEC`) or co-ops (`SP`/`MP` property types) and since when.
  - **units**: the Legals `unit` field on unit deeds gives unit designations, which can confirm or fill the DOF Condo Units list. For co-ops, it may be the only bulk public trace of unit numbers (to confirm how often co-op unit sales carry `unit`).
  - **change signals**: a new `CDEC`, `ADEC` or `TERDECL` on a lot means its condo structure changed and its Units are Stale.
  - **matching**: BBL only, no BIN.
- **Terms**: Open Data datasets fall under the general NYC Open Data terms (the old terms page now returns 404; see the [Open Data FAQ](https://www.nyc.gov/opendata/get-started/FAQs) and [catalog-verification.md](catalog-verification.md#8-terms-of-use-per-publisher)); DOF-specific terms for the extract: to confirm.
- **Terms Status**: `pending` for the Open Data datasets. **Suggestion (not a decision): `blocked` for the ACRIS website**, based on the notice quoted above.

## Buildings Subject to HPD Jurisdiction

- **Publisher**: NYC Dept. of Housing Preservation and Development (HPD). Dataset [`kj4p-ruqc`](https://data.cityofnewyork.us/d/kj4p-ruqc), made public 2/14/2014. Data dictionary: [HPD Building Open Data.pdf](https://data.cityofnewyork.us/api/views/kj4p-ruqc/files/c8bfaa8d-0b3d-40c5-bf6c-ae4a133dc871?download=true&filename=HPD%20Building%20Open%20Data.pdf) (attached to the dataset).
- **Coverage**: not every Building. The description lists buildings where HPD has required registration, started litigation, received a complaint, started a work order (emergency repair, demolition or AEP), or added the property to the Alternative Enforcement Program ([metadata](https://data.cityofnewyork.us/api/views/kj4p-ruqc.json)).
- **Grain**: one row per HPD `buildingid`. On 2026-11-22: 381,934 rows, 381,934 distinct `buildingid`, 369,843 with a `bin`, 358,566 distinct `bin`.
- **Fields ✅**: `buildingid`, `boroid`, `boro`, `housenumber`, `lowhousenumber`, `highhousenumber`, `streetname`, `zip`, `block`, `lot`, `bin`, `communityboard`, `censustract`, `managementprogram`, `dobbuildingclassid`, `dobbuildingclass`, `legalstories`, `legalclassa`, `legalclassb`, `registrationid`, `lifecycle`, `recordstatusid`, `recordstatus`.
- **Legal unit counts**: **yes.** `legalclassa` is "the number of apartments in a multiple dwelling", and `legalclassb` is "the number of rooms in a multiple dwelling without individual baths and kitchens" ([metadata](https://data.cityofnewyork.us/api/views/kj4p-ruqc.json), [PDF](https://data.cityofnewyork.us/api/views/kj4p-ruqc/files/c8bfaa8d-0b3d-40c5-bf6c-ae4a133dc871?download=true&filename=HPD%20Building%20Open%20Data.pdf)). 337,435 Active rows have `legalclassa > 0`. A sample row: 424 East 14 Street, BIN 1006017, `dobbuildingclass` "NEW LAW TENEMENT", `legalstories` 5, `legalclassa` 23. Counts only, no unit list.
- **Watch out**:
  - No single BBL column. Build it from `boroid` + `block` + `lot`.
  - Placeholder BINs are common: 5,611 rows have `bin` in (1000000, 2000000, 3000000, 4000000, 5000000), and 356 Active rows have `bin = 0`. ADR 0004 already forbids matching on them.
  - Some rows have address and block/lot set to `0` (for example `buildingid` 859129, Inactive).
  - Filter on `recordstatus = 'Active'` and `lifecycle = 'Building'` (351,550 rows). Other lifecycles: `Land`, `Planned`, `UnderConstruction`, `Demolished`, `Undetermined`. Inactive rows include 10,669 demolished buildings, which are useful history.
  - `dobbuildingclass` is a DOB class "as augmented by HPD for other than Multiple Dwellings", not the DOF building class used in PLUTO.
  - `registrationid` links to HPD Multiple Dwelling Registrations (`tesw-yqqr`); `0` means no registration.
  - Same Publisher as HPD Multiple Dwelling Registrations, so the two are one Lineage Group.
  - The PDF describes XML and pipe-delimited files "named Buildingsyyyymmdd" with the date being "the last day of the quarter covered by the file", while also saying the data is "updated monthly". Whether those files are still published outside Socrata: to confirm.
- **Cadence**: monthly ("Update Frequency: Monthly", "Automation: Yes" in the [metadata](https://data.cityofnewyork.us/api/views/kj4p-ruqc.json)). Last updated 2026-11-05.
- **Access**: Socrata API. ([dataset](https://data.cityofnewyork.us/d/kj4p-ruqc))
- **Collection ladder**: **step 1** (Socrata API).
- **Use for this project**:
  - **units**: legal Class A unit count per Building, keyed by BIN. It is a second, independent Claim next to PLUTO `unitsres` (DCP/DOF, a different Lineage Group). Disagreement between them is a natural Review Queue item.
  - **attributes**: `legalstories`.
  - **identity**: address ranges (`lowhousenumber`/`highhousenumber`) per BIN, and lifecycle status (demolished, under construction).
  - **matching**: layer 1 (BIN), after dropping placeholder BINs.
- **Terms**: general NYC Open Data terms (the old terms page now returns 404; see the [Open Data FAQ](https://www.nyc.gov/opendata/get-started/FAQs) and [catalog-verification.md](catalog-verification.md#8-terms-of-use-per-publisher)). The dataset's attribution link points to an old HPD Open Data page (`http://www.nyc.gov/html/hpd/html/pr/HPD-Open-Data.shtml`); HPD-specific terms: to confirm.
- **Terms Status**: `pending`.

## DCP Housing Database

- **Publisher**: NYC Dept. of City Planning (DCP). Built from DOB job filings, permits and certificates of occupancy.
- **Location**:
  - Project level, tabular: [`br6q-ssj3`](https://data.cityofnewyork.us/d/br6q-ssj3) "Housing Database Project Level Files", current version `26Q2.1` (all 111,909 rows carry `version = 26Q2.1`).
  - Map view of the same data: [`ete7-a5jd`](https://data.cityofnewyork.us/d/ete7-a5jd).
  - [`6umk-irkx`](https://data.cityofnewyork.us/d/6umk-irkx) "Housing Database" is only a link to the DCP download page.
  - Aggregates (no Building grain, not useful here): by Community District `dbdt-5s7j`, 2020 NTA `kyz5-72x5`, 2020 CDTA `48dt-mn3z`, 2020 Census Block `8zyi-kxay`, 2020 Census Tract `nahe-je7c`, 2024 City Council `szq8-b4uy`.
  - DCP download page with all past versions: [housing-project-level](https://www.nyc.gov/content/planning/pages/resources/datasets/housing-project-level), according to the dataset description. The page renders only with JavaScript; the files it offers: to confirm.
  - Build code: [NYCPlanning/data-engineering, products/developments](https://github.com/NYCPlanning/data-engineering/tree/main/products/developments) (DCP's official GitHub, linked from the `ete7-a5jd` description).
- **Grain**: one row per DOB job (`job_number`); no duplicate `job_number` found. Job types: Alteration 63,090; New Building 35,188; Demolition 13,631. One Building can have many rows (one BIN has 162).
- **Fields ✅** (main ones): `job_number`, `job_type`, `job_status`, `residflag`, `nonresflag`, `classainit`, `classaprop`, `classanet`, `hotelinit`, `hotelprop`, `otherbinit`, `otherbprop`, `units_co`, `boro`, `bin`, `bbl`, `addressnum`, `addressst`, `occ_init`, `occ_prop`, `bldg_class`, `job_desc`, `datefiled`, `datepermit`, `datelstupd`, `datecomplt`, `compltyear`, `permityear`, `floorsinit`, `floorsprop`, `enlargemnt`, `ownership`, `landmark`, `latitude`, `longitude`, `geomsource`, `dcpedited`, `version`, `hpdaffrdbl`, `hpd_id`, `hpd_jobrel`, `nta2020`, `ntaname20`, `bctcb2020`. Plus zoning, school, fire, police and floodplain fields.
- **Unit changes per Building**: yes, per job. `classainit` (existing Class A units at application), `classaprop` (proposed), `classanet` (net change), `units_co` ("number of dwelling units provided on the temporary or final certificates of occupancy", may include Class B and hotel units). Summing completed jobs per BIN over time gives the change in legal units since 2010. Only jobs that affect residential units are included ("Only those jobs with a value of 'residential' are included" ([data dictionary](https://data.cityofnewyork.us/api/views/br6q-ssj3/files/2e79ebab-7ab2-4d2f-bad9-f9bc9b5caf7f?download=true&filename=Housing_Database_Data_Dictionary.xlsx))).
- **Watch out**:
  - Scope is jobs "filed or completed in NYC since January 1, 2010" ([metadata](https://data.cityofnewyork.us/api/views/br6q-ssj3.json)), but `datefiled` reaches back to 1998 for jobs completed after 2010. It is not a full history of a Building.
  - Withdrawn jobs are present (`job_status` "9. Withdrawn": 9,957 rows). The `ete7-a5jd` description says there are two versions, one with only active and completed jobs and one that includes inactive jobs; this Socrata table seems to be the one that includes them (to confirm). Filter on status before summing.
  - Most unit fields come from the applicant: "most of the information associated with a record is provided by the applicant, and not necessarily checked by the City" ([data dictionary](https://data.cityofnewyork.us/api/views/br6q-ssj3/files/2e79ebab-7ab2-4d2f-bad9-f9bc9b5caf7f?download=true&filename=Housing_Database_Data_Dictionary.xlsx)).
  - `classainit` is "Set to 0 for New Buildings" and `classaprop` is "Set to 0 for Demolitions" (same dictionary).
  - `geomsource` shows how each point was placed. 95,194 rows use the footprint matched by BIN; 14,630 use Geosupport coordinates; others use PLUTO or raw lat/lon.
  - 6 rows have a placeholder BIN (`_000000`).
  - Derived from DOB data already in the catalog (DOB NOW filings, Certificates of Occupancy). Treat DCP Housing DB and DOB as one Lineage Group for unit counts, so their agreement is not independent confirmation.
  - The build README says DCP gets some DOB NOW and certificate of occupancy data by email or FTP with credentials ([README](https://github.com/NYCPlanning/data-engineering/blob/main/products/developments/README.md)), so the Housing Database may hold certificate data not available in public DOB datasets.
- **Cadence**: every 6 months: "updated semiannually, at the end of the second and fourth quarters of each year" ([metadata](https://data.cityofnewyork.us/api/views/br6q-ssj3.json)). Latest load 2026-09-30; latest `datelstupd` 2026-08-07.
- **Access**: Socrata API ([dataset](https://data.cityofnewyork.us/d/br6q-ssj3)). Past versions on the DCP page (to confirm), which matters because Socrata keeps only the current version.
- **Collection ladder**: **step 1** (Socrata API).
- **Use for this project**:
  - **change signals**: a completed new building, alteration or demolition on a BIN marks its unit and floor Claims as Stale. It is cleaner than raw DOB filings because DCP removes administrative and test jobs.
  - **units**: `classaprop`/`units_co` of the latest completed job is a Claim for the current legal unit count. Lower-ranked than HPD `legalclassa` or PLUTO until checked.
  - **attributes**: `floorsprop`, completion year for new buildings (a check on PLUTO `yearbuilt`).
  - **matching**: BIN and BBL on every row.
- **Terms**: general NYC Open Data terms (the old terms page now returns 404; see the [Open Data FAQ](https://www.nyc.gov/opendata/get-started/FAQs) and [catalog-verification.md](catalog-verification.md#8-terms-of-use-per-publisher)); DCP-specific terms for the download page: to confirm.
- **Terms Status**: `pending`.

---

## Suggested catalog changes

1. Move these four Sources from "Not researched yet" into the catalog sections, all with Terms Status `pending`:
   - **Building identity**: add "Geoclient API (v2)" and "Geosupport Desktop Edition" as matching tools. Note that Geosupport, Geoclient and PAD are one Lineage Group.
   - **Units**: add "Buildings Subject to HPD Jurisdiction (`kj4p-ruqc`)" with `legalclassa` as a legal unit count per BIN.
   - **Units** and **Changes over time**: add "ACRIS Real Property (Master `bnx9-e6tj`, Legals `8h5j-fqxa`, plus code tables `7isb-wh4c`, `94g4-w6xz`)". Skip Parties (`636b-3b5g`) because it holds personal data the project does not need.
   - **Changes over time**: add "DCP Housing Database Project Level (`br6q-ssj3`)".
2. Add a separate line for the **ACRIS website** (document images) with a **suggested** `blocked` status, citing the DOF notice that denies access to automated scripts. The owner decides.
3. Update "The short version" table:
   - "Building attributes ... unit count" can also cite HPD Jurisdiction (`legalclassa`) and the DCP Housing Database.
   - "List of Units" can mention ACRIS Legals `unit` as a possible partial source for condos and co-ops, to confirm.
4. In the HPD Multiple Dwelling Registrations entry, note that `registrationid` joins it to HPD Jurisdiction, and that both are one Lineage Group (HPD).
5. In the DOB Certificates of Occupancy entry, note that the DCP Housing Database already includes certificate of occupancy unit counts (`units_co`) for jobs since 2010. That may cover part of the "later certificates" gap.
6. Add to the general Open Data rules: always keep the latest `good_through_date` per ACRIS document, and always filter by `recordstatus`/`lifecycle` (HPD) or `job_status` (DCP), since all three tables mix current and inactive records.

## Open items (to confirm)

- Geoclient rate limits, quotas and API-specific terms (need the portal pages, which require JavaScript or sign-up).
- Geosupport Desktop Edition: current download URL, latest release, whether stored outputs count as "derivatives", and whether it runs in a Linux container.
- ACRIS: what Legals rows with `borough = 5` are; whether condo unit deeds use unit BBLs in `lot`; how often co-op transfers carry `unit`; condo declarations before 2003.
- HPD Jurisdiction: whether the pipe-delimited/XML files are still published; HPD-specific terms.
- DCP Housing Database: whether `br6q-ssj3` is the "inactive included" version; which past versions the DCP page offers.
