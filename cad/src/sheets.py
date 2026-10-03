"""HatchSide general arrangement drawing HTS-DWG-001 (Rev P2).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/HTS-DWG-001.svg, .pdf and .png from the parametric model (cad/src/model.py):
the tripod, mast, winch, rope and rim guard with the grab head hung on the rope. Figures in the
notes come from HTS-CAL-001 (python docs/04-calcs/sizing.py). The concept sheet in media/ is
HTS-DWG-010; the making sketches of the build plan are HTS-DWG-101 onward.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src"), str(ROOT / "docs/04-calcs")]
from build123d import Compound  # noqa: E402
from drawing import Sheet, project_views  # noqa: E402
import model as m  # noqa: E402
import sizing  # noqa: E402

P = m.PARAMS
g = sizing.geometry()
s = sizing.structure()
_, loads, tripod = sizing.masses()
tp = sizing.tipping(tripod)

asm = Compound(children=[c.shape for c in m.components(heads=False)])
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

sh = Sheet(project="HatchSide", title="No-entry tripod over a hatch: general arrangement", dwg_no="HTS-DWG-001",
           rev="P2", author="Amish Chadha", date="2026-10-03", concept=True, scale=None,
           material="Legs 6082-T6 Al tube; head, feet, bracket S275 galvanized; A4 fasteners. See bom/bom.csv",
           revisions=[("P1", "Preliminary GA from the TRL 3 model (HTS-CAL-001)", "2026-10-03", "AC"),
                      ("P2", "Design for construction (HTS-DDR-002)", "2026-10-03", "AC")])
sh.add_ortho(views, ["front", "top", "right"])
sh.add_svg(views["iso"], 276, 37, 140, 80, label="Isometric view", sublabel="Not to scale; grab on the rope")
sh.add_notes("Key dimensions (mm) and data", [
    f"Leg pins on {2 * P['R_HUB']:.0f} circle at {P['PIN_Z']:.0f}; feet on {2 * P['R_FOOT']:.0f} circle",
    f"Legs {g['Lp']:.0f} pin to pin, {g['theta']:.1f} deg from vertical; adjust +/- {P['ADJ_PITCH']:.0f}",
    f"Upper 60 x 60 x 4 x {P['UP'][2]:.0f}; lower 50 x 50 x 3 x {P['LO'][2]:.0f}; overlap {g['overlap']:.0f}",
    f"Sheave 150 OD at {g['zs']:.0f}; mast top {P['CHEEK_TOP']:.0f}; rope drops on the axis",
    f"Rope 6 mm 7x19 A4 x 15 m; winch drum {P['DRUM_S']:.0f} down leg A",
    f"Chains 6 mm, {g['foot_side']:.0f} between feet; chain lugs {P['CHAIN_LUG_R']:.0f} outboard",
    f"Rim guard: 6 panels {P['GUARD_H']:.0f} high on a hexagon, {2 * P['GUARD_R']:.0f} across flats",
    f"SWL {sizing.A['swl_kg']:.0f} kg; proof 1.5 x; leg buckling margin {s['sf_buckle']:.1f}",
    f"Tips with the rope {tp['ang']:.0f} deg off vertical at SWL; work within 10 deg",
    f"Tripod with winch about {tripod:.0f} kg; heaviest pack {max(loads.values()):.0f} kg",
    "Heads pass a 560 mm opening; standard tab 10 thick, 20 hole",
    "Material winch: never lift a person with it",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=133, width=140)
sh.save(ROOT / "cad/drawings/HTS-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/HTS-DWG-001.svg, .pdf, .png")
