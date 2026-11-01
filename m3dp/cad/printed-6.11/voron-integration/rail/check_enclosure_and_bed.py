"""Reference350 enclosure clearance for the raised-rail prototype.

Official250 source is resized by the configurator's100mm increments, not by
scaling hardware. Actual bed edge, gantry stroke and panel fit remain measured
commissioning inputs. No Klipper coordinates are generated here.
"""
from pathlib import Path
import importlib.util,json
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common
from OCC.Core.gp import gp_Pnt
from front_bracket_geometry import geometry,RAIL_Y,RAIL_Z
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',HERE/'cad_checks.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def box(p,s):return BRepPrimAPI_MakeBox(gp_Pnt(*p),*s).Shape()
def intersection(a,b):return v.volume(BRepAlgoAPI_Common(a,b).Shape())
bed_front=-456.0064116881106
bed_top=-78.08598871886406
door_inner=-496.0064116881959
front_frame_bottom=-136.09598881885788
front_frame_top_bottom=373.90401138135854
roof_bottom=394.9040112811351
mgn_z=-.0865699
nozzle_z=mgn_z-13.5-55.5
nozzle_y=-424.15338596084644-24.52053-17.70108593
dock_y0=nozzle_y-14.655
dock_z0=nozzle_z+43
pad_rear=dock_y0+21.153684484622
zshift_zero=bed_top-nozzle_z
zshift_min=zshift_zero-5
zshift_max=zshift_zero+310
# Full-height boxes conservatively bound both closed door leaves/front posts.
fixed=[('closed_doors',box((-242,door_inner-3,-123),(484,3,504))),
       ('left_front_post',box((-255,-496.0064117,front_frame_bottom),(20,20,530))),
       ('right_front_post',box((235,-496.0064117,front_frame_bottom),(20,20,530))),
       ('front_lower_crossbar',box((-235,-496.0064117,front_frame_bottom),(470,20,20))),
       ('front_upper_crossbar',box((-235,-496.0064117,front_frame_top_bottom),(470,20,20))),
       ('top_panel',box((-242,-483.006339,roof_bottom),(484,484,3)))]
overlaps=[]
for side in ['left','right']:
    design=geometry(side);primitives=list(design['boxes'])
    for triangle in design['gussets']:
        vertices=triangle['vertices']+[tuple(p[i]+triangle['direction'][i] for i in range(3)) for p in triangle['vertices']]
        p=tuple(min(v[i] for v in vertices) for i in range(3))
        size=tuple(max(v[i] for v in vertices)-p[i] for i in range(3))
        primitives.append((triangle['name']+'BoundingBox',p,size))
    for name,p,size in primitives:
        # Sweeping each primitive without its holes is conservative.
        swept=box((p[0],p[1],p[2]+zshift_min),(size[0],size[1],size[2]+zshift_max-zshift_min))
        for feature,obstacle in fixed:
            value=intersection(swept,obstacle)
            if value>.0001:overlaps.append({'side':side,'part':name,'obstacle':feature,'mm3':value})
rail_swept=box((-200,RAIL_Y-10,RAIL_Z-10+zshift_min),(400,20,20+zshift_max-zshift_min))
for feature,obstacle in fixed:
    value=intersection(rail_swept,obstacle)
    if value>.0001:overlaps.append({'part':'new400mmrail','obstacle':feature,'mm3':value})
head_top_hardware=RAIL_Z+16+1+2.75
report={'status':'pass' if not overlaps else 'fail','configured_Z_test_range_mm':[-5,310],
        'coordinate_frame':'rear crossbrace center, X across, +Y rearward, +Z upward',
        'rail_center_mm':[0,RAIL_Y,RAIL_Z],'rail_cut_length_mm':400,
        'rail_in_dock_source_frame':{'Y':[65,85],'Z':[-11.5,8.5]},
        'adapter_standoff_mm':11,'front_joint_precontact_margin_mm':4,
        'parked_nozzle_y_mm':nozzle_y,'physical350_bed_front_y_mm':bed_front,
        'nozzle_pad_rear_y_mm':pad_rear,'pad_to_bed_front_clearance_mm':bed_front-pad_rear,
        'pad_bottom_below_active_nozzle_mm':7.3,
        'bare_rail_to_closed_door_inner_face_mm':RAIL_Y-10-door_inner,
        'top_clamp_with_1mm_washer_and_M5_button_head_z_mm':head_top_hardware,
        'top_hardware_to_front_crossbar_at_Z310_mm':front_frame_top_bottom-(head_top_hardware+zshift_max),
        'roof_bottom_z_mm':roof_bottom,'gantry_shift_at_Z0_mm':zshift_zero,
        'gantry_shift_at_Z310_mm':zshift_max,
        'swept_support_and_rail_enclosure_overlaps':overlaps,
        'limitations':['This is a reference-model fit check, not physical qualification.',
                       'Measure actual bed size/edge, closed doors, Z travel and all cable loops before commissioning.',
                       'Final blower/duct integration is checked separately; no full350mm printable-area promise is made.']}
(HERE/'raised-rail-enclosure-and-bed-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2));assert not overlaps
