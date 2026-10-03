"""HatchSide product appearance model (build123d), TRL 3, constructable design (HTS-DDR-002).

Finished-product look for photoreal renders, built from the constructable model: every component of
cad/src/model.py components() is used as it is (feet and pads, telescoping legs, tripod head with
mast cheeks, sheave and axle, hinge and foot bolts, adjust pins, leg-spread chains, winch bracket,
hand winch, line counter, wire rope, head interface, snatch block, cleat, rim guard, and the five tool
heads). Only the look is added: a safe working load label on leg A, a warning label on the winch
(material winch, never lift a person), a street slab with a 560 mm manhole frame, and a 1.75 m
mannequin standing outside the leg-spread chains beside the winch for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: the opening is centred on the Z axis, leg A (the winch leg) points to -Y. Groups:
"tripod" (tripod, winch, rope, rim guard and labels), "grab" (the grab hung on the rope), "heads"
(sampler, rake, retrieval head and DomeReach on the ground beside the tripod, as in model.py),
"lineup" (the five heads side by side for the detail view) and "context" (street, manhole, person).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Compound, Pos, Rot  # noqa: E402
from model import PARAMS, box, components, domereach, head_comps, leg_frame, rod  # noqa: E402

TITLE = "HatchSide: no-entry tripod, hand winch and tool heads for manholes, tanks and biogas digesters"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["tripod", "grab", "heads", "context"], "explode": False, "el": 24, "az": -40,
     "note": "Product render from the front right and above (about 24 deg elevation): tripod over a 560 mm "
             "street manhole inside its six-panel rim guard, hand winch on leg A, grab hung on the rope; "
             "sampler, rake, retrieval head and DomeReach on the ground beside it; 1.75 m person outside "
             "the leg-spread chains for scale"},
    {"name": "exploded", "groups": ["tripod", "grab"], "explode": True, "el": 26, "az": -55,
     "note": "Exploded view from the front right and above (about 26 deg elevation): feet and pads, lower "
             "and upper legs, tripod head with mast and sheave, bolts and pins, chains, winch bracket, winch "
             "and line counter, rope and head interface, snatch block, rim guard and the grab head"},
    {"name": "detail", "groups": ["lineup"], "explode": False, "el": 18, "az": -35,
     "note": "Detail from the front right, slightly above (about 18 deg elevation): the five tool heads side "
             "by side, each with the same 10 mm lifting tab: grab, sampler, rake, retrieval head, and "
             "DomeReach laid in front"},
]

C_GALV = "#B8BEC6"       # hot-dip galvanized steel
C_GALV2 = "#9EA5AD"
C_ALU = "#C9CED4"        # mill-finish aluminium tube
C_ALU2 = "#B4BAC1"
C_STAIN = "#D5D9DE"      # stainless fasteners, pins and rope
C_ROPE = "#8F959C"
C_RUBBER = "#26292E"
C_WINCH = "#A32020"      # painted winch body
C_ACCENT = "#0F766E"
C_YELLOW = "#E8B517"     # safety-yellow guard frames and labels
C_HDPE = "#F2F2EE"
C_INK = "#1F2937"
C_COUNTER = "#1D4ED8"
C_CLEAR = "#CFE8F5"
C_STREET = "#8E8B86"
C_FRAME = "#5B5F63"
C_CLAY = "#B9B4AC"

# Each model component: (display name, colour, material, group)
LOOK = {
    "feet": ("Feet with clevis and chain lug (galvanized)", C_GALV2, "metal", "tripod"),
    "pads": ("Rubber foot pads", C_RUBBER, "rubber", "tripod"),
    "lower": ("Lower legs, 50 mm square aluminium tube", C_ALU, "metal", "tripod"),
    "lower_sleeves": ("Foot crush sleeves", C_GALV, "metal", "tripod"),
    "upper": ("Upper legs, 60 mm square aluminium tube", C_ALU2, "metal", "tripod"),
    "upper_sleeves": ("Hinge crush sleeves", C_GALV, "metal", "tripod"),
    "head": ("Tripod head with mast cheeks (galvanized)", C_GALV2, "metal", "tripod"),
    "sheave": ("Head sheave, 150 mm", C_ACCENT, "painted", "tripod"),
    "axle": ("Sheave axle bolt M20", C_STAIN, "metal", "tripod"),
    "hinge_bolts": ("Leg hinge bolts M16", C_STAIN, "metal", "tripod"),
    "foot_bolts": ("Foot bolts M16", C_STAIN, "metal", "tripod"),
    "adj_pins": ("Leg adjust pins, ball-lock", C_STAIN, "metal", "tripod"),
    "chains": ("Leg-spread chains (galvanized)", C_GALV, "metal", "tripod"),
    "bracket": ("Winch bracket and clamp plate (galvanized)", C_GALV2, "metal", "tripod"),
    "bracket_bolts": ("Clamp bolts M10 and stop bolt M12", C_STAIN, "metal", "tripod"),
    "winch": ("Hand winch, 450 kg, automatic brake", C_WINCH, "painted", "tripod"),
    "counter": ("Line length counter", C_COUNTER, "plastic", "tripod"),
    "rope": ("Wire rope, 6 mm stainless", C_ROPE, "metal", "tripod"),
    "interface": ("Head interface: swivel and shackle", C_STAIN, "metal", "tripod"),
    "snatch": ("Snatch block", C_ACCENT, "painted", "tripod"),
    "cleat": ("Working line cleat", C_FRAME, "metal", "tripod"),
    "guard": ("Rim guard panel frames (safety yellow)", C_YELLOW, "painted", "tripod"),
    "boards": ("Rim guard splash boards (HDPE)", C_HDPE, "plastic", "tripod"),
    "guard_pins": ("Rim guard drop pins", C_STAIN, "metal", "tripod"),
    "grab_shells": ("Grab shells (galvanized)", C_GALV2, "metal", "grab"),
    "grab_yoke": ("Grab closing yoke and hinge pin", C_ACCENT, "painted", "grab"),
    "grab_frame": ("Grab head beam, tag rods and pins", C_GALV, "metal", "grab"),
    "sampler": ("Sampler cage, ballast and caps", C_STAIN, "metal", "heads"),
    "sampler_tube": ("Sampler tube, clear PVC", C_CLEAR, "clear", "heads"),
    "rake": ("Rake head (galvanized)", C_GALV2, "metal", "heads"),
    "retrieval": ("Retrieval head (galvanized)", C_GALV2, "metal", "heads"),
    "connector": ("Auto-locking connector on sling", C_STAIN, "metal", "heads"),
    "dr_pole": ("DomeReach pole and tiller (aluminium)", C_ALU, "metal", "heads"),
    "dr_arm": ("DomeReach arm and clevis", C_ACCENT, "painted", "heads"),
    "dr_roller": ("DomeReach sealant roller", C_HDPE, "rubber", "heads"),
}

HEAD_LOOK = {"grab": (C_GALV2, "metal"), "sampler": (C_STAIN, "metal"), "rake": (C_GALV2, "metal"),
             "retrieval": (C_GALV2, "metal")}


def product_parts(P=PARAMS):
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ the constructable components as modelled
    for c in components(P, heads=True):
        if c.key not in LOOK:
            continue
        name, col, mat, grp = LOOK[c.key]
        add(name, c.shape, col, mat, c.bom, grp, c.explode)

    # ------------------------------------------------------------ labels: SWL on leg A, warning on the winch
    LA = leg_frame(P["LEG_AZ"][0], P)
    w = P["UP"][0] / 2
    swl = LA * box(-24, 24, w, w + 0.8, -720, -560)
    add("Safe working load label (150 kg) on leg A", swl, C_YELLOW, "paper", 24, "tripod", (0, -200, 120))
    ink = LA * (box(-16, 16, w + 0.8, w + 1.1, -600, -580) + box(-16, 8, w + 0.8, w + 1.1, -640, -625)
                + box(-16, 12, w + 0.8, w + 1.1, -690, -675))
    add("Safe working load label print", ink, C_INK, "paper", 24, "tripod", (0, -200, 120))
    sd, yb = P["DRUM_S"], w + P["BRACKET_T"]
    warn = LA * box(-59.8, -59.0, yb + 20, P["DRUM_Y"] + 50, -(sd + 60), -(sd - 40))
    add("Winch warning label (never lift a person)", warn, C_YELLOW, "paper", 24, "tripod", (0, -650, 650))

    # ------------------------------------------------------------ detail lineup: the five heads side by side
    hc = head_comps(P)
    x = -900.0
    for k in ("grab", "sampler", "rake", "retrieval"):
        s = hc[k]
        b = s.bounding_box()
        placed = Pos(x - b.min.X, 0, -b.min.Z) * s
        col, mat = HEAD_LOOK[k]
        add(f"{k.capitalize()} head (detail)", placed, col, mat, None, "lineup")
        x += b.size.X + 180
    d = domereach(P)
    dr = Compound(children=[d["pole"], d["tiller"], d["arm"], d["roller"]])
    lay = Rot(0, -90, 0) * dr
    b = lay.bounding_box()
    add("DomeReach head (detail, laid down)", Pos(-900 - b.min.X, -650 - b.max.Y, -b.min.Z) * lay, C_ACCENT,
        "painted", None, "lineup")
    floor = box(-1100, 3200, -1100, 400, -20, 0)
    add("Workshop floor (detail)", floor, "#D8D5CF", "paper", None, "lineup")

    # ------------------------------------------------------------ context: street, manhole frame and cover, person
    slab = box(-2400, 2400, -2600, 1900, -120, 0) - rod((0, 0, -200), (0, 0, 10), 280)
    add("Street (asphalt)", slab, C_STREET, "paper", None, "context")
    frame = rod((0, 0, -40), (0, 0, 0), 360) - rod((0, 0, -50), (0, 0, 10), 280)
    add("Manhole frame (cast iron)", frame, C_FRAME, "metal", None, "context")
    cover = Pos(1350, -800, 0) * rod((0, 0, 0), (0, 0, 30), 300)
    add("Manhole cover, lifted off (cast iron)", cover, C_FRAME, "metal", None, "context")
    from context_parts import mannequin
    person = Pos(900, -1500, 0) * Rot(0, 0, 180) * mannequin(1750, "stand")
    add("Person, 1.75 m mannequin (scale)", person, C_CLAY, "clay", None, "context")
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:52s} {p['group']:8s} {p['material']:8s} vol={s.volume / 1000:9.2f} cm3")
