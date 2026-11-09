"""HatchSide parametric model (build123d), kit 1.9 interface, TRL 3 (stage P3, detail level D3).

Run from the repo root:  python .kit/cad_check.py --export     (fidelity check, STEP per part and per assembly)
                         python cad/src/model.py                 (masses by BOM line and the clearance checks)

Two concept options are modelled to D3 (STANDARDS section 24; Amish, 2026-10-24: "Detail every option"):

  A  Tripod and hand winch (the current design, HTS-DDR-001 and HTS-DDR-002; carried to the drawing, BOM and build plan).
     Three telescoping square aluminium legs hinged under a steel head plate with a cheek-plate mast and a 150 mm
     sheave, a two-speed hand winch with an automatic load brake clamped to leg A, 15 m of 6 mm stainless rope, a
     standard 10 mm head tab with a shackle and swivel, a six-panel rim guard and five tool heads (grab, sampler,
     rake, retrieval guide, DomeReach). Every joint is bolted, pinned or welded as drawn.
  B  Straddle-frame davit (alternative, not carried to the drawing, BOM or build plan). A rectangular steel base frame
     is laid round the opening; a mast at its rear carries a bolted boom whose tip sheave stands over the opening
     centre, and the same winch, rope, tab and heads hang from it. The load is carried by bending of mast and boom
     and by the base frame bearing on the ground, instead of by axial thrust in three legs.

Axes (both options): the centre of the opening is the Z axis, Z is up and the ground is z = 0. Option A: leg A (the
winch leg) points to -Y (the front); legs B and C point to azimuths 30 and 150 degrees. Option B: the mast stands at
-Y and the boom reaches to +Y. The rope drops vertically on the Z axis. Units mm.
Sizing is in HTS-CAL-001 (docs/04-calcs/sizing.py), which reads PARAMS, geometry() and the helpers here.
CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Circle, Compound, Cone, Cylinder, Location, Plane, Pos, Rot, Sketch, Torus,  # noqa: E402
                       Polygon, Vector, extrude, revolve)
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import hs_parts as hp  # noqa: E402
from hs_parts import (bar, bolt_set, box, drill, nylon_washer, orient, plate, ring_weld, stock_between, tube_between,  # noqa: E402
                      weld_bead)

ROOT = HERE.parents[1]
TITLE = "HatchSide"

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # tripod geometry: leg hinge pins on a circle at the head, foot pins on a circle on the ground
    "PIN_Z": 2250.0, "R_HUB": 110.0, "R_FOOT": 1500.0, "FOOT_PIN_Z": 70.0,
    "LEG_AZ": (270.0, 30.0, 150.0),               # leg A (winch), B (cleat), C
    # legs: upper 60 x 60 x 4 and lower 50 x 50 x 3 square aluminium tube (6082-T6)
    "UP": (60.0, 4.0, 1450.0), "LO": (50.0, 3.0, 1500.0),
    "END_HOLE": 30.0,                              # hinge and foot holes, from the tube end
    "ADJ_FROM_END": 40.0, "ADJ_PITCH": 75.0, "ADJ_N": 3,   # adjust holes (lower leg: -1, 0, +1)
    "PIN_D": 16.0, "HOLE_D": 17.0, "ADJ_PIN_D": 12.0,
    "SLEEVE": (25.0, 3.5),                         # steel crush sleeve OD and wall in the leg ends
    # head plate and lugs (S275, hot-dip galvanized after welding)
    "HUB_R": 160.0, "HUB_T": 10.0, "HUB_Z0": 2310.0, "CABLE_HOLE": 40.0,
    "LUG_T": 8.0, "LUG_HALF": 45.0, "LUG_GAP": 1.0,
    # mast: twin cheek plates above the head plate; sheave 150 mm OD, 125 mm at the rope
    "CHEEK_T": 6.0, "CHEEK_X": 17.0, "CHEEK_Y": (-150.0, 30.0), "CHEEK_TOP": 2515.0,
    "SHEAVE": (75.0, 62.5, 28.0), "AXLE_D": 20.0, "ROPE_D": 6.0,
    "ROPE_OFFSET": 110.0,                          # rope line from leg A axis, on its outer side
    # winch (bought, 450 kg, automatic load brake) on a bracket on leg A, positions along the leg
    "BRACKET_S": (1022.0, 1292.0), "BRACKET_T": 8.0, "STOP_S": 1015.0, "STOP_D": 12.0,
    "CLAMP_BOLT_D": 10.0, "CLAMP_X": 42.0, "DRUM_S": 1157.0, "DRUM_Y": 150.0, "DRUM_R": 30.0,
    "DRUM_FL": 70.0, "ROPE_LAYER_R": 40.0,
    # feet (S275 plate, galvanized) and the leg-spread chains
    "FOOT_PLATE": (140.0, 360.0, 8.0), "PAD_T": 10.0, "CLEVIS_T": 8.0, "CHAIN_LUG_R": 140.0,
    "CHAIN_D": 6.0,
    # hook height of the head interface (shackle pin) in the assembly
    "HOOK_Z": 1100.0,
    # rim guard: six panels on a hexagon round the opening, 25 x 25 x 2 aluminium frame, HDPE board
    "GUARD_R": 690.0, "GUARD_H": 400.0, "GUARD_TUBE": (25.0, 2.0), "BOARD_T": 6.0,
    "GUARD_SETBACK": 25.0, "RING": (30.0, 14.0, 30.0),
    # standard head interface: 10 mm tab, 60 wide, 20 mm hole 30 mm below its top edge
    "TAB": (60.0, 10.0, 20.0, 30.0, 90.0),         # width, thickness, hole, hole below top, height
    # grab: shells R x length, sheet; tag rods; hinge pin
    "GRAB_R": 185.0, "GRAB_B": 290.0, "GRAB_SHEET": 3.0, "GRAB_PLATE": 5.0, "GRAB_ROD": 440.0,
    "GRAB_PIN": 25.0, "GRAB_HEAD_X": 60.0,
    # sampler: clear PVC tube OD x wall x length, cage radius, ballast ring
    "SAMP_TUBE": (75.0, 3.0, 600.0), "SAMP_CAGE_R": 60.0, "SAMP_PLATE_D": 150.0, "SAMP_BALLAST": (150.0, 90.0, 40.0),
    # rake: tine bar length, tines, tine length
    "RAKE_W": 400.0, "RAKE_TINES": 9, "RAKE_TINE": (12.0, 250.0),
    # retrieval head: top disc, funnel to throat, funnel depth
    "RET_D": 300.0, "RET_THROAT": 120.0, "RET_DEPTH": 250.0,
    # DomeReach: pole OD x wall, two sections, arm, arm angle from the pole (deg), roller
    "DR_POLE": (50.0, 3.0, 1500.0), "DR_ARM": (40.0, 3.0, 700.0), "DR_ARM_DEG": 45.0, "DR_ROLLER": (60.0, 230.0),
    "DR_TILLER": (25.0, 600.0, 250.0),             # tiller tube OD, length, below the top
}


def geometry(P=PARAMS):
    """Derived tripod geometry used by the model, the drawing and the calculations."""
    dr = P["R_FOOT"] - P["R_HUB"]
    dz = P["PIN_Z"] - P["FOOT_PIN_Z"]
    Lp = math.hypot(dr, dz)
    th = math.degrees(math.atan2(dr, dz))
    s, c = math.sin(math.radians(th)), math.cos(math.radians(th))
    rp = P["SHEAVE"][1]
    # sheave centre height so that the rope from the winch runs parallel to leg A at ROPE_OFFSET
    zs = P["PIN_Z"] + (P["ROPE_OFFSET"] - rp + (P["R_HUB"] - rp) * c) / s
    up_bot = P["UP"][2] - P["END_HOLE"]                        # upper leg bottom end, along the leg
    lo_top = Lp + P["END_HOLE"] - P["LO"][2]                   # lower leg top end, along the leg
    return dict(Lp=Lp, theta=th, sin=s, cos=c, zs=zs, up_bot=up_bot, lo_top=lo_top,
                overlap=up_bot - lo_top, adj_s=up_bot - P["ADJ_FROM_END"],
                height=P["CHEEK_TOP"], foot_side=math.sqrt(3) * P["R_FOOT"])


def radial(phi):
    """Location of the radial frame for azimuth phi: local +Y points out along phi, +Z up."""
    return Rot(0, 0, phi - 90)


def leg_frame(phi, P=PARAMS):
    """Leg-local frame: origin at the hinge pin, the leg runs down -Z, local +Y is the outer side."""
    g = geometry(P)
    return radial(phi) * Pos(0, P["R_HUB"], P["PIN_Z"]) * Rot(g["theta"], 0, 0)


def leg_point(phi, s, y=0.0, P=PARAMS):
    """Global point at distance s down leg phi from its hinge pin, offset y to the outer side."""
    v = leg_frame(phi, P) * Pos(0, y, -s)
    p = v.position
    return (p.X, p.Y, p.Z)




# ---- extra dimensions added by the kit 1.9 model (nothing in the kit 1.7 design changes; HTS-DDR-003)
PARAMS.update({
    "STRIP": 2.0,                     # nylon isolating strip between the winch bracket plates and leg A
    "NYLON": 1.0,                     # nylon isolating washer in the 1 mm gap at every aluminium joint
    "CLEAT_BOLT_S": 40.0,             # cleat bolts at +-40 mm along the leg (the two 7 mm holes of BOM line 2)
    "STOP_BOLT_L": 100.0,             # M12 x 100 stop bolt
})
CLEAT_S = 1700.0                                   # cleat position down leg B (mm)

OPTIONS = {"A": "Tripod and hand winch", "B": "Straddle-frame davit"}
PRINCIPLES = {
    "A": "A three-legged telescoping aluminium tripod stands over the opening; a hand winch on one leg runs a "
         "stainless rope over a head sheave so any of five tool heads hangs on the axis and is worked from the rim.",
    "B": "A rectangular steel base frame lies round the opening; a mast at its rear carries a bolted boom whose tip "
         "sheave stands over the opening centre, so the load is carried in bending and by the frame on the ground.",
}
CHOSEN = "A"
OPTION_VIEWS = {"A": {"el": 24, "az": -48, "scale": "person", "ground_z": 0},
                "B": {"el": 24, "az": -48, "scale": "person", "ground_z": 0}}


# =====================================================================================================
# Part collector
# =====================================================================================================
class Asm:
    """Collects part() dicts. `bom` groups share an explode vector for the exploded view."""

    def __init__(self, explode):
        self.parts = []
        self.explode = explode

    def add(self, name, shape, material, kind="made", bom=None, group="shell", note=""):
        ex = self.explode.get(bom, (0, 0, 0))
        self.parts.append(part(name, shape, material, kind=kind, bom=bom, group=group, explode=ex, note=note))

    def many(self, plist, bom=None, group="shell"):
        """Add part() dicts made elsewhere (fasteners), giving them the group's explode vector."""
        ex = self.explode.get(bom, (0, 0, 0))
        for p in plist:
            p["explode"] = ex
            p["group"] = group
            self.parts.append(p)


def fasteners(d, grip, face, shank, bom=None, tag="", material="stainless", L=None, washers=True):
    return bolt_set(d, grip, face, shank, material=material, bom=bom, tag=tag, L=L, washers=washers)


def glob_part(name, shape, material, kind="made", bom=None):
    return part(name, shape, material, kind=kind, bom=bom)


EXPLODE_A = {1: (0, 0, -250), 2: (0, 0, -120), 3: (0, 0, 150), 4: (0, 0, 600), 5: (0, 0, 900), 6: (0, 0, 450),
             7: (0, 0, 0), 8: (0, 0, -550), 9: (0, -300, 300), 10: (0, -650, 650), 11: (0, 0, 0), 12: (0, -800, 800),
             13: (0, 0, 250), 14: (0, 300, 600), 15: (0, 0, 0), 16: (0, 0, 500), 17: (0, 0, -150)}

HEAD_SPOTS = {"sampler": (1800, -600, 0), "rake": (-1850, 450, 0), "retrieval": (-1800, -750, 0),
              "domereach": (0, -2000, 0)}
BAG_SPOT = (-2150, -1300)


def _geo(P):
    g = geometry(P)
    g["LF"] = {a: leg_frame(a, P) for a in P["LEG_AZ"]}
    return g


# ------------------------------------------------------------------------------------- tripod parts
def _upper_leg(P, g, stop):
    w, t, L = P["UP"]
    s = Pos(0, 0, P["END_HOLE"]) * Rot(180, 0, 0) * cp.shs(w, t, L)
    s = drill(s, (0, 0, 0), "x", P["HOLE_D"])
    s = drill(s, (0, 0, -g["adj_s"]), "x", P["ADJ_PIN_D"] + 1)
    if stop:
        s = drill(s, (0, 0, -P["STOP_S"]), "y", P["STOP_D"] + 1)
    return s


