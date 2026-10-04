"""
Splendor Board Game Storage Box & Organizer Generator
Modeled using SolidPython2 with fully parametric variables.

Designed for:
- 90 Cards: 40x Tier 1, 30x Tier 2, 20x Tier 3
- 10 Noble Tiles
- 40 Gem Tokens: 5 stacks of 7 gems (23.5mm), 1 stack of 5 gold (16.7mm)

Features:
- Individual removable deck trays for Tier 1, Tier 2, Tier 3 cards with finger cutouts & bottom push slots.
- Removable token tray with individual full-depth finger channels for pulling out each stack separately.
- Removable Noble tile tray with extra utility compartment.
- Master storage box and secure lid to organize all modules together.
"""

from solid2 import (
    cube,
    cylinder,
    circle,
    sphere,
    translate,
    rotate,
    scale,
    linear_extrude,
    hull,
    text,
    union,
    difference,
    intersection,
    polygon,
    square,
    scad_render_to_file,
    set_global_fn,
)

# Set global smooth arc resolution for OpenSCAD
set_global_fn(64)

# ==============================================================================
# PARAMETERS & PARAMETRIC VARIABLES
# ==============================================================================

# Shared Item Dimensions (Imported from dimensions.py)
try:
    from dimensions import (
        CARD_CORNER_RADIUS,
        CARD_LENGTH,
        CARD_THICKNESS,
        CARD_WIDTH,
        GEM_STACK_H,
        GOLD_STACK_H,
        NOBLE_LENGTH,
        NOBLE_STACK_H,
        NOBLE_TILE_COUNT,
        NOBLE_WIDTH,
        TIER1_CARD_COUNT,
        TIER1_STACK_H,
        TIER2_CARD_COUNT,
        TIER2_STACK_H,
        TIER3_CARD_COUNT,
        TIER3_STACK_H,
        TOKEN_DIAMETER,
        TOKEN_THICKNESS,
    )
except ImportError:
    from .dimensions import (
        CARD_CORNER_RADIUS,
        CARD_LENGTH,
        CARD_THICKNESS,
        CARD_WIDTH,
        GEM_STACK_H,
        GOLD_STACK_H,
        NOBLE_LENGTH,
        NOBLE_STACK_H,
        NOBLE_TILE_COUNT,
        NOBLE_WIDTH,
        TIER1_CARD_COUNT,
        TIER1_STACK_H,
        TIER2_CARD_COUNT,
        TIER2_STACK_H,
        TIER3_CARD_COUNT,
        TIER3_STACK_H,
        TOKEN_DIAMETER,
        TOKEN_THICKNESS,
    )

# 4. Clearances & Tolerances (Adjustable for 3D printer fit)
CARD_CLEARANCE_W = 1.5  # Total width clearance (0.75mm per side)
CARD_CLEARANCE_L = 1.5  # Total length clearance (0.75mm per side)
NOBLE_CLEARANCE = 1.5
TOKEN_CLEARANCE_D = 1.2  # Diameter clearance for token wells

# 5. Wall & Floor Thicknesses
WALL_THICKNESS = 1.6
FLOOR_THICKNESS = 1.6
OUTER_BOX_WALL = 2.4
OUTER_BOX_FLOOR = 2.0
TRAY_FIT_TOLERANCE = 0.4  # Gap between outer box cavity & trays

# 6. Exterior Dimensions (Uniform height & harmonized footprint)
TRAY_HEIGHT = 24.0

CARD_TRAY_OUTER_W = (
    CARD_WIDTH + CARD_CLEARANCE_W + 2 * WALL_THICKNESS
)  # 67.7 -> rounded to 67.5
CARD_TRAY_OUTER_L = (
    CARD_LENGTH + CARD_CLEARANCE_L + 2 * WALL_THICKNESS
)  # 92.7 -> rounded to 92.5
CARD_TRAY_OUTER_W = 67.5
CARD_TRAY_OUTER_L = 92.5

NOBLE_TRAY_OUTER_W = 67.5
NOBLE_TRAY_OUTER_L = 92.5

TOKEN_TRAY_OUTER_W = 135.0  # 2 * 67.5 = 135.0 mm (fits exactly next to Noble Tray!)
TOKEN_TRAY_OUTER_L = 92.5

