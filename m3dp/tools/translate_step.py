# Translate Chinese part/feature names in a STEP file to English (geometry untouched).
# Usage: python3 translate_step.py SRC.STEP DST.STEP NAMEMAP.csv DST_FILENAME
import re,csv,sys
M={
"打印头6.11":("Printhead 6.11","Top-level assembly"),
"17 44双联齿轮":("HGX gear 17T-44T double (compound) gear","Extruder reduction gear"),
"2510风扇":("2510 fan","Hotend heatsink fan, 25x25x10"),
"36圆饼步进电机":("NEMA14 36mm pancake stepper","Extruder motor"),
"36齿挤出齿轮":("36T extruder drive gear","3 in assembly"),
"4020离心风扇_По умолчанию":("4020 blower fan_Default","Part cooling; suffix was Russian 'Default'"),
"M3螺母":("M3 hex nut",""),
"M4六角隔离柱10":("M4 hex standoff 10mm",""),
"M4六角隔离柱14":("M4 hex standoff 14mm",""),
"M4带孔螺栓":("M4 hollow through-hole bolt","Filament/PTFE pass-through"),
"MGN12H":("MGN12H rail carriage","Printer X carriage (already on Voron)"),
"N52磁铁 6 4":("N52 magnet 6x4mm",""),
"P1P陶瓷加热片":("Bambu P1P ceramic heater",""),
"半圆头螺栓_M3*16":("Button head screw M3x16 ISO7380",""),
"半圆头螺栓_M3*22":("Button head screw M3x22 ISO7380",""),
"压簧":("Compression spring","Idler spring"),
"喷嘴+喉管_拓竹":("Nozzle + heatbreak (Bambu Lab style)",""),
"圆头销外径3长4":("Round head pin OD3 x L4","Kinematic coupling ball"),
"圆柱头螺栓_M2.5*14":("Socket head cap screw M2.5x14 DIN912",""),
"圆柱头螺栓_M3*10":("Socket head cap screw M3x10 DIN912",""),
"圆柱头螺栓_M3*15":("Socket head cap screw M3x15 DIN912",""),
"圆柱头螺栓_M3*22":("Socket head cap screw M3x22 DIN912",""),
"圆柱头螺栓_M3*8":("Socket head cap screw M3x8 DIN912",""),
"圆柱销外径1.5长5":("Dowel pin OD1.5 x L5","Kinematic coupling V-groove"),
"垫圈_3.2*6*0.5":("Washer 3.2x6x0.5",""),
"带轴承摆臂打印一体式":("Swing arm with bearing - printed one-piece version","Alternative to the CNC swing arm"),
"弹簧撑板":("Spring support plate",""),
"打印头背板cnc（三叉戟）":("Printhead back plate CNC (Trident)",""),
"拓竹P1P热端组件":("Bambu P1P hotend assembly",""),
"摆杆外带轴承（CNC）":("Swing lever outer with bearing (CNC)",""),
"摆杆外带轴承（CNC）_摆杆内":("Swing lever outer with bearing (CNC)_inner lever",""),
"散热翅片_拓竹":("Heatsink (Bambu Lab style)",""),
"新热端模块":("Hotend module (new)","Repeated once per tool"),
"沉头螺栓_M3*16":("Countersunk screw M3x16 DIN7991",""),
"涡流调平":("Eddy current leveling probe","BTT Eddy-style"),
"热端固定件":("Hotend holder",""),
"百瑞特防滑螺母_M4":("M4 anti-loosening lock nut",""),
"直径3长16圆柱销":("Dowel pin D3 x 16",""),
"直径3长24圆柱销":("Dowel pin D3 x 24",""),
"硅胶套":("Silicone sock",""),
"简化盖板_简化盖板右":("Simplified cover_right",""),
"简化盖板_简化盖板左":("Simplified cover_left",""),
"耗材丝":("Filament (reference body)",""),
"轴承_3x7x3":("Bearing 3x7x3 (683ZZ)",""),
"轴承外径6内径3厚2.5":("Bearing OD6 ID3 W2.5 (MR63ZZ)",""),
"顶部磁铁固定板":("Top magnet retaining plate",""),
"风道改":("Part cooling duct (modified)",""),
"热端停靠坞中置（CNC）":("Hotend dock center-mount (CNC)",""),
}
src,dst,csvp,fname=sys.argv[1:5]
t=open(src,encoding='latin1').read()
def dec(s): return re.sub(r'\\X2\\([0-9A-Fa-f]+)\\X0\\',lambda m:bytes.fromhex(m.group(1)).decode('utf-16-be'),s)
miss=set();used={}
def rep(m):
    s=m.group(1)
    if '\\X' not in s: return m.group(0)
    d=dec(s)
    if d in M: used[d]=M[d][0]; return "'"+M[d][0]+"'"
    e=d
    for a,b in [('基体零件','Base part'),('切除-拉伸','Cut-Extrude'),('凸台-拉伸','Boss-Extrude'),('倒角','Chamfer'),('旋转','Revolve'),('圆角','Fillet'),('输入','Imported'),('Odebrat vysunutím','Cut-Extrude'),('钢 - 缎光','Steel - satin'),('钢','Steel'),('实体','Body'),('摆臂','Swing arm'),('盖板','Cover plate'),('背板','Back plate')]: e=e.replace(a,b)
    if all(ord(c)<128 for c in e): used[d]=e; M.setdefault(d,(e,'SolidWorks body/feature name')); return "'"+e+"'"
    miss.add(d); return m.group(0)
t2=re.sub(r"'([^']*)'",rep,t)
t2=re.sub(r"FILE_NAME \('[^']*'",f"FILE_NAME ('{fname}'",t2,count=1)
open(dst,'w',encoding='latin1').write(t2)
print("translated",len(used),"missing",miss)
w=csv.writer(open(csvp,'w',newline='',encoding='utf-8-sig'))
w.writerow(["Chinese","English","Note"])
for k in sorted(used): w.writerow([k,M[k][0],M[k][1]])
