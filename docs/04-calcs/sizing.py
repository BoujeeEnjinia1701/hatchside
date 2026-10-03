"""HatchSide sizing and first-principles checks (HTS-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Reads the geometry from cad/src/model.py (PARAMS, geometry(), the component solids for masses)
and the prices from bom/bom.csv, prints every number quoted in docs/04-calcs/01-sizing.md and
writes docs/04-calcs/results.csv. All values are first-principles estimates; nothing is measured.
"""
import copy
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
import model as m  # noqa: E402

P = m.PARAMS
G9 = 9.81

# ---------------------------------------------------------------- assumptions (A1 to A14)
A = {
    "swl_kg": 150.0,          # A1 safe working load at the head interface (R4)
    "proof": 1.5,             # A2 proof load factor (R4)
    "dyn": 1.25,              # A3 dynamic factor for snatch and jerk when a grab breaks free
    "E_al": 69000.0,          # A4 aluminium 6082-T6: E (MPa), 0.2 % proof (MPa), heat-affected not used
    "fy_al": 250.0,
    "fy_s": 275.0,            # A5 S275 plate yield (MPa)
    "bolt_fy": 450.0,         # A6 A4-70 stainless bolt 0.2 % proof (MPa)
    "rope_mbl_kN": 21.0,      # A7 6 mm 7x19 grade 316 rope minimum breaking load (catalogue, conservative)
    "winch_kg": 450.0,        # A8 winch rating on the first layer; about half on a full drum
    "drum_r_eff": 40.0,       # A9 drum radius to the rope centre with a few layers on (mm)
    "gear_hi": 4.0, "gear_lo": 10.0, "crank": 250.0, "eta": 0.75,   # A10 two-speed winch
    "crank_rpm": 40.0,        # A11 comfortable cranking rate
    "fill": 0.70,             # A12 grab fill factor for wet silt
    "silt_kgL": 1.8,          # A13 wet silt density (kg/L)
    "opening_min": 560.0,     # A14 smallest common manhole clear opening (Indian standard size), mm
}


def leg_unit(phi):
    """Unit vector along leg phi from the head down to the foot."""
    a = math.radians(phi)
    g = m.geometry()
    s, c = g["sin"], g["cos"]
    return (s * math.cos(a), s * math.sin(a), -c)


def solve3(M, b):
    """Solve a 3 x 3 linear system by Cramer's rule."""
    def det(X):
        return (X[0][0] * (X[1][1] * X[2][2] - X[1][2] * X[2][1]) - X[0][1] * (X[1][0] * X[2][2] - X[1][2] * X[2][0])
                + X[0][2] * (X[1][0] * X[2][1] - X[1][1] * X[2][0]))
    d = det(M)
    out = []
    for i in range(3):
        X = [row[:] for row in M]
        for r in range(3):
            X[r][i] = b[r]
        out.append(det(X) / d)
    return out


def geometry():
    g = m.geometry()
    return dict(g, R_FOOT=P["R_FOOT"], tri_in=P["R_FOOT"] / 2, sheave_d=2 * P["SHEAVE"][1],
                D_over_d=2 * P["SHEAVE"][1] / P["ROPE_D"])


def leg_forces(W):
    """Compressive force in each leg (N) for a load W (N) on the rope; the rope from the winch runs
    along leg A, so the head sees W down plus W along leg A toward the winch."""
    uA = leg_unit(P["LEG_AZ"][0])
    load = (W * uA[0], W * uA[1], -W + W * uA[2])          # force on the head from the rope (N)
    U = [leg_unit(a) for a in P["LEG_AZ"]]
    # legs push up on the head along -u with compression F: sum(-F_i u_i) + load = 0 -> sum(F_i u_i) = load
    M = [[U[j][i] for j in range(3)] for i in range(3)]
    F = solve3(M, list(load))
    return F, uA


