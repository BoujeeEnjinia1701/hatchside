# Review note: HatchSide

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (HTS-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (HTS-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (HTS-REQ-001 v0.1): 12 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## Session 2026-10-03: TRL 2 (populate)

Run under kit 1.7.0 (`/to-trl3`), with Amish's pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Kit 1.7.0 installed in `.kit/` and `.claude/commands/`; `CLAUDE.md` replaced with `.kit/CLAUDE.md`.

### What was done

- `docs/01-problem.md` (HTS-PRB-001 v0.3): budget as a value-engineering target, co-design checklist, first candidate partners, safety section, answered questions.
- `docs/02-concept.md` (HTS-PRC-001 v0.3): how it works, components, design choices, first-order numbers, safety, patent design-arounds, shared blocks.
- `docs/03-requirements.md` (HTS-REQ-001 v0.3): 14 measurable requirements (R13 and R14 added).
- Concept media from `cad/src/concept_media.py`: `media/hero.png`, `media/concept-blueprint.png` and `.pdf`, `media/model.glb`, `media/viewer.html`, `media/cutaway.png`, `media/exploded.png`, `media/flow.png` (flow values marked as estimates).
- `bom/bom.csv`: 24 lines, every line priced.

### Results

The concept is one tripod, a hand winch and five heads worked from the rim; the TRL 2 numbers were superseded by the TRL 3 calculations below.

### Requirements not met

None at TRL 2 apart from R11 (corrosion), which cannot be shown on paper.

### Decisions made under the pre-approval

HTS-DDR-001, D1 to D12: 150 kg safe working load; retrieval head kept as a clip-on guide only; two-speed hand winch with automatic brake; 15 m of 6 mm stainless rope; square aluminium legs; galvanized steel and A4 stainless; DomeReach design depth 2.5 m, generic sealant, single hinge; R13 and R14 added; India first, with candidate partners to approach (not agreed); value-engineering target unchanged at USD 5,000.

### Safety concerns

Lifting over confined spaces with toxic or explosive air. Every document carries a safety section; the winch is a material winch and never lifts a person; the retrieval head never hauls.

## Session 2026-10-03: TRL 3 (advance, design for construction, build plan)

### What was done

- `docs/04-calcs/01-sizing.md` (HTS-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model with 31 interference checks and eight clearance checks; STEP and STL in `cad/step/` and `cad/stl/` (assembly, tripod and each head).
- `cad/drawings/HTS-DWG-001` (SVG, PDF, PNG), general arrangement, Rev P2.
- Making sketches `cad/drawings/HTS-DWG-101` to `HTS-DWG-112`; pictures in `docs/05-build-plan/` (overview, 10 joints, 14 steps) from `cad/src/build_plan_media.py`.
- `docs/05-build-plan.md` (HTS-BLD-001 v0.1) and `docs/06-design-decisions.md` (HTS-DEC-001 v0.1).
- `docs/decisions/0001-trl2-review-decisions.md` (HTS-DDR-001) and `docs/decisions/0002-design-for-construction.md` (HTS-DDR-002).
- Concept media regenerated from the constructable model.
- `cad/src/product_model.py` (appearance model, views hero, exploded and detail); scenes exported to `/home/claude/renders/hatchside` for the photoreal render on Amish's Mac. `media/render-hero.png` does not exist yet.
- `project.yaml`: trl 3, trl_target 3, `design_state: constructable`, evidence listed. README leads with `media/render-hero.png`, links the build plan and has a "Building the prototype" section.

### Results (HTS-CAL-001)

- Design case 150 kg x 1.5 x 1.25 = 2,759 N on the rope; winch leg 3.85 kN against 21.2 kN Euler buckling (margin 5.5).
- Rope safety factor 14.3 at the safe working load; sheave to rope ratio 20.8.
- Tips with the rope about 25 degrees off vertical at 150 kg (requirement 10 degrees).
- Crank force 31 N at 150 kg in low gear.
- Heaviest pack 23.7 kg (grab); tripod with winch and rope 71.4 kg; whole kit about 151 kg.
- Grab 10.8 L per cycle (estimate); about 166 L of silt an hour at 3 m.
- Value-engineering target: USD 5,000. Estimated cost of the constructable design: USD 2,838 (USD 2,162 under the target).

### Requirements not met

- R11, corrosion resistance: not verifiable on paper; TRL 4 coupon test.
- R5, R7 and R8 are met on estimates; R10 is met against an assumed 2.5 m digester depth.

### Decisions made under the pre-approval

- HTS-DDR-002, design for construction C1 to C12, all decided (Amish's pre-approval quoted above).
- Appearance model deviations from `model.py`: only labels (safe working load on leg A, "never lift a person" on the winch), a street slab, a manhole frame and lifted cover, a 1.75 m mannequin, and a detail lineup of the five heads; no change to any dimension. Decided under the pre-approval.
- Open decisions: none. Items to confirm when parts are bought are in HTS-DEC-001.

### Build plan findings: design changes made for construction (2026-10-03)

- Legs made telescoping square tubes with a ball-lock pin; M16 joints through steel crush sleeves with nylon isolation.
- Separate mast replaced by cheek plates on the head plate, with the sheave set so the rope runs parallel to leg A; rope keeper bar added.
- Winch bracket clamps round leg A under a through stop bolt that takes the rope pull.
- Feet given clevis plates, rubber pads and outboard chain lugs. Checking the joint pictures found that the leg-spread chains passed through the clevis plates; the foot plate was lengthened from 180 to 280 mm and the chain lug moved from 85 to 140 mm outboard, giving 12 mm clearance. The chains (now correctly 2.78 m, not 1.83 m) moved to the rim guard pack so no pack exceeds 25 kg. A feet/chains interference check was added to the model.
- Standard 10 mm tab defined for every head; grab given a closing yoke, tag rods and head beam with a working line through a snatch block; rim guard made of six pinned panels; retrieval head made a guide only; DomeReach made a single-hinge pole.

### Safety concerns

- Lifting over confined spaces: the frame is for tool heads only, never people; proof load to 225 kg with a competent person before any use over an opening (build plan S5).
- Load-path welds by a competent welder, inspected before galvanizing; no welding of galvanized steel.
- Retrieval: the HatchSide winch never hauls a person; certified rescue equipment and trained rescuers only. Relaxing this needs certification of the frame, winch and rope to a personnel standard.
- Gas: certified gas detector at the opening before and during work; no sparks or flames near sewers and digesters.
- Stability: keep the rope within 10 degrees of vertical; boards under the feet on soft ground.

### Recommended next step

Render `media/render-hero.png` (and the exploded and detail views) on Amish's Mac from the exported scenes, then run `python .kit/cards.py .` and the image check. At TRL 4 the first work is CalRig proof-load testing of the tripod, winch and rope, then the head trials of HTS-BLD-001 section 5.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.

## Session 2026-10-24: kit 1.9.1 upgrade

Run on 2026-11-05 under kit 1.9.1 (`/upgrade-1.8` then `/upgrade-1.9`), stage P3, TRL cap 3. Amish's standing instruction of 2026-10-23 applies to STEM fixes only; nothing below was decided by Amish.

### What was added

- Pipeline documents: `docs/01b-stem-check.md` (HTS-STM-001 v0.2) with `docs/04-calcs/stem_check.py` and `stem_results.csv`; `docs/02a-concept-options.md` (HTS-OPT-001); `docs/03a-user-requirements.md` (14 URs); `docs/03-requirements.md` (now HTS-PRS-001 v0.3: R1 to R14 migrated to PR-001 to PR-014 with a Was column, PR-015 to PR-018 added); `docs/03b-traceability.md` (generated by `python .kit/trace.py`, 0 gaps); `docs/07-regulatory.md`, `08-feasibility.md`, `09-risk.md` (hazard analysis and design FMEA), `10-market.md`, `11-plan.md`; users-and-needs and stakeholder tables in `docs/01-problem.md` (v0.4).
- Decisions: `docs/decisions/0003-concept-selection.md` (HTS-DDR-003), `0004-kit-1-9-model-corrections.md` (HTS-DDR-004); `docs/06-design-decisions.md` v0.2 with D13 to D17 open.
- Calculations: `docs/04-calcs/sizing.py` now reads the D3 model (masses by BOM line) and has `option_b()`; `01-sizing.md` v0.2 refreshed, with a 10 degree rope case, a winch stall case, corrected foot reactions and a section for option B.
- CAD: `cad/src/model.py` rebuilt to the kit 1.9 interface (`PARAMS`, `OPTIONS`, `PRINCIPLES`, `CHOSEN="A"`, `OPTION_VIEWS`, `ALLOWED_CONTACTS`, `components(option)`); option A and option B both at D3 with real stock, every fastener, welds as beads, edge breaks and BOM line numbers for A. Regenerated: `cad/drawings/HTS-DWG-001` and the build plan sketches HTS-DWG-101 to 112, `docs/05-build-plan/` pictures, `media/` concept media, STEP (option A split by `cad/src/slim_step.py`, option B one file) and STL at 0.2 mm (`cad/src/export_stl.py`); `cad/src/product_model.py` for the photoreal renders (not rendered here).
- `README.md` links line, "Concept options" and "STEM check" sections; `project.yaml` (`stage: P3`, `stem_check`, `concept_options`, `concept_chosen`, evidence).

### Results

- STEM check: 24 claims, 16 within known science, 8 plausible, none fails, so no fix to the working principle was needed. The independent review (headless `claude -p --model claude-opus-5-5`, shown only the STM, CAL, PRS and `sizing.py`) found no arithmetic error and moved S9 and S12 to Plausible, added the winch stall case (S24), widened S1 to the 10 degree rope case, and corrected the foot reactions and chain tension (339 N, not 1,195 N) in the calculation note. Details in HTS-STM-001, Independent review.
- Option scores (HTS-OPT-001): A 160, B 138 of 180; A leads by 14 %, outside the 10 % band. Recommendation: A, **Proposed, awaiting Amish**.
- CAD fidelity (`cad/fidelity.json`, D3, passes): option A 395 parts (204 made or bought, 127 fasteners, 64 welds), 197.7 kg including cones and empty bags (the kit itself 153.0 kg); option B 480 parts (180 made or bought, 233 fasteners, 67 welds), 347.9 kg. Bare share 0 for both.
- Cost: USD 2,838 against the USD 5,000 target (`budget_usd` unchanged); option B about USD 3,910 (estimate).

### Requirements not met

- PR-008 (grab, 10 L per cycle): at risk, 10.8 L gross but 9.7 L after the 10 % drip (STM S9).
- PR-011 (corrosion): not verifiable on paper; TRL 4 coupon test.
- Option B only: PR-006 (a 26.2 kg side rail) is not met and PR-005 (setup) is not estimated and likely over 10 minutes.

### Decisions awaiting Amish

D13 concept (A or B), D14 confirm the model corrections in HTS-DDR-004 (one shackle per chain lug, a 44 x 45 mm lug on a 140 x 360 mm foot plate, an interface 14.2 mm longer, M16 x 110 hinge bolts), D15 a second winch bracket position (idea from B), D16 grab volume for PR-008, D17 a load limiter against winch stall. All in `docs/06-design-decisions.md`. Co-design partners remain unapproached.

### Safety concerns

Unchanged: the kit is a material hoist, never for people, with certified gas detection and no entry. New in this session: misuse as rescue gear (RSK H1) is the top hazard; the winch at stall can load the rope to a factor of 4.8; hand-cranking and carry limits rest on screening values; the regulatory register has many "to assess" rows and nothing is certified.

### Kit and model notes

- `project_views` (`.kit/drawing.py`): a tilt of 0.006 degrees gave a silent empty front view; 0.03 degrees works but then the SVG exporter fails on a nearly closed ellipse arc (start equals end), so `cad/src/sheets.py` and `concept_media.py` carry a small workaround.
- `cad_check.py --export` writes a 68 MB single assembly STEP for option A, over the 45 MB repo limit; `cad/src/slim_step.py` splits it. The interference check takes about 8 minutes for option A.
- The kit material table has no PVC, so the traffic cones (steel density, about 40 kg for four cones and chain) and bags inflate option A's modelled mass; the kit mass of 153.0 kg excludes them.
- Hardware helpers: `hp.shackle(pin_d, inside, depth)` puts the legs at inside/2, so the clear gap is inside minus twice the leg radius.
- The options picture `media/options.png` is rendered by the coordinator and is not in this commit; `render.py --check` warns about it.

### Recommended next step

Amish decides D13 to D17 and approves the partner approach; no TRL 4 work starts until the cap is lifted.
