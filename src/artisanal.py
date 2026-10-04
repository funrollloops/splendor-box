import solid2 as s

try:
    import dimensions as d
except ImportError:
    from . import dimensions as d

CARD_RADIUS = d.CARD_CORNER_RADIUS
FUDGE = 0.01  # Avoid co-planar surfaces
WALL_THICKNESS = 1.5  # Thickness of the box walls
B_INNER_WIDTH = max(d.CARD_WIDTH, d.NOBLE_WIDTH) + max(
    d.CARD_WIDTH * 2, d.TOKEN_DIAMETER * 3
)
B_OUTER_WIDTH = B_INNER_WIDTH + WALL_THICKNESS * 2
B_INNER_LENGTH = d.CARD_LENGTH
B_OUTER_LENGTH = B_INNER_LENGTH + WALL_THICKNESS * 2
B_INNER_HEIGHT = max(
    d.TIER1_STACK_H + d.NOBLE_STACK_H, d.GEM_STACK_H + d.TIER2_STACK_H
)
B_OUTER_HEIGHT = B_INNER_HEIGHT + WALL_THICKNESS
BOX_RADIUS = WALL_THICKNESS # CARD_RADIUS


def rounded_rectangle(w, l, h, r):
    """Create a rounded rectangle with the given width, length, a height of 1, and corner radius at (0, 0)."""
    return s.hull()(
        s.translate([r, r, 0])(s.cylinder(r=r, h=h)),
        s.translate([w - r, r, 0])(s.cylinder(r=r, h=h)),
        s.translate([w - r, l - r, 0])(s.cylinder(r=r, h=h)),
        s.translate([r, l - r, 0])(s.cylinder(r=r, h=h)),
    )


def tokens(h):
    """Edge aligned at 0, 0"""
    r = d.TOKEN_RADIUS
    token = s.cylinder(r=d.TOKEN_RADIUS, h=h + FUDGE)
    l = [
        s.translate([x * r * 2, y * r * 2, 0])(token)
        for x in range(3)
        for y in range(2)
    ]

    cutout_ratio = 0.7
    # Unused rectangle cutout; disc used instead cause it's cool.
    rectangle_cutout = s.translate(
        [
            d.TOKEN_DIAMETER * (1 - cutout_ratio),
            d.TOKEN_DIAMETER * (1 - cutout_ratio),
            0,
        ]
    )(
        s.cube(
            d.TOKEN_DIAMETER * 2 * cutout_ratio + d.TOKEN_DIAMETER,
            d.TOKEN_DIAMETER * 2 * cutout_ratio,
            d.GEM_STACK_H + FUDGE,
            center=False,
        )
    )
    disc_cutouts = s.union()(
        *(
            s.translate(x * d.TOKEN_DIAMETER, d.TOKEN_DIAMETER, 0)(
                s.cylinder(r=d.TOKEN_RADIUS * cutout_ratio, h=h + FUDGE)
            )
            for x in range(0, 3)
        )
    )
    return s.union()(s.translate([r, r, 0])(s.union()(*l)), disc_cutouts)


def card_stack(h):
    """Create a stack of cards with the given height."""
    return rounded_rectangle(
        d.CARD_WIDTH + FUDGE, d.CARD_LENGTH, h + FUDGE, CARD_RADIUS
    )


def rounded_box_except_top(w, l, h, r):
    """Create a rounded box with the given width, length, height, and corner radius at (0, 0)."""
    corner = s.union()(s.sphere(r=r), s.cylinder(r=r, h=h - r))
    return s.hull()(
        s.translate([r, r, r])(corner),
        s.translate([w - r, r, r])(corner),
        s.translate([w - r, l - r, r])(corner),
        s.translate([r, l - r, r])(corner),
    )


def rounded_box(w, l, h, r):
    """Create a rounded box with the given width, length, height, and corner radius at (0, 0)."""
    corner = s.union()(
        s.sphere(r=r), s.translate(0, 0, h - 2 * r)(s.sphere(r=r))
    )
    return s.hull()(
        s.translate([r, r, r])(corner),
        s.translate([w - r, r, r])(corner),
        s.translate([w - r, l - r, r])(corner),
        s.translate([r, l - r, r])(corner),
    )


def scoop(thickness, r):
    return s.rotate(-90, 0, 0)(s.cylinder(r=r, h=thickness + FUDGE))