def _lower_leg(P, g, cleat):
    w, t, L = P["LO"]
    s = Pos(0, 0, -g["lo_top"]) * Rot(180, 0, 0) * cp.shs(w, t, L)
    s = drill(s, (0, 0, -g["Lp"]), "x", P["HOLE_D"])
    for k in range(P["ADJ_N"]):
        s = drill(s, (0, 0, -(g["adj_s"] + (k - (P["ADJ_N"] - 1) / 2) * P["ADJ_PITCH"])), "x", P["ADJ_PIN_D"] + 1)
    if cleat:
        for sgn in (-1, 1):
            s = drill(s, (0, 0, -(CLEAT_S + sgn * P["CLEAT_BOLT_S"])), "y", 7.0)
    return s


def _sleeve(inner_w, P):
    od, wall = P["SLEEVE"]
    return orient(cp.round_tube(od, wall, inner_w), "+x")        # along +X from 0 to inner_w


def _ball_lock_pin(P):
    """12 mm ball-lock quick-release pin along X through the origin: button head at -X, locking balls at +X, lanyard ring."""
    d = P["ADJ_PIN_D"]
    shaft = Pos(-35, 0, 0) * orient(cp.round_bar(d, 82, 0.8), "+x")             # x from -35 to +47
    head = Pos(-48, 0, 0) * orient(cp.round_bar(24, 13, 1.5), "+x")              # button handle
    tip = Pos(47, 0, 0) * orient(cp.round_bar(d - 1, 4, 0.8), "+x")
    ring = Pos(-44, 0, 22) * Rot(0, 90, 0) * Torus(8, 1.4)
    return Compound([shaft, head, tip, ring])


def build_tripod(A, P, g):
    az = P["LEG_AZ"]
    LF = g["LF"]
    # ---------------- legs (BOM 2, 3) with crush sleeves, hinge and foot bolts, adjust pins
    for i, a in enumerate(az):
        n = "ABC"[i]
        A.add(f"Upper leg {n}, 60 x 60 x 4 aluminium", LF[a] * _upper_leg(P, g, i == 0), "aluminium", bom=3)
        A.add(f"Lower leg {n}, 50 x 50 x 3 aluminium", LF[a] * _lower_leg(P, g, i == 1), "aluminium", bom=2)
        A.add(f"Hinge crush sleeve {n}", LF[a] * Pos(-(P["UP"][0] / 2 - P["UP"][1]), 0, 0) * _sleeve(2 * (P["UP"][0] / 2 - P["UP"][1]), P),
              "mild_steel", bom=3)
        A.add(f"Foot crush sleeve {n}", LF[a] * Pos(-(P["LO"][0] / 2 - P["LO"][1]), 0, -g["Lp"]) * _sleeve(2 * (P["LO"][0] / 2 - P["LO"][1]), P),
              "mild_steel", bom=2)
        A.add(f"Leg adjust pin {n}, 12 mm ball-lock", LF[a] * Pos(0, 0, -g["adj_s"]) * _ball_lock_pin(P), "stainless",
              kind="bought", bom=7)
        # nylon isolating washers at the hinge (between lug and upper leg) and at the foot (between clevis and lower leg)
        xl = P["UP"][0] / 2
        for sx in (-1, 1):
            A.add(f"Hinge nylon isolating washer {n}{'+' if sx > 0 else '-'}",
                  LF[a] * Pos(sx * (xl + 0.5), 0, 0) * orient(Pos(0, 0, -0.5) * nylon_washer(16, P["NYLON"]), "+x"), "hdpe_natural",
                  kind="fastener", bom=6)
            xf = P["LO"][0] / 2
            A.add(f"Foot nylon isolating washer {n}{'+' if sx > 0 else '-'}",
                  LF[a] * Pos(sx * (xf + 0.5), 0, -g["Lp"]) * orient(Pos(0, 0, -0.5) * nylon_washer(16, P["NYLON"]), "+x"), "hdpe_natural",
                  kind="fastener", bom=6)
        xh = P["UP"][0] / 2 + P["NYLON"] + P["LUG_T"]
        A.many([dict(p, shape=LF[a] * p["shape"]) for p in
                fasteners(16, 2 * xh, (-xh, 0, 0), "+x", bom=6, tag=f" (hinge {n})")], bom=6)
        xf = P["LO"][0] / 2 + P["NYLON"] + P["CLEVIS_T"]
        A.many([dict(p, shape=LF[a] * p["shape"]) for p in
                fasteners(16, 2 * xf, (-xf, 0, -g["Lp"]), "+x", bom=6, tag=f" (foot {n})")], bom=6)


def build_feet(A, P, g):
    px, py, pt = P["FOOT_PLATE"]
    R, zp = P["R_FOOT"], P["FOOT_PIN_Z"]
    z1 = P["PAD_T"] + pt
    xo = P["LO"][0] / 2 + P["NYLON"]
    for i, a in enumerate(P["LEG_AZ"]):
        n = "ABC"[i]
        RF = radial(a)
        A.add(f"Foot rubber pad {n}", RF * cp.break_edges(box(-px / 2, px / 2, R - py / 2, R + py / 2, 0, P["PAD_T"], 0), 2.0),
              "epdm", bom=1)
        # sheet() is built from z = 0 up: lift it to sit from PAD_T to PAD_T + pt
        base = RF * Pos(0, R, P["PAD_T"]) * cp.sheet(px, py, pt, holes=[(0, -90, 9), (0, 90, 9)], r_corner=8, edge=0.5)
        A.add(f"Foot plate {n}, 8 mm S275 galvanised", base, "galvanised", bom=1)
        for sx in (-1, 1):
            cl = plate("yz", 100, zp + 28 - z1, P["CLEVIS_T"], (sx * (xo + P["CLEVIS_T"] / 2), R, (z1 + zp + 28) / 2),
                       holes=[(0, zp - (z1 + zp + 28) / 2, P["HOLE_D"])], r_corner=12)
            A.add(f"Foot clevis plate {n}{'+' if sx > 0 else '-'}", RF * cl, "galvanised", bom=1)
        lug = plate("yz", 44, 45, 8, (0, R + 148, z1 + 22.5), holes=[(-8, 0, 14)], r_corner=8)
        lug = RF * Pos(0, 0, 0) * lug
        A.add(f"Chain lug {n}", lug, "galvanised", bom=1)
        # welds: clevis plates (both faces) and the chain lug (both faces) to the foot plate
        for sx in (-1, 1):
            xi = sx * xo
            xout = sx * (xo + P["CLEVIS_T"])
            A.add(f"Weld, clevis {n}{'+' if sx > 0 else '-'} inner", RF * weld_bead((xi, R - 50, z1), "+y", 100, "-x" if sx > 0 else "+x", "+z", 6),
                  "mild_steel", kind="weld", bom=1)
            A.add(f"Weld, clevis {n}{'+' if sx > 0 else '-'} outer", RF * weld_bead((xout, R - 50, z1), "+y", 100, "+x" if sx > 0 else "-x", "+z", 6),
                  "mild_steel", kind="weld", bom=1)
            A.add(f"Weld, chain lug {n}{'+' if sx > 0 else '-'}", RF * weld_bead((sx * 4, R + 126, z1), "+y", 44, "+x" if sx > 0 else "-x", "+z", 5),
                  "mild_steel", kind="weld", bom=1)


def build_head(A, P, g):
    z0, t = P["HUB_Z0"], P["HUB_T"]
    hub = Pos(0, 0, z0) * extrude(Sketch() + Circle(P["HUB_R"]) - Pos(0, 0) * Circle(P["CABLE_HOLE"] / 2) - Pos(0, 95) * Circle(6.5), t)
    hub = cp.break_edges(hub, 1.0)
    A.add("Tripod head plate, 10 mm S275 galvanised", hub, "galvanised", bom=4)
    xo = P["UP"][0] / 2 + P["NYLON"]
    for i, a in enumerate(P["LEG_AZ"]):
        n = "ABC"[i]
        RF = radial(a)
        zc = (P["PIN_Z"] - P["LUG_HALF"] + z0) / 2
        h = z0 - (P["PIN_Z"] - P["LUG_HALF"])
        for sx in (-1, 1):
            xc = sx * (xo + P["LUG_T"] / 2)
            lug = plate("yz", 2 * P["LUG_HALF"], h, P["LUG_T"], (xc, P["R_HUB"], zc),
                        holes=[(0, P["PIN_Z"] - zc, P["HOLE_D"])], r_corner=6)
            A.add(f"Hinge lug {n}{'+' if sx > 0 else '-'}", RF * lug, "galvanised", bom=4)
            xin = sx * xo
            xout = sx * (xo + P["LUG_T"])
            y0 = P["R_HUB"] - P["LUG_HALF"]
            A.add(f"Weld, lug {n}{'+' if sx > 0 else '-'} outer", RF * weld_bead((xout, y0, z0), "+y", 2 * P["LUG_HALF"], "+x" if sx > 0 else "-x", "-z", 6),
                  "mild_steel", kind="weld", bom=4)
            A.add(f"Weld, lug {n}{'+' if sx > 0 else '-'} inner", RF * weld_bead((xin, y0, z0), "+y", 2 * P["LUG_HALF"], "-x" if sx > 0 else "+x", "-z", 6),
                  "mild_steel", kind="weld", bom=4)
    # mast cheek plates, rope keeper bar, back gusset
    rp, rf = P["SHEAVE"][1], P["SHEAVE"][0]
    y0, y1 = P["CHEEK_Y"]
    top = P["CHEEK_TOP"]
    zc = (z0 + t + top) / 2
    for sx in (-1, 1):
        xc = sx * (P["CHEEK_X"] + P["CHEEK_T"] / 2)
        ch = plate("yz", y1 - y0, top - (z0 + t), P["CHEEK_T"], (xc, (y0 + y1) / 2, zc),
                   holes=[(-rp - (y0 + y1) / 2, g["zs"] - zc, P["AXLE_D"] + 1)], r_corner=10)
        A.add(f"Mast cheek plate {'+' if sx > 0 else '-'}", ch, "galvanised", bom=4)
        xin = sx * P["CHEEK_X"]
        xout = sx * (P["CHEEK_X"] + P["CHEEK_T"])
        A.add(f"Weld, cheek {'+' if sx > 0 else '-'} inner", weld_bead((xin, y0, z0 + t), "+y", y1 - y0, "-x" if sx > 0 else "+x", "+z", 5),
              "mild_steel", kind="weld", bom=4)
        A.add(f"Weld, cheek {'+' if sx > 0 else '-'} outer", weld_bead((xout, y0, z0 + t), "+y", y1 - y0, "+x" if sx > 0 else "-x", "+z", 5),
              "mild_steel", kind="weld", bom=4)
    keeper = Pos(-P["CHEEK_X"], -rp, g["zs"] + rf + 10) * orient(cp.round_bar(12, 2 * P["CHEEK_X"], 1.0), "+x")
    A.add("Rope keeper bar, 12 mm", keeper, "galvanised", bom=4)
    gus = box(-P["CHEEK_X"], P["CHEEK_X"], y1 - 8, y1, z0 + t, z0 + t + 120, 1.5)
    A.add("Mast back gusset, 8 mm", gus, "galvanised", bom=4)
    A.add("Weld, back gusset", weld_bead((-P["CHEEK_X"], y1, z0 + t), "+x", 2 * P["CHEEK_X"], "+y", "+z", 5), "mild_steel", kind="weld", bom=4)
    # sheave, axle bolt M20, spacer washers
    ys, zs = -rp, g["zs"]
    w = P["SHEAVE"][2]
    rc = rp - P["ROPE_D"] / 2
    prof = [(10.5, -w / 2), (rf, -w / 2), (rf, -w / 2 + 4), (rp, -w / 2 + 9), (rc, -3), (rc, 3), (rp, w / 2 - 9),
            (rf, w / 2 - 4), (rf, w / 2), (10.5, w / 2)]
    from build123d import Axis, Face, Polyline, Wire
    sh = revolve(Face(Wire(Polyline(*[(r, 0, z) for r, z in prof], close=True))), Axis.Z)
    sh = Pos(0, ys, zs) * Rot(0, 90, 0) * sh
    A.add("Head sheave, 150 mm, sealed bearing", sh, "stainless", kind="bought", bom=5)
    for sx in (-1, 1):
        sp = Pos(sx * (w / 2 + 1.5), ys, zs) * orient(Pos(0, 0, -1.5) * extrude(Sketch() + Circle(16) - Circle(P["AXLE_D"] / 2 + 0.3), 3), "+x")
        A.add(f"Sheave spacer washer {'+' if sx > 0 else '-'}", sp, "stainless", kind="fastener", bom=5)
    xe = P["CHEEK_X"] + P["CHEEK_T"]
    A.many(fasteners(20, 2 * xe + 2 * 0.0, (-xe, ys, zs), "+x", bom=5, tag=" (sheave axle)", L=std20(2 * xe)), bom=5)


