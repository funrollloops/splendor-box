import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import artisanal as art
import splendor_box as sb
import travel_box as tb
import two_piece_travel as tpt


class TestSplendorBox(unittest.TestCase):
    def test_tray_layout_alignment(self):
        """Ensure top and bottom row module footprints match perfectly."""
        row1_w = sb.CARD_TRAY_OUTER_W * 3  # 3 Card Trays
        row2_w = sb.TOKEN_TRAY_OUTER_W + sb.NOBLE_TRAY_OUTER_W  # Token + Noble Tray
        self.assertEqual(row1_w, row2_w)

    def test_master_box_dimensions(self):
        """Ensure master box inner cavity can fit all trays with clearance."""
        total_w = sb.CARD_TRAY_OUTER_W * 3
        total_l = sb.CARD_TRAY_OUTER_L * 2
        self.assertGreater(sb.MASTER_INNER_W, total_w)
        self.assertGreater(sb.MASTER_INNER_L, total_l)
        self.assertGreaterEqual(sb.MASTER_INNER_H, sb.TRAY_HEIGHT)

    def test_card_trays_generation(self):
        """Verify card tray solidpython objects are created."""
        t1 = sb.generate_card_tray(1, sb.TIER1_STACK_H)
        t2 = sb.generate_card_tray(2, sb.TIER2_STACK_H)
        t3 = sb.generate_card_tray(3, sb.TIER3_STACK_H)
        self.assertIsNotNone(t1)
        self.assertIsNotNone(t2)
        self.assertIsNotNone(t3)

    def test_token_noble_trays_generation(self):
        """Verify token and noble tray objects generation."""
        tokens = sb.generate_token_tray()
        nobles = sb.generate_noble_tray()
        box = sb.generate_master_box()
        lid = sb.generate_master_lid()
        self.assertIsNotNone(tokens)
        self.assertIsNotNone(nobles)
        self.assertIsNotNone(box)
        self.assertIsNotNone(lid)

    def test_travel_box_generation(self):
        """Verify ultra-compact travel case solidpython objects."""
        base = tb.generate_lower_base()
        cards = tb.generate_card_tray()
        lid = tb.generate_travel_lid()
        assembly = tb.generate_travel_assembly()
        self.assertIsNotNone(base)
        self.assertIsNotNone(cards)
        self.assertIsNotNone(lid)
        self.assertIsNotNone(assembly)

    def test_two_piece_travel_generation(self):
        """Verify two-piece travel box solidpython objects."""
        bottom = tpt.generate_bottom_frame()
        lid = tpt.generate_top_lid()
        assembly = tpt.generate_two_piece_assembly()
        self.assertIsNotNone(bottom)
        self.assertIsNotNone(lid)
        self.assertIsNotNone(assembly)

    def test_artisanal_generation(self):
        """Verify artisanal box bottom object generation."""
        bottom = art.bottom()
        self.assertIsNotNone(bottom)
