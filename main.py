"""
Main entry script to generate OpenSCAD (.scad) and STL files for:
1. Two-Piece Ultra-Compact Splendor Travel Case (Bottom Frame + Top Lid)
2. Full Modular Splendor Desktop Organizer System
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import artisanal as art
import splendor_box as sb
import travel_box as tb
import two_piece_travel as tpt

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("==================================================")
    print("   SPLENDOR STORAGE & TRAVEL BOX GENERATOR       ")
    print("==================================================")
    print(f"Output directory: {OUTPUT_DIR}\n")

    models = {
        # 1. Two-Piece Ultra-Compact Travel Case (Primary 2-piece design)
        "two_piece_bottom": tpt.generate_bottom_frame(),
        "two_piece_lid": tpt.generate_top_lid(),
        "two_piece_assembly": tpt.generate_two_piece_assembly(),
        # 2. Travel Box Models
        "travel_base": tb.generate_lower_base(),
        "travel_card_tray": tb.generate_card_tray(),
        "travel_lid": tb.generate_travel_lid(),
        "travel_assembly": tb.generate_travel_assembly(),
        # 3. Full Modular Desktop Box Models
        "card_tray_tier1": sb.generate_card_tray(1, sb.TIER1_STACK_H),
        "card_tray_tier2": sb.generate_card_tray(2, sb.TIER2_STACK_H),
        "card_tray_tier3": sb.generate_card_tray(3, sb.TIER3_STACK_H),
        "token_tray": sb.generate_token_tray(),
        "noble_tray": sb.generate_noble_tray(),
        "master_box": sb.generate_master_box(),
        "master_lid": sb.generate_master_lid(),
        "full_assembly": sb.generate_full_assembly(),
        # 4. Artisanal Box Models
        "artisanal_bottom": art.bottom(),
        "artisanal_lid": art.lid(),
        "artisanal_cover": art.cover(),
        "artisanal_assembly": art.assembly(),
    }

    for name, obj in models.items():
        scad_path = os.path.join(OUTPUT_DIR, f"{name}.scad")
        sb.scad_render_to_file(obj, scad_path)
        print(f" [+] Generated OpenSCAD file: {scad_path}")

    print("\nAll OpenSCAD (.scad) models successfully generated.")


if __name__ == "__main__":
    main()
