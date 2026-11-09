---
doc_id: HTS-STM-001
title: HatchSide STEM check
project: HatchSide
doc_type: STEM check
version: "0.2"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First STEM check, written at the kit 1.9.1 upgrade (stage P3) for option A (S1 to S18) and option B (S19 to S23)
- version: "0.2"
  date: '2026-11-05'
  author: Amish Chadha
  change: Independent review recorded; S9 and S12 moved to Plausible, S24 (winch at stall) added, S1 widened to the 10 degree rope case, S8 and S6 restated
---

# HatchSide STEM check

All 24 claims were checked against known science: 16 sit within known science and 8 are plausible and need a measurement or a supplier figure (grab output, the grab load carried by one person, winch drum size, grab breakout, sealant cure, corrosion life, ignition and grab closing force); none fails, so no fix to the working principle was needed. Two proposals that follow from the review (the grab volume and a load limiter) go to Amish as HTS-DEC-001 D16 and D17. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which reads its numbers from `docs/04-calcs/sizing.py` and the kit 1.9 model; results in `docs/04-calcs/stem_results.csv`.

The reference product is option A (the tripod and hand winch, the design since kit 1.7) at the design case: 150 kg safe working load times 1.5 for proof times 1.25 for jerk, 2,759 N on the rope. Option B (the straddle-frame davit) is checked at the same case.

## Claims checked

