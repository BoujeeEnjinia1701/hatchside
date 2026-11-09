---
doc_id: HTS-PRS-001
title: HatchSide product requirements and specifications
project: HatchSide
doc_type: Product requirements and specifications
version: "0.3"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Populated to TRL 2, then TRL 3 results from the calculation note
- version: "0.3"
  date: '2026-11-05'
  author: Amish Chadha
  change: Kit 1.9.1 upgrade; R1 to R14 migrated to PR-001 to PR-014 (column Was), each traced to a user requirement in HTS-URS-001; PR-015 to PR-018 added; figures refreshed from the kit 1.9 model
---

# HatchSide product requirements and specifications

What the kit must do, each requirement traced to a user need in HTS-URS-001 (links in HTS-RTM-001). Fourteen requirements are the original R1 to R14, migrated to PR-001 to PR-014 with their old numbers in the Was column; PR-015 to PR-018 are new. The requirements describe option A, the tripod and hand winch, which is the current design and is **proposed, awaiting Amish** as the concept (HTS-OPT-001, HTS-DDR-003). On paper 16 of the 18 are met or met by design; PR-008 (grab output) is at risk, at 9.7 L net against 10 L, and PR-011 (corrosion) cannot be shown on paper and waits for a TRL 4 coupon test. None is failed. Option B, the straddle-frame davit, is compared in HTS-OPT-001 and misses PR-005 and PR-006; those statuses are for option A. Method: STANDARDS section 22.

The **reference job** is a 560 mm street manhole 10 m deep, or a household digester opening 2.5 m deep, worked by a crew of two or three with a certified gas detector.

