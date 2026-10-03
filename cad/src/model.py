"""HatchSide parametric model (build123d), TRL 3, constructable design (HTS-DDR-002).

Run from the repo root:  python cad/src/model.py          exports STEP and STL and prints the checks
                         python cad/src/model.py --check  prints the constructability checks only
Exports into cad/step and cad/stl:
    hatchside-assembly      tripod, mast, winch, rope, rim guard and the grab head hung on the rope
    hatchside-tripod        tripod, head and mast, winch and bracket (no tool head)
    hatchside-head-<name>   each tool head on its own: grab, sampler, rake, retrieval, domereach

Axes: the centre of the opening is the Z axis, Z is up and the ground is z = 0. Leg A, the winch
leg, points to -Y (the front); legs B and C point to azimuths 30 and 150 degrees. The rope drops
vertically on the Z axis from the head sheave, which turns in the plane x = 0.

Every component is a shape that can be cut, drilled, bent, welded or bought, and every joint has
a fixing (decided by Amish Chadha under his 2026-10-03 pre-approval, HTS-DDR-002):
    square aluminium legs that telescope (50 mm inside 60 mm) with a ball-lock pin, hinged to
    lug pairs under a steel head plate with M16 bolts through steel crush sleeves;
    the mast is a pair of steel cheek plates above the head plate that carries the 150 mm sheave
    high enough that the rope from the winch runs parallel to leg A and drops on the axis;
    steel feet with clevis plates, a rubber pad and an outer lug for the leg-spread chains;
    the winch bracket clamps round leg A and bears on a through stop bolt that takes the rope pull;
    every tool head carries the same 10 mm lifting tab (the published head interface).
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (HTS-CAL-001), cad/src/sheets.py (HTS-DWG-001), the concept media,
the build plan pictures and the appearance model. CONCEPT, NOT FOR FABRICATION.
"""
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

from build123d import (Box, Compound, Location, Plane, Pos, Rot, Solid, Vector, export_step,  # noqa: F401
                       export_stl)

ROOT = Path(__file__).resolve().parents[2]

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
    "FOOT_PLATE": (140.0, 280.0, 8.0), "PAD_T": 10.0, "CLEVIS_T": 8.0, "CHAIN_LUG_R": 140.0,
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

# Densities (kg/m3) for masses in HTS-CAL-001
RHO = {"steel": 7850.0, "alu": 2700.0, "hdpe": 960.0, "rubber": 1300.0, "pvc": 1400.0, "bought": 0.0}

CLEAT_S = 1700.0                                   # cleat position down leg B (mm)

# BOM line numbers (bom/bom.csv order)
BOM = {"feet": 1, "lower": 2, "upper": 3, "head": 4, "sheave": 5, "bolts": 6, "adj_pins": 7, "chains": 8,
       "bracket": 9, "winch": 10, "rope": 11, "counter": 12, "interface": 13, "snatch": 14, "guard": 15,
       "guard_pins": 16, "grab": 17, "sampler": 18, "rake": 19, "retrieval": 20, "domereach": 21}


# ------------------------------------------------------------------ helpers
def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def rod(p0, p1, r):
    """Solid cylinder of radius r from point p0 to point p1."""
    a, b = Vector(*p0), Vector(*p1)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def tube(p0, p1, ro, ri):
    return rod(p0, p1, ro) - rod(p0, p1, ri)


def sq_tube(w, t, s0, s1):
    """Square tube along -Z (leg-local), from s0 to s1 below the origin."""
    return box(-w / 2, w / 2, -w / 2, w / 2, -s1, -s0) - box(-w / 2 + t, w / 2 - t, -w / 2 + t, w / 2 - t, -s1 - 1, -s0 + 1)


def comp(shapes):
    return Compound(children=[s for s in shapes if s is not None])


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


@dataclass
class Comp:
    key: str
    name: str
    shape: object
    color: str
    bom: int | None
    explode: tuple = (0.0, 0.0, 0.0)
    material: str = "steel"
    make: str = "make"
    extra_kg: float = 0.0           # bought mass not represented by the solid (kg)

    @property
    def volume(self):
        return sum(s.volume for s in self.shape.solids())

    @property
    def mass(self):
        return self.volume * 1e-9 * RHO.get(self.material, 0.0) + self.extra_kg


# ------------------------------------------------------------------ tripod parts
def upper_leg(P=PARAMS, stop=False):
    """stop=True: leg A, with the cross hole for the winch bracket's stop bolt."""
    w, t, L = P["UP"]
    g = geometry(P)
    s0 = -P["END_HOLE"]
    leg = sq_tube(w, t, s0, s0 + L)
    if stop:
        leg -= rod((0, -w, -P["STOP_S"]), (0, w, -P["STOP_S"]), P["STOP_D"] / 2 + 0.5)
    for s in (0.0, g["adj_s"]):
        d = P["HOLE_D"] if s == 0 else P["ADJ_PIN_D"] + 1
        leg -= rod((-w, 0, -s), (w, 0, -s), d / 2)
    return leg


def upper_sleeve(P=PARAMS):
    w, t, _ = P["UP"]
    od, wall = P["SLEEVE"]
    return tube((-(w / 2 - t), 0, 0), (w / 2 - t, 0, 0), od / 2, od / 2 - wall)


def lower_leg(P=PARAMS, cleat_holes=False):
    """cleat_holes=True: leg B, with the two 7 mm holes for the cleat bolts."""
    w, t, L = P["LO"]
    g = geometry(P)
    leg = sq_tube(w, t, g["lo_top"], g["lo_top"] + L)
    leg -= rod((-w, 0, -g["Lp"]), (w, 0, -g["Lp"]), P["HOLE_D"] / 2)
    for k in range(P["ADJ_N"]):
        s = g["adj_s"] + (k - (P["ADJ_N"] - 1) / 2) * P["ADJ_PITCH"]
        leg -= rod((-w, 0, -s), (w, 0, -s), (P["ADJ_PIN_D"] + 1) / 2)
    if cleat_holes:
        for s in (CLEAT_S - 40, CLEAT_S + 40):
            leg -= rod((0, -w, -s), (0, w, -s), 3.5)
    return leg


def lower_sleeve(P=PARAMS):
    w, t, _ = P["LO"]
    g = geometry(P)
    od, wall = P["SLEEVE"]
    return tube((-(w / 2 - t), 0, -g["Lp"]), (w / 2 - t, 0, -g["Lp"]), od / 2, od / 2 - wall)


