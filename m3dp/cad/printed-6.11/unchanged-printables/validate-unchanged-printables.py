"""Independent geometry, mesh, and native-tree checks after GUI export."""
from pathlib import Path
import json,math,zipfile,xml.etree.ElementTree as ET
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf,gp_Ax1,gp_Pnt,gp_Dir,gp_Vec
from OCC.Extend.TopologyUtils import TopologyExplorer
import cad_checks as v

HERE=Path(__file__).resolve().parent
selection=json.loads((HERE/'source-selection.json').read_text())
native=json.loads((HERE/'unchanged-printables-native-validation.json').read_text())
reopen=json.loads((HERE/'unchanged-printables-native-reopen.json').read_text())
with zipfile.ZipFile(HERE/'unchanged-printables-6.11.FCStd') as z:
    document=ET.fromstring(z.read('Document.xml'))
    placements={o.get('name'):o.find("Properties/Property[@name='Placement']/PropertyPlacement").attrib
                for o in document.find('ObjectData').findall('Object')}
reports=[]
for row in selection['parts']:
    name=row['basename'];source=v.read_step(HERE/'source'/(name+'.step'))
    target=v.read_step(HERE/(name+'-print-position.step'))
    if name=='hotend-holder':
        t=gp_Trsf();t.SetRotation(gp_Ax1(gp_Pnt(0,0,0),gp_Dir(1,0,0)),-math.pi/2)
        source=BRepBuilderAPI_Transform(source,t,True).Shape()
    # Use the actual native placement, not FreeCAD's tessellation-dependent
    # displayed bounds, to reconstruct the export without a registration fit.
    p=placements['Print_'+name.replace('-','_')]
    t=gp_Trsf();t.SetTranslation(gp_Vec(float(p['Px']),float(p['Py']),float(p['Pz'])))
    expected=BRepBuilderAPI_Transform(source,t,True).Shape()
    assert BRepCheck_Analyzer(target).IsValid() and len(list(TopologyExplorer(target).solids()))==1
    delta=v.difference(expected,target)
    assert delta<0.001, (name,delta)
    assert abs(v.bbox(target)[2])<0.00001
    native_row=next(r for r in native if r['basename']==name)
    reopened_row=next(r for r in reopen if r['label']==name)
    assert abs(native_row['volume_mm3']-v.volume(target))<0.001
    assert abs(reopened_row['volume_mm3']-v.volume(target))<0.001
    mesh=v.mesh_checks(HERE/(name+'.stl'))
    mesh['relative_volume_error']=abs(mesh['signed_volume_mm3']-v.volume(target))/v.volume(target)
    assert mesh['relative_volume_error']<0.005,(name,mesh)
    reports.append({'basename':name,'quantity_for_six_tools':row['quantity_for_six_tools'],
        'source_to_print_position_difference_mm3':delta,'native_reopened':True,
        'step_valid':True,'step_solids':1,'volume_mm3':v.volume(target),
        'print_bounds_mm':v.bbox(target),'mesh':mesh,'orientation':native_row['orientation']})
with zipfile.ZipFile(HERE/'unchanged-printables-6.11.FCStd') as z:
    doc=ET.fromstring(z.read('Document.xml'))
    objects=doc.find('Objects').findall('Object')
    assert len(objects)==4 and all(o.get('type')=='Part::Feature' for o in objects)
(HERE/'unchanged-printables-independent-validation.json').write_text(json.dumps(reports,indent=2))
print(json.dumps(reports,indent=2))
