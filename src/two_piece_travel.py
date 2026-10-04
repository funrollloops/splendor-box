"""
Splendor 2-Piece Ultra-Compact Travel Box
Modeled using SolidPython2 with fully parametric variables.

Features:
- Exactly 2 printable parts: Bottom Skeletal Tray + Top Enclosing Lid.
- Bottom Layer:
  - 10 Noble Tiles (60x60mm x 16.62mm) at the bottom left with dedicated front, back, and side finger cutouts.
  - 6 Token Stacks (5 gem @ 23.5mm, 1 gold @ 16.7mm) at the bottom right.
- Top Layer:
  - Tier 1 Cards (40 cards, 13.8mm) stacked ON TOP of the Noble tiles (resting on the Tier 1 shelf at Z = NOBLE_SHELF_Z).
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

# Shared Item Dimensions (Imported from dimensions.py)
try:
    from dimensions import (
        CARD_CORNER_RADIUS,
        CARD_LENGTH,
        CARD_WIDTH,
        GEM_STACK_H,
        GOLD_STACK_H,
        NOBLE_LENGTH,
        NOBLE_STACK_H,
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
        NOBLE_LENGTH,
        NOBLE_STACK_H,
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


def double_concave_fillet(r, gap, depth, h):
    """
    Generates a 3D double-concave fillet separator that cradles
    the rounded corners of two adjacent card stacks.
    Base is along the wall (y=0) extending into +y.
    """
    x_c = gap / 2.0 + r
    y_c = r
    w_base = 2 * x_c + 0.2
    base_block = translate([-w_base / 2.0, -0.2])(square([w_base, depth + 0.2]))
    circle_left = translate([-x_c, y_c])(circle(r=r))
    circle_right = translate([x_c, y_c])(circle(r=r))
    profile_2d = base_block - (circle_left + circle_right)
    return linear_extrude(height=h)(profile_2d)


# ==============================================================================
# PIECE 1: BOTTOM SKELETON FRAME & TRAY
# ==============================================================================


def generate_bottom_frame():
    """
    Creates the open skeletal frame holding:
    - Bottom Left: 10 Noble Tiles (60x60mm) with front, back, and side finger cutouts
    - Top Left (above Nobles): Tier 1 Cards (40 cards) resting on NOBLE_SHELF_Z
    - Bottom Right: 6 Gem Token Stacks (2x3 grid) from Z = BASE_FLOOR_THICKNESS to TOKEN_SHELF_Z
    - Top Right (above Tokens): Tier 2 & Tier 3 Cards resting on TOKEN_SHELF_Z
    """
    outer_w = TOTAL_OUTER_W
    outer_l = TOTAL_OUTER_L
    total_h = FRAME_MAX_H

    outer_shell = rounded_box([outer_w, outer_l, total_h], r=3.5)

    cuts = []

    # --------------------------------------------------------------------------
    # 1. LEFT SECTION: NOBLES (BOTTOM) + TIER 1 CARDS (TOP)
    # --------------------------------------------------------------------------
    noble_w = NOBLE_WIDTH + NOBLE_CLEARANCE
    noble_l = NOBLE_LENGTH + NOBLE_CLEARANCE

    noble_x = FRAME_WALL + (LEFT_SECTION_W - noble_w) / 2.0
    noble_y = FRAME_WALL + (SECTION_L - noble_l) / 2.0

    # 1a. Noble Bottom Cavity (up to NOBLE_SHELF_Z)
    noble_cavity_h = NOBLE_SHELF_Z - BASE_FLOOR_THICKNESS
    noble_cavity = translate([noble_x, noble_y, BASE_FLOOR_THICKNESS])(
        rounded_box([noble_w, noble_l, noble_cavity_h + 0.1], r=CARD_CORNER_RADIUS)
    )
    cuts.append(noble_cavity)

    # Noble bottom finger push hole
    noble_bottom_hole = translate(
        [noble_x + noble_w / 2.0, noble_y + noble_l / 2.0, -2]
    )(cylinder(r=15.0, h=BASE_FLOOR_THICKNESS + 4))
    cuts.append(noble_bottom_hole)

    # Dedicated Noble Side Finger Cutouts (front/back and left outer wall)
    noble_scoop_w = 26.0
    noble_scoop_r = noble_scoop_w / 2.0
    noble_scoop_2d = hull()(
        circle(r=noble_scoop_r)
        + translate([-noble_scoop_r, 0])(square([noble_scoop_w, total_h + 10]))
    )

    # Front/Back Noble finger scoops
    noble_fb_scoop = translate(
        [noble_x + noble_w / 2.0, outer_l / 2.0, BASE_FLOOR_THICKNESS + noble_scoop_r]
    )(
        rotate([90, 0, 0])(
            linear_extrude(height=outer_l + 10, center=True)(noble_scoop_2d)
        )
    )
    cuts.append(noble_fb_scoop)

    # 1b. Tier 1 Lower Card Cavity (resting on NOBLE_SHELF_Z above Nobles, up to TOKEN_SHELF_Z)
    card1_w = CARD_WIDTH + CARD_CLEARANCE_W
    card1_l = CARD_LENGTH + CARD_CLEARANCE_L
    card1_x = FRAME_WALL + (LEFT_SECTION_W - card1_w) / 2.0
    card1_y = FRAME_WALL + (SECTION_L - card1_l) / 2.0

    t1_lower_h = TOKEN_SHELF_Z - NOBLE_SHELF_Z + 0.1
    card1_lower_cavity = translate([card1_x, card1_y, NOBLE_SHELF_Z])(
        rounded_box([card1_w, card1_l, t1_lower_h], r=CARD_CORNER_RADIUS)
    )
    cuts.append(card1_lower_cavity)

    # Tier 1 card deck U-shaped finger scoops (front & back)
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

    # 2a. 6 Token Wells (from BASE_FLOOR_THICKNESS up to TOKEN_SHELF_Z)
    w_floor_z = BASE_FLOOR_THICKNESS
    for col in range(3):
        cx = token_start_x + col * col_spacing
        for row in range(2):
            cy = token_start_y + row * row_spacing

            # Main token cylinder cutout
            cuts.append(
                translate([cx, cy, w_floor_z])(
                    cylinder(r=well_r, h=TOKEN_SHELF_Z - w_floor_z + 0.1)
                )
            )

            # Bottom push hole under each token stack
            cuts.append(
                translate([cx, cy, -2])(cylinder(r=10.0, h=BASE_FLOOR_THICKNESS + 4))
            )

    # Four rectangular prisms to create space for fingers, laid out in a rectangle
    # with each corner at the center of one of a corner token stack (30mm wide cutouts).
    cutout_w = 30.0
    x_left = token_start_x
    x_right = token_start_x + 2 * col_spacing
    y_bottom = token_start_y
    y_top = token_start_y + row_spacing
    chan_z = w_floor_z + 1.0
    chan_h = TOKEN_SHELF_Z - w_floor_z

    # Bottom horizontal prism: from (x_left, y_bottom) to (x_right, y_bottom)
    cuts.append(
        translate([x_left, y_bottom - cutout_w / 2.0, chan_z])(
            cube([x_right - x_left, cutout_w, chan_h])
        )
    )
    # Top horizontal prism: from (x_left, y_top) to (x_right, y_top)
    cuts.append(
        translate([x_left, y_top - cutout_w / 2.0, chan_z])(
            cube([x_right - x_left, cutout_w, chan_h])
        )
    )
    # Left vertical prism: from (x_left, y_bottom) to (x_left, y_top)
    cuts.append(
        translate([x_left - cutout_w / 2.0, y_bottom, chan_z])(
            cube([cutout_w, y_top - y_bottom, chan_h])
        )
    )
    # Right vertical prism: from (x_right, y_bottom) to (x_right, y_top)
    cuts.append(
        translate([x_right - cutout_w / 2.0, y_bottom, chan_z])(
            cube([cutout_w, y_top - y_bottom, chan_h])
        )
    )

    # 2b. Continuous Card Bay across Tier 1, 2 & 3 (resting on TOKEN_SHELF_Z)
    card2_w = CARD_WIDTH + CARD_CLEARANCE_W
    card2_l = CARD_LENGTH + CARD_CLEARANCE_L
    card_gap = 2.0

    t1_x = card1_x
    t2_x = t1_x + card1_w + card_gap
    t3_x = t2_x + card2_w + card_gap

    right_end_x = t3_x + card2_w + 1.5
    upper_card_bay_w = right_end_x - card1_x

    # Continuous upper cavity for all 3 decks above TOKEN_SHELF_Z (no thick divider wall)
    upper_card_bay = translate([card1_x, card1_y, TOKEN_SHELF_Z])(
        rounded_box([upper_card_bay_w, card1_l, total_h + 10], r=CARD_CORNER_RADIUS)
    )
    cuts.append(upper_card_bay)

    # Tier 2 rounded U-shaped finger scoops (front & back)
    t2_scoop_cut = translate(
        [t2_x + card2_w / 2.0, outer_l / 2.0, TOKEN_SHELF_Z + t1_scoop_r]
    )(rotate([90, 0, 0])(linear_extrude(height=outer_l + 10, center=True)(t1_scoop_2d)))
    cuts.append(t2_scoop_cut)

    # Tier 3 rounded U-shaped finger scoops (front & back)
    t3_scoop_cut = translate(
        [t3_x + card2_w / 2.0, outer_l / 2.0, TOKEN_SHELF_Z + t1_scoop_r]
    )(rotate([90, 0, 0])(linear_extrude(height=outer_l + 10, center=True)(t1_scoop_2d)))
    cuts.append(t3_scoop_cut)

    # --------------------------------------------------------------------------
    # 3. EXTERIOR SNAP DETENT GROOVES (Left and Right short end exterior walls)
    # --------------------------------------------------------------------------
    detent_y = (outer_l - DETENT_WIDTH) / 2.0

    left_groove = translate([-0.2, detent_y, DETENT_Z])(
        cube([DETENT_DEPTH + 0.2, DETENT_WIDTH, DETENT_HEIGHT])
    )
    right_groove = translate([outer_w - DETENT_DEPTH, detent_y, DETENT_Z])(
        cube([DETENT_DEPTH + 0.2, DETENT_WIDTH, DETENT_HEIGHT])
    )
    cuts.append(left_groove)
    cuts.append(right_groove)

    # Union all cuts into a single clean CSG object before difference
    all_cuts = cuts[0]
    for c in cuts[1:]:
        all_cuts = all_cuts + c

    # Double-concave fillet dividers between card stacks on front & back walls
    # (between Tier 1 & 2, and between Tier 2 & 3)
    x_fillet1 = t1_x + card1_w + card_gap / 2.0
    x_fillet2 = t2_x + card2_w + card_gap / 2.0

    fillet_z = TOKEN_SHELF_Z
    fillet_h = total_h - fillet_z
    fillet_depth = 3.0

    fillets = (
        # Fillet between Tier 1 and Tier 2 (front wall & back wall)
        translate([x_fillet1, card1_y, fillet_z])(
            double_concave_fillet(
                r=CARD_CORNER_RADIUS, gap=card_gap, depth=fillet_depth, h=fillet_h
            )
        )
        + translate([x_fillet1, card1_y + card1_l, fillet_z])(
            rotate([0, 0, 180])(
                double_concave_fillet(
                    r=CARD_CORNER_RADIUS, gap=card_gap, depth=fillet_depth, h=fillet_h
                )
            )
        )
        # Fillet between Tier 2 and Tier 3 (front wall & back wall)
        + translate([x_fillet2, card1_y, fillet_z])(
            double_concave_fillet(
                r=CARD_CORNER_RADIUS, gap=card_gap, depth=fillet_depth, h=fillet_h
            )
        )
        + translate([x_fillet2, card1_y + card1_l, fillet_z])(
            rotate([0, 0, 180])(
                double_concave_fillet(
                    r=CARD_CORNER_RADIUS, gap=card_gap, depth=fillet_depth, h=fillet_h
                )
            )
        )
    )

    return (outer_shell - all_cuts) + fillets


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
        rounded_box([lid_inner_w, lid_inner_l, skirt_depth + 1.1], r=3.0)
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
