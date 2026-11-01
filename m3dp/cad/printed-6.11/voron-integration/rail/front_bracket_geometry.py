"""Fixed prototype dimensions in the verified rear-crossbrace datum (mm).

Two forked supports retain the stock idlers and Z-belt clamps. Each uses the
existing two M5 axes and adds24mm under the original button-head bearing plane.
The400mm crossrail is a new part. This does not establish machine coordinates.
"""
RAIL_Y=-482.530002
RAIL_Z=48.91343
RAIL_LENGTH=400.0
ARM_INNER=226.0
ARM_OUTER=231.5
BELT_FRONT=-456.60633
BELT_REAR=-447.60633

def geometry(side):
    # CAD reference's small left/right placement differences are intentional.
    mount_x=244.977387 if side=='right' else 244.977205
    front_y=-459.779018
    rear_y=front_y+15.5
    mount_z=20.504002 if side=='right' else 20.400017
    front=RAIL_Y-6
    boxes=[
        ('ExistingClampBoltRiser',(mount_x-6,front_y-5.5,mount_z),(12,rear_y-front_y+11,24)),
        ('ForwardBeltFork',(ARM_INNER,front_y-5.5,mount_z+6),(mount_x+6-ARM_INNER,BELT_FRONT-2-(front_y-5.5),18)),
        ('RearBeltFork',(ARM_INNER,BELT_REAR+2,mount_z+6),(mount_x+6-ARM_INNER,rear_y+5.5-(BELT_REAR+2),18)),
        ('LongForwardArm',(ARM_INNER,front,mount_z+6),(ARM_OUTER-ARM_INNER,rear_y+5.5-front,18)),
        ('RaisedRailColumn',(ARM_INNER,front,mount_z+6),(ARM_OUTER-ARM_INNER,12,RAIL_Z+16-(mount_z+6))),
        ('RailTopClamp',(176,front,RAIL_Z+10),(ARM_OUTER-176,18.2,6)),
        ('RailRearRegister',(176,RAIL_Y+10.2,RAIL_Z+6),(24,2,10)),
    ]
    holes=[('ExistingM5Front',(mount_x,front_y,mount_z-.1),2.75,24.2,(0,0,1)),
           ('ExistingM5Rear',(mount_x,rear_y,mount_z-.1),2.75,24.2,(0,0,1)),
           ('RailM5Inner',(182,RAIL_Y,RAIL_Z+9.9),2.75,6.2,(0,0,1)),
           ('RailM5Outer',(194,RAIL_Y,RAIL_Z+9.9),2.75,6.2,(0,0,1))]
    gussets=[
        {'name':'TopClampGusset','plane':'xz','vertices':[
            (201,front,RAIL_Z+10),(ARM_INNER,front,RAIL_Z-10),(ARM_OUTER,front,RAIL_Z+10)],'direction':(0,12,0)},
        {'name':'ColumnBackGusset','plane':'yz','vertices':[
            (ARM_INNER,front+12,RAIL_Z+10),(ARM_INNER,rear_y+5.5,mount_z+6),(ARM_INNER,front+12,mount_z+6)],
         'direction':(ARM_OUTER-ARM_INNER,0,0)},
    ]
    if side=='left':
        boxes=[(n,(-p[0]-s[0],p[1],p[2]),s) for n,p,s in boxes]
        holes=[(n,(-p[0],p[1],p[2]),r,h,d) for n,p,r,h,d in holes]
        gussets=[dict(t,vertices=[(-p[0],p[1],p[2]) for p in t['vertices']],
                      direction=(-t['direction'][0],t['direction'][1],t['direction'][2])) for t in gussets]
    return {'side':side,'boxes':boxes,'holes':holes,'gussets':gussets,
            'mounting_axes':[[-mount_x if side=='left' else mount_x,y,mount_z] for y in [front_y,rear_y]],
            'mounting_stack_added_mm':24.0,'replacement_screws':'2 x M5x40 BHCS per side; replaces stock M5x16 BHCS'}