Table 1. Claims, governing science and verdicts.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Each leg of the tripod carries its share of 150 kg times the 1.5 proof and 1.25 dynamic factors, with the rope up to 10 degrees off vertical, without buckling | Physics | Strength of materials | Euler buckling of a pinned column, P = pi^2 E I / L^2, for the weaker 50 x 50 x 3 lower tube over the whole 2585 mm pin-to-pin length (6082-T6, E 69 GPa) gives 21.2 kN; the leg force is 3.85 kN with the rope vertical and 4.45 kN at 10 degrees in the worst direction; the limit is half the Euler load, a knock-down for imperfection and the telescoping joint; the 110 mm rope offset at the winch adds a bending moment that is not yet in the note (HTS-CAL-001 section 10) | 4.45 kN <= 10.62 kN | Within known science | HTS-CAL-001 section 3 |
| S2 | The 6 mm 7x19 stainless rope holds 150 kg with a factor of at least 5 | Physics | Strength of materials | Rope minimum breaking load 21 kN (catalogue figure used in the calculation note) over a working load of 1.47 kN: factor 14.3; a factor of 5 is the usual minimum for rope that lifts goods | 1.47 kN <= 4.2 kN | Within known science | HTS-CAL-001 section 3 |
| S3 | The tripod does not tip when the rope hangs 10 degrees off vertical at the safe working load | Physics | Mechanics and statics | Overturning about a foot edge: tan(angle) = (W + weight of the tripod, winch and rope) x inradius / (W x sheave height); inradius 750 mm, sheave 2413 mm, tripod 75 kg | 25 degrees >= 10 degrees | Within known science | HTS-CAL-001 section 6 |
| S4 | One person turns the winch against 150 kg at a comfortable cranking rate | Biology | Human physiology and biomechanics | Input power = load x rope speed / efficiency, with the low gear (10:1) at 40 rpm and efficiency 0.75; sustained hand-cranking about 75 W for an average adult; crank force 31 N at 250 mm | 32.9 W <= 75 W | Within known science | HTS-CAL-001 section 4 |
| S5 | The leg hinge and foot pins (M16) and the 4 mm aluminium walls carry the leg force in bearing and shear | Physics | Strength of materials | M16 A4-70 in double shear on the thread root 13.3 MPa (limit 0.6 x 450 MPa proof); bearing on the 4 mm upper-leg wall 30.1 MPa and, governing, on the 3 mm lower-leg wall at the foot pin 40.1 MPa (limit the 6082-T6 proof stress 250 MPa, so a ratio of 0.16); highest ratio shown | 0.16 of allowable <= 1 of allowable | Within known science | HTS-CAL-001 section 3 |
| S6 | The three leg-spread chains hold the feet in at the design case | Physics | Strength of materials | Chain tension 339 N (largest horizontal foot thrust over the square root of 3, equilateral layout; leg A below the winch carries the force less the rope pull) on two 6 mm wires of 28.3 mm2 each, about 6 MPa against a yield of about 250 MPa for low-carbon steel with a factor of 2; the calculation note also compares it with a 5 kN working limit for 6 mm grade 30 chain, to confirm on purchase | 6 MPa <= 125 MPa | Within known science | HTS-CAL-001 section 3 |
| S7 | The stop bolt (M12) that takes the rope pull on leg A holds at the design case | Physics | Strength of materials | Single shear 33.8 MPa on the thread root against 0.6 x 450 MPa; bearing on the leg wall 28.7 MPa against 250 MPa | 0.13 of allowable <= 1 of allowable | Within known science | HTS-CAL-001 section 3 |
| S8 | The 150 mm head sheave and the winch drum are large enough for the 6 mm rope | Engineering and technology | Manufacturing tolerances | Rope makers advise a sheave of many rope diameters for 7x19 rope (commonly 18 or more) to limit bending fatigue and strength loss; the standard to cite is to be assessed (HTS-REG-001, G12) | Sheave D/d = 20.8. The drum in the model has a 60 mm core, so D/d is about 10 at the core and about 13 on the outer layer; that is low for 7x19 rope, so the winch maker's drum size and rope recommendation govern. Confirm when the winch is bought (HTS-DEC-001, item 2) | Plausible, to confirm at TRL 3 | TRL 4 |
| S9 | The grab brings up at least 10 L of wet silt per cycle | Mathematics | Units and dimensional analysis | Two quarter-cylinder shells of 182 mm inside radius, geometric volume 15.4 L; 70 % fill gives 10.8 L, and about 10 % drips back on the way up (HTS-CAL-001 section 8), leaving 9.7 L | 9.7 L net against 10 L: 3 % short on estimates for the fill factor (70 %) and the drip (10 %), neither measured. At 72 % fill the net is 10 L; PR-008 is at risk (fix proposed to Amish: HTS-DEC-001 D16) | Plausible, to confirm at TRL 3 | TRL 4 |
| S10 | A full grab with its wet silt is within the winch's safe working load | Physics | Mechanics and statics | Grab 23.7 kg plus 19 kg of wet silt (1.8 kg/L, 10.8 L) against the 150 kg safe working load | 43.1 kg <= 150 kg | Within known science | HTS-CAL-001 section 8 |
| S11 | A grab buried in settled sludge frees with the pull the winch can give | Physics | Fluid mechanics | Breakout of an object from settled sludge is suction and shear that depend on the sludge; no cited figure was found | The 450 kg winch rating and the 150 kg safe working load leave room over the 43 kg full grab, but the real breakout force is not known; a jerk is covered by the 1.25 dynamic factor. Observe at a field trial (TRL 4) | Plausible, to confirm at TRL 3 | TRL 4 |
| S12 | The heaviest carried load can be carried by one person | Biology | Ergonomics | ISO 11228-1 gives a 25 kg reference mass under ideal conditions, before multipliers for distance from the body, grip and frequency; 25 kg is the project's own target (HTS-PRB-001), not the recommended limit | Heaviest packed load 23.7 kg (grab head, a bulky 370 x 372 x 772 mm shape) against the 25 kg target; the margin is 1.3 kg and the multipliers are not applied. Loads 1 and 2 travel together (29 kg) and the tripod is stood up by two people. Weigh each load and assess against ISO 11228-1 at TRL 4 | Plausible, to confirm at TRL 3 | TRL 4 |
| S13 | Every head, lowered with the grab closed, passes a 560 mm manhole clear opening with 20 mm to spare | Mathematics | Geometry | Plan diagonal of each head from the bounding box of its modelled parts; the 560 mm clear opening is the smallest common street manhole (PRB) | 525 mm <= 540 mm | Within known science | HTS-CAL-001 section 7 |
| S14 | The DomeReach arm reaches the floor of a 2.5 m deep household digester from the rim | Mathematics | Geometry | Hinge 2640 mm below the rim with the tiller 200 mm above it, plus the 700 mm arm: tool 3340 mm below the rim against the 2,500 mm depth assumed from household digester guidance | 3340 mm >= 2500 mm | Within known science | HTS-CAL-001 section 7 |
| S15 | A hand-applied roller coat of generic sealant on the dome headspace seals small leaks | Chemistry | Materials chemistry | Sealant types for biogas domes are flexible, moisture- or solvent-cured coatings; the cure in wet, methane and H2S headspace depends on the product (to assess in HTS-FEA-001) | The tool only places a generic sealant by type; whether a product cures on a wet dome is the supplier's claim and needs a field check. No product is named | Plausible, to confirm at TRL 3 | TRL 4 |
| S16 | Galvanized steel, 6082 aluminium and A4 stainless fasteners last in sewer splash if the dissimilar metals are isolated | Chemistry | Corrosion | Zinc and aluminium are anodic to stainless steel in wet, chloride and sulfide environments; nylon and stainless washers isolate the aluminium legs from steel fasteners; hydrogen sulfide attacks zinc and copper alloys over time | Isolation is in the model (nylon washers and strips). Life in sewer atmospheres is not known from a cited source; coupon test at TRL 4 (R11 / PR-011) | Plausible, to confirm at TRL 3 | TRL 4 |
| S17 | The kit makes no ignition source in a flammable atmosphere | Chemistry | Combustion and hazards | Ignition needs a spark, heat or static discharge in a flammable mixture (methane, H2S); hand tools and a mechanical winch have no electrics, but steel on steel or on concrete can spark and polyester rope can build static | No claim of intrinsic safety is made. The kit is used only after a certified gas detector reads safe and ventilation is running; ATEX or similar assessment is outside the scope and listed in HTS-REG-001 | Plausible, to confirm at TRL 3 | TRL 4 |
| S18 | A clamshell grab of 3 mm sheet shells and a 6 mm bar yoke closes on the 10 mm working line | Physics | Mechanics and statics | Closing lever action: the working line pulls the yoke, which rotates the shells about the 25 mm hinge pin; the force the line needs depends on silt resistance | Geometry shown in the model; the closing force against compacted sludge is not calculated here and is to be measured at TRL 4 | Plausible, to confirm at TRL 3 | TRL 4 |
| S19 | The 100 x 100 x 5 mast carries the boom moment and the load (option B) | Physics | Strength of materials | Bending M = design load x 1125 mm = 3104 N m on a section modulus of 57 cm3, plus axial load; S275 at 0.9 of yield | 57 MPa <= 248 MPa | Within known science | HTS-CAL-001 section 11 |
| S20 | The 80 x 80 x 4 boom carries the load at its tip (option B) | Physics | Strength of materials | Cantilever M = design load x 982 mm = 2711 N m plus the rope's axial pull; 80 x 80 x 4 section modulus 29 cm3, S275 at 0.9 of yield | 95 MPa <= 248 MPa | Within known science | HTS-CAL-001 section 11 |
| S21 | The four M16 bolts of the boom root hold the boom to the mast (option B) | Physics | Strength of materials | Couple on a 90 mm row spacing: tension 15.1 kN per upper bolt against 0.6 x 450 MPa x 157 mm2 = 42.4 kN | 15.1 kN <= 42.4 kN | Within known science | HTS-CAL-001 section 11 |
| S22 | The mast spigot joint (two M16 bolts on 200 mm) and the rear cross rail carry the bending moment (option B) | Physics | Strength of materials | Joint bolt shear 49 MPa and bearing 97 MPa; rear cross rail bending 151 MPa under the uplift of the rear bolt pair; highest ratio shown against 0.6 x 450 MPa shear, 275 MPa bearing and 0.9 of yield in bending | 0.61 of allowable <= 1 of allowable | Within known science | HTS-CAL-001 section 11 |
| S23 | The straddle frame does not tip with the rope 10 degrees off vertical (option B) | Physics | Mechanics and statics | The load line is inside the frame's support rectangle; tip angle about each edge from the centre of mass of the frame, mast, boom and winch; smallest of three directions | 46.5 degrees >= 10 degrees | Within known science | HTS-CAL-001 section 11 |
| S24 | At stall the hand winch cannot overload the rope or the legs (option A) | Physics | Strength of materials | The winch can pull up to its 450 kg first-layer rating, not only the 150 kg safe working load: rope pull 4414 N against a 21 kN minimum breaking load (factor 4.8) and leg A 6.16 kN against 21.2 kN Euler (factor 3.4); an accident case, checked for a factor of 2 on the rope and 1.5 on buckling | 0.43 of allowable <= 1 of allowable | Within known science | HTS-CAL-001 section 3 |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails**. A "Plausible" row stays open until the measurement named in its check; "TRL 4" in the last column means a test or a supplier figure that cannot be had on paper.