# Master Box Internal Cavity Dimensions
MASTER_INNER_W = (
    CARD_TRAY_OUTER_W * 3 + TRAY_FIT_TOLERANCE * 2
)  # 3 card trays = 202.5 + 0.8 = 203.3mm
MASTER_INNER_L = (
    CARD_TRAY_OUTER_L * 2 + TRAY_FIT_TOLERANCE * 2
)  # 2 rows = 185.0 + 0.8 = 185.8mm
MASTER_INNER_H = TRAY_HEIGHT + 0.6

MASTER_OUTER_W = MASTER_INNER_W + 2 * OUTER_BOX_WALL
MASTER_OUTER_L = MASTER_INNER_L + 2 * OUTER_BOX_WALL
MASTER_OUTER_H = MASTER_INNER_H + OUTER_BOX_FLOOR

# Finger Cutout Sizes
SIDE_CUTOUT_W = 28.0
BOTTOM_SLOT_W = 22.0
BOTTOM_SLOT_L = 48.0
TOKEN_FINGER_CHANNEL_W = 18.0

# ==============================================================================
# HELPER GEOMETRY FUNCTIONS
# ==============================================================================


def rounded_box(size, r, center=False):
    """Generates a 3D box with rounded vertical edges."""
    x, y, z = size
    if r <= 0:
        return cube(size, center=center)

    r = min(r, x / 2.0 - 0.01, y / 2.0 - 0.01)
    c2d = (
        translate([r, r])(circle(r=r))
        + translate([x - r, r])(circle(r=r))
        + translate([x - r, y - r])(circle(r=r))
        + translate([r, y - r])(circle(r=r))
    )
    res = linear_extrude(height=z)(hull()(c2d))
    if center:
        res = translate([-x / 2.0, -y / 2.0, -z / 2.0])(res)
    return res


def rounded_slot_2d(w, l):
    """Generates a 2D stadium/slot shape centered at origin."""
    r = w / 2.0
    half_l = max(0.001, (l - w) / 2.0)
    return hull()(
        translate([0, -half_l])(circle(r=r)) + translate([0, half_l])(circle(r=r))
    )


# ==============================================================================
# MODULE 1: REMOVABLE CARD TRAYS (TIER 1, TIER 2, TIER 3)
# ==============================================================================