def std20(grip):
    return hp.std_length(grip + 2 * 3 + 18 + 2 * 2.5 + 0)


def build_chains(A, P, g):
    for i in range(3):
        a, b = chain_point(P["LEG_AZ"][i], P), chain_point(P["LEG_AZ"][(i + 1) % 3], P)
        d = Vector(*b) - Vector(*a)
        u = d.normalized()
        a2, b2 = Vector(*a) + u * 40, Vector(*b) - u * 40
        links = hp.link_chain(tuple(a2), tuple(b2), P["CHAIN_D"], 18.0, 21.0)
        sol = list(links.solids())
        third = len(sol) // 3 + 1
        for k in range(3):
            seg = sol[k * third:(k + 1) * third]
            if seg:
                A.add(f"Leg-spread chain {i + 1}, 6 mm grade 30, section {k + 1}", Compound(seg), "galvanised", kind="bought", bom=8)

    for i in range(3):
        pt = chain_point(P["LEG_AZ"][i], P)
        nxt = Vector(*chain_point(P["LEG_AZ"][(i + 1) % 3], P)) - Vector(*pt)
        prv = Vector(*chain_point(P["LEG_AZ"][(i - 1) % 3], P)) - Vector(*pt)
        ph = math.radians(P["LEG_AZ"][i] - 90)
        tang = Vector(math.cos(ph), math.sin(ph), 0)
        mean = nxt.normalized() + prv.normalized()
        zdir = (mean - tang * mean.dot(tang)).normalized()
        body, pin = hp.shackle(8.0, 18.0, 14.0)
        loc = hp.frame(Vector(*pt), tang, zdir)
        A.add(f"Chain shackle {i + 1}, 8 mm body", loc * Compound([body]), "galvanised", kind="bought", bom=8)
        A.add(f"Chain shackle {i + 1}, screw pin", loc * pin, "stainless", kind="bought", bom=8)


def chain_point(phi, P=PARAMS):
    R = P["R_FOOT"] + P["CHAIN_LUG_R"]
    z = P["PAD_T"] + P["FOOT_PLATE"][2] + 22.5
    a = math.radians(phi)
    return (R * math.cos(a), R * math.sin(a), z)


# ------------------------------------------------------------------------------------- winch, rope, interface
def build_winch(A, P, g):
    az = P["LEG_AZ"]
    LA = g["LF"][az[0]]
    w, t, st = P["UP"][0] / 2, P["BRACKET_T"], P["STRIP"]
    s0, s1 = P["BRACKET_S"]
    sd, yd, rd = P["DRUM_S"], P["DRUM_Y"], P["DRUM_R"]
    zc = -(s0 + s1) / 2
    ch = P["CLAMP_X"]
    holes_c = [(sx * ch, -(s) - zc, 11.0) for sx in (-1, 1) for s in (s0 + 22, s1 - 22)]
    holes_w = [(sx * 40.0, -(sd + dz) - zc, 8.0) for sx in (-1, 1) for dz in (-70.0, 70.0)]
    yf = w + st + t / 2
    A.add("Winch bracket front plate, 8 mm S275 galvanised", LA * plate("xz", 120, s1 - s0, t, (0, yf, zc), holes=holes_c + holes_w, r_corner=8),
          "galvanised", bom=9)
    A.add("Winch bracket back plate, 8 mm S275 galvanised", LA * plate("xz", 120, s1 - s0, t, (0, -yf, zc), holes=holes_c, r_corner=8),
          "galvanised", bom=9)
    for sy, nm in ((1, "front"), (-1, "back")):
        A.add(f"Bracket isolating strip {nm}, nylon", LA * plate("xz", 120, s1 - s0, st, (0, sy * (w + st / 2), zc), holes=holes_c + (holes_w if sy > 0 else []), r_corner=8, edge=0.3),
              "hdpe_natural", kind="made", bom=9)
    yb = w + st + t
    for sx in (-1, 1):
        for s in (s0 + 22, s1 - 22):
            A.many([dict(p, shape=LA * p["shape"]) for p in
                    fasteners(10, 2 * yb, (sx * ch, -yb, -s), "+y", bom=9, tag=f" (clamp {'+' if sx > 0 else '-'}x, s {s:.0f})", L=90)], bom=9)
    A.many([dict(p, shape=LA * p["shape"]) for p in
            fasteners(12, 2 * yb, (0, -yb, -P["STOP_S"]), "+y", bom=9, tag=" (stop bolt)", L=100)], bom=9)
    winch_hardware(A, P, LA, yb, sd)


def winch_hardware(A, P, LA, yb, sd, bl=20):
    """The bought hand winch (base, side plates, drum, axle, gearbox, crank), its four base bolts and the line counter, in
    the frame LA whose local Y is outward from the mounting face at y = yb and whose local -Z runs along the mounting
    surface (the drum axis is at z = -sd)."""
    yd = P["DRUM_Y"]
    rd = P["DRUM_R"]
    # ---- winch body (bought): base, side plates, drum, axle, gearbox, crank shaft, arm, grip
    yw = yb
    base = plate("xz", 110, 190, 8, (0, yw + 4, -sd), holes=[(sx * 40.0, dz, 9.0) for sx in (-1, 1) for dz in (-70.0, 70.0)], r_corner=8)
    A.add("Hand winch base plate", LA * base, "zinc_plated", kind="bought", bom=10)
    ytop = yd + 72
    for sx in (-1, 1):
        sp = plate("yz", ytop - (yw + 8), 160, 4, (sx * 57, (ytop + yw + 8) / 2, -sd), holes=[(yd - (ytop + yw + 8) / 2, 0, 24.5)], r_corner=10)
        A.add(f"Hand winch side plate {'+' if sx > 0 else '-'}", LA * sp, "zinc_plated", kind="bought", bom=10)
    rc = revolve_profile([(12.25, -55), (70, -55), (70, -51), (rd, -51), (rd, 51), (70, 51), (70, 55), (12.25, 55)])
    A.add("Hand winch drum with flanges", LA * Pos(0, yd, -sd) * orient(rc, "+x"), "zinc_plated", kind="bought", bom=10)
    A.add("Hand winch drum axle", LA * Pos(-59, yd, -sd) * orient(cp.round_bar(24, 59 + 78, 1.0), "+x"), "mild_steel", kind="bought", bom=10)
    gb = cp.break_edges(Pos(59 + 9.5, (yw + 50 + yd + 60) / 2, -(sd + 10)) * Box(19, yd + 60 - (yw + 50), 120), 3.0)
    A.add("Hand winch gearbox and load brake housing", LA * gb, "painted_steel", kind="bought", bom=10)
    ysh, zsh = yw + 70, -(sd + 40)
    A.add("Hand winch crank shaft", LA * Pos(59, ysh, zsh) * orient(cp.round_bar(18, 41 + 35, 1.0), "+x"), "mild_steel", kind="bought", bom=10)
    arm = box(92, 102, ysh - 10, ysh + 10, -(sd + 290) , -(sd + 30), 2.0)
    arm = arm - Pos(97, ysh, zsh) * orient(Cylinder(9.0, 40), "+x")
    A.add("Hand winch crank arm", LA * arm, "painted_steel", kind="bought", bom=10)
    grip = Pos(102, ysh, -(sd + 280)) * orient(cp.round_tube(30, 8, 113), "+x")
    A.add("Hand winch crank grip", LA * grip, "rubber_belt", kind="bought", bom=10)
    # four base bolts into the tapped front plate
    for sx in (-1, 1):
        for dz in (-70.0, 70.0):
            A.many([dict(p, shape=LA * p["shape"]) for p in
                    hp.screw_in(8, bl, (sx * 40.0, yw + 8, -(sd + dz)), "-y", bom=10, tag=" (winch base)")], bom=10)
    # line length counter on its stand, bolted to the bracket front plate
    ry = P["ROPE_OFFSET"]
    cz = -(sd - 90)
    body = box(-22, 22, ry + 6, ry + 40, cz - 15, cz + 15, 2.0) + box(-22, 22, ry - 40, ry - 6, cz - 15, cz + 15, 2.0)
    A.add("Line length counter body", LA * Compound([body]), "matte_black", kind="bought", bom=12)
    stand = box(-22, 22, yw + 8, ry - 40, cz - 10, cz + 10, 2.0)
    A.add("Line counter stand", LA * stand, "zinc_plated", kind="bought", bom=12)
    face = box(-16, 16, ry + 40, ry + 42, cz - 9, cz + 9, 0.3)
    A.add("Line counter dial", LA * face, "glass", kind="bought", bom=12)


def revolve_profile(pts):
    from build123d import Axis, Face, Polyline, Wire
    return revolve(Face(Wire(Polyline(*[(r, 0, z) for r, z in pts], close=True))), Axis.Z)


def rope_points(P, g, hz):
    az = P["LEG_AZ"]
    rp = P["SHEAVE"][1]
    a = leg_point(az[0], P["DRUM_S"], P["ROPE_OFFSET"], P)
    c_y, c_z = -rp, g["zs"]
    t_y, t_z = c_y - rp * g["cos"], c_z + rp * g["sin"]
    a0 = math.atan2(t_z - c_z, t_y - c_y)
    wrap = [(0.0, c_y + rp * math.cos(a0 + (0 - a0) * k / 24), c_z + rp * math.sin(a0 + (0 - a0) * k / 24)) for k in range(25)]
    return [a] + wrap + [(0.0, 0.0, hz + IFACE_TOP)]


IFACE_TOP = 155.2       # rope end above the shackle pin, at the top of the thimble


def build_rope(A, P, g, hz):
    pts = rope_points(P, g, hz)
    A.add("Wire rope 6 mm 7x19 grade 316, run drum to head interface", cp.rope(pts, P["ROPE_D"]), "stainless", kind="bought", bom=11)
    LA = g["LF"][P["LEG_AZ"][0]]
    wound = revolve_profile([(rd_ := P["DRUM_R"], -50), (P["ROPE_LAYER_R"], -50), (P["ROPE_LAYER_R"], 50), (rd_, 50)])
    A.add("Wire rope wound on the drum (3 layers, envelope)", LA * Pos(0, P["DRUM_Y"], -P["DRUM_S"]) * orient(wound, "+x"), "stainless",
          kind="bought", bom=11)
    thimble = Pos(0, 0, hz + IFACE_TOP - 19) * Rot(90, 0, 0) * Torus(12, 4)
    A.add("Rope thimble", thimble, "stainless", kind="bought", bom=11)
    fer = Pos(0, 0, hz + IFACE_TOP + 4) * (Cylinder(7, 24) - Cylinder(P["ROPE_D"] / 2, 30))
    A.add("Swaged ferrule", fer, "stainless", kind="bought", bom=11)


def build_interface(A, P, hz, with_gauge=True):
    """Shackle with its pin through the tab hole, swivel with two eyes, gauge plate and the spare shackle."""
    body, pin = hp.shackle(11.0, 23.0, 36.0)
    A.add("Bow shackle 3/8 in, 11 mm screw pin: body", Pos(0, 0, hz) * body, "stainless", kind="bought", bom=13)
    A.add("Bow shackle 3/8 in: screw pin", Pos(0, 0, hz) * pin, "stainless", kind="bought", bom=13)
    lower = Pos(0, 0, hz + 47.2) * Rot(90, 0, 0) * Torus(10, 3.5)
    barrel = Pos(0, 0, hz + 86.2) * Cylinder(9, 58)
    upper = Pos(0, 0, hz + 124.2) * Rot(0, 90, 0) * Torus(10, 3.5)
    A.add("Eye-and-eye swivel, grade 316", Compound([lower, barrel, upper]), "stainless", kind="bought", bom=13)
    if with_gauge:
        gp = plate("xz", 60, 90, 10, (700, -2100, 5), holes=[(0, 15, 20.0)], r_corner=4)
        A.add("Head interface gauge plate, 10 mm, 20 mm hole", gp, "galvanised",
              bom=13)
        b2, p2 = hp.shackle(11.0, 23.0, 36.0)
        spare = Pos(1050, -2150, 12) * Rot(0, 90, 0) * Compound([b2, p2])
        A.add("Spare bow shackle 3/8 in", spare, "stainless", kind="bought", bom=13)


# ------------------------------------------------------------------------------------- snatch block, cleat, working line
def cleat_inner_point(P, g, s, y):
    return leg_point(P["LEG_AZ"][1], s, y, P)