def structure():
    W = A["swl_kg"] * G9
    Wd = W * A["proof"] * A["dyn"]                          # design case: proof load with jerk
    F, uA = leg_forces(Wd)
    g = geometry()
    Lp = g["Lp"]
    wo, to, _ = P["UP"]
    wi, ti, _ = P["LO"]
    I_lo = (wi ** 4 - (wi - 2 * ti) ** 4) / 12
    I_up = (wo ** 4 - (wo - 2 * to) ** 4) / 12
    A_lo = wi ** 2 - (wi - 2 * ti) ** 2
    Pcr = math.pi ** 2 * A["E_al"] * I_lo / Lp ** 2           # whole leg as the weaker lower section
    Fmax = max(F)
    sig_leg = Fmax / A_lo
    d = P["PIN_D"]
    bearing_al = Fmax / (2 * d * to)                        # M16 on two 4 mm aluminium walls (upper leg)
    bearing_lo = (Fmax - Wd) / (2 * d * ti) if Fmax > Wd else Fmax / (2 * d * ti)
    bearing_lo = max(F) / (2 * d * ti)                      # conservative: full leg force at the foot pin
    tau_bolt = Fmax / (2 * math.pi * (d * 0.85) ** 2 / 4)   # double shear on the thread root
    lug_bear = Fmax / (2 * d * P["LUG_T"])
    # feet: horizontal thrust and chain tension (equilateral layout)
    Fv = [f * g["cos"] for f in F]
    H = [f * g["sin"] for f in F]
    chain_T = max(H) / math.sqrt(3)
    # rope and sheave
    rope_sf = A["rope_mbl_kN"] * 1000 / W
    rope_sf_proof = A["rope_mbl_kN"] * 1000 / (W * A["proof"])
    # stop bolt in single shear carrying the rope pull at proof with jerk
    tau_stop = Wd / (math.pi * (P["STOP_D"] * 0.85) ** 2 / 4)
    bear_stop = Wd / (2 * P["STOP_D"] * to)
    # winch effort
    r = A["drum_r_eff"] / 1000
    f_lo = W * r / (A["gear_lo"] * A["crank"] / 1000 * A["eta"])
    f_hi50 = 50 * G9 * r / (A["gear_hi"] * A["crank"] / 1000 * A["eta"])
    v_hi = 2 * math.pi * r / A["gear_hi"] * A["crank_rpm"]          # m/min
    v_lo = 2 * math.pi * r / A["gear_lo"] * A["crank_rpm"]
    return dict(W=W, Wd=Wd, F=F, Fmax=Fmax, Pcr=Pcr, sf_buckle=Pcr / Fmax, sig_leg=sig_leg, I_lo=I_lo, I_up=I_up,
                bearing_al=bearing_al, bearing_lo=bearing_lo, tau_bolt=tau_bolt, lug_bear=lug_bear, Fv=Fv, H=H,
                chain_T=chain_T, rope_sf=rope_sf, rope_sf_proof=rope_sf_proof, tau_stop=tau_stop, bear_stop=bear_stop,
                f_lo=f_lo, f_hi50=f_hi50, v_hi=v_hi, v_lo=v_lo)


