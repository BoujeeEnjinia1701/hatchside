---
doc_id: HTS-BLD-001
title: HatchSide prototype build plan
project: HatchSide
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First build plan; design made constructable (HTS-DDR-002)
---

# HatchSide prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions and items to confirm are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; the sampler, rake, retrieval head and DomeReach stand beside the tripod.*

The prototype is one complete HatchSide kit: a three-legged aluminium tripod about 2.5 m tall with a steel head, a hand winch clamped to one leg, a stainless rope over a sheave at the top, a six-panel rim guard, and five tool heads that hang on the rope by the same steel tab. Figure 1 shows the 18 groups of components in the order you make or fit them. Twelve kinds of part are made in a small fabrication shop: the feet, lower and upper legs, the tripod head, the winch bracket, the rim guard panels, and the parts of the grab, sampler, rake, retrieval head and DomeReach. Everything else is bought: the sheave, winch, rope, line counter, swivel and shackles, snatch block, chain, pins and fasteners. The work is sawing and drilling aluminium tube, cutting, drilling, rolling and welding steel plate and sheet, and sending the steel parts out for hot-dip galvanizing. The parts cost about USD 2,838, from the bill of materials.

> **Safety:** HatchSide lifts loads over an open confined space. It is a material-handling frame for tool heads only: never lift or lower a person with it, and never enter the space. Nothing built to this plan is used over a real opening until the proof load of safety stop S5 has passed with a competent person present. Load-path welds (the tripod head, feet and grab) are made by a competent welder. Weld before galvanizing, never after: zinc fumes from welding galvanized steel are toxic. Cut aluminium and steel edges are sharp; deburr everything.

## 2. What changed to make it buildable

The concept showed what HatchSide does; its parts were shapes with no joints. Each change below keeps what the kit does, and all are recorded in decision record HTS-DDR-002.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Legs | Three adjustable legs | 60 mm square upper tube, 50 mm square lower tube sliding inside it, three adjust holes and a ball-lock pin (Figure 15) | Telescopes without turning; no machining |
| Leg joints | Not shown | M16 bolts through steel sleeves pressed between the tube walls, between steel lugs at the head and clevis plates at the feet (Figures 14 and 16) | Stops the bolts crushing the thin aluminium walls |
| Mast | A separate mast | Two steel cheek plates welded on the head plate, holding the sheave at the height where the rope runs parallel to leg A (Figure 17) | One welded part; the rope touches nothing |
| Winch mounting | Not shown | Clamp plates round leg A, under a stop bolt through the leg that takes the rope pull (Figure 18) | The load path does not rely on friction on aluminium |
| Feet and chains | A chain with no fixing | Steel feet with a clevis, a rubber pad and an outer lug for the chains (Figure 16) | A flat bearing and an anchor for each chain |
| Head interface | "One coupling" | A 10 mm steel tab with a 20 mm hole on every head, a screw-pin shackle and a swivel (Figure 19) | One tool-free coupling anyone can copy |
| Grab | A clamshell shape | Rolled shells on a hinge pin, tag rods to a head beam, a yoke closed by a working line through a snatch block (Figures 20 and 21) | Closes from the rim without power |
| Rim guard | A ring | Six flat panels pinned at the corners with drop pins (Figure 22) | Packs flat; no tools |
| Retrieval head | A head that lifts | A funnel guide with an auto-locking connector, steered by a pole; the haul is made with certified rescue equipment | The winch is not rated for people |
| DomeReach | A head shape | A two-section pole with one hinged arm worked by a pull line (Figure 23) | One hinge, no gripper; folds to pass a 560 mm opening |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. Leg A is the winch leg; leg B carries the cleat. "Outer face" of a leg is the face away from the centre of the tripod. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4. Every steel part is welded first, then hot-dip galvanized; drill and weld nothing after galvanizing.

### 3.1 Feet (make 3)

![Figure 2. Foot making sketch](../cad/drawings/HTS-DWG-101.png)

*Figure 2. Foot with clevis and chain lug (HTS-DWG-101).*

**What it is and what it is made from.** The steel foot each leg stands on. S275 steel plate 8 mm thick; a 10 mm rubber pad underneath.

**How to make it.**