def build_working_line(A, P, g, hz, z_eye):
    """Snatch block under the head plate, cleat on leg B, working line from the grab yoke eye over the block to the cleat."""
    z0, t = P["HUB_Z0"], P["HUB_T"]
    y = 95.0
    # eye bolt M12 through the head plate with washer and nut above; eye ring below
    shank = Pos(0, y, z0 - 8) * cp.round_bar(12, 8 + t + 14, 0.8)
    ring = Pos(0, y, z0 - 22) * Rot(0, 90, 0) * Torus(10, 3.5)
    collar = Pos(0, y, z0 - 8) * (Cylinder(16, 3) )
    A.add("Eye bolt M12 A4 (snatch block hanger)", Compound([shank, ring, Pos(0, 0, 0) * collar]), "stainless", kind="bought", bom=14)
    # nut and washer on top of the plate
    s_, k_, m_, d2_, h_, p_ = cp.ISO[12]
    A.many([cp.part("M12 washer (ISO 7089) eye bolt", Pos(0, y, z0 + t) * cp.washer(12), "stainless", kind="fastener", bom=14),
            cp.part("M12 hex nut (ISO 4032) eye bolt", Pos(0, y, z0 + t + h_) * cp.hex_nut(12), "stainless", kind="fastener", bom=14)], bom=14)
    zb = z0 - 30
    eye = Pos(0, y, zb) * Rot(90, 0, 0) * Torus(8, 3)
    stem = Pos(0, y, zb - 11) * cp.round_bar(10, 11, 0.5)
    cz = zb - 11
    sheave_z = cz - 55
    for sx in (-1, 1):
        cheek = plate("yz", 50, 90, 3, (sx * 9.5, y, cz - 40), holes=[(0, sheave_z - (cz - 40), 8.5)], r_corner=14)
        A.add(f"Snatch block cheek {'+' if sx > 0 else '-'}", cheek, "stainless", kind="bought", bom=14)
    A.add("Snatch block swivel eye and stem", Compound([eye, stem]), "stainless", kind="bought", bom=14)
    prof = [(5.5, -6), (25, -6), (25, -3), (21, -1.5), (21, 1.5), (25, 3), (25, 6), (5.5, 6)]
    sh = Pos(0, y, sheave_z) * Rot(0, 90, 0) * revolve_profile(prof)
    A.add("Snatch block sheave, 50 mm", sh, "aluminium", kind="bought", bom=14)
    A.add("Snatch block axle pin 8 mm", Pos(-12.5, y, sheave_z) * orient(cp.round_bar(8, 25, 0.5), "+x"), "stainless", kind="bought", bom=14)
    # cleat on the inner face of leg B (lower leg)
    LB = g["LF"][P["LEG_AZ"][1]]
    w = P["LO"][0] / 2
    sc = CLEAT_S
    base = plate("xz", 28, 150, 10, (0, -(w + 5), -sc), holes=[(0, sg * P["CLEAT_BOLT_S"], 7.0) for sg in (-1, 1)], r_corner=6)
    horns = [box(-9, 9, -(w + 10 + 18), -(w + 10), -(sc + sg * 62.5) - 12.5, -(sc + sg * 62.5) + 12.5, 3.0) for sg in (-1, 1)]
    A.add("Working line cleat, 150 mm aluminium", LB * Compound([base] + horns), "aluminium", kind="bought", bom=14)
    for sg in (-1, 1):
        A.many([dict(p, shape=LB * p["shape"]) for p in
                fasteners(6, 2 * w + 10, (0, -(w + 10), -(sc + sg * P["CLEAT_BOLT_S"])), "+y", bom=14,
                          tag=f" (cleat {'+' if sg > 0 else '-'})")], bom=14)
    # working line 10 mm polyester: grab yoke eye -> up the near side of the sheave -> over it -> down to the cleat horn
    ys = y
    rr = 26.0
    arc = [(0.0, ys + rr * math.cos(math.radians(a_)), sheave_z + rr * math.sin(math.radians(a_))) for a_ in range(180, -1, -15)]
    cl = leg_point(P["LEG_AZ"][1], sc + 62.5, -(w + 10 + 9))
    line = cp.rope([(0.0, 40.0, z_eye)] + arc + [cl], 10.0)
    A.add("Working line 10 mm polyester (grab closing line, drawn to the cleat)", line, "rope", kind="bought", bom=14)


# ------------------------------------------------------------------------------------- rim guard
def build_guard(A, P):
    R, H = P["GUARD_R"], P["GUARD_H"]
    a, tw = P["GUARD_TUBE"]
    half = R * math.tan(math.radians(30)) - P["GUARD_SETBACK"]
    xc = R * math.tan(math.radians(30))
    od, idd, h = P["RING"]
    y0, y1 = R - a / 2, R + a / 2
    gaz = [P["LEG_AZ"][0] + 60 * k for k in range(6)]
    rc = R / math.cos(math.radians(30))
    zr = (70.0, 170.0, 270.0)
    zc_b = (a + 5 + H - a - 70) / 2
    for k, phi in enumerate(gaz):
        n = k + 1
        RF = radial(phi)
        rail_len = 2 * (half - a)
        top = Pos(-(half - a), R, H - a / 2) * orient(cp.shs(a, tw, rail_len), "+x")
        bot = Pos(-(half - a), R, a / 2) * orient(cp.shs(a, tw, rail_len), "+x")
        sl = Pos(-half + a / 2, R, 0) * cp.shs(a, tw, H)
        sr = Pos(half - a / 2, R, 0) * cp.shs(a, tw, H)
        # rivet holes in the two stiles (inner face): three each
        for st in (sl, sr):
            pass
        for z in zr:
            sl = drill(sl, (-half + a / 2, R - a / 2, z), "y", 4.0, 60)
            sr = drill(sr, (half - a / 2, R - a / 2, z), "y", 4.0, 60)
        rings = []
        for x_end, zs in ((xc, (40.0, 300.0)), (-xc, (75.0, 335.0))):
            sx = 1 if x_end > 0 else -1
            for z in zs:
                ring = Pos(x_end, R, z) * (cp.round_tube(od, (od - idd) / 2, h))
                lug = box(min(sx * half, sx * (xc - od / 2 + 3)), max(sx * half, sx * (xc - od / 2 + 3)), R - 4, R + 4, z, z + h, 1.0)
                rings += [ring, lug]
        A.add(f"Rim guard panel {n} frame, 25 x 25 x 2 aluminium welded", RF * Compound([top, bot, sl, sr] + rings), "aluminium", bom=15)
        rv = [(sx * (half - a / 2), z - zc_b) for sx in (-1, 1) for z in zr]
        board = RF * plate("xz", 2 * half - 4, 275.0, P["BOARD_T"], (0, y0 - P["BOARD_T"] / 2, zc_b),
                           holes=[(u, v, 4.0) for u, v in rv], r_corner=4)
        A.add(f"Rim guard panel {n} splash board, 6 mm HDPE", board, "hdpe_natural", bom=15)
        for sx in (-1, 1):
            for z in zr:
                rivet = Pos(sx * (half - a / 2), y0 - P["BOARD_T"], z) * orient(
                    Pos(0, 0, -0.75) * Cylinder(4, 1.5) + Pos(0, 0, 4.0) * Cylinder(2, 8.0), "+y")
                A.add(f"Pop rivet 4 mm, panel {n}", RF * rivet, "aluminium", kind="fastener", bom=15)
        pin_phi = phi + 30
        px, py = rc * math.cos(math.radians(pin_phi)), rc * math.sin(math.radians(pin_phi))
        pin = Pos(px, py, 30) * (cp.round_bar(12, H + 6, 0.8))
        tee = Pos(px, py, H + 36) * Rot(0, 0, math.degrees(math.atan2(py, px)) + 90) * Rot(0, 90, 0) * Pos(0, 0, -30) * cp.round_bar(10, 60, 0.8)
        A.add(f"Rim guard drop pin {n}, 12 mm with T handle", Compound([pin, tee]), "stainless", bom=16)


# ------------------------------------------------------------------------------------- tool heads (local frame: tab hole at the origin, Z up)
def _rod(p0, p1, r):
    return bar(p0, p1, 2 * r, 0.0)


def _tab(P, z_bot=None):
    w, t, d, below, h = P["TAB"]
    zb = -(h - below) if z_bot is None else z_bot
    s = Pos(0, 0, (zb + below) / 2) * Box(w, t, below - zb)
    s = cp.break_edges(s, 1.0)
    return drill(s, (0, 0, 0), "y", d, 40)


def _clip(centre, axis, r_pin):
    """R-clip drawn as a retaining ring round a pin end."""
    ring = Torus(r_pin + 1.3, 1.2)
    return Pos(*centre) * orient(ring, axis)


def build_grab(A, P, L, tag=""):
    """Clamshell grab, closed, in the placement L (a Location). Returns the z of the hinge pin (local)."""
    R, B = P["GRAB_R"], P["GRAB_B"]
    ts, tp = P["GRAB_SHEET"], P["GRAB_PLATE"]
    xh = P["GRAB_HEAD_X"]
    z_head_pin = -92.0
    ear_x, ear_dz = R - 30, 35.0
    z_h = z_head_pin - math.sqrt(P["GRAB_ROD"] ** 2 - (ear_x - xh) ** 2) - ear_dz
    hb = B / 2
    bom = 17
    for side, sx in (("left", -1), ("right", 1)):
        ylen = hb if sx < 0 else hb + tp + 1
        cyl_o = Rot(90, 0, 0) * Cylinder(R, 2 * ylen)
        cyl_i = Rot(90, 0, 0) * Cylinder(R - ts, 2 * ylen + 2)
        quad = Pos(sx * R / 2, 0, -R / 2) * Box(R, 2 * ylen + 4, R)
        shell = Pos(0, 0, z_h) * ((cyl_o - cyl_i) & quad)
        cover = Pos((sx * R * 0.5 + sx * (R - ts)) / 2, 0, z_h - ts / 2) * Box(abs(R - ts - R * 0.5), 2 * ylen, ts)
        A.add(f"Grab {side} shell, 3 mm S275 rolled and flat cover", L * (shell + cover), "galvanised", bom=bom)
        p0 = hb if sx < 0 else hb + tp + 1
        for sy in (-1, 1):
            y_lo, y_hi = sorted((sy * p0, sy * (p0 + tp)))
            disc = (Pos(0, (y_lo + y_hi) / 2, 0) * Rot(90, 0, 0) * Cylinder(R, tp)) & Pos(sx * R / 2, (y_lo + y_hi) / 2, -R / 2) * Box(R, tp + 2, R)
            disc = Pos(0, 0, z_h) * disc
            ear = box(min(sx * (R - 55), sx * R), max(sx * (R - 55), sx * R), y_lo, y_hi, z_h - 5, z_h + ear_dz + 22, 0)
            boss = Pos(0, (y_lo + y_hi) / 2, z_h) * Rot(90, 0, 0) * Cylinder(35, tp)
            pl = disc + ear + boss
            pl = pl - Pos(0, (y_lo + y_hi) / 2, z_h) * Rot(90, 0, 0) * Cylinder(P["GRAB_PIN"] / 2 + 0.25, tp + 2)
            pl = pl - Pos(sx * ear_x, (y_lo + y_hi) / 2, z_h + ear_dz) * Rot(90, 0, 0) * Cylinder(6.5, tp + 2)
            A.add(f"Grab {side} end plate {'front' if sy < 0 else 'back'}, 5 mm", L * cp.break_edges(pl, 0.8), "galvanised", bom=bom)

    yk0 = hb + 2 * tp + 3
    bars = []
    for sy in (-1, 1):
        y_lo, y_hi = sorted((sy * yk0, sy * (yk0 + 6)))
        b_ = box(-25, 25, y_lo, y_hi, z_h - 30, z_h + 300, 1.0)
        b_ = b_ - Pos(0, (y_lo + y_hi) / 2, z_h) * Rot(90, 0, 0) * Cylinder(P["GRAB_PIN"] / 2 + 0.25, 8)
        bars.append(b_)
    cross = box(-25, 25, -(yk0 + 6), yk0 + 6, z_h + 300, z_h + 310, 1.0)
    eye = box(-5, 5, 20, 60, z_h + 310, z_h + 350, 1.0) - Pos(0, 40, z_h + 332) * orient(Cylinder(7, 20), "+x")
    A.add("Grab closing yoke, 6 mm bar (two arms, crossbar, eye plate)", L * Compound(bars + [cross, eye]), "galvanised", bom=bom)
    for sy in (-1, 1):
        A.add(f"Weld, yoke arm {'front' if sy < 0 else 'back'} to crossbar",
              L * weld_bead((-25, sy * yk0, z_h + 300), "+x", 50, "-y" if sy > 0 else "+y", "-z", 5),
              "mild_steel", kind="weld", bom=bom)
    pinL = P["GRAB_PIN"]
    A.add("Grab hinge pin, 25 mm", L * (Pos(0, -(yk0 + 12), z_h) * orient(cp.round_bar(pinL, 2 * (yk0 + 12), 1.0), "+y")), "stainless", bom=bom)
    yr0 = yk0 + 8
    rods_, pins = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            y_lo, y_hi = sorted((sy * yr0, sy * (yr0 + 6)))
            a = Vector(sx * ear_x, 0, z_h + ear_dz)
            b = Vector(sx * xh, 0, z_head_pin)
            d = b - a
            ang = math.degrees(math.atan2(d.X, d.Z))
            bar_ = Pos(a.X, (y_lo + y_hi) / 2, a.Z) * Rot(0, ang, 0) * box(-15, 15, -3, 3, -15, d.length + 15, 2.0)
            bar_ = bar_ - Pos(a.X, (y_lo + y_hi) / 2, a.Z) * Rot(90, 0, 0) * Cylinder(6.5, 10)
            bar_ = bar_ - Pos(b.X, (y_lo + y_hi) / 2, b.Z) * Rot(90, 0, 0) * Cylinder(6.5, 10)
            A.add(f"Grab tag rod {'L' if sx < 0 else 'R'}{'front' if sy < 0 else 'back'}, 30 x 6 flat", L * bar_, "galvanised", bom=bom)
        A.add(f"Grab ear pin {'L' if sx < 0 else 'R'}, 12 mm", L * (Pos(sx * ear_x, -(yr0 + 12), z_h + ear_dz) * orient(cp.round_bar(12, 2 * (yr0 + 12), 0.8), "+y")),
              "stainless", bom=bom)
        A.add(f"Grab head pin {'L' if sx < 0 else 'R'}, 12 mm", L * (Pos(sx * xh, -(yr0 + 20), z_head_pin) * orient(cp.round_bar(12, 2 * (yr0 + 20), 0.8), "+y")),
              "stainless", bom=bom)
        for sy in (-1, 1):
            A.add(f"R-clip, ear pin {'L' if sx < 0 else 'R'}{'f' if sy < 0 else 'b'}", L * _clip((sx * ear_x, sy * (yr0 + 9), z_h + ear_dz), "+y", 6),
                  "stainless", kind="fastener", bom=bom)
            A.add(f"R-clip, head pin {'L' if sx < 0 else 'R'}{'f' if sy < 0 else 'b'}", L * _clip((sx * xh, sy * (yr0 + 17), z_head_pin), "+y", 6),
                  "stainless", kind="fastener", bom=bom)
    for sy in (-1, 1):
        A.add(f"R-clip, hinge pin {'f' if sy < 0 else 'b'}", L * _clip((0, sy * (yk0 + 9), z_h), "+y", 12.5), "stainless", kind="fastener", bom=bom)
    yl0 = yr0 + 7
    plate_ = box(-80, 80, -(yl0 + 8), yl0 + 8, -70, -60, 1.0) - Pos(0, 40, -65) * Cylinder(15, 12)
    A.add("Grab head beam, 10 mm S275 plate", L * plate_, "galvanised", bom=bom)
    A.add("Grab head tab, 10 mm, 20 mm hole", L * _tab(P, -60), "galvanised", bom=bom)
    A.add("Weld, grab tab (front)", L * weld_bead((-30, -5, -60), "+x", 60, "-y", "+z", 5), "mild_steel", kind="weld", bom=bom)
    A.add("Weld, grab tab (back)", L * weld_bead((-30, 5, -60), "+x", 60, "+y", "+z", 5), "mild_steel", kind="weld", bom=bom)
    for sx in (-1, 1):
        for sy in (-1, 1):
            y_lo, y_hi = sorted((sy * yl0, sy * (yl0 + 8)))
            lg = box(min(sx * 40, sx * 80), max(sx * 40, sx * 80), y_lo, y_hi, -112, -70, 1.0)
            lg = lg - Pos(sx * xh, (y_lo + y_hi) / 2, z_head_pin) * Rot(90, 0, 0) * Cylinder(6.5, 12)
            A.add(f"Grab beam lug {'L' if sx < 0 else 'R'}{'front' if sy < 0 else 'back'}", L * lg, "galvanised", bom=bom)
            xa, xb = (40, 80)
            A.add(f"Weld, beam lug {'L' if sx < 0 else 'R'}{'f' if sy < 0 else 'b'}",
                  L * weld_bead((sx * 40 if sx > 0 else sx * 80, y_lo if sy > 0 else y_hi, -70), "+x", 40,
                                "-y" if sy > 0 else "+y", "-z", 4), "mild_steel", kind="weld", bom=bom)
    return z_h




