---
doc_id: HTS-FEA-001
title: HatchSide feasibility assessment
project: HatchSide
doc_type: Feasibility
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First draft at the kit 1.9.1 upgrade (stage P3), for option A with option B noted
---

# HatchSide feasibility assessment

Feasible on paper for option A: a galvanized steel head, three telescoping aluminium legs, a bought hand winch and five tool heads, all from stock sections that a local workshop can cut, drill and weld, at USD 2,838 in parts against the USD 5,000 value-engineering target. What paper cannot settle is how the kit behaves in sewage, how it feels in a crew's hands and whether a buyer will accept an uncertified lifting frame; those wait for TRL 4 and for a co-design partner. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Leg buckling factor 5.5 and rope factor 14.3 at the design case; the tripod tips only at 25.0 degrees against the 10 degrees required; every head passes a 560 mm opening; 16 STEM claims are within known science and 8 are plausible, none fails | High | The grab nets 9.7 L against 10 L (STM S9, PR-008 at risk); grab breakout from sludge and the sealant cure are unknown (STM S11, S15); the winch drum D/d is to confirm (S8) | STM; CAL-001; HTS-PRS-001 |
| Materials | 6082-T6 square tube legs, S275 plate hot-dip galvanized, A4 fasteners, 316 rope, HDPE and nylon isolators | Medium | Corrosion life in sewer air (hydrogen sulfide, chloride) is unproven; aluminium and zinc are anodic to stainless fittings and rely on the isolating washers (STM S16, PR-011) | STM S16; CAL-001 section 3 |
| Manufacturing and assembly | Every made part is cut, drilled or welded from stock tube, plate and bar; 395 parts in the D3 model, of which 129 are made, 75 bought, 127 fasteners and 64 welds; a 14-step prototype build plan (paper only) | High | Load-path welds in the head and winch bracket need a competent welder; a galvanizer is needed in town | BLD-001; model fidelity record `cad/fidelity.json` |
| Power and controls | Human powered, about 33 W of hand input in low gear at 150 kg; no electrics, no controls | High | A winch with an automatic load brake is a bought part that must hold when the crank is released | CAL-001 section 4; STM S4 |
| Supply of parts | Winch, rope, shackles, sheave, chain, line counter and connector are catalogue lifting items; the rest is local stock | Medium | The winch (USD 320) is the price-sensitive part: a commercial worm-gear hand winch listed at USD 715.99 shows the range (MKT); catalogue ratings must be confirmed on purchase (HTS-DEC-001, items 1 to 5) | BOM; MKT |
| Regulation and acceptance | Not certified for lifting people and says so; context rules (OSHA, EN, Indian law) are in HTS-REG-001 | Low | A buyer in a regulated setting may insist on certified equipment for any use near a person; a legal review is needed before any sale | REG; RSK H1 |

Ratings: High, Medium, Low.

## Option B

The straddle-frame davit (HTS-OPT-001) is also feasible on paper: its mast, boom and bolt checks carry large margins (CAL-001 section 11), and it is more stable (46 degrees against 25). It is less feasible as a field kit, because its frame is 1.8 m wide by 2.3 m long, its heaviest piece is 26.2 kg against the 25 kg limit and its cost estimate is USD 3,910 against USD 2,838.

## Open items before TRL 4

- Confirm the winch rating, drum capacity and base hole pattern with the supplier (HTS-DEC-001, items 1 and 2).
- Measure common manhole, hatch and digester openings with the first partner (HTS-PRB-001).
- Read G2, G5 and G12 in HTS-REG-001 with a qualified reviewer.
