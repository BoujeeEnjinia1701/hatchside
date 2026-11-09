"""HatchSide repo-specific CAD helpers (kit 1.9). Built on .kit/cad_parts.py; nothing here belongs in .kit/.

Helpers the parts library does not have (suggested kit additions are listed in docs/REVIEW.md):
    orient(shape, d)          turn a part built along +Z to point along +x, -x, +y, -y, +z or -z
    plate(plane, ...)         a flat plate in any of the three planes, with holes and rounded corners
    box(...)                  an axis-aligned block with eased edges (never a bare box)
    bar(p0, p1, d)            a round bar between two points, ends chamfered
    tube_between(p0, p1,...)  a round tube between two points
    stock_between(...)        square or rectangular hollow section between two points
    weld_bead(...)            a fillet weld bead along a run, between two faces named by direction
    ring_weld(r, leg)         a fillet weld round a bar or tube where it meets a plate at z = 0
    bolt_set(...)             an ISO bolt, washers and nut, with the bolt length taken from the ISO 4017 series
    std_length(L)             the next standard bolt length at or above L
    link_chain(...)           a chain drawn link by link along a straight run
    shackle(...), carabiner() bought rigging hardware
All sizes in millimetres.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Axis, Box, Circle, Compound, Cone, Cylinder, Face, Location, Plane, Polyline, Pos, Rot,  # noqa: E402
                       Sketch, SlotOverall, Solid, Torus, Vector, Wire, extrude, fillet, revolve)
import cad_parts as cp  # noqa: E402

ROT_TO = {"+z": (0, 0, 0), "-z": (180, 0, 0), "+x": (0, 90, 0), "-x": (0, -90, 0), "+y": (-90, 0, 0), "-y": (90, 0, 0)}
VEC = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}
OPP = {"-z": "+z", "+z": "-z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}

ISO_4017_LENGTHS = (10, 12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160)


def orient(shape, d):
    """Rotate a shape built along +Z so that +Z points along d ('+x', '-x', '+y', '-y', '+z', '-z')."""
    return Rot(*ROT_TO[d]) * shape


def std_length(L):
    for s in ISO_4017_LENGTHS:
        if s >= L - 1e-6:
            return s
    return int(math.ceil(L / 10) * 10)


def box(x0, x1, y0, y1, z0, z1, r=1.0):
    """Block between the coordinates, edges eased by r (a cut and deburred part, not a bare box)."""
    b = Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
    return cp.break_edges(b, r) if r else b


def plate(plane, a, b, t, centre, holes=(), r_corner=3.0, edge=0.5):
    """Flat plate a x b x t centred on `centre` (thickness symmetric about the centre). plane 'yz' (normal X, a along
    Y, b along Z), 'xz' (normal Y, a along X, b along Z) or 'xy' (normal Z, a along X, b along Y). holes
    [(u, v, dia)] are measured from the plate centre along (a, b)."""
    s = Pos(0, 0, -t / 2) * cp.sheet(a, b, t, holes=holes, r_corner=r_corner, edge=edge)       # in XY, t along Z
    if plane == "yz":
        s = Plane.YZ.location * s
    elif plane == "xz":
        s = Plane.XZ.location * s
    return Pos(*centre) * s


def bar(p0, p1, d, chamfer=0.5):
    """Round bar of diameter d between two points."""
    a, b = Vector(*p0), Vector(*p1)
    v = b - a
    s = cp.round_bar(d, v.length, chamfer)
    return _along(s, a, v)


def _along(shape, a, v):
    """Move a shape built along +Z from the origin so it starts at point a and points along vector v."""
    v = Vector(*v) if not isinstance(v, Vector) else v
    z = v.normalized()
    if abs(z.Z) > 0.99999:
        loc = Pos(a.X, a.Y, a.Z) * (Rot(180, 0, 0) if z.Z < 0 else Rot(0, 0, 0))
        return loc * shape
    from build123d import Location
    return Location(Plane(origin=a, z_dir=z)) * shape


def tube_between(p0, p1, od, wall):
    a, b = Vector(*p0), Vector(*p1)
    v = b - a
    return _along(cp.round_tube(od, wall, v.length), a, v)


def stock_between(p0, p1, a, b_, t, roll=0.0):
    """Rectangular hollow section a x b_ x t between two points (the a side is rotated `roll` degrees about the run)."""
    p, q = Vector(*p0), Vector(*p1)
    v = q - p
    s = Rot(0, 0, roll) * cp.rhs(a, b_, t, v.length)
    return _along(s, p, v)


def drill(shape, centre, direction, dia, length=2000.0):
    """Subtract a through hole of diameter dia along direction ('x', 'y' or 'z') through `centre`."""
    ax = {"x": "+x", "y": "+y", "z": "+z"}[direction]
    cyl = Pos(*centre) * orient(Cylinder(dia / 2, length), ax)
    return shape - cyl


def weld_bead(p0, run, length, leg_a, leg_b, leg):
    """Fillet weld bead from point p0 along direction `run` for `length`, its two legs along leg_a and leg_b
    (direction strings such as '+y', '-z'). The bead fills the corner between the two faces that meet along the run."""
    import numpy as np
    a, b, r = (np.array(VEC[v], float) for v in (leg_a, leg_b, run))
    p0 = np.array(p0, float)
    tri = [tuple(p0), tuple(p0 + a * leg), tuple(p0 + b * leg)]
    face = Face(Wire(Polyline(*tri, close=True)))
    bead = extrude(face, amount=length, dir=tuple(r))
    try:
        bead = fillet(bead.edges().filter_by(Axis((0, 0, 0), tuple(r))), leg * 0.12)
    except Exception:
        pass
    return bead


def ring_weld(r, leg, inside=False):
    """Fillet weld bead round a bar or tube of radius r where it meets a plate at z = 0, on the +Z side."""
    pts = ((r, 0, 0), (r - leg, 0, 0), (r, 0, leg)) if inside else ((r, 0, 0), (r + leg, 0, 0), (r, 0, leg))
    return revolve(Face(Wire(Polyline(*pts, close=True))), Axis.Z)


_BOLT_CACHE = {}


def _bolt_parts(d, L):
    """Cached ISO 4017 bolt of exact length L, washer and nut (shapes at the origin, head up, z = 0 at the bolt seat)."""
    key = (d, L)
    if key not in _BOLT_CACHE:
        s, k, m, d2, h, p = cp.ISO[d]
        _BOLT_CACHE[key] = dict(bolt=Pos(0, 0, h) * cp.hex_bolt(d, L), washer=cp.washer(d), nut=cp.hex_nut(d))
    return _BOLT_CACHE[key]


def bolt_length(d, grip, n_washers=2):
    """ISO length for a bolt clamping `grip` mm (washers included in the stack): grip + washers + nut + 2 pitches."""
    s, k, m, d2, h, p = cp.ISO[d]
    return std_length(grip + n_washers * h + m + 2 * p)


def bolt_set(d, grip, face, shank, material="stainless", bom=None, group="fixings", tag="", explode=(0, 0, 0),
             L=None, washers=True):
    """Bolt, two washers and nut for a joint `grip` thick. `face` is the centre of the joint face on the head side;
    `shank` the direction the bolt points into the joint ('+x' ... '-z'). Returns part() dicts of kind fastener.
    The bolt length is the next ISO 4017 length unless L is given."""
    s, k, m, d2, h, p = cp.ISO[d]
    L = L or bolt_length(d, grip, 2 if washers else 0)
    c = _bolt_parts(d, L)
    up = OPP[shank]
    mk = lambda nm, shp: cp.part(f"{nm}{tag}", Pos(*face) * orient(shp, up), material, kind="fastener", bom=bom,
                                 group=group, explode=explode)
    out = [mk(f"M{d}x{L} hex bolt (ISO 4017)", c["bolt"] if washers else Pos(0, 0, -h) * c["bolt"])]
    if washers:
        out.append(mk(f"M{d} washer (ISO 7089)", c["washer"]))
        out.append(mk(f"M{d} washer (ISO 7089)", Pos(0, 0, -grip - h) * c["washer"]))
        out.append(mk(f"M{d} hex nut (ISO 4032)", Pos(0, 0, -grip - h - m) * c["nut"]))
    else:
        out.append(mk(f"M{d} hex nut (ISO 4032)", Pos(0, 0, -grip - m) * c["nut"]))
    return out


def nylon_washer(d, t=1.0):
    """Nylon isolating washer for a bolt of size d (outside diameter of the ISO 7089 washer), thickness t."""
    d2 = cp.ISO[d][3]
    return extrude(Sketch() + Circle(d2 / 2) - Circle(d * 0.54), t)


def link_chain(p0, p1, wire=6.0, pitch=18.0, width=21.0):
    """A straight run of chain, drawn link by link from p0 to p1 (end links lie flat, then alternate 90 degrees).
    Link inside length = pitch, outside width = width, made of `wire` round bar (stadium links)."""
    a, b = Vector(*p0), Vector(*p1)
    v = b - a
    L = v.length
    n = int(L // pitch)
    outer = width / 2
    # one link: a stadium ring of wire section, built as a torus pair joined by two straight bars
    r = outer - wire / 2
    straight = pitch - 2 * r + 2 * wire  # centre-line straight length
    straight = max(straight, 0.1)
    # build the link from two half tori (cut) and two cylinders along Z
    ring = Rot(90, 0, 0) * Torus(r, wire / 2)                       # ring in the XZ plane, axis along Y
    keep_top = ring & Pos(0, 0, r + straight / 2) * Box(4 * r, 4 * r, 2 * r)
    keep_bot = ring & Pos(0, 0, -r - straight / 2) * Box(4 * r, 4 * r, 2 * r)
    top = Pos(0, 0, straight / 2) * keep_top
    bot = Pos(0, 0, -straight / 2) * keep_bot
    side = [Pos(sx * r, 0, 0) * Cylinder(wire / 2, straight) for sx in (-1, 1)]
    link = Compound([top, bot] + side)
    links = []
    for i in range(n):
        z = pitch / 2 + i * pitch
        roll = 0 if i % 2 == 0 else 90
        links.append(Pos(0, 0, z) * Rot(0, 0, roll) * link)
    return _along(Compound(links), a, v)


def shackle(pin_d=11.0, inside=23.0, depth=22.0):
    """Bow shackle with a screw pin. Ring in the YZ plane, pin along Y through the origin, bow hanging toward +Z.
    The two legs stand at y = +-inside/2, so a plate up to `inside` thick fits between them. Returns (body, pin)."""
    r = pin_d * 0.55
    R = inside / 2 + r
    ring = Rot(0, 90, 0) * Torus(inside / 2 + 0.0, r)
    bow = ring & (Pos(0, 0, 2 * R) * Box(4 * R, 4 * R, 4 * R))
    bow = Pos(0, 0, depth) * bow
    legs = [Pos(0, sy * inside / 2, depth / 2) * Cylinder(r, depth) for sy in (-1, 1)]
    lugs = [Pos(0, sy * inside / 2, 0) * Rot(90, 0, 0) * Cylinder(r * 1.45, 2 * r) for sy in (-1, 1)]
    body = Compound([bow] + legs + lugs)
    L = inside + 4 * r + 4
    pin = Rot(90, 0, 0) * Cylinder(pin_d / 2, L)
    pin = pin + Pos(0, -L / 2 - 2.5, 0) * Rot(90, 0, 0) * Cylinder(pin_d * 0.85, 5)
    return body, pin


def oval_link(length, width, wire):
    """One stadium-shaped link (a ring of round bar) in the XZ plane: outside width `width` (X), outside length `length`
    (Z), centred on the origin."""
    r = width / 2 - wire / 2
    straight = max(length - width, 0.1)
    ring = Rot(90, 0, 0) * Torus(r, wire / 2)
    top = Pos(0, 0, straight / 2) * (ring & (Pos(0, 0, r) * Box(4 * r, 4 * r, 2 * r)))
    bot = Pos(0, 0, -straight / 2) * (ring & (Pos(0, 0, -r) * Box(4 * r, 4 * r, 2 * r)))
    side = [Pos(sx * r, 0, 0) * Cylinder(wire / 2, straight) for sx in (-1, 1)]
    return Compound([top, bot] + side)


def carabiner(length=110.0, width=58.0, wire=10.0):
    """Auto-locking steel connector (EN 362 type): an oval body in the XZ plane, long axis along Z, centred on the
    origin, with a gate bar on the +X side and a locking sleeve. Returns (body, gate, sleeve)."""
    body = oval_link(length, width, wire)
    xg = width / 2 - wire / 2
    gate = Pos(xg, 0, length * 0.12) * Cylinder(wire * 0.3, length * 0.48)
    sleeve = Pos(xg, 0, length * 0.38) * Cylinder(wire * 0.38, 16) - Pos(xg, 0, length * 0.38) * Cylinder(wire * 0.3, 20)
    return body, gate, sleeve


def cone_frustum(r0, r1, h, wall=None):
    """Solid or hollow cone from radius r0 at z = 0 to r1 at z = h."""
    c = Pos(0, 0, h / 2) * Cone(r0, r1, h)
    if wall:
        c = c - Pos(0, 0, h / 2 + 0.01) * Cone(r0 - wall, r1 - wall, h)
    return c


def rect_ring(x0, x1, y0, y1, z0, z1, t, r=0.5):
    """Hollow block (thin-walled rectangular tube section) between coordinates, open along Z."""
    o = box(x0, x1, y0, y1, z0, z1, r)
    i = Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0) - 2 * t, abs(y1 - y0) - 2 * t, abs(z1 - z0) + 2)
    return o - i


def frame(origin, y_dir, z_dir):
    """Location whose local Y is y_dir and local Z is z_dir (the two must be perpendicular)."""
    y = Vector(*y_dir) if not isinstance(y_dir, Vector) else y_dir
    z = Vector(*z_dir) if not isinstance(z_dir, Vector) else z_dir
    x = y.cross(z).normalized()
    return Location(Plane(origin=origin, x_dir=x, z_dir=z))


def screw_in(d, L, face, shank, material="stainless", bom=None, tag="", washer=True):
    """Hex bolt screwed into a tapped plate (no nut): the head, with a washer, sits on `face`; the shank points
    into the part along `shank`."""
    s, k, m, d2, h, p = cp.ISO[d]
    up = OPP[shank]
    key = (d, L)
    c = _bolt_parts(d, L)
    out = [cp.part(f"M{d}x{L} hex bolt (ISO 4017){tag}", Pos(*face) * orient(c["bolt"] if washer else Pos(0, 0, -h) * c["bolt"], up),
                   material, kind="fastener", bom=bom)]
    if washer:
        out.append(cp.part(f"M{d} washer (ISO 7089){tag}", Pos(*face) * orient(c["washer"], up), material, kind="fastener", bom=bom))
    return out
