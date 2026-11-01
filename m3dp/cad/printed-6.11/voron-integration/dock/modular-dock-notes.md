# Raised front-rail paired docks — prototype

This version holds six tools in three identical two-station modules on a raised 2020 rail attached to the moving gantry. It preserves the corrected 6.11 latch, pin and nozzle-pad geometry. The earlier low saddle and front-mounted fan carrier are historical prototypes, not the primary assembly.

The pair uses **34 mm internal station spacing** and **38 mm between pairs**, with a **72 mm repeat**. Three pairs occupy 216 mm at the dock bodies; the staggered fan-clamp ear extends the complete plastic envelope to **221 mm**. The final gantry supports use a **400 mm 2020 crossrail**; do not use the 216 mm dock-body span as the rail cut length.

## Print quantities

| Primary file | Six-tool quantity |
|---|---:|
| `two-station-dock.stl` — raised hanger, dock pair and two fan cages together | 3 |
| `fan-retainer-left.stl` | 3 |
| `fan-retainer-middle.stl` | 3 |
| `fan-retainer-right.stl` | 3 |
| `2510-cage-fit-coupon.stl` | 1 initially |
| `raised-2020-saddle-fit-coupon.stl` | 1 initially |

The coupon STLs are in `stl/coupons/`; production STLs are in `stl/`. Print the coupons in the same **ASA**, orientation and settings intended for production. Reuse the left and middle retainer designs on the fan coupon. The main module's front-face-down orientation leaves the original nozzle fingers above the bed: review and place slicer supports beneath those overhangs. Keep supports off the latch seats and pad-contact surfaces where possible. The supplied orientation is a starting point, not proof of a successful print.

The primary native document is explicitly named `two-station-raised-rail-dock-prototype.FCStd`. Its imported source and editable primitive/Boolean features remain in the tree. `BuildRaisedDockCarrier.FCMacro` uses the bundled `raised-carrier-spec.json` and `source-two-station-dock-34mm.brep`; `VerifyRaisedDockCarrier.FCMacro` checks uniquely named copies without changing the original native files.

## Raised rail and fastening

Coordinates below are the original dock frame: X runs along the row, Y is vertical, and positive Z is rearward into the printer. The 2020 rail occupies **Y65–85, Z−11.5–8.5**. The hanger's upper bearing face seats directly on **Y85**; do not put a spacer under that face without recalculating the nozzle height. The lower shelf and rear wall have 0.15 mm nominal insertion clearance. All added material stays at or behind Z−11.5.

Use **two top M3 clamps per pair: six screws and six compatible 2020 M3 T-nuts total**. The clamp bores are Ø3.4 mm. Use the saddle coupon and the actual extrusion/T-nut to determine screw length: under-head distance to the top rail face is **3.5 mm** with the specified 0.5 mm washer; add the measured slot/thread recess and required engagement, then check for bottoming out. Existing screw sizes may be suitable. The upper socket-head envelope ends at Y91.5 with a 3 mm head and 0.5 mm washer. The original lower saddle holes are not the raised-rail clamps.

The final reference placement uses the 11 mm TAP adapter at the original head height and parks the MGN carriage 2 mm farther rearward. It retains calculated door and nozzle-pad/bed gaps of approximately 3.476 mm and 3.870 mm, respectively. These are source-CAD values, not measured printer clearances. The global gantry support placement must be checked with that final TAP adapter and head pose. A change of head height or fore/aft offset changes door, bed and frame clearance even though these local dock dimensions are unchanged. Keep the stock enclosure; do not resolve a fit problem by moving parked nozzles over the physical bed.

## Fan cages and rear retainers

Use the **six already purchased 24 V 2510 fans**; the seventh fan is assigned to the active head. The cages assume a nominal 25×25×10 mm body, a 25.3×25.3 mm internal opening and a 10 mm axial stack. The front retaining lip is 1 mm thick, with a Ø24 mm airflow opening. The fan body occupies Z−10.5 to−0.5; there is only **0.5 mm modeled clearance to the dock's front plane**, so actual fit must be checked with the coupon and a dock before printing all three modules. Do not assume every purchased fan matches the source CAD. Adjust only the measured cage-fit dimensions; do not scale the whole dock and its latch geometry.

The cage holds the fan perimeter, so its screw-hole pitch is not used. Orient the fan's airflow toward the parked heatsink (+dock Z), confirm the arrow on the actual fan, and rotate the body so the cable exits the lower-right relief without being pinched. Fit the three keyed rear retainers: the middle one holds the adjacent edges of both fans; the staggered outer retainers avoid the neighboring pair.

For the complete row use **nine M3×8 retainer screws, nine M3 washers (≤7 mm OD, 0.5 mm thick), and nine of the purchased M3 heat-set inserts (5 mm OD ×4 mm long)**. These are stock checks, not instructions to purchase duplicates. The user selected **Ø4.6 mm (`4p6`)** after the sleeve-coupon comparison: `4p6` was preferred cold, `4p5`/`4p6` were reported best after heat-setting and cooling, and screws passed through easily. The three named `InsertTrialBore` radii (left, middle and right) are 2.3 mm, with the same radius in the cage coupon's left and middle seats. The separate retainers retain their Ø3.4 mm screw clearance holes. Install each insert flush with the raised key face. In the nominal stack, an 8 mm screw passes through the 2 mm retainer and 0.5 mm washer, fully engages the 4 mm insert and enters the provided tip relief without bottoming out. Check this on the cage coupon; the sleeve results do not establish retention in the dock bosses, and torque/pullout, repeat-coupon and thermal-performance results remain unreported. Do not overtighten the thin fan housing.

The purchased fan current is still unverified. Read its label before using the proposed three-fan-per-EBB output wiring. Keep wiring outside the latch, actuator, moving head and enclosure sweeps. Route fan leads along the sides of the hanger legs within the available depth, and keep wires and fixings behind Z−11.5; wrapping a tie over the front face would spend the door clearance.

## Qualification still required

For the 4.6 mm bore revision, `m3dp/cad/printed-6.11/insert-bore-4p6-validation.json` is the authoritative validation record and supersedes affected earlier geometry checks. Consult its recorded status and scope; the following describes the baseline integration checks.

The source geometry checks preserve the latch/pin region and separate adjacent modules. Against the final11 head candidate, all twelve checked docking snapshots introduce no collision with the raised hanger, fans, retainers, detector bodies, fastener envelopes or neighboring parked tools. At the maximum 0.85 mm axial press, the replacement duct clears the neighboring lower coupling pins by 0.776 mm and the conservative actuator-pin envelope by 0.806 mm. These small margins require physical confirmation; they are not a clearance guarantee for unmodeled cables or different hardware. They do not establish ASA stiffness, heated creep, cooling performance, vibration durability, actual fan dimensions, cable clearance or the full articulated arm motion. The maximal 0.85 mm axial compression of the source latch cannot be treated as a rigid-head motion: the original closed-arm bearing itself touches the original dock at that extreme.

Before powered tool changes, verify the coupons, assemble one pair, check the fan-to-finger clearance both unloaded and while pressing the silicone nozzle pad, and move the unheated mechanism manually through release and pickup with neighboring tools installed. Check rail stiffness under the actual actuator load. Then validate cooling and repeated heated cycles before printing with this experimental assembly. Retain a physical clearance margin from the stock doors, bed, gantry joints and upper frame using the final whole-printer layout.