def adj_pin(P=PARAMS):
    g = geometry(P)
    d = P["ADJ_PIN_D"]
    s = g["adj_s"]
    return rod((-42, 0, -s), (42, 0, -s), d / 2) + rod((-50, 0, -s), (-42, 0, -s), 11) + rod((42, 0, -s), (47, 0, -s), 4)


def hinge_bolt(x_half, P=PARAMS, s=0.0):
    d = P["PIN_D"]
    return (rod((-x_half - 2, 0, -s), (x_half + 12, 0, -s), d / 2) + rod((-x_half - 12, 0, -s), (-x_half - 2, 0, -s), 13)
            + rod((x_half + 2, 0, -s), (x_half + 12, 0, -s), 13.5))


def head_plate(P=PARAMS):
    z0, t = P["HUB_Z0"], P["HUB_T"]
    plate = Pos(0, 0, z0 + t / 2) * Solid.make_cylinder(P["HUB_R"], t, Plane(origin=(0, 0, -t / 2)))
    plate -= rod((0, 0, z0 - 1), (0, 0, z0 + t + 1), P["CABLE_HOLE"] / 2)
    plate -= rod((0, 95, z0 - 1), (0, 95, z0 + t + 1), 6.5)            # eye bolt for the snatch block
    parts = [plate]
    xo = P["UP"][0] / 2 + P["LUG_GAP"]
    for phi in P["LEG_AZ"]:
        for sx in (-1, 1):
            x0 = sx * xo
            x1 = sx * (xo + P["LUG_T"])
            lug = box(min(x0, x1), max(x0, x1), P["R_HUB"] - P["LUG_HALF"], P["R_HUB"] + P["LUG_HALF"],
                      P["PIN_Z"] - P["LUG_HALF"], z0)
            lug -= rod((-80, P["R_HUB"], P["PIN_Z"]), (80, P["R_HUB"], P["PIN_Z"]), P["HOLE_D"] / 2)
            parts.append(radial(phi) * lug)
    # mast: two cheek plates with the axle hole, stiffened by a spacer that is also the rope keeper
    g = geometry(P)
    rp, rf = P["SHEAVE"][1], P["SHEAVE"][0]
    y0, y1 = P["CHEEK_Y"]
    for sx in (-1, 1):
        x0, x1 = sx * P["CHEEK_X"], sx * (P["CHEEK_X"] + P["CHEEK_T"])
        ch = box(min(x0, x1), max(x0, x1), y0, y1, z0 + t, P["CHEEK_TOP"])
        ch -= rod((-60, -rp, g["zs"]), (60, -rp, g["zs"]), P["AXLE_D"] / 2 + 0.5)
        parts.append(ch)
    parts.append(rod((-P["CHEEK_X"], -rp, g["zs"] + rf + 10), (P["CHEEK_X"], -rp, g["zs"] + rf + 10), 6))
    # cheek gusset across the back (inner edge, clear of the rope), welded to the plate
    parts.append(box(-P["CHEEK_X"], P["CHEEK_X"], y1 - 8, y1, z0 + t, z0 + t + 120))
    return comp(parts)


def sheave(P=PARAMS):
    g = geometry(P)
    rf, rp, w = P["SHEAVE"]
    y, z = -rp, g["zs"]
    core = rod((-w / 2 + 4, y, z), (w / 2 - 4, y, z), rp - P["ROPE_D"] / 2)
    fl = rod((-w / 2, y, z), (-w / 2 + 4, y, z), rf) + rod((w / 2 - 4, y, z), (w / 2, y, z), rf)
    hub = rod((-w / 2, y, z), (w / 2, y, z), 22)
    s = (core + fl + hub) - rod((-w, y, z), (w, y, z), P["AXLE_D"] / 2 + 0.5)
    xe = P["CHEEK_X"] + P["CHEEK_T"]
    axle = rod((-xe - 3, y, z), (xe + 14, y, z), P["AXLE_D"] / 2) + rod((-xe - 13, y, z), (-xe - 3, y, z), 16) \
        + rod((xe + 2, y, z), (xe + 14, y, z), 16.5)
    washers = rod((-P["CHEEK_X"], y, z), (-w / 2, y, z), 16) + rod((w / 2, y, z), (P["CHEEK_X"], y, z), 16)
    washers -= rod((-60, y, z), (60, y, z), P["AXLE_D"] / 2)
    return s, axle + washers


def foot(P=PARAMS):
    px, py, pt = P["FOOT_PLATE"]
    R, zp = P["R_FOOT"], P["FOOT_PIN_Z"]
    pad = box(-px / 2, px / 2, R - py / 2, R + py / 2, 0, P["PAD_T"])
    z1 = P["PAD_T"] + pt
    plate = box(-px / 2, px / 2, R - py / 2, R + py / 2, P["PAD_T"], z1)
    xo = P["LO"][0] / 2 + 1
    parts = [plate]
    for sx in (-1, 1):
        x0, x1 = sx * xo, sx * (xo + P["CLEVIS_T"])
        cl = box(min(x0, x1), max(x0, x1), R - 50, R + 50, z1, zp + 28)
        cl -= rod((-80, R, zp), (80, R, zp), P["HOLE_D"] / 2)
        parts.append(cl)
    lug = box(-4, 4, R + 60, R + py / 2 + 20, z1, z1 + 45)
    lug -= rod((-10, R + P["CHAIN_LUG_R"], z1 + 22), (10, R + P["CHAIN_LUG_R"], z1 + 22), 7)
    parts.append(lug)
    return comp(parts), pad


def chain_point(phi, P=PARAMS):
    R = P["R_FOOT"] + P["CHAIN_LUG_R"]
    z = P["PAD_T"] + P["FOOT_PLATE"][2] + 22
    a = math.radians(phi)
    return (R * math.cos(a), R * math.sin(a), z)


def chains(P=PARAMS):
    out = []
    az = P["LEG_AZ"]
    for i in range(3):
        a, b = chain_point(az[i], P), chain_point(az[(i + 1) % 3], P)
        d = Vector(*b) - Vector(*a)
        u = d.normalized()
        a2, b2 = Vector(*a) + u * 28, Vector(*b) - u * 28   # shackle at each lug
        out.append(rod(tuple(a2), tuple(b2), P["CHAIN_D"]))       # chain envelope, 12 mm wide
    return comp(out)