def generate_card_tray(tier_num, stack_height):
    """
    Creates a removable card tray for a specific Tier deck.
    Includes elevated floor matching stack height, dual side finger cutouts,
    bottom push slot, and embossed tier numerals.
    """
    outer_w = CARD_TRAY_OUTER_W
    outer_l = CARD_TRAY_OUTER_L
    total_h = TRAY_HEIGHT

    card_w = CARD_WIDTH + CARD_CLEARANCE_W
    card_l = CARD_LENGTH + CARD_CLEARANCE_L

    # Calculate floor height so top of stack is slightly below top of tray (~1.5mm rim)
    cavity_depth = stack_height + 2.0
    cavity_depth = min(cavity_depth, total_h - FLOOR_THICKNESS)
    floor_h = total_h - cavity_depth

    # Outer tray shell
    tray_outer = rounded_box([outer_w, outer_l, total_h], r=3.0)

    # Internal card cavity
    cavity_x = (outer_w - card_w) / 2.0
    cavity_y = (outer_l - card_l) / 2.0
    card_cavity = translate([cavity_x, cavity_y, floor_h])(
        rounded_box([card_w, card_l, total_h + 10], r=CARD_CORNER_RADIUS)
    )

    # Side finger cutouts (left and right walls)
    side_cutout_r = SIDE_CUTOUT_W / 2.0
    side_cutout_y = outer_l / 2.0

    left_cutout = translate([-5, side_cutout_y, floor_h + side_cutout_r])(
        rotate([0, 90, 0])(
            linear_extrude(height=outer_w + 10)(
                hull()(
                    circle(r=side_cutout_r)
                    + translate([total_h, 0])(circle(r=side_cutout_r))
                )
            )
        )
    )

    # Bottom push slot (centered in floor)
    bottom_slot_2d = rounded_slot_2d(BOTTOM_SLOT_W, BOTTOM_SLOT_L)
    bottom_slot_3d = translate([outer_w / 2.0, outer_l / 2.0, -1])(
        linear_extrude(height=floor_h + 2)(bottom_slot_2d)
    )

    # Front scoop / window cutout (rounded U-shape)
    front_scoop_w = 32.0
    front_scoop_r = front_scoop_w / 2.0
    front_scoop_2d = hull()(
        circle(r=front_scoop_r)
        + translate([-front_scoop_r, 0])(square([front_scoop_w, total_h + 10]))
    )
    front_scoop = translate(
        [outer_w / 2.0, cavity_y / 2.0, floor_h + front_scoop_r + 2.0]
    )(
        rotate([90, 0, 0])(
            linear_extrude(height=cavity_y + 10, center=True)(front_scoop_2d)
        )
    )

    # Embossed Tier Marker
    tier_roman = "I" if tier_num == 1 else ("II" if tier_num == 2 else "III")
    marker_text = linear_extrude(height=0.8)(
        text(
            tier_roman,
            size=9,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    # Emboss inside card cavity floor
    marker_emboss = translate([outer_w / 2.0, cavity_y + 12.0, floor_h])(marker_text)

    # Front face engraved text
    front_text = linear_extrude(height=0.8)(
        text(
            f"TIER {tier_roman}",
            size=6,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    front_engrave = translate([outer_w / 2.0, 0.4, total_h / 2.0])(
        rotate([90, 0, 0])(front_text)
    )

    result = (tray_outer + marker_emboss) - (
        card_cavity + left_cutout + bottom_slot_3d + front_scoop + front_engrave
    )
    return result


# ==============================================================================
# MODULE 2: REMOVABLE GEM TOKEN TRAY (6 SEPARATE STACK WELLS)
# ==============================================================================


def generate_token_tray():
    """
    Creates a removable token tray holding 6 stacks of gem tokens.
    Layout: 3 columns x 2 rows of token wells.
    Every stack has full-depth side finger channels so each stack can be pulled out separately!
    """
    outer_w = TOKEN_TRAY_OUTER_W
    outer_l = TOKEN_TRAY_OUTER_L
    total_h = TRAY_HEIGHT

    tray_outer = rounded_box([outer_w, outer_l, total_h], r=3.0)

    well_d = TOKEN_DIAMETER + TOKEN_CLEARANCE_D
    well_r = well_d / 2.0

    # 3 columns, 2 rows center coordinates
    col_spacing = outer_w / 3.0
    row_spacing = outer_l / 2.0

    cuts = []

    for row in range(2):
        for col in range(3):
            cx = col_spacing * (col + 0.5)
            cy = row_spacing * (row + 0.5)

            # Gold stack is at col=2, row=1 (5 tokens = 16.7mm), others are 7 tokens = 23.5mm
            is_gold = col == 2 and row == 1
            stack_h = GOLD_STACK_H if is_gold else GEM_STACK_H

            well_depth = min(stack_h + 1.5, total_h - FLOOR_THICKNESS)
            well_floor_z = total_h - well_depth

            # 1. Main cylindrical well
            well_cut = translate([cx, cy, well_floor_z])(
                cylinder(r=well_r, h=total_h + 5)
            )
            cuts.append(well_cut)

            # 2. Dual full-depth finger channels (front and back of each stack)
            channel_w = TOKEN_FINGER_CHANNEL_W
            channel_cut = translate(
                [cx - channel_w / 2.0, cy - well_r - 6, well_floor_z + 1.0]
            )(cube([channel_w, well_d + 12, total_h + 5]))
            cuts.append(channel_cut)

            # 3. Bottom finger push hole
            push_hole = translate([cx, cy, -1])(cylinder(r=9.0, h=well_floor_z + 2))
            cuts.append(push_hole)

            # 4. Chamfer / scoop inside well floor for smooth sliding single tokens out
            ramp_scoop = translate([cx, cy, well_floor_z + 2.0])(
                rotate([0, 90, 0])(cylinder(r=well_r - 2.0, h=channel_w, center=True))
            )
            # We subtract a sphere at bottom center for thumb scoop
            thumb_scoop = translate([cx, cy, well_floor_z + well_r])(sphere(r=well_r))
            # Add subtle floor scoop
            cuts.append(thumb_scoop)

    # Front face text label
    label_text = linear_extrude(height=0.8)(
        text(
            "GEM TOKENS",
            size=6,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    label_engrave = translate([outer_w / 2.0, 0.4, total_h / 2.0])(
        rotate([90, 0, 0])(label_text)
    )
    cuts.append(label_engrave)

    # Subtract all cuts from outer tray shell
    tray_cuts = cuts[0]
    for c in cuts[1:]:
        tray_cuts += c

    return tray_outer - tray_cuts


# ==============================================================================
# MODULE 3: REMOVABLE NOBLE TILE TRAY
# ==============================================================================


def generate_noble_tray():
    """
    Creates a removable Noble Tile tray holding 10 tiles (60x60mm).
    Also includes a side utility compartment for first player marker or extras.
    """
    outer_w = NOBLE_TRAY_OUTER_W
    outer_l = NOBLE_TRAY_OUTER_L
    total_h = TRAY_HEIGHT

    tray_outer = rounded_box([outer_w, outer_l, total_h], r=3.0)

    noble_w = NOBLE_WIDTH + NOBLE_CLEARANCE
    noble_l = NOBLE_LENGTH + NOBLE_CLEARANCE

    stack_h = NOBLE_STACK_H
    cavity_depth = min(stack_h + 1.5, total_h - FLOOR_THICKNESS)
    floor_h = total_h - cavity_depth

    cavity_x = (outer_w - noble_w) / 2.0
    cavity_y = WALL_THICKNESS + 1.0

    # 1. Main Noble Tile Cavity
    noble_cavity = translate([cavity_x, cavity_y, floor_h])(
        rounded_box([noble_w, noble_l, total_h + 5], r=CARD_CORNER_RADIUS)
    )

    # 2. Side Finger Cutouts (left and right)
    side_r = 13.0
    left_cutout = translate([-5, cavity_y + noble_l / 2.0, floor_h + side_r])(
        rotate([0, 90, 0])(
            linear_extrude(height=outer_w + 10)(
                hull()(circle(r=side_r) + translate([total_h, 0])(circle(r=side_r)))
            )
        )
    )

    # 3. Bottom Push Slot
    bottom_slot = translate([outer_w / 2.0, cavity_y + noble_l / 2.0, -1])(
        linear_extrude(height=floor_h + 2)(rounded_slot_2d(20.0, 40.0))
    )

    # 4. Utility Compartment (for First Player tile / accessories)
    util_y = cavity_y + noble_l + WALL_THICKNESS
    util_l = outer_l - util_y - WALL_THICKNESS - 1.0
    util_w = noble_w

    util_cavity = translate([cavity_x, util_y, FLOOR_THICKNESS])(
        rounded_box([util_w, util_l, total_h + 5], r=2.0)
    )

    # Front face text label
    label_text = linear_extrude(height=0.8)(
        text(
            "NOBLES",
            size=6,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    label_engrave = translate([outer_w / 2.0, 0.4, total_h / 2.0])(
        rotate([90, 0, 0])(label_text)
    )

    return tray_outer - (
        noble_cavity + left_cutout + bottom_slot + util_cavity + label_engrave
    )


# ==============================================================================
# MODULE 4: MASTER STORAGE BOX & LID
# ==============================================================================


def generate_master_box():
    """
    Creates the outer master box that neatly organizes all 5 removable module trays.
    Includes side finger scoops for easily grabbing any tray out of the box.
    """
    inner_w = MASTER_INNER_W
    inner_l = MASTER_INNER_L
    inner_h = MASTER_INNER_H

    outer_w = MASTER_OUTER_W
    outer_l = MASTER_OUTER_L
    outer_h = MASTER_OUTER_H

    box_shell = rounded_box([outer_w, outer_l, outer_h], r=4.0)

    # Inner cavity
    cavity = translate([OUTER_BOX_WALL, OUTER_BOX_WALL, OUTER_BOX_FLOOR])(
        rounded_box([inner_w, inner_l, inner_h + 10], r=2.0)
    )

    # Finger relief scoops on outer box walls (4 sides) to lift out trays easily
    scoop_r = 15.0

    # Front & Back scoops
    fb_scoop_y1 = -5
    fb_scoop_y2 = outer_l - OUTER_BOX_WALL - 1

    fb_scoops = translate([outer_w / 2.0, fb_scoop_y1, outer_h])(
        rotate([-90, 0, 0])(cylinder(r=scoop_r, h=outer_l + 10))
    )

    # Side scoops
    side_scoops = translate([-5, outer_l / 2.0, outer_h])(
        rotate([0, 90, 0])(cylinder(r=scoop_r, h=outer_w + 10))
    )

    # Front box label
    box_text = linear_extrude(height=1.0)(
        text(
            "SPLENDOR",
            size=10,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    box_engrave = translate([outer_w / 2.0, 0.5, outer_h / 2.0])(
        rotate([90, 0, 0])(box_text)
    )

    return box_shell - (cavity + fb_scoops + side_scoops + box_engrave)


def generate_master_lid():
    """
    Creates a fitted lid that secures all component trays inside the master box.
    Features an elegant top embossed title and gem logo motif.
    """
    inner_w = MASTER_INNER_W
    inner_l = MASTER_INNER_L

    outer_w = MASTER_OUTER_W
    outer_l = MASTER_OUTER_L

    lid_top_h = 2.0
    rim_h = 4.0
    rim_wall = 1.6

    # Outer lid plate
    lid_plate = rounded_box([outer_w + 0.8, outer_l + 0.8, lid_top_h], r=4.5)

    # Inner alignment rim (fits inside master box cavity)
    rim_w = inner_w - 0.4
    rim_l = inner_l - 0.4

    rim_outer = translate(
        [(outer_w + 0.8 - rim_w) / 2.0, (outer_l + 0.8 - rim_l) / 2.0, lid_top_h]
    )(rounded_box([rim_w, rim_l, rim_h], r=2.0))
    rim_inner = translate(
        [
            (outer_w + 0.8 - rim_w) / 2.0 + rim_wall,
            (outer_l + 0.8 - rim_l) / 2.0 + rim_wall,
            lid_top_h - 0.1,
        ]
    )(rounded_box([rim_w - 2 * rim_wall, rim_l - 2 * rim_wall, rim_h + 1], r=1.5))

    alignment_rim = rim_outer - rim_inner

    # Embossed Top Logo & Artwork
    title_text = linear_extrude(height=1.0)(
        text(
            "S P L E N D O R",
            size=14,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    sub_text = linear_extrude(height=0.8)(
        text(
            "ORGANIZER",
            size=7,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )

    top_title = translate([outer_w / 2.0, outer_l / 2.0 + 8, lid_top_h])(title_text)
    top_sub = translate([outer_w / 2.0, outer_l / 2.0 - 8, lid_top_h])(sub_text)

    # Gem diamond icon
    diamond_2d = polygon([[-8, 0], [0, 12], [8, 0], [0, -12]])
    diamond_3d = translate([outer_w / 2.0 - 50, outer_l / 2.0, lid_top_h])(
        linear_extrude(height=0.8)(scale([0.6, 0.6])(diamond_2d))
    ) + translate([outer_w / 2.0 + 50, outer_l / 2.0, lid_top_h])(
        linear_extrude(height=0.8)(scale([0.6, 0.6])(diamond_2d))
    )

    return lid_plate + alignment_rim + top_title + top_sub + diamond_3d


# ==============================================================================
# FULL ASSEMBLY VISUALIZER
# ==============================================================================


def generate_full_assembly():
    """
    Renders all modules nested in their exact positions inside the master box.
    Useful for visualizing the full assembled organizer layout.
    """
    box = generate_master_box()
    t1 = generate_card_tray(1, TIER1_STACK_H)
    t2 = generate_card_tray(2, TIER2_STACK_H)
    t3 = generate_card_tray(3, TIER3_STACK_H)
    tokens = generate_token_tray()
    nobles = generate_noble_tray()

    base_x = OUTER_BOX_WALL + TRAY_FIT_TOLERANCE / 2.0
    base_y = OUTER_BOX_WALL + TRAY_FIT_TOLERANCE / 2.0
    base_z = OUTER_BOX_FLOOR

    # Row 1 (Back row): Card Trays Tier 1, Tier 2, Tier 3
    row1_y = base_y + CARD_TRAY_OUTER_L + TRAY_FIT_TOLERANCE

    placed_t1 = translate([base_x, row1_y, base_z])(t1)
    placed_t2 = translate([base_x + CARD_TRAY_OUTER_W, row1_y, base_z])(t2)
    placed_t3 = translate([base_x + CARD_TRAY_OUTER_W * 2, row1_y, base_z])(t3)

    # Row 2 (Front row): Token Tray + Noble Tray
    row2_y = base_y
    placed_tokens = translate([base_x, row2_y, base_z])(tokens)
    placed_nobles = translate([base_x + TOKEN_TRAY_OUTER_W, row2_y, base_z])(nobles)

    lid = translate([0, 0, MASTER_OUTER_H + 15.0])(generate_master_lid())

    return box + placed_t1 + placed_t2 + placed_t3 + placed_tokens + placed_nobles + lid
