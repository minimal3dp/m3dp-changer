"""Independent PythonOCC check of the actual native/STEP exports; no model edits."""
from pathlib import Path
import json,hashlib
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace,BRepBuilderAPI_Transform
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox,BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Fuse,BRepAlgoAPI_Common
from OCC.Core.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
from OCC.Core.TopAbs import TopAbs_IN
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.gp import gp_Pnt,gp_Vec,gp_Trsf
from OCC.Extend.TopologyUtils import TopologyExplorer
R=Path(__file__).resolve().parent
OUT=R/'top-export-airway-validation.json'
def read(p):
 if p.suffix=='.step':
  r=STEPControl_Reader();assert r.ReadFile(str(p))==1;r.TransferRoots();return r.OneShape()
 s=TopoDS_Shape();breptools.Read(s,str(p),BRep_Builder());return s
def bbox(s):
 b=Bnd_Box();brepbndlib.AddOptimal(s,b);return list(b.Get())
def vol(s):
 g=GProp_GProps();brepgprop.VolumeProperties(s,g);return g.Mass()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def refine(shape):
 u=ShapeUpgrade_UnifySameDomain(shape,True,True,True);u.Build();return u.Shape()
def cap_fuse(a,b):
 op=BRepAlgoAPI_Fuse(refine(a),b);op.SetFuzzyValue(1e-6);op.Build();assert op.IsDone();return op.Shape()
source_path=R/'source/cx/original-4020-duct-assembly-reference.brep'
source=read(source_path)
source=max(TopologyExplorer(source).solids(),key=vol)
caps=[BRepPrimAPI_MakeBox(gp_Pnt(40.4,-87.3,-13.5),.8,19.6,30.6).Shape()]
jets=[]
for f in TopologyExplorer(source).faces():
 a=BRepAdaptor_Surface(f)
 if a.GetType()!=GeomAbs_Plane or bbox(f)[1]<50:continue
 outer=breptools.OuterWire(f);holes=[]
 for w in TopologyExplorer(f).wires():
  if w.IsSame(outer):continue
  g=GProp_GProps();brepgprop.SurfaceProperties(BRepBuilderAPI_MakeFace(a.Plane(),w,True).Face(),g)
  if abs(g.Mass())>20:holes.append(abs(g.Mass()))
 if not holes:continue
 face=BRepBuilderAPI_MakeFace(a.Plane(),outer,True).Face();n=a.Plane().Axis().Direction();t=gp_Trsf();t.SetTranslation(gp_Vec(n).Multiplied(-.25));face=BRepBuilderAPI_Transform(face,t,True).Shape()
 caps.append(BRepPrimAPI_MakePrism(face,gp_Vec(n).Multiplied(.5)).Shape());jets+=holes
assert len(caps)==3 and len(jets)==2
points={'neck':(59,-48,1),'side_port':(34.5,45.5,5),'original_plenum':(30,44,10),'left_jet':(10,52.35,-16),'right_jet':(29.9,52.35,-16)}
report={'status':'running','method':'OCC coplanar-face refinement and1e-6mm diagnostic cap fuses; original export geometry unchanged','source_cap_input_sha256':sha(source_path),'jet_areas_mm2':jets,'files':{}}
try:
 for filename in ['tap-top-fan-duct-PROTOTYPE-native.brep','tap-top-fan-duct-PROTOTYPE.step']:
  p=R/filename;duct=read(p);b=bbox(duct);box=BRepPrimAPI_MakeBox(gp_Pnt(b[0]-2,b[1]-2,b[2]-2),b[3]-b[0]+4,b[4]-b[1]+4,b[5]-b[2]+4).Shape()
  sealed=duct
  for cap in caps:sealed=cap_fuse(sealed,cap)
  air=BRepAlgoAPI_Cut(box,sealed).Shape();solids=list(TopologyExplorer(air).solids())
  row={'sha256':sha(p),'valid':BRepCheck_Analyzer(air).IsValid(),'air_solid_volumes_mm3':[vol(s)for s in solids]};report['files'][filename]=row
  assert row['valid'] and len(solids)==2 and all(v>0 for v in row['air_solid_volumes_mm3']),row
  row['air_solids_common_volume_mm3']=vol(BRepAlgoAPI_Common(solids[0],solids[1]).Shape())
  assert abs(row['air_solids_common_volume_mm3'])<1e-6
  cavities=[s for s in solids if BRepClass3d_SolidClassifier(s,gp_Pnt(*points['neck']),1e-6).State()==TopAbs_IN]
  assert len(cavities)==1
  cavity=cavities[0];cb=bbox(cavity);row['cavity_bounds_mm']=cb
  row['enclosed']=all(cb[k]>b[k]-1 and cb[k+3]<b[k+3]+1 for k in range(3))
  row['connected_stages']={n:BRepClass3d_SolidClassifier(cavity,gp_Pnt(*pt),1e-6).State()==TopAbs_IN for n,pt in points.items()}
  assert row['enclosed'] and all(row['connected_stages'].values()),row
  row['pass']=True;print(json.dumps(row),flush=True)
 report['status']='passed'
except Exception as exc:
 report['status']='failed';report['error']=str(exc);OUT.write_text(json.dumps(report,indent=2));raise
OUT.write_text(json.dumps(report,indent=2))