def bracket(P=PARAMS):
    """Winch bracket in leg A's frame: front plate, back clamp plate, four M10 clamp bolts, stop bolt."""
    s0, s1 = P["BRACKET_S"]
    w, t = P["UP"][0] / 2, P["BRACKET_T"]
    front = box(-60, 60, w, w + t, -s1, -s0)
    back = box(-60, 60, -w - t, -w, -s1, -s0)
    bolts = []
    for sx in (-1, 1):
        for s in (s0 + 22, s1 - 22):
            hole = rod((sx * P["CLAMP_X"], -w - t - 1, -s), (sx * P["CLAMP_X"], w + t + 1, -s), P["CLAMP_BOLT_D"] / 2 + 0.5)
            front -= hole
            back -= hole
            bolts.append(rod((sx * P["CLAMP_X"], -w - t - 8, -s), (sx * P["CLAMP_X"], w + t + 10, -s), P["CLAMP_BOLT_D"] / 2))
    stop = rod((0, -w - 14, -P["STOP_S"]), (0, w + 14, -P["STOP_S"]), P["STOP_D"] / 2)
    return comp([front, back]), comp(bolts + [stop])


def winch_body(P=PARAMS):
    """Bought hand winch with automatic load brake (envelope), in leg A's frame on the bracket."""
    w, t = P["UP"][0] / 2, P["BRACKET_T"]
    yb = w + t
    sd, yd, rd = P["DRUM_S"], P["DRUM_Y"], P["DRUM_R"]
    base = box(-55, 55, yb, yb + 8, -(sd + 95), -(sd - 95))
    sides = box(-59, -55, yb + 8, yd + 72, -(sd + 80), -(sd - 80)) + box(55, 59, yb + 8, yd + 72, -(sd + 80), -(sd - 80))
    drum = rod((-55, yd, -sd), (55, yd, -sd), rd)
    fl = rod((-55, yd, -sd), (-51, yd, -sd), P["DRUM_FL"]) + rod((51, yd, -sd), (55, yd, -sd), P["DRUM_FL"])
    gear = box(59, 78, yb + 50, yd + 60, -(sd + 70), -(sd - 50))
    shaft = rod((59, yb + 70, -(sd + 40)), (100, yb + 70, -(sd + 40)), 9)
    arm = box(92, 102, yb + 60, yb + 80, -(sd + 290), -(sd + 30))
    grip = rod((102, yb + 70, -(sd + 280)), (215, yb + 70, -(sd + 280)), 15)
    body = comp([base, sides, fl, gear, shaft, arm, grip])
    rope_on_drum = rod((-50, yd, -sd), (50, yd, -sd), P["ROPE_LAYER_R"]) - rod((-60, yd, -sd), (60, yd, -sd), rd)
    return body, rope_on_drum


def line_counter(P=PARAMS):
    w, t = P["UP"][0] / 2, P["BRACKET_T"]
    y = P["ROPE_OFFSET"]
    sd = P["DRUM_S"]
    body = box(-22, 22, y + 5, y + 40, -(sd - 105), -(sd - 75)) + box(-22, 22, y - 40, y - 5, -(sd - 105), -(sd - 75))
    stand = box(-22, 22, w + t, y - 40, -(sd - 100), -(sd - 80))
    return body + stand


def rope_path(P=PARAMS, hook_z=None):
    """Rope from the drum up leg A to the sheave, and the vertical drop to the head interface."""
    g = geometry(P)
    rp = P["SHEAVE"][1]
    a = leg_point(P["LEG_AZ"][0], P["DRUM_S"], P["ROPE_OFFSET"], P)
    # tangent point on the sheave: centre + rp * outer normal of leg A
    c_y, c_z = -rp, g["zs"]
    t_y, t_z = c_y - rp * g["cos"], c_z + rp * g["sin"]
    r = P["ROPE_D"] / 2
    up = rod(a, (0, t_y, t_z), r)
    # wrap over the sheave as short straight pieces
    wrap = []
    a0 = math.atan2(t_z - c_z, t_y - c_y)
    pts = [(0, c_y + rp * math.cos(a0 + (0 - a0) * k / 8), c_z + rp * math.sin(a0 + (0 - a0) * k / 8)) for k in range(9)]
    for p0, p1 in zip(pts[:-1], pts[1:]):
        wrap.append(rod(p0, p1, r))
    drop = rod((0, 0, g["zs"]), (0, 0, (P["HOOK_Z"] if hook_z is None else hook_z) + 190), r)
    return comp([up, drop] + wrap)


def interface(z, P=PARAMS):
    """Head interface at shackle pin height z: screw-pin bow shackle, swivel, thimble eye (bought)."""
    r = 5.5
    pin = rod((0, -22, z), (0, 22, z), r)
    legs = rod((0, -13.5, z), (0, -13.5, z + 45), r) + rod((0, 13.5, z), (0, 13.5, z + 45), r)
    crown = rod((0, -19, z + 45), (0, 19, z + 45), r)
    swivel = rod((0, 0, z + 51), (0, 0, z + 140), 12)
    eye = rod((0, 0, z + 140), (0, 0, z + 190), 8)
    return comp([pin, legs, crown, swivel, eye])


def snatch_block(P=PARAMS):
    z0 = P["HUB_Z0"]
    eye = rod((0, 95, z0 - 45), (0, 95, z0 + P["HUB_T"] + 10), 6)
    body = rod((-14, 95, z0 - 95), (14, 95, z0 - 95), 38)
    hook = box(-6, 6, 85, 105, z0 - 60, z0 - 45)
    return comp([eye, body, hook])


def cleat(P=PARAMS):
    """Bought cleat on leg B's lower leg (leg frame), with two M6 through bolts."""
    s = CLEAT_S
    w = P["LO"][0] / 2
    base = box(-14, 14, w, w + 10, -(s + 75), -(s - 75))
    horns = box(-10, 10, w + 10, w + 30, -(s + 70), -(s - 70))
    bolts = rod((0, -w - 6, -(s - 40)), (0, w + 12, -(s - 40)), 3) + rod((0, -w - 6, -(s + 40)), (0, w + 12, -(s + 40)), 3)
    return base + horns + bolts


