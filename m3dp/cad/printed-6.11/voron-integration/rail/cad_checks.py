"""Independent OCC + STL topology checks; does not need the FreeCAD GUI.
Run using FreeCAD's bundled Python, after build-six-tool-dock.FCMacro.
"""
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
import json
import math
import struct
import xml.etree.ElementTree as ET
import zipfile
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Extend.TopologyUtils import TopologyExplorer

ROOT = Path(__file__).resolve().parent
TOL_MM3 = 0.0001

def read_step(path):
    r = STEPControl_Reader()
    if r.ReadFile(str(path)) != 1:
        raise AssertionError("Cannot read STEP: " + str(path))
    r.TransferRoots()
    return r.OneShape()

def volume(s):
    g = GProp_GProps()
    brepgprop.VolumeProperties(s, g)
    return g.Mass()

def bbox(s):
    b = Bnd_Box()
    brepbndlib.AddOptimal(s, b)
    return list(b.Get())

def clip(s, a, b):
    box = BRepPrimAPI_MakeBox(gp_Pnt(a, -60, -1), b-a, 100, 30).Shape()
    return BRepAlgoAPI_Common(s, box).Shape()

def move(s, x):
    t = gp_Trsf()
    t.SetTranslation(gp_Vec(x, 0, 0))
    return BRepBuilderAPI_Transform(s, t, True).Shape()

def difference(a, b):
    return volume(BRepAlgoAPI_Cut(a, b).Shape()) + volume(BRepAlgoAPI_Cut(b, a).Shape())

def stl_triangles(path):
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0] if len(data) >= 84 else 0
    if len(data) == 84 + 50 * count:
        return [struct.unpack_from('<12f', data, 84+50*i)[3:] for i in range(count)]
    vertices = []
    for line in data.decode('ascii').splitlines():
        terms = line.strip().split()
        if terms and terms[0] == 'vertex':
            vertices.append(tuple(float(x) for x in terms[1:]))
    assert len(vertices) % 3 == 0
    return [sum(vertices[i:i+3], ()) for i in range(0, len(vertices), 3)]

def mesh_checks(path):
    triangles = stl_triangles(path)
    vertices = {}
    edges = defaultdict(list)
    adjacency = defaultdict(set)
    signed_volume = 0.0
    for index, flat in enumerate(triangles):
        pts = [tuple(flat[i:i+3]) for i in (0,3,6)]
        ids = []
        for p in pts:
            # 0.00001 mm welding tolerance is far below export chord tolerance.
            key = tuple(round(v, 5) for v in p)
            ids.append(vertices.setdefault(key, len(vertices)))
        assert len(set(ids)) == 3, 'Degenerate triangle after precision welding'
        a,b,c = pts
        signed_volume += (a[0]*(b[1]*c[2]-b[2]*c[1]) + a[1]*(b[2]*c[0]-b[0]*c[2]) + a[2]*(b[0]*c[1]-b[1]*c[0])) / 6
        for start,end in zip(ids,ids[1:]+ids[:1]):
            edges[tuple(sorted((start,end)))].append((index, 1 if start<end else -1))
    assert all(len(v)==2 for v in edges.values()), 'STL has boundary/nonmanifold edges'
    assert all(sum(direction for _,direction in v)==0 for v in edges.values()), 'STL winding is inconsistent'
    for pair in edges.values():
        a,b = pair[0][0],pair[1][0]
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen=set()
    components=0
    for i in range(len(triangles)):
        if i in seen:continue
        components+=1
        todo=[i];seen.add(i)
        while todo:
            for n in adjacency[todo.pop()]:
                if n not in seen:seen.add(n);todo.append(n)
    assert components==1, 'STL has disconnected components'
    assert signed_volume>0, 'STL is inside-out'
    pts=list(vertices)
    return dict(triangles=len(triangles),vertices=len(vertices),edges=len(edges),
                connected_components=components,watertight=True,consistent_winding=True,
                signed_volume_mm3=signed_volume,
                bounds_mm=[min(p[i] for p in pts) for i in range(3)]+[max(p[i] for p in pts) for i in range(3)])

