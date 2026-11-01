"""Prototype raised-rail pair hanger; all coordinates retain the dock datum."""
import json,math
from pathlib import Path
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox,BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse,BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.STEPControl import STEPControl_Writer,STEPControl_AsIs
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.gp import gp_Pnt,gp_Ax2,gp_Dir,gp_Trsf
from OCC.Extend.TopologyUtils import TopologyExplorer
OUT=Path(__file__).resolve().parent
INSERT_BORE=4.6  # Selected from the user's heat-set/cool-down coupon test (4p6).
def box(n,x,y,z,dx,dy,dz):return dict(type='box',name=n,values=[x,y,z,dx,dy,dz])
def cyl(n,x,y,z,r,h,axis=(0,0,1)):return dict(type='cylinder',name=n,values=[x,y,z,r,h],axis=axis)
def primitive(o):
 v=o['values']
 return BRepPrimAPI_MakeBox(gp_Pnt(*v[:3]),*v[3:]).Shape() if o['type']=='box' else BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*v[:3]),gp_Dir(*o['axis'])),*v[3:]).Shape()
def read(p):
 s=TopoDS_Shape();breptools.Read(s,str(p),BRep_Builder());return s
def volume(s):
 p=GProp_GProps();brepgprop.VolumeProperties(s,p);return p.Mass()
def bbox(s):
 b=Bnd_Box();brepbndlib.AddOptimal(s,b);return list(b.Get())
def fuse(items):
 s=items[0]
 for q in items[1:]:s=BRepAlgoAPI_Fuse(s,q).Shape()
 return s
add=[box('TopBearingPlate',26,85,-11.5,72,3,22.5),box('RearSpine',26,61.85,8.65,72,26.15,2.35),box('LowerRailShelf',26,61.85,-11.5,72,3,22.5)]
cut=[]
for i,x in enumerate([31.7,65.7],1):
 add.append(box(f'FrontLeg{i}',x-3.5,-2.15,-11.5,7,64.3,9))
 add.append(box(f'UpperLegGusset{i}',x-3.5,31,-2.5,7,31.15,6.5))
 cut.append(cyl(f'TopClamp{i}',x,84.9,-1.5,1.7,3.2,(0,1,0)))
# Front rings support fan faces without any front protruding hardware.
for i,x in enumerate([48,82],1):
 add += [box(f'Fan{i}FrontLip',x-14.5,-30.5,-11.5,29,29,1),
         box(f'Fan{i}LeftWall',x-14.5,-30.5,-10.5,1.85,29,10),
         box(f'Fan{i}RightWall',x+12.65,-30.5,-10.5,1.85,29,10),
         box(f'Fan{i}BottomWall',x-14.5,-30.5,-10.5,29,1.85,10),
         box(f'Fan{i}TopWall',x-14.5,-3.35,-10.5,29,1.85,10),
         box(f'Fan{i}UpperTie',x-14.5,-2,-11.5,29,7,2.5)]
 cut.append(cyl(f'Fan{i}AirWindow',x,-16,-11.6,12,1.2))
 cut.append(box(f'Fan{i}CableExit',x+10.5,-31.5,-10.5,5,5,10.1))
# Stagger outer retainers, so adjoining modules have no overlapping clamp ears.
bosses=[('Left',31,-24),('Middle',65,-16),('Right',99,-8)]
for n,x,y in bosses:
 add.append(box(n+'RetainerBoss',x-4,y-5,-11.5,8,10,11))
 add.append(box(n+'RetainerKey',x-3,y-4,-.5,6,8,.8))
 cut.append(cyl(n+'InsertTrialBore',x,y,-5.5,INSERT_BORE/2,6))
 cut.append(cyl(n+'ScrewTipRelief',x,y,-8,1.7,8.5))
retainers=[]
for n,x,y in bosses:
 lo,hi={'Left':(27,36.5),'Middle':(59.5,70.5),'Right':(93.5,103)}[n]
 ymin,ymax=(-29,-3)if n=='Middle' else(y-5,y+5)
 retainers.append({'basename':'fan-retainer-'+n.lower(),'add':[box(n+'Retainer',lo,ymin,-.5,hi-lo,ymax-ymin,2)],'cut':[box(n+'KeyPocket',x-3.1,y-4.1,-.6,6.2,8.2,1),cyl(n+'RetainerBolt',x,y,-.6,1.7,2.2)]})
spec={'source_dock':'source-two-station-dock-34mm.brep','rail_bbox':[26,65,-11.5,98,85,8.5],'fan_body_bbox_per_station':[[35.5,-28.5,-10.5,60.5,-3.5,-.5],[69.5,-28.5,-10.5,94.5,-3.5,-.5]],'designs':[{'basename':'two-station-raised-rail-dock-prototype','source':True,'add':add,'cut':cut}]+retainers}
coupon_add=[o for o in add if (o['name'].startswith('Fan1') and o['name']!='Fan1UpperTie') or o['name'].startswith(('LeftRetainer','MiddleRetainer'))]
coupon_cut=[o for o in cut if o['name'].startswith(('Fan1','LeftInsert','LeftScrew','MiddleInsert','MiddleScrew'))]
spec['designs'].append({'basename':'2510-cage-fit-coupon','add':coupon_add,'cut':coupon_cut})
spec['designs'].append({'basename':'raised-2020-saddle-fit-coupon','add':[box('CouponTop',0,85,-11.5,24,3,22.5),box('CouponBack',0,61.85,8.65,24,26.15,2.35),box('CouponBottom',0,61.85,-11.5,24,3,22.5)],'cut':[cyl('CouponClamp',12,84.9,-1.5,1.7,3.2,(0,1,0))]})
(OUT/'raised-carrier-spec.json').write_text(json.dumps(spec,indent=2))
dock=read(OUT/spec['source_dock']);reports=[];finals={}
for d in spec['designs']:
 s=fuse(([dock]if d.get('source')else[])+[primitive(o)for o in d['add']])
 for o in d['cut']:s=BRepAlgoAPI_Cut(s,primitive(o)).Shape()
 r={'name':d['basename'],'valid':BRepCheck_Analyzer(s).IsValid(),'solids':len(list(TopologyExplorer(s).solids())),'volume':volume(s),'bbox':bbox(s)}
 assert r['valid'] and r['solids']==1,r
 breptools.Write(s,str(OUT/(d['basename']+'.brep')))
 w=STEPControl_Writer();w.Transfer(s,STEPControl_AsIs);w.Write(str(OUT/(d['basename']+'.step')))
 reports.append(r);finals[d['basename']]=s
carrier=finals[spec['designs'][0]['basename']]
rail=primitive(box('Rail',26,65,-11.5,72,20,20))
reports[0]['rail_overlap_mm3']=volume(BRepAlgoAPI_Common(carrier,rail).Shape())
protect=primitive(box('ProtectedDock',25,-60,0,74,100,35))
reports[0]['source_material_removed_mm3']=volume(BRepAlgoAPI_Cut(dock,carrier).Shape())
latch=primitive(box('LatchProtection',26,0,0,72,31,35))
reports[0]['latch_pin_region_added_mm3']=volume(BRepAlgoAPI_Common(BRepAlgoAPI_Cut(carrier,dock).Shape(),latch).Shape())
tr=gp_Trsf();tr.SetValues(1,0,0,72,0,1,0,0,0,0,1,0)
reports[0]['next_carrier_overlap_mm3']=volume(BRepAlgoAPI_Common(carrier,BRepBuilderAPI_Transform(carrier,tr,True).Shape()).Shape())
(OUT/'raised-carrier-occ-validation.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
