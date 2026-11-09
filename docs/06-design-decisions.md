---
doc_id: HTS-DEC-001
title: HatchSide design decisions register
project: HatchSide
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened at TRL 3; every decision made under Amish's 2026-10-03 pre-approval
- version: "0.2"
  date: '2026-11-05'
  author: Amish Chadha
  change: Kit 1.9.1 upgrade; open decisions D13 to D17 added (proposed, awaiting Amish); STEM check recorded
---

# HatchSide design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

> **Safety:** Several decisions below set the safety case of a lifting frame used over confined spaces. Each took the conservative option and names the evidence that would relax it. HatchSide is a material-handling frame for tool heads; it is never used to lift or lower a person, and nobody enters the space.

## Open decisions

All proposed at the kit 1.9.1 upgrade (2026-11-05), awaiting Amish. Nothing below is decided.

| # | Decision | Recommendation | Options | Record |
| --- | --- | --- | --- | --- |
| D13 | Concept: tripod and hand winch (A) or straddle-frame davit (B) | **Proposed, awaiting Amish:** A, which scores 160 of 180 against 141 for B (13.8 % lead, outside the 10 % band) | A; B; keep both open | HTS-OPT-001; HTS-DDR-003 |
| D14 | Confirm the corrections made when the model was rebuilt to D3: one shackle per chain lug, a 44 x 45 mm lug on a 140 x 360 mm foot plate (80 mm longer), a 14.2 mm longer head interface, M16 x 110 hinge bolts, and the model fixes K1 to K11 | **Proposed, awaiting Amish:** confirm; no price changes and no change to the pitch | Confirm; revert any item (the D3 check then fails until it is remodelled) | HTS-DDR-004 |
| D15 | Offer a second, lower winch bracket position on leg A, the idea taken from option B (winch at waist height) | **Proposed, awaiting Amish:** not applied; test with a crew first | Apply to the model and BOM; leave as is | HTS-OPT-001 |
| D16 | The grab nets 9.7 L against the 10 L of PR-008 once the 10 % drip is counted (STM S9) | **Proposed, awaiting Amish:** lengthen both shells by about 25 mm (gross 16.4 L, net 10.3 L); the plan diagonal becomes 542 mm against the 540 mm limit, so either accept 2 mm less spare in a 560 mm opening or narrow the shell plates; not applied to the model | Lengthen the shells; keep the grab and restate PR-008 as 9 L net; raise the fill factor after a trial | HTS-STM-001 S9; HTS-CAL-001 section 8 |
| D17 | The hand winch can pull its 450 kg rating, so a snag could load the rope to 4.4 kN (factor 4.8) and leg A to 6.2 kN (STM S24) | **Proposed, awaiting Amish:** add a shear link or friction clutch rated at about 1.5 times the safe working load in the crank drive; not applied | Add a limiter; accept the stall case as it is; choose a winch rated nearer 300 kg | HTS-STM-001 S24 |

Standing instruction (2026-10-23): STEM-check fixes that keep the working principle are implemented and recorded here as decided under that instruction. The STEM check (HTS-STM-001) found no failing claim, so no such fix was made.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The winch's base hole pattern | Sets the four winch holes in the front bracket plate | HTS-DDR-002, C5 |
| 2 | The winch drum holds 15 m of 6 mm rope with three turns to spare, its first-layer rating is at least 450 kg, and its drum core is large enough for 7x19 rope (the model's core is 60 mm, D/d about 10) | R3 and R4 rest on these catalogue figures | HTS-CAL-001, A8 |
| 3 | The rope's certificate shows a minimum breaking load of at least 21 kN | Rope safety factor of 14.3 | HTS-CAL-001, A7 |
| 4 | The chain's working load limit is at least 5 kN, and 2.78 m plus the three lug shackles sets the 3.0 m foot circle | Chain tension 1,195 N at the design case; leg spread | HTS-CAL-001, section 3 |
| 5 | The sheave's bore is 20 mm, its width fits between cheeks 34 mm apart with the two washers, and its rating is at least 500 kg | Axle and cheek spacing | HTS-DDR-002, C3 |
| 6 | The ball-lock pins' 70 mm grip suits the 60 mm upper leg | Leg adjustment | HTS-DDR-002, C1 |
| 7 | The EN 362 connector's gate opening fits the rings of common rescue lines | Retrieval head use | HTS-DDR-001, D2 |
| 8 | A generic roller-applied digester sealant is sold in the first region, and its cure needs no entry | DomeReach | HTS-DDR-001, D8 |

## Value engineering

Value-engineering target: USD 5,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,838 (USD 2,162 under the target). Main cost drivers and savings worth trying:

- The largest lines are the hand winch (USD 320), the grab head (USD 260), the rim guard panels (6 x USD 48), the DomeReach head (USD 225), the sampler (USD 145) and the tripod head (USD 140).
- Galvanizing is priced at a minimum lot for each steel part; sending all steel parts in one lot is the simplest saving.
- The rim guard could use HDPE board on a steel tube frame from local stock, or reuse traffic barrier panels, if cost matters more than weight.
- Making the design constructable added the foot chain lugs and longer foot plates (USD 6 across three feet) and longer chains (USD 12).

## Decisions made

All decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Safe working load 150 kg for tool heads, proof 1.5 times; WellSling does not share the frame (D1) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | Retrieval head kept as a clip-on guide only; the haul is made with certified rescue equipment. Conservative safety option; relaxing it needs personnel certification of frame, winch and rope (D2) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | Two-speed hand winch with an automatic load brake, 450 kg (D3); 15 m of 6 mm 7x19 grade 316 rope (D4) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | 6082-T6 square aluminium legs, telescoping (D5); hot-dip galvanized S275 and A4 stainless (D6) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | DomeReach: 2.5 m design depth (D7), generic sealant (D8), single hinged arm and no gripper (D9) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | Requirements R13 (heads pass 560 mm) and R14 (stable at 10 degrees) added (D10) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | India first; first candidates to approach, not agreed: a municipal sewer department running mechanised cleaning, and a household biogas programme in India or Nepal (D11) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | Value-engineering target stays USD 5,000; overruns accepted; `budget_usd` unchanged (D12) | Amish, pre-approval quoted above | HTS-DDR-001 |
| 2026-10-03 | Design for construction C1 to C12: telescoping square legs, sleeved M16 joints, cheek-plate mast, winch bracket with stop bolt, clevis feet with outboard chain lugs, standard 10 mm tab, closing grab, pinned rim guard, guide-only retrieval head, single-hinge DomeReach, checked clearances | Amish, pre-approval quoted above | HTS-DDR-002 |
| 2026-10-03 | Appearance model adds only labels (safe working load, "never lift a person"), a street with a manhole and a 1.75 m person for scale; no change to the design | Amish, pre-approval quoted above | `docs/REVIEW.md`, 2026-10-03 |
