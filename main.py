"""
Main entry point to generate OpenSCAD (.scad) and STL files
for the Splendor Storage Box system using solidpython2.
"""

import os
import sys
import subprocess

# Ensure src/ directory is on Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import splendor_box as sb

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("==================================================")
    print("   SPLENDOR COMPONENT STORAGE BOX GENERATOR       ")
    print("==================================================")
    print(f"Output directory: {OUTPUT_DIR}\n")

    models = {
        "card_tray_tier1": sb.generate_card_tray(1, sb.TIER1_STACK_H),
        "card_tray_tier2": sb.generate_card_tray(2, sb.TIER2_STACK_H),
        "card_tray_tier3": sb.generate_card_tray(3, sb.TIER3_STACK_H),
        "token_tray": sb.generate_token_tray(),
        "noble_tray": sb.generate_noble_tray(),
        "master_box": sb.generate_master_box(),
        "master_lid": sb.generate_master_lid(),
        "full_assembly": sb.generate_full_assembly(),
    }

    for name, obj in models.items():
        scad_path = os.path.join(OUTPUT_DIR, f"{name}.scad")
        sb.scad_render_to_file(obj, scad_path)
        print(f" [+] Generated OpenSCAD file: {scad_path}")

    print("\nAll OpenSCAD (.scad) models successfully generated.")


if __name__ == "__main__":
    main()