def build_sampler(A, P, L):
    od, wall, Lt = P["SAMP_TUBE"]
    rc, D = P["SAMP_CAGE_R"], P["SAMP_PLATE_D"]
    bom = 18
    top = Pos(0, 0, -66) * (cp.sheet(D, D, 6, holes=[(0, 0, 32.0)], r_corner=D / 2 - 0.5, edge=0.6))
    A.add("Sampler top plate, 6 mm", L * top, "stainless", bom=bom)
    bot = Pos(0, 0, -766) * (cp.sheet(D, D, 6, holes=[(0, 0, od + 2.0)], r_corner=D / 2 - 0.5, edge=0.6))
    A.add("Sampler bottom plate, 6 mm", L * bot, "stainless", bom=bom)
    bo, bi, bh = P["SAMP_BALLAST"]
    A.add("Sampler ballast ring, 3.5 kg steel", L * Pos(0, 0, -766 - bh) * cp.break_edges(cp.round_tube(bo, (bo - bi) / 2, bh), 1.5),
          "mild_steel", bom=bom)
    A.add("Sampler tab, 10 mm, 20 mm hole", L * _tab(P, -60), "galvanised", bom=bom)
    A.add("Weld, sampler tab", L * weld_bead((-30, -5, -60), "+x", 60, "-y", "+z", 5), "mild_steel", kind="weld", bom=bom)
    for k, a_ in enumerate((45, 135, 225, 315)):
        x, y = rc * math.cos(math.radians(a_)), rc * math.sin(math.radians(a_))
        A.add(f"Sampler cage rod {k + 1}, 10 mm stainless", L * Pos(x, y, -760) * cp.round_bar(10, 694, 0.8), "stainless", bom=bom)
        A.add(f"Weld, cage rod {k + 1} top", L * Pos(x, y, -66) * Rot(180, 0, 0) * ring_weld(5, 3.0), "mild_steel", kind="weld", bom=bom)
        A.add(f"Weld, cage rod {k + 1} bottom", L * Pos(x, y, -760) * ring_weld(5, 3.0), "mild_steel", kind="weld", bom=bom)
    A.add("Sampler tube, 75 mm clear PVC", L * Pos(0, 0, -120 - Lt) * cp.round_tube(od, wall, Lt), "polycarbonate", kind="bought", bom=bom)
    for z, nm in ((-260, "upper"), (-620, "lower")):
        ring = Pos(0, 0, z) * cp.break_edges(cp.round_tube(2 * (rc - 5), (rc - 5) - od / 2, 20), 1.0)
        A.add(f"Sampler tube clamp ring ({nm}), stainless", L * ring, "stainless", bom=bom)
    for zc, nm, sgn in ((-120, "top", 1), (-120 - Lt, "bottom", -1)):
        plug = Pos(0, 0, zc - 6 if sgn > 0 else zc + 6) * Cylinder(od / 2 - wall - 0.5, 12)
        disc = Pos(0, 0, zc + 3 if sgn > 0 else zc - 3) * Cylinder(45, 6)
        A.add(f"Sampler {nm} rubber cap", L * cp.break_edges(plug + disc, 1.0), "epdm", kind="bought", bom=bom)
    latch = box(-8, 8, 30, 58, -110, -66, 1.0) + box(-8, 8, 30, 70, -100, -92, 1.0)
    A.add("Sampler trip latch", L * latch, "stainless", bom=bom)
    A.add("Sampler cap cord, 4 mm elastic", L * cp.rope([(0, 0, -112), (0, 20, -104), (0, 44, -96)], 4.0), "rubber_belt", kind="bought", bom=bom)


def build_rake(A, P, L):
    W = P["RAKE_W"]
    d, Lt = P["RAKE_TINE"]
    bom = 19
    barb = box(-W / 2, W / 2, -6, 6, -460, -410, 1.5) - Pos(0, 0, -435) * Rot(90, 0, 0) * Cylinder(8, 30)
    A.add("Rake tine bar, 50 x 12 flat", L * barb, "galvanised", bom=bom)
    A.add("Rake ballast bar, 40 x 40", L * box(-W / 2 + 10, W / 2 - 10, -20, 20, -410, -370, 2.0), "galvanised", bom=bom)
    A.add("Rake top plate, 12 mm", L * box(-45, 45, -20, 20, -72, -60, 1.5), "galvanised", bom=bom)
    A.add("Rake tab, 10 mm, 20 mm hole", L * _tab(P, -60), "galvanised", bom=bom)
    A.add("Weld, rake tab", L * weld_bead((-30, -5, -60), "+x", 60, "-y", "+z", 5), "mild_steel", kind="weld", bom=bom)
    n = P["RAKE_TINES"]
    for k in range(n):
        x = -W / 2 + 20 + k * (W - 40) / (n - 1)
        A.add(f"Rake tine {k + 1}, 12 mm", L * Pos(x, 0, -460 - Lt) * cp.round_bar(d, Lt, 1.0), "galvanised", bom=bom)
        A.add(f"Weld, rake tine {k + 1}", L * Pos(x, 0, -460) * Rot(180, 0, 0) * ring_weld(d / 2, 3.0), "mild_steel", kind="weld", bom=bom)
    for sx in (-1, 1):
        a = Vector(sx * (W / 2 - 25), 0, -370)
        b = Vector(sx * 22, 0, -72)
        dv = b - a
        ang = math.degrees(math.atan2(dv.X, dv.Z))
        bail = Pos(a.X, 0, a.Z) * Rot(0, ang, 0) * box(-20, 20, -4, 4, 0, dv.length + 8, 1.0)
        bail = bail & Pos(0, 0, (-370 - 72) / 2) * Box(2 * W, 40, 298)
        A.add(f"Rake bail {'L' if sx < 0 else 'R'}, 40 x 8", L * bail, "galvanised", bom=bom)
    drag = box(-6, 6, -45, -6, -455, -415, 1.5) - Pos(0, -30, -435) * orient(Cylinder(8, 30), "+x")
    A.add("Rake drag eye plate", L * drag, "galvanised", bom=bom)
    A.add("Weld, rake drag eye", L * weld_bead((-6, -6, -455), "+x", 12, "-y", "-z", 4), "mild_steel", kind="weld", bom=bom)


def build_retrieval(A, P, L):
    D, T, H = P["RET_D"], P["RET_THROAT"], P["RET_DEPTH"]
    bom = 20
    disc = Pos(0, 0, -66) * cp.sheet(D, D, 6, holes=[(0, 0, T - 20.0)], r_corner=D / 2 - 0.5, edge=0.6)
    strap = box(-60, 60, -15, 15, -66, -60, 1.0)
    A.add("Retrieval guide top disc, 6 mm, with cross strap", L * (disc + strap), "galvanised", bom=bom)
    A.add("Retrieval guide tab, 10 mm, 20 mm hole", L * _tab(P, -60), "galvanised", bom=bom)
    A.add("Weld, guide tab", L * weld_bead((-30, -5, -60), "+x", 60, "-y", "+z", 5), "mild_steel", kind="weld", bom=bom)
    outer = Solid_cone(D / 2, T / 2, H)
    inner = Solid_cone(D / 2 - 2.5, T / 2 - 2.5, H + 0.1)
    fun = Pos(0, 0, -66 - H / 2) * outer - Pos(0, 0, -66 - H / 2 + 0.0) * inner
    A.add("Retrieval funnel, 2.5 mm sheet", L * fun, "galvanised", bom=bom)
    socket = Pos(D / 2 - 30, 0, -60) * cp.round_tube(33.7, 3.2, 150)
    gus = box(D / 2 - 50, D / 2 - 14, -4, 4, -60, 0, 0.8)
    A.add("Pole socket 33.7 mm with gusset", L * (socket + gus), "galvanised", bom=bom)
    A.add("Retrieval sling, 5 mm steel", L * Pos(0, 0, -66 - H - 30) * cp.round_bar(10, H + 30, 0.8), "stainless", kind="bought", bom=bom)
    body, gate, sleeve = hp.carabiner(110, 58, 10)
    cz = -66 - H - 30 - 55
    A.add("EN 362 auto-locking connector", L * Pos(0, 0, cz) * Compound([body, gate, sleeve]), "stainless", kind="bought", bom=bom)


def Solid_cone(r0, r1, h):
    """Cone frustum along Z centred on z = 0, r0 at the top, r1 at the bottom."""
    return Cone(r1, r0, h)