1. Cut a base plate 140 x 280 mm, two clevis plates 100 long x 80 high, and a chain lug 100 x 45 mm, all from 8 mm plate.
2. Drill a 17 mm hole through both clevis plates together, 70 mm above the ground when they stand on the base (62 mm above the base's top face), centred along their length.
3. Drill a 14 mm hole in the chain lug, 20 mm from its outer end, so its centre ends up 140 mm beyond the clevis centre, toward the outer end of the foot.
4. Clamp a 52 mm spacer block between the clevis plates and stand them on the base, centred both ways, along the 280 mm direction. Weld both sides with 5 mm fillets.
5. Weld the chain lug on the centre line at the outer end of the base, overhanging the end by 20 mm, 5 mm fillets both sides.
6. Galvanize. Then bond a 140 x 280 x 10 mm rubber pad under the base with contact adhesive.

**How it fits the parts next to it.** The lower leg sits between the clevis plates on an M16 bolt through its steel sleeve, with 1 mm clearance each side (Figure 16). The leg-spread chains shackle to the lug; the lug is far enough out that each chain passes 12 mm clear of the clevis plates.

**Check before moving on.** A 50 mm square tube offcut slides between the clevis plates without forcing; a 16 mm rod passes straight through both holes.

### 3.2 Lower legs (make 3)

![Figure 3. Lower leg making sketch](../cad/drawings/HTS-DWG-102.png)

*Figure 3. Lower leg (HTS-DWG-102).*

**What it is and what it is made from.** The bottom half of each leg, sliding inside the upper leg. 50 x 50 x 3 mm 6082-T6 (or 6061-T6) aluminium square tube, 1,500 mm long.

**How to make it.**

1. Saw to 1,500 mm, square both ends, deburr inside and out.
2. Drill the foot pin hole, 17 mm, through two opposite walls, 30 mm from the bottom end.
3. Press a steel sleeve, 25 mm outside, 3.5 mm wall, 44 mm long, between the walls at that hole. It must sit flush with the inside of both walls.
4. Drill three 13 mm adjust holes through the same two walls: the centre hole 1,235 mm from the bottom end, one 75 mm above it and one 75 mm below it. Mark the centre hole "N" (normal length).
5. Leg B only: drill two 7 mm holes through the other two walls, on the centre line, 875 and 955 mm from the bottom end, for the cleat.

**How it fits the parts next to it.** It slides inside the upper leg with 1 mm clearance on each side, and the adjust pin passes through both tubes (Figure 15). Its bottom sits between the foot's clevis plates.

**Check before moving on.** It slides the full length of an upper leg offcut without binding; all three adjust holes line up with a 12 mm rod.

### 3.3 Upper legs (make 3)

![Figure 4. Upper leg making sketch](../cad/drawings/HTS-DWG-103.png)

*Figure 4. Upper leg (HTS-DWG-103).*

**What it is and what it is made from.** The top half of each leg, hinged to the tripod head. 60 x 60 x 4 mm 6082-T6 (or 6061-T6) aluminium square tube, 1,450 mm long.

**How to make it.**

1. Saw to 1,450 mm, square both ends, deburr inside the bottom end well so the lower leg slides in.
2. Drill the hinge hole, 17 mm, through two opposite walls, 30 mm from the top end. Press in a steel sleeve 25 mm outside, 3.5 mm wall, 52 mm long, flush with the inside of the walls.
3. Drill the adjust hole, 13 mm, through the same two walls, 40 mm from the bottom end.
4. Leg A only: drill a 13 mm stop bolt hole through the other two walls, 1,045 mm from the top end (1,015 mm below the hinge hole). Mark leg A with red tape.
5. Rivet the adjust pin's lanyard 100 mm above the adjust hole.

**How it fits the parts next to it.** The top end sits between a pair of lugs on the tripod head on an M16 bolt (Figure 14). The lower leg slides inside the bottom end.

**Check before moving on.** On leg A, a 12 mm rod passes square through the stop bolt hole; the hinge and adjust holes are parallel when sighted along the tube.

### 3.4 Tripod head with mast cheeks

![Figure 5. Tripod head making sketch](../cad/drawings/HTS-DWG-104.png)

*Figure 5. Tripod head with mast cheeks (HTS-DWG-104).*

**What it is and what it is made from.** The welded steel top of the tripod: a round plate that the legs hinge to, with two cheek plates above it that hold the sheave. S275 plate 10, 8 and 6 mm thick.

**How to make it.**

1. Cut the head plate, a 320 mm disc 10 mm thick. Drill a 40 mm hole in the centre for the rope and a 13 mm hole 95 mm from the centre, on the side away from leg A, for the snatch block eye bolt.
2. Cut six lugs from 8 mm plate, 90 wide x 105 high. Drill a 17 mm hinge hole in each, so its centre ends up 60 mm below the plate.
3. Mark three leg lines on the underside, 120 degrees apart, one of them (leg A) pointing the same way as the cheeks. Stand the lugs in pairs either side of each line, 62 mm apart inside, with the hinge holes 110 mm from the plate centre. Jig each pair with a 52 mm spacer and a 16 mm rod through both holes.
4. Cut two cheek plates from 6 mm plate, 180 x 195 mm. Drill a 21 mm axle hole in each, 63 mm toward leg A from the plate centre and 93 mm above the plate's top face.
5. Stand the cheeks on top of the plate, 34 mm apart inside, centred on the leg A line, with a 12 mm rope keeper bar across them 85 mm above the axle hole and an 8 mm gusset across their back edges, 120 mm high.
6. Weld everything with 6 mm fillets both sides. A competent welder makes these welds: they carry the load. Then galvanize.

**How it fits the parts next to it.** The upper legs hinge between the lug pairs (Figure 14); the sheave turns between the cheeks on an M20 bolt (Figure 17); the rope passes down through the centre hole.

**Check before moving on.** A 16 mm rod passes through each lug pair; a 20 mm rod passes through both cheeks square to them; welds are inspected for full fusion and no cracks before galvanizing.

### 3.5 Winch bracket and clamp plate

![Figure 6. Winch bracket making sketch](../cad/drawings/HTS-DWG-105.png)

*Figure 6. Winch bracket and clamp plate (HTS-DWG-105).*

**What it is and what it is made from.** Two steel plates that clamp round leg A and carry the winch. S275 plate 8 mm thick.

**How to make it.**

1. Cut two plates 120 x 270 mm.
2. Clamp them together and drill four 11 mm holes, 42 mm each side of the centre line and 22 mm from each end.
3. Drill the winch's four base holes in the front plate to suit the winch bought, measured from the winch itself.
4. Deburr and galvanize. Cut two nylon strips 2 mm thick to go between the plates and the leg.

**How it fits the parts next to it.** The plates sit on the front and back faces of leg A with the nylon strips between, held by four M10 x 90 stainless bolts with nyloc nuts, snug but not crushing the tube. Their top edges sit just under the M12 stop bolt through the leg, which takes the rope pull (Figure 18).

**Check before moving on.** The winch base sits flat on the front plate with all four bolts through.

### 3.6 Rim guard panels (make 6)

![Figure 7. Rim guard panel making sketch](../cad/drawings/HTS-DWG-106.png)

*Figure 7. Rim guard panel (HTS-DWG-106).*

**What it is and what it is made from.** One side of the hexagonal barrier round the opening. 25 x 25 x 2 mm aluminium square tube, with a 6 mm HDPE splash board.

**How to make it.**

1. Make a frame 746 long x 400 high from the tube, mitred and TIG welded, or butted and riveted with corner gussets.
2. Make four rings, 30 mm outside, 14 mm inside, 30 mm long, each on an 8 mm lug. Fix them 25 mm beyond each end post: at the right end 40 and 300 mm up, at the left end 75 and 335 mm up, so they interleave with the next panel's.
3. Rivet a 696 x 275 mm HDPE board to the inner face with 10 rivets, its bottom edge 30 mm up.
4. Paint the top rail in yellow and black bands.

**How it fits the parts next to it.** Six panels make a hexagon 1,380 mm across the flats. At each corner a 12 mm drop pin passes through four rings, two from each panel (Figure 22).

**Check before moving on.** Two panels pin together and swing through 120 degrees without the rings binding.

### 3.7 Grab shells (make 1 left and 1 right)

![Figure 8. Grab shell making sketch](../cad/drawings/HTS-DWG-107.png)

*Figure 8. Grab shell (HTS-DWG-107).*

**What it is and what it is made from.** The two buckets of the clamshell grab. 3 mm S275 sheet, with 5 mm end plates.

**How to make it.**

1. Cut each shell sheet 288 mm (developed) by 290 mm (left) or 302 mm (right). Roll to a 182 mm inside radius over a quarter turn.
2. Cut four end plates from 5 mm plate: a quarter disc of 185 mm radius with an ear 55 x 62 mm at the outer corner and a 35 mm radius boss at the hinge corner. Drill the hinge hole, 26 mm, at the corner, and the ear hole, 13 mm, 155 mm out and 35 mm up from it.
3. Left shell: fit the end plates inside the sheet ends, 290 mm apart. Right shell: fit them 302 mm apart, so they sit 1 mm outside the left shell's plates.
4. Jig both shells on a 25 mm bar through the hinge holes. Weld 4 mm fillets inside, with a 90 x 3 mm cover strip along the outer edge. Galvanize.

**How it fits the parts next to it.** The shells' end plates interleave on the 25 mm hinge pin, with the yoke bars outside them (Figure 20).

**Check before moving on.** On the 25 mm bar, the shells close edge to edge with no gap over 3 mm and open freely.

### 3.8 Grab head beam, tag rods and yoke

![Figure 9. Grab head beam, tag rods and yoke making sketch](../cad/drawings/HTS-DWG-108.png)

*Figure 9. Grab head beam, tag rods and yoke (HTS-DWG-108).*

**What it is and what it is made from.** The parts that hang the shells from the rope and close them. S275 plate and flat bar; 25 mm and 12 mm bright bar.

**How to make it.**

1. Head beam: 160 x 362 mm from 10 mm plate, with the standard tab welded on top (10 mm thick, 60 wide, a 20 mm hole 30 mm below its top edge) and a 30 mm hole for the closing line 40 mm off centre.
2. Weld four lugs 40 x 42 x 8 mm under the beam ends, each with a 13 mm hole.
3. Tag rods: four 30 x 6 mm flat bars with 13 mm holes 440 mm apart.
4. Yoke: two 50 x 6 mm bars 330 mm long with a 26 mm hole 30 mm from the bottom, joined at the top by a 50 x 10 mm crossbar with a 14 mm closing eye.
5. Hinge pin: 25 mm bar 340 mm long; pins: 12 mm bar, each drilled for an R-clip. Galvanize the welded parts.

**How it fits the parts next to it.** The tag rods pin to the shell ears at the bottom and inside the beam lugs at the top (Figure 21). The yoke rides on the hinge pin outside the shells. The shackle of the head interface goes through the tab.

**Check before moving on.** The tab hole takes the 11 mm shackle pin; the gauge plate of section 3.13 matches the tab.

### 3.9 Sampler head

![Figure 10. Sampler head making sketch](../cad/drawings/HTS-DWG-109.png)

*Figure 10. Sampler head (HTS-DWG-109).*

**What it is and what it is made from.** A clear tube in a ballasted cage, closed at depth. Clear PVC tube, stainless rod and plate, a steel ballast ring.

**How to make it.**

1. Cut the tube 75 mm outside, 3 mm wall, 600 mm long, ends square.
2. Cut top and bottom plates, 150 mm discs 6 mm thick. Top plate: the standard tab and a 32 mm hole. Bottom plate: a 100 mm hole.
3. Weld four 10 mm stainless rods, 694 mm long, on a 120 mm circle between the plates.
4. Bolt a steel ballast ring (150 mm outside, 90 mm inside, 40 mm thick) under the bottom plate.
5. Fit two clamp rings that hold the tube 54 mm below the top plate.
6. Fit the caps: 90 x 10 mm rubber discs on hinged arms, pulled shut by elastic cord through the tube, held open by a trip latch on the top plate.

**How it fits the parts next to it.** It hangs from the shackle by its tab; the working line goes to the trip latch. The sample centre is 420 mm below the shackle pin.

**Check before moving on.** With the caps latched open, a jerk on the trip line closes both caps; the tube holds water upside down.

### 3.10 Rake head

![Figure 11. Rake head making sketch](../cad/drawings/HTS-DWG-110.png)

*Figure 11. Rake head (HTS-DWG-110).*

**What it is and what it is made from.** A ballasted tine bar for breaking scum and loosening blockages. S275 flat bar and round bar.

**How to make it.**

1. Cut a tine bar 400 x 50 x 12 mm with a 16 mm hole in the middle.
2. Drill nine 12.5 mm holes through it at 45 mm pitch; push in nine 12 mm tines 250 mm long and plug weld both sides.
3. Weld a 380 x 40 x 40 mm ballast bar on top of the tine bar.
4. Weld two 40 x 8 mm bails from the ballast ends up to a 90 x 40 x 12 mm top plate carrying the standard tab.
5. Weld a 40 x 40 x 12 mm drag eye with a 16 mm hole on the front face. Galvanize.

**How it fits the parts next to it.** It hangs by its tab; the working line clips to the drag eye to draw the tines through scum.

**Check before moving on.** It hangs level from the tab hole within 5 degrees.

### 3.11 Retrieval head

![Figure 12. Retrieval head making sketch](../cad/drawings/HTS-DWG-111.png)

*Figure 12. Retrieval head (HTS-DWG-111).*

**What it is and what it is made from.** A funnel that guides an auto-locking connector onto the ring of a line already on a casualty. S275 plate and sheet; a bought EN 362 connector.

**How to make it.**

1. Cut a top disc 300 mm across, 6 mm thick, with a 100 mm hole and the standard tab.
2. Roll a funnel from 2.5 mm sheet, 300 mm across at the top to 120 mm at the throat, 250 mm deep. Seam weld and weld to the disc.
3. Weld a pole socket of 33.7 x 3.2 mm tube, 150 mm long, at the rim, with a gusset.
4. Galvanize. Hang a 300 mm steel sling from the disc with an EN 362 auto-locking steel connector below the throat.

**How it fits the parts next to it.** It hangs by its tab; a 2 m pole in the socket steers it.

**Check before moving on.** The connector gate opens when pressed onto a test ring and locks by itself.

> **Safety:** The retrieval head only clips a connector to a line already on a casualty. The haul is made with certified rescue equipment by trained rescuers, never with the HatchSide winch.

### 3.12 DomeReach head

![Figure 13. DomeReach making sketch](../cad/drawings/HTS-DWG-112.png)

*Figure 13. DomeReach head (HTS-DWG-112).*

**What it is and what it is made from.** A long pole with one hinged arm for work inside a household biogas digester. 6082-T6 aluminium tube; stainless pins; a bought paint roller and tools.

**How to make it.**

1. Cut two pole sections from 50 x 3 mm tube, 1,500 mm long. Join them with a 160 mm sleeve and a 10 mm pin.
2. Fit a top cap with the standard tab, and a 25 mm tiller 600 mm long on a clamp collar 250 mm below the top.
3. Fit a fairlead ring 500 mm below the top for the arm's pull line.
4. Fit a plug in the bottom end with a clevis of two 56 x 150 x 8 mm plates; drill a 12 mm pin hole 60 mm below the pole end.
5. Make the arm from 40 x 40 x 3 mm tube 700 mm long, pinned on the 12 mm pin, with a tool fork at its end for a 230 mm sealant roller, a scum paddle or a scoop basket.

**How it fits the parts next to it.** It hangs from the shackle by its top tab; the pull line runs from the arm tip through the fairlead to the operator (Figure 23). It has one hinge and no gripper.

**Check before moving on.** With the arm folded down along the pole, it passes a 560 mm ring.

### 3.13 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Head sheave and axle (line 5).** Wire rope sheave 150 mm outside, 125 mm at the rope, for 6 mm rope, sealed ball bearing on a 20 mm bore, rated at least 500 kg; M20 x 70 A4 bolt, nyloc nut and two 3 mm spacer washers.
- **Hinge and foot bolts (line 6).** Six M16 x 100 A4-70 bolts with nyloc nuts, washers and nylon isolating washers.
- **Adjust pins (line 7).** Three 12 mm stainless ball-lock pins, 70 mm grip, with lanyards.
- **Leg-spread chains (line 8).** Three 2.78 m lengths of 6 mm galvanized chain, grade 30 or better, each with two 8 mm screw-pin shackles.
- **Hand winch (line 10).** Two-speed hand winch with an automatic (Weston-type) load brake, rated at least 450 kg on the first layer, drum for at least 15 m of 6 mm rope, galvanized or zinc plated, four-bolt base, 250 mm crank. A material winch, marked as not for lifting people.
- **Wire rope (line 11).** 15 m of 6 mm 7x19 grade 316 stainless rope, minimum breaking load at least 21 kN, with a swaged thimble eye made by the supplier.
- **Line counter (line 12).** Mechanical rope length counter for 6 mm rope, 0.1 m resolution, resettable.
- **Head interface set (line 13).** A grade 316 eye-and-eye swivel rated at least 500 kg; two 3/8 in screw-pin bow shackles (11 mm pin, rated at least 1 t); a gauge plate of 10 mm steel with a 20 mm hole 30 mm below its top edge, for checking every new head's tab.
- **Snatch block, working line and cleat (line 14).** Snatch block with a 50 mm sheave for 10 mm rope, rated at least 500 kg, with an M12 A4 eye bolt; 30 m of 10 mm polyester line; a 150 mm aluminium cleat with two M6 A4 bolts.
- **Drop pins (line 16).** Six 12 mm stainless rods 400 mm long with 60 mm T-handles.
- **Work zone, bags and labels (lines 22 to 24).** Four 750 mm cones and 10 m of barrier chain; five carry bags; a safe working load plate (150 kg), a "never lift a person" label for the winch and a warning label for each head.

### 3.14 The joints in close-up

Each close-up is cut open where the inside matters. The words in each section above say which faces touch and what holds them.

![Figure 14. Joint 1](05-build-plan/joint-01.png)

*Figure 14. Leg hinge at the head: upper leg between a lug pair on an M16 bolt through a steel crush sleeve; 1 mm gap each side, filled by the nylon washers.*

![Figure 15. Joint 2](05-build-plan/joint-02.png)

*Figure 15. Telescoping leg: the 50 mm lower leg slides in the 60 mm upper leg with 1 mm each side; the 12 mm ball-lock pin passes through both.*

![Figure 16. Joint 3](05-build-plan/joint-03.png)

*Figure 16. Foot: lower leg between the clevis plates on an M16 bolt; chains shackled to the outer lug.*

![Figure 17. Joint 4](05-build-plan/joint-04.png)

*Figure 17. Sheave in the mast cheeks: M20 bolt through both cheeks; the keeper bar sits 10 mm above the rope.*

![Figure 18. Joint 5](05-build-plan/joint-05.png)

*Figure 18. Winch bracket on leg A: clamp plates either side of the leg; the stop bolt above them takes the rope pull.*

![Figure 19. Joint 6](05-build-plan/joint-06.png)

*Figure 19. Head interface: rope eye, swivel and screw-pin shackle through the 20 mm hole in a head's 10 mm tab.*

![Figure 20. Joint 7](05-build-plan/joint-07.png)

*Figure 20. Grab hinge: the shells' end plates interleave on the 25 mm pin; the yoke bars ride outside.*

![Figure 21. Joint 8](05-build-plan/joint-08.png)

*Figure 21. Tag rods to the head beam: each rod pinned inside a lug under the beam.*

![Figure 22. Joint 9](05-build-plan/joint-09.png)

*Figure 22. Rim guard corner: four rings from two panels interleave on one 12 mm drop pin.*

![Figure 23. Joint 10](05-build-plan/joint-10.png)

*Figure 23. DomeReach arm hinge and roller: one 12 mm pin in a clevis; the pull line from the arm tip sets the angle.*

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 4 and 11 to 14 are done on the bench; steps 5 to 10 at the test frame or opening.

### Step 1: fit the sheave in the mast

![Figure 24. Step 1](05-build-plan/step-01.png)

*Figure 24. Step 1.*

Head upside down on the bench, then upright. Slide the sheave between the cheeks with a 3 mm washer either side and push the M20 bolt through; nyloc nut snug, the sheave must spin freely. The rope keeper bar is already welded above it.

### Step 2: bolt the upper legs to the head

![Figure 25. Step 2](05-build-plan/step-02.png)

*Figure 25. Step 2.*

Each upper leg between its lug pair with nylon washers between the lugs and the tube; M16 bolt through the lugs and the leg's sleeve; nyloc nut snug so the leg swings without wobble. Leg A, with the red tape, goes on the lugs under the cheeks.

### Step 3: slide in the lower legs and pin them

![Figure 26. Step 3](05-build-plan/step-03.png)

*Figure 26. Step 3.*

Slide each lower leg into its upper leg and push the ball-lock pin through both at the hole marked "N". Check the balls have sprung out on the far side.

### Step 4: pin the feet to the legs

![Figure 27. Step 4](05-build-plan/step-04.png)

*Figure 27. Step 4.*

Each lower leg between its foot's clevis plates, nylon washers either side, M16 bolt through the sleeve, nyloc nut snug; pads down.

### Step 5: shackle the leg-spread chains

![Figure 28. Step 5](05-build-plan/step-05.png)

*Figure 28. Step 5.*

Stand the tripod over the opening (or the test frame) first. Shackle a chain between each pair of foot lugs and tighten the shackle pins by hand; the chains set the 3.0 m foot circle. Check the head is level within 2 degrees.

### Step 6: clamp the winch bracket to leg A

![Figure 29. Step 6](05-build-plan/step-06.png)

*Figure 29. Step 6.*

Push the M12 stop bolt through leg A and fit its nyloc nut. Place the front and back plates either side of the leg below it, nylon strips between, top edges touching the stop bolt; four M10 bolts snug.

### Step 7: bolt on the winch and line counter

![Figure 30. Step 7](05-build-plan/step-07.png)

*Figure 30. Step 7.*

Winch base flat on the front plate with four bolts, drum across the leg, crank to the right as you face leg A. Fit the line counter where the rope leaves the drum.

### Step 8: reeve the rope and fit the head interface

![Figure 31. Step 8](05-build-plan/step-08.png)

*Figure 31. Step 8.*

Anchor the plain end on the drum as the winch maker says and wind on all but about 3 m in tidy layers. Lead the rope through the counter, up the outside of leg A, over the sheave under the keeper bar and down through the head plate. Shackle the swivel to the thimble eye and a bow shackle to the swivel. **Hold point:** at least three full turns stay on the drum with the hook at the deepest working point.

### Step 9: hang the snatch block and fit the cleat

![Figure 32. Step 9](05-build-plan/step-09.png)

*Figure 32. Step 9.*

Screw the M12 eye bolt into the head plate's 13 mm hole with a nut on top, hang the snatch block on it, and bolt the cleat to leg B through its two 7 mm holes. Run the working line through the snatch block and make the tail off on the cleat.

### Step 10: pin the rim guard round the opening

![Figure 33. Step 10](05-build-plan/step-10.png)

*Figure 33. Step 10.*

Stand the six panels round the opening inside the legs, splash boards facing in. Leave one corner open while placing, then drop a pin through the four rings at each corner.

### Step 11: put the grab shells and yoke on the hinge pin

![Figure 34. Step 11](05-build-plan/step-11.png)

*Figure 34. Step 11.*

Left shell first, right shell over its end plates, yoke bars outside; washers and R-clips on the hinge pin.

### Step 12: fit the tag rods and the head beam

![Figure 35. Step 12](05-build-plan/step-12.png)

*Figure 35. Step 12.*

Tag rods on the ear pins, then the beam lugs over the rods' top ends; R-clips on every pin.

### Step 13: hang the grab and lead the closing line

![Figure 36. Step 13](05-build-plan/step-13.png)

*Figure 36. Step 13.*

Shackle the grab's tab to the bow shackle and screw the pin home by hand. Tie the working line to the yoke's closing eye; it runs up through the snatch block to the cleat. Pulling the line lifts the yoke and closes the shells.

### Step 14: assemble DomeReach

![Figure 37. Step 14](05-build-plan/step-14.png)

*Figure 37. Step 14.*

Join the pole sections at the sleeve and pin; arm on the clevis pin; roller on the fork; pull line from the arm tip through the fairlead.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of HTS-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Fit and movement | R2, R5 | Stand the tripod over a 0.5 m and a 1.2 m test opening at each leg setting | Feet clear both openings; legs lock at all three settings; head level within 2 degrees |
| Packed loads | R6 | Weigh each of the nine packs | No pack over 25 kg |
| Setup time | R5 | Two people from packed to the grab on the rope, timed | 10 minutes or less |
| Head change | R7 | Swap the grab for the sampler, timed, no tools | Under 2 minutes |
| Heads pass the opening | R13 | Pass each head, as it hangs, through a 560 mm ring | No head touches the ring; DomeReach folded |
| Winch and brake, light load | R3, R4 | Lift and lower a 50 kg test weight 1 m; release the crank part way | The brake holds the weight at every point; three turns stay on the drum at full payout |
| Proof load | R4 | Safety stop S5: 225 kg (1.5 times 150 kg) hung 300 mm off the ground for 5 minutes | No permanent set in legs, bolts or bracket; the brake holds; no rope damage |
| Stability | R14 | At 150 kg, pull the rope 10 degrees off vertical with a hand line, toward each foot edge in turn | No foot lifts |
| Grab | R8 | Ten cycles in a test chamber of wet sand | Average payload 10 L or more |
| Sampler | R9 | Take samples at three set depths in a layered tank | Sample centre within 0.2 m of the set depth |
| DomeReach | R10 | Work the arm through a 560 mm opening into a 2.5 m deep test pit | The roller touches the floor and walls; the tiller stays above the rim |
| No entry | R1 | Walk every head through its task at a mock manhole | Nobody's body crosses the plane of the rim |
| Corrosion | R11 | Coupons of each material in salt spray or sewage for 100 hours | No structural corrosion |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any part is galvanized.** All welding on that part is finished; the load-path welds of the tripod head, feet, bracket and grab are inspected by the welder and a second person for full fusion, size and no cracks. No welding or cutting is ever done on galvanized steel.
- **S2. Before the tripod is first stood up.** Every hinge and foot bolt has its nyloc nut; every adjust pin's balls are out on the far side; the chains are shackled with the pins hand-tight; the ground is level and firm (boards under the feet on soft ground).
- **S3. Before the rope takes any load.** The stop bolt is through leg A above the bracket; the rope is under the keeper bar; at least three turns are on the drum at the deepest point; the winch's "never lift a person" label is on.
- **S4. Before any load is lifted.** Everyone stands clear of the area under the load and outside the leg-spread chains except the winch operator, who stands beside leg A; hard hats and gloves on; nobody puts a hand between the rope and the sheave.
- **S5. Proof load, before any use over an opening.** A competent person is present. The tripod stands on level ground, not over an opening. A 225 kg test weight is lifted 300 mm and held for 5 minutes, then lowered and every joint inspected. Any bent part, slipped bracket, rope damage or brake creep stops the work until the cause is fixed and the proof load repeated.
- **S6. Before working over a real opening (outside this plan).** The air at the opening is tested with a certified gas detector and stays tested; the site is coned off with the rim guard pinned; no sparks or flames near sewers or digesters; the rope stays within 10 degrees of vertical; nobody leans over the guard. Nobody enters the space for any reason.
- **S7. Retrieval head.** The retrieval head is never used to lift a person with the HatchSide winch. Any rescue haul is made with certified rescue equipment by trained rescuers.

## 7. Tools, skills and workspace

**Tools.** Metal-cutting bandsaw or cold saw for tube and bar; bench drill with drills to 26 mm and a step drill; magnetic base drill for the head plate if the bench drill is small; MIG or stick welder for steel and a TIG welder (or rivet tool and gussets) for the guard frames; plate rolls for the grab shells and retrieval funnel (or a fabricator who rolls them); arbor press or vice for the leg sleeves; angle grinder with flap discs; files and deburring tool; scriber, square, protractor, steel rule and calipers; spirit level and digital angle finder; spanners and sockets for M10, M12, M16 and M20; crane scale or a calibrated 225 kg proof weight and a scale to 50 kg; stopwatch.

**Skills.** A competent welder for the load-path steel welds. Otherwise ordinary fabrication: marking out, sawing, drilling, rolling, riveting and bolting. The proof load (S5) is supervised by a person competent in lifting equipment inspection.

**Workspace.** A fabrication shop with a bench and a welding bay; access to a hot-dip galvanizer; a level concrete yard with room for a 3.5 m circle and overhead clearance of 3 m for standing the tripod and the proof load.

**Personal protective equipment.** Safety glasses, welding helmet and gloves, hearing protection when sawing and grinding, cut-resistant gloves for sheet, safety boots and hard hats once the tripod is up.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/HTS-DWG-101` to `HTS-DWG-112`.
- General arrangement: `cad/drawings/HTS-DWG-001.pdf`, Rev P2.
- Calculations: `docs/04-calcs/01-sizing.md` (HTS-CAL-001) and `docs/04-calcs/sizing.py`.
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0002-design-for-construction.md` (HTS-DDR-002), with HTS-DDR-001.
- Requirements: `docs/03-requirements.md` (HTS-REQ-001).
