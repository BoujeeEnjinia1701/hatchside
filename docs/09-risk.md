---
doc_id: HTS-RSK-001
title: HatchSide risk register and hazard analysis
project: HatchSide
doc_type: Risk register
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

# HatchSide risk register and hazard analysis

The top risks are that the kit is mistaken for rescue or fall-protection equipment (H1), that a load or a person falls into the opening (H2, H3), that the tripod tips on soft ground or a slanted rope (H4) and that the people who would build it cannot get catalogue ratings for the winch, rope and chain (P1). All the design controls are in the model; none has been tested. Method: STANDARDS section 23 and ISO 12100 as guidance (HTS-REG-001, G8). Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection is 1 (certain to be seen) to 5 (cannot be seen).

> **Safety:** HatchSide is used over an open confined space whose air can kill in seconds. Every control below assumes a certified gas detector, a no-entry rule, a guarded opening and a crew that has read the labels. The kit never lifts or lowers a person.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Winch, rope or chain ratings are lower than the catalogue figures used | Different supplier or an unrated import | Safety factors in CAL-001 fall; the kit is unsafe for its SWL | 3 | 5 | Design lead | Keep the checks in HTS-DEC-001 items 2 to 4; buy with certificates; proof load at TRL 4 |
| P2 | No co-design partner agrees | Candidates are not yet approached | Needs stay unconfirmed (HTS-URS-001 is a desk draft) | 3 | 4 | Amish | Approach the candidates in HTS-PRB-001; record the outcome |
| P3 | Legal review finds the kit is lifting machinery in a market | The machinery definition and local rules differ (HTS-REG-001 G6) | Certification cost or a sales ban | 3 | 4 | Design lead | Get a qualified review before any sale; state the non-certified status everywhere |
| P4 | Corrosion in sewer air is faster than expected | Hydrogen sulfide, chloride and mud | Early replacement of aluminium legs or fasteners | 3 | 3 | Design lead | Coupon test at TRL 4; sacrificial nylon washers; replace-by-inspection plan |
| P5 | A patent holder objects to DomeReach | Bandicoot patents and litigation noted in HTS-PRB-001 | Redesign of the arm | 2 | 3 | Design lead | Single hinge, no gripper; freedom-to-operate check is to assess (G15) |
| P6 | Local galvanizing or welding quality is poor | Load-path welds by an untrained welder | Weak head or winch bracket | 3 | 4 | Local fabricator | Weld sizes are drawn as beads in the model; competent-welder note in BLD-001; proof load |
| P7 | Cost rises above the USD 5,000 target | Winch and rope price | Kit unaffordable for the target users | 2 | 3 | Amish | The estimate is USD 2,838; the winch is the swing line (MKT) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | The kit is used to lift or lower a person | Crew treats it as a rescue tripod; the retrieval head invites a haul | Fall, rope failure, death | 5 | 3 | Labels on winch and heads (PR-018); guide-only retrieval head (HTS-DDR-001, D2); winch brake sized for material; instructions say never | Medium: depends on the crew; no design can remove the misuse |
| H2 | A tool head or load falls into the opening | Shackle pin not tightened; rope parted | Injury below; spill into the water | 4 | 2 | Screw-pin shackles with moused pins; 14.3 rope factor; head interface gauge plate; nobody under a raised load | Low |
| H3 | A person or the crew's feet slip into the opening | Open manhole, wet ground | Fall into the space | 5 | 2 | Six-panel rim guard with drop pins and splash boards (PR-015); cones and barrier chain | Low to medium |
| H4 | The tripod tips or a foot slides | Soft ground, slanted rope, dragged load | Crush, load dropped into the opening | 4 | 3 | Tip angle 25.0 degrees against 10 required (PR-014); chains hold the spread; boards under the feet on soft ground | Medium on soft or sloping ground |
| H5 | Toxic or flammable atmosphere reaches the crew | Gas released when sludge is lifted | Poisoning, fire | 5 | 3 | Certified gas detector before and during work; ventilation; no ignition claim (STM S17); crew stays upwind | Medium |
| H6 | Fingers caught in the winch, sheave or snatch block | Hands near the drum or rope | Crush injury | 3 | 3 | Drum flanges on the winch; gloves and hands kept clear of the drum and sheave; the cleat keeps the working line off the sheave; a guard over the drum is a TRL 4 question | Low |
| H7 | Vehicle strikes the crew or the frame | Street manhole in traffic | Injury | 5 | 2 | Cones, barrier chain and local work-zone rules (G11) | Medium until the city rules are known |
| H8 | Back strain from carrying or setting up | Loads near 25 kg, a bulky grab, and legs and head stood up together | Musculoskeletal injury | 2 | 3 | No load over 25 kg (PR-006); two-person stand-up of the tripod; ISO 11228-1 assessment of each load at TRL 4 (STM S12) | Low to medium |
| H9 | Contact with sewage, sludge or digester sealant | Splash at the rim | Infection, skin or eye harm | 3 | 4 | Splash boards; gloves and eye protection; wash; sealant SDS (G13) | Low to medium |
| H10 | A grab or rake snags and the winch overloads | Debris in the sewer | Jerk on the rope and legs; at stall the rope pulls 4.4 kN | 3 | 3 | 1.25 dynamic factor in CAL-001; stall case checked (STM S24: rope factor 4.8, leg factor 3.4); a shear link is proposed (HTS-DEC-001 D17); stop and free by hand lines | Low to medium |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Winch brake | Hold the load when the crank is released | Brake slips | Load runs down into the opening | Worn pawl or oil on the brake | 5 | 2 | 3 | 30 | Buy a winch with an automatic load brake; inspect before each shift; proof load |
| F2 | Wire rope 6 mm | Carry the load from drum to head | Rope breaks or kinks | Head and load fall | Sharp bend, corrosion, overload | 5 | 2 | 3 | 30 | 316 rope, factor 14.3; D/d 20.8 on the sheave; discard rules; thimble and ferrules |
| F3 | Swaged ferrule and thimble | End fitting of the rope | Ferrule slips | Head falls | Poor swage by a local shop | 5 | 2 | 4 | 40 | Rope made by the supplier with the swaged eye; no field swaging |
| F4 | Screw-pin shackle (interface) | Joins the swivel to the head tab | Pin works loose | Head falls | Vibration, unmoused pin | 5 | 2 | 2 | 20 | Mouse the pin; check at each head change; spare shackle in the kit |
| F5 | Leg (50 x 50 x 3 and 60 x 60 x 4) | Carry compression | Buckles | Tripod collapses | Overload, bent tube, wrong pin setting | 5 | 1 | 2 | 10 | Euler factor 5.5; inspect for dents; ball-lock pins fully home |
| F6 | Leg adjust pin | Hold the telescoped length | Pin not engaged | Leg slides | Pin not fully through | 4 | 3 | 2 | 24 | Ball-lock pin gives a click; lanyard; check at set-up |
| F7 | Hinge and foot bolts (M16) with crush sleeves | Join legs to head and feet | Bolt loosens or sleeve missing | Leg flops | Vibration, wrong assembly | 4 | 2 | 3 | 24 | Nylock nuts; sleeves drawn on the sheets; check at set-up |
| F8 | Leg-spread chain | Hold the feet on the 3.0 m circle | Chain or shackle parts | Feet spread | Overload, corrosion | 4 | 2 | 3 | 24 | Chain tension 1,195 N; confirm working load at purchase (HTS-DEC-001, item 4) |
| F9 | Head plate welds and cheeks | Carry the sheave axle and legs | Weld cracks | Head collapses | Poor welding, fatigue | 5 | 2 | 4 | 40 | Welds drawn as beads in the model; competent welder; magnetic-particle check is outside TRL 3 |
| F10 | Winch bracket and stop bolt | Carry the rope pull into leg A | Clamp slips or bolt shears | Winch slides down the leg | Stop bolt omitted | 4 | 2 | 3 | 24 | M12 stop bolt takes the pull (shear 33.8 MPa); clamp only keeps it square |
| F11 | Grab hinge pin and shells | Close and hold silt | Pin falls out | Shell drops silt | R-clip missing | 3 | 3 | 2 | 18 | R-clips on pins; check before lowering |
| F12 | Sampler caps | Close the tube at depth | Caps open early | Sample lost | Cord stretched, latch worn | 2 | 3 | 3 | 18 | Elastic cord kept in the spares; trip latch checked |
| F13 | DomeReach arm and pivot | Reach the dome seam | Arm drops or pin lost | Tool lost in the digester | Split pin missing | 3 | 3 | 3 | 27 | Split pin through the 12 mm pivot; pull line; recoverable by the pole |
| F14 | Rim guard panel | Stop feet and tools going in | Panel not pinned | Gap in the guard | Crew skips the drop pin | 4 | 3 | 2 | 24 | Drop pins on lanyards; set-up checklist |
| F15 | Labels | Tell the crew what the kit is not | Label missing or illegible | Misuse (H1) | Weather, wear | 5 | 3 | 3 | 45 | Labels on winch and every head; replaceable; training note |

RPN above 30 means a control is already in the design and is named in the Action column; none has been tested.

## Option B

Option B (HTS-OPT-001) adds failure modes the tripod does not have: a bolted mast and boom joint that carries a moment (FMEA S 5, O 2, D 3), a frame that has to stand level on a street (H4) and heavier parts that raise H8. Its first-pass FMEA is not repeated here because the concept is not chosen; it would be written if Amish selects B.
