"""HatchSide prototype build plan pictures (HTS-BLD-001, STANDARDS section 18).

Run from the repo root:
    python cad/src/build_plan_media.py                     everything (better one group per process)
    python cad/src/build_plan_media.py overview
    python cad/src/build_plan_media.py sheets [101 102 ...]
    python cad/src/build_plan_media.py joints [1 2 ...]
    python cad/src/build_plan_media.py steps [1 2 ...]
Every picture is drawn from cad/src/model.py, so the pictures and the model never disagree:
    docs/05-build-plan/overview.png       every component pulled apart, numbered in build order
    cad/drawings/HTS-DWG-101 to 112       making sketches for the made components
    docs/05-build-plan/joint-NN.png       close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png        one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from build123d import Compound, Pos, Rot  # noqa: E402
import model as m  # noqa: E402

P = m.PARAMS
OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-03"
PROJECT = "HatchSide"
_C = None


def comps():
    global _C
    if _C is None:
        _C = {c.key: c for c in m.components(heads=False)}
    return _C


def part(key, name=None, explode=None, color=None):
    c = comps()[key]
    return Part(name or c.name, c.shape, color or c.color, c.bom, c.explode if explode is None else explode)


def window(parts, lo, hi):
    """Keep only what lies inside the box lo..hi (zoom for a joint close-up)."""
    cutter = m.box(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
    out = []
    for p in parts:
        kept = []
        for s in p.shape.solids():
            try:
                r = s & cutter
                if r is not None and r.volume > 1e-3:
                    kept.append(r)
            except Exception:
                pass
        if kept:
            out.append(Part(p.name, Compound(children=kept), p.color, p.bom, p.explode, p.alpha))
    return out


def around(pt, half):
    return (pt[0] - half[0], pt[1] - half[1], pt[2] - half[2]), (pt[0] + half[0], pt[1] + half[1], pt[2] + half[2])


AZ = P["LEG_AZ"]
G = m.geometry()


def leg_dir_xy(phi, d):
    a = math.radians(phi)
    return (d * G["sin"] * math.cos(a), d * G["sin"] * math.sin(a), -d * G["cos"])


# ------------------------------------------------------------------ overview
def overview():
    C = comps()
    order = [("feet", "Feet and rubber pads", ("feet", "pads"), (0, 0, -350)),
             ("lower", "Lower legs with foot sleeves", ("lower", "lower_sleeves"), (0, 0, -100)),
             ("upper", "Upper legs with hinge sleeves", ("upper", "upper_sleeves"), (0, 0, 380)),
             ("head", "Tripod head with mast cheeks", ("head",), (0, 0, 700)),
             ("sheave", "Head sheave and axle", ("sheave", "axle"), (0, 0, 1050)),
             ("bolts", "Hinge bolts, foot bolts, adjust pins", ("hinge_bolts", "foot_bolts", "adj_pins"), (450, 0, 300)),
             ("chains", "Leg-spread chains", ("chains",), (0, 0, -650)),
             ("bracket", "Winch bracket and bolts", ("bracket", "bracket_bolts"), (0, -450, 150)),
             ("winch", "Hand winch and line counter", ("winch", "counter"), (0, -800, 300)),
             ("rope", "Wire rope", ("rope",), (0, -250, -350)),
             ("interface", "Head interface (swivel, shackle)", ("interface",), (0, 0, 350)),
             ("snatch", "Snatch block and cleat", ("snatch", "cleat"), (0, 400, 650)),
             ("guard", "Rim guard panels and drop pins", ("guard", "boards", "guard_pins"), (0, 0, 0)),
             ("grab", "Grab head", ("grab_shells", "grab_yoke", "grab_frame"), (0, 0, -150))]
    ps = [Part(n, Compound(children=[C[k].shape for k in ks]), C[ks[0]].color, None, e) for _, n, ks, e in order]
    # the four other heads, beside the tripod
    for key, name in (("sampler", "Sampler head"), ("rake", "Rake head"), ("retrieval", "Retrieval head"),
                      ("domereach", "DomeReach head")):
        cs = [c for c in m.components(heads=True) if c.key.startswith(key[:4]) or (key == "domereach" and c.key.startswith("dr_"))
              or (key == "retrieval" and c.key == "connector")]
        ps.append(Part(name, Compound(children=[c.shape for c in cs]), cs[0].color, None, (0, 0, 0)))
    return bv.overview(ps, OUT / "overview.png", f"{PROJECT}: every component in build order",
                       subtitle="Pulled apart and numbered in build order; the four other heads stand beside the tripod",
                       key=True, size=(11, 7.5))


# ------------------------------------------------------------------ making sketches
def neighbours(*keys):
    C = comps()
    return [Part(C[k].name, C[k].shape, C[k].color) for k in keys]


def sheet(no):
    C = comps()
    fa = m.foot()[0]
    up = m.upper_leg(P, True)
    lo = m.lower_leg(P, True)
    gp = m.guard_panel(P)
    gr = m.grab_parts(P)
    flat = Rot(0, 90, 0)      # a leg drawn lying along X
    specs = {
        101: dict(key="feet", title="Foot with clevis and chain lug: making sketch",
                  shape=Compound(children=[fa, m.foot()[1]]), view=Pos(0, -P["R_FOOT"], 0) * Compound(children=[fa, m.foot()[1]]),
                  nb=("lower", "chains", "pads"),
                  material="8 mm S275 plate, hot-dip galvanized; 10 mm rubber pad",
                  notes=["Base plate 140 x 280 x 8; rubber pad the same size bonded under",
                         "Two clevis plates 100 long x 80 high x 8, 52 apart inside",
                         "17 mm pin hole in both, 70 above the ground, 50 from the clevis ends",
                         "Clevis centred 140 from each end of the base plate",
                         "Chain lug 8 thick, 100 x 45, at the outer end; 14 mm hole 140 out",
                         "Weld clevis and lug to the base with 5 mm fillets both sides",
                         "Clamp a 52 mm spacer between the clevis plates while welding",
                         "Galvanize, then bond the pad with contact adhesive",
                         "Fits: lower leg sits between the clevis plates on an M16 bolt",
                         "through a steel crush sleeve; chains shackle to the lug",
                         "Make 3"]),
        102: dict(key="lower", title="Lower leg: making sketch", view=flat * lo,
                  nb=("upper", "feet", "adj_pins"),
                  material="50 x 50 x 3 mm 6082-T6 aluminium square tube, 1,500 long",
                  notes=["Saw 1,500 long, square ends, deburr",
                         "Foot pin hole 17 mm through both side walls, 30 from the bottom",
                         "Press a 25 x 3.5 steel sleeve 44 long between the walls there",
                         "Three 13 mm adjust holes, same faces, at 75 pitch:",
                         "  centre hole 1,235 from the bottom end, one 75 each side",
                         "Leg B only: two 7 mm cleat holes on the outer face,",
                         "  875 and 955 from the bottom end, on the centre line",
                         "Mark the 1,235 hole 'N' (normal length)",
                         "Fits: slides inside the upper leg with 1 mm each side",
                         "Make 3"]),
        103: dict(key="upper", title="Upper leg: making sketch", view=flat * up,
                  nb=("lower", "head", "bracket"),
                  material="60 x 60 x 4 mm 6082-T6 aluminium square tube, 1,450 long",
                  notes=["Saw 1,450 long, square ends, deburr inside the bottom end",
                         "Hinge hole 17 mm through two opposite walls, 30 from the top",
                         "Press a 25 x 3.5 steel sleeve 52 long between the walls there",
                         "Adjust hole 13 mm, same faces, 40 from the bottom end",
                         "Leg A only: 13 mm stop bolt hole through the other two faces,",
                         "  1,045 from the top end (1,015 below the hinge hole)",
                         "Rivet the adjust pin lanyard 100 above the adjust hole",
                         "Fits: top between a lug pair on an M16 bolt; lower leg inside",
                         "Make 3; mark leg A with red tape"]),
        104: dict(key="head", title="Tripod head with mast cheeks: making sketch", view=C["head"].shape,
                  nb=("upper", "sheave", "snatch"),
                  material="S275 plate 10, 8 and 6 mm; welded; hot-dip galvanized",
                  notes=["Head plate: 320 disc x 10, 40 hole in the centre for the rope,",
                         "  13 hole 95 from the centre (away from leg A) for the eye bolt",
                         "Lugs: six 8 mm plates 90 wide x 105 high, in pairs 62 apart",
                         "  inside, at 120 deg; 17 hinge hole 60 below the plate, 110 out",
                         "Cheeks: two 6 mm plates 180 x 195, 34 apart inside, on the",
                         "  centre line over leg A; 21 axle hole 63 toward leg A, 93 up",
                         "Rope keeper 12 bar across the cheeks 85 above the axle",
                         "Gusset 8 mm across the cheeks' back edge, 120 high",
                         "Jig the lugs with three 52 mm spacers and a 16 mm rod",
                         "Fillet welds 6 mm both sides; competent welder; then galvanize"]),
        105: dict(key="bracket", title="Winch bracket and clamp plate: making sketch",
                  view=m.bracket(P)[0], nb=("upper", "winch", "bracket_bolts"),
                  material="8 mm S275 plate, hot-dip galvanized; A4 bolts",
                  notes=["Two plates 120 x 270 x 8, front and back of leg A",
                         "Four 11 mm holes 42 each side of the centre line,",
                         "  22 from each end, drilled through both plates together",
                         "Front plate: four winch base holes to suit the winch bought",
                         "Fit nylon strips 2 mm between plates and the leg",
                         "Top edge of both plates bears on the M12 stop bolt",
                         "Clamp bolts M10 x 90 A4 with nylocks; snug, not crushing",
                         "Fits: winch base bolts flat to the front plate, drum across",
                         "the leg, crank to the right as you face the leg"]),
        106: dict(key="guard", title="Rim guard panel: making sketch", view=Pos(0, -P["GUARD_R"], 0) * Compound(children=[gp[0], gp[1]]),
                  nb=("guard_pins", "boards", "grab_shells"),
                  material="25 x 25 x 2 mm aluminium tube; 6 mm HDPE board",
                  notes=["Frame 746 long x 400 high from 25 x 25 x 2 tube, mitred or",
                         "  butted and TIG welded (or riveted with corner gussets)",
                         "Four rings 30 OD x 14 ID x 30 long on 8 mm lugs, centred",
                         "  25 beyond each end post: right end at 40 and 300 up,",
                         "  left end at 75 and 335 up (they interleave with the next)",
                         "Splash board 696 x 275 x 6 HDPE riveted to the inner face,",
                         "  bottom edge 30 up, 10 rivets",
                         "Fits: six panels make a hexagon 1,380 across flats; a 12 mm",
                         "drop pin through four rings joins each corner",
                         "Make 6; paint the top rail with yellow and black bands"]),
        107: dict(key="grab_shells", title="Grab shell: making sketch", view=gr["shell_right"],
                  nb=("grab_yoke", "grab_frame"),
                  material="3 mm S275 sheet; 5 mm S275 end plates; galvanized",
                  notes=["Shell sheet 288 (developed) x 290 (302 for the right shell),",
                         "  rolled to 182 inside radius over a quarter turn",
                         "Top cover strip 90 x 3 along the outer edge",
                         "End plates 5 mm: quarter disc 185 radius, ear 55 x 62",
                         "  at the outer corner, boss 35 radius at the hinge",
                         "Hinge hole 26 at the corner; ear hole 13, 155 out, 35 up",
                         "Left shell: plates fit inside the sheet ends (290 apart)",
                         "Right shell: plates 1 mm outside the left shell's (302 apart)",
                         "Jig both shells on a 25 bar through the hinge holes",
                         "Weld 4 mm fillets inside; make 1 left and 1 right"]),
        108: dict(key="grab_frame", title="Grab head beam, tag rods and yoke: making sketch",
                  view=Compound(children=[gr["head_beam"], gr["tag_rods"], gr["yoke"], gr["pins"], gr["hinge_pin"]]),
                  nb=("grab_shells", "interface"),
                  material="S275 plate and flat bar; 25 and 12 mm bright bar; galvanized",
                  notes=["Head beam 160 x 362 x 10 with the standard tab on top:",
                         "  tab 10 thick, 60 wide, 20 hole 30 below its top edge",
                         "30 hole for the closing line 40 off centre",
                         "Four lugs 40 x 42 x 8 under the beam ends, 13 holes",
                         "Tag rods: four 30 x 6 flat bars, 440 between 13 holes",
                         "Yoke: two 50 x 6 bars 330 long, 26 hole 30 from the bottom,",
                         "  joined by a 50 x 10 crossbar with a 14 hole closing eye",
                         "Hinge pin 25 bar 340 long; pins 12 bar; R-clips and washers",
                         "Fits: rods pin to the shell ears and the beam lugs; yoke",
                         "rides on the hinge pin outside the shells"]),
        109: dict(key="grab_frame", title="Sampler head: making sketch",
                  view=Compound(children=list(m.sampler(P).values())), nb=(),
                  material="Clear PVC tube; stainless rod and plate; steel ballast",
                  notes=["Tube 75 OD x 3 wall x 600 clear PVC, ends square",
                         "Cage: four 10 mm stainless rods 694 long on a 120 circle,",
                         "  welded to 150 x 6 top and bottom plates",
                         "Top plate has the standard tab and a 32 hole; bottom plate",
                         "  a 100 hole; ballast ring 150 / 90 x 40 bolted under it",
                         "Two clamp rings hold the tube 54 below the top plate",
                         "Caps: 90 x 10 rubber discs on hinged arms, pulled shut",
                         "  by elastic cord through the tube; latch on the top plate",
                         "Set: caps latched open; trip: a jerk on the working line",
                         "Sample 2.2 L; its centre 420 below the shackle pin"]),
        110: dict(key="grab_frame", title="Rake head: making sketch", view=m.rake(P), nb=(),
                  material="S275 flat bar and round bar; hot-dip galvanized",
                  notes=["Tine bar 400 x 50 x 12 with a 16 hole in the middle",
                         "Nine 12 mm tines 250 long at 45 pitch, welded into",
                         "  12.5 holes through the bar (plug weld both sides)",
                         "Ballast bar 380 x 40 x 40 welded on top of the tine bar",
                         "Two bails 40 x 8 from the ballast ends up to a 90 x 40 x 12",
                         "  top plate that carries the standard tab",
                         "Drag eye 40 x 40 x 12, 16 hole, on the front face",
                         "Use: lower on the rope, pull the working line on the drag",
                         "eye to draw the tines through scum, lift, repeat"]),
        111: dict(key="grab_frame", title="Retrieval head: making sketch",
                  view=Compound(children=list(m.retrieval(P).values())), nb=(),
                  material="S275 plate and sheet; EN 362 connector (bought)",
                  notes=["Top disc 300 x 6 with a 100 hole and the standard tab",
                         "Funnel rolled from 2.5 sheet: 300 at the top to 120 at",
                         "  the throat, 250 deep; seam welded; welded to the disc",
                         "Pole socket 33.7 x 3.2 tube 150 long at the rim, gusseted",
                         "Steel sling 300 long from the disc to an EN 362",
                         "  auto-locking connector hanging below the throat",
                         "Use: steer with the 2 m pole so the connector clips the",
                         "ring of a line already on the casualty's harness",
                         "The haul is made with certified rescue equipment only"]),
        112: dict(key="grab_frame", title="DomeReach head: making sketch",
                  view=Compound(children=list(m.domereach(P).values())), nb=(),
                  material="6082-T6 aluminium tube; A4 pins; bought roller and tools",
                  notes=["Pole: two 50 x 3 tubes 1,500 long joined by a 160 sleeve",
                         "  and a 10 mm pin; top cap with the standard tab",
                         "Tiller: 25 tube 600 long on a clamp collar 250 below the top",
                         "Fairlead ring 500 below the top for the arm pull line",
                         "Clevis: two 56 x 150 x 8 plates on a plug in the bottom,",
                         "  12 pin hole 60 below the pole end",
                         "Arm 40 x 40 x 3 x 700 on the 12 pin; tool fork at its end",
                         "Tools: 230 sealant roller, scum paddle, scoop basket",
                         "Single hinge only, no gripper; folds down to pass 560",
                         "Reaches 2.6 m below the rim with the tiller still above it"]),
    }
    sp = specs[no]
    pc = C[sp["key"]]
    if no >= 109:
        local = {109: Compound(children=list(m.sampler(P).values())), 110: m.rake(P),
                 111: Compound(children=list(m.retrieval(P).values())), 112: Compound(children=list(m.domereach(P).values()))}[no]
        me = Part("this head", local, "#0F766E")
        nbs = []
    else:
        me = Part(pc.name, pc.shape, pc.color)
        nbs = neighbours(*sp["nb"])
    if no in (107, 108):
        nbs = [Part("grab", Compound(children=[C[k].shape for k in ("grab_shells", "grab_yoke", "grab_frame") if k != sp["key"]]), "#999")]
    return bv.component_sheet(me, nbs, PROJECT, f"HTS-DWG-{no}", sp["title"], sp["material"], sp["notes"], DATE,
                              out_dir=str(DWG), view_shape=sp["view"])


# ------------------------------------------------------------------ joints
def joints(n):
    C = comps()
    A = AZ[0]
    if n == 1:
        pin = m.leg_point(A, 0)
        ps = [part("head"), part("upper"), part("upper_sleeves"), part("hinge_bolts")]
        return bv.joint(window(ps, *around(pin, (160, 160, 140))), OUT / "joint-01.png",
                        "Joint 1: leg hinge at the head",
                        "Upper leg between a lug pair on an M16 bolt through a steel crush sleeve", cut="+X", azim=-30)
    if n == 2:
        p = m.leg_point(A, G["adj_s"])
        ps = [part("upper"), part("lower"), part("adj_pins")]
        return bv.joint(window(ps, *around(p, (110, 110, 200))), OUT / "joint-02.png",
                        "Joint 2: telescoping leg and adjust pin",
                        "50 mm lower leg slides in the 60 mm upper leg; 12 mm ball-lock pin through both", cut="+X",
                        azim=-30)
    if n == 3:
        p = m.leg_point(A, G["Lp"])
        ps = [part("feet"), part("pads"), part("lower"), part("lower_sleeves"), part("foot_bolts"), part("chains")]
        return bv.joint(window(ps, *around(p, (190, 220, 130))), OUT / "joint-03.png",
                        "Joint 3: foot, leg and chains",
                        "Lower leg on an M16 bolt between the clevis plates; chains shackled to the outer lug",
                        azim=-35)
    if n == 4:
        p = (0, -60, G["zs"] - 40)
        ps = [part("head"), part("sheave"), part("axle"), part("rope")]
        return bv.joint(window(ps, *around(p, (60, 140, 160))), OUT / "joint-04.png",
                        "Joint 4: sheave in the mast cheeks",
                        "M20 axle through both cheeks; the rope keeper bar sits 10 mm above the rope", cut="+X",
                        azim=-20, elev=12)
    if n == 5:
        p = m.leg_point(A, (P["BRACKET_S"][0] + P["BRACKET_S"][1]) / 2, 60)
        ps = [part("upper"), part("bracket"), part("bracket_bolts"), part("winch"), part("counter"), part("rope")]
        return bv.joint(window(ps, *around(p, (260, 260, 260))), OUT / "joint-05.png",
                        "Joint 5: winch bracket on leg A",
                        "Clamp plates either side of the leg; the stop bolt above them takes the rope pull",
                        azim=-120, elev=20)
    if n == 6:
        z = P["HOOK_Z"]
        ps = [part("interface"), part("rope"), part("grab_frame")]
        return bv.joint(window(ps, *around((0, 0, z + 40), (120, 120, 200))), OUT / "joint-06.png",
                        "Joint 6: the head interface",
                        "Rope eye, swivel and screw-pin shackle through the 20 mm hole in every head's 10 mm tab",
                        azim=-60)
    if n in (7, 8):
        gr = m.grab_parts(P)
        zh = gr["_z_h"]
        ps = [Part("Grab shell, left", gr["shell_left"], "#0E7490"), Part("Grab shell, right", gr["shell_right"], "#22D3EE"),
              Part("Closing yoke", gr["yoke"], "#C2410C"), Part("Hinge pin 25 mm", gr["hinge_pin"], "#111827"),
              Part("Tag rods", gr["tag_rods"], "#155E75"), Part("Pins 12 mm", gr["pins"], "#111827"),
              Part("Head beam and tab", gr["head_beam"], "#0F766E")]
        if n == 7:
            return bv.joint(window(ps, (-120, -200, zh - 90), (120, 200, zh + 90)), OUT / "joint-07.png",
                            "Joint 7: grab hinge", "Shell end plates interleave on the 25 mm pin; the yoke bars ride outside",
                            cut="+X", azim=-35)
        return bv.joint(window(ps, (-200, -200, -130), (200, 200, 40)), OUT / "joint-08.png",
                        "Joint 8: tag rods to the head beam", "Each rod pinned inside a lug under the 10 mm beam",
                        azim=-35)
    if n == 9:
        rc = P["GUARD_R"] / math.cos(math.radians(30))
        a = math.radians(A + 30)
        p = (rc * math.cos(a), rc * math.sin(a), 200)
        ps = [part("guard"), part("boards"), part("guard_pins")]
        return bv.joint(window(ps, *around(p, (110, 110, 260))), OUT / "joint-09.png",
                        "Joint 9: rim guard corner", "Four rings from two panels interleave on one 12 mm drop pin",
                        azim=-60)
    if n == 10:
        d = m.domereach(P)
        zb = -30 - 2 * P["DR_POLE"][2]
        ps = [Part("Pole", d["pole"], "#6D28D9"), Part("Arm, clevis and fork", d["arm"], "#A78BFA"),
              Part("Sealant roller", d["roller"], "#9CA3AF")]
        return bv.joint(window(ps, (-120, -160, zb - 160), (620, 160, zb + 600)), OUT / "joint-10.png",
                        "Joint 10: DomeReach arm hinge and roller",
                        "One 12 mm pin in a clevis; the pull line from the arm tip sets the angle", azim=-80, elev=10)


# ------------------------------------------------------------------ steps
STEPS = {
    1: ("Step 1: fit the sheave in the mast", ["head"], ["sheave", "axle"], {"sheave": (0, 0, 0), "axle": (300, 0, 0)}),
    2: ("Step 2: bolt the upper legs to the head", ["head", "sheave", "axle"], ["upper", "upper_sleeves", "hinge_bolts"], None),
    3: ("Step 3: slide in the lower legs and pin them", ["head", "sheave", "axle", "upper", "hinge_bolts"],
        ["lower", "lower_sleeves", "adj_pins"], None),
    4: ("Step 4: pin the feet to the legs", ["head", "upper", "lower", "adj_pins"], ["feet", "pads", "foot_bolts"], None),
    5: ("Step 5: shackle the leg-spread chains", ["head", "upper", "lower", "feet", "pads"], ["chains"], None),
    6: ("Step 6: clamp the winch bracket to leg A", ["head", "upper", "lower", "feet", "chains"], ["bracket", "bracket_bolts"], None),
    7: ("Step 7: bolt on the winch and line counter", ["head", "upper", "lower", "feet", "chains", "bracket"],
        ["winch", "counter"], None),
    8: ("Step 8: reeve the rope and fit the head interface", ["head", "sheave", "upper", "lower", "feet", "chains", "bracket",
                                                              "winch", "counter"], ["rope", "interface"], {"rope": (0, 0, 0)}),
    9: ("Step 9: hang the snatch block and fit the cleat", ["head", "upper", "lower", "feet", "chains", "winch", "rope"],
        ["snatch", "cleat"], None),
    10: ("Step 10: pin the rim guard round the opening", ["head", "upper", "lower", "feet", "chains", "winch", "rope"],
         ["guard", "boards", "guard_pins"], {"guard": (0, 0, 0), "boards": (0, 0, 0)}),
    13: ("Step 13: hang the grab and lead the closing line", ["head", "upper", "lower", "feet", "chains", "winch", "rope",
                                                              "interface", "guard", "boards"],
         ["grab_shells", "grab_yoke", "grab_frame"], {"grab_shells": (0, 0, -500), "grab_yoke": (0, 0, -500), "grab_frame": (0, 0, -500)}),
}
SUB = {1: "Head on the bench, mast up; washers either side of the sheave",
       2: "Legs folded together on the ground; nylock nuts snug, legs swing freely",
       3: "Normal length: the pin through the hole marked N",
       4: "Foot bolts snug; pads down",
       5: "Stand the tripod over the opening first; chains set the 3 m foot circle",
       6: "Plates either side of leg A, stop bolt through the leg above them",
       7: "Crank to the right; counter where the rope leaves the drum",
       8: "Rope up leg A, over the sheave, down through the head plate",
       9: "Working line through the snatch block, tail to the cleat on leg B",
       10: "Six panels; leave one corner open while placing, then drop the pin",
       13: "Shackle on the tab; closing line from the yoke eye through the snatch block"}


def step(n):
    if n in (11, 12, 14):
        return local_step(n)
    title, done, new, ex = STEPS[n]
    ex = ex or {}
    d = [part(k) for k in done]
    nw = [part(k, explode=ex.get(k)) for k in new]
    return bv.step(d, nw, OUT / f"step-{n:02d}.png", title, SUB[n], label_done=n <= 3, azim=-58,
                   elev=20 if n not in (1,) else 24)


def local_step(n):
    if n in (11, 12):
        gr = m.grab_parts(P)
        sl = Part("Grab shell, left", gr["shell_left"], "#0E7490", None, (-250, 0, 0))
        sr = Part("Grab shell, right", gr["shell_right"], "#22D3EE", None, (250, 0, 0))
        yk = Part("Closing yoke", gr["yoke"], "#C2410C", None, (0, 0, 250))
        hp = Part("Hinge pin 25 mm", gr["hinge_pin"], "#111827", None, (0, 450, 0))
        tr = Part("Tag rods", gr["tag_rods"], "#155E75", None, (0, 0, 200))
        pn = Part("Pins 12 mm", gr["pins"], "#111827", None, (0, 300, 0))
        hb = Part("Head beam and tab", gr["head_beam"], "#0F766E", None, (0, 0, 350))
        if n == 11:
            return bv.step([sl], [sr, yk, hp], OUT / "step-11.png", "Step 11: put the grab shells and yoke on the hinge pin",
                           "Left shell first, right shell over its end plates, yoke bars outside; washers and R-clips",
                           azim=-35)
        return bv.step([sl, sr, yk, hp], [tr, hb, pn], OUT / "step-12.png", "Step 12: fit the tag rods and the head beam",
                       "Rods on the ear pins, then the beam lugs over the rods' top ends; R-clips on every pin",
                       azim=-35, label_done=False)
    d = m.domereach(P)
    po = Part("Pole sections, cap and tiller", Compound(children=[d["pole"], d["tiller"]]), "#6D28D9")
    ar = Part("Arm and clevis", d["arm"], "#A78BFA", None, (250, 0, -200))
    ro = Part("Sealant roller", d["roller"], "#9CA3AF", None, (250, 0, 150))
    return bv.step([po], [ar, ro], OUT / "step-14.png", "Step 14: assemble DomeReach",
                   "Join the poles at the sleeve and pin; arm on the clevis pin; roller on the fork; pull line to the fairlead",
                   azim=-80, elev=12, size=(6, 8))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    nums = [int(a) for a in sys.argv[2:]]
    if what in ("overview", "all"):
        print(overview())
    if what in ("sheets", "all"):
        for no in nums or range(101, 113):
            print(sheet(no))
    if what in ("joints", "all"):
        for n in nums or range(1, 11):
            print(joints(n))
    if what in ("steps", "all"):
        for n in nums or range(1, 15):
            print(step(n))