# ------------------------------------------------------------------ rim guard
def guard_panel(P=PARAMS):
    """One rim guard panel in the radial frame (normal along +Y), frame centre line at GUARD_R."""
    R, H = P["GUARD_R"], P["GUARD_H"]
    a, tw = P["GUARD_TUBE"]
    half = R * math.tan(math.radians(30)) - P["GUARD_SETBACK"]
    y0, y1 = R - a / 2, R + a / 2

    def rect_tube_x(x0, x1, z0):
        return box(x0, x1, y0, y1, z0, z0 + a) - box(x0 - 1, x1 + 1, y0 + tw, y1 - tw, z0 + tw, z0 + a - tw)

    def rect_tube_z(x0, z0, z1):
        return box(x0, x0 + a, y0, y1, z0, z1) - box(x0 + tw, x0 + a - tw, y0 + tw, y1 - tw, z0 - 1, z1 + 1)

    frame = [rect_tube_x(-half + a, half - a, 0), rect_tube_x(-half + a, half - a, H - a),
             rect_tube_z(-half, 0, H), rect_tube_z(half - a, 0, H)]
    board = box(-half + a, half - a, y0 - P["BOARD_T"], y0, a + 5, H - a - 70)
    xc = R * math.tan(math.radians(30))
    od, idd, h = P["RING"]
    rings = []
    for x_end, zs in ((xc, (40.0, 300.0)), (-xc, (75.0, 335.0))):
        sx = 1 if x_end > 0 else -1
        for z in zs:
            ring = tube((x_end, R, z), (x_end, R, z + h), od / 2, idd / 2)
            lug = box(min(sx * half, sx * (xc - od / 2 + 3)), max(sx * half, sx * (xc - od / 2 + 3)), R - 4, R + 4, z, z + h)
            rings += [ring, lug]
    return comp(frame + rings), board


def guard_pins(P=PARAMS):
    R = P["GUARD_R"]
    rc = R / math.cos(math.radians(30))
    out = []
    for k in range(6):
        a = math.radians(P["LEG_AZ"][0] + 30 + 60 * k)
        x, y = rc * math.cos(a), rc * math.sin(a)
        out.append(rod((x, y, 30), (x, y, P["GUARD_H"] + 30), (P["RING"][1] - 2) / 2)
                   + rod((x - 30, y, P["GUARD_H"] + 30), (x + 30, y, P["GUARD_H"] + 30), 5))
    return comp(out)


def guard_azimuths(P=PARAMS):
    return [P["LEG_AZ"][0] + 60 * k for k in range(6)]


# ------------------------------------------------------------------ tool heads (local: tab hole at origin)
def tab(P=PARAMS, z_bot=None):
    w, t, d, below, h = P["TAB"]
    zb = -(h - below) if z_bot is None else z_bot
    s = box(-w / 2, w / 2, -t / 2, t / 2, zb, below)
    return s - rod((0, -t, 0), (0, t, 0), d / 2)


def grab_parts(P=PARAMS):
    """Clamshell grab, closed. Returns dict of name: shape. Hinge pin along Y."""
    R, B = P["GRAB_R"], P["GRAB_B"]
    ts, tp = P["GRAB_SHEET"], P["GRAB_PLATE"]
    xh = P["GRAB_HEAD_X"]
    z_head_pin = -92.0
    ear_x, ear_dz = R - 30, 35.0
    z_h = z_head_pin - math.sqrt(P["GRAB_ROD"] ** 2 - (ear_x - xh) ** 2) - ear_dz
    hb = B / 2
    out = {}
    for side, sx, (p0, p1) in (("left", -1, (hb, hb + tp)), ("right", 1, (hb + tp + 1, hb + 2 * tp + 1))):
        ylen = hb if sx < 0 else hb + tp + 1
        cyl_o = rod((0, -ylen, z_h), (0, ylen, z_h), R)
        cyl_i = rod((0, -ylen - 1, z_h), (0, ylen + 1, z_h), R - ts)
        quad = box(min(0, sx * R), max(0, sx * R), -ylen - 2, ylen + 2, z_h - R, z_h)
        shell = (cyl_o - cyl_i) & quad
        cover = box(min(sx * R * 0.5, sx * (R - ts)), max(sx * R * 0.5, sx * (R - ts)), -ylen, ylen, z_h - ts, z_h)
        plates = []
        for sy in (-1, 1):
            ya, yb = sy * p0, sy * p1
            y_lo, y_hi = min(ya, yb), max(ya, yb)
            disc = rod((0, y_lo, z_h), (0, y_hi, z_h), R) & box(min(0, sx * R), max(0, sx * R), y_lo - 1, y_hi + 1, z_h - R, z_h)
            ear = box(min(sx * (R - 55), sx * R), max(sx * (R - 55), sx * R), y_lo, y_hi, z_h - 5, z_h + ear_dz + 22)
            boss = rod((0, y_lo, z_h), (0, y_hi, z_h), 35)
            pl = disc + ear + boss
            pl -= rod((0, y_lo - 1, z_h), (0, y_hi + 1, z_h), P["GRAB_PIN"] / 2 + 0.5)
            pl -= rod((sx * ear_x, y_lo - 1, z_h + ear_dz), (sx * ear_x, y_hi + 1, z_h + ear_dz), 6.5)
            plates.append(pl)
        out[f"shell_{side}"] = comp([shell, cover] + plates)
    # closing yoke: two flat bars on the hinge pin, crossbar and closing-line eye
    yk0 = hb + 2 * tp + 3
    bars = []
    for sy in (-1, 1):
        y_lo, y_hi = sorted((sy * yk0, sy * (yk0 + 6)))
        b_ = box(-25, 25, y_lo, y_hi, z_h - 30, z_h + 300)
        b_ -= rod((0, y_lo - 1, z_h), (0, y_hi + 1, z_h), P["GRAB_PIN"] / 2 + 0.5)
        bars.append(b_)
    cross = box(-25, 25, -(yk0 + 6), yk0 + 6, z_h + 300, z_h + 310)
    eye = box(-5, 5, 20, 60, z_h + 310, z_h + 350) - rod((-10, 40, z_h + 332), (10, 40, z_h + 332), 7)
    out["yoke"] = comp(bars + [cross, eye])
    out["hinge_pin"] = rod((0, -(yk0 + 12), z_h), (0, yk0 + 12, z_h), P["GRAB_PIN"] / 2)
    # tag rods: 30 x 6 flat bar from each ear pin to the head beam lugs
    yr0 = yk0 + 8
    rods_, pins = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            y_lo, y_hi = sorted((sy * yr0, sy * (yr0 + 6)))
            a = Vector(sx * ear_x, 0, z_h + ear_dz)
            b = Vector(sx * xh, 0, z_head_pin)
            d = b - a
            L = d.length
            ang = math.degrees(math.atan2(d.X, d.Z))
            bar = Pos(a.X, (y_lo + y_hi) / 2, a.Z) * Rot(0, ang, 0) * box(-15, 15, -(y_hi - y_lo) / 2, (y_hi - y_lo) / 2, -15, L + 15)
            bar -= rod((a.X, y_lo - 1, a.Z), (a.X, y_hi + 1, a.Z), 6.5)
            bar -= rod((b.X, y_lo - 1, b.Z), (b.X, y_hi + 1, b.Z), 6.5)
            rods_.append(bar)
        pe = (hb if sx < 0 else hb + tp + 1)
        pins.append(rod((sx * ear_x, -(yr0 + 12), z_h + ear_dz), (sx * ear_x, yr0 + 12, z_h + ear_dz), 6))
        pins.append(rod((sx * xh, -(yr0 + 20), z_head_pin), (sx * xh, yr0 + 20, z_head_pin), 6))
        _ = pe
    out["tag_rods"] = comp(rods_)
    out["pins"] = comp(pins)
    # head beam: 12 mm plate, four lugs, closing-line hole, the standard tab
    yl0 = yr0 + 7
    plate = box(-80, 80, -(yl0 + 8), yl0 + 8, -70, -60) - rod((0, 40, -80), (0, 40, -50), 15)
    lugs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            y_lo, y_hi = sorted((sy * yl0, sy * (yl0 + 8)))
            lg = box(min(sx * 40, sx * 80), max(sx * 40, sx * 80), y_lo, y_hi, -112, -70)
            lg -= rod((sx * xh, y_lo - 1, z_head_pin), (sx * xh, y_hi + 1, z_head_pin), 6.5)
            lugs.append(lg)
    out["head_beam"] = comp([plate, tab(P, -60)] + lugs)
    out["_z_h"] = z_h
    return out


