"""
Splendor Ultra-Compact Travel Box & Organizer
Modeled using SolidPython2 with fully parametric variables.

Designed for portability, lightweight material usage, and fast gameplay setup:
- 3 Card Stacks (Tier 1: 40 cards, Tier 2: 30 cards, Tier 3: 20 cards) in separate wells with rounded finger cutouts.
- 6 Token Stacks (5 gem @ 23.5mm, 1 gold @ 16.7mm) with full-depth finger channels.
- 10 Noble Tiles (stored in 2 stacks of 5 tiles).
- Built-in perimeter snap latch lock mechanism (No rubber band required!).
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

set_global_fn(64)

# ==============================================================================
# PARAMETERS & PARAMETRIC VARIABLES
# ==============================================================================

# Shared Item Dimensions (Imported from dimensions.py)
try:
    from dimensions import (
        CARD_CORNER_RADIUS,
        CARD_LENGTH,
        CARD_WIDTH,
        GEM_STACK_H,
        GOLD_STACK_H,
        NOBLE_5_STACK_H,
        NOBLE_LENGTH,
        NOBLE_WIDTH,
        TIER1_STACK_H,
        TIER2_STACK_H,
        TIER3_STACK_H,
        TOKEN_DIAMETER,
    )
except ImportError:
    from .dimensions import (
        CARD_CORNER_RADIUS,
        CARD_LENGTH,
        CARD_WIDTH,
        GEM_STACK_H,
        GOLD_STACK_H,
        NOBLE_5_STACK_H,
        NOBLE_LENGTH,
        NOBLE_WIDTH,
        TIER1_STACK_H,
        TIER2_STACK_H,
        TIER3_STACK_H,
        TOKEN_DIAMETER,
    )

# Clearances & Tolerances
CARD_CLEARANCE_W = 1.4
CARD_CLEARANCE_L = 1.4
NOBLE_CLEARANCE = 1.4
TOKEN_CLEARANCE_D = 1.2

# Compact Shell Specifications
WALL_THICKNESS = 1.5
FLOOR_THICKNESS = 1.4
LATCH_FIT_CLEARANCE = 0.35

# Inner Cavity & Layout Calculations
# Card Layer: 3 cards side-by-side (width-wise)
CARD_WELL_W = CARD_WIDTH + CARD_CLEARANCE_W  # 64.4mm
CARD_WELL_L = CARD_LENGTH + CARD_CLEARANCE_L  # 89.4mm

INNER_BOX_W = CARD_WELL_W * 3 + WALL_THICKNESS * 2  # 196.2mm
INNER_BOX_L = CARD_WELL_L  # 89.4mm

OUTER_BOX_W = INNER_BOX_W + 2 * WALL_THICKNESS  # 199.2mm
OUTER_BOX_L = INNER_BOX_L + 2 * WALL_THICKNESS  # 92.4mm

# Lower Layer Heights
TOKEN_WELL_DEPTH = GEM_STACK_H + 1.2  # 24.7mm
LOWER_BASE_H = TOKEN_WELL_DEPTH + FLOOR_THICKNESS  # ~26.1mm

# Upper Card Layer Heights
CARD_WELL_DEPTH = TIER1_STACK_H + 1.5  # 15.3mm
UPPER_CARD_H = CARD_WELL_DEPTH + FLOOR_THICKNESS  # ~16.7mm

# Snap Latch Geometry Specifications
DETENT_WIDTH = 18.0
DETENT_HEIGHT = 2.4
DETENT_DEPTH = (
    0.8  # Shallow groove on 1.5mm exterior wall (does NOT penetrate interior)
)
DETENT_Z_FROM_TOP = 5.0  # Distance from top edge of lower base


# Helper: rounded box
def rounded_box(size, r, center=False):
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


# ==============================================================================
# LOWER LAYER: TOKEN & NOBLE BASE
# ==============================================================================


def generate_lower_base():
    """
    Creates the compact lower base containing:
    - 6 token wells (arranged 2x3)
    - 2 noble tile wells (each holding 5 noble tiles)
    - Exterior side detent grooves for lid snap locking (without interior penetration)
    """
    outer_w = OUTER_BOX_W
    outer_l = OUTER_BOX_L
    total_h = LOWER_BASE_H

    base_shell = rounded_box([outer_w, outer_l, total_h], r=3.0)

    cuts = []

    # 1. TOKEN WELLS (6 Stacks: 2 rows x 3 columns)
    well_d = TOKEN_DIAMETER + TOKEN_CLEARANCE_D
    well_r = well_d / 2.0

    token_start_x = WALL_THICKNESS + well_r + 1.0
    col_spacing = well_d + 0.8
    row_spacing = well_d + 0.8
    token_start_y = (outer_l - row_spacing) / 2.0

    for col in range(3):
        cx = token_start_x + col * col_spacing
        for row in range(2):
            cy = token_start_y + row * row_spacing

            is_gold = col == 2 and row == 1
            stack_h = GOLD_STACK_H if is_gold else GEM_STACK_H
            w_depth = stack_h + 1.2
            w_floor_z = total_h - w_depth

            # Well cylinder
            cuts.append(
                translate([cx, cy, w_floor_z])(cylinder(r=well_r, h=total_h))
            )

            # Finger channels (front/back)
            chan_w = 18.0
            cuts.append(
                translate(
                    [cx - chan_w / 2.0, cy - well_r - 4, w_floor_z + 1.0]
                )(cube([chan_w, well_d + 8, total_h]))
            )

            # Bottom push hole
            cuts.append(
                translate([cx, cy, -1])(cylinder(r=9.0, h=w_floor_z + 2))
            )

    # 2. NOBLE TILE WELLS (2 stacks of 5 tiles: 60x60mm each)
    noble_w = NOBLE_WIDTH + NOBLE_CLEARANCE
    noble_l = NOBLE_LENGTH + NOBLE_CLEARANCE
    noble_stack_h = NOBLE_5_STACK_H + 1.0

    noble_floor_z = total_h - noble_stack_h
    noble_x = outer_w - WALL_THICKNESS - noble_w / 2.0 - 2.0

    # Noble tile cut out (holds 2 stacks of 5 tiles)
    noble_cavity = translate(
        [noble_x - noble_w / 2.0, (outer_l - noble_l) / 2.0, noble_floor_z]
    )(rounded_box([noble_w, noble_l, total_h], r=CARD_CORNER_RADIUS))
    cuts.append(noble_cavity)

    # Side finger cutout for noble tiles
    noble_cutout = translate([noble_x - 12, -5, noble_floor_z + 3])(
        cube([24, outer_l + 10, total_h])
    )
    cuts.append(noble_cutout)

    # Bottom push slot for noble tiles
    cuts.append(
        translate([noble_x, outer_l / 2.0, -1])(
            cylinder(r=12.0, h=noble_floor_z + 2)
        )
    )

    # 3. EXTERIOR SNAP DETENT GROOVES (Left and Right short end exterior walls only!)
    detent_z = total_h - DETENT_Z_FROM_TOP
    detent_y = (outer_l - DETENT_WIDTH) / 2.0

    # Left wall exterior groove
    left_groove = translate([-0.1, detent_y, detent_z])(
        cube([DETENT_DEPTH + 0.1, DETENT_WIDTH, DETENT_HEIGHT])
    )
    # Right wall exterior groove
    right_groove = translate([outer_w - DETENT_DEPTH, detent_y, detent_z])(
        cube([DETENT_DEPTH + 0.1, DETENT_WIDTH, DETENT_HEIGHT])
    )

    cuts.append(left_groove)
    cuts.append(right_groove)

    # Subtract all cuts from outer base shell
    tray_cuts = cuts[0]
    for c in cuts[1:]:
        tray_cuts += c

    return base_shell - tray_cuts


# ==============================================================================
# UPPER LAYER: CARD DECK HOLDER TRAY (3 SEPARATE TIERS)
# ==============================================================================


def generate_card_tray():
    """
    Creates the upper card tray with 3 separate card wells (Tier 1, Tier 2, Tier 3).
    Each card stack can be pulled out separately!
    """
    outer_w = OUTER_BOX_W
    outer_l = OUTER_BOX_L
    total_h = UPPER_CARD_H

    tray_outer = rounded_box([outer_w, outer_l, total_h], r=3.0)

    card_w = CARD_WELL_W
    card_l = CARD_WELL_L

    cuts = []

    # 3 Card Wells Side-by-Side
    tiers = [(1, TIER1_STACK_H), (2, TIER2_STACK_H), (3, TIER3_STACK_H)]
    col_w = (outer_w - 2 * WALL_THICKNESS) / 3.0

    for idx, (tier_num, stack_h) in enumerate(tiers):
        cx = WALL_THICKNESS + idx * col_w + col_w / 2.0
        cy = outer_l / 2.0

        cavity_depth = stack_h + 1.5
        floor_z = total_h - cavity_depth

        # 1. Card Cavity
        well_cut = translate([cx - card_w / 2.0, cy - card_l / 2.0, floor_z])(
            rounded_box([card_w, card_l, total_h + 5], r=CARD_CORNER_RADIUS)
        )
        cuts.append(well_cut)

        # 2. Dual rounded U-shaped finger cutouts (front & back walls)
        scoop_w = 26.0
        scoop_r = scoop_w / 2.0
        scoop_shape_2d = hull()(
            circle(r=scoop_r)
            + translate([-scoop_r, 0])(square([scoop_w, total_h + 10]))
        )
        scoop_cut = translate([cx, outer_l / 2.0, floor_z + scoop_r])(
            rotate([90, 0, 0])(
                linear_extrude(height=outer_l + 10, center=True)(scoop_shape_2d)
            )
        )
        cuts.append(scoop_cut)

        # 3. Bottom finger push slot
        push_slot = translate([cx, cy, -1])(
            linear_extrude(height=floor_z + 2)(
                hull()(
                    translate([0, -15])(circle(r=9))
                    + translate([0, 15])(circle(r=9))
                )
            )
        )
        cuts.append(push_slot)

        # 4. Embossed Tier numeral in cavity floor
        tier_roman = (
            "I" if tier_num == 1 else ("II" if tier_num == 2 else "III")
        )
        marker = linear_extrude(height=0.8)(
            text(
                tier_roman,
                size=8,
                font="Liberation Sans:style=Bold",
                halign="center",
                valign="center",
            )
        )
        cuts.append(translate([cx, cy - 25, floor_z])(marker))

    tray_cuts = cuts[0]
    for c in cuts[1:]:
        tray_cuts += c

    return tray_outer - tray_cuts


# ==============================================================================
# TRAVEL SNAP LID & LATCH MECHANISM
# ==============================================================================


def generate_travel_lid():
    """
    Creates a travel lid with integrated side snap-latches/tabs near the bottom
    skirt edge that align precisely with the detents on the lower base.
    """
    fit_tol = LATCH_FIT_CLEARANCE  # 0.35mm tolerance for sliding fit
    lid_inner_w = OUTER_BOX_W + 2 * fit_tol
    lid_inner_l = OUTER_BOX_L + 2 * fit_tol

    wall = WALL_THICKNESS
    lid_outer_w = lid_inner_w + 2 * wall
    lid_outer_l = lid_inner_l + 2 * wall

    top_plate_h = 1.8
    # Skirt depth extends over top card tray (~16.7mm) + 6.0mm down lower base = ~22.7mm skirt height
    skirt_overlap_base = 6.0
    skirt_depth = UPPER_CARD_H + skirt_overlap_base
    total_lid_h = skirt_depth + top_plate_h

    # Local Z layout:
    # Z = 0: Bottom rim of lid skirt
    # Z = skirt_depth (22.7mm): Top of skirt / bottom of top plate
    # Z = total_lid_h (24.5mm): Top outer surface of lid

    # 1. Outer lid shell (skirt + top plate)
    lid_shell = rounded_box([lid_outer_w, lid_outer_l, total_lid_h], r=4.0)

    # 2. Hollow cavity inside skirt (opening from bottom Z=0 up to top plate underside Z=skirt_depth)
    cavity = translate([wall, wall, -1])(
        rounded_box([lid_inner_w, lid_inner_l, skirt_depth + 1], r=3.0)
    )

    # 3. Integrated Inward Snap Tabs (positioned near bottom skirt rim Z=0!)
    tab_w = DETENT_WIDTH - 0.4  # 17.6mm width
    tab_h = DETENT_HEIGHT - 0.2  # 2.2mm height
    tab_proj = DETENT_DEPTH - 0.1  # 0.7mm protrusion into base detent

    tab_y = (lid_outer_l - tab_w) / 2.0
    # Center of tab relative to skirt bottom (z=0):
    # detent center on base is at Z = (LOWER_BASE_H - DETENT_Z_FROM_TOP + DETENT_HEIGHT/2.0) = 26.1 - 5.0 + 1.2 = 22.3mm
    # Lid skirt bottom sits at Z = (LOWER_BASE_H - skirt_overlap_base) = 26.1 - 6.0 = 20.1mm
    # So tab_center_local_z = 22.3 - 20.1 = 2.2mm above skirt bottom (z=0)!
    tab_local_z = 2.2 - (tab_h / 2.0)  # ~1.1mm above bottom edge

    left_tab = translate([wall, tab_y, tab_local_z])(
        cube([tab_proj, tab_w, tab_h])
    )
    right_tab = translate([lid_outer_w - wall - tab_proj, tab_y, tab_local_z])(
        cube([tab_proj, tab_w, tab_h])
    )

    # 4. Finger-pull tabs attached to bottom edge of skirt (Z=0 to Z=6.0mm)
    pull_tab_w = 24.0
    pull_tab_l = 3.0
    pull_left = translate([-pull_tab_l, (lid_outer_l - pull_tab_w) / 2.0, 0])(
        rounded_box([pull_tab_l + wall, pull_tab_w, 6.0], r=1.5)
    )
    pull_right = translate(
        [lid_outer_w - wall, (lid_outer_l - pull_tab_w) / 2.0, 0]
    )(rounded_box([pull_tab_l + wall, pull_tab_w, 6.0], r=1.5))

    # 5. Top embossed logo (on outer top plate Z=total_lid_h)
    logo_text = linear_extrude(height=0.8)(
        text(
            "SPLENDOR",
            size=12,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    logo_emboss = translate(
        [lid_outer_w / 2.0, lid_outer_l / 2.0, total_lid_h]
    )(logo_text)

    return (
        (lid_shell - cavity)
        + left_tab
        + right_tab
        + pull_left
        + pull_right
        + logo_emboss
    )


def generate_travel_assembly():
    """
    Generates full stacked assembly of the Travel Box system.
    """
    base = generate_lower_base()
    cards = translate([0, 0, LOWER_BASE_H])(generate_card_tray())

    # Position lid upright over cards & lower base
    fit_tol = LATCH_FIT_CLEARANCE
    lid_x = -fit_tol - WALL_THICKNESS
    lid_y = -fit_tol - WALL_THICKNESS
    # Skirt bottom rests at LOWER_BASE_H - 6.0mm so snap tab at local_z=1.1mm aligns with base detent at Z=22.3mm!
    lid_z = LOWER_BASE_H - 6.0

    lid = translate([lid_x, lid_y, lid_z])(generate_travel_lid())
    return base + cards + lid
