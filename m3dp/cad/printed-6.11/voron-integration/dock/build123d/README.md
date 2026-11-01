# build123d 2510 cage fit coupon — 4.6 mm inserts

A parametric recreation of the existing 2510 cage coupon. Geometry is built from
primitives; the existing STEP is used only for verification.

## Files

- `2510-cage-fit-coupon-build123d-4p6.stl` — print this coupon at 100% scale.
  The front lip is on Z=0; bounding size is 42 × 29 × 11.8 mm.
- `2510-cage-fit-coupon-build123d-4p6.step` — editable solid for Fusion or other
  CAD software, retaining the original dock coordinates.
- `build_2510_cage_fit_coupon.py` — parameterized build123d source.
- `verification.json` — reference/output hashes, dimensions and validation.
- `2510-cage-fit-coupon-build123d-4p6.png` — preview.

## Verified geometry

Two insert seats are 4.6 mm diameter and 5.8 mm deep, centered at (31, -24)
and (65, -16) in the dock datum. Each has a coaxial 3.4 mm screw-tip relief
extending a further 2.5 mm below the insert seat, with a 3.5 mm bottom floor.

The cage retains the 29 mm outer size, 25.3 mm cavity, 1.85 mm walls,
10 mm fan depth, 1 mm front lip, 24 mm airflow opening, cable relief, and
two raised retainer keys.

Against `../2510-cage-fit-coupon.step`, exact Boolean comparison reported
zero added and removed material. Volume is 3552.558952443813 mm³; bounds and
mass properties match. The rebuilt solid has 40 faces versus the reference's
68 because coplanar subdivisions were removed. The tool's separate mesh
sampler flagged tessellation differences; these are recorded in the receipt.

The saved source was executed successfully. The final model passed B-rep and
mesh validation as one watertight manifold solid. The STEP also passed the
written-and-reimported gate. Varying only the insert diameter by ±10% rebuilt
valid solids; this was not a full parameter audit.

## Print note

The original 6 mm wide raised keys leave 0.7 mm of material on each side of a
4.6 mm insert hole. The printability check flagged this as thinner than two
0.4 mm nozzle perimeters. Review these small regions in the slicer preview.
The recreation preserves this reference geometry.

On 2026-10-30, the user reported printing
`2510-cage-fit-coupon-build123d-4p6.stl` and that the fan fit perfectly.
Fan body fit is confirmed for this print.

On 2026-10-31, the user reported that the installed cage retainers fit great.
Retainer fit is confirmed for this assembly. Insert retention, clamping strength,
torque/pullout, cable exit clearance, and heated operation remain unreported.

## Regenerate

Tested with build123d 0.13.0 and build123d-mcp 0.3.91.

1. Use build123d-mcp `execute_file` with the absolute path to
   `build_2510_cage_fit_coupon.py`. It registers `cage_rebuilt` in dock
   coordinates and `cage_print` translated by (-27, 30.5, 11.5) mm.
2. Use `validate` on `cage_print`.
3. Use `bank_candidate` with `object_name="cage_rebuilt"` and the STEP
   output filename; this validates the written STEP before accepting it.
4. Use `export` with `object_name="cage_print"`, `format="stl"`, and
   the STL output filename.