def grab(P=PARAMS):
    d = grab_parts(P)
    return comp([v for k, v in d.items() if not k.startswith("_")])


def sampler(P=PARAMS):
    od, wall, L = P["SAMP_TUBE"]
    rc = P["SAMP_CAGE_R"]
    D = P["SAMP_PLATE_D"]
    top = rod((0, 0, -66), (0, 0, -60), D / 2) - rod((0, 0, -70), (0, 0, -50), 16)
    bot = rod((0, 0, -766), (0, 0, -760), D / 2) - rod((0, 0, -770), (0, 0, -750), 50)
    bo, bi, bh = P["SAMP_BALLAST"]
    ballast = rod((0, 0, -766 - bh), (0, 0, -766), bo / 2) - rod((0, 0, -770 - bh), (0, 0, -760), bi / 2)
    rods_ = [rod((rc * math.cos(math.radians(a)), rc * math.sin(math.radians(a)), -760),
                 (rc * math.cos(math.radians(a)), rc * math.sin(math.radians(a)), -66), 5) for a in (45, 135, 225, 315)]
    tube_ = tube((0, 0, -120 - L), (0, 0, -120), od / 2, od / 2 - wall)
    clamps = [rod((0, 0, z), (0, 0, z + 20), rc + 5) - rod((0, 0, z - 1), (0, 0, z + 21), od / 2) for z in (-260, -620)]
    caps = rod((0, 0, -120), (0, 0, -110), 45) + rod((0, 0, -120 - L - 10), (0, 0, -120 - L), 45)
    latch = box(-8, 8, 30, 58, -110, -66) + box(-8, 8, 30, 70, -100, -92)
    return {"frame": comp([top, bot, ballast, tab(P, -60)] + rods_ + clamps), "tube": tube_, "caps": caps + latch}


def rake(P=PARAMS):
    W = P["RAKE_W"]
    d, L = P["RAKE_TINE"]
    bar = box(-W / 2, W / 2, -6, 6, -460, -410) - rod((0, -10, -435), (0, 10, -435), 8)
    ballast = box(-W / 2 + 10, W / 2 - 10, -20, 20, -410, -370)
    tines = [rod((-W / 2 + 20 + k * (W - 40) / (P["RAKE_TINES"] - 1), 0, -460 - L),
                 (-W / 2 + 20 + k * (W - 40) / (P["RAKE_TINES"] - 1), 0, -460), d / 2) for k in range(P["RAKE_TINES"])]
    bails = []
    for sx in (-1, 1):
        a = Vector(sx * (W / 2 - 25), 0, -370)
        b = Vector(sx * 22, 0, -72)
        dv = b - a
        ang = math.degrees(math.atan2(dv.X, dv.Z))
        bails.append(Pos(a.X, 0, a.Z) * Rot(0, ang, 0) * box(-20, 20, -4, 4, 0, dv.length))
    top = box(-45, 45, -20, 20, -72, -60)
    drag = box(-6, 6, -45, -6, -455, -415) - rod((-10, -30, -435), (10, -30, -435), 8)
    return comp([bar, ballast, top, tab(P, -60), drag] + tines + bails)


def retrieval(P=PARAMS):
    D, T, H = P["RET_D"], P["RET_THROAT"], P["RET_DEPTH"]
    disc = rod((0, 0, -66), (0, 0, -60), D / 2) - rod((0, 0, -70), (0, 0, -50), T / 2 - 10)
    outer = Solid.make_cone(D / 2, T / 2, H, Plane(origin=(0, 0, -66), z_dir=(0, 0, -1)))
    inner = Solid.make_cone(D / 2 - 2.5, T / 2 - 2.5, H + 0.1, Plane(origin=(0, 0, -65.95), z_dir=(0, 0, -1)))
    funnel = outer - inner
    socket = tube((D / 2 - 30, 0, -60), (D / 2 - 30, 0, 90), 16.85, 13.65)
    gusset = box(D / 2 - 50, D / 2 - 14, -4, 4, -60, 0)
    sling = rod((0, 0, -66 - H - 30), (0, 0, -66), 5)
    hook = box(-55, 55, -11, 11, -66 - H - 90, -66 - H - 30) - box(-35, 35, -12, 12, -66 - H - 75, -66 - H - 45)
    return {"frame": comp([disc, funnel, socket, gusset, tab(P, -60)]), "connector": comp([sling, hook])}