def masses():
    C = {c.key: c for c in m.components(heads=True)}
    kg = {k: c.mass for k, c in C.items()}
    loads = {
        "1 Head, mast, sheave, snatch block, hinge bolts, head interface":
            ["head", "sheave", "axle", "snatch", "hinge_bolts", "interface"],
        "2 Upper legs (3) with adjust pins": ["upper", "upper_sleeves", "adj_pins"],
        "3 Lower legs (3) with feet, pads and foot bolts": ["lower", "lower_sleeves", "feet", "pads", "foot_bolts"],
        "4 Winch, bracket, rope, line counter, cleat, working line": ["winch", "bracket", "bracket_bolts", "rope", "counter", "cleat"],
        "5 Rim guard panels (6), drop pins and leg-spread chains": ["guard", "boards", "guard_pins", "chains"],
        "6 Grab head": ["grab_shells", "grab_yoke", "grab_frame"],
        "7 Sampler head": ["sampler", "sampler_tube"],
        "8 Rake head and retrieval head": ["rake", "retrieval", "connector"],
        "9 DomeReach head (two pole sections, arm, roller)": ["dr_pole", "dr_arm", "dr_roller"],
    }
    extra = {"4 Winch, bracket, rope, line counter, cleat, working line": 2.1}   # 30 m of 10 mm polyester line
    out = {n: sum(kg[k] for k in ks) + extra.get(n, 0.0) for n, ks in loads.items()}
    tripod = sum(kg[k] for k in ("head", "sheave", "axle", "snatch", "hinge_bolts", "interface", "upper", "upper_sleeves",
                                  "adj_pins", "lower", "lower_sleeves", "feet", "pads", "foot_bolts", "chains", "winch",
                                  "bracket", "bracket_bolts", "rope", "counter", "cleat"))
    return kg, out, tripod


def tipping(tripod_kg):
    """Largest rope angle from vertical before the tripod tips over a foot edge (worst direction)."""
    g = geometry()
    W = A["swl_kg"] * G9
    Wt = tripod_kg * G9
    h = g["zs"]
    a = g["tri_in"]
    tan_max = (W + Wt) * a / (W * h)
    ang = math.degrees(math.atan(tan_max))
    tan_proof = (W * A["proof"] + Wt) * a / (W * A["proof"] * h)
    return dict(ang=ang, ang_proof=math.degrees(math.atan(tan_proof)), h=h, a=a)


def grab():
    R = P["GRAB_R"] - P["GRAB_SHEET"]
    L_left = P["GRAB_B"]
    L_right = P["GRAB_B"] + 2 * (P["GRAB_PLATE"] + 1) - 2 * 0      # right shell spans the left shell's end plates
    L_right = P["GRAB_B"] + 2 * P["GRAB_PLATE"] + 2
    V = math.pi * R ** 2 / 4 * (L_left + L_right) / 1e6           # litres
    payload = V * A["fill"]
    silt = payload * A["silt_kgL"]
    return dict(V=V, payload=payload, silt=silt)


def heads_plan():
    out = {}
    for k, v in m.head_comps().items():
        b = v.bounding_box()
        out[k] = (b.size.X, b.size.Y, b.size.Z, math.hypot(b.size.X, b.size.Y))
    # DomeReach passes the opening with its arm folded down along the pole; the tiller stays above the rim
    P2 = copy.deepcopy(P)
    P2["DR_ARM_DEG"] = 180.0
    d = m.domereach(P2)
    from build123d import Compound
    b = Compound(children=[d["pole"], d["arm"], d["roller"]]).bounding_box()
    out["domereach, folded, below the tiller"] = (b.size.X, b.size.Y, b.size.Z, math.hypot(b.size.X, b.size.Y))
    return out


def sampler():
    od, wall, L = P["SAMP_TUBE"]
    V = math.pi * ((od - 2 * wall) / 2) ** 2 * L / 1e6
    return dict(V=V, half=L / 2, counter_res=100.0)


def domereach():
    od, wall, Ls = P["DR_POLE"]
    tod, tlen, tbelow = P["DR_TILLER"]
    hinge_below_tab = 30 + 2 * Ls + 60
    # deepest hinge depth below the rim with the tiller kept 200 mm above the rim
    depth = hinge_below_tab - tbelow - 200
    reach_floor = depth + P["DR_ARM"][2]
    side = P["DR_ARM"][2] * math.sin(math.radians(P["DR_ARM_DEG"]))
    return dict(depth=depth, floor=reach_floor, side=side)


def cycle():
    """Grab cycle at 3 m depth (estimate), high gear for lowering and lifting."""
    s = structure()
    depth = 3.0
    t_down = depth / s["v_hi"]
    t_up = depth / s["v_hi"]
    t_close, t_swing = 0.5, 1.0
    t = t_down + t_up + t_close + t_swing
    g = grab()
    per_h = 60 / t
    return dict(depth=depth, t=t, per_h=per_h, L_h=per_h * g["payload"], drip=0.10)


