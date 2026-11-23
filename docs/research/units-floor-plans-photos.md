# Sources for Units, Floor Plans and Photos

Research into possible Sources for the three Gaps in `docs/source-catalog.md`: unit-level detail (unit lists for rentals, bedrooms, size), Floor Plans and Photos.

Researched on 2026-11-22. Only terms pages, `robots.txt` files, official documentation and dataset metadata were read. No listing, building page, photo or floor plan was collected. Dataset fields come from each dataset's own metadata (`https://data.cityofnewyork.us/api/views/<id>.json`); no rows were downloaded.

**Suggested status** is only a suggestion for the owner. Nothing here is `approved`. `pending` means the owner should read the terms; `blocked` is suggested only where the text forbids automated use clearly.

**Fetch notes.** Several sites refused our requests, so some facts could not be read on the page itself:

- DOB BIS (`a810-bisweb.nyc.gov`) and DOB NOW (`a810-dobnow.nyc.gov`) answered `403` with the message *"Access is restricted to locations within the United States. For security reasons, any attempt to connect from outside the country will be blocked."*
- `loc.gov`, `streeteasy.com`, `zillow.com`, `trulia.com` and `apartments.com` answered `403` to both our fetch tools. Where this file uses them, the text comes from search-engine snippets of the official page. Those spots are marked **(snippet)** and still need checking on the page.
- `housingconnect.nyc.gov` refused the connection.

## Summary

| Source | What it offers | Access | Terms summary | Suggested status |
|---|---|---|---|---|
| HPD Housing Maintenance Code Violations (`wvxf-dwi5`) | `apartment` and `story` per violation, with BIN/BBL | Socrata API | NYC Open Data terms | `pending` |
| HPD Complaints and Problems (`ygpa-z7cr`) | `apartment`, `unit_type`, `space_type` per complaint | Socrata API | NYC Open Data terms | `pending` |
| DOF Rolling Sales (`usep-8jbt`) | `apartment_number`, units and gross sq ft per sale | Socrata API | NYC Open Data terms | `pending` |
| DOF Property Valuation and Assessment (`8y4t-faws`) | `aptno`, `coop_apts`, `units`, `gross_sqft`, `residential_area_gross` | Socrata API | NYC Open Data terms | `pending` |
| ACRIS Real Property Legals (`8h5j-fqxa`) | `unit` per recorded document | Socrata API | NYC Open Data terms. The ACRIS website itself blocks scripts | `pending` (Open Data); website: suggest `blocked` |
| HPD Affordable Housing Production by Building (`hg8x-zxpr`) | Count of studio and 1–6 BR units per building | Socrata API | NYC Open Data terms | `pending` |
| HPD Housing Connect lotteries by Building (`nibs-na6y`) | Studio to 4 BR unit mix per advertised lottery | Socrata API | NYC Open Data terms | `pending` |
| HPD Local Law 44 Unit Income Rent (`9ay9-xkek`) | Units by bedroom size and rents per building | Socrata API | NYC Open Data terms | `pending` |
| HPD Buildings Subject to HPD Jurisdiction (`kj4p-ruqc`) | `legalclassa` and `legalclassb` (legal unit counts), `legalstories` | Socrata API | NYC Open Data terms | `pending` |
| DOB NOW: Certificate of Occupancy (`pkdm-hqz6`) | CO records after DOB NOW, `number_of_dwelling_units` | Socrata API | NYC Open Data terms | `pending` |
| DOB Certificate of Occupancy PDFs (BIS / DOB NOW) | Scanned COs, one building at a time | Web portal only, US-only | NYC.gov Terms of Use | `pending` (manual only) |
| DOB approved plans and drawings | Plans filed with job applications | Records request with notarized owner authorization | Access is limited to owners and people they authorize | suggest `blocked` (access requirement) |
| HPD Online I-cards | Historical building index cards | HPD Online website | NYC.gov Terms of Use | `pending`; content to confirm |
| Municipal Archives 1940s and 1980s tax photos | One photo per building, searchable by block and lot | Preservica website; prints by order | Non-commercial use exempt from licensing; credit line required | `pending` |
| LPC designation reports and datasets | Reports on landmarks (PDF links in `buis-pvji`); building database (`gpmc-yuvp`) | Open Data plus PDFs on nyc.gov | NYC.gov terms: City property, all rights reserved | `pending` |
| Rent Guidelines Board stabilized building lists | Buildings with at least one stabilized unit; no unit list | PDF per borough | No specific terms; NYC.gov footer terms | `pending` |
| Housing Connect portal | Lottery listings | Website (refused our connection) | HPD/HDC terms, nothing on automation found | `pending`; prefer the Open Data copies |
| Library of Congress HABS/HAER/HALS | Measured drawings (incl. floor plans) and photos of historic buildings | loc.gov JSON API | "No known restrictions" on US Government–made images **(snippet)** | `pending` |
| NYPL Digital Collections | Historic NYC photos; public-domain items free to reuse | Website; the Repo API was due to shut on 2026-08-01 | Public-domain items free to reuse; others vary | `pending` |
| Wikimedia Commons | Photos under per-file free licenses | MediaWiki API, dumps | License per file; User-Agent policy wants contact info | `pending` |
| Vivmark Residential (equityapartments.com, avaloncommunities.com) | Building pages, Floor Plans, Photos | Website | Forbids robots and scrapers; Content includes "floor plans" | suggest `blocked` |
| Stonehenge NYC | Building pages, unit images | Website | Forbids "any automated means" | suggest `blocked` |
| Fetner Properties | Building pages | Website | Forbids "any robot, spider or other automatic device" | suggest `blocked` |
| Rudin (rudin.com, rudinresidential.com) | Building pages | Website | Forbids users to "harvest any information"; personal non-commercial license | suggest `blocked` |
| Related Rentals | Building pages, Floor Plans, Photos | Website | Personal non-commercial license; no general robot clause found | `pending` |
| Greystar | Building pages, Photos | Website | View and copy "solely for your personal, non-commercial use"; no robot clause found | `pending` |
| LeFrak | Building pages | Website | Download "for non-commercial, personal use only"; no robot clause; `Crawl-delay: 10` | `pending` |
| Glenwood Management | Building pages, listings | Website | No terms page found. Disclaimer: listings "may not be re-published" without consent | `pending` |
| TF Cornerstone | Building pages | Website | Terms page is rendered by JavaScript; text not read | `pending` (to confirm) |
| StreetEasy / Zillow / Trulia | Units, Photos, Floor Plans | Website; Bridge API for some Zillow datasets | Zillow terms forbid automated queries **(snippet)**; StreetEasy `robots.txt` disallows `/building/*/floorplans` | suggest `blocked` |
| Redfin | Units, Photos, Floor Plans | Website | "No Scrubbing or Scraping" | suggest `blocked` |
| Realtor.com (Move) | Units, Photos, Floor Plans | Website | Forbids scraping and "any automated means" | suggest `blocked` |
| RentHop | Rental units, Photos | Website | "Any automated means of accessing the Site ... is prohibited" | suggest `blocked` |
| Compass | Units, Photos, Floor Plans | Website | Forbids crawling, spidering and scraping | suggest `blocked` |
| Apartments.com (CoStar) | Units, Photos, Floor Plans | Website | Terms bind bots and forbid scraping **(snippet)** | suggest `blocked` (to confirm on page) |
| REBNY RLS feed | NYC broker listing data | IDX/VOW/other feeds, for RLS participants only | Data license; members only | `pending`; not open to this project |