def build_domereach(A, P, L):
    od, wall, Ls = P["DR_POLE"]
    bom = 21
    top = -30.0
    A.add("DomeReach pole section 1, 50 x 3 aluminium", L * Pos(0, 0, top - Ls) * cp.round_tube(od, wall, Ls), "aluminium", bom=bom)
    A.add("DomeReach pole section 2, 50 x 3 aluminium", L * Pos(0, 0, top - 2 * Ls) * cp.round_tube(od, wall, Ls), "aluminium", bom=bom)
    joint = Pos(0, 0, top - Ls - 80) * cp.round_tube(od + 8.0, 3.5, 160)
    A.add("DomeReach spigot joint sleeve", L * joint, "aluminium", bom=bom)
    A.add("DomeReach top cap with tab", L * (Pos(0, 0, top) * cp.break_edges(Cylinder(od / 2, 8).moved(Pos(0, 0, 4)), 1.0) + _tab(P, top + 8)), "aluminium", bom=bom)
    tod, tlen, tbelow = P["DR_TILLER"]
    collar = Pos(0, 0, -tbelow - 30) * cp.round_tube(od + 12, 6, 60)
    yc_ = (od + 12) / 2
    lh = tlen / 2 - yc_
    t_r = Pos(0, yc_, -tbelow) * orient(cp.round_bar(tod, lh, 1.0), "+y")
    t_l = Pos(0, -yc_, -tbelow) * orient(cp.round_bar(tod, lh, 1.0), "-y")
    A.add("DomeReach tiller on its clamp collar", L * Compound([collar, t_r, t_l]), "aluminium", bom=bom)
    zb = top - 2 * Ls
    fair = Pos(0, 0, top - 500 - 15) * cp.round_tube(od + 24, 12, 30)
    eyer = Pos(od / 2 + 14, 0, top - 500) * Rot(0, 90, 0) * Torus(9, 3)
    A.add("DomeReach fairlead ring", L * Compound([fair, eyer]), "aluminium", bom=bom)
    # clevis collar with two ears, arm on a 12 mm pin, plug, pull line, sealant roller
    plug = Pos(0, 0, zb + 30) * Cylinder(od / 2 - wall - 0.3, 60)
    A.add("DomeReach pole end plug", L * cp.break_edges(plug, 1.0), "hdpe_natural", bom=bom)
    zh = zb - 60                                   # hinge height, 60 mm below the pole end
    cl_collar = Pos(0, 0, zb) * cp.round_tube(od + 12, 6, 90)
    A.add("DomeReach clevis collar", L * cl_collar, "mild_steel", bom=bom)
    for sy in (-1, 1):
        ear = plate("xz", 70, 180, 6, (0, sy * 34, zb), holes=[(0, zh - zb, 12.5)], r_corner=10)
        A.add(f"DomeReach clevis ear {'rear' if sy < 0 else 'front'}", L * ear, "mild_steel", bom=bom)
    ang = P["DR_ARM_DEG"]
    aw, at, aL = P["DR_ARM"]
    arm = Pos(0, 0, zh) * Rot(0, ang, 0) * (Pos(0, 0, -15) * cp.shs(aw, at, aL + 15))
    arm = arm - Pos(0, 0, zh) * orient(Cylinder(6.3, 80), "+y")
    A.add("DomeReach arm, 40 x 40 x 3 aluminium", L * arm, "aluminium", bom=bom)
    A.add("DomeReach arm pin, 12 mm with split pin", L * Pos(0, -45, zh) * orient(cp.round_bar(12, 90, 0.8), "+y"), "stainless", bom=bom)
    A.add("Split pin, DomeReach arm", L * Pos(0, 41, zh) * cp.split_pin(12), "stainless", kind="fastener", bom=bom)
    tip = Vector(0, 0, zh) + Vector(math.sin(math.radians(ang)), 0, math.cos(math.radians(ang))) * (aL + 45)
    rd, rw = P["DR_ROLLER"]
    fork = Pos(tip.X, 0, tip.Z) * Rot(0, ang, 0) * box(-6, 6, -rw / 2 - 14, rw / 2 + 14, -45, 0, 1.0)
    for sy in (-1, 1):                              # axle bearing blocks on the fork, standing above its upper face
        blk = Pos(tip.X, sy * (rw / 2 + 7), tip.Z) * Rot(0, ang, 0) * box(-12, 12, -5, 5, 0, 50, 1.0)
        fork = fork + blk
    fork = fork - Pos(tip.X + 30 * math.sin(math.radians(ang)), 0, tip.Z + 30 * math.cos(math.radians(ang))) * orient(Cylinder(8.3, 400), "+y")
    A.add("DomeReach tool fork", L * fork, "aluminium", bom=bom)
    sx_, sz_ = 30 * math.sin(math.radians(ang)), 30 * math.cos(math.radians(ang))
    roller = Pos(tip.X + sx_, 0, tip.Z + sz_) * Rot(90, 0, 0) * (Cylinder(rd / 2, rw) - Cylinder(8.5, rw + 2))
    A.add("DomeReach roller axle, 16.5 mm", L * Pos(tip.X + sx_, -(rw / 2 + 14), tip.Z + sz_) * orient(cp.round_bar(16.5, rw + 28, 0.8), "+y"), "stainless", kind="bought", bom=bom)
    A.add("DomeReach sealant roller, 60 x 230", L * roller, "epdm", kind="bought", bom=bom)
    A.add("DomeReach pull line, 6 mm", L * cp.rope([(od / 2 + 14, 0, top - 500), (od / 2 + 20, 0, top - 1200), (aL * 0.35 * math.sin(math.radians(ang)) + 10, 0, zh + aL * 0.35 * math.cos(math.radians(ang)) + 26)], 6.0),
          "rope", kind="bought", bom=bom)


# ------------------------------------------------------------------------------------- accessories and labels
def cone_traffic(A, P, xy, n):
    x, y = xy
    base = Pos(x, y, 0) * cp.sheet(380, 380, 12, r_corner=20, edge=0.8)
    shell = Pos(x, y, 12 + 360) * (Cone(120, 20, 720) - Pos(0, 0, 3) * Cone(117, 17, 716))
    A.add(f"Traffic cone {n}, 750 mm: base", base, "epdm", kind="bought", bom=22)
    A.add(f"Traffic cone {n}, 750 mm: body", shell, "safety_red", kind="bought", bom=22)


def barrier_chain(A, P, pts):
    """10 m plastic barrier chain drawn between the cones as a sagging run of 8 mm round links (envelope)."""
    A.add("Barrier chain, plastic, between the cones", cp.rope(pts, 8.0), "safety_yellow", kind="bought", bom=22)


def carry_bag(A, P, xy, n, rot=0.0):
    x, y = xy
    body = cp.break_edges(Pos(0, 0, 150) * Box(600, 280, 300), 40.0)
    body = body - cp.break_edges(Pos(0, 0, 150) * Box(594, 274, 294), 37.0)     # 3 mm canvas shell, empty (the heads are modelled separately)
    strap = cp.rope([(-150, 0, 300), (-150, 0, 380), (150, 0, 380), (150, 0, 300)], 20.0)
    A.add(f"Carry bag {n}, canvas", Pos(x, y, 0) * Rot(0, 0, rot) * body, "canvas", kind="bought", bom=23)
    A.add(f"Carry bag {n} handle", Pos(x, y, 0) * Rot(0, 0, rot) * strap, "canvas", kind="bought", bom=23)


def labels(A, P, g):
    LA = g["LF"][P["LEG_AZ"][0]]
    w = P["UP"][0] / 2
    A.add("Safe working load label (150 kg) on leg A", LA * plate("xz", 48, 160, 0.8, (0, w + 0.4, -640), r_corner=3, edge=0.2),
          "safety_yellow", kind="made", bom=24)
    A.add("Winch warning label (never lift a person)",
          LA * plate("yz", 100, 100, 0.8, (-59.4, 130.0, -P["DRUM_S"]), r_corner=3, edge=0.2), "safety_yellow", kind="made", bom=24)


