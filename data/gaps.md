# Gaps

Facts we wanted but could not source well, plus Cala claims that need a human check before they go on the page. Never fill these from memory.

Claim numbers refer to `data/claims_trastuzumab.md`. Raw responses are in `data/raw/trastuzumab/<chapter>.json`.

## Trastuzumab (Herceptin)

### Vague or untraceable stats (not used on the page)

| # | Claim | Problem | Status |
|---|---|---|---|
| 1 | problem #3: trastuzumab "reduced mortality in HER2+ tumors by about 33%" and brought survival "comparable with HER2-negative disease" | No trial named, no timeframe. Sources are a ScienceDirect topic page and an Australian surgeon's clinic page. | Left out |
| 2 | origin #2: HER2 is amplified in "about 25–30%" of breast cancers | Only sources are chemicalbook.com and patentdocs.org. Conflicts with near_death #3 (Lasker Foundation), which says ~20–25%. | Page uses Lasker's 20–25%. Check which figure is right. |
| 3 | adjuvant #1: "combined **interim** analysis" of NSABP B-31 / NCCTG N9831 showing **10-year** overall survival 84% vs 75.2% | Interim and 10-year don't fit together. Cited PMC4226805 is the planned joint OS analysis; PMC4489560 is a review. Hazard ratios were cut off in the response. | Left out. Page uses the HERA stat instead. Find the actual 10-year B-31/N9831 paper. |
| 4 | pivotal_trial #4 vs #5: heart damage 27% (anthracycline arm) and 13% (paclitaxel arm) vs 28% and 11% | Two sources give slightly different numbers for the same trial. | Page uses 27% / 13% from PubMed 11870163 (stronger source). Confirm. |
| 5 | problem #6: humanized antibody is ">90% humanized" | Sources are IEDB, a reagent seller (synbio-tech) and a general review. Not Herceptin-specific. | Left out |

### Weak or indirect sources

| # | Claim | Problem | Status |
|---|---|---|---|
| 6 | pivotal_trial #1–3: 469 women; median survival 20.3 → 25.1 months; response 50% vs 32% | Only source is a review on *adjuvant* use (sage.cnpereading.com), not the trial paper itself. | Used on page. Find the primary trial publication. |
| 7 | problem #4–5: mouse antibody triggers a human anti-mouse antibody (HAMA) response, so it had to be humanized | General antibody facts from weak sources (IEDB, biorbyt.com.cn, synbio-tech.com). | Left out. The page only says 4D5 was humanized (Lasker source). |
| 8 | origin #5: Slamon led the first human trial at UCLA in 1990 | Sources are jewishlink.news and Healio. Healio is OK; want a UCLA or journal source. | Used on page |
| 9 | near_death #1: Genentech "wanted no part of it" | Direct quote; sources are UCLA Health and Cancer History Project. Need exact wording and who said it. | Paraphrased on page, no quote marks, until verified |
| 10 | advocates #2: advocates cut trial enrollment time | Only source is a USPTO petition document. Same idea in advocates #1 via a Genentech press release on drugs.com. | Page uses advocates #1 wording |
| 11 | approval: Sept 25, 1998 | Only source is Drugs.com. Want the FDA record (openFDA or FDA label history). | Used on page |
| 12 | adjuvant #4: adjuvant approval Nov 16, 2006 | Drugs.com and an Arkansas Blue Cross policy page. Want FDA. | Used on page |
| 13 | successors #3: margetuximab | No source returned at all. | Left out |
| 14 | successors #6: trastuzumab duocarmazine (SYD985) | Only one source (MDPI review); approval status unknown. | Left out |
| 15 | funding #3: recent Revlon $1M "Love is On" donation | Sourced, but off-topic for the story. | Left out |

### Not covered by Cala yet (queries not run)

| # | Missing | Why it matters |
|---|---|---|
| 16 | Date of the pivotal metastatic trial (when it ran, when it was published) | Lifeline needs a year; page currently folds the trial into the 1998 approval chapter |
| 17 | Date 4D5 was humanized | Would give the "scientific problem" its own dated chapter |
| 18 | *Living Proof* (2008 film) and Robert Bazell's *HER-2: The Making of Herceptin* | Good cultural "today" beat; mentioned in CLAUDE.md but not yet sourced |
| 19 | HercepTest / HER2 testing as a companion diagnostic | Explains how patients are picked for the drug |
| 20 | Stomach (gastric) cancer approval, Oct 2010 | Appears only in a summary paragraph, not as a cited claim |
| 21 | Approval dates for pertuzumab, Kadcyla, Enhertu | Successor claims have no dates; the Landscape will need them |

## Trastuzumab deruxtecan (Enhertu)

Claims in `data/claims_trastuzumab_deruxtecan.md`; raw responses in `data/raw/trastuzumab_deruxtecan/`.

| # | Claim | Problem | Status |
|---|---|---|---|
| 1 | Year Daiichi Sankyo started the program | Cala gave no date for the origin | Origin chapter is dated by Herceptin's 1998 approval, the antibody it reuses |
| 2 | DESTINY-Breast03 date | Dated 2022 from the NEJM 2022 key-paper source; no exact date returned | Used "2022" |
| 3 | May 2026 early-breast-cancer approval | Month comes from Cala's summary and the press release title; no exact day | Used "May 2026" |
| 4 | DESTINY-Breast09 (first-line, with pertuzumab) and DESTINY-Breast11 | Results sourced, but no FDA approval date for first-line use | Left out |
| 5 | Kadcyla's own approval date | Not queried | Left out |

## Landscape (drugs.json)

| Claim | Problem | Status |
|---|---|---|
| Enhertu HER2-low approval: Aug 6, 2022 | Cala's date (her2_low #8, source Drugs.com). FDA announcements may give Aug 5, 2022. Want the FDA record. | Used for Enhertu's HER2-low row |
