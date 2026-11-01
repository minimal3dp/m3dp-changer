"""Independent exported-solid, mesh and native-edit validation."""
from pathlib import Path
import importlib.util,json,zipfile,xml.etree.ElementTree as ET
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.gp import gp_Pnt,gp_Vec,gp_Trsf
from OCC.Extend.TopologyUtils import TopologyExplorer
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',HERE/'cad_checks.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
native=json.loads((HERE/'front-rail-supports-native-validation.json').read_text())
reopened=json.loads((HERE/'front-rail-supports-native-reopen.json').read_text())
rows=[]
for name in ['front-rail-support-left','front-rail-support-right','front-gantry-fit-coupon']:
    source='front-rail-support-right' if name=='front-gantry-fit-coupon' else name
    expected=TopoDS_Shape();breptools.Read(expected,str(HERE/(source+'-preflight.brep')),BRep_Builder())
    if name=='front-gantry-fit-coupon':
        expected=BRepAlgoAPI_Common(expected,BRepPrimAPI_MakeBox(gp_Pnt(222,-467,20.504002),32,32,26).Shape()).Shape()
    record=next(r for r in native if r['name']==name)
    t=gp_Trsf();t.SetTranslation(gp_Vec(*record['print_translation_mm']));expected=BRepBuilderAPI_Transform(expected,t,True).Shape()
    exported=v.read_step(HERE/(name+'.step'))
    assert BRepCheck_Analyzer(exported).IsValid() and len(list(TopologyExplorer(exported).solids()))==1
    difference=v.difference(exported,expected);assert difference<.0001,(name,difference)
    mesh=v.mesh_checks(HERE/(name+'.stl'))
    mesh['relative_volume_error']=abs(mesh['signed_volume_mm3']-v.volume(exported))/v.volume(exported)
    assert mesh['relative_volume_error']<.005
    with zipfile.ZipFile(HERE/(name+'.FCStd')) as z:
        xml=ET.fromstring(z.read('Document.xml'));types=[o.get('type') for o in xml.find('Objects').findall('Object')]
        assert types.count('Part::Box')>=7 and types.count('Part::Cylinder')==4 and 'Part::Compound' in types
        assert types.count('Part::Extrusion')==2 and types.count('Sketcher::SketchObject')==2
        assert not any('Python' in a for a in types)
    check=next(r for r in reopened if r['name']==name)
    assert check['native_bore_edit_roundtrip'] and abs(check['volume_mm3']-v.volume(exported))<.0001
    rows.append({'name':name,'valid':True,'solids':1,'volume_mm3':v.volume(exported),
                 'export_geometry_difference_mm3':difference,'mesh':mesh,'native_edit_roundtrip':True})
(HERE/'front-rail-supports-independent-validation.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