def domereach(P=PARAMS):
    od, wall, Ls = P["DR_POLE"]
    top = -30.0
    upper = tube((0, 0, top - Ls), (0, 0, top), od / 2, od / 2 - wall)
    lower = tube((0, 0, top - 2 * Ls), (0, 0, top - Ls), od / 2, od / 2 - wall)
    joint = tube((0, 0, top - Ls - 80), (0, 0, top - Ls + 80), od / 2 + 4, od / 2 + 0.5)
    cap = rod((0, 0, top), (0, 0, top + 8), od / 2) + tab(P, top + 8)
    tod, tlen, tbelow = P["DR_TILLER"]
    collar = tube((0, 0, -tbelow - 30), (0, 0, -tbelow + 30), od / 2 + 6, od / 2 + 0.5)
    tiller = rod((0, -tlen / 2, -tbelow), (0, -od / 2 - 4, -tbelow), tod / 2) + rod((0, od / 2 + 4, -tbelow), (0, tlen / 2, -tbelow), tod / 2)
    zb = top - 2 * Ls
    clev = box(-28, 28, od / 2 - 2, od / 2 + 6, zb - 90, zb + 60) + box(-28, 28, -od / 2 - 6, -od / 2 + 2, zb - 90, zb + 60)
    clev = clev - rod((0, -40, zb - 60), (0, 40, zb - 60), 6.5)
    plug = rod((0, 0, zb), (0, 0, zb + 60), od / 2 - wall)
    fair = tube((0, 0, top - 500 - 15), (0, 0, top - 500 + 15), od / 2 + 12, od / 2 + 0.5) + tube((od / 2 + 14, 0, top - 500 - 6), (od / 2 + 14, 0, top - 500 + 6), 10, 6)
    aw, at, aL = P["DR_ARM"]
    ang = P["DR_ARM_DEG"]
    hinge = Vector(0, 0, zb - 60)
    arm = Pos(hinge.X, 0, hinge.Z) * Rot(0, ang, 0) * (box(-aw / 2, aw / 2, -aw / 2, aw / 2, -15, aL)
                                                      - box(-aw / 2 + at, aw / 2 - at, -aw / 2 + at, aw / 2 - at, -16, aL + 1))
    arm_pin = rod((0, -40, zb - 60), (0, 40, zb - 60), 6)
    tip = hinge + Vector(math.sin(math.radians(ang)), 0, math.cos(math.radians(ang))) * (aL + 30)
    rd, rw = P["DR_ROLLER"]
    fork = Pos(tip.X, 0, tip.Z) * Rot(0, ang, 0) * (box(-6, 6, -rw / 2 - 14, rw / 2 + 14, -45, 0))
    roller = rod((tip.X + 30 * math.sin(math.radians(ang)), -rw / 2, tip.Z + 30 * math.cos(math.radians(ang))),
                 (tip.X + 30 * math.sin(math.radians(ang)), rw / 2, tip.Z + 30 * math.cos(math.radians(ang))), rd / 2)
    return {"pole": comp([upper, lower, joint, cap, plug, fair]), "tiller": comp([collar, tiller]),
            "arm": comp([clev, arm, arm_pin, fork]), "roller": roller}


# ------------------------------------------------------------------ assembly
COL = {"foot": "#4B5563", "pad": "#1F2937", "lower": "#B8C0C8", "upper": "#9AA4AE", "sleeve": "#6B7280",
       "head": "#0F766E", "sheave": "#D97706", "bolt": "#111827", "chain": "#78716C", "bracket": "#374151",
       "winch": "#B91C1C", "rope": "#57534E", "counter": "#1D4ED8", "iface": "#CA8A04", "snatch": "#7C3AED",
       "guard": "#E8B517", "board": "#F3F4F6", "gpin": "#111827", "grab": "#0E7490", "grab2": "#155E75",
       "yoke": "#C2410C", "samp": "#0369A1", "samp_tube": "#BAE6FD", "rake": "#4D7C0F", "ret": "#BE185D",
       "dr": "#6D28D9", "dr2": "#A78BFA", "cleat": "#334155"}

HEAD_SPOTS = {"sampler": (1800, -600, 0), "rake": (-1850, 450, 0), "retrieval": (-1800, -750, 0),
              "domereach": (0, -2000, 0)}


