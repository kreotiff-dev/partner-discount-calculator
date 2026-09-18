import unittest

from discount import calculate_partner_discount


class CalculatePartnerDiscountTests(unittest.TestCase):
    def test_discount_is_zero_below_first_threshold(self) -> None:
        self.assertEqual(calculate_partner_discount(9_999), 0)

    def test_discount_is_five_at_first_threshold(self) -> None:
        self.assertEqual(calculate_partner_discount(10_000), 5)

    def test_discount_is_five_at_second_threshold_minus_one(self) -> None:
        self.assertEqual(calculate_partner_discount(49_999), 5)

    def test_discount_is_ten_at_second_threshold(self) -> None:
        self.assertEqual(calculate_partner_discount(50_000), 10)

    def test_discount_is_fifteen_at_third_threshold(self) -> None:
        self.assertEqual(calculate_partner_discount(300_000), 15)
