# Splendor Board Game Component Storage & Travel Box System

A fully parametric 3D printable storage box, tabletop organizer, and ultra-compact travel case system for **Splendor**, designed using **SolidPython2**.

---

## 2-Piece Ultra-Compact Travel Solution ([`src/two_piece_travel.py`](file:///home/sagarm/p/splendor-box/src/two_piece_travel.py))

Designed for maximum space efficiency, lightweight material usage, and zero rubber bands. Consists of **exactly 2 printable parts**:

1. **Bottom Skeletal Tray ([`output/two_piece_bottom.stl`](file:///home/sagarm/p/splendor-box/output/two_piece_bottom.stl))**:
   - **Noble Layer (Bottom Left)**: Stores 10 Noble tiles (60x60mm x 16.62mm height) at the bottom.
   - **Tier 1 Card Shelf (Top Left)**: Tier 1 deck (40 cards, 13.8mm) sits directly on top of the Noble tiles.
   - **Gem Token Layer (Bottom Right)**: 6 token stacks arranged in a 2x3 grid with open skeleton retaining posts for maximum finger clearance.
   - **Tier 2 & 3 Card Shelves (Top Right)**: Tier 2 deck (30 cards) and Tier 3 deck (20 cards) sit directly on top of the gem token stacks.
   - **Rounded U-shaped Finger Scoops**: Generous finger cutouts on all 3 card decks and token stacks.

2. **Top Enclosing Lid ([`output/two_piece_lid.stl`](file:///home/sagarm/p/splendor-box/output/two_piece_lid.stl))**:
   - Encloses the loaded skeletal tray completely, holding cards, tokens, and noble tiles flush in place.
   - Integrated side snap tabs click into exterior base detents to lock the box securely without rubber bands.

---

## Systems & Features

### 1. Two-Piece Travel Case ([`src/two_piece_travel.py`](file:///home/sagarm/p/splendor-box/src/two_piece_travel.py))
*Footprint: ~202 x 92 x 36 mm. 2 parts total.*

### 2. Multi-Tray Travel Case ([`src/travel_box.py`](file:///home/sagarm/p/splendor-box/src/travel_box.py))
*Footprint: ~199 x 92 x 43 mm. 3 parts total.*

### 3. Full Tabletop Organizer System ([`src/splendor_box.py`](file:///home/sagarm/p/splendor-box/src/splendor_box.py))
*Footprint: ~208 x 191 x 26.5 mm. 7 parts total.*

---

## Component Dimensions Reference

| Component | Quantity | Dimensions per piece | Stack Height | Clearance |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1 Cards** | 40 | 63 mm W x 88 mm L x 0.35 mm | 13.8 mm | 1.4 mm W / L |
| **Tier 2 Cards** | 30 | 63 mm W x 88 mm L x 0.35 mm | 10.2 mm | 1.4 mm W / L |
| **Tier 3 Cards** | 20 | 63 mm W x 88 mm L x 0.35 mm | 6.9 mm | 1.4 mm W / L |
| **Noble Tiles** | 10 | 60 mm W x 60 mm L x 1.70 mm | 16.62 mm | 1.4 mm W / L |
| **Gem Tokens** | 35 (5 x 7) | 43 mm Diameter x 3.3 mm | 23.50 mm | 1.2 mm Diameter |
| **Gold Tokens** | 5 | 43 mm Diameter x 3.3 mm | 16.70 mm | 1.2 mm Diameter |

---

## Makefile Commands

```bash
# Build everything (.scad scripts + .stl 3D models)
make all

# Render OpenSCAD (.scad) scripts
make scad

# Compile .stl 3D printable files
make stl

# Run unit test suite
make test

# Format Python files with Ruff
make format

# Clean output build directory
make clean
```
