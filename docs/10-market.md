---
doc_id: HTS-MKT-001
title: HatchSide market and viability
project: HatchSide
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First draft at the kit 1.9.1 upgrade (stage P3), for option A
---

# HatchSide market and viability

Municipal sanitation departments, biogas programmes and informal sanitation crews need a low-cost way to stay out of confined spaces, and the commercial tripod-and-winch sets that exist cost about USD 5,200 to 6,100 and carry no work tools; HatchSide's parts estimate is USD 2,838 and an open design lets any workshop build it. Prices and benchmarks are cited with the date they were checked (2026-11-05). Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Municipal sewer and drain crews | Urban local bodies in India; later other countries with mechanised sanitation programmes (NAMASTE, HTS-REG-001 G10) | Bandicoot cleaning robot: first unit about INR 10 lakh (about USD 1,500 at the time, 2018 article, [Quartz](https://qz.com/1217899/bandicoot-robot-indias-answer-to-manual-scavenging-clogged-sewers)); beta units INR 10 to 12 lakh to make ([Forbes India](https://www.forbesindia.com/article/startups-special-2018/bandicoot-genrobotics-robot-that-scoops-out-filth-from-sewers/50401/1)); both are older prices | 2,838 (BOM, option A) | A manual kit that does the grab, rake and sample jobs for a fraction of a robot, repaired in the municipal workshop |
| Household biogas technicians and programmes | Rural India, Nepal and similar; DomeReach with the shared frame | No close product found; digester maintenance guidance says work from above ground where possible ([energypedia](https://energypedia.info/wiki/Maintenance_of_a_Biogas_Plant)) | 2,838 for the kit; DomeReach alone about 225 plus the share of the frame (BOM line 21) | Reseal a dome from the opening without entering |
| Industrial and oil and gas tank contractors | Tank roof hatches, frac tanks, in regulated markets | Confined-space tripod with winch: USD 5,853.29 to 6,120.19 across variants ([PK Safety, 3M DBI-SALA 83010](https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010)); a similar 7 ft set with 60 ft cable listed at USD 5,229.00 and a 7 ft tripod alone at USD 1,660.00 on retailer pages seen in search results (links not recorded; to re-check) | 2,838 | Same price class for a kit that carries work tools; but it is not certified for people and cannot replace a rescue tripod |
| Winch only (component benchmark) | Buyers and fabricators | Thern 1,000 lb worm-gear hand winch with automatic brake: USD 715.99 ([GME Supply](https://www.gmesupply.com/thern-1000-pound-worm-gear-hand-winch)) | BOM winch line: 320 (a two-speed winch, supplier not chosen) | Shows the winch price range; the BOM figure is an estimate to confirm on purchase |

Viability: on paper the kit is cheaper than the commercial sets because it is a material hoist and not a personnel rescue system, so it skips the certification that adds most of their price. That also limits who may buy it for which use (HTS-REG-001 G1 to G6). Whether crews will choose it over the habit of entering is a co-design question that paper cannot answer.

## Open route

Who would build it: municipal workshops, local fabricators with a welder and drill, sanitation NGOs, university engineering departments and makerspaces. The drawings, BOM and build plan are published under CERN-OHL-S-2.0 (hardware) and MIT (software), so anyone can build and sell the design, and improvements must be shared back. A workshop that builds it for sale takes on the certification and liability questions in HTS-REG-001; the repository does not.

## Sources

- PK Safety, "3M DBI-SALA Confined Space Aluminum Tripod w/ Winch 83010," https://pksafety.com/products/3m-dbi-sala-confined-space-aluminum-tripod-w-winch-83010, checked 2026-11-05.
- GME Supply, "Thern 1000 Pound Worm Gear Hand Winch," https://www.gmesupply.com/thern-1000-pound-worm-gear-hand-winch, checked 2026-11-05.
- Quartz, "Bandicoot robot: India's answer to manual scavenging and clogged sewers," https://qz.com/1217899/bandicoot-robot-indias-answer-to-manual-scavenging-clogged-sewers (article of early 2018), checked 2026-11-05.
- Forbes India, "Startups special 2018: Genrobotics' Bandicoot," https://www.forbesindia.com/article/startups-special-2018/bandicoot-genrobotics-robot-that-scoops-out-filth-from-sewers/50401/1, checked 2026-10-03 (HTS-PRB-001).
- Energypedia, "Maintenance of a Biogas Plant," https://energypedia.info/wiki/Maintenance_of_a_Biogas_Plant, as cited in HTS-PRB-001.
- Retailer listings for a 3M DBI-SALA 7 ft tripod with 60 ft cable (USD 5,229.00) and a 3M 7 ft tripod alone (USD 1,660.00), seen in web search results on 2026-11-05; the pages were not recorded, so these two figures are to re-check before use.
