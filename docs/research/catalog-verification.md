# Source catalog verification

Verification of the items in [`docs/source-catalog.md`](../source-catalog.md) that were marked "to confirm" or otherwise unverified.

- **Retrieval date**: 2026-11-22. All pages, metadata and files below were read on this date.
- **Method**: Socrata metadata API (`https://data.cityofnewyork.us/api/views/<id>.json`), attachments linked from that metadata, the Socrata catalog search API, DCP pages on nyc.gov (read through the nyc.gov content API that renders them), official PDFs, the official `CityOfNewYork/nyc-geo-metadata` repo, and the sites' own terms pages. No listing portal content was accessed beyond attempts to read terms pages.
- **Terms Status**: this document does not approve any Source. It reports what the terms say. Terms decisions belong to the project owner.

## Summary

| # | Item | Finding | Status |
|---|---|---|---|
| 1 | PAD address ranges | Yes. The address file is a table of address ranges (low and high house number per BIN, with parity). | verified |
| 1 | PAD condo crosswalk | Yes, as ranges: each BBL-file row maps a contiguous range of unit BBLs (low to high) to the condo billing BBL. It does not list unit BBLs one by one. | verified |
| 1 | PAD version and layout | DCP's page: **26D** (data of November 2026). NYC Open Data still says 26c. Zip holds `bobaadr.txt`, `bobabbl.txt`, `snd26Dcow.txt` and PDFs. The address file has 3 fields not in the published layout PDF. | verified |
| 2 | Building Footprints dataset ID | `5zhs-2jue` (named "BUILDING"), map view `jh45-qr5r`; historic (demolished) footprints `ipkp-snf6`. | verified |
| 2 | Building Footprints field names | Socrata field names are lowercase (`bin`, `base_bbl`, `mappluto_bbl`, ...) plus `last_edited_date`, `last_status_type`, `name`. | verified |
| 2 | Building Footprints cadence | Edited daily by OTI, published weekly. Open Data metadata says "Automation: No". | verified |
| 3 | PLUTO cadence | DCP's own page and readme: major release quarterly (all fields), minor release monthly (zoning fields only). | verified |
| 3 | PLUTO current version | DCP page: **26v3** (data of October 2026). Open Data `64uk-42ks` still says 26v2 (rows last updated 2026-08-24). | verified |
| 4 | DOF Condo Units cadence | Monthly in practice: extracted last Friday of each month, refreshed on the 1st; last row update 2026-11-01. The metadata field "Weekly" disagrees with the description. | verified (monthly); metadata field is inconsistent |
| 5 | DOB CO `bs8b-p36w` fields | 25 data fields read from metadata and data dictionary (list below). Dwelling units: `pr_dwelling_unit`, `ex_dwelling_unit`. | verified |
| 5 | DOB NOW CO dataset ID | `pkdm-hqz6`, "DOB NOW: Certificate of Occupancy", for COs since March 2021. | verified |
| 6 | StreetEasy terms | Every StreetEasy page tried (and Zillow's terms page) returned HTTP 403 to automated fetches. Clause not read. | to confirm |
| 7 | PLUTO vs Footprints lineage | Not independent for year built (both trace to DOF assessment data) or number of buildings (PLUTO counts Footprints BINs). Mostly independent for height (OTI) vs floors (DOF). | verified |
| 8 | Agency terms beyond NYC Open Data | DCP: BYTES "use limitations" (no-warranty disclaimer). DOF: dataset disclaimer. OTI: points to Open Data terms and NYC.gov Terms of Use. HPD, DOB: nothing found in metadata or attachments. None forbids automated use. Catalog's Open Data terms link is dead (404). | partly verified; HPD/DOB agency pages to confirm |

## 1. PAD (Property Address Directory), `bc8t-ecyu`

### Address ranges: yes

The DCP user guide says: "Addresses are expressed in PAD in the form of address ranges, specified by the borough code, the 5SC and the low and high house numbers of the range. A single address is represented in PAD as an address range in which the low and high house numbers are equal." Ranges are always one parity, except where a Continuous Parity Indicator is set. ([PAD user guide, padgui.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/padgui.pdf))

The address file (`bobaadr.txt`) carries, per row, `boro`, `block`, `lot`, `bin`, `lhnd`/`lhns` (low house number, display and sort formats), `hhnd`/`hhns` (high house number), `stname`, `addrtype`, `zipcode` and more. ([PAD file layout, padlayout.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/padlayout.pdf))

The user guide also documents address types that matter for matching: real address ranges, pseudo-addresses (no official status, "not likely to serve successfully as mailing addresses"), vanity addresses (for example 1049 Fifth Ave, whose entrance is on E. 86th St), and non-addressable place names (NAPs) such as STUYVESANT TOWN. ([padgui.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/padgui.pdf))

### Condo crosswalk: yes, as BBL ranges

The user guide: "Condo lots ... are represented as a range of contiguous BBLs contained in a single building of a Condo complex. The loboro, loblock, and lolot fields represent the Low BBL of this contiguous range of BBLs and the hiboro, hiblock, and hilot fields represent the High BBL ... The billboro, billblock, and billlot fields represent the DOF Condo Billing BBL for this range." ([padgui.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/padgui.pdf))

Checked in the 26D data: rows with `condoflag = "C"` exist (26,448 of 874,268 BBL rows). Example row: low BBL 1-00004-1001, high BBL 1-00004-1052, billing BBL 1-00004-7501, condo number 0835. ([pad_26d.zip](https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/pad/pad_26d.zip))

Consequence: PAD gives billing BBL ↔ unit BBL *range* per condo building, not a list of units. Expanding a range into individual unit BBLs assumes the range has no holes; DOF Condo Units (`eguu-7ie3`) lists each unit BBL explicitly and is the better source for the unit list. PAD's range is a useful cross-check (different Publisher, but see note on lineage: both trace to DOF tax lots).

### Version and file layout

- DCP page: "Update Frequency: Quarterly", "Latest Release: 26D", "Date of Data: November 2026". ([DCP PAD page](https://www.nyc.gov/content/planning/pages/resources/datasets/pad))
- NYC Open Data `bc8t-ecyu` description: "Current version: 26c". It is a file (blob) asset named `pad.zip`, not a table, and has no columns in the API. Metadata: Update Frequency Quarterly, Automation Yes. ([metadata](https://data.cityofnewyork.us/api/views/bc8t-ecyu.json), [dataset](https://data.cityofnewyork.us/d/bc8t-ecyu))
- So on the retrieval date the Open Data copy lagged DCP by one release. DCP's direct zip is the more current Source.
- Contents of `pad_26d.zip` (listed with `unzip -l`): `bobaadr.txt` (address file, ~1.33M rows), `bobabbl.txt` (BBL file, ~874k rows), `snd26Dcow.txt` (Street Name Dictionary), plus PDFs "Bytes of the Big Apple Property Address Directory.pdf", "Bytes of the Big Apple Street Name Dictionary.pdf", `SND_metadata.pdf`. Both PAD files are quoted, comma-delimited, with a header row.
- **Layout drift**: the header of `bobaadr.txt` in 26D has `dapsflag`, `naubflag` and `physical_id`, which do not appear in the [layout PDF](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/padlayout.pdf). Their meaning: to confirm (not found in padlayout.pdf; the user guide was searched only for condo and range terms). The BBL file header matches the layout: `loboro, loblock, lolot, lobblscc, hiboro, hiblock, hilot, hibblscc, boro, block, lot, bblscc, billboro, billblock, billlot, billbblscc, condoflag, condonum, coopnum, numbf, numaddr, vacant, interior`.
- Note: the column descriptions in `padlayout.pdf` are shifted by one row against the field names when the PDF is extracted as text; the user guide's field table is easier to read.

## 2. Building Footprints

### Dataset IDs

Found with the Socrata catalog API ([query](https://api.us.socrata.com/api/catalog/v1?domains=data.cityofnewyork.us&q=building%20footprints)):

| ID | Name | Type | Notes |
|---|---|---|---|
| `5zhs-2jue` | BUILDING | dataset (table) | Current footprints. Created on Socrata 2024-11-13; "Date Made Public" 5/3/2016. ([metadata](https://data.cityofnewyork.us/api/views/5zhs-2jue.json), [dataset](https://data.cityofnewyork.us/d/5zhs-2jue)) |
| `jh45-qr5r` | Building Footprints (Map) | map | Map view of the same data. ([metadata](https://data.cityofnewyork.us/api/views/jh45-qr5r.json)) |
| `u9wf-3gbt` | BUILDING_P | dataset | Centroid points. |
| `ipkp-snf6` | BUILDING_HISTORIC | dataset | Historic footprints; may help detect demolitions. |
| `9xsq-wn7d` | BUILDING_HISTORIC_P | dataset | Historic centroid points. |

All are attributed to the Office of Technology and Innovation (OTI). The `5zhs-2jue` description links to the GitHub metadata the catalog already cites.

### Field names (Socrata `5zhs-2jue`)

`the_geom`, `name`, `bin`, `doitt_id`, `shape_area`, `base_bbl`, `objectid`, `construction_year`, `feature_code`, `geom_source`, `ground_elevation`, `height_roof`, `last_edited_date`, `last_status_type`, `mappluto_bbl`, `shape_length`. ([metadata](https://data.cityofnewyork.us/api/views/5zhs-2jue.json))

Compared with the catalog: all nine listed fields exist, but in lowercase on Socrata. New fields worth recording: `last_edited_date` and `last_status_type` (values include Demolition, Alteration, Geometry, Initialization, Correction, Marked for Construction, Marked For Demolition, Constructed), useful as Stale signals. `GLOBALID` is "not published in all datasets" and is absent here. ([GitHub metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md))

The other "Watch out" items in the catalog were re-read in the GitHub metadata and are correct: million BINs are placeholders and BIN is not unique; split buildings keep the original BIN ("BINs will be duplicated in these cases"); `BASE_BBL` can be out of sync "due to temporary synchronziation issues between city agencies"; Area and Length are "Do not use"; features captured are "All buildings >400 sq. feet and taller than 12 feet" plus others with BINs. Additional: `FEATURE_CODE = 1003` is a placeholder triangle, and `NAME` "has not been actively maintained". ([GitHub metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md))

### Update cadence

- GitHub metadata: "Last Update: Weekly", "Update Frequency: Features are updated daily by OTI staff and released publicly on NYC Open Data and NYCMaps." Metadata date 10/09/2025. ([GitHub metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md))
- Open Data metadata for `5zhs-2jue`: "Update Frequency: Weekly", "Automation: No". Rows last updated 2026-11-23 00:17 UTC. ([metadata](https://data.cityofnewyork.us/api/views/5zhs-2jue.json))

## 3. PLUTO, `64uk-42ks`

### Release cadence: confirmed on the city's own page

DCP page: "There are two types of PLUTO updates: major and minor. Major updates occur quarterly, and all fields are updated. Minor updates are released monthly between major updates and only include updates to the zoning attributes." The same page lists "Update Frequency: Monthly". ([DCP PLUTO page](https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change))

The PLUTO readme says the same and explains the numbering: major = digit after "v" (24v1), minor = decimal (24v1.1). ([pluto_readme.pdf, Open Data attachment for 26v2](https://data.cityofnewyork.us/api/views/64uk-42ks/files/b1acde6a-307f-4050-a2d3-301fe9bfb1f0?download=true&filename=pluto_readme.pdf); current copy on [DCP](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/pluto_readme.pdf))

Consequence for us: building fields such as `numfloors`, `unitsres`, `yearbuilt` change only on major releases (quarterly).

### Current version

- DCP page: "Latest Release: 26v3", "Date of Data: October 2026". Download: `nyc_pluto_26v3_csv.zip`. ([DCP PLUTO page](https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change))
- Open Data `64uk-42ks` description: "Current version: 26v2"; rows last updated 2026-08-24. Metadata says Quarterly, Automation Yes. ([metadata](https://data.cityofnewyork.us/api/views/64uk-42ks.json))
- So the Open Data table lagged DCP by one release on the retrieval date. Whether DCP's 26v3 is a major release: to confirm (the 26v3 readme was not read; only the 26v2 readme attached to Open Data was).

## 4. DOF Digital Tax Map: Condominium Units, `eguu-7ie3`

- Description: "Data is extracted from DOF's internal system on the last Friday of each month and refreshed on ArcGIS Online on the 1st." ([metadata](https://data.cityofnewyork.us/api/views/eguu-7ie3.json))
- Metadata fields: "Update Frequency: Weekly", "Data Change Frequency: Daily", "Update Frequency Details: DOF Tax Map Unit (TMU) makes daily edits to the Tax Map that can be observed on DOF's Property Information Portal." ([metadata](https://data.cityofnewyork.us/api/views/eguu-7ie3.json))
- Observed: rows last updated 2026-11-01 15:03 UTC (the 1st of the month), matching the monthly description. One observation only.
- Reading: the underlying tax map changes daily; the published table is refreshed monthly. The "Weekly" field appears inconsistent with both the description and the observed update. Treat the cadence as monthly and track the actual `rowsUpdatedAt` over time.
- The description also says the Tax Map alternates between "Set A" and "Set B" each month, and carries a disclaimer: it "may not reflect the latest changes in other City systems (e.g., exemptions or buildings data). It is provided for informational purposes only and is not guaranteed to be accurate as of today's date."
- Full field list (16): `condo_base_boro`, `condo_base_block`, `condo_base_lot`, `condo_base_bbl`, `condo_number`, `condo_key`, `condo_base_bbl_key`, `unit_boro`, `unit_block`, `unit_lot`, `unit_bbl`, `unit_designation`, `floor_text`, `model`, `geometry_type`, `effective_tax_year`.

## 5. DOB Certificates of Occupancy

### `bs8b-p36w` (DOB Certificate Of Occupancy, 7/12/2012 to March 2021)

Data fields from the metadata ([metadata](https://data.cityofnewyork.us/api/views/bs8b-p36w.json)): `job_number`, `job_type`, `c_o_issue_date`, `bin_number`, `borough`, `house_number`, `street_name`, `block`, `lot`, `postcode`, `pr_dwelling_unit`, `ex_dwelling_unit`, `application_status_raw`, `filing_status_raw`, `item_number`, `issue_type`, `latitude`, `longitude`, `community_board`, `council_district`, `census_tract`, `bin`, `bbl`, `nta`, `location`; plus five Socrata computed region columns (`:@computed_region_*`).

Notes from the data dictionary ([DD_DOB_Certificate_Of_Occupancy.xlsx](https://data.cityofnewyork.us/api/views/bs8b-p36w/files/c85974d4-39be-4625-b5c3-03b36afc476d?download=true&filename=DD_DOB_Certificate_Of_Occupancy.xlsx)):

- `pr_dwelling_unit`: "the proposed number of dwelling units in the building after the proposed work has been completed, as reported by the applicant". `ex_dwelling_unit`: existing units "as reported by the applicant". So these are applicant-reported, not a DOB count.
- `bin_number` comes from DOB's BIS database; `bin` and `bbl` are added later by geocoding the address ("Geocoded based on address"). The two BINs can differ.
- `block` and `lot` are as submitted on the job application and "may not reflect the current data for the building".
- `job_type` values include A1 (major alteration) and NB (new building).
- Metadata: Update Frequency Daily, Automation Yes; rows last updated 2026-11-20 even though coverage ends in March 2021.
- The description confirms: "PDFs of the actual COs are viewable in www.nyc.gov/bis."

### DOB NOW: Certificate of Occupancy, `pkdm-hqz6` (March 2021 onward)

- The `bs8b-p36w` description links to it: "For COs issued since March 2021, see DOB NOW: Certificate of Occupancy dataset." ([dataset](https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Certificate-of-Occupancy/pkdm-hqz6), [metadata](https://data.cityofnewyork.us/api/views/pkdm-hqz6.json))
- Fields: `job_filing_name`, `job_type`, `bin`, `borough`, `house_no`, `street_name`, `block`, `lot`, `zip_code`, `submitted_date`, `c_of_o_status`, `c_of_o_sequence`, `c_of_o_filing_type`, `community_board`, `c_of_o_issuance_date`, `application_number`, `number_of_dwelling_units`, `c_of_o_number`, `latitude`, `longitude`, `citycouncildistrict`, `bbl`, `censustract2010`, `ntaname`.
- Unlike the older dataset, it has a single `number_of_dwelling_units` (no proposed/existing pair).
- Cadence conflict: metadata says "Update Frequency: Daily"; the data dictionary says "Publishing Frequency: Monthly" and "This data will initiallly be published on Open Data on a monthly basis." Rows last updated 2026-11-21. ([data dictionary](https://data.cityofnewyork.us/api/views/pkdm-hqz6/files/90b77d47-f8e5-49a7-b020-ea3e23624c9c?download=true&filename=Data%20Dictionary%20-%20DOB%20NOW%20Certificate%20of%20Occupancy_FINAL.xlsx))
- The data dictionary says block, lot, borough and address are "Supplied by DOB NOW applicant"; it gives the agency site as `https://a810-dobnow.nyc.gov/publish/Index.html#!/` and says rows are not removed on update.

## 6. StreetEasy terms of use

**Status: to confirm.** The clause could not be read.

What was tried, on 2026-11-22:

- `https://streeteasy.com/terms`, `https://streeteasy.com/terms-of-use`, `https://streeteasy.com/info/terms-of-use`: HTTP 403 ("Access to this page has been denied") from both a command-line request and the fetch tool.
- `https://streeteasy.com/adterms` (StreetEasy's advertiser "Terms of Service", found by web search): HTTP 403.
- Zillow's terms page (`https://www.zillow.com/corp/Terms.htm`): HTTP 403. StreetEasy is described in search results as a Zillow brand; whether Zillow's terms of use cover StreetEasy is to confirm on the primary page.
- No further attempts were made, to stay within the "terms pages only, no scraping" rule.

Suggested next step for the owner: open StreetEasy's terms page in a normal browser (linked from the site footer), copy the automated-access clause and its date into the catalog. The site blocking automated requests to its own terms page is itself a sign that it does not want automated access, but this is an observation, not the terms.

For comparison, Redfin's own terms, read directly on 2026-11-22 (last updated September 29, 2025), section 2.3.5 "No Scrubbing or Scraping": "You may not automatedly crawl or query the Services for any purpose or by any means (including, without limitation, screen and database scraping, spiders, robots, crawlers and any other automated activity with the purpose of obtaining information from the Services) unless you have received prior express written permission from the applicable Redfin Company." ([Redfin Terms of Use](https://www.redfin.com/about/terms-of-use)). **Suggestion**: `blocked` is consistent with this text; the owner decides.

## 7. Do PLUTO and Building Footprints derive from each other?

Yes, for some fields. Their agreement on those fields should not count as independent confirmation.

What the primary documents say:

| Field pair | PLUTO source | Footprints source | Independent? |
|---|---|---|---|
| `yearbuilt` vs `construction_year` | DOF Property Tax System (PTS); for ~26,000 buildings in historic districts replaced by LPC's database date. ([PLUTO data dictionary](https://data.cityofnewyork.us/api/views/64uk-42ks/files/153f6ffb-8789-450e-9266-774cb9cd2b77?download=true&filename=pluto_datadictionary.pdf)) | "Originally this column was populated using the Department of Finance Real Property Assessment Database (RPAD). After 2017 we used imagery and city information systems to populate this value in real time." ([GitHub metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md)) | **No** for buildings populated from RPAD (DOF's predecessor system to PTS, per the PLUTO readme). Possibly yes for post-2017 footprints, but a row does not say which method set it. |
| `numbldgs` vs count of footprints | "calculated by taking the BIN for every building in OTI's Building Footprints dataset, running Geosupport function BN to get the BBL ... and summing" ([data dictionary](https://data.cityofnewyork.us/api/views/64uk-42ks/files/153f6ffb-8789-450e-9266-774cb9cd2b77?download=true&filename=pluto_datadictionary.pdf)) | Footprints itself | **No.** PLUTO's value is derived from Footprints. |
| `numfloors` vs `height_roof` | DOF PTS. DCP once corrected ~20 values "for buildings for which NUMBER OF FLOORS was not consistent with the height of the building in DoITT's Building Footprints". ([readme](https://data.cityofnewyork.us/api/views/64uk-42ks/files/b1acde6a-307f-4050-a2d3-301fe9bfb1f0?download=true&filename=pluto_readme.pdf)) | DOB plan drawings, EagleView oblique imagery, Cyclomedia imagery. ([GitHub metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md)) | **Mostly yes**, and they measure different things (floors vs feet). A small number of PLUTO values were edited using Footprints. |
| `bbl` vs `mappluto_bbl` / `base_bbl` | DOF tax lots; condos aggregated to the billing lot. | `mappluto_bbl` exists "for joining the building footprints data to DCP's MapPLUTO data". | **No.** These are join keys built to match. |
| Building location | PLUTO's source list includes "Office of Technology & Innovation – Building Footprint Centroids". ([readme](https://data.cityofnewyork.us/api/views/64uk-42ks/files/b1acde6a-307f-4050-a2d3-301fe9bfb1f0?download=true&filename=pluto_readme.pdf)) | Footprints itself | **No** (which PLUTO field uses the centroids: to confirm). |
| `unitsres`, `bldgclass` | DOF PTS (condo values summed from unit lots). | Not in Footprints. | n/a |

Wider upstream: PLUTO lists its sources as DCP, DOF, DCAS and LPC data, including DOF's Digital Tax Map, DOF's CAMA, Geosupport 26C and OTI Building Footprint Centroids. ([readme](https://data.cityofnewyork.us/api/views/64uk-42ks/files/b1acde6a-307f-4050-a2d3-301fe9bfb1f0?download=true&filename=pluto_readme.pdf)) This means PLUTO also shares upstream with DOF Condo Units (`eguu-7ie3`, the Digital Tax Map) and with PAD (Geosupport/DCP).

Suggested Lineage Groups (for the owner to decide, per ADR 0005): put PLUTO and DOF datasets in one group for `yearbuilt`, `numfloors`, unit counts and BBL fields; put PLUTO `numbldgs` and Footprints in one group. Height (Footprints) vs floors (PLUTO) can be treated as independent with a note.

## 8. Terms of use, per publisher

### General NYC Open Data terms

- The catalog links `https://www.nyc.gov/html/data/terms.html`. On 2026-11-22 it returns **HTTP 404**.
- The last archived copy (Wayback Machine, 2025-04-01, [snapshot](http://web.archive.org/web/20250401004630/https://www.nyc.gov/html/data/terms.html)) said: "the user agrees to all of the Terms of Use of NYC.gov as well as the Privacy Policy for NYC.gov. The user also agrees to any additional terms of use defined by entities providing data or feeds through the Site." and "Older versions of data sets will not be retained." This matches what the catalog says, but it is an archived copy of a page that no longer exists.
- The current NYC Open Data FAQ says: "Are there restrictions on how I can use Open Data? Open Data belongs to all New Yorkers. There are no restrictions on the use of Open Data." ([NYC Open Data FAQs](https://www.nyc.gov/opendata/get-started/FAQs))
- The Open Data site's footer now links the general [NYC.gov Terms of Use](https://www.nyc.gov/main/terms-of-use). That page has no section on Open Data or datasets. It says content is "the property of the City of New York. All rights are reserved", disclaims warranties "WITH RESPECT TO THE QUALITY, CONTENT, ACCURACY, COMPLETENESS, CURRENCY", and directs requests to use City intellectual property to the relevant agency. No last-updated date is shown.
- Whether the FAQ's "no restrictions" or the NYC.gov "all rights reserved" governs Open Data downloads, now that the dedicated terms page is gone: to confirm (owner decision; possibly by asking the Open Data team via its [contact page](https://www.nyc.gov/opendata/contact-us)).
- None of the Socrata metadata records in the catalog sets a `license` (all `null`).

### Per publisher

| Source | Publisher | Agency-specific terms found | Where |
|---|---|---|---|
| PAD `bc8t-ecyu` | DCP | Yes, "Use limitations" for BYTES of the BIG APPLE: data "provided ... for informational purposes only. DCP does not warranty the completeness, accuracy, content, or fitness for any particular purpose ..." No restriction on automated use or redistribution. | [DCP PAD page](https://www.nyc.gov/content/planning/pages/resources/datasets/pad), "Access & Use Information" |
| PLUTO `64uk-42ks` | DCP | Same BYTES use limitations text. | [DCP PLUTO page](https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change) |
| Building Footprints `5zhs-2jue` | OTI | "Use Limitations: Open Data policies and restrictions apply. See Terms of Use" (links the old Open Data overview, which now redirects to a page without terms). The ArcGIS item "Building" has license info "NYC.gov Terms of Use". | [GitHub metadata](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_BuildingFootprints.md); [ArcGIS item JSON](https://www.arcgis.com/sharing/rest/content/items/870bf69e8a8044aea4488e564c0b4010?f=json) |
| DOF Condo Units `eguu-7ie3` | DOF | Disclaimer in the description (informational only, not guaranteed accurate). ArcGIS items Set A and Set B have empty license info. | [metadata](https://data.cityofnewyork.us/api/views/eguu-7ie3.json); [Set A item JSON](https://www.arcgis.com/sharing/rest/content/items/4da1c8c5f64d4771ae5861dd8ea3775c?f=json) |
| HPD Registrations `tesw-yqqr` | HPD | None found in metadata or the attached PDF. HPD's own site terms: to confirm (not checked). | [metadata](https://data.cityofnewyork.us/api/views/tesw-yqqr.json); [HPD Registration Open Data.pdf](https://data.cityofnewyork.us/api/views/tesw-yqqr/files/54b2086b-b656-49cb-8db8-14b3f1dcf05b?download=true&filename=HPD%20Registration%20Open%20Data.pdf) |
| DOB NOW Build `w9ak-ipjd` | DOB | None found in metadata or data dictionary. DOB's own site terms: to confirm (not checked). | [metadata](https://data.cityofnewyork.us/api/views/w9ak-ipjd.json) |
| DOB CO `bs8b-p36w`, `pkdm-hqz6` | DOB | None found in metadata or data dictionaries. | [metadata](https://data.cityofnewyork.us/api/views/bs8b-p36w.json), [metadata](https://data.cityofnewyork.us/api/views/pkdm-hqz6.json) |

No terms found for any NYC Source forbid automated access. Nothing here suggests `blocked` for any city Source.

### Other findings along the way

- **HPD cadence conflict**: Open Data metadata says Monthly (Automation Yes); the attached PDF says "The registration information in this file is updated quarterly, normally as of April 30, July 31, October 30 and January 31." The PDF describes an older XML file format, so it may be out of date. Rows last updated 2026-11-04. ([metadata](https://data.cityofnewyork.us/api/views/tesw-yqqr.json), [PDF](https://data.cityofnewyork.us/api/views/tesw-yqqr/files/54b2086b-b656-49cb-8db8-14b3f1dcf05b?download=true&filename=HPD%20Registration%20Open%20Data.pdf))
- **HPD garden complexes**: "a registration may apply to more than one building ... there will be more than one Registration element with the same RegistrationID" with different BuildingIDs. So `registrationid` is not unique per Building; `buildingid` is the building key. (same PDF)
- **Catalog cites non-primary sources**: the Zillow and Redfin terms links point to `conductatlas.com`, a third-party summary site. Redfin's own page was read (section 6). Zillow's own page returned 403: to confirm.

## Suggested catalog changes

1. **PAD**: replace "Address ranges and condo crosswalk: to confirm" with: address file gives address ranges (low/high house number, parity) per BIN; BBL file maps each condo building's unit-BBL range (low/high) to the billing BBL. Not a unit-by-unit list.
2. **PAD**: version is 26D on DCP (November 2026); Open Data `bc8t-ecyu` lagged at 26c. Prefer DCP's direct zip (`pad_YYx.zip`) as the Fetch target, and record the version per Fetch. Add the file names `bobaadr.txt`, `bobabbl.txt`. Note that the address file has `dapsflag`, `naubflag`, `physical_id` not in the layout PDF.
3. **PAD**: add a "Watch out" for pseudo-addresses, vanity addresses and NAPs (`addrtype`).
4. **Building Footprints**: set the dataset ID to `5zhs-2jue` (map `jh45-qr5r`); mention `ipkp-snf6` (historic). Use lowercase Socrata field names. Add `last_edited_date` and `last_status_type`. Note "Automation: No" on Open Data. Placeholder footprints have `feature_code = 1003`.
5. **PLUTO**: replace the mirror-based cadence note with the DCP page's text (quarterly major, all fields; monthly minor, zoning only). Version on DCP is 26v3 (October 2026); Open Data `64uk-42ks` lagged at 26v2. Decide whether to Fetch from DCP directly.
6. **PLUTO**: add data sources per field: `numfloors`, `unitsres`, `yearbuilt` from DOF PTS (`yearbuilt` partly from LPC, flagged by `dcpedited`); `numbldgs` from OTI Footprints.
7. **DOF Condo Units**: cadence is monthly (extract last Friday, refresh on the 1st); the "Weekly" metadata field is inconsistent. Add the full 16-field list and the Set A / Set B note.
8. **DOB Certificates of Occupancy**: fill the field list for `bs8b-p36w`; add `pkdm-hqz6` as the DOB NOW CO dataset with its fields. Note that dwelling unit counts are applicant-reported, that `bin_number` (BIS) and `bin` (geocoded) can differ, and that the DOB NOW CO cadence is stated as both Daily and Monthly.
9. **HPD Registrations**: note the Monthly vs quarterly conflict, and that `registrationid` can cover several buildings (use `buildingid`).
10. **Lineage Groups**: record that PLUTO and Footprints are not independent for year built, number of buildings, BBL and location; and that PLUTO, PAD and DOF Condo Units share DOF tax-lot upstream. Owner to decide the groups in the seed.
11. **General terms**: replace the dead link `https://www.nyc.gov/html/data/terms.html` (404). Cite the [Open Data FAQ](https://www.nyc.gov/opendata/get-started/FAQs) ("There are no restrictions on the use of Open Data") and the [NYC.gov Terms of Use](https://www.nyc.gov/main/terms-of-use); keep the archived text only as history. Keep "no old versions retained" but mark its source as the archived page.
12. **Agency terms**: add DCP's BYTES use limitations (no-warranty disclaimer) to PAD and PLUTO, and DOF's disclaimer to Condo Units. HPD and DOB agency terms remain to confirm. All Terms Status values stay `pending` until the owner decides.
13. **Listing portals**: replace the `conductatlas.com` links with primary sources: [Redfin Terms of Use](https://www.redfin.com/about/terms-of-use) section 2.3.5 (quoted above). Zillow and StreetEasy primary terms pages returned 403 to automated requests; the owner should read them in a browser and record the clause and date.
