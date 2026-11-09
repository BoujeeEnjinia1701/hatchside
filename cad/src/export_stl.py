"""Export the HatchSide models as STL at 0.2 mm tolerance (kit 1.9).

Run from the repo root:  python cad/src/export_stl.py
Writes cad/stl/hatchside-assembly.stl (option A, made and bought parts; fasteners and weld beads are in the STEP files), hatchside-assembly-B.stl (option B), hatchside-tripod.stl and one
file per tool head. Printing is not the aim; the meshes are for viewing and for other tools.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "cad/src"), str(ROOT / ".kit")]
from build123d import Compound, export_stl  # noqa: E402
import model as M  # noqa: E402

TOL, ANG = 0.2, 0.5
OUT = ROOT / "cad/stl"


def write(name, parts):
    shapes = [p["shape"] for p in parts if p["kind"] in ("made", "bought")]
    f = OUT / f"{name}.stl"
    export_stl(Compound(shapes), str(f), tolerance=TOL, angular_tolerance=ANG)
    print(f.name, len(shapes), "parts", round(f.stat().st_size / 1e6, 1), "MB", flush=True)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    a = M.components("A")
    heads = {17: "grab", 18: "sampler", 19: "rake", 20: "retrieval", 21: "domereach"}
    for b, nm in heads.items():
        write(f"hatchside-head-{nm}", [p for p in a if p.get("bom") == b])
    write("hatchside-tripod", [p for p in a if p.get("bom") in range(1, 17)])
    write("hatchside-assembly", a)
    write("hatchside-assembly-B", M.components("B"))