# ------------------------------------------------------------------------------------- option A
def option_a():
    P = PARAMS
    g = _geo(P)
    A = Asm(EXPLODE_A)
    hz = P["HOOK_Z"]
    build_tripod(A, P, g)
    build_feet(A, P, g)
    build_head(A, P, g)
    build_chains(A, P, g)
    build_winch(A, P, g)
    build_rope(A, P, g, hz)
    build_interface(A, P, hz)
    build_guard(A, P)
    zh_ = build_grab(A, P, Pos(0, 0, hz))
    build_working_line(A, P, g, hz, hz + zh_ + 332)
    build_sampler(A, P, Pos(*HEAD_SPOTS["sampler"]) * Pos(0, 0, 806))
    build_rake(A, P, Pos(*HEAD_SPOTS["rake"]) * Pos(0, 0, 710))
    build_retrieval(A, P, Pos(*HEAD_SPOTS["retrieval"]) * Pos(0, 0, 456))
    zb = -30 - 2 * P["DR_POLE"][2] - 60
    Ld = Pos(*HEAD_SPOTS["domereach"]) * Pos(zb / 2 + 30, 0, 38.0) * Rot(0, -90, 0)
    build_domereach(A, P, Ld)
    cones = [(1500, -1700), (-1500, -1700), (-1500, 1500), (1500, 1500)]
    for n, xy in enumerate(cones, 1):
        cone_traffic(A, P, xy, n)
    barrier_chain(A, P, [(1500, -1700, 600), (0, -1700, 560), (-1500, -1700, 600)])
    for n in range(5):
        carry_bag(A, P, (BAG_SPOT[0] - 680 * (n % 2), BAG_SPOT[1] - 380 * (n // 2)), n + 1, rot=4.0 * (n % 3))
    labels(A, P, g)
    return A.parts


ALLOWED_CONTACTS = [
    ("screw pin", "Chain shackle"), ("screw pin", "Bow shackle"), ("screw pin", "Hanger shackle"),
    ("drum axle", "gearbox"), ("crank shaft", "gearbox"),
    ("Wire rope 6 mm", "wound on the drum"), ("Rope thimble", "Swaged ferrule"), ("sheave", "Wire rope"),
    ("Weld, cheek", "Mast back gusset"),
    ("Working line", "Grab closing yoke"), ("Working line", "Snatch block"), ("Working line", "cleat"),
    ("Eye bolt", "Snatch block swivel"), ("Sampler trip latch", "Sampler cap cord"),
    ("Carry bag", "handle"), ("Traffic cone", "Barrier chain"), ("DomeReach pull line", "DomeReach arm"),
    ("DomeReach pull line", "fairlead ring"), ("Split pin", "arm pin"), ("Split pin", "DomeReach arm"),
    ("DomeReach roller axle", "DomeReach sealant roller"),
]


def head_location(name):
    """Where option A places each hung head: the placement of the head's builder origin (the tab hole)."""
    P = PARAMS
    if name == "sampler":
        return Pos(*HEAD_SPOTS["sampler"]) * Pos(0, 0, 806)
    if name == "rake":
        return Pos(*HEAD_SPOTS["rake"]) * Pos(0, 0, 710)
    if name == "retrieval":
        return Pos(*HEAD_SPOTS["retrieval"]) * Pos(0, 0, 456)
    if name == "domereach":
        zb = -30 - 2 * P["DR_POLE"][2] - 60
        return Pos(*HEAD_SPOTS["domereach"]) * Pos(zb / 2 + 30, 0, 38.0) * Rot(0, -90, 0)
    raise ValueError(name)


def components(option=None):
    option = option or CHOSEN
    if option == "A":
        return option_a()
    if option == "B":
        return option_b()
    raise ValueError(f"unknown option {option}")


# =====================================================================================================
# Option B: straddle-frame davit
# =====================================================================================================
PB = {
    "FZ": 30.0,                       # frame lifted on spacer blocks so the nuts under the rails clear the ground
    "RAIL": (80.0, 5.0), "SIDE_X": 900.0, "SIDE_Y": (-1290.0, 1040.0), "CROSS_Y": (1000.0, -1000.0, -1250.0),
    "MAST": (100.0, 5.0), "MAST_Y": -1125.0, "MAST_TOP": 2220.0, "BASE_PLATE": (250.0, 300.0, 10.0),
    "STUB": (80.0, 5.0, 400.0), "JOINT_Z": 1160.0, "CAP": (150.0, 200.0, 10.0),
    "BOOM": (80.0, 4.0), "BOOM_Z": 2152.5, "BOOM_Y0": -1045.0, "BOOM_Y1": -118.0, "SOCKET_T": 20.0, "ROOT_T": 10.0,
    "SHEAVE_Z": 2320.0, "TIP_SHEAVE_Y": -62.5, "TOP_SHEAVE_Y": -1190.5,
    "WINCH_Z": 1100.0, "CBS": 30.0, "WINCH_Y": -1143.0, "MOUNT_T": 8.0, "BLOCK_Y": -200.0,
}
EXPLODE_B = {}


def tri_plate(plane, pts, t, centre):
    """Right-triangle (or any polygon) plate with outline `pts` [(u, v), ...] in the plane's own axes ('yz' or 'xz')."""
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    if area < 0:
        pts = pts[::-1]
    s = Pos(0, 0, -t / 2) * extrude(Polygon(*pts, align=None), t)
    if plane == "yz":
        s = Plane.YZ.location * s
    elif plane == "xz":
        s = Plane.XZ.location * s
    return Pos(*centre) * s


def _csleeve(od, wall, L, axis, centre):
    """Steel crush sleeve of length L centred on `centre`, axis along '+x', '+y' or '+z'."""
    return Pos(*centre) * orient(Pos(0, 0, -L / 2) * cp.round_tube(od, wall, L), axis)


def _holes_z(shape, pts, dia):
    for (x, y) in pts:
        shape = shape - Pos(x, y, 0) * Cylinder(dia / 2, 4000)
    return shape


def build_frame_b(A, PB):
    w, t = PB["RAIL"]
    fz, sx = PB["FZ"], PB["SIDE_X"]
    y0, y1 = PB["SIDE_Y"]
    zc, top = fz + w / 2, fz + w
    xin = sx - w / 2
    # bolt points: gusset corners (two on the side rail, two on the cross rail), mast base (four on the two cross rails)
    gus = {}
    for sxs in (-1, 1):
        for cy, yc in ((1000.0, 925.0), (-1000.0, -1000.0), (-1250.0, -1175.0)):
            gus[(sxs, cy)] = [(sxs * 900.0, yc - 35.0), (sxs * 900.0, yc + 35.0), (sxs * 830.0, cy), (sxs * 770.0, cy)]
    mast_b = [(sxs * 90.0, PB["MAST_Y"] + sy * 125.0) for sxs in (-1, 1) for sy in (-1, 1)]
    allpts = [p for v in gus.values() for p in v] + mast_b
    for s_, nm in ((-1, "left"), (1, "right")):
        rail = stock_between((s_ * sx, y0, zc), (s_ * sx, y1, zc), w, w, t)
        pts = [p for p in allpts if abs(p[0] - s_ * sx) < 31]
        A.add(f"Side rail {nm}, 80 x 80 x 5 S275 galvanised", _holes_z(rail, pts, 13.5), "galvanised")
    names = {1000.0: "front", -1000.0: "rear", -1250.0: "mast sill"}
    for cy in PB["CROSS_Y"]:
        rail = stock_between((-xin, cy, zc), (xin, cy, zc), w, w, t)
        pts = [p for p in allpts if abs(p[1] - cy) < 1.0 and abs(p[0]) < xin]
        A.add(f"Cross rail ({names[cy]}), 80 x 80 x 5 S275 galvanised", _holes_z(rail, pts, 17.0 if cy != 1000.0 else 13.5), "galvanised")
    for xp in (-sx, sx):
        for yp in (500.0, -500.0):
            A.add(f"Frame spacer block ({xp:+.0f}, {yp:+.0f}), HDPE", Pos(xp, yp, 0) * cp.break_edges(cp.sheet(100, 100, fz, r_corner=10), 1.5),
                  "hdpe_black", kind="bought")
    for (sxs, cy), bolts in gus.items():
        yc = {1000.0: 925.0, -1000.0: -1000.0, -1250.0: -1175.0}[cy]
        cx = sxs * 830.0
        holes = [(bx - cx, by - yc, 13.5) for bx, by in bolts]
        gh = 135 if cy == -1000.0 else 210
        g_ = plate("xy", 200, gh, 8, (cx, yc, top + 4), holes=holes, r_corner=10)
        A.add(f"Corner gusset {'R' if sxs > 0 else 'L'} at y {cy:+.0f}, 8 mm S275 galvanised", g_, "galvanised")
        for bx, by in bolts:
            A.add(f"Frame crush sleeve ({bx:+.0f}, {by:+.0f})", _csleeve(20.0, 3.0, w - 2 * t, "+z", (bx, by, zc)), "mild_steel", kind="fastener")
            A.many(fasteners(12, 8 + w, (bx, by, top + 8), "-z", tag=f" (gusset {bx:+.0f}, {by:+.0f})"), bom=None)


def build_mast_b(A, PB, P):
    mw, mt = PB["MAST"]
    my = PB["MAST_Y"]
    w, t = PB["RAIL"]
    fz = PB["FZ"]
    bx, by, bt = PB["BASE_PLATE"]
    zb0 = fz + w
    z_base = zb0 + bt
    holes = [(sx * 90.0, sy * 125.0, 17.0) for sx in (-1, 1) for sy in (-1, 1)]
    A.add("Mast base plate, 10 mm S275 galvanised", plate("xy", bx, by, bt, (0, my, zb0 + bt / 2), holes=holes, r_corner=10), "galvanised")
    for sx in (-1, 1):
        for sy in (-1, 1):
            xy = (sx * 90.0, my + sy * 125.0)
            A.add(f"Mast base crush sleeve ({xy[0]:+.0f}, {xy[1]:+.0f})", _csleeve(24.0, 3.5, w - 2 * t, "+z", (xy[0], xy[1], fz + w / 2)), "mild_steel", kind="fastener")
            A.many(fasteners(16, bt + w, (xy[0], xy[1], zb0 + bt), "-z", tag=f" (mast base {xy[0]:+.0f}, {xy[1]:+.0f})"), bom=None)
    jz, ztop = PB["JOINT_Z"], PB["MAST_TOP"]
    stub_w, stub_t, stub_L = PB["STUB"]
    zbolts = (jz - 100.0, jz + 100.0)
    m1 = Pos(0, my, z_base) * cp.rhs(mw, mw, mt, jz - z_base)
    m2 = Pos(0, my, jz) * cp.rhs(mw, mw, mt, ztop - jz)
    m1 = drill(m1, (0, my, zbolts[0]), "x", 17.0, 400)
    m2 = drill(m2, (0, my, zbolts[1]), "x", 17.0, 400)
    # cleat bolt holes (one wall only) and winch-side clearances stay in the +x wall of the lower section
    for sg in (-1, 1):
        m1 = drill(m1, (mw / 2 - 2.5, my + sg * PB["CBS"], 800.0), "x", 7.0, 20)
    A.add("Mast lower section, 100 x 100 x 5 S275 galvanised", m1, "galvanised")
    A.add("Mast upper section, 100 x 100 x 5 S275 galvanised", m2, "galvanised")
    stub = Pos(0, my, jz - stub_L / 2) * cp.rhs(stub_w, stub_w, stub_t, stub_L)
    for z in zbolts:
        stub = drill(stub, (0, my, z), "x", 17.0, 400)
    A.add("Mast spigot stub, 80 x 80 x 5 S275 galvanised", stub, "galvanised")
    for z in zbolts:
        A.add(f"Mast joint crush sleeve (z {z:.0f})", _csleeve(24.0, 3.5, stub_w - 2 * stub_t, "+x", (0, my, z)), "mild_steel", kind="fastener")
        A.many(fasteners(16, mw, (-mw / 2, my, z), "+x", tag=f" (mast joint z {z:.0f})", L=130), bom=None)
    # foot welds: four runs, each in two pieces so they clear the rib
    for (px, py, run, la) in ((-mw / 2, my + mw / 2, "+x", "+y"), (-mw / 2, my - mw / 2, "+x", "-y")):
        for x0 in (px, px + mw / 2 + 6):
            A.add(f"Weld, mast foot {la}", weld_bead((x0, py, z_base), run, mw / 2 - 6, la, "+z", 6), "mild_steel", kind="weld")
    for (px, py, la) in ((mw / 2, my - mw / 2, "+x"), (-mw / 2, my - mw / 2, "-x")):
        for y0_ in (py, py + mw / 2 + 6):
            A.add(f"Weld, mast foot {la}", weld_bead((px, y0_, z_base), "+y", mw / 2 - 6, la, "+z", 6), "mild_steel", kind="weld")
    L_, H_ = 75.0, 150.0
    A.add("Mast rib front, 8 mm", tri_plate("yz", [(0, 0), (L_, 0), (0, H_)], 8, (0, my + mw / 2, z_base)), "galvanised")
    A.add("Mast rib back, 8 mm", tri_plate("yz", [(0, 0), (-L_, 0), (0, H_)], 8, (0, my - mw / 2, z_base)), "galvanised")
    A.add("Mast rib right, 8 mm", tri_plate("xz", [(0, 0), (L_, 0), (0, H_)], 8, (mw / 2, my, z_base)), "galvanised")
    A.add("Mast rib left, 8 mm", tri_plate("xz", [(0, 0), (-L_, 0), (0, H_)], 8, (-mw / 2, my, z_base)), "galvanised")
    for sg in (-1, 1):
        A.add(f"Weld, rib front {sg:+d}", weld_bead((sg * 4, my + mw / 2, z_base + 7), "+z", H_ - 7, f"{'+' if sg > 0 else '-'}x", "+y", 4), "mild_steel", kind="weld")
        A.add(f"Weld, rib back {sg:+d}", weld_bead((sg * 4, my - mw / 2, z_base + 7), "+z", H_ - 7, f"{'+' if sg > 0 else '-'}x", "-y", 4), "mild_steel", kind="weld")
        A.add(f"Weld, rib right {sg:+d}", weld_bead((mw / 2, my + sg * 4, z_base + 7), "+z", H_ - 7, f"{'+' if sg > 0 else '-'}y", "+x", 4), "mild_steel", kind="weld")
        A.add(f"Weld, rib left {sg:+d}", weld_bead((-mw / 2, my + sg * 4, z_base + 7), "+z", H_ - 7, f"{'+' if sg > 0 else '-'}y", "-x", 4), "mild_steel", kind="weld")
    # cap with the mast-top sheave bracket
    cx, cy_, ct = PB["CAP"]
    A.add("Mast cap, 10 mm S275 galvanised", plate("xy", cx, cy_, ct, (0, my, ztop + ct / 2), r_corner=10), "galvanised")
    A.add("Weld, mast cap rear", weld_bead((-mw / 2, my - mw / 2, ztop), "+x", mw, "-y", "-z", 5), "mild_steel", kind="weld")
    for sx in (-1, 1):
        A.add(f"Weld, mast cap side {sx:+d}", weld_bead((sx * mw / 2, my - mw / 2, ztop), "+y", mw, f"{'+' if sx > 0 else '-'}x", "-z", 5),
              "mild_steel", kind="weld")
    ys, zs = PB["TOP_SHEAVE_Y"], PB["SHEAVE_Z"]
    sheave_b(A, P, ys, zs, "Mast-top")
    zt = ztop + ct
    ch_h = (zs + 100) - zt
    for sx in (-1, 1):
        ch = plate("yz", 160, ch_h, P["CHEEK_T"], (sx * (P["CHEEK_X"] + P["CHEEK_T"] / 2), my - 60, zt + ch_h / 2),
                   holes=[(ys - (my - 60), zs - (zt + ch_h / 2), P["AXLE_D"] + 1)], r_corner=10)
        A.add(f"Mast-top cheek plate {'+' if sx > 0 else '-'}", ch, "galvanised")
        xin, xout = sx * P["CHEEK_X"], sx * (P["CHEEK_X"] + P["CHEEK_T"])
        for xx, la, nm in ((xin, "-x" if sx > 0 else "+x", "inner"), (xout, "+x" if sx > 0 else "-x", "outer")):
            A.add(f"Weld, mast-top cheek {'+' if sx > 0 else '-'} {nm}", weld_bead((xx, my - 140, zt), "+y", 160 - 40, la, "+z", 5), "mild_steel", kind="weld")
    A.many(fasteners(20, 46, (-23, ys, zs), "+x", tag=" (mast-top sheave axle)", L=80), bom=None)


def sheave_b(A, P, ys, zs, tag):
    rp, rf, w = P["SHEAVE"][1], P["SHEAVE"][0], P["SHEAVE"][2]
    rc = rp - P["ROPE_D"] / 2
    prof = [(10.5, -w / 2), (rf, -w / 2), (rf, -w / 2 + 4), (rp, -w / 2 + 9), (rc, -3), (rc, 3), (rp, w / 2 - 9),
            (rf, w / 2 - 4), (rf, w / 2), (10.5, w / 2)]
    sh = Pos(0, ys, zs) * orient(revolve_profile(prof), "+x")
    A.add(f"{tag} sheave, 150 mm, sealed bearing", sh, "stainless", kind="bought")
    for sx in (-1, 1):
        sp = Pos(sx * (w / 2 + 1.5), ys, zs) * orient(Pos(0, 0, -1.5) * extrude(Sketch() + Circle(16) - Circle(P["AXLE_D"] / 2 + 0.3), 3), "+x")
        A.add(f"{tag} sheave spacer washer {'+' if sx > 0 else '-'}", sp, "stainless", kind="fastener")


def build_boom_b(A, PB, P):
    bw, bt = PB["BOOM"]
    my, mw = PB["MAST_Y"], PB["MAST"][0]
    y_face = my + mw / 2
    zb = PB["BOOM_Z"]
    st, rt = PB["SOCKET_T"], PB["ROOT_T"]
    zt = PB["MAST_TOP"]
    pat = [(sx * 60.0, sz * 45.0) for sx in (-1, 1) for sz in (-1, 1)]
    zcp = zt - 135 / 2
    A.add("Boom socket plate, 20 mm S275 galvanised, tapped M16",
          plate("xz", 160, 135, st, (0, y_face + st / 2, zcp), holes=[(u, zb - zcp + v, 16.0) for u, v in pat], r_corner=8), "galvanised")
    A.add("Weld, boom socket bottom", weld_bead((-mw / 2, y_face, zt - 135), "+x", mw, "-z", "+y", 5), "mild_steel", kind="weld")
    for sx in (-1, 1):
        A.add(f"Weld, boom socket side {sx:+d}", weld_bead((sx * mw / 2, y_face, zt - 135), "+z", 123, f"{'+' if sx > 0 else '-'}x", "-y", 5),
              "mild_steel", kind="weld")
    A.add("Boom root plate, 10 mm S275 galvanised",
          plate("xz", 160, 135, rt, (0, y_face + st + rt / 2, zcp), holes=[(u, zb - zcp + v, 17.0) for u, v in pat], r_corner=8), "galvanised")
    for u, v in pat:
        A.many(hp.screw_in(16, 30, (u, y_face + st + rt, zb + v), "-y", tag=f" (boom root {u:+.0f}, {v:+.0f})"), bom=None)
    y0, y1 = PB["BOOM_Y0"], PB["BOOM_Y1"]
    A.add("Boom, 80 x 80 x 4 S275 galvanised", stock_between((0, y0, zb), (0, y1, zb), bw, bw, bt), "galvanised")
    h = bw / 2
    for sz in (-1, 1):
        A.add(f"Weld, boom root {'top' if sz > 0 else 'bottom'}", weld_bead((-h, y0, zb + sz * h), "+x", bw, "+y", f"{'+' if sz > 0 else '-'}z", 5), "mild_steel", kind="weld")
    for sx in (-1, 1):
        A.add(f"Weld, boom root side {sx:+d}", weld_bead((sx * h, y0, zb - h), "+z", bw, "+y", f"{'+' if sx > 0 else '-'}x", 5), "mild_steel", kind="weld")
    A.add("Boom tip plate, 8 mm S275 galvanised", plate("xz", bw, bw, 8, (0, y1 + 4, zb), r_corner=4), "galvanised")
    ys, zs = PB["TIP_SHEAVE_Y"], PB["SHEAVE_Z"]
    sheave_b(A, P, ys, zs, "Boom-tip")
    zt_b = zb + h
    ch_h = (zs + 100) - zt_b
    for sx in (-1, 1):
        ch = plate("yz", 220, ch_h, P["CHEEK_T"], (sx * (P["CHEEK_X"] + P["CHEEK_T"] / 2), -80, zt_b + ch_h / 2),
                   holes=[(ys + 80, zs - (zt_b + ch_h / 2), P["AXLE_D"] + 1)], r_corner=10)
        A.add(f"Boom-tip cheek plate {'+' if sx > 0 else '-'}", ch, "galvanised")
        xin, xout = sx * P["CHEEK_X"], sx * (P["CHEEK_X"] + P["CHEEK_T"])
        for xx, la, nm in ((xin, "-x" if sx > 0 else "+x", "inner"), (xout, "+x" if sx > 0 else "-x", "outer")):
            A.add(f"Weld, boom-tip cheek {'+' if sx > 0 else '-'} {nm}", weld_bead((xx, -190, zt_b), "+y", 80, la, "+z", 5), "mild_steel", kind="weld")
    A.many(fasteners(20, 46, (-23, ys, zs), "+x", tag=" (boom-tip sheave axle)", L=80), bom=None)


def build_winch_b(A, PB, P):
    my, mw = PB["MAST_Y"], PB["MAST"][0]
    mt, zw, sd = PB["MOUNT_T"], PB["WINCH_Z"], P["DRUM_S"]
    y_rear = my - mw / 2
    holes = [(sx * 40.0, dz, 8.0) for sx in (-1, 1) for dz in (-70.0, 70.0)]
    A.add("Winch mounting plate, 8 mm S275 galvanised", plate("xz", 100, 270, mt, (0, y_rear - mt / 2, zw), holes=holes, r_corner=8), "galvanised")
    for sz in (-1, 1):
        A.add(f"Weld, winch mount {'top' if sz > 0 else 'bottom'}", weld_bead((-50, y_rear, zw + sz * 135), "+x", 100, f"{'+' if sz > 0 else '-'}z", "-y", 5),
              "mild_steel", kind="weld")
    L = Pos(0, PB["WINCH_Y"], zw + sd) * Rot(0, 0, 180)
    winch_hardware(A, P, L, 40.0, sd, bl=16)
    return L


def build_rope_b(A, PB, P, L, hz):
    rp = P["SHEAVE"][1]
    drum = (L * Pos(0, P["ROPE_OFFSET"], -P["DRUM_S"])).position
    ys1, zs, ys2 = PB["TOP_SHEAVE_Y"], PB["SHEAVE_Z"], PB["TIP_SHEAVE_Y"]
    pts = [(drum.X, drum.Y, drum.Z)]
    for k in range(13):
        a = math.radians(180 - k * 7.5)
        pts.append((0.0, ys1 + rp * math.cos(a), zs + rp * math.sin(a)))
    for k in range(13):
        a = math.radians(90 - k * 7.5)
        pts.append((0.0, ys2 + rp * math.cos(a), zs + rp * math.sin(a)))
    pts.append((0.0, 0.0, hz + IFACE_TOP))
    A.add("Wire rope 6 mm 7x19 grade 316, run drum to head interface", cp.rope(pts, P["ROPE_D"]), "stainless", kind="bought")
    wound = revolve_profile([(P["DRUM_R"], -50), (P["ROPE_LAYER_R"], -50), (P["ROPE_LAYER_R"], 50), (P["DRUM_R"], 50)])
    A.add("Wire rope wound on the drum (3 layers, envelope)", L * Pos(0, P["DRUM_Y"], -P["DRUM_S"]) * orient(wound, "+x"), "stainless", kind="bought")
    A.add("Rope thimble", Pos(0, 0, hz + IFACE_TOP - 19) * Rot(90, 0, 0) * Torus(12, 4), "stainless", kind="bought")
    A.add("Swaged ferrule", Pos(0, 0, hz + IFACE_TOP + 4) * (Cylinder(7, 24) - Cylinder(P["ROPE_D"] / 2, 30)), "stainless", kind="bought")


def build_working_line_b(A, PB, P, z_eye, hz):
    """Block hanger arm welded to the boom tip plate, 5/16 in shackle, snatch block, working line to a cleat on the mast."""
    h = PB["BOOM"][0] / 2
    zb_ = PB["BOOM_Z"]
    y_tip = PB["BOOM_Y1"] + 8                         # outer face of the tip plate (-110)
    xa = 28.0                                          # arm centre line, beside the rope
    ya1 = 140.0
    ah = 80.0
    zc_a = zb_ - h + 20.0                              # arm 80 high: 20 above the boom underside, 60 below
    zc_a = zb_ - h + ah / 2 - 20.0
    la = ya1 - y_tip
    hole_y, hole_dz = ya1 - 25.0, -(ah / 2 - 12.5)
    arm = plate("yz", la, ah, 8, (xa, y_tip + la / 2, zc_a), holes=[(hole_y - (y_tip + la / 2), hole_dz, 11.0)], r_corner=8)
    A.add("Block hanger arm, 8 mm S275 galvanised", arm, "galvanised")
    for sg in (-1, 1):
        A.add(f"Weld, hanger arm {'outer' if sg > 0 else 'inner'}", weld_bead((xa + sg * 4, y_tip, zb_ - h), "+z", ah - 20.0, f"{'+' if sg > 0 else '-'}x", "+y", 4),
              "mild_steel", kind="weld")
    zp = zc_a + hole_dz
    body, pin = hp.shackle(8.0, 18.0, 16.0)
    loc = Pos(xa, hole_y, zp) * Rot(0, 0, 90) * Rot(180, 0, 0)
    A.add("Hanger shackle 5/16 in, body", loc * body, "stainless", kind="bought")
    A.add("Hanger shackle 5/16 in, screw pin", loc * pin, "stainless", kind="bought")
    ze = zp - (16.0 + 9.0) - 0.3
    eye = Pos(xa, hole_y, ze) * Rot(0, 90, 0) * Torus(8, 3)
    stem = Pos(xa, hole_y, ze - 11) * cp.round_bar(10, 6, 0.5)
    cz = ze - 11
    sheave_z = cz - 55
    for sx in (-1, 1):
        cheek = plate("yz", 50, 90, 3, (xa + sx * 9.5, hole_y, cz - 40), holes=[(0, sheave_z - (cz - 40), 8.5)], r_corner=14)
        A.add(f"Snatch block cheek {'+' if sx > 0 else '-'}", cheek, "stainless", kind="bought")
    A.add("Snatch block swivel eye and stem", Compound([eye, stem]), "stainless", kind="bought")
    prof = [(5.5, -6), (25, -6), (25, -3), (21, -1.5), (21, 1.5), (25, 3), (25, 6), (5.5, 6)]
    A.add("Snatch block sheave, 50 mm", Pos(xa, hole_y, sheave_z) * Rot(0, 90, 0) * revolve_profile(prof), "aluminium", kind="bought")
    A.add("Snatch block axle pin 8 mm", Pos(xa - 12.5, hole_y, sheave_z) * orient(cp.round_bar(8, 25, 0.5), "+x"), "stainless", kind="bought")
    # cleat on the +x face of the mast
    mw, my = PB["MAST"][0], PB["MAST_Y"]
    x0, zc = mw / 2, 800.0
    base = plate("yz", 150, 28, 10, (x0 + 5, my, zc), holes=[(sg * PB["CBS"], 0, 7.0) for sg in (-1, 1)], r_corner=6)
    horns = [box(x0 + 10, x0 + 28, my + sg * 62.5 - 12.5, my + sg * 62.5 + 12.5, zc - 9, zc + 9, 3.0) for sg in (-1, 1)]
    A.add("Working line cleat, 150 mm aluminium", Compound([base] + horns), "aluminium", kind="bought")
    for sg in (-1, 1):
        A.many(fasteners(6, 15, (x0 + 10, my + sg * PB["CBS"], zc), "-x", tag=f" (cleat {sg:+d})"), bom=None)
    rr = 26.0
    arc = [(xa, hole_y + rr * math.cos(math.radians(a_)), sheave_z + rr * math.sin(math.radians(a_))) for a_ in range(180, -1, -15)]
    line = cp.rope([(0.0, 40.0, z_eye), (0.0, 40.0, hz + 220.0)] + arc + [(x0 + 19, my + 62.5, zc + 14)], 10.0)
    A.add("Working line 10 mm polyester (grab closing line, drawn to the cleat)", line, "rope", kind="bought")


def option_b():
    P = PARAMS
    A = Asm(EXPLODE_B)
    hz = P["HOOK_Z"]
    build_frame_b(A, PB)
    build_mast_b(A, PB, P)
    build_boom_b(A, PB, P)
    L = build_winch_b(A, PB, P)
    build_rope_b(A, PB, P, L, hz)
    build_interface(A, P, hz)
    build_guard(A, P)
    zh_ = build_grab(A, P, Pos(0, 0, hz))
    build_working_line_b(A, PB, P, hz + zh_ + 332, hz)
    build_sampler(A, P, Pos(*HEAD_SPOTS["sampler"]) * Pos(0, 0, 806))
    build_rake(A, P, Pos(*HEAD_SPOTS["rake"]) * Pos(0, 0, 710))
    build_retrieval(A, P, Pos(*HEAD_SPOTS["retrieval"]) * Pos(0, 0, 456))
    zb = -30 - 2 * P["DR_POLE"][2] - 60
    Ld = Pos(*HEAD_SPOTS["domereach"]) * Pos(zb / 2 + 30, 0, 38.0) * Rot(0, -90, 0)
    build_domereach(A, P, Ld)
    cones = [(1500, -1700), (-1500, -1700), (-1500, 1500), (1500, 1500)]
    for n, xy in enumerate(cones, 1):
        cone_traffic(A, P, xy, n)
    barrier_chain(A, P, [(1500, -1700, 600), (0, -1700, 560), (-1500, -1700, 600)])
    for n in range(5):
        carry_bag(A, P, (BAG_SPOT[0] - 680 * (n % 2), BAG_SPOT[1] - 380 * (n // 2)), n + 1, rot=4.0 * (n % 3))
    mw, my = PB["MAST"][0], PB["MAST_Y"]
    A.add("Safe working load label (150 kg) on the mast", plate("yz", 48, 160, 0.8, (-mw / 2 - 0.4, my, 700), r_corner=3, edge=0.2), "safety_yellow", kind="made")
    A.add("Winch warning label (never lift a person)", plate("xz", 100, 100, 0.8, (0, my - mw / 2 - 0.4, 800), r_corner=3, edge=0.2), "safety_yellow", kind="made")
    return A.parts
