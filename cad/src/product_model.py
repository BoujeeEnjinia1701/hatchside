"""HatchSide product appearance model for photoreal renders (kit 1.9), TRL 3, constructable design (HTS-DDR-003).

Every part of the chosen design comes from cad/src/model.py components("A") as it is: feet and pads, telescoping legs,
tripod head with mast cheeks, sheave and axle, every hinge and foot bolt, adjust pins, leg-spread chains and shackles,
winch bracket and hand winch, line counter, wire rope, head interface, snatch block and cleat, rim guard, the five tool
heads, cones, barrier chain and labels. Only the scene is added as context parts: a street (concrete ground) with a
560 mm manhole, its cast-iron frame and a lifted cover, a workshop floor for the detail view, and a 1.75 m mannequin
standing on the ground outside the leg-spread chains. The carry bags stay out of the pictures.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: the opening is centred on the Z axis, ground level is z = 0, leg A (the winch leg) points to -Y.
Groups: "tripod" (tripod, winch, rope, rim guard, labels), "grab" (the grab hung on the rope), "heads" (sampler, rake,
retrieval head and DomeReach on the ground beside the tripod), "accessory" (cones and barrier chain), "lineup" (the
five heads side by side for the detail view) and "context" (street, manhole, person).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Compound, Cylinder, Location, Pos, Rot  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P  # noqa: E402

TITLE = "HatchSide: no-entry tripod, hand winch and tool heads for manholes, tanks and biogas digesters"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["tripod", "grab", "heads", "accessory", "context"], "explode": False, "el": 22, "az": -40,
     "args": ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=38,-65", "--lens=35"],
     "note": "Site render from the front right and above (about 22 deg elevation): the tripod over a 560 mm street "
             "manhole inside its six-panel rim guard, hand winch on leg A, grab hung on the rope; sampler, rake, "
             "retrieval head and DomeReach on the ground beside it, cones and barrier chain round the work zone; "
             "1.75 m person outside the leg-spread chains for scale"},
    {"name": "studio", "groups": ["tripod", "grab"], "explode": False, "el": 24, "az": -48,
     "note": "Studio render from the front right and above (about 24 deg elevation): tripod with its three leg "
             "hinges, head sheave and rope, hand winch and line counter on leg A, leg-spread chains, rim guard "
             "panels with drop pins, and the grab hung on the rope"},
    {"name": "exploded", "groups": ["tripod", "grab"], "explode": True, "el": 26, "az": -55,
     "note": "Exploded view from the front right and above (about 26 deg elevation): feet and pads, lower and upper "
             "legs, tripod head with mast and sheave, bolts and pins, chains, winch bracket, winch and line counter, "
             "rope and head interface, snatch block, rim guard and the grab head"},
    {"name": "detail", "groups": ["lineup"], "explode": False, "el": 18, "az": -35,
     "note": "Detail from the front right, slightly above (about 18 deg elevation): the four hung tool heads side by "
             "side, each with the same 10 mm lifting tab: grab, sampler, rake and retrieval head, with the DomeReach "
             "laid in front"},
]


def _group(p):
    b = p.get("bom")
    if b in (18, 19, 20, 21):
        return "heads"
    if b == 17:
        return "grab"
    if b == 22:
        return "accessory"
    return "tripod"


def lineup():
    """The tool heads side by side on a workshop floor, each at the origin of its own builder and set on the floor."""
    out = []
    specs = [("Grab", lambda A, L: model.build_grab(A, P, L)), ("Sampler", lambda A, L: model.build_sampler(A, P, L)),
             ("Rake", lambda A, L: model.build_rake(A, P, L)), ("Retrieval", lambda A, L: model.build_retrieval(A, P, L))]
    x = -900.0
    for nm, fn in specs:
        A = model.Asm({})
        fn(A, Location())
        bb = Compound([p["shape"] for p in A.parts]).bounding_box()
        d = Pos(x - bb.min.X, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z)
        for p in A.parts:
            q = dict(p)
            q["shape"] = d * p["shape"]
            q["name"] = f"{p['name']} (detail)"
            q["group"] = "lineup"
            q["explode"] = (0, 0, 0)
            out.append(q)
        x += bb.size.X + 180
    A = model.Asm({})
    model.build_domereach(A, P, Rot(0, -90, 0))
    bb = Compound([p["shape"] for p in A.parts]).bounding_box()
    d = Pos(-900 - bb.min.X, -650 - bb.max.Y, -bb.min.Z)
    for p in A.parts:
        q = dict(p)
        q["shape"] = d * p["shape"]
        q["name"] = f"{p['name']} (detail, laid down)"
        q["group"] = "lineup"
        q["explode"] = (0, 0, 0)
        out.append(q)
    out.append(dict(part("Workshop floor (detail)", Pos(1150, -350, -20) * cp.sheet(4300, 1500, 20, r_corner=1.0, edge=0.2), "concrete", "context"),
                    group="lineup"))
    return out


def scene():
    """Street, manhole and operator. Ground level is z = 0; every site part reaches below ground and is named (site)."""
    out = []
    frame = Pos(0, 0, -75) * (Cylinder(360, 150) - Cylinder(280, 170))
    out.append(part("Manhole frame (site)", frame, "mild_steel", "context"))
    void = Pos(0, 0, -1000) * Cylinder(280, 2004)
    out.append(part("Manhole shaft opening (site)", void, "matte_black", "context"))
    cover = Pos(1350, -800, -40) * Cylinder(300, 80)
    out.append(part("Manhole cover, lifted off (site)", cover, "mild_steel", "context"))
    from context_parts import mannequin
    person = Pos(650, -1250, 0) * Rot(0, 0, 180) * mannequin(1750, "stand")
    out.append(part("Person, 1.75 m mannequin (scale)", person, "skin", "context"))
    return out


def product_parts():
    out = []
    for p in model.components(model.CHOSEN):
        if p.get("bom") == 23:                      # carry bags stay out of the pictures
            continue
        q = dict(p)
        q["group"] = _group(p)
        out.append(q)
    out += lineup()
    for p in scene():
        q = dict(p)
        q["group"] = "context"
        out.append(q)
    return out


if __name__ == "__main__":
    ps = product_parts()
    for p in ps:
        if p["group"] in ("context", "lineup") and p["kind"] in ("context",):
            s = p["shape"]
            print(f"{p['name']:60s} {p['group']:10s} {p['material_name'] if 'material_name' in p else p.get('material')} valid={s.is_valid}")
    print(len(ps), "parts")
