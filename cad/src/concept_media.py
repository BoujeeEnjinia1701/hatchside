"""HatchSide concept media from the TRL 3 constructable model (HTS-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process.
Geometry comes from cad/src/model.py; flow values come from HTS-CAL-001 (docs/04-calcs/sizing.py)
and are estimates. The pictures use the pieces of .kit/concept.py render_all, one at a time.

Axes as model.py: the opening is centred on the Z axis, leg A (the winch leg) points to the front
(-Y). The tripod stands over a 560 mm street manhole inside its rim guard with the grab hanging on
the rope; the sampler, rake, retrieval head and DomeReach head stand on the ground beside it. The
cutaway removes the front half and shows the grab lowered 1.2 m down the manhole shaft.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src"), str(ROOT / "docs/04-calcs")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as m  # noqa: E402

PROJECT, TITLE, DWG, DATE = "HatchSide", "No-entry tripod and tool heads concept", "HTS-DWG-010", "2026-10-03"
MD = ROOT / "media"
GROUND = "#D6D3CD"


def parts(heads=True, hook_z=None):
    return [Part(c.name, c.shape, c.color, c.bom, c.explode) for c in m.components(heads=heads, hook_z=hook_z)]


def ground(depth=0.0, shaft=False):
    """Street surface with a 560 mm manhole and its frame; with shaft=True the shaft walls and silt."""
    from build123d import Compound
    slab = m.box(-2400, 2400, -2300, 1700, -120, 0) - m.rod((0, 0, -200), (0, 0, 10), 280)
    frame = m.rod((0, 0, -40), (0, 0, 0), 360) - m.rod((0, 0, -50), (0, 0, 10), 280)
    out = [Part("Street and manhole frame (context)", Compound(children=[slab, frame]), GROUND, None)]
    if shaft:
        wall = m.rod((0, 0, -3000), (0, 0, -120), 400) - m.rod((0, 0, -3010), (0, 0, -110), 280)
        silt = m.rod((0, 0, -3000), (0, 0, -2600), 280)
        out += [Part("Manhole shaft (context)", wall, "#BDB8AF", None), Part("Silt (context)", silt, "#7C6A4F", None)]
    return out


def hero():
    ps = K.with_scale_figure(parts()) + ground()
    return K._render(ps, MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale")


def flat(ps):
    """Flatten nested compounds to their solids so the half-space cut is clean."""
    from build123d import Compound
    return [Part(p.name, Compound(children=list(p.shape.solids())), p.color, p.bom, p.explode) for p in ps]


def cutaway():
    ps = flat([p for p in parts(heads=False, hook_z=-1600)] + ground(shaft=True))
    return K._render(K.cutaway_parts(ps), MD / "cutaway.png", azim=-90, elev=14, title=f"{PROJECT}: cutaway",
                     note="Front half removed; grab lowered 1.6 m down a 560 mm manhole; seen from the front, 14 deg elevation")


BOM_SHORT = {1: "Feet and rubber pads (3)", 2: "Lower legs (3)", 3: "Upper legs (3)", 4: "Tripod head and mast",
             5: "Head sheave and axle", 6: "Hinge and foot bolts", 7: "Leg adjust pins", 8: "Leg-spread chains",
             9: "Winch bracket and bolts", 10: "Hand winch", 11: "Wire rope", 12: "Line length counter",
             13: "Head interface", 14: "Snatch block and cleat", 15: "Rim guard panels (6)", 16: "Rim guard drop pins",
             17: "Grab head"}


def exploded():
    ps = [Part(BOM_SHORT.get(p.bom, p.name), p.shape, p.color, p.bom, p.explode) for p in parts(heads=False)]
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True,
                     title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")


def web():
    return K.export_web_model(parts(), "media", title=f"{PROJECT}: {TITLE}")


def flow():
    import sizing
    cy = sizing.cycle()
    gross = round(cy["L_h"])
    drip = round(gross * cy["drip"])
    return K.flow_diagram(
        [("Silt in the chamber", "worked from the rim"), ("Grab loads (est.)", gross), ("Lifted to the rim (est.)", gross),
         ("Into the bin (est.)", gross - drip)],
        MD / "flow.png",
        f"{PROJECT}: silt removed per hour with the grab at {cy['depth']:.0f} m depth, about {cy['per_h']:.0f} cycles "
        f"(all values are estimates)", "L/h",
        [(2, "Drips back down the shaft (est.)", drip)])


def blueprint():
    import shutil
    import sizing
    from build123d import Compound
    from drawing import Sheet, project_views
    g = sizing.geometry()
    s = sizing.structure()
    _, loads, tripod = sizing.masses()
    gr = sizing.grab()
    _, tot = sizing.cost()
    ps = parts(heads=False)
    shown = K.with_scale_figure(ps)
    views = project_views(Compound(children=[p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in shown]), MD / "_views_fig")["iso"]
    sh = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P1", author="Amish Chadha", date=DATE, theme="blueprint",
               material="Massing model for concept communication",
               revisions=[("P1", "Concept sheet from the constructable model", DATE, "AC")])
    sh.add_ortho(views)
    sh.add_svg(views["iso"], 276, 37, 140, 113, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    sh.add_notes("Key figures", [
        f"Safe working load {sizing.A['swl_kg']:.0f} kg; hand winch with automatic brake",
        f"Sheave {g['zs'] / 1000:.2f} m up; feet on a {2 * m.PARAMS['R_FOOT'] / 1000:.1f} m circle",
        "Straddles openings 0.5 to 1.2 m; nobody enters",
        f"Five heads: grab ({gr['payload']:.0f} L, est.), sampler, rake,",
        "retrieval head, DomeReach for biogas digesters",
        f"Tripod with winch about {tripod:.0f} kg; no load over 25 kg",
        f"Leg buckling margin {s['sf_buckle']:.1f} at proof load",
        f"Parts about USD {tot:,.0f}; target USD 5,000",
    ], x=276, y=168, width=140)
    sh.save(MD / "concept-blueprint")
    shutil.rmtree(MD / "_views", ignore_errors=True)
    shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


if __name__ == "__main__":
    fns = {"hero": hero, "cutaway": cutaway, "exploded": exploded, "flow": flow, "web": web, "blueprint": blueprint}
    for w in sys.argv[1:] or list(fns):
        print(w, "->", fns[w]())
