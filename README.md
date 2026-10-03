# Splendor Board Game Component Storage Box & Organizer

A fully parametric 3D printable storage box and organizer system for **Splendor**, designed using **SolidPython2**.

---

## Features & Highlights

- **Modular Independent Deck Trays**:
  - **Tier 1 Card Tray**: Holds 40 Tier 1 cards (13.8 mm stack height).
  - **Tier 2 Card Tray**: Holds 30 Tier 2 cards (10.2 mm stack height).
  - **Tier 3 Card Tray**: Holds 20 Tier 3 cards (6.9 mm stack height).
  - *Each stack can be lifted out separately* during setup and placed directly on the play table!
  - Features dual side finger scoops, bottom finger push slots, front deck art windows, and embossed Roman numerals (`I`, `II`, `III`).

- **Gem Token Tray**:
  - Houses 6 token wells (5 gem stacks of 7 tokens @ 23.5 mm height + 1 gold stack of 5 tokens @ 16.7 mm height).
  - *Full-depth side finger channels* on both sides of every single stack allow players to pinch and pull out any token stack independently.
  - Bottom push holes for effortless stack lifting.

- **Noble Tile Tray**:
  - Holds 10 Noble tiles (60 x 60 mm x 16.62 mm stack height) with side finger access.
  - Includes an integrated utility pocket for the First Player marker or expansion tokens.

- **Master Storage Box & Fitted Lid**:
  - Accommodates all 5 removable module trays (3 Card Trays, 1 Token Tray, 1 Noble Tray) in a compact 208 mm x 191 mm x 26.5 mm footprint.
  - Keeps all components securely locked in place during transport or vertical shelf storage.

---

## Component Dimensions Reference

| Component | Quantity | Dimensions per piece | Stack Height | Clearance |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1 Cards** | 40 | 63 mm W x 88 mm L x 0.35 mm | 13.8 mm | 1.5 mm W / L |
| **Tier 2 Cards** | 30 | 63 mm W x 88 mm L x 0.35 mm | 10.2 mm | 1.5 mm W / L |
| **Tier 3 Cards** | 20 | 63 mm W x 88 mm L x 0.35 mm | 6.9 mm | 1.5 mm W / L |
| **Noble Tiles** | 10 | 60 mm W x 60 mm L x 1.70 mm | 16.62 mm | 1.5 mm W / L |
| **Gem Tokens** | 35 (5 x 7) | 43 mm Diameter x 3.3 mm | 23.50 mm | 1.2 mm Diameter |
| **Gold Tokens** | 5 | 43 mm Diameter x 3.3 mm | 16.70 mm | 1.2 mm Diameter |

---

## Parameterized SolidPython2 Variables

All parameters are located in [`src/splendor_box.py`](file:///home/sagarm/p/splendor-box/src/splendor_box.py):

```python
# Card Specifications
CARD_WIDTH = 63.0
CARD_LENGTH = 88.0
CARD_CORNER_RADIUS = 3.5

# Stack Heights
TIER1_STACK_H = 13.8
TIER2_STACK_H = 10.2
TIER3_STACK_H = 6.9

# Gem Tokens
TOKEN_DIAMETER = 43.0
GEM_STACK_H = 23.50
GOLD_STACK_H = 16.70

# Noble Tiles
NOBLE_WIDTH = 60.0
NOBLE_LENGTH = 60.0
NOBLE_STACK_H = 16.62

# Clearances & Tolerances
CARD_CLEARANCE_W = 1.5
CARD_CLEARANCE_L = 1.5
TOKEN_CLEARANCE_D = 1.2
TRAY_FIT_TOLERANCE = 0.4
```

---

## Usage Instructions

### 1. Generating OpenSCAD Files
Run `main.py` using Python / `uv`:
```bash
uv run python main.py
```
This generates all `.scad` files in the `output/` directory:
- [`output/card_tray_tier1.scad`](file:///home/sagarm/p/splendor-box/output/card_tray_tier1.scad)
- [`output/card_tray_tier2.scad`](file:///home/sagarm/p/splendor-box/output/card_tray_tier2.scad)
- [`output/card_tray_tier3.scad`](file:///home/sagarm/p/splendor-box/output/card_tray_tier3.scad)
- [`output/token_tray.scad`](file:///home/sagarm/p/splendor-box/output/token_tray.scad)
- [`output/noble_tray.scad`](file:///home/sagarm/p/splendor-box/output/noble_tray.scad)
- [`output/master_box.scad`](file:///home/sagarm/p/splendor-box/output/master_box.scad)
- [`output/master_lid.scad`](file:///home/sagarm/p/splendor-box/output/master_lid.scad)
- [`output/full_assembly.scad`](file:///home/sagarm/p/splendor-box/output/full_assembly.scad)

### 2. Running Unit Tests
```bash
uv run python -m unittest discover -s tests
```

---

## Recommended 3D Printing Settings

- **Layer Height**: 0.2 mm (or 0.16 mm for fine embossed text)
- **Infill**: 15% - 20% (Gyroid or Grid)
- **Wall Loops**: 3 walls (1.2 mm wall thickness)
- **Supports**: None required! All angles and bridges are designed overhang-free.
- **Material**: PLA or PETG
