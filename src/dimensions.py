"""
Physical dimensions and specifications for Splendor board game components.
Shared across all box organizers, travel cases, and tray generators.
"""

# ==============================================================================
# 1. Card Specifications
# ==============================================================================
CARD_WIDTH = 63.0
CARD_LENGTH = 88.0
CARD_THICKNESS = 0.35
CARD_CORNER_RADIUS = 3.5

TIER1_CARD_COUNT = 40
TIER2_CARD_COUNT = 30
TIER3_CARD_COUNT = 20
TOTAL_CARD_COUNT = 90

TIER1_STACK_H = 13.8
TIER2_STACK_H = 10.2
TIER3_STACK_H = 6.9

# ==============================================================================
# 2. Noble Tile Specifications
# ==============================================================================
NOBLE_WIDTH = 60.0
NOBLE_LENGTH = 60.0
NOBLE_THICKNESS = 1.70
NOBLE_TILE_COUNT = 10
NOBLE_STACK_H = 16.62
NOBLE_5_STACK_H = 8.5  # Stack height for 5 tiles (half set)

# ==============================================================================
# 3. Gem Token Specifications
# ==============================================================================
TOKEN_DIAMETER = 43.0
TOKEN_THICKNESS = 3.3
GEM_STACK_H = 23.50  # 7 tokens * 3.3mm (~23.5mm)
GOLD_STACK_H = 16.70  # 5 tokens * 3.3mm (~16.7mm)

GEM_TOKENS_PER_STACK = 7
GOLD_TOKENS_PER_STACK = 5
GEM_STACK_COUNT = 5
GOLD_STACK_COUNT = 1
TOTAL_TOKEN_COUNT = 40

__all__ = [
    # Card specifications
    "CARD_WIDTH",
    "CARD_LENGTH",
    "CARD_THICKNESS",
    "CARD_CORNER_RADIUS",
    "TIER1_CARD_COUNT",
    "TIER2_CARD_COUNT",
    "TIER3_CARD_COUNT",
    "TOTAL_CARD_COUNT",
    "TIER1_STACK_H",
    "TIER2_STACK_H",
    "TIER3_STACK_H",
    # Noble tile specifications
    "NOBLE_WIDTH",
    "NOBLE_LENGTH",
    "NOBLE_THICKNESS",
    "NOBLE_TILE_COUNT",
    "NOBLE_STACK_H",
    "NOBLE_5_STACK_H",
    # Gem token specifications
    "TOKEN_DIAMETER",
    "TOKEN_THICKNESS",
    "GEM_STACK_H",
    "GOLD_STACK_H",
    "GEM_TOKENS_PER_STACK",
    "GOLD_TOKENS_PER_STACK",
    "GEM_STACK_COUNT",
    "GOLD_STACK_COUNT",
    "TOTAL_TOKEN_COUNT",
]
