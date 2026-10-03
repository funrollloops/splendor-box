import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import splendor_box as sb


class TestSplendorBox(unittest.TestCase):
    def test_dimensions_valid(self):
        """Verify component dimensions and clearance parameters."""
        self.assertEqual(sb.CARD_WIDTH, 63.0)
        self.assertEqual(sb.CARD_LENGTH, 88.0)
        self.assertEqual(sb.NOBLE_WIDTH, 60.0)
        self.assertEqual(sb.NOBLE_LENGTH, 60.0)
        self.assertEqual(sb.TOKEN_DIAMETER, 43.0)
        self.assertEqual(sb.TIER1_CARD_COUNT, 40)
        self.assertEqual(sb.TIER2_CARD_COUNT, 30)
        self.assertEqual(sb.TIER3_CARD_COUNT, 20)

    def test_tray_layout_alignment(self):
        """Ensure top and bottom row module footprints match perfectly."""
        row1_w = sb.CARD_TRAY_OUTER_W * 3  # 3 Card Trays
        row2_w = sb.TOKEN_TRAY_OUTER_W + sb.NOBLE_TRAY_OUTER_W  # Token + Noble Tray
        self.assertEqual(row1_w, 202.5)
        self.assertEqual(row2_w, 202.5)

    def test_master_box_dimensions(self):
        """Ensure master box inner cavity can fit all trays with clearance."""
        self.assertGreater(sb.MASTER_INNER_W, 202.5)
        self.assertGreater(sb.MASTER_INNER_L, 185.0)
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
