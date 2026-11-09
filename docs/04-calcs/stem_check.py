"""HatchSide STEM check calculations (HTS-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. Reference product: the HatchSide kit as modelled in cad/src/model.py, option A (tripod
and hand winch, the design since kit 1.7) for S1 to S18 and S24, and option B (straddle-frame davit) for S19 to S23. Every number is
read from the calculation note's script (docs/04-calcs/sizing.py, HTS-CAL-001), which in turn reads the detailed model, so a
changed dimension changes the check. A check is a first-order screen; the calculation note holds the working.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs/04-calcs"), str(ROOT / "cad/src")]
from stem_check import Check, limits, G, WITHIN, PLAUSIBLE  # noqa: E402,F401
import sizing as S  # noqa: E402
from model import PARAMS as P  # noqa: E402

c = Check(ROOT / "docs/04-calcs/stem_results.csv")
A = S.A
s = S.structure()
kg, loads, tripod = S.masses()
tp = S.tipping(tripod)
gr = S.grab()
dr = S.domereach()
sm = S.sampler()
hp = S.heads_plan()
cy = S.cycle()
ob = S.option_b()
W = s["W"]

# ---- option A: tripod and hand winch
c.claim("S1", "Each leg of the tripod carries its share of 150 kg times the 1.5 proof and 1.25 dynamic factors, with the rope up to 10 degrees off vertical, without buckling", "Physics",
        "Strength of materials",
        f"Euler buckling of a pinned column, P = pi^2 E I / L^2, for the weaker 50 x 50 x 3 lower tube over the whole {S.geometry()['Lp']:.0f} mm pin-to-pin length "
        f"(6082-T6, E 69 GPa) gives {s['Pcr'] / 1e3:.1f} kN; the leg force is {s['Fmax'] / 1e3:.2f} kN with the rope vertical and {s['tilt_F'] / 1e3:.2f} kN at 10 degrees in the worst direction; "
        "the limit is half the Euler load, a knock-down for imperfection and the telescoping joint; the 110 mm rope offset at the winch adds a bending moment that is not yet in the note (HTS-CAL-001 section 10)",
        round(s["tilt_F"] / 1e3, 2), round(s["Pcr"] / 1e3 / 2.0, 2), "kN", closed_by="HTS-CAL-001 section 3")
c.claim("S2", "The 6 mm 7x19 stainless rope holds 150 kg with a factor of at least 5", "Physics", "Strength of materials",
        f"Rope minimum breaking load 21 kN (catalogue figure used in the calculation note) over a working load of {W / 1e3:.2f} kN: factor {s['rope_sf']:.1f}; "
        f"a factor of 5 is the usual minimum for rope that lifts goods",
        round(W / 1e3, 2), round(A["rope_mbl_kN"] / 5, 2), "kN", closed_by="HTS-CAL-001 section 3")
c.claim("S3", "The tripod does not tip when the rope hangs 10 degrees off vertical at the safe working load", "Physics", "Mechanics and statics",
        f"Overturning about a foot edge: tan(angle) = (W + weight of the tripod, winch and rope) x inradius / (W x sheave height); inradius {tp['a']:.0f} mm, "
        f"sheave {tp['h']:.0f} mm, tripod {tripod:.0f} kg",
        round(tp["ang"], 1), 10.0, "degrees", rule="above", closed_by="HTS-CAL-001 section 6")
c.claim("S4", "One person turns the winch against 150 kg at a comfortable cranking rate", "Biology", "Human physiology and biomechanics",
        f"Input power = load x rope speed / efficiency, with the low gear (10:1) at 40 rpm and efficiency {A['eta']}; sustained hand-cranking about 75 W "
        f"for an average adult; crank force {s['f_lo']:.0f} N at 250 mm",
        round(W * s["v_lo"] / 60 / A["eta"], 1), limits.HUMAN_SUSTAINED_W, "W", closed_by="HTS-CAL-001 section 4")
c.claim("S5", "The leg hinge and foot pins (M16) and the 4 mm aluminium walls carry the leg force in bearing and shear", "Physics", "Strength of materials",
        f"M16 A4-70 in double shear on the thread root {s['tau_bolt']:.1f} MPa (limit 0.6 x 450 MPa proof); bearing on the 4 mm upper-leg wall {s['bearing_al']:.1f} MPa and, governing, on the 3 mm lower-leg wall at the foot pin "
        f"{s['bearing_lo']:.1f} MPa (limit the 6082-T6 proof stress 250 MPa, so a ratio of {s['bearing_lo'] / A['fy_al']:.2f}); highest ratio shown",
        round(max(s["tau_bolt"] / (0.6 * A["bolt_fy"]), s["bearing_al"] / A["fy_al"], s["bearing_lo"] / A["fy_al"], s["lug_bear"] / A["fy_s"]), 2), 1.0, "of allowable",
        closed_by="HTS-CAL-001 section 3")
c.claim("S6", "The three leg-spread chains hold the feet in at the design case", "Physics", "Strength of materials",
        f"Chain tension {s['chain_T']:.0f} N (largest horizontal foot thrust over the square root of 3, equilateral layout; leg A below the winch carries the force less the rope pull) on two 6 mm wires of 28.3 mm2 each, about "
        f"{s['chain_T'] / 56.5:.0f} MPa against a yield of about 250 MPa for low-carbon steel with a factor of 2; the calculation note also compares it with a 5 kN working limit for 6 mm grade 30 chain, to confirm on purchase",
        round(s["chain_T"] / 56.5, 1), 125.0, "MPa", closed_by="HTS-CAL-001 section 3")
c.claim("S7", "The stop bolt (M12) that takes the rope pull on leg A holds at the design case", "Physics", "Strength of materials",
        f"Single shear {s['tau_stop']:.1f} MPa on the thread root against 0.6 x 450 MPa; bearing on the leg wall {s['bear_stop']:.1f} MPa against 250 MPa",
        round(max(s["tau_stop"] / (0.6 * A["bolt_fy"]), s["bear_stop"] / A["fy_al"]), 2), 1.0, "of allowable", closed_by="HTS-CAL-001 section 3")
c.cited("S8", "The 150 mm head sheave and the winch drum are large enough for the 6 mm rope", "Engineering and technology", "Manufacturing tolerances",
        "Rope makers advise a sheave of many rope diameters for 7x19 rope (commonly 18 or more) to limit bending fatigue and strength loss; the standard to cite is to be assessed (HTS-REG-001, G12)",
        f"Sheave D/d = {S.geometry()['D_over_d']:.1f}. The drum in the model has a 60 mm core, so D/d is about 10 at the core and about 13 on the outer layer; that is low for 7x19 rope, so the "
        "winch maker's drum size and rope recommendation govern. Confirm when the winch is bought (HTS-DEC-001, item 2)", PLAUSIBLE, closed_by="")
c.cited("S9", "The grab brings up at least 10 L of wet silt per cycle", "Mathematics", "Units and dimensional analysis",
        f"Two quarter-cylinder shells of 182 mm inside radius, geometric volume {gr['V']:.1f} L; 70 % fill gives {gr['payload']:.1f} L, and about 10 % drips back on the way up (HTS-CAL-001 section 8), leaving {gr['net']:.1f} L",
        f"{gr['net']:.1f} L net against 10 L: 3 % short on estimates for the fill factor (70 %) and the drip (10 %), neither measured. At 72 % fill the net is 10 L; PR-008 is at risk (fix proposed to Amish: HTS-DEC-001 D16)", PLAUSIBLE, closed_by="")
c.claim("S10", "A full grab with its wet silt is within the winch's safe working load", "Physics", "Mechanics and statics",
        f"Grab {kg[17]:.1f} kg plus {gr['silt']:.0f} kg of wet silt (1.8 kg/L, {gr['payload']:.1f} L) against the 150 kg safe working load",
        round(kg[17] + gr["silt"], 1), 150.0, "kg", closed_by="HTS-CAL-001 section 8")
c.cited("S11", "A grab buried in settled sludge frees with the pull the winch can give", "Physics", "Fluid mechanics",
        "Breakout of an object from settled sludge is suction and shear that depend on the sludge; no cited figure was found",
        f"The 450 kg winch rating and the 150 kg safe working load leave room over the {kg[17] + gr['silt']:.0f} kg full grab, but the real breakout force is not known; "
        "a jerk is covered by the 1.25 dynamic factor. Observe at a field trial (TRL 4)", PLAUSIBLE, closed_by="")
c.cited("S12", "The heaviest carried load can be carried by one person", "Biology", "Ergonomics",
        "ISO 11228-1 gives a 25 kg reference mass under ideal conditions, before multipliers for distance from the body, grip and frequency; 25 kg is the project's own target (HTS-PRB-001), not the recommended limit",
        f"Heaviest packed load {max(loads.values()):.1f} kg (grab head, a bulky 370 x 372 x 772 mm shape) against the 25 kg target; the margin is 1.3 kg and the multipliers are not applied. "
        "Loads 1 and 2 travel together (29 kg) and the tripod is stood up by two people. Weigh each load and assess against ISO 11228-1 at TRL 4", PLAUSIBLE, closed_by="")
c.claim("S13", "Every head, lowered with the grab closed, passes a 560 mm manhole clear opening with 20 mm to spare", "Mathematics", "Geometry",
        "Plan diagonal of each head from the bounding box of its modelled parts; the 560 mm clear opening is the smallest common street manhole (PRB)",
        round(max(v[3] for k, v in hp.items() if not k.startswith("domereach"))), 540.0, "mm", closed_by="HTS-CAL-001 section 7")
c.claim("S14", "The DomeReach arm reaches the floor of a 2.5 m deep household digester from the rim", "Mathematics", "Geometry",
        f"Hinge {dr['depth']:.0f} mm below the rim with the tiller 200 mm above it, plus the 700 mm arm: tool {dr['floor']:.0f} mm below the rim against the 2,500 mm depth "
        "assumed from household digester guidance", round(dr["floor"]), 2500.0, "mm", rule="above", closed_by="HTS-CAL-001 section 7")
c.cited("S15", "A hand-applied roller coat of generic sealant on the dome headspace seals small leaks", "Chemistry", "Materials chemistry",
        "Sealant types for biogas domes are flexible, moisture- or solvent-cured coatings; the cure in wet, methane and H2S headspace depends on the product (to assess in HTS-FEA-001)",
        "The tool only places a generic sealant by type; whether a product cures on a wet dome is the supplier's claim and needs a field check. No product is named", PLAUSIBLE, closed_by="")
c.cited("S16", "Galvanized steel, 6082 aluminium and A4 stainless fasteners last in sewer splash if the dissimilar metals are isolated", "Chemistry", "Corrosion",
        "Zinc and aluminium are anodic to stainless steel in wet, chloride and sulfide environments; nylon and stainless washers isolate the aluminium legs from steel fasteners; "
        "hydrogen sulfide attacks zinc and copper alloys over time",
        "Isolation is in the model (nylon washers and strips). Life in sewer atmospheres is not known from a cited source; coupon test at TRL 4 (R11 / PR-011)", PLAUSIBLE, closed_by="")
c.cited("S17", "The kit makes no ignition source in a flammable atmosphere", "Chemistry", "Combustion and hazards",
        "Ignition needs a spark, heat or static discharge in a flammable mixture (methane, H2S); hand tools and a mechanical winch have no electrics, but steel on steel or on concrete can spark "
        "and polyester rope can build static",
        "No claim of intrinsic safety is made. The kit is used only after a certified gas detector reads safe and ventilation is running; ATEX or similar assessment is outside the scope and listed in HTS-REG-001",
        PLAUSIBLE, closed_by="")
c.cited("S18", "A clamshell grab of 3 mm sheet shells and a 6 mm bar yoke closes on the 10 mm working line", "Physics", "Mechanics and statics",
        "Closing lever action: the working line pulls the yoke, which rotates the shells about the 25 mm hinge pin; the force the line needs depends on silt resistance",
        "Geometry shown in the model; the closing force against compacted sludge is not calculated here and is to be measured at TRL 4", PLAUSIBLE, closed_by="")

# ---- option B: straddle-frame davit
c.claim("S19", "The 100 x 100 x 5 mast carries the boom moment and the load (option B)", "Physics", "Strength of materials",
        f"Bending M = design load x {ob['arm_mast']:.0f} mm = {ob['M_mast']:.0f} N m on a section modulus of 57 cm3, plus axial load; S275 at 0.9 of yield",
        round(ob["sig_mast"]), round(ob["fall"]), "MPa", closed_by="HTS-CAL-001 section 11")
c.claim("S20", "The 80 x 80 x 4 boom carries the load at its tip (option B)", "Physics", "Strength of materials",
        f"Cantilever M = design load x {ob['arm_boom']:.0f} mm = {ob['M_boom']:.0f} N m plus the rope's axial pull; 80 x 80 x 4 section modulus 29 cm3, S275 at 0.9 of yield",
        round(ob["sig_boom"]), round(ob["fall"]), "MPa", closed_by="HTS-CAL-001 section 11")
c.claim("S21", "The four M16 bolts of the boom root hold the boom to the mast (option B)", "Physics", "Strength of materials",
        f"Couple on a 90 mm row spacing: tension {ob['T_root'] / 1e3:.1f} kN per upper bolt against 0.6 x 450 MPa x 157 mm2 = {0.6 * 450 * 157 / 1e3:.1f} kN",
        round(ob["T_root"] / 1e3, 1), round(0.6 * 450 * 157 / 1e3, 1), "kN", closed_by="HTS-CAL-001 section 11")
c.claim("S22", "The mast spigot joint (two M16 bolts on 200 mm) and the rear cross rail carry the bending moment (option B)", "Physics", "Strength of materials",
        f"Joint bolt shear {ob['tau_joint']:.0f} MPa and bearing {ob['bear_joint']:.0f} MPa; rear cross rail bending {ob['sig_rail']:.0f} MPa under the uplift of the rear bolt pair; "
        "highest ratio shown against 0.6 x 450 MPa shear, 275 MPa bearing and 0.9 of yield in bending",
        round(max(ob["tau_joint"] / (0.6 * 450), ob["bear_joint"] / 275, ob["sig_rail"] / ob["fall"]), 2), 1.0, "of allowable", closed_by="HTS-CAL-001 section 11")
c.claim("S23", "The straddle frame does not tip with the rope 10 degrees off vertical (option B)", "Physics", "Mechanics and statics",
        "The load line is inside the frame's support rectangle; tip angle about each edge from the centre of mass of the frame, mast, boom and winch; smallest of three directions",
        round(min(ob["tip"].values()), 1), 10.0, "degrees", rule="above", closed_by="HTS-CAL-001 section 11")
c.claim("S24", "At stall the hand winch cannot overload the rope or the legs (option A)", "Physics", "Strength of materials",
        f"The winch can pull up to its 450 kg first-layer rating, not only the 150 kg safe working load: rope pull {s['stall_pull']:.0f} N against a 21 kN minimum breaking load "
        f"(factor {s['stall_rope_sf']:.1f}) and leg A {s['stall_F'] / 1e3:.2f} kN against {s['Pcr'] / 1e3:.1f} kN Euler (factor {s['Pcr'] / s['stall_F']:.1f}); an accident case, checked for a factor of 2 on the rope and 1.5 on buckling",
        round(max(2 * s["stall_pull"] / (A["rope_mbl_kN"] * 1000), 1.5 * s["stall_F"] / s["Pcr"]), 2), 1.0, "of allowable", closed_by="HTS-CAL-001 section 3")

if __name__ == "__main__":
    c.write()