## Fields not relevant

- Biology: no living material is in the design. Human effort (S4) and carried loads (S12) are checked as ergonomics, and exposure to gas and sewage is a hazard in HTS-RSK-001, not a claim.
- Chemistry: no reaction is claimed except the sealant cure (S15) and corrosion (S16); neither is calculated.

## Concept options

STEM verdict for each option in HTS-OPT-001.

- Option A, tripod and hand winch (S1 to S18 and S24): within known science on 11 claims (S1 to S7, S10, S13, S14 and S24); 8 plausible rows are open to field or supplier data or a TRL 4 weighing.
- Option B, straddle-frame davit (S19 to S23): within known science on all five claims, with large strength margins and a tip angle of 46 degrees. No option has a Fails row. Option B's miss is a requirement (PR-006, a 26.2 kg side rail), not a science claim, so it is not recorded here.

## Independent review

A second reviewer (a headless `claude -p --model claude-opus-5-5` session) was given only this document, the script and its results, the calculation note HTS-CAL-001, the requirements HTS-PRS-001 and `sizing.py`, without the author's reasoning, and was asked to refute the headline results and every "Within known science" verdict. It re-derived every headline number (leg forces 3,850 and 1,091 N, Euler load 21.2 kN, rope factor 14.3, tip angle, crank force 31 N, mast and boom stresses) and found no arithmetic error. It disputed load paths, missing load cases and limits. What changed:

