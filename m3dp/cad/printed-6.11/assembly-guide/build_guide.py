"""Compose the B1 assembly guide from CAD renders; does not generate CAD geometry."""
from pathlib import Path
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / 'output/pdf/CxChanger-B1-illustrated-assembly-guide.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
W, H = 612, 792
INK, MUTED, LIGHT = '#183044', '#526577', '#eef3f6'
COL = dict(P1='#e6ad26', P3='#58ab70', P4='#9c80d2', P5='#509acd',
           P8='#eb8155', Holder='#38b6ae', Detector='#dc669b')
c = canvas.Canvas(str(OUT), pagesize=(W, H))
c.setTitle('M3DP Changer B1 - Illustrated assembly guide')
c.setAuthor('Minimal3DP - derived from CxChanger 6.11')
page_no = 0

def rect(x, y, w, h, fill=LIGHT, stroke=None, radius=8):
    c.setFillColor(HexColor(fill))
    c.setStrokeColor(HexColor(stroke or fill))
    c.roundRect(x, H-y-h, w, h, radius, fill=1, stroke=bool(stroke))

def text(s, x, y, w=528, size=11, color=INK, bold=False, leading=None):
    style = ParagraphStyle('p', fontName='Arial-Bold' if bold else 'Arial', fontSize=size,
                           leading=leading or size*1.36, textColor=HexColor(color))
    p = Paragraph(s, style)
    _, h = p.wrap(w, 1000)
    if y < 747 and y+h > 747:
        raise ValueError(f'Page {page_no}: content crosses footer: {s[:65]} at {y+h}')
    p.drawOn(c, x, H-y-h)
    return h

def image(fn, x, y, w):
    h = w * .75
    c.drawImage(str(HERE/'images'/fn), x, H-y-h, width=w, height=h, mask='auto')
    return lambda px, py: (x+px*w/800, y+py*w/800)

def arrow(x1, y1, x2, y2, color=INK, width=1.2):
    c.setStrokeColor(HexColor(color)); c.setFillColor(HexColor(color)); c.setLineWidth(width)
    c.line(x1, H-y1, x2, H-y2)
    angle = math.atan2(y2-y1, x2-x1)
    p = c.beginPath(); p.moveTo(x2, H-y2)
    for d in (-.48, .48):
        p.lineTo(x2-6*math.cos(angle+d), H-(y2-6*math.sin(angle+d)))
    p.close(); c.drawPath(p, fill=1, stroke=0)

def label(s, x, y, target, color=INK, w=142):
    ty = y+13
    sx = x+w if target[0] > x+w/2 else x
    arrow(sx, ty, *target, color=color)
    style = ParagraphStyle('l', fontName='Arial-Bold', fontSize=10, leading=12.4,
                           textColor=HexColor(INK))
    p = Paragraph(s, style); _, h = p.wrap(w-14, 100)
    rect(x, y-2, w, h+8, '#ffffff', radius=3)
    rect(x, y, 3, h+4, color, radius=0)
    p.drawOn(c, x+8, H-y-h-1)

def box(title, body, x, y, w=528, h=82, color=COL['Holder']):
    rect(x,y,w,h)
    rect(x,y,4,h,color,radius=0)
    text(title,x+15,y+11,w-30,11,bold=True)
    text(body,x+15,y+31,w-30,10.5)

def step(n, title, body, y, x=42, w=528):
    rect(x,y,24,24,INK,radius=12)
    c.setFont('Arial-Bold',11); c.setFillColor(white)
    c.drawCentredString(x+12,H-y-16,str(n))
    text(title,x+36,y,w-36,12,bold=True)
    return text(body,x+36,y+21,w-36,11)+29

