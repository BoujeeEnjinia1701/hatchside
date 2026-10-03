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