def bottom():
    """At the bottom of the box, nobles on the left and gems on the
    right. On the next layer up, the three stacks of cards."""

    WT = WALL_THICKNESS
    card_spacing = d.CARD_WIDTH + (B_INNER_WIDTH - d.CARD_WIDTH * 3) / 2

    b_outer = s.translate([-WT, -WT, -WT])(
        rounded_box(
            B_OUTER_WIDTH,
            B_OUTER_LENGTH,
            B_OUTER_HEIGHT - FUDGE,
            BOX_RADIUS,
        )
    )

    nobles = rounded_rectangle(
        d.NOBLE_WIDTH, d.NOBLE_LENGTH, d.NOBLE_STACK_H + FUDGE, CARD_RADIUS
    )

    gem_y_offset = (d.CARD_LENGTH - d.TOKEN_DIAMETER * 2) / 2
    noble_x_offset = (d.CARD_WIDTH - d.NOBLE_WIDTH) / 2
    noble_y_offset = (d.CARD_LENGTH - d.NOBLE_LENGTH) / 2

    tier1_slot_height = B_INNER_HEIGHT - d.NOBLE_STACK_H
    assert tier1_slot_height >= d.TIER1_STACK_H
    tier2_slot_height = B_INNER_HEIGHT - d.GEM_STACK_H
    assert tier2_slot_height >= d.TIER2_STACK_H
    assert tier2_slot_height >= d.TIER3_STACK_H

    card_scoops = [
        s.translate([card_spacing * i + d.CARD_WIDTH / 2, y, B_INNER_HEIGHT])(
            scoop(
                WT + 2 * FUDGE,
                (tier2_slot_height if i else tier1_slot_height) + 3,
            )
        )
        for i in range(3)
        for y in (-WT - FUDGE, B_INNER_LENGTH - FUDGE)
    ]

    # Noble scoops, not used because gem scoops work for nobles too!
    noble_scoops = [
        s.translate(d.CARD_WIDTH / 2, noble_y_offset, d.NOBLE_STACK_H)(
            s.scale(d.NOBLE_STACK_H, noble_y_offset - WT, d.NOBLE_STACK_H)(
                s.sphere()
            )
        ),
        s.translate(
            d.CARD_WIDTH / 2, noble_y_offset + d.NOBLE_LENGTH, d.NOBLE_STACK_H
        )(
            s.scale(d.NOBLE_STACK_H, noble_y_offset - WT, d.NOBLE_STACK_H)(
                s.sphere()
            )
        ),
    ]

    return s.difference()(
        s.union()(b_outer),
        # Nobles, centered under the tier 1 card stack.
        s.translate(
            [
                noble_x_offset,
                noble_y_offset,
                0,
            ]
        )(nobles),
        # Scoops for the nobles, centered under the tier 1 card stack.
        # Gems, centered under the tier 2 and 3 card stacks.
        s.translate([d.CARD_WIDTH, gem_y_offset, 0])(tokens(d.GEM_STACK_H)),
        # Card slots.
        s.translate([0, 0, d.NOBLE_STACK_H])(card_stack(tier1_slot_height)),
        s.translate([card_spacing, 0, d.GEM_STACK_H])(
            card_stack(tier2_slot_height)
        ),
        s.translate([card_spacing * 2, 0, d.GEM_STACK_H])(
            card_stack(tier2_slot_height)
        ),
        *card_scoops,
        # Cutout for card dividers so gem stacks are not obstructed.
        s.translate([BOX_RADIUS, gem_y_offset, d.GEM_STACK_H])(
            s.cube(
                B_INNER_WIDTH - 2 * BOX_RADIUS,
                B_INNER_LENGTH - 2 * gem_y_offset,
                tier2_slot_height,
                center=False,
            )
        ),
    )

def cover():
    """The top of the box, with a lip to hold the lid in place."""
    WT = WALL_THICKNESS
    return s.difference()(
        s.translate([-WT, -WT, -WT])(
            rounded_box(
                B_OUTER_WIDTH + 2 * WT,
                B_OUTER_LENGTH + 2 * WT,
                B_OUTER_HEIGHT + WT,
                BOX_RADIUS,
            )
        ),
        rounded_box_except_top(B_OUTER_WIDTH, B_OUTER_LENGTH, B_OUTER_HEIGHT + FUDGE, BOX_RADIUS)
    )


def lid():
  """Rather than a full-height cover, this is a shallow lid that
  locks into the box with tabs."""
  pass