Table 1. Product requirements and specifications. Status from HTS-CAL-001 (kit 1.9 model, 2026-11-05).

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-004 | Safety | No entry needed | Every head shall be fitted, lowered, worked and recovered from outside the opening, with nobody entering | All five heads | pass or fail | n/a | Task walkthrough for every head at a mock manhole, TRL 4; inspection of the model at TRL 3 | Met on paper: every head is fitted, worked and recovered from the rim | R1 |
| PR-002 | UR-002 | Physical architecture | Fits common openings | The tripod shall straddle openings from 0.5 to 1.2 m across | 0.5 to 1.2 | range | m | Setup trials on sample manholes and hatches, TRL 4; analysis (CAL-001 section 2) | Met on paper: feet on a 3.0 m circle; rim guard inner face 672 mm from the centre | R2 |
| PR-003 | UR-003 | Performance | Working depth | At least 10 m of rope shall be available below the rim | 10 | min | m | Winch drum capacity check and depth trial, TRL 4 | Met on paper: 15 m of rope; drum capacity to confirm on purchase | R3 |
| PR-004 | UR-008 | Safety | Working load | The head interface shall carry a safe working load of 150 kg, proof loaded to 1.5 times, with a 1.25 dynamic factor on the proof case | 150; 1.5 | min; min | kg; factor | Analysis (CAL-001 section 3), TRL 3; proof-load test at TRL 4 | Met on paper: leg buckling factor 5.5 at proof with jerk (4.8 with the rope 10 degrees off vertical); rope factor 14.3 at the working load and 4.8 with the winch at stall | R4 |
| PR-005 | UR-005 | Usability | Fast setup | A crew of two shall set the kit up in 10 minutes or less | 10 | max | min | Timed setup trial, TRL 4; estimate (CAL-001 section 8) | Met on paper (estimate): 9.0 min | R5 |
| PR-006 | UR-006 | Logistics | Portable loads | No single packed load shall exceed 25 kg | 25 | max | kg | Weigh each packed load, TRL 4; model masses (CAL-001 section 5) | Met on paper: heaviest load 23.7 kg (grab head); whole kit 153.0 kg in nine loads | R6 |
| PR-007 | UR-010 | Usability | Quick head change | A head shall be changed in under 2 minutes without tools | 2 | max | min | Timed changeover trial, TRL 4 | Met on paper (estimate): one screw-pin shackle, about 1 min | R7 |
| PR-008 | UR-004 | Performance | Grab clears silt | The grab shall bring up at least 10 L of wet silt per cycle | 10 | min | L | Trial in a silt-filled test chamber, TRL 4; analysis (CAL-001 section 8) | **At risk** (estimate): 10.8 L at 70 % fill but 9.7 L after the 10 % that drips back (CAL-001 section 8; STM S9); a bigger grab or a lower target is proposed to Amish (HTS-DEC-001 D16) | R8 |
| PR-009 | UR-014 | Performance | Depth sample | The sampler shall take a sample whose centre is at a chosen depth within 0.2 m | 0.2 | max | m | Trial in a layered test tank, TRL 4 | Met on paper: line counter reads 0.1 m; tube centre known from the interface | R9 |
| PR-010 | UR-003, UR-004 | Performance | DomeReach to the floor | The DomeReach tool shall reach 2.5 m below the opening rim (design depth, HTS-DDR-001, D7) | 2.5 | min | m | Trial at a partner digester, TRL 4; analysis (CAL-001 section 7) | Met on paper: hinge 2.6 m, tool 3.3 m below the rim | R10 |
| PR-011 | UR-009 | Materials | Corrosion resistance | No structural corrosion after 100 hours of salt spray or sewage immersion | 100 | min | h | Material coupon test, TRL 4 | To verify at TRL 4: not verifiable on paper; galvanized steel, 6082 aluminium, A4 fasteners and rope with isolating washers | R11 |
| PR-012 | UR-007 | Cost | Value-engineering target | Parts shall cost at or near the USD 5,000 value-engineering target (a hypothetical control target) | 5,000 | max | USD | Priced BOM (`bom/bom.csv`) | Met on paper: USD 2,838, USD 2,162 under the target | R12 |
| PR-013 | UR-002 | Physical architecture | Heads pass a small manhole | Every head, as it hangs, shall pass a 560 mm opening with 20 mm to spare | 540 | max | mm | Pass each head through a 560 mm ring, TRL 4; model bounding boxes (CAL-001 section 7) | Met on paper: largest plan diagonal 525 mm (grab); DomeReach passes folded | R13 |
| PR-014 | UR-008 | Safety | Stable in use | The tripod shall stay stable with the rope 10 degrees off vertical at the safe working load | 10 | min | degrees | Tilt-pull test during proof loading, TRL 4; analysis (CAL-001 section 6) | Met on paper: tips at 25.0 degrees at the safe working load | R14 |
| PR-015 | UR-012 | Safety | Guard the opening | A rim guard of six hinged panels with drop pins shall surround the opening, with a splash board on each panel, plus four cones and 10 m of barrier chain for the work zone | 6; 4 | min | panels; cones | Inspection of the model and build plan, TRL 3; trial at TRL 4 | Met by design: BOM lines 15, 16 and 22 | New |
| PR-016 | UR-011 | Physical architecture | Made locally | Every made part shall be cut, drilled, bent or welded from stock sheet, plate, bar and tube with a drill and a welder; every other part is bought | No machining | pass or fail | n/a | Inspection of the model, BOM and build plan | Met by design: parts are named with their stock in the D3 model; BOM column make_buy | New |
| PR-017 | UR-013 | Usability | Winch effort | One person shall raise and lower a full 150 kg load at a sustained input power no higher than the screening value for hand cranking | 75 | max | W | Analysis (CAL-001 section 4), TRL 3; crank-force measurement at TRL 4 | Met on paper: about 33 W in low gear (31 N at the 250 mm crank) | New |
| PR-018 | UR-008 | Safety | Not for lifting people | The winch shall carry a label that it never lifts or lowers a person; the retrieval head shall clip a line only, with the haul made on certified rescue equipment | Labels on winch and each head | pass or fail | n/a | Inspection of the model labels (BOM line 24) | Met by design: labels on the head and winch; retrieval head is guide-only (HTS-DDR-001, D2) | New |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, environment and durability, cost. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Most routine sewer, tank and digester tasks can be done with grab, rake, sampler and pole tools from the rim.
- Crews carry and use a certified gas detector alongside the kit.
- A commodity two-speed hand winch with an automatic load brake is available in the first region.
- Household biogas digesters have an opening of at least 560 mm and a depth of about 2.5 m below the rim; both are to be measured with the first partner.
- The sustained hand-cranking limit of 75 W is the screening value in `.kit/stem_check.py`; an assessment against a cited ergonomics standard belongs to TRL 4.

## Safety

> **Safety:** PR-004 and PR-014 are material-handling requirements for tool heads. Nothing in this document qualifies HatchSide for lifting, lowering or rescuing a person, and the winch must never be used for that. A proof load to 1.5 times the safe working load with a competent person present comes before any use over a real opening. Gas testing, traffic guarding and the no-entry rule apply to every trial.
