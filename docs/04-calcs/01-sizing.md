---
doc_id: HTS-CAL-001
title: HatchSide sizing and first-principles checks
project: HatchSide
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First calculation note at TRL 3, from the constructable model (HTS-DDR-002)
---

# HatchSide sizing and first-principles checks

The constructable HatchSide meets every requirement that can be checked on paper. At the design case (150 kg safe working load, times 1.5 for proof, times 1.25 for jerk) the most loaded leg carries 3.85 kN against an Euler buckling load of 21.2 kN, the rope has a safety factor of 14.3 at the safe working load, the tripod tips only when the rope is about 25 degrees off vertical, no packed load exceeds 23.7 kg, and every head except DomeReach passes a 560 mm manhole opening as it hangs (DomeReach passes with its arm folded). The estimated parts cost is USD 2,838 against the USD 5,000 value-engineering target. Corrosion resistance (R11) cannot be shown on paper and is left to a TRL 4 coupon test.

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
| Euler buckling, whole leg taken as the weaker 50 x 3 mm section over 2,585 mm | 21.2 kN | 3,850 N | 5.5 |
| Axial stress in the 50 x 3 mm tube | 6.8 MPa | 250 MPa | Large |
| Hinge bolt bearing on the 4 mm upper leg walls | 30.1 MPa | About 250 MPa | Large; the steel crush sleeve stops the walls closing |
| Foot bolt bearing on the 3 mm lower leg walls | 40.1 MPa | About 250 MPa | Large |
| M16 bolt, double shear on the thread root | 13.3 MPa | About 260 MPa | Large |
| Head lug bearing (8 mm S275) | 15.0 MPa | About 275 MPa | Large |
| Vertical force at the feet | 3,246 N (A), 920 N (B and C) | | |
| Horizontal thrust at the feet | 2,070 N (A), 586 N (B and C) | | |
| Leg-spread chain tension | 1,195 N | About 5 kN working limit for 6 mm grade 30 chain (to confirm on purchase) | About 4 |
| M12 stop bolt, single shear | 33.8 MPa | About 260 MPa | Large |
| Stop bolt bearing on the 4 mm leg wall | 28.7 MPa | About 250 MPa | Large |
| Rope safety factor at the safe working load | 14.3 | 5 or more for a material hoist | Met |
| Rope safety factor at proof load | 9.5 | | Met |

Buckling governs the legs, and even then the margin is 5.5 with the whole leg taken as the weaker section. The stresses at the bolts and lugs are low because the joints were sized for handling, stiffness and wear rather than strength. The chain working limit is a typical catalogue figure and is listed in the design decisions register to confirm when the chain is bought.

## 4. Winch effort and rope speed

With a 40 mm effective drum radius, a 250 mm crank and 75 % efficiency, lifting 150 kg in low gear (10:1) needs a crank force of about 31 N, and lifting a 50 kg loaded grab in high gear (4:1) about 26 N. At 40 rpm the rope moves 2.51 m/min in high gear and 1.01 m/min in low gear. Both forces are comfortable for one person. The winch is a material winch with an automatic load brake, so the load holds when the crank is released.

## 5. Masses and packed loads (R6)

Masses come from the model solids and the material densities, plus the stated mass of bought parts (winch 9 kg, rope 2.3 kg, chains 6.7 kg, working line 2.1 kg and others).

*Table 3. Packed loads.*

| Load | Contents | Mass |
| --- | --- | --- |
| 1 | Head, mast, sheave, snatch block, hinge bolts, head interface | 16.8 kg |
| 2 | Upper legs (3) with adjust pins | 11.1 kg |
| 3 | Lower legs (3) with feet, pads and foot bolts | 20.3 kg |
| 4 | Winch, bracket, rope, line counter, cleat, working line | 18.6 kg |
| 5 | Rim guard panels (6), drop pins and leg-spread chains | 23.4 kg |
| 6 | Grab head | 23.7 kg |
| 7 | Sampler head | 11.4 kg |
| 8 | Rake head and retrieval head | 18.6 kg |
| 9 | DomeReach head (two pole sections, arm, roller) | 7.2 kg |

The tripod with winch and rope is about 71.4 kg and the whole kit about 151 kg. The heaviest load, the grab, is 23.7 kg, under the 25 kg limit of R6. In use the legs stay bolted to the head (loads 1 and 2 travel together on a cart) and the crew stands the tripod as one piece.

## 6. Stability (R14)

The tripod tips over the nearest edge of the foot triangle when the moment of a sideways rope pull about that edge exceeds the restoring moment of the rope load and the tripod's own weight. With the sheave 2,413 mm high, the edge 750 mm from the centre and a 71.4 kg tripod, the largest rope angle from vertical before tipping is 24.6 degrees at the safe working load and 22.3 degrees at proof load. The requirement is to stay stable with the rope 10 degrees off vertical, so the margin is more than double. Crews keep the rope within 10 degrees and never drag a load sideways with the winch.

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
| Retrieval head | 300 x 300 | 496 | 424 | Yes |
| DomeReach, arm folded, below the tiller | 86 x 258 | 3,910 | 272 | Yes |

## 8. Grab output and setup time (R5)

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
| R8 | Grab lifts 10 L per cycle | 10.8 L at 70 % fill | Met on paper (estimate) |
| R9 | Sample at depth within 0.2 m | Counter reads 0.1 m; tube centre known | Met on paper |
| R10 | DomeReach reaches the digester floor | Hinge 2.6 m, tool 3.3 m below the rim | Met on paper (depth taken as 2.5 m) |
| R11 | Corrosion resistance | Galvanized steel, 6082 aluminium, A4 fasteners and rope | **Not verifiable on paper**; TRL 4 coupon test |
| R12 | Value-engineering target | Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 2,838 (USD 2,162 under the target) | Under the target |
| R13 | Every head passes a 560 mm opening | Largest diagonal 525 mm | Met on paper |
| R14 | Stable with the rope 10 degrees off vertical | Tips at 25 degrees at the safe working load | Met on paper |

## 10. Limits of this note

- The buckling check treats each leg as one pin-ended column of the weaker section. The real telescoped leg is stiffer; the check is conservative.
- Winch performance, drum capacity and rope breaking load are catalogue figures to confirm when the parts are bought.
- Ground bearing is not checked: on soft ground the feet need boards (listed in the build plan's safety stops).
- Fatigue, wear of the sheave bearing and corrosion are TRL 4 questions.