def start(title, subtitle):
    global page_no
    if page_no: c.showPage()
    page_no += 1
    c.setFillColor(HexColor(INK)); c.rect(0,H-8,W,8,fill=1,stroke=0)
    text('M3DP CHANGER  /  B1 BENCH ASSEMBLY',42,27,528,9,MUTED,bold=True)
    text(title,42,49,528,25,bold=True,leading=28)
    text(subtitle,42,87,528,10.5,MUTED)
    c.setStrokeColor(HexColor('#d9e2e8')); c.setLineWidth(.6); c.line(42,43,570,43)
    text('Corrected 6.11 + integral pillars  |  4.6 mm insert bores  |  01 Nov 2026',42,754,480,8,MUTED)
    c.setFont('Arial-Bold',9); c.setFillColor(HexColor(INK)); c.drawRightString(570,29,f'{page_no:02d}')

start('See the finished arrangement', 'Eight printed pieces: one mechanism, one detector mount and two removable hotend holders.')
m=image('01-head-overview.png',60,128,492)
label('P1  Magnet plate',42,161,m(318,134),COL['P1'])
label('P3  Left cover',42,238,m(310,201),COL['P3'])
label('Holder  Removable tool',42,347,m(364,304),COL['Holder'])
label('Motor  Carriage side',426,137,m(410,78))
label('Detector mount',426,193,m(495,86),COL['Detector'])
label('P5  Backplate',426,258,m(478,222),COL['P5'])
label('P4  Right cover',426,315,m(421,188),COL['P4'])
label('P8  Moving arm',426,378,m(448,257),COL['P8'])
arrow(306,474,306,502)
text('NOZZLE DOWN',258,507,110,9,MUTED,bold=True)
box('Start here', 'Lay out the seven part types on page 2. Build the head first, then make the two hotend modules. Only one module attaches to the head at a time.',42,543,h=85)
text('Reading the pictures',42,649,528,12,bold=True)
text('Colors identify parts; your prints can all be black. The motor is behind the mechanism on the carriage side. The long teal holder is on the coupling side. Views are assembly orientations, not print orientations.',42,672,528,11)

start('Match each print to its name', 'Keep these four adapted plates together: P1, P3, P4 and P5.')
cards=[('P1','Magnet plate','part-p1.png','Two integral pillars; one piece.','1'),
       ('P3','Left cover','part-p3.png','Smaller cover; reinforced bolt seat.','1'),
       ('P4','Right cover','part-p4.png','Matching right cover; bolt seat.','1'),
       ('P5','Backplate','part-p5.png','Two insert seats near the lower end.','1'),
       ('P8','Printed arm','part-p8.png','One-piece moving arm with roller fork.','1'),
       ('Holder','Hotend holder','part-holder.png','Make one module for T0 and one for T1.','2'),
       ('Detector','Detector mount','part-detector.png','Small bracket with pivot hole and arc slot.','1')]
