"""Check corrected detector native/STEP/mesh equivalence independently."""
from pathlib import Path
import sys,json,hashlib,zipfile,xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'rail'))
from cad_checks import read_step,volume,difference,mesh_checks
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepCheck import BRepCheck_Analyzer,BRepCheck_Shell,BRepCheck_NoError
from OCC.Extend.TopologyUtils import TopologyExplorer
R=Path(__file__).resolve().parent

def read(p):
 s=TopoDS_Shape();breptools.Read(s,str(p),BRep_Builder());return s

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=R/'tool-detector-mount';native=json.loads((R/'native-validation.json').read_text());reopen=json.loads((R/'native-reopen-validation.json').read_text())
assert reopen['native_bore_edit_roundtrip']
assert reopen['original_unchanged_sha256']==sha(base.with_suffix('.FCStd'))
s=read_step(base.with_suffix('.step'));n=read(R/'tool-detector-mount-native.brep');preflight=read(R/'detector-mount-seating-preflight.brep')
assert BRepCheck_Analyzer(s).IsValid() and len(list(TopologyExplorer(s).solids()))==1
assert all(BRepCheck_Shell(shell).Closed()==BRepCheck_NoError for shell in TopologyExplorer(s).shells())
delta=difference(s,n);assert delta<.0001
preflight_delta=difference(s,preflight);assert preflight_delta<.001
assert abs(volume(s)-native['volume_mm3'])<.0001 and abs(volume(s)-reopen['volume_mm3'])<.0001
assert abs(volume(s)-922.9211078839311)<.001
m=mesh_checks(base.with_suffix('.stl'));m['relative_volume_error']=abs(m['signed_volume_mm3']-volume(s))/volume(s);assert m['relative_volume_error']<.005
with zipfile.ZipFile(base.with_suffix('.FCStd')) as z:
 xml=ET.fromstring(z.read('Document.xml'));objs=xml.find('Objects').findall('Object');names=[o.get('name') for o in objs];types=[o.get('type') for o in objs]
 assert 'P5SeatingBoss' not in names and 'SupportedMount' not in names
 assert 'M3Bore' in names and 'DetectorMountFinal' in names and not any('Python' in t for t in types)
report={'status':'passed','valid_closed_single_solid':True,'volume_mm3':volume(s),'native_STEP_geometry_difference_mm3':delta,'preflight_geometry_difference_mm3':preflight_delta,'preflight_comparison_note':('Exact current seating preflight match.' if preflight_delta<.0001 else 'Original diagnostic boss removal extended0.00001mm into the seating face; difference is bounded below0.001mm3.'),'mesh':m,'native_distinct_disk_reopen_and_edit':True,'obsolete_boss_absent':True,'files':{p.name:sha(p)for p in [base.with_suffix('.FCStd'),base.with_suffix('.step'),base.with_suffix('.stl'),R/'tool-detector-mount-native.brep']},'physical_switch_actuation_verified':False}
(R/'independent-export-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