def components(P=PARAMS, heads=True, hook_z=None):
    """Every component of the prototype, in build order, positioned as assembled.
    With heads=True the sampler, rake, retrieval head and DomeReach head stand on the ground beside
    the tripod (HEAD_SPOTS); the grab hangs on the rope."""
    g = geometry(P)
    hz = P["HOOK_Z"] if hook_z is None else hook_z
    az = P["LEG_AZ"]
    C = []
    ft, pad = foot(P)
    C.append(Comp("feet", "Feet with clevis and chain lug (3)", comp([radial(a) * ft for a in az]), COL["foot"],
                  BOM["feet"], (0, 0, -250)))
    C.append(Comp("pads", "Rubber foot pads (3)", comp([radial(a) * pad for a in az]), COL["pad"], BOM["feet"],
                  (0, 0, -400), "rubber"))
    C.append(Comp("lower", "Lower legs, 50 mm square aluminium (3)", comp([leg_frame(a) * lower_leg(P, a == az[1]) for a in az]),
                  COL["lower"], BOM["lower"], (0, 0, -120), "alu"))
    C.append(Comp("lower_sleeves", "Foot crush sleeves (3)", comp([leg_frame(a) * lower_sleeve(P) for a in az]),
                  COL["sleeve"], BOM["lower"], (0, 0, -120)))
    C.append(Comp("upper", "Upper legs, 60 mm square aluminium (3)", comp([leg_frame(a) * upper_leg(P, a == az[0]) for a in az]),
                  COL["upper"], BOM["upper"], (0, 0, 150), "alu"))
    C.append(Comp("upper_sleeves", "Hinge crush sleeves (3)", comp([leg_frame(a) * upper_sleeve(P) for a in az]),
                  COL["sleeve"], BOM["upper"], (0, 0, 150)))
    C.append(Comp("head", "Tripod head with mast cheeks", head_plate(P), COL["head"], BOM["head"], (0, 0, 600)))
    shv, axle = sheave(P)
    C.append(Comp("sheave", "Head sheave, 150 mm", shv, COL["sheave"], BOM["sheave"], (0, 0, 900), "bought",
                  "buy", 1.2))
    C.append(Comp("axle", "Sheave axle bolt M20 and washers", axle, COL["bolt"], BOM["sheave"], (350, 0, 900)))
    hb = [leg_frame(a) * hinge_bolt(P["UP"][0] / 2 + P["LUG_GAP"] + P["LUG_T"], P) for a in az]
    fb = [leg_frame(a) * hinge_bolt(P["LO"][0] / 2 + 1 + P["CLEVIS_T"], P, g["Lp"]) for a in az]
    C.append(Comp("hinge_bolts", "Leg hinge bolts M16 (3)", comp(hb), COL["bolt"], BOM["bolts"], (0, 0, 450)))
    C.append(Comp("foot_bolts", "Foot bolts M16 (3)", comp(fb), COL["bolt"], BOM["bolts"], (0, 0, -250)))
    C.append(Comp("adj_pins", "Leg adjust pins, ball-lock 12 mm (3)", comp([leg_frame(a) * adj_pin(P) for a in az]),
                  COL["bolt"], BOM["adj_pins"], (0, 0, 0)))
    C.append(Comp("chains", "Leg-spread chains (3)", chains(P), COL["chain"], BOM["chains"], (0, 0, -550), "bought",
                  "buy", 3 * 2.78 * 0.8))
    br, bb = bracket(P)
    LA = leg_frame(az[0])
    C.append(Comp("bracket", "Winch bracket and clamp plate", LA * br, COL["bracket"], BOM["bracket"],
                  (0, -350 * g["cos"], 350 * g["sin"])))
    C.append(Comp("bracket_bolts", "Clamp bolts M10 and stop bolt M12", LA * bb, COL["bolt"], BOM["bracket"],
                  (0, -250 * g["cos"], 250 * g["sin"])))
    wb, wr = winch_body(P)
    C.append(Comp("winch", "Hand winch, 450 kg, automatic brake", LA * wb, COL["winch"], BOM["winch"],
                  (0, -650 * g["cos"], 650 * g["sin"]), "bought", "buy", 9.0))
    C.append(Comp("counter", "Line length counter", LA * line_counter(P), COL["counter"], BOM["counter"],
                  (0, -800 * g["cos"], 800 * g["sin"]), "bought", "buy", 0.6))
    C.append(Comp("rope", "Wire rope, 6 mm stainless, 15 m", comp([rope_path(P, hz), LA * wr]), COL["rope"], BOM["rope"],
                  (0, 0, 0), "bought", "buy", 2.3))
    C.append(Comp("interface", "Head interface: swivel and shackle", interface(hz, P), COL["iface"], BOM["interface"],
                  (0, 0, 250), "bought", "buy", 0.5))
    C.append(Comp("snatch", "Snatch block for the working line", snatch_block(P), COL["snatch"], BOM["snatch"],
                  (0, 300, 600), "bought", "buy", 0.9))
    C.append(Comp("cleat", "Working line cleat on leg B", leg_frame(az[1]) * cleat(P), COL["cleat"], BOM["snatch"],
                  (500, 300, 0), "bought", "buy", 0.3))
    gp, bd = guard_panel(P)
    gaz = guard_azimuths(P)
    C.append(Comp("guard", "Rim guard panels (6)", comp([radial(a) * gp for a in gaz]), COL["guard"], BOM["guard"],
                  (0, 0, 0), "alu"))
    C.append(Comp("boards", "Rim guard splash boards, HDPE (6)", comp([radial(a) * bd for a in gaz]), COL["board"],
                  BOM["guard"], (0, 0, 0), "hdpe"))
    C.append(Comp("guard_pins", "Rim guard drop pins (6)", guard_pins(P), COL["gpin"], BOM["guard_pins"], (0, 0, 500)))
    gr = grab_parts(P)
    gl = Pos(0, 0, hz)
    C.append(Comp("grab_shells", "Grab shells (2)", comp([gl * gr["shell_left"], gl * gr["shell_right"]]), COL["grab"],
                  BOM["grab"], (0, 0, -300)))
    C.append(Comp("grab_yoke", "Grab closing yoke and hinge pin", comp([gl * gr["yoke"], gl * gr["hinge_pin"]]),
                  COL["yoke"], BOM["grab"], (0, 0, -150)))
    C.append(Comp("grab_frame", "Grab head beam, tag rods and pins",
                  comp([gl * gr["head_beam"], gl * gr["tag_rods"], gl * gr["pins"]]), COL["grab2"], BOM["grab"],
                  (0, 0, 0)))
    if heads:
        s = sampler(P)
        L_s = Pos(*HEAD_SPOTS["sampler"]) * Pos(0, 0, 806)
        C.append(Comp("sampler", "Sampler head", comp([L_s * s["frame"], L_s * s["caps"]]), COL["samp"],
                      BOM["sampler"], (300, 0, 0)))
        C.append(Comp("sampler_tube", "Sampler tube, clear PVC", L_s * s["tube"], COL["samp_tube"], BOM["sampler"],
                      (300, 0, 0), "pvc"))
        L_r = Pos(*HEAD_SPOTS["rake"]) * Pos(0, 0, 460 + P["RAKE_TINE"][1])
        C.append(Comp("rake", "Rake head", L_r * rake(P), COL["rake"], BOM["rake"], (300, 0, 0)))
        r = retrieval(P)
        L_t = Pos(*HEAD_SPOTS["retrieval"]) * Pos(0, 0, 66 + P["RET_DEPTH"] + 90)
        C.append(Comp("retrieval", "Retrieval head", L_t * r["frame"], COL["ret"], BOM["retrieval"], (-300, 0, 0)))
        C.append(Comp("connector", "Auto-locking connector on sling", L_t * r["connector"], COL["bolt"],
                      BOM["retrieval"], (-300, 0, 0), "bought", "buy", 0.4))
        d = domereach(P)
        # laid on the ground for display along X, top to the left, arm swung up 45 degrees
        zb = -30 - 2 * P["DR_POLE"][2] - 60
        L_d = Pos(*HEAD_SPOTS["domereach"]) * Pos(zb / 2, 0, P["DR_POLE"][0] / 2 + 13) * Rot(0, -90, 0)
        C.append(Comp("dr_pole", "DomeReach pole and tiller", comp([L_d * d["pole"], L_d * d["tiller"]]), COL["dr"],
                      BOM["domereach"], (-300, 0, 0), "alu"))
        C.append(Comp("dr_arm", "DomeReach arm and clevis", L_d * d["arm"], COL["dr2"], BOM["domereach"], (-300, 0, 0),
                      "alu"))
        C.append(Comp("dr_roller", "DomeReach sealant roller", L_d * d["roller"], COL["board"], BOM["domereach"],
                      (-300, 0, 0), "bought", "buy", 0.3))
    return C


