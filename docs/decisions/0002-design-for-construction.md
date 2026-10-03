---
doc_id: HTS-DDR-002
title: HatchSide design for construction
project: HatchSide
doc_type: Design decision record
version: "1.0"
status: Released
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "1.0"
  date: '2026-10-03'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, decided under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish Chadha under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

STANDARDS section 18 asks for a design in which every part can be made with the stated process and every part fits and fastens to its neighbours (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 2 concept named ten components (tripod, mast and head sheave, hand winch, head interface, five heads and a rim guard) as massing shapes with no joints, no way to hold the winch, no anchorage for the leg-spread chain and no way to close the grab. The changes below keep what HatchSide does and its pitch: a tripod over the opening, a hand winch, one head interface and five heads, all worked from the rim. None changes the safety case except to make it more conservative (C10).

Every change is in `cad/src/model.py`. Its checks (`python cad/src/model.py --check`) test 31 pairs of neighbouring parts for interference, all at 0 mm³, and eight clearances, all positive (Table 2).

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| C1 | Legs | Three adjustable legs, shape not defined | Square 6082-T6 tube: 60 x 60 x 4 upper, 50 x 50 x 3 lower sliding inside it with 2 mm total clearance, three adjust holes at 75 mm pitch, one 12 mm ball-lock pin | Square tube telescopes without turning, takes a pin through flat walls and needs no machining |
| C2 | Leg hinges and foot joints | Not defined | M16 A4 bolts through steel crush sleeves (25 x 3.5 mm) pressed between the tube walls, between 8 mm lug pairs (head) and 8 mm clevis plates (feet), with nylon isolating washers | A bolt alone would crush the thin aluminium walls; the sleeve carries the clamp load and stops galvanic contact |
| C3 | Mast | A separate mast above the tripod | Two 6 mm steel cheek plates welded to the 10 mm head plate, carrying the sheave on an M20 axle; sheave height set so the rope from the winch runs parallel to leg A, 110 mm outside its centre line | No separate mast to make or join; the rope never touches the leg or the plate |
| C4 | Rope keeper | None | A 12 mm bar across the cheeks 10 mm above the rope | Stops the rope jumping off the sheave when slack |
| C5 | Winch mounting | None | Front and back 8 mm clamp plates round leg A with four M10 bolts, sitting under an M12 stop bolt through the leg that takes the rope pull | A friction clamp on aluminium can slide; the stop bolt makes the load path positive |
| C6 | Feet and chain | A leg-spread chain with no anchorage | Steel feet: 140 x 280 x 8 base plate, two clevis plates, an outer chain lug with a 14 mm hole 140 mm outboard of the clevis, a 10 mm bonded rubber pad; 6 mm chains shackled lug to lug, clear of the clevis plates | Gives the chain a fixing and the foot a flat bearing; the lug sits far enough out that the chains pass 12 mm clear of the clevis plates |
| C7 | Head interface | "One published coupling" | A 10 mm steel tab, 60 wide, with a 20 mm hole 30 mm below its top edge on every head; a 3/8 in screw-pin bow shackle and a 500 kg swivel on the rope eye | A single, published, tool-free coupling (R7) that any workshop can copy |
| C8 | Grab | A clamshell shape | Two rolled 3 mm shells with 5 mm end plates interleaved on a 25 mm hinge pin, four 30 x 6 tag rods to a 10 mm head beam, and a closing yoke worked by a working line through a snatch block on the head plate and tied off on a cleat on leg B | Closes from the rim with no power and no entry |
| C9 | Rim guard | A barrier ring | Six 746 x 400 mm aluminium frames on a hexagon, each with an HDPE splash board, joined at the corners by 12 mm drop pins through interleaved rings | Flat panels pack; drop pins need no tools |
| C10 | Retrieval head | A "retrieval harness head" that lifts | A funnel guide with an EN 362 auto-locking connector on a short steel sling, steered by a 2 m pole; the haul is made with certified rescue equipment, never with the HatchSide winch (HTS-DDR-001, D2) | Conservative: the material winch is not rated for people |
| C11 | DomeReach | A head shape | Two 50 x 3 aluminium pole sections with a sleeve and pin, a top cap with the standard tab, a tiller on a clamp collar, a clevis and a single 700 mm arm on a 12 mm pin worked by a pull line through a fairlead | Single hinge, no gripper (patent design-around); folds to pass a 560 mm opening |
| C12 | Clearances | Not checked | Sheave rim 17.8 mm above the head plate; upper leg top corner 18.6 mm below it; lower leg end 13.3 mm above the foot plate; lower leg top 19.4 mm from the stop bolt at the shortest setting; chains 12 mm clear of the clevis plates and 111.5 mm outside the rim guard | Measured from the model so nothing rubs or jams at any leg setting |

*Table 2. Constructability checks from the model.*

| Check | Result |
| --- | --- |
| Interference between 31 pairs of neighbouring parts | 0 mm³ in every pair |
| Leg overlap at normal length / longest setting | 305 mm / 230 mm |
| Lower leg top to stop bolt edge, shortest setting | 19.4 mm |
| Upper leg top corner to head plate | 18.6 mm |
| Sheave rim to head plate | 17.8 mm |
| Lower leg end corner to foot plate | 13.3 mm |
| Chain edge to clevis plate where the chain passes the clevis end | 12.0 mm |
| Chain to rim guard frame, mid-side | 111.5 mm |

## Consequences

- BOM lines 1 to 24 are priced for the constructable parts; the estimated cost is USD 2,838 against the USD 5,000 value-engineering target.
- The general arrangement drawing HTS-DWG-001 moves to Rev P2; making sketches HTS-DWG-101 to HTS-DWG-112 are added.
- HTS-CAL-001 is computed from this design.
- `design_state: constructable` is set in `project.yaml`.
- Facts that can only be settled with real parts (winch base holes, drum capacity, chain working limit, sheave bore) are in the design decisions register under "To confirm when parts are bought".
