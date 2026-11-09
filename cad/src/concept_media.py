"""HatchSide concept media from the TRL 3 constructable model (HTS-DDR-002).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint ...]
With no argument it draws everything; on a small machine run one picture per process.
Geometry comes from cad/src/model.py components("A") (kit 1.9, detail level D3); flow values come from HTS-CAL-001 (docs/04-calcs/sizing.py)
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
import build123d  # noqa: E402
from build123d import Compound, Cylinder, Pos, Rot  # noqa: E402

# The kit exports model.glb with build123d's default 0.001 mm chord tolerance, which gives a very large file for 400
# parts with threads and welds. A 0.2 mm chord and 0.3 rad angle are ample for the web viewer and keep it small.
_export_gltf = build123d.export_gltf


def _coarse_gltf(*a, **k):
    k["linear_deflection"] = 0.8
    k["angular_deflection"] = 0.6
    return _export_gltf(*a, **k)


build123d.export_gltf = _coarse_gltf

PROJECT, TITLE, DWG, DATE = "HatchSide", "No-entry tripod and tool heads concept", "HTS-DWG-010", "2026-10-24"
MD = ROOT / "media"
GROUND = "#D6D3CD"
HEAD_LINES = (18, 19, 20, 21)          # sampler, rake, retrieval and DomeReach heads, laid out round the tripod
SITE_LINES = (22, 23, 24)              # cones, bags and labels


def parts(heads=True, hook_z=None, site=True):
    """Parts of option A as concept Part tuples. heads=False leaves out the four heads lying round the tripod and
    the cones and bags (the grab stays on the rope); hook_z lowers the head interface and grab."""
    old = m.PARAMS["HOOK_Z"]
    if hook_z is not None:
        m.PARAMS["HOOK_Z"] = hook_z
    try:
        comps = m.components("A")
    finally:
        m.PARAMS["HOOK_Z"] = old
    out = []
    for p in comps:
        if not heads and p.get("bom") in HEAD_LINES + SITE_LINES:
            continue
        if not site and p.get("bom") in SITE_LINES:
            continue
        out.append(Part(p["name"], p["shape"], p["color"], p.get("bom") if p["kind"] in ("made", "bought") else None,
                        p.get("explode", (0, 0, 0))))
    return out


def grouped(ps):
    """One Part per BOM item, named as in bom/bom.csv, so the exploded legend reads "1 Foot with clevis and chain lug";
    fasteners and welds join the item they belong to."""
    import csv
    names = {int(r["item"].split()[0]): " ".join(r["item"].split()[1:]) for r in csv.DictReader(open(ROOT / "bom/bom.csv"))}
    out, by = [], {}
    for p in ps:
        if p.bom is None:
            out.append(p)
        else:
            by.setdefault(p.bom, []).append(p)
    for b, g in sorted(by.items()):
        out.append(Part(names.get(b, g[0].name), Compound([q.shape for q in g]), g[0].color, b, g[0].explode))
    return out


def ground(depth=0.0, shaft=False):
    """Street surface with a 560 mm manhole and its frame; with shaft=True the shaft walls and silt."""
    slab = Pos(0, -300, -60) * build123d.Box(4800, 4000, 120) - Pos(0, 0, -100) * Cylinder(280, 220)
    frame = Pos(0, 0, -20) * Cylinder(360, 40) - Pos(0, 0, -20) * Cylinder(280, 60)
    out = [Part("Street and manhole frame (context)", Compound(children=[slab, frame]), GROUND, None)]
    if shaft:
        wall = Pos(0, 0, -1560) * Cylinder(400, 2880) - Pos(0, 0, -1560) * Cylinder(280, 3000)
        silt = Pos(0, 0, -2800) * Cylinder(280, 400)
        out += [Part("Manhole shaft (context)", wall, "#BDB8AF", None), Part("Silt (context)", silt, "#7C6A4F", None)]
    return out


def hero():
    ps = K.with_scale_figure(parts()) + ground()
    return K._render(ps, MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale")


def flat(ps):
    """Flatten nested compounds to their solids so the half-space cut is clean."""
    return [Part(p.name, Compound(children=list(p.shape.solids())), p.color, p.bom, p.explode) for p in ps]


def cutaway():
    ps = flat(parts(heads=False, hook_z=-1600) + ground(shaft=True))
    return K._render(K.cutaway_parts(ps), MD / "cutaway.png", azim=-90, elev=14, title=f"{PROJECT}: cutaway",
                     note="Front half removed; grab lowered 1.6 m down a 560 mm manhole; seen from the front, 14 deg elevation")


def exploded():
    ps = grouped(parts(heads=False))
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")


def web():
    # the web model leaves out fasteners and weld beads (they are in the STEP files) to keep model.glb under about 20 MB
    return K.export_web_model([p for p in parts() if p.bom is not None], "media", title=f"{PROJECT}: {TITLE}")


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
    """Concept sheet projected from the made and bought parts of the tripod, winch, rim guard and grab (BOM lines 1 to 17):
    hidden-line projection of every bolt and weld bead takes hours and adds nothing at sheet scale. An open elliptical
    edge whose ends meet trips svgpathtools, so such an arc is drawn as a chord."""
    import shutil
    import build123d.exporters as bx
    import svgpathtools
    import sizing
    from drawing import Sheet, project_views
    orig = bx.ExportSVG._ellipse_segments

    def safe(self, edge, reverse):
        try:
            return orig(self, edge, reverse)
        except AssertionError:
            c = edge.geom_adaptor()
            return [svgpathtools.Line(self._path_point(c.Value(c.FirstParameter())), self._path_point(c.Value(c.LastParameter())))]
    bx.ExportSVG._ellipse_segments = safe
    g = sizing.geometry()
    s = sizing.structure()
    _, loads, tripod = sizing.masses()
    gr = sizing.grab()
    _, tot = sizing.cost()
    # the leg-spread chain links (hundreds of torus faces) are left out of the projection: they run out of memory and are a thin line at this scale
    ps = [p for p in parts(heads=False) if p.bom is not None and not p.name.startswith("Leg-spread chain")]
    shown = K.with_scale_figure(ps)
    tilt = Rot(0.03, 0.03, 0.03)     # 0.03 degrees off the axes: exactly axis-aligned faces can stall the hidden-line projection (0.006 gave an empty front view)
    views = project_views(Compound(children=[tilt * p.shape for p in ps]), MD / "_views")
    views["iso"] = project_views(Compound(children=[tilt * p.shape for p in shown]), MD / "_views_fig")["iso"]
    sh = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P2", author="Amish Chadha", date=DATE, theme="blueprint",
               material="Concept model; fasteners and welds not drawn at this scale",
               revisions=[("P1", "Concept sheet from the constructable model", "2026-10-03", "AC"),
                          ("P2", "Redrawn from the kit 1.9 detailed model", DATE, "AC")])
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
