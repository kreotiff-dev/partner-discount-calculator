import unittest

from partner_discount_service import PARTNER_TOTAL_QUANTITY_QUERY
from partner_discount_service import get_partner_with_discount


class FakeCursor:
    def __init__(self, row: tuple[int, str, int] | None) -> None:
        self.row = row
        self.parameters: tuple[int] | None = None
        self.query = ""

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        return None

    def execute(self, query: str, parameters: tuple[int]) -> None:
        self.query = query
        self.parameters = parameters

    def fetchone(self) -> tuple[int, str, int] | None:
        return self.row


class FakeConnection:
    def __init__(self, row: tuple[int, str, int] | None) -> None:
        self.cursor_instance = FakeCursor(row)

    def cursor(self) -> FakeCursor:
        return self.cursor_instance


class PartnerDiscountServiceTests(unittest.TestCase):
    def test_returns_partner_data_with_discount(self) -> None:
        database_connection = FakeConnection((7, "ООО Тест", 50_000))

        partner = get_partner_with_discount(7, database_connection)

        self.assertEqual(partner["partner_id"], 7)
        self.assertEqual(partner["partner_name"], "ООО Тест")
        self.assertEqual(partner["total_quantity"], 50_000)
        self.assertEqual(partner["discount_percent"], 10)
        self.assertEqual(database_connection.cursor_instance.parameters, (7,))

    def test_returns_none_for_missing_partner(self) -> None:
        database_connection = FakeConnection(None)

        partner = get_partner_with_discount(404, database_connection)

        self.assertIsNone(partner)

    def test_query_uses_sum_and_left_join(self) -> None:
        normalized_query = PARTNER_TOTAL_QUANTITY_QUERY.lower()

        self.assertIn("sum(di.quantity)", normalized_query)
        self.assertIn("left join deliveries", normalized_query)
        self.assertIn("left join delivery_items", normalized_query)