Table 2. Review findings and what was done.

| Finding | Disposition |
| --- | --- |
| S9: the calculation note says about 10 % of the silt drips back, so the grab nets 9.7 L, below the 10 L of PR-008 | Accepted. S9 moved to Plausible; PR-008 is now **At risk**; a bigger grab or a lower target goes to Amish (HTS-DEC-001 D16). The wording "half-cylinder" was wrong and is back to "quarter-cylinder shell" |
| S12: 25 kg is the ISO 11228-1 reference mass before multipliers, not a recommended limit; the margin is 1.3 kg | Accepted. S12 moved to Plausible; the 25 kg is stated as the project's own target; weigh and assess at TRL 4 |
| The hand winch can pull its 450 kg rating at stall, 4.41 kN on the rope (factor 4.8) and 6.16 kN in leg A (Euler factor 3.4) | Accepted. S24 added and within an accident-case rule of 2 on the rope and 1.5 on buckling; a shear link or load limiter is proposed to Amish (D17) |
| S1: with the rope 10 degrees off vertical the worst leg force is 4.45 kN, not 3.85 kN; the 110 mm rope offset adds bending; Euler ignores imperfection | Accepted. S1 now uses the 10 degree case and half the Euler load as its limit (factor 2.4); the offset moment is listed as a limit of the note (HTS-CAL-001 section 10) |
| Table 2 of the calculation note: the foot reactions did not balance (vertical sum 5,086 N against 2,759 N); leg A below the winch carries 1,091 N, so the chain tension is about 339 N, not 1,195 N | Accepted. HTS-CAL-001 and `sizing.py` corrected (foot 920 N vertical and 586 N horizontal on every foot); S6 restated; the earlier figure was conservative |
| A9 and S8: the model drum has a 60 mm core, so D/d is about 10 at the core, low for 7x19 rope | Accepted. S8 says so and stays Plausible; the winch maker's drum size and rope advice are to be confirmed on purchase (HTS-DEC-001, item 2) |
| S3: stale "75 kg" tripod mass in the table; the winch moves the centre of mass and costs about 1 degree | The table is regenerated from `sizing.py` (74.7 kg); the tip angle is a first-order figure with a margin of 2 times the 10 degrees required, which a degree does not change |
| S5: the 0.16 ratio is the 3 mm foot pin wall, not the 4 mm hinge wall; the shear area differs between S5 and S21 | Label fixed. The two shear areas are the thread root area and the stress area; both are small against the limit |
| S13: a clamshell may be lowered open | The model and the note use the closed grab; the check now says so |
| S7: which leg wall the bracket sits on | The bracket stands 1,044 to 1,270 mm from the hinge pin, on the 4 mm upper leg; prying from the offset is not checked |
| Option B: rolled section is about 5 % weaker than the sharp-corner modulus; the front cross rail and the side rails were not checked; the rope's axial load in the mast | Noted in HTS-CAL-001 section 11 as not checked; margins of 1.6 to 3 cover the 5 % |
| The 75 W hand-cranking value has no source | It is the screening value in `.kit/stem_check.py`; no external source was found; marked in the note |

No verdict moved from Plausible to Within, and no claim fails.

## Sources

- Euler column buckling, strength of materials: any standard textbook; 6082-T6 properties as in HTS-CAL-001, Table 1 (A4, A5, A6).
- ISO 11228-1, manual handling: lifting and carrying, reference mass 25 kg before multipliers (clauses not read).
- Sustained hand-cranking power of about 75 W: the screening value in `.kit/stem_check.py` (`limits.HUMAN_SUSTAINED_W`); no external source was found.
- Rope minimum breaking load 21 kN for 6 mm 7x19 grade 316: catalogue value, to confirm on purchase (HTS-DEC-001, item 3).
- Wire rope bending: rope-maker guidance on sheave diameter, not read from a named standard; "to assess" in HTS-REG-001, G12.
- Regulatory and market sources: HTS-REG-001 and HTS-MKT-001.
