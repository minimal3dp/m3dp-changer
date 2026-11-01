"""Parametric 2510 cage coupon, recreated from the raised-carrier dimensions.

All dimensions are millimetres. Run with build123d-mcp execute_file().
The reference STEP is used only by the separate verification, never this model.
"""
from build123d import *

# Dimensions in mm; preserve the existing dock coordinate system.
insert_diameter = 4.6
fan_outer = 29.0
wall_thickness = 1.85
fan_depth = 10.0
lip_thickness = 1.0
air_diameter = 24.0
fan_x, fan_y, base_z = 48.0, -16.0, -11.5
boss_width, boss_length = 8.0, 10.0
boss_offset_x, boss_stagger_y = 17.0, 8.0
key_width, key_length, key_height = 6.0, 8.0, 0.8
insert_seat_depth = 5.8
tip_diameter, tip_depth = 3.4, 8.3
cable_width, cable_reach, cable_overrun = 4.0, 4.0, 1.0
cut_epsilon = 0.1

fan_min_x = fan_x - fan_outer / 2
fan_min_y = fan_y - fan_outer / 2
floor_z = base_z + lip_thickness
rim_z = floor_z + fan_depth
key_top_z = rim_z + key_height
boss_centers = [(fan_x - boss_offset_x, fan_y - boss_stagger_y), (fan_x + boss_offset_x, fan_y)]
corner = (Align.MIN, Align.MIN, Align.MIN)
axial = (Align.CENTER, Align.CENTER, Align.MIN)

cage = Pos(fan_min_x, fan_min_y, base_z) * Box(fan_outer, fan_outer, lip_thickness + fan_depth, align=corner)

# Hollow the cage, leaving the 1 mm front lip and 1.85 mm walls.
cage = cage - Pos(fan_min_x + wall_thickness, fan_min_y + wall_thickness, floor_z) * Box(fan_outer - 2 * wall_thickness, fan_outer - 2 * wall_thickness, fan_depth + cut_epsilon, align=corner)

# Airflow opening through the front lip.
cage = cage - Pos(fan_x, fan_y, base_z - cut_epsilon) * Cylinder(air_diameter / 2, lip_thickness + 2 * cut_epsilon, align=axial)

# Left retainer boss.
x, y = boss_centers[0]
cage = cage + Pos(x - boss_width / 2, y - boss_length / 2, base_z) * Box(boss_width, boss_length, lip_thickness + fan_depth, align=corner)

# Raised key for the left retainer.
cage = cage + Pos(x - key_width / 2, y - key_length / 2, rim_z) * Box(key_width, key_length, key_height, align=corner)

# Middle retainer boss.
x, y = boss_centers[1]
cage = cage + Pos(x - boss_width / 2, y - boss_length / 2, base_z) * Box(boss_width, boss_length, lip_thickness + fan_depth, align=corner)

# Raised key for the middle retainer.
cage = cage + Pos(x - key_width / 2, y - key_length / 2, rim_z) * Box(key_width, key_length, key_height, align=corner)

# Lower-right cable relief, open to the side and rear of the cage.
cage = cage - Pos(fan_min_x + fan_outer - cable_width, fan_min_y - cable_overrun, floor_z) * Box(cable_width + cable_overrun, cable_reach + cable_overrun, fan_depth + cut_epsilon, align=corner)

# Left 4.6 mm heat-set insert seat.
x, y = boss_centers[0]
cage = cage - Pos(x, y, key_top_z - insert_seat_depth) * Cylinder(insert_diameter / 2, insert_seat_depth + 2 * cut_epsilon, align=axial)

# Left coaxial 3.4 mm screw-tip relief; retain the bottom floor.
cage = cage - Pos(x, y, key_top_z - tip_depth) * Cylinder(tip_diameter / 2, tip_depth + 2 * cut_epsilon, align=axial)

# Middle 4.6 mm heat-set insert seat.
x, y = boss_centers[1]
cage = cage - Pos(x, y, key_top_z - insert_seat_depth) * Cylinder(insert_diameter / 2, insert_seat_depth + 2 * cut_epsilon, align=axial)

# Middle coaxial 3.4 mm screw-tip relief.
cage = cage - Pos(x, y, key_top_z - tip_depth) * Cylinder(tip_diameter / 2, tip_depth + 2 * cut_epsilon, align=axial)

result = cage
# Preserve the assembly datum in STEP; translate the STL onto the print bed.
print_offset = -result.bounding_box().min
print_coupon = Pos(print_offset.X, print_offset.Y, print_offset.Z) * result
show(result, 'cage_rebuilt')
show(print_coupon, 'cage_print')