def head_comps(P=PARAMS):
    """Each tool head on its own (local frame, tab hole at the origin) for its STEP and sheet."""
    gr = grab_parts(P)
    s, r, d = sampler(P), retrieval(P), domereach(P)
    return {"grab": comp([v for k, v in gr.items() if not k.startswith("_")]),
            "sampler": comp([s["frame"], s["tube"], s["caps"]]), "rake": rake(P),
            "retrieval": comp([r["frame"], r["connector"]]),
            "domereach": comp([d["pole"], d["tiller"], d["arm"], d["roller"]])}


def assembly(P=PARAMS, heads=False):
    return Compound(children=[c.shape for c in components(P, heads=heads)])


# ------------------------------------------------------------------ checks
def _overlap(a, b):
    """Interference volume, solid by solid with a bounding-box prefilter (compound booleans can
    return false slivers)."""
    tot = 0.0
    for sa in a.solids():
        ba = sa.bounding_box()
        for sb in b.solids():
            bb_ = sb.bounding_box()
            if (ba.min.X > bb_.max.X or bb_.min.X > ba.max.X or ba.min.Y > bb_.max.Y or bb_.min.Y > ba.max.Y
                    or ba.min.Z > bb_.max.Z or bb_.min.Z > ba.max.Z):
                continue
            try:
                r = sa & sb
                tot += r.volume if r is not None else 0.0
            except Exception:
                return float("nan")
    return tot


def checks(P=PARAMS):
    """Constructability checks: interference between neighbours, clearances, envelope."""
    g = geometry(P)
    C = {c.key: c for c in components(P, heads=False)}
    pairs = [("upper", "lower"), ("upper", "head"), ("lower", "feet"), ("upper", "hinge_bolts"), ("lower", "foot_bolts"),
             ("upper", "adj_pins"), ("lower", "adj_pins"), ("head", "sheave"), ("head", "axle"), ("sheave", "axle"),
             ("upper", "bracket"), ("lower", "bracket"), ("upper", "bracket_bolts"), ("bracket", "winch"),
             ("upper", "winch"), ("head", "rope"), ("upper", "rope"), ("guard", "lower"), ("guard", "chains"),
             ("boards", "grab_shells"), ("grab_shells", "grab_yoke"), ("grab_shells", "grab_frame"),
             ("grab_yoke", "grab_frame"), ("head", "snatch"), ("upper_sleeves", "hinge_bolts"),
             ("lower_sleeves", "foot_bolts"), ("feet", "pads"), ("head", "upper_sleeves"), ("lower", "cleat"), ("feet", "chains"), ("lower", "chains")]
    rows = []
    for a, b in pairs:
        rows.append((f"{C[a].name} / {C[b].name}", _overlap(C[a].shape, C[b].shape)))
    # minimum gaps of note
    gaps = {
        "leg overlap at nominal length (mm)": g["overlap"],
        "leg overlap at the longest setting (mm)": g["overlap"] - P["ADJ_PITCH"],
        "lower leg top to stop bolt edge, shortest setting (mm)": (g["lo_top"] - P["ADJ_PITCH"]) - (P["STOP_S"] + P["STOP_D"] / 2),
        "upper leg top corner to head plate (mm)": P["HUB_Z0"] - (P["PIN_Z"] + P["END_HOLE"] * g["cos"] + P["UP"][0] / 2 * g["sin"]),
        "sheave rim to head plate (mm)": g["zs"] - P["SHEAVE"][0] - (P["HUB_Z0"] + P["HUB_T"]),
        "lower leg end corner to foot plate (mm)": P["FOOT_PIN_Z"] - P["END_HOLE"] * g["cos"] - P["LO"][0] / 2 * g["sin"] - (P["PAD_T"] + P["FOOT_PLATE"][2]),
        "chain edge to clevis plate, where the chain passes the clevis end (mm)":
            ((P["CHAIN_LUG_R"] - 50) * math.tan(math.radians(30)) - P["CHAIN_D"]) - (P["LO"][0] / 2 + 1 + P["CLEVIS_T"]),
        "chain to rim guard frame, mid-side (mm)": (P["R_FOOT"] + P["CHAIN_LUG_R"]) / 2 - P["CHAIN_D"] - (P["GUARD_R"] + P["GUARD_TUBE"][0] / 2),
    }
    return rows, gaps


def export(P=PARAMS):
    step, stl = ROOT / "cad/step", ROOT / "cad/stl"
    step.mkdir(parents=True, exist_ok=True)
    stl.mkdir(parents=True, exist_ok=True)
    cs = components(P, heads=False)
    tripod_keys = {"grab_shells", "grab_yoke", "grab_frame", "guard", "boards", "guard_pins"}
    items = {"hatchside-assembly": Compound(children=[c.shape for c in cs]),
             "hatchside-tripod": Compound(children=[c.shape for c in cs if c.key not in tripod_keys])}
    for k, v in head_comps(P).items():
        items[f"hatchside-head-{k}"] = v
    for name, shape in items.items():
        export_step(shape, str(step / f"{name}.step"))
        export_stl(shape, str(stl / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        print("wrote", name)


if __name__ == "__main__":
    g = geometry()
    print({k: round(v, 1) if isinstance(v, float) else v for k, v in g.items()})
    rows, gaps = checks()
    print("Interference (mm3):")
    for n, v in rows:
        print(f"  {v:10.1f}  {n}")
    print("Clearances:")
    for n, v in gaps.items():
        print(f"  {v:8.1f}  {n}")
    if "--check" not in sys.argv:
        export()
