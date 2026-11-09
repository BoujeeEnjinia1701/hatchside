---
doc_id: HTS-CAL-001
title: HatchSide sizing and first-principles checks
project: HatchSide
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First calculation note at TRL 3, from the constructable model (HTS-DDR-002)
- version: "0.2"
  date: '2026-11-05'
  author: Amish Chadha
  change: Kit 1.9.1 upgrade; masses and head sizes re-read from the D3 model (HTS-DDR-004); section 11 added for option B and PR-015 to PR-018 for the new requirements
---

# HatchSide sizing and first-principles checks

The constructable HatchSide meets every requirement that can be checked on paper except one at risk: the grab nets 9.7 L against 10 L once the drip is counted (R8, PR-008). At the design case (150 kg safe working load, times 1.5 for proof, times 1.25 for jerk) the most loaded leg carries 3.85 kN against an Euler buckling load of 21.2 kN, the rope has a safety factor of 14.3 at the safe working load, the tripod tips only when the rope is about 25 degrees off vertical, no packed load exceeds 23.7 kg, and every head except DomeReach passes a 560 mm manhole opening as it hangs (DomeReach passes with its arm folded). The estimated parts cost is USD 2,838 against the USD 5,000 value-engineering target. The rope also holds with the winch at stall (factor 4.8). Corrosion resistance (R11) cannot be shown on paper and is left to a TRL 4 coupon test.

All numbers are first-principles estimates from the model geometry; nothing has been built or measured. The script `docs/04-calcs/sizing.py` reads the geometry from `cad/src/model.py` and the prices from `bom/bom.csv`, prints every number in this note and writes `docs/04-calcs/results.csv`.

> **Safety:** HatchSide lifts loads over an open confined space. These calculations size a material-handling frame for tool heads only. They do not qualify the frame, winch or rope for lifting, lowering or rescuing people, and the design is not certified equipment. A proof-load test with a competent person (CalRig, TRL 4) must come before any use over a real opening.

## 1. Assumptions

*Table 1. Assumptions.*

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A1 | Safe working load at the head interface | 150 kg | R4 |
| A2 | Proof load factor | 1.5 | R4 |
| A3 | Dynamic factor for snatch when a grab breaks free of silt | 1.25 | Engineering judgement for a hand winch (slow rope speed) |
| A4 | Aluminium 6082-T6 tube: elastic modulus, 0.2 % proof | 69,000 MPa, 250 MPa | Handbook values; welds are not used on the legs |
| A5 | S275 plate yield | 275 MPa | EN 10025 |
| A6 | A4-70 stainless bolt, 0.2 % proof | 450 MPa | ISO 3506 |
| A7 | 6 mm 7x19 grade 316 rope minimum breaking load | 21 kN | Conservative catalogue value |
| A8 | Winch rating | 450 kg on the first layer, about half on a full drum | Typical two-speed hand winch |
| A9 | Effective drum radius with a few layers on | 40 mm | Model drum and rope |
| A10 | Winch gear ratios, crank, efficiency | 4:1 and 10:1, 250 mm, 0.75 | Typical two-speed hand winch |
| A11 | Comfortable cranking rate | 40 rpm | Engineering judgement |
| A12 | Grab fill factor in wet silt | 70 % | Estimate |
| A13 | Wet silt density | 1.8 kg/L | Estimate |
| A14 | Smallest common manhole clear opening | 560 mm | Common street manhole size in India |

## 2. Geometry

The legs are pinned on a 220 mm circle at the head, 2,250 mm above the ground, and on a 3,000 mm circle at the feet. Each leg is 2,585 mm pin to pin and leans 32.5 degrees from vertical. The feet form an equilateral triangle with 2,598 mm sides; the shortest distance from the centre to a side (the tipping edge) is 750 mm. The sheave centre is 2,413 mm above the ground and the top of the mast is 2,515 mm. The sheave is 125 mm across at the rope, so the ratio of sheave to rope diameter is 20.8. The upper and lower legs overlap by 305 mm at normal length and by 230 mm at the longest setting; the adjust pin gives 75 mm either way along the leg.

The sheave height is set so that the rope from the winch drum runs parallel to leg A, 110 mm outside its centre line, and drops vertically on the axis of the opening. This keeps the rope clear of the leg and the head plate without a separate mast.

## 3. Structure

The design case is the safe working load times the proof factor times the dynamic factor: 1,472 N x 1.5 x 1.25 = 2,759 N on the rope. Because the rope also runs from the sheave down along leg A to the winch, the head sees the load downward plus the same pull along leg A. Solving the three leg directions for equilibrium gives the forces in Table 2.

*Table 2. Structural checks at the design case (2,759 N on the rope).*