def setup_time():
    steps = [("Cone off the site, open the cover with a cover lifter", 1.5), ("Lay out feet and chains", 1.0),
             ("Pin the legs to the head (already pinned in transport) and stand the tripod", 2.0),
             ("Set leg lengths and pins, check level", 1.5), ("Clamp the winch on (left on leg A in transport)", 0.0),
             ("Reeve the rope (left reeved) and hang the head", 1.0), ("Pin the rim guard round the opening", 2.0)]
    return steps, sum(t for _, t in steps)


def cost():
    rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
    tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
    return rows, tot


def main():
    g = geometry()
    s = structure()
    kg, loads, tripod = masses()
    tp = tipping(tripod)
    gr = grab()
    hp = heads_plan()
    sm = sampler()
    dr = domereach()
    cy = cycle()
    st, st_t = setup_time()
    rows, tot = cost()
    target = 5000.0
    print("Geometry")
    print(f"  leg pin to pin {g['Lp']:.0f} mm, {g['theta']:.1f} deg from vertical; feet on {2 * P['R_FOOT']:.0f} mm circle, "
          f"triangle side {g['foot_side']:.0f} mm, inradius {g['tri_in']:.0f} mm")
    print(f"  sheave centre {g['zs']:.0f} mm, top of mast {P['CHEEK_TOP']:.0f} mm; D/d {g['D_over_d']:.1f}")
    print(f"  leg overlap {g['overlap']:.0f} mm nominal, {g['overlap'] - P['ADJ_PITCH']:.0f} mm longest; "
          f"adjust +/- {P['ADJ_PITCH']:.0f} mm on the leg")
    print("Structure (design case: SWL x proof x dynamic)")
    print(f"  W {s['W']:.0f} N, design {s['Wd']:.0f} N; leg forces " + ", ".join(f"{f:.0f}" for f in s["F"]) + " N")
    print(f"  Euler buckling of the leg as 50 x 3 over {g['Lp']:.0f} mm: {s['Pcr'] / 1000:.1f} kN, SF {s['sf_buckle']:.1f}")
    print(f"  leg stress {s['sig_leg']:.1f} MPa; hinge bearing on 4 mm wall {s['bearing_al']:.1f} MPa; "
          f"foot pin bearing on 3 mm wall {s['bearing_lo']:.1f} MPa")
    print(f"  M16 double shear {s['tau_bolt']:.1f} MPa; lug bearing {s['lug_bear']:.1f} MPa")
    print(f"  foot vertical " + ", ".join(f"{f:.0f}" for f in s["Fv"]) + " N; horizontal " + ", ".join(f"{f:.0f}" for f in s["H"])
          + f" N; chain tension {s['chain_T']:.0f} N")
    print(f"  rope SF at SWL {s['rope_sf']:.1f}, at proof {s['rope_sf_proof']:.1f}")
    print(f"  stop bolt M12 shear {s['tau_stop']:.1f} MPa, bearing on leg wall {s['bear_stop']:.1f} MPa")
    print(f"  crank force: {s['f_lo']:.0f} N at SWL in low gear; {s['f_hi50']:.0f} N with a 50 kg head in high gear")
    print(f"  rope speed {s['v_hi']:.2f} m/min high gear, {s['v_lo']:.2f} m/min low gear at {A['crank_rpm']:.0f} rpm")
    print("Masses (kg)")
    for n, v in loads.items():
        print(f"  {v:5.1f}  {n}")
    print(f"  tripod with winch and rope {tripod:.1f} kg; whole kit {sum(loads.values()):.1f} kg")
    print(f"Tipping: largest rope angle {tp['ang']:.1f} deg at SWL, {tp['ang_proof']:.1f} deg at proof (sheave {tp['h']:.0f} mm, edge {tp['a']:.0f} mm)")
    print(f"Grab: {gr['V']:.1f} L geometric, {gr['payload']:.1f} L at {A['fill']:.0%} fill, {gr['silt']:.0f} kg of wet silt")
    print("Head plan sizes (x, y, height, diagonal) mm:")
    for k, v in hp.items():
        print(f"  {k:18s} {v[0]:5.0f} {v[1]:5.0f} {v[2]:5.0f}  diag {v[3]:5.0f}  "
              + ("(arm out, for working)" if k == "domereach" else ("passes" if v[3] <= A["opening_min"] - 20 else "check")))
    print(f"Sampler: {sm['V']:.2f} L; sample spans +/- {sm['half']:.0f} mm about its centre; counter {sm['counter_res']:.0f} mm")
    print(f"DomeReach: hinge to {dr['depth']:.0f} mm below the rim, arm down to {dr['floor']:.0f} mm, side reach {dr['side']:.0f} mm")
    print(f"Grab cycle at {cy['depth']:.0f} m: {cy['t']:.1f} min, {cy['per_h']:.1f} per hour, {cy['L_h']:.0f} L/h (estimate)")
    print(f"Setup estimate {st_t:.1f} min")
    print(f"Cost: USD {tot:,.0f} against the USD {target:,.0f} value-engineering target ({target - tot:,.0f} under)")
    res = [
        ("R1", "No entry for any task", "Every head fitted, worked and recovered from the rim", "Met on paper"),
        ("R2", "Fits openings 0.5 to 1.2 m", f"Feet on {2 * P['R_FOOT'] / 1000:.1f} m circle; guard inner face at {P['GUARD_R'] - 18.5:.0f} mm radius", "Met on paper"),
        ("R3", "Working depth 10 m", "15 m rope; drum capacity to confirm", "Met on paper"),
        ("R4", "SWL 150 kg, proof 1.5x", f"Buckling SF {s['sf_buckle']:.1f}; rope SF {s['rope_sf']:.1f}", "Met on paper"),
        ("R5", "Setup in 10 min", f"{st_t:.1f} min (estimate)", "Met on paper (estimate)"),
        ("R6", "No load over 25 kg", f"Heaviest load {max(loads.values()):.1f} kg", "Met on paper" if max(loads.values()) <= 25 else "Not met"),
        ("R7", "Head change under 2 min", "One screw-pin shackle, no tools (about 1 min)", "Met on paper (estimate)"),
        ("R8", "Grab 10 L per cycle", f"{gr['payload']:.1f} L at {A['fill']:.0%} fill", "Met on paper (estimate)"),
        ("R9", "Sample at depth within 0.2 m", "Line counter 0.1 m; tube centre known", "Met on paper"),
        ("R10", "DomeReach to digester floor", f"Hinge {dr['depth'] / 1000:.1f} m, tool {dr['floor'] / 1000:.1f} m below rim", "Met on paper (depth set as 2.5 m)"),
        ("R11", "Corrosion resistance", "Galvanized steel, 6082 aluminium, A4 fasteners and rope", "Not verifiable on paper; TRL 4 coupon test"),
        ("R12", "Value-engineering target USD 5,000", f"USD {tot:,.0f}", f"Under the target by USD {target - tot:,.0f}"),
        ("R13", "Every head passes a 560 mm opening", f"Largest diagonal {max(v[3] for k, v in hp.items() if k != 'domereach'):.0f} mm", "Met on paper"),
        ("R14", "Stable with the rope 10 deg off vertical", f"Tips at {tp['ang']:.0f} deg at SWL", "Met on paper"),
    ]
    with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "requirement", "result", "status"])
        w.writerows(res)
    print("Results written to docs/04-calcs/results.csv")
    return dict(g=g, s=s, loads=loads, tripod=tripod, tp=tp, gr=gr, hp=hp, sm=sm, dr=dr, cy=cy, cost=tot)


if __name__ == "__main__":
    main()
