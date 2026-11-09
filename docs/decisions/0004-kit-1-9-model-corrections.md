---
doc_id: HTS-DDR-004
title: "HatchSide kit 1.9 detailed model, corrections"
project: HatchSide
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-11-05'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-11-05'
  author: Amish Chadha
  change: First record, at the kit 1.9.1 upgrade; dimension changes proposed for Amish to confirm
---

# 0004: Kit 1.9 detailed model, corrections and dimension changes

- **Date:** 2026-11-05
- **Status:** proposed, awaiting Amish to confirm. The changes are already in `cad/src/model.py` and `bom/bom.csv` because the D3 check cannot pass without them; none changes the pitch, the working principle or a price.

## Context

Kit 1.9 requires every option modelled with real stock, every fastener, welds as beads and edge breaks, with no overlapping parts (`python .kit/cad_check.py --export`, 5 mm3 tolerance). The kit 1.7 model of option A used massing shapes for several parts, so building it as a real assembly exposed places where parts overlapped or did not fit. Each is corrected below; the previous design values are kept wherever the check allowed.

## Decision

*Table 1. Corrections made when the model was rebuilt to D3.*

| # | Part | Before | Now | Why |
| --- | --- | --- | --- | --- |
| K1 | Chain shackles | Two screw-pin shackles per chain (BOM line 8) | One 8 mm screw-pin shackle per foot lug, three in all, each joining the ends of two chains; cost unchanged | A shackle cannot join two chains at one lug and clear the lug; the chains meet at the lug |
| K2 | Chain lug and foot plate | Lug 100 x 45 mm, hole 140 mm outboard; foot plate 140 x 280 mm | Lug 44 x 45 mm with the hole at its inner end, still 140 mm outboard; foot plate 140 x 360 mm | The shackle bow must pass the plate end, and the lug must stand on the foot plate; the chain still clears the clevis plates |
| K3 | Head interface | Swivel and shackle packed tight | Shackle depth 36 mm; the interface is 14.2 mm longer | The shackle body clears the swivel eye and the tab with room for the pin |
| K4 | Winch bracket nylon strips | Strips as plain blocks | 2 mm nylon strips drilled for the clamp and winch bolts | The bolts passed through solid nylon |
| K5 | Cleat | Placed on the leg | On the inner face of leg B, two M6 through bolts at 40 mm | The cleat and its bolts met the leg wall |
| K6 | Hinge bolts | M16 x 100 | M16 x 110 (BOM line 6) | Length for the sleeve, two nylon washers and the nut |
| K7 | Grab pins | Pins placed beside the grab | Hinge, ear and head pins through their holes | The pins were off the part in the old model |
| K8 | Rake | Bails through the top plate | Bails clipped at the plate; drag eye weld legs corrected | Overlap |
| K9 | DomeReach | Pivot across the arm, tiller through the pole | Pivot axis along the swing, ears each side, a split pin, tiller in two halves outside the collar, fork and roller axle with bearing blocks | Overlaps and a missing roller axle; the reach in HTS-CAL-001 section 7 is unchanged |
| K10 | Carry bags | Overlapping solids | Respaced, modelled as 3 mm empty canvas shells | Overlap; the heads are modelled separately |
| K11 | Rim guard splash board | Not riveted | Riveted with 4 mm pop rivets at the stiles | Fasteners must be modelled |

Dimension changes to review: K2 (foot plate 80 mm longer, about 0.7 kg each, cost unchanged because galvanizing is priced at a minimum lot) and K3 (interface 14.2 mm longer). All other changes are fastener or placement corrections.

## Consequences

- BOM text for lines 1, 6 and 8 changes; no price changes (`budget_usd` stays 5,000).
- HTS-CAL-001 is recomputed from the corrected model: masses 153.0 kg for the whole kit, heaviest load 23.7 kg, tip angle 25.0 degrees; no verdict changes.
- `docs/decisions/0002-design-for-construction.md` is a released record of kit 1.7 values and is not edited; this record supersedes its C6 chain lug dimensions.
