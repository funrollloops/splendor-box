"""
Splendor 2-Piece Ultra-Compact Travel Box
Modeled using SolidPython2 with fully parametric variables.

Features:
- Exactly 2 printable parts: Bottom Skeletal Tray + Top Enclosing Lid.
- Bottom Layer:
  - 10 Noble Tiles (60x60mm x 16.62mm) at the bottom left.
  - 6 Token Stacks (5 gem @ 23.5mm, 1 gold @ 16.7mm) at the bottom right.
- Top Layer:
  - Tier 1 Cards (40 cards, 13.8mm) stacked ON TOP of the Noble tiles.
  - Tier 2 Cards (30 cards, 10.2mm) & Tier 3 Cards (20 cards, 6.9mm) stacked ON TOP of the Gem tokens.
- Minimal skeleton frame with maximum finger accessibility around tokens, nobles, and decks.
- Perimeter snap latch lid locks everything securely for travel without rubber bands.
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

# Card Specifications
CARD_WIDTH = 63.0
CARD_LENGTH = 88.0
CARD_CORNER_RADIUS = 3.5

TIER1_STACK_H = 13.8
TIER2_STACK_H = 10.2
TIER3_STACK_H = 6.9

# Noble Tile Specifications (10 tiles)
NOBLE_WIDTH = 60.0
NOBLE_LENGTH = 60.0
NOBLE_STACK_H = 16.62

# Gem Token Specifications (6 stacks)
TOKEN_DIAMETER = 43.0
GEM_STACK_H = 23.50  # 7 tokens
GOLD_STACK_H = 16.70  # 5 tokens

# Clearances & Tolerances
CARD_CLEARANCE_W = 1.4
CARD_CLEARANCE_L = 1.4
NOBLE_CLEARANCE = 1.4
TOKEN_CLEARANCE_D = 1.2
LATCH_FIT_CLEARANCE = 0.35

# Frame & Wall Specifications
FRAME_WALL = 1.5
SHELF_THICKNESS = 1.4
BASE_FLOOR_THICKNESS = 1.4

# Layout Dimensions
# Left Section: Nobles (bottom) + Tier 1 Cards (top)
LEFT_SECTION_W = max(
    NOBLE_WIDTH + NOBLE_CLEARANCE, CARD_WIDTH + CARD_CLEARANCE_W
)  # ~64.4mm
SECTION_L = CARD_LENGTH + CARD_CLEARANCE_L  # 89.4mm

# Right Section: 6 Tokens in 2x3 grid (bottom) + Tier 2 & Tier 3 Cards (top)
TOKEN_WELL_D = TOKEN_DIAMETER + TOKEN_CLEARANCE_D  # 44.2mm
RIGHT_SECTION_W = TOKEN_WELL_D * 3 + 1.2  # 133.8mm

# Total Inner Footprint
TOTAL_INNER_W = LEFT_SECTION_W + FRAME_WALL + RIGHT_SECTION_W  # ~199.7mm
TOTAL_INNER_L = SECTION_L  # 89.4mm

TOTAL_OUTER_W = TOTAL_INNER_W + 2 * FRAME_WALL  # ~202.7mm
TOTAL_OUTER_L = TOTAL_INNER_L + 2 * FRAME_WALL  # ~92.4mm

# Vertical Heights
NOBLE_SHELF_Z = BASE_FLOOR_THICKNESS + NOBLE_STACK_H + 0.4  # ~18.4mm
TIER1_TOP_Z = NOBLE_SHELF_Z + TIER1_STACK_H + 0.5  # ~32.7mm

TOKEN_SHELF_Z = BASE_FLOOR_THICKNESS + GEM_STACK_H + 0.4  # ~25.3mm
TIER2_TOP_Z = TOKEN_SHELF_Z + TIER2_STACK_H + 0.5  # ~36.0mm

FRAME_MAX_H = TIER2_TOP_Z  # ~36.0mm

# Snap Detent Specs
DETENT_WIDTH = 18.0
DETENT_HEIGHT = 2.4
DETENT_DEPTH = 0.8
DETENT_Z = 12.0  # Height above bottom base for detent groove


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
# PIECE 1: BOTTOM SKELETON FRAME & TRAY
# ==============================================================================


def generate_bottom_frame():
    """
    Creates the open skeletal frame holding:
    - Bottom Left: 10 Noble Tiles (60x60mm)
    - Top Left (above Nobles): Tier 1 Cards (40 cards)
    - Bottom Right: 6 Gem Token Stacks (2x3 grid)
    - Top Right (above Tokens): Tier 2 Cards & Tier 3 Cards side-by-side
    - Large finger cutouts everywhere with skeleton trusses for maximum material efficiency.
    """
    outer_w = TOTAL_OUTER_W
    outer_l = TOTAL_OUTER_L
    total_h = FRAME_MAX_H

    # Outer perimeter skeleton box
    outer_shell = rounded_box([outer_w, outer_l, total_h], r=3.5)

    cuts = []

    # --------------------------------------------------------------------------
    # 1. LEFT SECTION: NOBLES (BOTTOM) + TIER 1 CARDS (TOP)
    # --------------------------------------------------------------------------
    noble_w = NOBLE_WIDTH + NOBLE_CLEARANCE
    noble_l = NOBLE_LENGTH + NOBLE_CLEARANCE

    noble_x = FRAME_WALL + (LEFT_SECTION_W - noble_w) / 2.0
    noble_y = FRAME_WALL + (SECTION_L - noble_l) / 2.0

    # Noble bottom cavity
    noble_cavity = translate([noble_x, noble_y, BASE_FLOOR_THICKNESS])(
        rounded_box([noble_w, noble_l, NOBLE_SHELF_Z], r=CARD_CORNER_RADIUS)
    )
    cuts.append(noble_cavity)

    # Noble finger cutouts (front & back and side)
    noble_finger_y = translate([noble_x + 12, -5, BASE_FLOOR_THICKNESS + 2])(
        cube([noble_w - 24, outer_l + 10, NOBLE_SHELF_Z])
    )
    noble_finger_x = translate([-5, noble_y + 12, BASE_FLOOR_THICKNESS + 2])(
        cube([LEFT_SECTION_W + 10, noble_l - 24, NOBLE_SHELF_Z])
    )
    noble_bottom_hole = translate(
        [noble_x + noble_w / 2.0, noble_y + noble_l / 2.0, -1]
    )(cylinder(r=15.0, h=BASE_FLOOR_THICKNESS + 2))
    cuts.append(noble_finger_y)
    cuts.append(noble_finger_x)
    cuts.append(noble_bottom_hole)

    # Tier 1 Card Deck Well (above Nobles)
    card1_w = CARD_WIDTH + CARD_CLEARANCE_W
    card1_l = CARD_LENGTH + CARD_CLEARANCE_L
    card1_x = FRAME_WALL + (LEFT_SECTION_W - card1_w) / 2.0
    card1_y = FRAME_WALL + (SECTION_L - card1_l) / 2.0

    card1_cavity = translate([card1_x, card1_y, NOBLE_SHELF_Z])(
        rounded_box([card1_w, card1_l, total_h + 5], r=CARD_CORNER_RADIUS)
    )
    cuts.append(card1_cavity)

    # Tier 1 rounded U-shaped finger scoops (front & back)
    t1_scoop_w = 28.0
    t1_scoop_r = t1_scoop_w / 2.0
    t1_scoop_2d = hull()(
        circle(r=t1_scoop_r)
        + translate([-t1_scoop_r, 0])(square([t1_scoop_w, total_h + 10]))
    )
    t1_scoop_cut = translate(
        [card1_x + card1_w / 2.0, outer_l / 2.0, NOBLE_SHELF_Z + t1_scoop_r]
    )(rotate([90, 0, 0])(linear_extrude(height=outer_l + 10, center=True)(t1_scoop_2d)))
    cuts.append(t1_scoop_cut)

    # --------------------------------------------------------------------------
    # 2. RIGHT SECTION: GEM TOKENS (BOTTOM) + TIER 2 & 3 CARDS (TOP)
    # --------------------------------------------------------------------------
    right_x_start = FRAME_WALL + LEFT_SECTION_W + FRAME_WALL
    well_d = TOKEN_WELL_D
    well_r = well_d / 2.0

    col_spacing = well_d
    row_spacing = well_d
    token_start_x = right_x_start + well_r + 0.6
    token_start_y = FRAME_WALL + well_r + (SECTION_L - 2 * well_d) / 2.0

    for col in range(3):
        cx = token_start_x + col * col_spacing
        for row in range(2):
            cy = token_start_y + row * row_spacing

            is_gold = col == 2 and row == 1
            stack_h = GOLD_STACK_H if is_gold else GEM_STACK_H
            w_floor_z = BASE_FLOOR_THICKNESS

            # Main token cylinder cutout
            cuts.append(
                translate([cx, cy, w_floor_z])(cylinder(r=well_r, h=TOKEN_SHELF_Z + 5))
            )

            # Full skeleton side cutouts around tokens for maximum finger room
            chan_w = 20.0
            cuts.append(
                translate([cx - chan_w / 2.0, cy - well_r - 4, w_floor_z + 1.0])(
                    cube([chan_w, well_d + 8, TOKEN_SHELF_Z])
                )
            )

            # Bottom push hole under each token stack
            cuts.append(
                translate([cx, cy, -1])(cylinder(r=10.0, h=BASE_FLOOR_THICKNESS + 2))
            )

    # Tier 2 & Tier 3 Card Deck Wells (above Tokens)
    card2_w = CARD_WIDTH + CARD_CLEARANCE_W
    card2_l = CARD_LENGTH + CARD_CLEARANCE_L

    # Tier 2 Deck sits over Token Columns 0 & 1
    t2_x = right_x_start + 1.0
    t2_y = FRAME_WALL + (SECTION_L - card2_l) / 2.0

    card2_cavity = translate([t2_x, t2_y, TOKEN_SHELF_Z])(
        rounded_box([card2_w, card2_l, total_h + 5], r=CARD_CORNER_RADIUS)
    )
    cuts.append(card2_cavity)

    # Tier 2 rounded U-shaped finger scoops
    t2_scoop_cut = translate(
        [t2_x + card2_w / 2.0, outer_l / 2.0, TOKEN_SHELF_Z + t1_scoop_r]
    )(rotate([90, 0, 0])(linear_extrude(height=outer_l + 10, center=True)(t1_scoop_2d)))
    cuts.append(t2_scoop_cut)

    # Tier 3 Deck sits over Token Column 2
    t3_x = t2_x + card2_w + FRAME_WALL
    t3_y = t2_y
    t3_floor_z = TOKEN_SHELF_Z + (
        TIER2_STACK_H - TIER3_STACK_H
    )  # Raised so top aligns with Tier 2!

    card3_cavity = translate([t3_x, t3_y, t3_floor_z])(
        rounded_box([card2_w, card2_l, total_h + 5], r=CARD_CORNER_RADIUS)
    )
    cuts.append(card3_cavity)

    # Tier 3 rounded U-shaped finger scoops
    t3_scoop_cut = translate(
        [t3_x + card2_w / 2.0, outer_l / 2.0, t3_floor_z + t1_scoop_r]
    )(rotate([90, 0, 0])(linear_extrude(height=outer_l + 10, center=True)(t1_scoop_2d)))
    cuts.append(t3_scoop_cut)

    # --------------------------------------------------------------------------
    # 3. EXTERIOR SNAP DETENT GROOVES (Left and Right short end exterior walls)
    # --------------------------------------------------------------------------
    detent_y = (outer_l - DETENT_WIDTH) / 2.0

    left_groove = translate([-0.1, detent_y, DETENT_Z])(
        cube([DETENT_DEPTH + 0.1, DETENT_WIDTH, DETENT_HEIGHT])
    )
    right_groove = translate([outer_w - DETENT_DEPTH, detent_y, DETENT_Z])(
        cube([DETENT_DEPTH + 0.1, DETENT_WIDTH, DETENT_HEIGHT])
    )
    cuts.append(left_groove)
    cuts.append(right_groove)

    # Subtract all cuts from outer perimeter shell
    tray_cuts = cuts[0]
    for c in cuts[1:]:
        tray_cuts += c

    return outer_shell - tray_cuts


# ==============================================================================
# PIECE 2: TOP ENCLOSING LID & SNAP LATCH
# ==============================================================================


def generate_top_lid():
    """
    Creates the top enclosing lid shell that slides over the loaded bottom frame.
    Holds cards, tokens, and noble tiles flush in place for travel.
    Features integrated snap tabs that lock into base detents.
    """
    fit_tol = LATCH_FIT_CLEARANCE
    lid_inner_w = TOTAL_OUTER_W + 2 * fit_tol
    lid_inner_l = TOTAL_OUTER_L + 2 * fit_tol

    wall = FRAME_WALL
    lid_outer_w = lid_inner_w + 2 * wall
    lid_outer_l = lid_inner_l + 2 * wall

    top_plate_h = 1.8
    skirt_depth = FRAME_MAX_H + 1.0  # Full height skirt enclosing bottom frame
    total_lid_h = skirt_depth + top_plate_h

    # 1. Outer lid cap with skirt
    lid_shell = rounded_box([lid_outer_w, lid_outer_l, total_lid_h], r=4.0)

    # 2. Hollow cavity inside skirt
    cavity = translate([wall, wall, -1])(
        rounded_box([lid_inner_w, lid_inner_l, skirt_depth + 1], r=3.0)
    )

    # 3. Inward Snap Tabs (positioned near bottom skirt rim Z=0!)
    tab_w = DETENT_WIDTH - 0.4
    tab_h = DETENT_HEIGHT - 0.2
    tab_proj = DETENT_DEPTH - 0.1

    tab_y = (lid_outer_l - tab_w) / 2.0
    tab_local_z = DETENT_Z + 1.0 - (tab_h / 2.0)

    left_tab = translate([wall, tab_y, tab_local_z])(cube([tab_proj, tab_w, tab_h]))
    right_tab = translate([lid_outer_w - wall - tab_proj, tab_y, tab_local_z])(
        cube([tab_proj, tab_w, tab_h])
    )

    # 4. Finger-pull tabs on bottom edge of short end skirts
    pull_tab_w = 26.0
    pull_tab_l = 3.0
    pull_left = translate([-pull_tab_l, (lid_outer_l - pull_tab_w) / 2.0, 0])(
        rounded_box([pull_tab_l + wall, pull_tab_w, 7.0], r=1.5)
    )
    pull_right = translate([lid_outer_w - wall, (lid_outer_l - pull_tab_w) / 2.0, 0])(
        rounded_box([pull_tab_l + wall, pull_tab_w, 7.0], r=1.5)
    )

    # 5. Top embossed logo
    logo_text = linear_extrude(height=0.8)(
        text(
            "SPLENDOR",
            size=13,
            font="Liberation Sans:style=Bold",
            halign="center",
            valign="center",
        )
    )
    logo_emboss = translate([lid_outer_w / 2.0, lid_outer_l / 2.0, total_lid_h])(
        logo_text
    )

    return (
        (lid_shell - cavity)
        + left_tab
        + right_tab
        + pull_left
        + pull_right
        + logo_emboss
    )


def generate_two_piece_assembly():
    """
    Generates full assembled model showing bottom frame + top lid enclosing it.
    """
    base = generate_bottom_frame()

    fit_tol = LATCH_FIT_CLEARANCE
    lid_x = -fit_tol - FRAME_WALL
    lid_y = -fit_tol - FRAME_WALL
    lid_z = -1.0

    lid = translate([lid_x, lid_y, lid_z])(generate_top_lid())
    return base + lid