for i,(key,name,fn,note,qty) in enumerate(cards):
    x=42+(i%3)*180; y=130+(i//3)*194
    rect(x,y,168,182,'#ffffff','#d9e2e8')
    image(fn,x+12,y+25,144)
    text(f'{key}  /  {qty}x',x+10,y+8,148,10,bold=True)
    rect(x+10,y+136,4,32,COL[key],radius=0)
    text(name,x+20,y+135,138,10,bold=True)
    text(note,x+20,y+151,138,9,leading=11)
box('Use the printed arm', 'P8 replaces the CNC-arm alternative. Do not add P2, P6 or P7, or duplicate their roller hardware.',222,518,w=348,h=82,color=COL['P8'])
box('These are assembly parts', 'Keep these B1 prints. The earlier fan, saddle and insert coupons were fit tests. This guide starts from the finished B1 parts.',222,612,w=348,h=84)
text('Exact STL filenames are listed in the companion assembly-guide/README.md.',42,719,528,9,MUTED)

start('Understand the layers', 'Exploded view: parts are spread apart to reveal the relationships; offsets are not assembly distances.')
m=image('02-head-exploded.png',42,130,528)
label('P3  Left cover',42,365,m(165,310),COL['P3'],100)
label('P4  Right cover',42,424,m(275,350),COL['P4'],132)
label('P1  Pillars face the covers',42,174,m(285,224),COL['P1'],143)
label('Motor behind P5',427,149,m(485,190),w=143)
label('P5  Carriage-side plate',427,242,m(400,280),COL['P5'],143)
label('P8  Arm beside gears',427,401,m(430,330),COL['P8'],143)
text('Order of work',42,542,528,13,bold=True)
step(1,'Prepare P5 and P1','Identify the holes on page 4. Insert the two long countersunk bolts before motor/gears obstruct the heads.',570)
step(2,'Fit the mechanism and covers','Use the pin and bearing seats to align the drive and P8. Close the covers squarely; then add each outside washer and nut.',636)
text('The detector and removable holder are shown separately on pages 7-9.',78,710,492,10,MUTED)

start('Identify the backplate holes', 'Look at the broad carriage-side face of P5. This view is from behind the assembled head.')
m=image('part-p5.png',42,128,528)
label('Rear bolt head here\nM3 x 30 countersunk'.replace('\n','<br/>'),42,145,m(342,162),COL['P5'],144)
label('Legacy insert seat<br/>4.6 mm bore',42,410,m(281,415),COL['P5'],140)
label('Legacy insert seat<br/>4.6 mm bore',430,433,m(506,467),COL['P5'],140)
step(1,'Leave these two seats unused for B1','These 4.6 mm bores were prepared for M3 inserts at the original blower interface. The current top blower is relocated. These holes do not fasten the B1 plates or the TAP adapter.',553)
step(2,'Pre-fit the rear through-bolt','The upper countersink takes the M3 x 30 bolt. It passes through the rear stack to P4. The rear hole is a clearance joint, not an insert seat.',632)
text('P1 pillar bores also take through-bolts. Do not install heat-set inserts in P1.',78,710,492,10,COL['P5'],bold=True)

start('Fit the drive and moving arm', 'Covers and hotend holder removed for visibility. Keep the spring mechanism in its original arrangement.')
m=image('03-gears-open.png',42,121,528)
label('HGX 17/44T<br/>compound gear',42,177,m(328,216),w=144)
label('Fixed 36T gear<br/>3 x 16 mm pin',42,286,m(329,303),w=144)
label('P8 pivot<br/>3 x 24 mm pin',426,157,m(480,226),COL['P8'],144)
label('Arm 36T gear<br/>Behind P8',426,281,m(436,299),COL['P8'],144)
label('683ZZ roller<br/>At the bottom of P8',426,414,m(480,410),COL['P8'],144)
text('P8 roller hardware order',42,536,528,12,bold=True)
text('<b>M3 x 8 head → 683ZZ bearing → 3.2 x 6 x 0.5 washer → P8 → M3 nut</b>',42,560,528,11)
text('MR63ZZ bearings (3 x 6 x 2.5 mm): two support the compound-gear axis in P5 and P3; the third sits in P4 at the P8 pivot. The other P3 opening receives the fixed-gear pin. These are not extra screw holes. Fit them before the covers; recheck free roller rotation, full gear turns and arm stroke.',42,592,528,10.5)
box('One shaft placement still needs a bench check', 'The saved source leaves the second 3 x 16 mm pin at the unused CNC arm. It is not shown installed at the P8 gear. Confirm the P8 gear shaft seating and retention before treating the head as assembled; do not copy the floating CNC pin position.',42,655,h=81,color=COL['P8'])

start('Close the two pillar joints', 'Schematic stacks below show hardware order; the CAD view identifies the two pillars on P1.')
m=image('part-p1.png',162,117,288)
label('10 mm pillar<br/>P3 / left joint',42,218,m(257,305),COL['P1'],142)
label('14 mm pillar<br/>P4 / rear joint',428,235,m(535,337),COL['P1'],142)
text('<b>Motor mounting:</b> left ear uses M3 x 15 socket head from P1 toward the motor. The right ear uses the M3 x 22 detector anchor shown on page 9.',42,300,528,10.5)

def stack(y, title, pieces, note):
    text(title,42,y,528,12,bold=True)
    x=42; top=y+29
    for i,(name,w,color) in enumerate(pieces):
        rect(x,top,w,50,color,radius=3)
        text(name,x+6,top+10,w-12,9,bold=True,leading=11)
        if i<len(pieces)-1: arrow(x+w+2,top+25,x+w+12,top+25)
        x+=w+14
    text(note,42,top+60,528,10,MUTED)

stack(350,'A  Left joint - M3 x 20 countersunk',[
    ('Head on P1',81,'#dce4eb'),('P1\n10 mm pillar'.replace('\n','<br/>'),119,'#f7e5b4'),('P3 cover',92,'#dceee1'),('Washer',69,'#dce4eb'),('M3 nut',69,'#dce4eb')],
    'Seat the head in P1. The washer and nut sit outside the green cover.')
stack(480,'B  Rear joint - M3 x 30 countersunk',[
    ('Head on P5',81,'#dce4eb'),('P1\n14 mm pillar'.replace('\n','<br/>'),119,'#f7e5b4'),('P4 cover',92,'#e8e0f3'),('Washer',69,'#dce4eb'),('M3 nut',69,'#dce4eb')],
    'The bolt starts at P5, continues through the P1 pillar, then exits the purple cover.')
box('Use the checked hardware sizes', '90-degree countersunk heads: actual diameter no larger than 5.6 mm. Washers: 3.2 mm ID, 7 mm maximum OD, 0.5 mm thick. Nuts: 5.5 mm across flats, 2.4 mm thick. Both heads must remain recessed.',42,619,h=92,color=COL['P1'])
text('Snug the joints only after everything seats squarely. Recheck free gear and arm movement.',42,721,528,10,bold=True)

start('Build two hotend modules', 'One teal holder per tool. Label the finished modules T0 and T1.')
m=image('09-module-front.png',42,128,528)
label('M3 x 10 cap heads<br/>Docking hooks - 2x',42,296,m(325,303),COL['Holder'],144)
arrow(186,317,*m(396,310),color=COL['Holder'])
label('M3 x 22 transverse<br/>Hotend clamps - 2x',426,338,m(452,339),COL['Holder'],144)
label('Bambu P1P hotend<br/>Nozzle points down',426,440,m(401,476),w=144)
step(1,'Seat the hotend in the holder','Fit the hotend into the lower pocket and align the transverse clamp holes. Use two M3 x 22 socket-head screws and the matching nut pockets.',552)
step(2,'Fit the separate docking hooks','Use two magnetic-head M3 x 10 socket-head screws at the hook locations, 15 mm apart. These are not the long transverse clamp screws. Each module uses four M3 nuts in total.',628)
text('Check actual hook heads attract the dock magnet. Ordinary stainless heads may not.',78,713,492,10,MUTED)

start('Connect the magnetic coupling', 'Holder mating face shown at left; the right view shows the module separated from the head.')
a=image('08-module.png',42,129,246)
b=image('05-coupling-separated.png',300,129,270)
label('Magnet - 3x',42,157,a(390,54),COL['Holder'],92)
label('Locating pins<br/>3x',42,269,a(345,345),COL['Holder'],90)
arrow(420,320,446,304,color=COL['Holder'])
text('Mate the teal holder to the coupling face of the head.',313,345,244,10,MUTED)
step(1,'Fit the coupling hardware','Each holder takes three N52 6 x 4 mm magnets and three round-head 3 x 4 mm locating pins. The head takes three opposing magnets and six 1.5 x 5 mm cylindrical pins, arranged as three locating grooves.',399)
step(2,'Check polarity before fixing magnets','Bring the module toward the head as shown. Every opposing magnet pair must attract. Check the polarity of each pair before securing the magnets in their pockets.',485)
step(3,'Check what actually touches','The three round-head pins seat against the three cylindrical-pin grooves. The opposing magnets must retain a small gap; magnet-to-magnet contact must not prevent the locating pins from seating.',570)
box('Fit one module at a time', 'Seat and remove T0, then repeat with T1. Check for rocking, snagging or contact with the P4 washer/nut. A good fit on one module does not confirm the other.',42,663,h=72)

start('Install the detector bracket', 'Rear view: the pink bracket sits directly on the motor mounting ear. No spacer belongs underneath.')
a=image('06-detector-seat.png',42,127,246)
b=image('07-detector-lifted.png',306,127,264)
text('SEATED POSITION',65,319,210,9,MUTED,bold=True)
text('LIFTED TO SHOW CONTACT',316,331,250,9,MUTED,bold=True)
label('Pivot hole',42,136,a(333,151),COL['Detector'],96)
label('Arc slot',42,240,a(310,190),COL['Detector'],80)
label('Anchor hole',442,287,b(380,285),COL['Detector'],128)
step(1,'Use the longer anchor screw','Replace the source M3 x 16 button-head anchor with M3 x 22. Keep the existing M3 nut below P5; add a second M3 nut above the detector. The mount sits directly against the motor ear.',374)
step(2,'Attach the D2F-01F switch','Use two M2 x 18 socket-head screws, two M2 nuts and four M2 washers (5 mm OD, 0.4 mm thick). Use one washer on each side of each joint. One hole is the pivot; the arc slot allows angular adjustment.',468)
step(3,'Aim the plunger toward the P8 actuator','The switch is omitted from these CAD views. Adjust its angle by moving P8 by hand, then secure it without bottoming the plunger. The mount geometry alone does not establish correct actuation.',562)
box('Required switch response', 'Empty head: not detected. Tool without filament: not detected. Tool with filament: detected. Repeat all three conditions before relying on automatic tool changes.',42,660,h=76,color=COL['Detector'])

start('Check the assembled mechanism', 'This is the next bench step after printing. Keep the parts for the final build once these checks pass.')
checks=[
 ('All plates seat squarely','P1, P3, P4 and P5 meet their supports without bending or rocking. There are no added metal standoffs at the integral pillars.'),
 ('Both through-bolts seat and clear','Heads remain recessed. Washers sit flat; nuts engage. The P4 washer/nut clears the hotend holder throughout attachment and removal.'),
 ('Drive and P8 move freely','Gears turn through complete revolutions. P8 moves through its full release/clamp stroke. The 683ZZ roller turns freely; pins remain seated.'),
 ('Both modules locate repeatably','T0 and T1 each seat on all three locating grooves. Magnet polarity is correct, magnets retain a gap, and the module does not rock.'),
 ('Detector repeats its truth table','Verify the three physical conditions on page 9. Adjust by hand before trusting the signal.'),
 ('Record the remaining shaft check','Confirm the P8 gear shaft installation and retention. Its second 3 x 16 mm pin was not saved in the printed-arm position in the source assembly.')]
y=136
for title,body in checks:
    c.setStrokeColor(HexColor(MUTED)); c.setLineWidth(1); c.rect(43,H-y-12,12,12,fill=0,stroke=1)
    text(title,68,y-2,502,12,bold=True)
    h=text(body,68,y+20,502,10.5)
    y+=h+44
box('After this bench fit', 'Continue with the TAP/top-blower and dock integration instructions. Those parts, wiring, heating and automatic motion are outside this B1 guide. Report which checks pass and any part or hole that does not line up.',42,615,h=87)
text('Source and validation',42,715,135,9,bold=True)
text('CAD-derived orientation, not a completed physical assembly test.\nSee source-audit.md for geometry selection and the known shaft omission.',185,715,385,8.5,leading=11)
c.save()
print(OUT)