| Check | Result | Limit or comparison | Margin |
| --- | --- | --- | --- |
| Leg compression, leg A (winch leg) | 3,850 N | | |
| Leg compression, legs B and C | 1,091 N each | | |
| Euler buckling, whole leg taken as the weaker 50 x 3 mm section over 2,585 mm | 21.2 kN | 3,850 N | 5.5 (4.8 with the rope 10 degrees off vertical) |
| Axial stress in the 50 x 3 mm tube | 6.8 MPa | 250 MPa | Large |
| Hinge bolt bearing on the 4 mm upper leg walls | 30.1 MPa | About 250 MPa | Large; the steel crush sleeve stops the walls closing |
| Foot bolt bearing on the 3 mm lower leg walls | 40.1 MPa | About 250 MPa | Large |
| M16 bolt, double shear on the thread root | 13.3 MPa | About 260 MPa | Large |
| Head lug bearing (8 mm S275) | 15.0 MPa | About 275 MPa | Large |
| Vertical force at the feet | 920 N at each foot (leg A below the winch carries 1,091 N, the winch's pull of 2,759 N having left the leg above it) | | |
| Horizontal thrust at the feet | 586 N at each foot | | |
| Leg force with the rope 10 degrees off vertical, worst direction | 4,453 N | Half the Euler load, 10.6 kN | 2.4 |
| Winch at stall (450 kg rating): rope pull and leg A force | 4,414 N rope (factor 4.8); 6,160 N in leg A (Euler factor 3.4) | Accident case: 2 on the rope, 1.5 on buckling | Met; a load limiter is proposed (HTS-DEC-001 D17) |
| Leg-spread chain tension | 339 N | About 5 kN working limit for 6 mm grade 30 chain (to confirm on purchase) | About 15 |
| M12 stop bolt, single shear | 33.8 MPa | About 260 MPa | Large |
| Stop bolt bearing on the 4 mm leg wall | 28.7 MPa | About 250 MPa | Large |
| Rope safety factor at the safe working load | 14.3 | 5 or more for a material hoist | Met |
| Rope safety factor at proof load | 9.5 | | Met |

Buckling governs the legs, and even then the margin is 5.5 with the whole leg taken as the weaker section. The stresses at the bolts and lugs are low because the joints were sized for handling, stiffness and wear rather than strength. The chain working limit is a typical catalogue figure and is listed in the design decisions register to confirm when the chain is bought. The version 0.1 note gave the chain tension as 1,195 N because it took leg A's full force at the foot; the independent review (HTS-STM-001) showed that the winch's pull leaves the leg above the winch, so the foot reactions now balance at 920 N vertical each.

## 4. Winch effort and rope speed

With a 40 mm effective drum radius, a 250 mm crank and 75 % efficiency, lifting 150 kg in low gear (10:1) needs a crank force of about 31 N, and lifting a 50 kg loaded grab in high gear (4:1) about 26 N. At 40 rpm the rope moves 2.51 m/min in high gear and 1.01 m/min in low gear. Both forces are comfortable for one person. The winch is a material winch with an automatic load brake, so the load holds when the crank is released.

## 5. Masses and packed loads (R6)

Masses come from the kit 1.9 model of option A (`cad/src/model.py`, `components("A")`): every part has its stock, material and solid, so the mass of each load is the sum of its parts by BOM line, with 2.1 kg added for the working line.

*Table 3. Packed loads.*

| Load | Contents | Mass |
| --- | --- | --- |
| 1 | Head, mast, sheave, snatch block, hinge bolts, head interface | 18.6 kg |
| 2 | Upper legs (3) with adjust pins | 10.7 kg |
| 3 | Lower legs (3) with feet, pads and foot bolts | 22.1 kg |
| 4 | Winch, bracket, rope, line counter, cleat, working line | 19.3 kg |
| 5 | Rim guard panels (6), drop pins and leg-spread chains | 20.9 kg |
| 6 | Grab head | 23.7 kg |
| 7 | Sampler head | 9.6 kg |
| 8 | Rake head and retrieval head | 18.5 kg |
| 9 | DomeReach head (two pole sections, arm, roller) | 9.6 kg |

The tripod with winch and rope is about 74.7 kg and the whole kit about 153.0 kg. The heaviest load, the grab, is 23.7 kg, under the 25 kg limit of R6. In use the legs stay bolted to the head (loads 1 and 2 travel together on a cart) and the crew stands the tripod as one piece.

## 6. Stability (R14)

The tripod tips over the nearest edge of the foot triangle when the moment of a sideways rope pull about that edge exceeds the restoring moment of the rope load and the tripod's own weight. With the sheave 2,413 mm high, the edge 750 mm from the centre and a 74.7 kg tripod, the largest rope angle from vertical before tipping is 25.0 degrees at the safe working load and 22.5 degrees at proof load. The requirement is to stay stable with the rope 10 degrees off vertical, so the margin is more than double. Crews keep the rope within 10 degrees and never drag a load sideways with the winch.

## 7. Tool heads

**Grab (R8).** Each clamshell is a quarter cylinder 182 mm inside radius. The two shells together hold 15.4 L; at 70 % fill that is 10.8 L, about 19 kg of wet silt per cycle.

**Sampler (R9).** The clear tube is 75 mm outside, 3 mm wall and 600 mm long, so it holds 2.24 L. Its centre is 420 mm below the shackle pin and the line counter reads to 0.1 m, so the sample centre is known to within 0.2 m.

**DomeReach (R10).** With the tiller kept 200 mm above the rim, the arm hinge reaches 2,640 mm below the rim and the end of the arm 3,340 mm. The arm swings out 495 mm at 45 degrees. A household fixed-dome digester depth of 2.5 m is assumed for R10.

**Passing the opening (R13).** Plan sizes of each head as it hangs (Table 4). Each must fit a 560 mm opening with 20 mm to spare, so the largest plan diagonal allowed is 540 mm.

*Table 4. Head plan sizes.*

| Head | Plan size (mm) | Height (mm) | Plan diagonal (mm) | Passes 560 mm |
| --- | --- | --- | --- | --- |
| Grab | 370 x 372 | 772 | 525 | Yes |
| Sampler | 150 x 150 | 836 | 212 | Yes |
| Rake | 400 x 65 | 740 | 405 | Yes |
| Retrieval head | 300 x 300 | 546 | 424 | Yes |
| DomeReach, arm folded, below the tiller | 70 x 258 | 3,865 | 267 | Yes |

## 8. Grab output and setup time (R5)

The 10.8 L is the gross figure at 70 % fill; with the 10 % that drips back on the way up the grab nets 9.7 L, so R8 (PR-008) is **at risk** on these estimates (HTS-DEC-001 D16).

At 3 m depth in high gear, one grab cycle (lower, close, lift, swing to the bin) takes about 3.9 minutes, about 15 cycles and about 166 L of silt per hour (estimate). About 10 % drips back down the shaft.

The setup estimate is 9.0 minutes for two people: cone off the site and lift the cover (1.5 min), lay out the feet and chains (1.0), stand the tripod with the legs already bolted to the head (2.0), set the leg pins and check level (1.5), hang the head on the rope already reeved (1.0), and pin the rim guard round the opening (2.0). The winch stays on leg A in transport.

## 9. Results against the requirements

*Table 5. Results (also written to `docs/04-calcs/results.csv`).*

| ID | Requirement | Result | Status |
| --- | --- | --- | --- |
| R1 | No entry for any task | Every head fitted, worked and recovered from the rim | Met on paper |
| R2 | Fits openings 0.5 to 1.2 m | Feet on a 3.0 m circle; rim guard inner face at 672 mm radius | Met on paper |
| R3 | Working depth 10 m | 15 m of rope; drum capacity to confirm when the winch is bought | Met on paper |
| R4 | Safe working load 150 kg, proof 1.5 times | Buckling margin 5.5; rope safety factor 14.3 | Met on paper |
| R5 | Setup in 10 minutes | 9.0 minutes (estimate) | Met on paper (estimate) |
| R6 | No load over 25 kg | Heaviest load 23.7 kg | Met on paper |
| R7 | Head change under 2 minutes without tools | One screw-pin shackle, about 1 minute | Met on paper (estimate) |
| R8 | Grab lifts 10 L per cycle | 10.8 L at 70 % fill; 9.7 L after the 10 % drip | **At risk** (estimate) |
| R9 | Sample at depth within 0.2 m | Counter reads 0.1 m; tube centre known | Met on paper |
| R10 | DomeReach reaches the digester floor | Hinge 2.6 m, tool 3.3 m below the rim | Met on paper (depth taken as 2.5 m) |
| R11 | Corrosion resistance | Galvanized steel, 6082 aluminium, A4 fasteners and rope | **Not verifiable on paper**; TRL 4 coupon test |
| R12 | Value-engineering target | Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 2,838 (USD 2,162 under the target) | Under the target |
| R13 | Every head passes a 560 mm opening | Largest diagonal 525 mm | Met on paper |
| R14 | Stable with the rope 10 degrees off vertical | Tips at 25 degrees at the safe working load | Met on paper |

The same requirements are numbered PR-001 to PR-014 in HTS-PRS-001 (R1 is PR-001, and so on). Four requirements were added at the kit 1.9.1 upgrade and are checked in section 10a.

## 10a. Requirements added at the kit 1.9.1 upgrade

**PR-015, guard the opening.** The model carries six rim guard panels (BOM line 15, 2.4 kg each), six drop pins (line 16) and four cones with 10 m of barrier chain (line 22); the guard inner face stands 672 mm from the centre, so it clears a 1.2 m opening. Met by design; traffic rules for the work zone are to assess (HTS-REG-001).

**PR-016, made locally.** Every made part in the model is a named stock size (SHS, RHS, plate, bar or sheet) with drilled holes, cut edges and welds as beads, and the BOM marks each line make or buy. Met by design.

**PR-017, winch effort.** The low-gear crank force is 31 N, and lifting 150 kg at 1.01 m/min needs about 25 W at the rope, 33 W of hand input at 75 % efficiency, against the 75 W screening value for sustained hand cranking (STM S4).

**PR-018, not for lifting people.** The labels (BOM line 24) and the guide-only retrieval head carry this requirement; no calculation applies.

## 11. Option B, the straddle-frame davit (HTS-OPT-001)

Option B is a base frame of four 80 x 80 x 5 rails straddling the opening, a bolted 100 x 100 x 5 mast behind it and an 80 x 80 x 4 boom with a tip sheave, with the same winch on the mast and the same heads. The detailed model is in `cad/src/model.py` (`components("B")`); the script `docs/04-calcs/sizing.py` (`option_b()`) reads its geometry. The numbers below are first-order checks at the same design case as option A (2,759 N), screened and not designed in detail.

*Table 6. Option B checks at the design case.*

| Check | Result | Limit | Comment |
| --- | --- | --- | --- |
| Mast bending, moment 3,104 N m (arm 1,125 mm) | 57 MPa | 248 MPa (0.9 of yield) | Large margin |
| Boom bending at the root plate, moment 2,711 N m (arm 983 mm) | 95 MPa | 248 MPa | Margin 2.6 |
| Boom root bolts, four M16 A4-70 | 15.1 kN per upper bolt | 42.4 kN (0.6 of proof) | Margin 2.8 |
| Mast spigot joint, two M16 bolts on a 200 mm pitch | 15.5 kN per bolt, 49 MPa shear, 97 MPa bearing | 270 MPa shear, 275 MPa bearing | Large margin |
| Mast base, four M16 | 6.2 kN tension per rear bolt | 42.4 kN | Large margin |
| Rear cross rail, 80 x 80 x 5, as a beam between the side rails | 151 MPa | 248 MPa | The reason for the 80 mm section; the 60 x 60 x 4 rail first tried would be at about 340 MPa |
| Tip angle at the safe working load | 46 degrees sideways, 48 toward the mast, 58 toward the front | 10 degrees (PR-014) | Stable; the load line is inside the frame |
| Winch crank force, low gear, with the two extra sheaves | 33 N | | Comparable to option A |
| Mass with the five heads | 348 kg, of which 240 kg is frame, mast, boom and winch | | Option A: 195 kg including bags, cones and chains |
| Heaviest single piece | 26.2 kg (a side rail) | 25 kg (PR-006) | **Not met**; a 80 x 80 x 4 rail would weigh about 22 kg |
| Cost estimate | USD 3,910 | USD 5,000 | Estimate only: 219 kg of fabricated steel at the rate of option A's plate work (USD 10 per kg), plus the bought lines of option A |

The check that matters for option B is the bending path: the load acts 1,125 mm in front of the mast axis, so the base plate bolts and the rear cross rail carry the moment, not the mast tube. Not checked for option B: the front cross rail in compression, the side rails under the rear rail's uplift, the rolled-corner section properties (about 5 % weaker than the sharp-corner values used) and the rope's axial load in the mast; the margins in Table 6 are 1.6 to 3 or more and cover the 5 %. Option B is stable, but it is bulky: its frame is 1.8 m wide and 2.3 m long, so it needs a clear, level area of about that size at the opening, and its pieces are heavier. Its setup time is not estimated in this note; its model has 233 fastener parts against 127 for option A.

## 10. Limits of this note

- The buckling check treats each leg as one pin-ended column of the weaker section. The real telescoped leg is stiffer; the check is conservative.
- Winch performance, drum capacity and rope breaking load are catalogue figures to confirm when the parts are bought. The drum in the model has a 60 mm core (D/d about 10 for the 6 mm rope), which a real winch may improve on.
- The rope runs 110 mm outside leg A's axis, so it puts a bending moment of about 300 N m on the leg at the winch; it is not yet added to the buckling check (an open item from the independent review).
- The tip angle is a first-order figure; the winch on leg A moves the centre of mass and costs about a degree.
- Ground bearing is not checked: on soft ground the feet need boards (listed in the build plan's safety stops).
- Fatigue, wear of the sheave bearing and corrosion are TRL 4 questions.