## 1. Public and government Sources

### Rules shared by NYC Sources

- **NYC.gov Terms of Use**, Section IV ([nyc.gov/main/terms-of-use](https://www.nyc.gov/main/terms-of-use)): *"All other design, information, text, graphics, images, pages, interfaces, links, software, and other items and materials contained in or displayed on NYC.gov, and the selection and arrangements thereof, are the property of the City of New York. All rights are reserved."* To reuse them: *"To request permission to use City intellectual property located on NYC.gov, please visit the List of NYC Agencies and then contact the appropriate agency."* The terms have no clause on crawling or `robots.txt`. The closest is a ban on any use that would *"disrupt NYC.gov or its servers or networks in any way"* (Section I.A).
- **`www.nyc.gov/robots.txt`**: `User-agent: *` / `Disallow: /html/misc/`. Nothing else.
- **NYC Open Data**: the terms are already summarized in the catalog. `data.cityofnewyork.us/robots.txt` sets `Crawl-delay: 1` and disallows browse and search pages, `/OData.svc/`, `/api/odata/` and `/tiles/`. It does not disallow the SODA resource API. The Open Data Law (NYC Admin. Code § 23-502(d)) is reported to require that public data sets be available "without any registration requirement, license requirement or restrictions on their use". **To confirm**: the official code site ([codelibrary.amlegal.com](https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/0-0-0-204578)) returned `403`, so we could not read the official text.

### Unit-level data on NYC Open Data

None of these is a complete unit list for rental buildings. Together they give partial unit numbers and, for subsidized buildings, bedroom mixes.

| Dataset | Publisher | Unit-level fields (from metadata) | What it can fill |
|---|---|---|---|
| [Housing Maintenance Code Violations `wvxf-dwi5`](https://data.cityofnewyork.us/d/wvxf-dwi5) | HPD | `apartment`, `story`, `bin`, `bbl`, `buildingid` | Unit numbers in rentals, but only for units that ever had a violation |
| [Housing Maintenance Code Complaints and Problems `ygpa-z7cr`](https://data.cityofnewyork.us/d/ygpa-z7cr) | HPD | `apartment`, `unit_type`, `space_type`, `bin`, `bbl` | Same, for units with complaints |
| [NYC Citywide Rolling Calendar Sales `usep-8jbt`](https://data.cityofnewyork.us/d/usep-8jbt) | DOF | `apartment_number`, `residential_units`, `gross_square_feet`, `year_built` | Unit numbers of sold condo and co-op units. Whether sq ft is per unit or per building: to confirm |
| [Property Valuation and Assessment Data `8y4t-faws`](https://data.cityofnewyork.us/d/8y4t-faws) | DOF | `aptno`, `coop_apts`, `units`, `condo_number`, `gross_sqft`, `residential_area_gross`, `bld_story` | Condo unit numbers and possibly unit area. Grain per condo unit: to confirm |
| [ACRIS – Real Property Legals `8h5j-fqxa`](https://data.cityofnewyork.us/d/8h5j-fqxa) | DOF | `unit`, `borough`, `block`, `lot` | Unit numbers named in recorded deeds and mortgages |
| [Affordable Housing Production by Building `hg8x-zxpr`](https://data.cityofnewyork.us/d/hg8x-zxpr) | HPD | `studio_units`, `_1_br_units` … `_6_br_units`, `unknown_br_units`, `total_units`, `bin`, `bbl` | Bedroom mix per building (HPD-financed projects only) |
| [Advertised Lotteries on Housing Connect By Building `nibs-na6y`](https://data.cityofnewyork.us/d/nibs-na6y) | HPD | `unit_distribution_studio` … `_4bed`, `unit_count`, `address_buildingidentificationnumber`, `address_bbl` | Bedroom mix of lottery units since July 2020 |
| [Local Law 44 – Unit Income Rent `9ay9-xkek`](https://data.cityofnewyork.us/d/9ay9-xkek) | HPD | `bedroomsize`, `totalunits`, rents, `buildingid` | Units by bedroom size per building (LL44 projects) |
| [Buildings Subject to HPD Jurisdiction `kj4p-ruqc`](https://data.cityofnewyork.us/d/kj4p-ruqc) | HPD | `legalclassa`, `legalclassb`, `legalstories`, `bin` | Legal unit counts per building (catalog "not researched yet" item) |
| [DOB NOW: Certificate of Occupancy `pkdm-hqz6`](https://data.cityofnewyork.us/d/pkdm-hqz6) | DOB | `number_of_dwelling_units`, `c_of_o_number`, `bin`, `bbl` | Fills the catalog's "later ones … ID to confirm" |
| [Housing Database Project Level Files `br6q-ssj3`](https://data.cityofnewyork.us/d/br6q-ssj3) | DCP | `classainit`, `classaprop`, `classanet`, `units_co`, `bin` | Unit changes per job (catalog "not researched yet" item) |

- **Terms**: NYC Open Data terms, as in the catalog. The metadata of all these datasets has no license field (`license: null`).
- **Caution**: the `apartment` values in HPD data are typed in by people and will need normalizing (see Unit in `GLOSSARY.md`). A unit seen only in a violation proves it exists, not that the list is complete.
- **ACRIS website**: its bandwidth notice ([a836-acris.nyc.gov](https://a836-acris.nyc.gov/BandwidthPolicy/ACRIS-BW-POL.html), served in place of `robots.txt`) says: *"Further access to ACRIS is denied. This can be due to multiple reasons such as detection of automated scripts/robots that are capturing data from the website or having exceeded the bandwidth limits..."* It sends bulk users to *"subscription data services"* or to NYC Open Data. Whether condominium declarations with floor plans are imaged in ACRIS: to confirm. Any such use would be manual only.

### DOB documents: Certificates of Occupancy, scans and approved plans

- **CO PDFs**: DOB's [Find Building Data](https://www.nyc.gov/site/buildings/dob/find-building-data.page) page says BIS *"contains the records of permits issued and job applications created before the launch of the DOB NOW system"* and that the DOB NOW Public Portal lists Certificates of Occupancy. [Using BIS](https://www.nyc.gov/site/buildings/industry/using-bis.page): *"You do not need to sign-up to access information in BIS."* What a CO PDF shows per floor (use, number of dwelling units) is to confirm on a sample, which we did not download.
  - **Access**: web portal, one building at a time. Both hosts block non-US connections (see Fetch notes). No `robots.txt` could be read for either host. No bulk download or API for the PDFs was found.
  - **Terms**: NYC.gov Terms of Use. No DOB-specific clause on automated access was found.
  - **Suggested status**: `pending`, as a manual step for single buildings.
- **Approved plans and drawings**: [Find Building Data](https://www.nyc.gov/site/buildings/dob/find-building-data.page): *"Use the DOB NOW: BIS Options portal to request drawings, plans or documents for properties located in New York City"*, with pickup at the borough office. The [ADM-73 Supplemental Records Request Form](https://www.nyc.gov/assets/buildings/pdf/adm_73_form.pdf) asks the owner or managing agent to sign *"I hereby authorize the above mentioned individual to view Department of Buildings records pertaining to the above requested record(s)."* Requestors who are not filing representatives must be a Professional Engineer, Registered Architect or Licensee and supply owner information.
  - **Suggested status**: `blocked`, because access needs the owner's notarized authorization, not because of terms. A FOIL route exists ([DOB FOIL requests](https://www.nyc.gov/site/buildings/dob/foil-requests.page)). Whether FOIL would release plans: to confirm.
- **HPD Online I-cards**: DOB's [Find Building Data](https://www.nyc.gov/site/buildings/dob/find-building-data.page) says HPD Online contains I-card images for NYC properties. What the cards contain (for example units per floor) is to confirm. `hpdonline.nyc.gov/robots.txt` returned `404`. Terms: NYC.gov Terms of Use. Suggested status `pending`.

### NYC Department of Records: Municipal Archives tax photographs

- **What it has**: the DORIS [press release of 2018-11-01](https://www.nyc.gov/assets/records/pdf/2018-11-01%20-%20PRESS%20RELEASE%20%20-%20Digitization%20and%20web%20access%20to%20720000%20photographs%20ca%201940.pdf): *"more than 720,000 photographs. The collection consists of individual pictures of every house and building in the five Boroughs of New York City, ca. 1940."* Photographers worked with *"a helper to place a sign identifying the property by its block and lot number"*. *"The 1940 collection is complemented by the second Citywide photograph survey completed by the tax assessment office in the mid-1980s."* Block and lot let a Photo be linked to a Tax Lot.
- **Access**: [nycrecords.access.preservica.com/1940s-tax-photographs](https://nycrecords.access.preservica.com/1940s-tax-photographs) has search fields including Block and Lot, and links to an order page for prints ([dorisorders.nyc.gov](https://dorisorders.nyc.gov/dorisorders/ui/order-reproductions)). Whether images can be downloaded directly, or whether a bulk or API route exists, is to confirm. `robots.txt` only disallows `/wp-admin/` (allows `admin-ajax.php`).
- **Terms**: [Municipal Archives Terms and Conditions](https://www.nyc.gov/site/records/historical-records/terms-and-conditions.page):
  - *"The Municipal Archives encourages the publication, use, and re-use of materials from its collection."*
  - *"Non-commercial uses of Municipal Archives and Library materials are exempt from the licensing requirement."*
  - *"All other publication and commercial uses of Municipal Archives and Library materials may be granted subject to the conditions listed in the Publish/Use Contract form (MA-45)."*
  - *"Acknowledgment is required for all published use of Archives and Library materials: Item Name, Collection, Courtesy of the Municipal Archives, City of New York."*
  - *"Content may be subject to third-party rights such as copyright or privacy rights."*
  - Nothing on bulk or automated access. The Preservica page footer links to the NYC.gov Terms of Use.
- **Note**: `1940s.nyc` is a third-party site, not the Publisher. Its `robots.txt` blocks many AI and agent user agents. It should not be used as a Source.
- **Suggested status**: `pending`. This is the most promising Photo Source found: official, covers every building, keyed by block and lot, and free for non-commercial use with a credit line.

### Landmarks Preservation Commission

- **What it has**: [Designation Reports](https://www.nyc.gov/site/lpc/designations/designation-reports.page) *"describe in detail the physical appearance of each building or site"*. Whether they contain photos or plans is not stated. On Open Data, [Individual Landmark Sites `buis-pvji`](https://data.cityofnewyork.us/d/buis-pvji) has a `url_report` field (link to the report PDF). [Individual Landmark and Historic District Building Database `gpmc-yuvp`](https://data.cityofnewyork.us/d/gpmc-yuvp) has per-building `bin`, `bbl`, `date_low`, `arch_build`, `style_prim`, `mat_prim`, `use_orig` and `build_type`.
- **Terms**: the reports page has no reuse statement, only *"© City of New York. 2025 All Rights Reserved."* NYC.gov Terms of Use apply. Permission goes through the agency.
- **Suggested status**: `pending`. Datasets: NYC Open Data terms.

### Rent Guidelines Board and DHCR

- **What it has**: [Buildings That Contain Rent Stabilized Units](https://rentguidelinesboard.cityofnewyork.us/resources/rent-stabilized-building-lists/) lists *"only those buildings that contain at least one rent stabilized unit"*, built from *"2025 Building Registrations filed with NYS Homes and Community Renewal (HCR), as of October 2026."* *"Listings are in pdf format."* One file per borough, for example `2025-DHCR-Bldg-File-Manhattan.pdf`.
- **Unit-level**: none. *"The lists do not indicate which apartments in these buildings are rent stabilized"*, and the RGB *"does not have any information concerning whether any particular apartment is rent stabilized"*. DHCR has a Rent Regulated Building Search ([HCR tenant online services](https://hcr.ny.gov/tenants-online-services)) at building level. Its terms were not read: to confirm.
- **Terms**: no specific terms on the page. `robots.txt` sets `Crawl-delay: 10`.
- **Suggested status**: `pending`. Useful as a building flag, not for Units.

### HPD Housing Connect

- **What it has**: lottery listings. The same data is on Open Data at building level (`nibs-na6y`) and lottery level (`vy5i-a666`), including bedroom mix.
- **Terms**: [NYC Housing Connect Terms and Conditions](https://www.nyc.gov/site/hpd/about/terms-and-conditions.page) cover applicants and accounts. No clause on automated access or reuse of listing content was found. They incorporate the NYC Terms of Use and the HDC Terms of Use. The HDC terms were not read: to confirm.
- **Access**: `housingconnect.nyc.gov` refused our connection, so its `robots.txt` was not read.
- **Suggested status**: `pending`. Prefer the Open Data datasets (ladder step 1).

### Library of Congress: HABS/HAER/HALS

- **What it has**: Historic American Buildings Survey records with measured drawings (including floor plans), photos and data pages. Which buildings in the chosen neighborhood are covered: to confirm.
- **Rights (snippet)**: the [HABS/HAER/HALS collection record](https://www.loc.gov/pictures/item/2009632512/) reads "No known restrictions on publication". Many item records read "No known restrictions on images made by the U.S. Government; images copied from other sources may be restricted" (for example [a HABS sheet record](https://www.loc.gov/resource/hhh.tx0972.sheet)). So each item's rights advisory has to be checked.
- **Access (snippet)**: [Working Within Limits](https://www.loc.gov/apis/json-and-yaml/working-within-limits/) gives about 20 requests per minute for the JSON/YAML API, with a one-hour block if exceeded, and other tiers for image and storage services.
- **To confirm**: every loc.gov page and `robots.txt` returned `403` to our fetch tools, so none of this was read on the page itself.
- **Suggested status**: `pending`.

### NYPL Digital Collections

- **Rights**: the [Repo API page](https://api.repo.nypl.org/) says the Public Domain filter *"limits results from the API to materials that have no copyright issues"*. Image links are given only for items marked *"No Known U.S. Copyright restrictions."* Attribution is *"Though not required"*, but NYPL asks for *"From The New York Public Library"* and a link back.
- **Access**: *"The limit per authentication token ... is 10,000 requests per day."* The same page says *"The Repo API is being deprecated and will no longer be available starting August 1st, 2026"*, with no public replacement. As of this research it should be treated as gone. `digitalcollections.nypl.org/robots.txt` returned a bot-protection page, so its rules are to confirm. The [public domain collections page](https://www.nypl.org/research/resources/public-domain-collections) returned no readable content: to confirm.
- **Suggested status**: `pending`, manual or case-by-case.

### Wikimedia Commons

- **Rights**: [Commons:Reusing content outside Wikimedia](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia): *"Each media file has its licensing specified on its file description page."* *"some licenses require that the original creator be attributed"*, and *"it is the content creator who must be credited, not the uploader."*
- **Automated access**: the [Robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy) says to honor `robots.txt` and *"Always identify your bot clearly via its User-Agent HTTP header"*. Limits: Action API, unauthenticated: concurrency 1 and under 5 requests per second. Media (`upload.wikimedia.org`): *"Always keep a total concurrency of at most 2, and limit your total download speed to 25 Mbps"*. The [User-Agent Policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy) asks for *"some way of contacting you, the operator"* and says generic agents *"will fail with an HTTP 403 error"*. `commons.wikimedia.org/robots.txt` disallows `/w/` and `/api/` for `*`. API use follows the robot policy instead.
- **Conflict with ADR 0006**: the ADR requires a generic User-Agent with no contact link. Wikimedia's policy asks for contact information. This needs an Owner Decision.
- **Suggested status**: `pending`.

## 2. Building and management company websites

Only each site's terms page (or, where there is none, its legal disclaimer) and `robots.txt` were read. To find a terms URL without opening other pages, we tried common paths (`/terms`, `/terms-of-use`) and searched the site's XML sitemap, which its `robots.txt` lists, for URLs containing "terms".

### Vivmark Residential (equityapartments.com, avaloncommunities.com)

- **Terms**: [equityapartments.com/terms](https://www.equityapartments.com/terms) ("Vivmark Residential Terms of Use", Effective Date: August 20, 2026). `avaloncommunities.com/terms-of-use` redirects to [vivmarkresidential.com/terms-of-use](https://vivmarkresidential.com/terms-of-use/) (Effective Date: August 17, 2026) with the same clauses.
- **Clauses**:
  - Section 5: Content includes *"images, photographs, illustrations, videos, audio, floor plans, maps, graphics, designs, data"*.
  - Section 7: *"you may not reproduce, distribute, modify, create derivative works of, publicly display, publicly perform, republish, download, store, transmit, scrape, data mine, monitor, copy, reverse engineer, or otherwise use any Content or portion of the Service for any commercial, political, automated, competitive, unlawful, or unauthorized purpose."*
  - Also: *"You also agree not to: (a) use any robot, spider, scraper, crawler, script, data-mining tool, automated device, manual process, or similar method to access, monitor, copy, scrape, or extract Content or information from the Service without Vivmark's prior written consent"*.
- **robots.txt**: equityapartments.com disallows only `/roommates/profile`, `/roommates/matches` and `/guestcard`. avaloncommunities.com disallows `*/contact-us`, `*/reset-password` and online application paths. Building and floor plan pages are not disallowed, but the terms win (ADR 0006).
- **Suggested status**: `blocked`.

### Stonehenge NYC

- **Terms**: [stonehengenyc.com/terms-of-use](https://www.stonehengenyc.com/terms-of-use), Stonehenge Management LLC, last updated March 29, 2022.
- **Clause**: you may not *"(vii) use any automated means, including, without limitation, agents, robots, scripts, or spiders, to access, monitor, or copy any part of the Services"*.
- **robots.txt**: disallows `/unit-images/`, `/building-images-masonry/`, `/amenities/`, `/videos/` and any URL with a query string (`/*?*`, including `?unit=`).
- **Suggested status**: `blocked`.

### Fetner Properties

- **Terms**: [fetner.com/terms-of-use](https://www.fetner.com/terms-of-use/), effective November 27, 2018.
- **Clause**: you agree not to *"Use any robot, spider or other automatic device, process or means to access a Website for any purpose, including monitoring or copying any of the material on a Website"* and not to *"Use any manual process to monitor or copy any of the material on a Website"*.
- **robots.txt**: `Allow: /`.
- **Suggested status**: `blocked`.

### Rudin (rudin.com, rudinresidential.com)

- **Terms**: [rudin.com/terms-of-use](https://www.rudin.com/terms-of-use), Rudin Management Co. Inc., effective July 20, 2026. They cover *"www.rudin.com and www.rudinresidential.com"*.
- **Clauses**:
  - You may not *"(ii) harvest any information from the Services or Content"*.
  - The license is *"to download, display, view, use, and play the Content ... and/or print one copy of the Content as it is displayed to you, in each case for your personal, non-commercial use only."*
- **robots.txt**: both hosts use a Drupal default. rudin.com adds `Disallow: /node/*` and `/marketing-request`.
- **Suggested status**: `blocked`. Automated collection is harvesting, and the license covers only content as displayed to a person.

### Related Rentals

- **Terms**: [relatedrentals.com/terms-use](https://www.relatedrentals.com/terms-use), The Related Companies, L.P., last updated December 19, 2019.
- **Clauses**:
  - Section 7: *"Related grants you a limited, non-exclusive, revocable, nontransferable, and non-sublicensable license to access and use the Services solely for your personal non-commercial purposes."*
  - Prohibited: *"Attempt to scrape or collect any personal or private information from the Services"*.
  - Prohibited: *"Resell the Services, in whole or in part, or any content residing or displayed within or through the Services."*
  - No general robot or crawler clause was found.
- **robots.txt**: Drupal default. Disallows `/search/`, `/admin/` and user paths. Building pages are not disallowed.
- **Suggested status**: `pending`. The owner should decide whether "personal non-commercial" covers automated Fetches and publishing Claims.

### Greystar

- **Terms**: [greystar.com/terms-of-use](https://www.greystar.com/terms-of-use), Greystar Real Estate Partners, LLC, last updated December 29, 2020.
- **Clause**: *"you are hereby authorized to view, download, cache, copy and print the Materials solely for your personal, non-commercial use and not for resale or further distribution, retransmission"*. Materials include *"graphics, images, video"*. No robot or scraping clause was found.
- **robots.txt**: `Allow: *`, `Disallow: /api/*`. A separate group blocks `Applebot`.
- **Suggested status**: `pending`. "Not for … further distribution" rules out republishing Photos and Floor Plans.

### LeFrak

- **Terms**: [lefrak.com/terms-of-use](https://www.lefrak.com/terms-of-use/), no date shown.
- **Clauses**:
  - *"You may download content for non-commercial, personal use only, provided that copyright, trademark or other proprietary notices remain unchanged and visible."*
  - *"Unless otherwise noted, the graphic images, buttons and text contained in this Website are the exclusive property of LeFrak."*
  - No automated-access clause.
- **robots.txt**: `crawl-delay: 10`. Disallows `/common/` (allows `/common/uploads/`), `/admin/` and `/includes/`.
- **Note**: lefrak.com is a corporate site. Whether LeFrak's residential leasing sites use other domains and terms: to confirm.
- **Suggested status**: `pending`.

### Glenwood Management

- **Terms**: no terms page found at the common paths or in the page sitemap. The [privacy page](https://www.glenwoodnyc.com/privacy-policy-3/) has a disclaimer: *"Listings on this website may not be re-published without the express written consent of the landlord."*
- **robots.txt**: `User-agent: *` / `Disallow:` (everything allowed).
- **Suggested status**: `pending`. Republishing listings needs written consent.

### TF Cornerstone

- **Terms**: [tfc.com/terms](https://tfc.com/terms) appears in the sitemap, but the page text is rendered by JavaScript and our fetch saw only the title. **To confirm** by reading the page in a browser.
- **robots.txt**: `Allow: /`.
- **Suggested status**: `pending`.

### Other Publishers checked, no terms found

| Publisher | Result | robots.txt |
|---|---|---|
| Gotham Organization (gothamorg.com) | No terms page in sitemap; only an accessibility policy | Cloudflare managed: `Content-Signal: search=yes,ai-train=no,use=reference`, `Allow: /`; blocks AI crawlers by name |
| Two Trees (twotreesny.com) | `/terms` returned an empty page | Same Cloudflare content signals |
| Rose Associates (roseassociates.com) | No terms page in sitemap | Allow all |
| The Durst Organization (durst.org) | Terms paths redirect to home page | `Allow: /` |
| Brodsky Organization (brodskyorg.com) | Connection failed | Not read |

All are `pending`. A missing terms page does not mean permission. `Content-Signal` is not part of RFC 9309. Whether collectors should honor it: Owner Decision.

## 3. Listing portals

| Portal | Terms page | Clause on automated access | robots.txt | API or feed |
|---|---|---|---|---|
| StreetEasy (Zillow Group) | Consumer terms not readable (`403`). The [advertising terms](https://streeteasy.com/adterms) **(snippet)** forbid advertisers to *"use any automated means of scraping or data extraction to collect data from Zillow Network, except as expressly permitted by Zillow writing"* and incorporate the Zillow Terms of Use | See Zillow | Disallows `/building/*/floorplans`, `/building/*/documents`, `/rental/*`, `/sale/*`, `/building/*/for-rent/*`, `/nyc/api` | A listing *intake* feed for advertisers ([feed format](https://streeteasy.com/home/feed_format)); no outbound data API found |
| Zillow / Trulia | [zillow.com/z/corp/terms/](https://www.zillow.com/z/corp/terms/) (`403`). **(snippet)**: forbids users to *"conduct automated queries (including screen and database scraping, spiders, robots, crawlers, bypassing "captcha" or similar precautions, or any other automated activity with the purpose of obtaining information from the Services)"* | As left | zillow.com: comment *"Access to and use of Zillow.com is governed by our Terms of Use"*, `Crawl-delay: 1` | Bridge API: [Zillow Group datasets](https://bridgedataoutput.com/docs/platform/API/zg-data) need Zillow approval; MLS listing data needs each MLS's approval ([Bridge docs](https://bridgedataoutput.com/docs/platform/Introduction/Signing-up-with-Bridge-API)) **(snippet)** |
| Redfin | [redfin.com/about/terms-of-use](https://www.redfin.com/about/terms-of-use) | *"2.3.5. No Scrubbing or Scraping. You may not automatedly crawl or query the Services for any purpose or by any means (including, without limitation, screen and database scraping, spiders, robots, crawlers and any other automated activity with the purpose of obtaining information from the Services) unless you have received prior express written permission"* | Large file; not needed given the terms | None found |
| Realtor.com (Move, Inc.) | [realtor.com/terms-of-service](https://www.realtor.com/terms-of-service/) | *"you shall not ... access, view, retrieve, refresh, reload, collect, scrape, text mine or data mine, index, process, store, harvest, or otherwise ingest the Move Network or any Content ... by any automated means (e.g., robot, spider, webcrawler, script, service, software, site search/retrieval application, extension, bot, browser automation tool, API client, AI agent or assistant ...)"* | Comment: *"Per https://www.realtor.com's Terms of Service, scraping data from this website is unauthorized without the express written permission from Move Sales, Inc."* | None found |
| RentHop | [renthop.com/resources/terms](https://www.renthop.com/resources/terms) | *"You agree not to access the Site by any means other than through the browser interface or mobile application we provide. Any automated means of accessing the Site, including through use of scripts, robots or web crawlers, is prohibited."* | Disallows `/r/visual/` and `/interaction/` | None found |
| Compass | [compass.com/legal/terms-of-service/](https://www.compass.com/legal/terms-of-service/), last updated July 27, 2026 | You may not *"(ix) use manual or automated software, devices, or other processes to "crawl" or "spider" any page of the Site; (x) harvest or scrape any Content from the Services"* | Not analyzed | None found |
| Apartments.com (CoStar) | [apartments.com/grow/about/terms-of-service](https://www.apartments.com/grow/about/terms-of-service) (`403`). **(snippet)**: anyone who uses the site *"including through a bot or other automated means, is bound by these Terms of Service"*; the prohibited list covers automated collection | As left | `robots.txt` itself returned "Access Denied" | None found |
| Rent.com | Not read | Not read | `robots.txt` returned `429` | To confirm |

- **REBNY RLS**: the NYC broker listing service offers IDX, VOW and other feeds only to RLS participants. *"an active membership does not automatically permit the use of or access to the RLS"* ([RLS FAQs](https://www.rebny.com/rls-faqs/), **(snippet)**). Not open to this project.
- **Conclusion**: every portal whose terms were read forbids automated access. This confirms the catalog's `blocked` status for the whole group. No portal offers an open API for listing Units, Photos or Floor Plans.

## 4. Copyright note

This is a summary of primary sources, not legal advice. Terms of use are a contract and apply on top of copyright: a site can forbid collecting even facts that copyright does not protect.

- **Facts are not protected.** Compendium (Third) § 313.3(C) ([chapter 300](https://www.copyright.gov/comp3/chap300/ch300-copyrightable-authorship.pdf)): *"Facts are not copyrightable and cannot be registered with the U.S. Copyright Office."* Bedroom counts, unit numbers and square footage are facts. A site's selection and arrangement of them can still be protected, and its terms can still forbid collecting them.
- **Photos are protected works.** The Copyright Office FAQ ([faq-fairuse](https://www.copyright.gov/help/faq/faq-fairuse.html)): *"The owner of the "work" is generally the photographer or, in certain situations, the employer of the photographer."* It also says: *"in cases of doubt, the Copyright Office recommends that permission be obtained."*
- **Floor Plans can be protected as architectural works.** [Circular 41](https://www.copyright.gov/circs/circ41.pdf): *"An architectural work is the design of a building as embodied in any tangible medium of expression, including a building, architectural plans, or drawings."* The protected authorship includes *"any arrangement and composition of walls or other permanent structures that divide the interior into separate rooms and spaces"*. *"Standard configurations of spaces, such as a square bathroom"* are excluded. A floor plan image on a website is therefore likely someone's protected work.
- **Photos of buildings from public places.** [17 U.S.C. § 120(a)](https://www.copyright.gov/title17/92chap1.html#120): *"The copyright in an architectural work that has been constructed does not include the right to prevent the making, distributing, or public display of pictures, paintings, photographs, or other pictorial representations of the work, if the building in which the work is embodied is located in or ordinarily visible from a public place."* This covers photos we take ourselves. It does not license copying someone else's photo.
- **Fair use is case by case.** [copyright.gov/fair-use](https://www.copyright.gov/fair-use/): *"Courts evaluate fair use claims on a case-by-case basis"*, and there is *"no formula to ensure that a predetermined percentage or amount of a work"* may be used. The four factors are purpose and character, nature of the work, amount used, and market effect.
- **Federal works are public domain.** [17 U.S.C. § 105](https://www.copyright.gov/title17/92chap1.html#105): *"Copyright protection under this title is not available for any work of the United States Government"*. Compendium § 313.6(C)(1) extends this to works by any federal officer or employee within official duties. This is why HABS drawings made by the government carry "no known restrictions". Items copied from other sources may not.
- **NYC City works are not automatically public domain.** Compendium § 313.6(C)(2): *"Other than works of the United States Government, a work that does not constitute a government edict may be registered, even if it was prepared by an officer or employee of a state, local, territorial, or foreign government"*. Government edicts (laws, rulings, ordinances) are not copyrightable. The [NYC.gov Terms of Use](https://www.nyc.gov/main/terms-of-use) claim City ownership of site content (*"All rights are reserved"*) and send permission requests to the agency. The [Municipal Archives terms](https://www.nyc.gov/site/records/historical-records/terms-and-conditions.page) grant non-commercial reuse with a credit line. Open Data has its own rules (see above). The copyright status of the 1940s tax photos specifically, which were taken by WPA-funded photographers for the City's tax office, was not found on any primary source: to confirm.

## Suggested catalog changes

1. **Replace secondary citations.** The Zillow and Redfin entries cite `conductatlas.com`. Cite instead [Redfin's terms § 2.3.5](https://www.redfin.com/about/terms-of-use) (read directly) and [Zillow's terms](https://www.zillow.com/z/corp/terms/) (snippet only; confirm on the page).
2. **StreetEasy**: replace "to confirm, expected to be similar" with: consumer terms not readable (`403`); the advertising terms forbid automated scraping and incorporate the Zillow Terms of Use; `robots.txt` disallows `/building/*/floorplans`, `/rental/*` and `/sale/*`.
3. **Add Realtor.com, RentHop, Compass and Apartments.com** to the listing portal entry. All forbid automated access, so the group stays `blocked`.
4. **Fix "List of Units — Only for condos"**: add partial rental unit numbers from the HPD Violations (`wvxf-dwi5`) and Complaints (`ygpa-z7cr`) `apartment` fields, and sold condo or co-op units from DOF Rolling Sales (`usep-8jbt`), DOF Property Valuation (`8y4t-faws`) and ACRIS Legals (`8h5j-fqxa`). Say they are partial, with a Gap reason for the rest.
5. **Fix "Unit attributes — Gap"**: bedroom mix per building (not per Unit) exists for subsidized buildings in `hg8x-zxpr`, `nibs-na6y` and `9ay9-xkek`. Per-Unit bedrooms and size remain a Gap.
6. **DOB Certificates of Occupancy**: the later dataset is DOB NOW: Certificate of Occupancy `pkdm-hqz6`. Note that BIS and DOB NOW block connections from outside the US, which matters for where collectors run.
7. **Resolve two "Not researched yet" items**: Buildings Subject to HPD Jurisdiction is `kj4p-ruqc` (`legalclassa`, `legalclassb`). The DCP Housing Database is `br6q-ssj3`. ACRIS: the website blocks scripts; use the Open Data ACRIS datasets.
8. **Add a Photo Source**: Municipal Archives 1940s and 1980s tax photographs, keyed by block and lot. Non-commercial use is exempt from licensing, with a required credit line. Status `pending`. Collection method: to confirm (no bulk or API route found).
9. **Add Floor Plan and Photo Sources with per-item rights**: LoC HABS (government-made items: no known restrictions), NYPL public-domain items, and Wikimedia Commons (license per file). Each Floor Plan or Photo Claim needs its own rights field, since rights differ per item, not per Source.
10. **Add LPC Sources**: Individual Landmark Sites `buis-pvji` (report links) and the LPC building database `gpmc-yuvp` (architect, style, materials, original use).
11. **Building websites**: record the eight terms reviewed above. Suggest `blocked` for Vivmark Residential, Stonehenge, Fetner and Rudin, and `pending` for Related, Greystar, LeFrak, Glenwood and TF Cornerstone. Replace "the most promising path" with: most large managers sampled forbid automated access, and those that do not limit use to personal, non-commercial viewing.
12. **DOB approved plans**: record as not usable. Access needs notarized owner authorization (ADM-73).
13. **Owner Decisions needed**:
    - Wikimedia's User-Agent policy asks for contact information, which conflicts with ADR 0006's generic User-Agent.
    - Whether collectors honor Cloudflare `Content-Signal` lines in `robots.txt`.
    - Whether a Gap reason is needed for "access requires authorization" (DOB plans), which is neither "no known source" nor "terms forbid".

## Not verified (to confirm)

- Exact text of NYC Admin. Code § 23-502(d): the official code site returned `403`.
- loc.gov rights and rate limits, Zillow, StreetEasy and Apartments.com terms: read only through search snippets because the pages returned `403`.
- TF Cornerstone terms: the page needs JavaScript.
- HDC Terms of Use, DHCR building search terms, and the Rent.com, Trulia and Brodsky pages: not read.
- What CO PDFs and HPD I-cards contain per floor or unit: no sample was downloaded.
- Whether the Municipal Archives Preservica site offers downloads or an API.
- Copyright status of the 1940s tax photographs.
