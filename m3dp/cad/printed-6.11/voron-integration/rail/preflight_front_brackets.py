"""OCC validation against original idlers, belts and conservative head sweep."""
from pathlib import Path
import importlib.util,json,math
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox,BRepPrimAPI_MakeCylinder,BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse,BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform,BRepBuilderAPI_MakePolygon,BRepBuilderAPI_MakeFace
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.gp import gp_Pnt,gp_Dir,gp_Ax1,gp_Ax2,gp_Trsf,gp_Vec
from OCC.Extend.TopologyUtils import TopologyExplorer
from front_bracket_geometry import geometry,RAIL_Y,RAIL_Z
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',HERE/'cad_checks.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def box(p,s):return BRepPrimAPI_MakeBox(gp_Pnt(*p),*s).Shape()
def read(name):
    s=TopoDS_Shape();breptools.Read(s,str(HERE/'reference'/name),BRep_Builder());return s
def move(s,x=0,y=0,z=0):
    t=gp_Trsf();t.SetTranslation(gp_Vec(x,y,z));return BRepBuilderAPI_Transform(s,t,True).Shape()
def normalized(s):
    t=gp_Trsf();t.SetRotation(gp_Ax1(gp_Pnt(),gp_Dir(0,0,1)),-math.pi/2)
    return move(BRepBuilderAPI_Transform(s,t,True).Shape(),163,-8.49958338,-33.40599583)
def overlap(a,b):return all(a[i]<b[i+3]-1e-6 and b[i]<a[i+3]-1e-6 for i in range(3))
def intersection(a,b):return v.volume(BRepAlgoAPI_Common(a,b).Shape())
def cylinder(p,r,h):return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*p),gp_Dir(0,0,1)),r,h).Shape()
head_low=box((-204.45,-481.03001,-69.11658),(428.45,428,108.03001))
head_upper=box((-204.45,-466.673916,38.91343),(428.45,414,80))
rail=box((-200,RAIL_Y-10,RAIL_Z-10),(400,20,20))
rows=[]
for side,idler,placed in [('left','B',9),('right','A',20)]:
    design=geometry(side);shape=None
    for name,p,s in design['boxes']:
        part=box(p,s);shape=part if shape is None else BRepAlgoAPI_Fuse(shape,part).Shape()
    for triangle in design['gussets']:
        wire=BRepBuilderAPI_MakePolygon()
        for p in triangle['vertices']:wire.Add(gp_Pnt(*p))
        wire.Close()
        rib=BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(wire.Wire()).Face(),gp_Vec(*triangle['direction'])).Shape()
        shape=BRepAlgoAPI_Fuse(shape,rib).Shape()
    for name,p,r,h,d in design['holes']:
        hole=BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*p),gp_Dir(*d)),r,h).Shape()
        shape=BRepAlgoAPI_Cut(shape,hole).Shape()
    assert BRepCheck_Analyzer(shape).IsValid()
    assert len(list(TopologyExplorer(shape).solids()))==1
    breptools.Write(shape,str(HERE/('front-rail-support-'+side+'-preflight.brep')))
    x=1 if side=='right' else -1
    belt=box((233.56083 if x==1 else -234.94087,-456.60633,-100),(1.38004,9,650))
    results={'head_lower_conservative_full_xy_sweep':intersection(shape,head_low),
             'head_upper_conservative_full_xy_sweep':intersection(shape,head_upper),
             'new_rail_exterior':intersection(shape,rail),'vertical_z_belt_full_height':intersection(shape,belt)}
    fixed=read('Front-Idler-'+idler+'-350.brep')
    kept=[p for p in TopologyExplorer(fixed).solids() if not 437<v.volume(p)<438]
    results['stock_idler_excluding_replaced_M5_screws']=sum(intersection(shape,p) for p in kept)
    joint=move(normalized(read('placed-'+str(placed)+'.brep')),50*x)
    sb=v.bbox(shape);parts=[(s,v.bbox(s)) for s in TopologyExplorer(joint).solids()]
    hardware=[cylinder((p[0],p[1],p[2]+24),4.75,2.75) for p in design['mounting_axes']]
    for xpos in [182*x,194*x]:
        hardware.extend([cylinder((xpos,RAIL_Y,RAIL_Z+16),5,1),cylinder((xpos,RAIL_Y,RAIL_Z+17),4.75,2.75)])
    hw=[(s,v.bbox(s)) for s in hardware]
    continuous_bounds_overlap=0
    for _,pb in parts:
        swept_bounds=box((pb[0],pb[1]-228.146484375,pb[2]),
                         (pb[3]-pb[0],pb[4]-pb[1]+228.146484375+127.873046875,pb[5]-pb[2]))
        if overlap(sb,v.bbox(swept_bounds)):
            continuous_bounds_overlap+=intersection(shape,swept_bounds)
        for metal,mb in hw:
            if overlap(mb,v.bbox(swept_bounds)):
                continuous_bounds_overlap+=intersection(metal,swept_bounds)
    worst=0;worst_y=None;hardware_worst=0
    # Only near the front limit can a joint meet these front-mounted parts.
    # Test0.5mm samples plus exact physical example endpoints.
    for distance in [*range(0,210,10),*[210+i*.5 for i in range(37)],228.146484375]:
        total=0;hardware_total=0
        for part,pb in parts:
            b=pb[:];b[1]-=distance;b[4]-=distance
            if overlap(sb,b):total+=intersection(shape,move(part,y=-distance))
            for metal,mb in hw:
                if overlap(mb,b):hardware_total+=intersection(metal,move(part,y=-distance))
        if total>worst:worst=total;worst_y=distance
        hardware_worst=max(hardware_worst,hardware_total)
    results['xy_joint_front_sweep_max']=worst
    results['new_button_heads_and_washers_to_xy_joint_sweep_max']=hardware_worst
    row={'side':side,'valid':True,'volume_mm3':v.volume(shape),'bbox_mm':v.bbox(shape),
         'overlaps_mm3':results,'worst_joint_forward_translation_mm':worst_y,
         'conservative_continuous_joint_solid_bbox_sweep_overlap_mm3':continuous_bounds_overlap,
         'replacement_screw_axes':design['mounting_axes']}
    rows.append(row);print(json.dumps(row),flush=True)
    assert continuous_bounds_overlap<.001,(side,continuous_bounds_overlap)
(HERE/'front-bracket-preflight.json').write_text(json.dumps(rows,indent=2))
assert max(v for r in rows for v in r['overlaps_mm3'].values())<0.001,rows
